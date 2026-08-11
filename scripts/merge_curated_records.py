#!/usr/bin/env python3
"""Merge manually evidence-checked records into the catalog authority."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def normalized_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.casefold())


def author_keys(names: list[str]) -> set[str]:
    keys = set()
    for name in names:
        tokens = re.findall(r"[a-z0-9]+", name.casefold())
        if tokens:
            keys.add(tokens[-1])
    return keys


def corroborated_title_match(existing: dict, candidate: dict) -> bool:
    return (
        existing.get("year") == candidate.get("year")
        and bool(author_keys(existing.get("authors") or []) & author_keys(candidate.get("authors") or []))
    )


def evidence_block(status: str, summary: str, source_url: str, locator: str) -> dict:
    return {
        "status": status,
        "summary": summary,
        "evidence": {"source_url": source_url, "locator": locator},
    }


def expand(item: dict, checked_on: str) -> dict:
    primary_url = item["primary_url"]
    evidence_level = item.get("evidence_level")
    default_locators = {
        "metadata-only": "metadata",
        "abstract": "abstract",
        "full-text": "full text",
        "project-page": "primary source",
    }
    locator = item.get("evidence_locator") or default_locators.get(evidence_level, "primary source")
    code = item.get("code") or {}
    dataset = item.get("dataset") or {}
    evaluation = item.get("evaluation") or {}
    baselines = item.get("baselines") or {}
    metadata_only = evidence_level == "metadata-only"
    scenario_locator = "title" if metadata_only else locator
    scenario_status = item.get("scenario_status") or ("inferred_from_title" if metadata_only else "reported")
    problem_status = item.get("problem_status") or ("inferred_from_title" if metadata_only else "reported")
    doi_url = primary_url if "doi.org/" in primary_url else item.get("doi_url", "")
    arxiv_url = primary_url if "arxiv.org/" in primary_url else item.get("arxiv_url", "")
    record = {
        "id": item["id"],
        "title": item["title"],
        "authors": item.get("authors") or [],
        "year": item["year"],
        "venue": item["venue"],
        "publication_state": item["publication_state"],
        "primary_url": primary_url,
        "urls": {
            "doi": doi_url,
            "arxiv": arxiv_url,
            "open_access_pdf": item.get("open_access_pdf", ""),
            "code": code.get("url", ""),
            "data": dataset.get("url", ""),
        },
        "scope": item["scope"],
        "topics": item["topics"],
        "primary_topic": item["primary_topic"],
        "top_venue": item.get("top_venue"),
        "code": {
            **evidence_block(
                code.get("status", "not_found"),
                code.get("summary", "No verified public code repository was found."),
                code.get("evidence_url", primary_url),
                code.get("locator", locator),
            ),
            "url": code.get("url", ""),
            "checked_on": checked_on,
        },
        "dataset": {
            **evidence_block(
                dataset.get("status", "not_reported_in_accessible_source"),
                dataset.get("summary", "The accessible sources do not report a dataset or data source."),
                dataset.get("evidence_url", primary_url),
                dataset.get("locator", locator),
            ),
            "names": dataset.get("names") or [],
        },
        "application_scenario": evidence_block(
            scenario_status,
            item["application_scenario"],
            item.get("scenario_evidence_url", primary_url),
            scenario_locator,
        ),
        "problem_solved": evidence_block(
            problem_status,
            item["problem_solved"],
            item.get("problem_evidence_url", primary_url),
            scenario_locator,
        ),
        "evaluation": {
            **evidence_block(
                evaluation.get("status", "not_reported_in_accessible_source"),
                evaluation.get("summary", "The accessible sources do not report final tests."),
                evaluation.get("evidence_url", primary_url),
                evaluation.get("locator", locator),
            ),
            "metrics_mentioned": evaluation.get("metrics") or [],
        },
        "baselines": {
            **evidence_block(
                baselines.get("status", "not_reported_in_accessible_source"),
                baselines.get("summary", "The accessible sources do not list a baseline."),
                baselines.get("evidence_url", primary_url),
                baselines.get("locator", locator),
            ),
            "names": baselines.get("names") or [],
        },
        "evidence_level": item["evidence_level"],
        "verification": {
            "checked_on": checked_on,
            "sources": list(dict.fromkeys([primary_url] + (item.get("verification_sources") or []))),
            "requested_id": item["id"],
            "note": item.get("verification_note", "Curated from primary paper/project evidence."),
        },
    }
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--checked-on", default="2026-08-11")
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    manual = json.loads(args.records.read_text(encoding="utf-8"))
    existing = {paper["id"]: paper for paper in catalog["papers"]}
    title_to_id = {normalized_title(paper["title"]): paper["id"] for paper in catalog["papers"]}
    replaced = 0
    added = 0
    for item in manual["records"]:
        record = expand(item, args.checked_on)
        record_title_key = normalized_title(record["title"])
        prior_id = record["id"] if record["id"] in existing else None
        title_match_id = title_to_id.get(record_title_key)
        if title_match_id is not None and title_match_id != prior_id:
            title_match = existing[title_match_id]
            if prior_id is not None or not corroborated_title_match(title_match, record):
                raise RuntimeError(
                    "Unsafe normalized-title collision for curated record "
                    f"{record['id']}: existing={title_match_id}"
                )
            prior_id = title_match_id
        if prior_id:
            prior = existing[prior_id]
            if prior.get("top_venue") and record.get("top_venue") not in {None, prior["top_venue"]}:
                raise RuntimeError(
                    f"Conflicting top venue for {prior_id}: {prior.get('top_venue')} vs {record.get('top_venue')}"
                )
            if record.get("top_venue") is None:
                record["top_venue"] = prior.get("top_venue")
            record["verification"]["sources"] = list(
                dict.fromkeys((prior.get("verification") or {}).get("sources", []) + record["verification"]["sources"])
            )
            prior_title_key = normalized_title(prior["title"])
            if title_to_id.get(prior_title_key) == prior_id:
                title_to_id.pop(prior_title_key)
            existing.pop(prior_id, None)
            replaced += 1
        else:
            added += 1
        existing[record["id"]] = record
        title_to_id[record_title_key] = record["id"]
    catalog["papers"] = sorted(
        existing.values(),
        key=lambda paper: (paper["scope"], -(paper.get("year") or 0), paper["primary_topic"], paper["title"].casefold()),
    )
    args.catalog.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"added": added, "replaced": replaced, "total": len(catalog["papers"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
