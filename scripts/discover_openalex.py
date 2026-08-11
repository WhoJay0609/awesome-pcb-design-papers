#!/usr/bin/env python3
"""Discover PCB-design literature candidates through the OpenAlex API.

This is a discovery aid, not the catalog authority. Every admitted record is
reviewed and linked to a DOI, publisher, conference, or arXiv page in
``data/papers.json``.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


API_URL = "https://api.openalex.org/works"
QUERY_SPECS = {
    "placement": [
        "printed circuit board component placement",
        "PCB placement optimization",
        "PCB layout placement",
    ],
    "routing": [
        "printed circuit board routing",
        "PCB autorouting",
        "PCB length matching routing",
        "PCB escape routing",
    ],
    "ai-eda": [
        "printed circuit board machine learning design",
        "PCB reinforcement learning placement routing",
        "large language model PCB design",
    ],
    "schematic-design": [
        "PCB schematic design automation",
        "printed circuit board netlist design",
        "PCB component selection automation",
    ],
    "si-pi-emc": [
        "PCB signal integrity design",
        "PCB power integrity design",
        "printed circuit board electromagnetic compatibility design",
    ],
    "thermal-reliability": [
        "PCB thermal design optimization",
        "printed circuit board reliability design",
        "PCB thermo mechanical design",
    ],
    "dfm-manufacturing": [
        "PCB design for manufacturability",
        "printed circuit board manufacturing optimization design",
        "PCB assembly optimization",
    ],
    "testing-inspection": [
        "PCB design for testability",
        "printed circuit board inspection design feedback",
        "PCB defect detection manufacturing",
    ],
    "benchmarks-tools": [
        "PCB design benchmark dataset",
        "open source PCB design automation",
        "printed circuit board EDA tool",
    ],
}

BOARD_TERMS = re.compile(
    r"\b(?:pcb|pcbs|pcba|printed[ -]circuit board|printed wiring board|"
    r"circuit board|package substrate)\b",
    re.IGNORECASE,
)


def reconstruct_abstract(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    ordered = sorted(
        ((position, token) for token, positions in index.items() for position in positions),
        key=lambda item: item[0],
    )
    return " ".join(token for _, token in ordered)


def normalized_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.casefold())


def best_url(work: dict) -> str:
    if work.get("doi"):
        return work["doi"]
    location = work.get("primary_location") or {}
    if location.get("landing_page_url"):
        return location["landing_page_url"]
    for location in work.get("locations") or []:
        if location.get("landing_page_url"):
            return location["landing_page_url"]
    return work.get("id", "")


def fetch(query: str, per_page: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "search": query,
            "per-page": per_page,
            "select": (
                "id,doi,title,publication_year,publication_date,type,authorships,"
                "primary_location,locations,abstract_inverted_index,keywords,topics,"
                "cited_by_count"
            ),
        }
    )
    request = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={"User-Agent": "awesome-pcb-design-papers/1.0 (literature discovery)"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = json.load(response)
    return payload.get("results", [])


def compact(work: dict, query_topic: str, query: str) -> dict:
    source = ((work.get("primary_location") or {}).get("source") or {})
    return {
        "openalex_id": work.get("id", ""),
        "doi": work.get("doi", ""),
        "title": work.get("title", "").strip(),
        "year": work.get("publication_year"),
        "publication_date": work.get("publication_date"),
        "venue": source.get("display_name", ""),
        "type": work.get("type", ""),
        "url": best_url(work),
        "authors": [
            (entry.get("author") or {}).get("display_name", "")
            for entry in work.get("authorships") or []
            if (entry.get("author") or {}).get("display_name")
        ],
        "abstract": reconstruct_abstract(work.get("abstract_inverted_index")),
        "keywords": [entry.get("display_name", "") for entry in work.get("keywords") or []],
        "openalex_topics": [entry.get("display_name", "") for entry in work.get("topics") or []],
        "cited_by_count": work.get("cited_by_count", 0),
        "query_topics": [query_topic],
        "queries": [query],
    }


def merge(existing: dict, incoming: dict) -> None:
    existing["query_topics"] = sorted(set(existing["query_topics"] + incoming["query_topics"]))
    existing["queries"] = sorted(set(existing["queries"] + incoming["queries"]))
    if not existing.get("abstract") and incoming.get("abstract"):
        existing["abstract"] = incoming["abstract"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-query", type=int, default=100)
    parser.add_argument("--include-weak", action="store_true")
    args = parser.parse_args()

    candidates: dict[str, dict] = {}
    query_log = []
    for topic, queries in QUERY_SPECS.items():
        for query in queries:
            works = fetch(query, args.per_query)
            admitted = 0
            for work in works:
                item = compact(work, topic, query)
                evidence_text = f"{item['title']} {item['abstract']}"
                if not args.include_weak and not BOARD_TERMS.search(evidence_text):
                    continue
                key = item["doi"].casefold() if item["doi"] else normalized_title(item["title"])
                if not key:
                    continue
                if key in candidates:
                    merge(candidates[key], item)
                else:
                    candidates[key] = item
                admitted += 1
            query_log.append(
                {"topic": topic, "query": query, "returned": len(works), "board_term_hits": admitted}
            )
            time.sleep(0.1)

    records = sorted(
        candidates.values(),
        key=lambda item: (
            -(item.get("year") or 0),
            -len(item.get("query_topics") or []),
            -(item.get("cited_by_count") or 0),
            item.get("title", "").casefold(),
        ),
    )
    output = {
        "source": "OpenAlex discovery API",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "query_log": query_log,
        "candidate_count": len(records),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(records)} candidates to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
