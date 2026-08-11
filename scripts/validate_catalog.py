#!/usr/bin/env python3
"""Validate catalog structure, scope thresholds, and top-venue audit closure."""

from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


TOP_VENUES = {"DAC", "ICCAD", "DATE", "ASP-DAC", "ISPD", "ECTC", "EPEPS"}
SCHEMA_VERSION = "2.0.0"
EVIDENCE_LEVELS = {"metadata-only", "abstract", "full-text", "project-page"}
OPEN_CODE_STATUSES = {"open", "partial_open", "utility_open", "open_archived"}
OPEN_DATA_STATUSES = {"open"}
REQUIRED_BLOCKS = (
    "code",
    "dataset",
    "application_scenario",
    "problem_solved",
    "evaluation",
    "baselines",
    "verification",
)
REQUIRED_PAPER_FIELDS = {
    "id",
    "title",
    "authors",
    "year",
    "venue",
    "publication_state",
    "primary_url",
    "urls",
    "scope",
    "topics",
    "primary_topic",
    "top_venue",
    "code",
    "dataset",
    "application_scenario",
    "problem_solved",
    "evaluation",
    "baselines",
    "evidence_level",
    "verification",
}
NON_ENGLISH_SCRIPT_MARKERS = (
    "BOPOMOFO",
    "CJK",
    "HANGUL",
    "HANGZHOU",
    "HIRAGANA",
    "IDEOGRAPH",
    "KANGXI",
    "KATAKANA",
    "KHITAN",
    "NUSHU",
    "TANGUT",
    "YI RADICAL",
    "YI SYLLABLE",
)
NON_ENGLISH_CODEPOINT_RANGES = (
    (0x1100, 0x11FF),
    (0x2E80, 0x33FF),
    (0x3400, 0x9FFF),
    (0xA000, 0xA4CF),
    (0xA960, 0xA97F),
    (0xAC00, 0xD7FF),
    (0xF900, 0xFAFF),
    (0xFE10, 0xFE4F),
    (0xFF65, 0xFF9F),
    (0x16FE0, 0x18DFF),
    (0x1AFF0, 0x1B2FF),
    (0x1F200, 0x1F2FF),
    (0x20000, 0x33FFF),
)
HUMANIZER_PUNCTUATION = re.compile(r"[\u2013\u2014\u2018\u2019\u201c\u201d]")


def normalized_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.casefold())


def valid_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def contains_non_english_script(value: str) -> bool:
    for character in value:
        if ord(character) < 128:
            continue
        codepoint = ord(character)
        if any(start <= codepoint <= end for start, end in NON_ENGLISH_CODEPOINT_RANGES):
            return True
        name = unicodedata.name(character, "")
        if any(marker in name for marker in NON_ENGLISH_SCRIPT_MARKERS):
            return True
        if character.isalpha() and not name.startswith("LATIN "):
            return True
    return False


def string_list(value: object, *, require_items: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not require_items or bool(value))
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def valid_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def canonical_doi(value: object) -> str:
    if not isinstance(value, str):
        return ""
    doi = value.strip().casefold()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi)
    return doi.removeprefix("doi:")


def as_dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path, nargs="?", default=Path("data/papers.json"))
    parser.add_argument("--audit", type=Path, default=Path("data/top_venue_audit.json"))
    parser.add_argument("--link-report", type=Path, default=Path("analysis/link_check.json"))
    parser.add_argument("--require-audit", action="store_true")
    args = parser.parse_args()

    payload = json.loads(args.catalog.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        print(json.dumps({"papers": 0, "pcb_core": 0, "related_eda": 0, "errors": 1}, indent=2))
        print("ERROR: catalog: root must be an object")
        return 1
    papers = payload.get("papers") or []
    errors = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"catalog: schema_version must be {SCHEMA_VERSION}")
    for field in ("cutoff_date", "topics", "papers"):
        if field not in payload:
            errors.append(f"catalog: missing required top-level field {field}")
    if not isinstance(papers, list):
        errors.append("catalog: papers must be a list")
        papers = []
    raw_topics = payload.get("topics") or []
    if not isinstance(raw_topics, list):
        errors.append("catalog: topics must be a list")
        raw_topics = []
    topic_ids = {
        topic["id"]
        for topic in raw_topics
        if isinstance(topic, dict) and isinstance(topic.get("id"), str) and topic["id"]
    }
    if len(topic_ids) != len(raw_topics):
        errors.append("catalog: every topic must be an object with a unique non-empty string id")
    if len(raw_topics) < 8:
        errors.append("catalog: topics must contain at least 8 entries")
    for index, topic in enumerate(raw_topics):
        if not isinstance(topic, dict):
            continue
        for field in ("id", "name"):
            if not isinstance(topic.get(field), str) or not topic[field]:
                errors.append(f"catalog: topic {index} {field} must be a non-empty string")
        name = topic.get("name")
        if isinstance(name, str) and contains_non_english_script(name):
            errors.append(f"catalog: topic {index} name must be English")
        if isinstance(name, str) and HUMANIZER_PUNCTUATION.search(name):
            errors.append(f"catalog: topic {index} name contains disallowed punctuation")
    seen_ids = set()
    seen_titles = set()
    for index, paper in enumerate(papers):
        if not isinstance(paper, dict):
            errors.append(f"index {index}: paper must be an object")
            continue
        missing_fields = sorted(REQUIRED_PAPER_FIELDS - paper.keys())
        if missing_fields:
            errors.append(f"index {index}: missing required fields {', '.join(missing_fields)}")
        raw_id = paper.get("id")
        label = raw_id if isinstance(raw_id, str) and raw_id else f"index {index}"
        for field in (
            "id",
            "title",
            "authors",
            "year",
            "venue",
            "publication_state",
            "primary_url",
            "urls",
            "scope",
            "topics",
            "primary_topic",
            "evidence_level",
        ):
            if paper.get(field) in (None, "", []):
                errors.append(f"{label}: missing {field}")
        if label in seen_ids:
            errors.append(f"{label}: duplicate id")
        seen_ids.add(label)
        for field in ("id", "title", "venue", "publication_state", "scope", "primary_topic", "evidence_level"):
            if not isinstance(paper.get(field), str) or not paper.get(field):
                errors.append(f"{label}: {field} must be a non-empty string")
        title = paper.get("title") if isinstance(paper.get("title"), str) else ""
        if html.unescape(title) != title:
            errors.append(f"{label}: title contains an HTML entity")
        title_key = normalized_title(title)
        if title_key in seen_titles:
            errors.append(f"{label}: duplicate normalized title")
        seen_titles.add(title_key)
        if not valid_url(paper.get("primary_url", "")):
            errors.append(f"{label}: primary_url must be HTTPS")
        if not string_list(paper.get("authors"), require_items=True):
            errors.append(f"{label}: authors must be a non-empty string list")
        raw_urls = paper.get("urls")
        if not isinstance(raw_urls, dict):
            errors.append(f"{label}: urls must be an object")
        urls = as_dict(raw_urls)
        for url_name in ("doi", "arxiv", "open_access_pdf", "code", "data"):
            url_value = urls.get(url_name)
            if not isinstance(url_value, str) or (url_value and not valid_url(url_value)):
                errors.append(f"{label}: urls.{url_name} must be empty or HTTPS")
        scope = paper.get("scope")
        if not isinstance(scope, str) or scope not in {"pcb-core", "related-eda"}:
            errors.append(f"{label}: invalid scope")
        if not string_list(paper.get("topics"), require_items=True):
            errors.append(f"{label}: topics must be a non-empty string list")
        elif not set(paper["topics"]).issubset(topic_ids):
            errors.append(f"{label}: unknown topic")
        primary_topic = paper.get("primary_topic")
        if not isinstance(primary_topic, str) or primary_topic not in topic_ids:
            errors.append(f"{label}: invalid primary_topic")
        elif string_list(paper.get("topics"), require_items=True) and primary_topic not in paper["topics"]:
            errors.append(f"{label}: primary_topic must be included in topics")
        top_venue = paper.get("top_venue")
        if top_venue is not None and (not isinstance(top_venue, str) or top_venue not in TOP_VENUES):
            errors.append(f"{label}: invalid top_venue")
        evidence_level = paper.get("evidence_level")
        if not isinstance(evidence_level, str) or evidence_level not in EVIDENCE_LEVELS:
            errors.append(f"{label}: invalid evidence_level")
        if type(paper.get("year")) is not int or not 1900 <= paper["year"] <= 2026:
            errors.append(f"{label}: invalid year")
        for block in REQUIRED_BLOCKS:
            value = paper.get(block)
            if not isinstance(value, dict):
                errors.append(f"{label}: missing structured block {block}")
        for block in ("code", "dataset", "application_scenario", "problem_solved", "evaluation", "baselines"):
            value = paper.get(block)
            if not isinstance(value, dict):
                continue
            status = value.get("status")
            summary = value.get("summary")
            if not isinstance(status, str) or not status:
                errors.append(f"{label}: {block} status must be a non-empty string")
            if not isinstance(summary, str) or not summary:
                errors.append(f"{label}: {block} summary must be a non-empty string")
            if not status or not summary:
                errors.append(f"{label}: {block} needs status and summary")
            if isinstance(summary, str) and html.unescape(summary) != summary:
                errors.append(f"{label}: {block} summary contains an HTML entity")
            if isinstance(summary, str) and contains_non_english_script(summary):
                errors.append(f"{label}: {block} summary must be English")
            if isinstance(summary, str) and HUMANIZER_PUNCTUATION.search(summary):
                errors.append(f"{label}: {block} summary contains disallowed punctuation")
            evidence = value.get("evidence")
            if not isinstance(evidence, dict):
                errors.append(f"{label}: {block} evidence must be an object")
                continue
            if not valid_url(evidence.get("source_url", "")):
                errors.append(f"{label}: {block} evidence source must be HTTPS")
            locator = evidence.get("locator")
            if not isinstance(locator, str) or not locator:
                errors.append(f"{label}: {block} evidence locator must be a non-empty string")
            if (
                paper.get("evidence_level") == "metadata-only"
                and isinstance(locator, str)
                and "abstract" in locator.casefold()
            ):
                errors.append(f"{label}: metadata-only {block} locator cannot claim abstract evidence")
            if (
                paper.get("evidence_level") == "abstract"
                and isinstance(locator, str)
                and "full text" in locator.casefold()
            ):
                errors.append(f"{label}: abstract-level {block} locator cannot claim full-text evidence")
            if (
                block == "application_scenario"
                and status == "classified_from_title_and_abstract"
                and (
                    paper.get("evidence_level") == "metadata-only"
                    or not isinstance(locator, str)
                    or "abstract" not in locator.casefold()
                )
            ):
                errors.append(f"{label}: title-and-abstract classification requires abstract evidence")
        code = as_dict(paper.get("code"))
        dataset = as_dict(paper.get("dataset"))
        evaluation = as_dict(paper.get("evaluation"))
        baselines = as_dict(paper.get("baselines"))
        if not isinstance(code.get("url"), str):
            errors.append(f"{label}: code.url must be a string")
        if not valid_date(code.get("checked_on")):
            errors.append(f"{label}: code.checked_on must be a YYYY-MM-DD date")
        if not string_list(dataset.get("names")):
            errors.append(f"{label}: dataset.names must be a string list")
        if not string_list(evaluation.get("metrics_mentioned")):
            errors.append(f"{label}: evaluation.metrics_mentioned must be a string list")
        if not string_list(baselines.get("names")):
            errors.append(f"{label}: baselines.names must be a string list")
        if paper.get("evidence_level") == "metadata-only":
            allowed_metadata_statuses = {
                "code": {"not_found", "not_reported_in_accessible_source"},
                "dataset": {"not_reported_in_accessible_source"},
                "application_scenario": {"classified_from_title", "inferred_from_title"},
                "problem_solved": {"not_reported_in_accessible_source", "inferred_from_title"},
                "evaluation": {"not_reported_in_accessible_source"},
                "baselines": {"not_reported_in_accessible_source"},
            }
            for block in ("application_scenario", "problem_solved", "evaluation", "baselines", "dataset", "code"):
                block_status = as_dict(paper.get(block)).get("status")
                if block_status not in allowed_metadata_statuses[block]:
                    errors.append(f"{label}: metadata-only {block} has an unsupported status")
        if code.get("url") and not valid_url(code["url"]):
            errors.append(f"{label}: code.url must be empty or HTTPS")
        code_status = code.get("status")
        dataset_status = dataset.get("status")
        if isinstance(code_status, str) and code_status in OPEN_CODE_STATUSES and not valid_url(code.get("url", "")):
            errors.append(f"{label}: open code status requires a verified code URL")
        if isinstance(code_status, str) and code_status in OPEN_CODE_STATUSES and code.get("url") != urls.get("code"):
            errors.append(f"{label}: open code URL must match urls.code")
        if isinstance(dataset_status, str) and dataset_status in OPEN_DATA_STATUSES and not valid_url(urls.get("data", "")):
            errors.append(f"{label}: open dataset status requires a verified data URL")
        verification = as_dict(paper.get("verification"))
        if not valid_date(verification.get("checked_on")):
            errors.append(f"{label}: verification.checked_on must be a YYYY-MM-DD date")
        if not string_list(verification.get("sources"), require_items=True):
            errors.append(f"{label}: verification.sources must be a non-empty string list")
        else:
            for source in verification["sources"]:
                if not valid_url(source):
                    errors.append(f"{label}: verification source must be HTTPS")
        for field in ("requested_id", "note"):
            if not isinstance(verification.get(field), str) or not verification.get(field):
                errors.append(f"{label}: verification.{field} must be a non-empty string")
        note = verification.get("note")
        if isinstance(note, str) and contains_non_english_script(note):
            errors.append(f"{label}: verification.note must be English")
        if isinstance(note, str) and HUMANIZER_PUNCTUATION.search(note):
            errors.append(f"{label}: verification.note contains disallowed punctuation")
        if "abstract" in paper:
            errors.append(f"{label}: do not redistribute full abstracts")

    paper_objects = [paper for paper in papers if isinstance(paper, dict)]
    core = [paper for paper in paper_objects if paper.get("scope") == "pcb-core"]
    related = [paper for paper in paper_objects if paper.get("scope") == "related-eda"]
    core_topics = {
        paper["primary_topic"]
        for paper in core
        if isinstance(paper.get("primary_topic"), str)
    }
    if len(core) < 100:
        errors.append(f"catalog: expected >=100 PCB-core papers, found {len(core)}")
    if len(core_topics) < 8:
        errors.append(f"catalog: expected >=8 PCB-core primary topics, found {len(core_topics)}")
    if sum(type(paper.get("year")) is int and paper["year"] >= 2024 for paper in core) < 30:
        errors.append("catalog: fewer than 30 PCB-core papers from 2024-2026")

    if args.audit.exists():
        audit = json.loads(args.audit.read_text(encoding="utf-8"))
        admitted = audit.get("admitted") or []
        venue_searches = audit.get("venue_searches") or []
        if not isinstance(admitted, list) or not isinstance(venue_searches, list):
            errors.append("top-venue audit: admitted and venue_searches must be lists")
            admitted = []
            venue_searches = []
        if any(not isinstance(entry, dict) for entry in admitted + venue_searches):
            errors.append("top-venue audit: admitted and venue_searches rows must be objects")
            admitted = [entry for entry in admitted if isinstance(entry, dict)]
            venue_searches = [entry for entry in venue_searches if isinstance(entry, dict)]
        search_venues = [entry.get("venue") if isinstance(entry.get("venue"), str) else None for entry in venue_searches]
        venue_search_occurrences = Counter(search_venues)
        audited_venues = {venue for venue in search_venues if venue is not None}
        if audited_venues != TOP_VENUES:
            errors.append(f"top-venue audit: venue set mismatch {sorted(audited_venues)}")
        if venue_search_occurrences != Counter({venue: 1 for venue in TOP_VENUES}):
            errors.append("top-venue audit: expected exactly one venue_searches row per venue")
        catalog_by_id = {
            paper["id"]: paper
            for paper in paper_objects
            if isinstance(paper.get("id"), str) and paper["id"]
        }
        seen_audit_dois = set()
        seen_audit_ids = set()
        admitted_counts = Counter()
        for entry in admitted:
            venue = entry.get("venue") if isinstance(entry.get("venue"), str) else None
            admitted_counts[venue] += 1
            doi = canonical_doi(entry.get("doi"))
            catalog_id = entry.get("catalog_id") if isinstance(entry.get("catalog_id"), str) else None
            if entry.get("catalog_status") != "included":
                errors.append(f"top-venue audit: {doi or catalog_id} is not marked included")
            if venue not in TOP_VENUES:
                errors.append(f"top-venue audit: invalid admitted venue {venue}")
            if not doi or doi in seen_audit_dois:
                errors.append(f"top-venue audit: duplicate or missing DOI {doi}")
            seen_audit_dois.add(doi)
            if not catalog_id or catalog_id in seen_audit_ids:
                errors.append(f"top-venue audit: duplicate or missing catalog_id {catalog_id}")
            seen_audit_ids.add(catalog_id)
            paper = catalog_by_id.get(catalog_id)
            if not paper:
                errors.append(f"top-venue audit: catalog_id not found {catalog_id}")
                continue
            if paper.get("scope") != "pcb-core" or paper.get("top_venue") != venue:
                errors.append(f"top-venue audit: scope/venue mismatch for {catalog_id}")
            if paper.get("year") != entry.get("year"):
                errors.append(f"top-venue audit: year mismatch for {catalog_id}")
            if isinstance(entry.get("title"), str) and html.unescape(entry["title"]) != entry["title"]:
                errors.append(f"top-venue audit: title contains an HTML entity for {catalog_id}")
            paper_title = paper.get("title") if isinstance(paper.get("title"), str) else ""
            if normalized_title(paper_title) != normalized_title(str(entry.get("title", ""))):
                errors.append(f"top-venue audit: title mismatch for {catalog_id}")
            paper_doi = canonical_doi(paper.get("id"))
            raw_paper_sources = as_dict(paper.get("verification")).get("sources")
            paper_sources = (
                {source.casefold() for source in raw_paper_sources}
                if string_list(raw_paper_sources)
                else set()
            )
            doi_url = f"https://doi.org/{doi}"
            if doi != paper_doi and doi_url not in paper_sources:
                errors.append(f"top-venue audit: DOI is not bound to {catalog_id}")
            sources = entry.get("verification_sources")
            if not string_list(sources) or not sources or any(not valid_url(source) for source in sources):
                errors.append(f"top-venue audit: invalid verification sources for {catalog_id}")
            elif doi_url not in {source.casefold() for source in sources}:
                errors.append(f"top-venue audit: verification sources do not bind DOI for {catalog_id}")
        search_counts = Counter()
        for search in venue_searches:
            venue = search.get("venue")
            if type(search.get("accepted_count")) is not int:
                errors.append(f"top-venue audit: {venue} accepted_count must be an integer")
            else:
                search_counts[venue] = search["accepted_count"]
        if dict(admitted_counts) != dict(search_counts):
            errors.append("top-venue audit: admitted counts do not match venue_searches")
        catalog_top_counts = Counter(
            paper["top_venue"]
            for paper in core
            if isinstance(paper.get("top_venue"), str) and paper["top_venue"]
        )
        if dict(admitted_counts) != dict(catalog_top_counts):
            errors.append("top-venue audit: admitted counts do not match catalog top-venue counts")
        if audit.get("cutoff_date") != payload.get("cutoff_date"):
            errors.append("top-venue audit: cutoff date does not match catalog")
    elif args.require_audit:
        errors.append(f"top-venue audit missing: {args.audit}")

    if not valid_date(payload.get("cutoff_date")):
        errors.append("catalog: cutoff_date must be a YYYY-MM-DD date")

    link_report = json.loads(args.link_report.read_text(encoding="utf-8")) if args.link_report.exists() else None
    if link_report is None:
        errors.append(f"link report missing: {args.link_report}")
    else:
        results = link_report.get("results")
        if not isinstance(results, list) or any(not isinstance(item, dict) for item in results):
            errors.append("link report: results must be a list of objects")
            results = []
        result_urls = [item.get("url") for item in results]
        valid_result_urls = [url for url in result_urls if isinstance(url, str)]
        if (
            len(valid_result_urls) != len(result_urls)
            or len(valid_result_urls) != len(set(valid_result_urls))
            or any(not valid_url(url) for url in valid_result_urls)
        ):
            errors.append("link report: result URLs must be unique HTTPS URLs")
        catalog_urls = {
            paper["primary_url"]
            for paper in paper_objects
            if isinstance(paper.get("primary_url"), str) and paper["primary_url"]
        }
        catalog_urls.update(
            url
            for paper in paper_objects
            for key in ("code", "data")
            if isinstance((url := as_dict(paper.get("urls")).get(key)), str) and url
        )
        if catalog_urls != set(valid_result_urls):
            errors.append("link report: URL set does not match catalog paper/code/data URLs")
        if link_report.get("url_count") != len(results):
            errors.append("link report: url_count does not match results")
        acceptable = sum(
            isinstance(item.get("status"), str)
            and item["status"] in {"reachable", "access-controlled"}
            for item in results
        )
        if link_report.get("acceptable_count") != acceptable:
            errors.append("link report: acceptable_count does not match results")
        result_by_url = {item["url"]: item for item in results if isinstance(item.get("url"), str)}
        for paper in paper_objects:
            code = as_dict(paper.get("code"))
            dataset = as_dict(paper.get("dataset"))
            code_status = code.get("status")
            dataset_status = dataset.get("status")
            if isinstance(code_status, str) and code_status in OPEN_CODE_STATUSES:
                url = code.get("url")
                if not isinstance(url, str) or (result_by_url.get(url) or {}).get("status") not in {"reachable", "access-controlled"}:
                    errors.append(f"{paper.get('id')}: open code URL is not acceptable in link snapshot")
            if isinstance(dataset_status, str) and dataset_status in OPEN_DATA_STATUSES:
                url = as_dict(paper.get("urls")).get("data")
                if not isinstance(url, str) or (result_by_url.get(url) or {}).get("status") not in {"reachable", "access-controlled"}:
                    errors.append(f"{paper.get('id')}: open data URL is not acceptable in link snapshot")

    summary = {
        "papers": len(papers),
        "pcb_core": len(core),
        "related_eda": len(related),
        "primary_topics": dict(
            Counter(
                paper["primary_topic"]
                for paper in core
                if isinstance(paper.get("primary_topic"), str)
            )
        ),
        "top_venues": dict(
            Counter(
                paper["top_venue"]
                for paper in core
                if isinstance(paper.get("top_venue"), str) and paper["top_venue"]
            )
        ),
        "errors": len(errors),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
