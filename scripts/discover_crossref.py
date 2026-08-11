#!/usr/bin/env python3
"""Discover PCB-design literature candidates through the Crossref API."""

from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from discover_openalex import BOARD_TERMS, QUERY_SPECS, normalized_title


API_URL = "https://api.crossref.org/works"
TAG_RE = re.compile(r"<[^>]+>")


def first_date(item: dict) -> tuple[int | None, str | None]:
    for field in ("published-print", "published-online", "issued", "created"):
        parts = ((item.get(field) or {}).get("date-parts") or [[]])[0]
        if not parts or parts[0] is None:
            continue
        year = int(parts[0])
        padded = [int(value) for value in parts[1:3]] + [1, 1]
        return year, f"{year:04d}-{padded[0]:02d}-{padded[1]:02d}"
    return None, None


def clean_markup(value: str) -> str:
    return html.unescape(TAG_RE.sub(" ", value or "")).strip()


def fetch(query: str, rows: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "query.bibliographic": query,
            "rows": rows,
            "select": (
                "DOI,title,author,published-print,published-online,issued,created,"
                "container-title,URL,abstract,type,subject,publisher,link"
            ),
        }
    )
    request = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={
            "Accept": "application/json",
            "User-Agent": "awesome-pcb-design-papers/1.0 (https://github.com/WhoJay0609)",
        },
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return json.load(response)["message"]["items"]
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 2:
                raise
            time.sleep(min(int(exc.headers.get("Retry-After", "2")), 20))
    return []


def compact(item: dict, topic: str, query: str) -> dict:
    year, publication_date = first_date(item)
    title_values = item.get("title") or []
    venue_values = item.get("container-title") or []
    doi = item.get("DOI", "").lower()
    return {
        "doi": doi,
        "title": clean_markup(title_values[0] if title_values else ""),
        "year": year,
        "publication_date": publication_date,
        "venue": clean_markup(venue_values[0] if venue_values else ""),
        "type": item.get("type", ""),
        "url": f"https://doi.org/{doi}" if doi else item.get("URL", ""),
        "authors": [
            " ".join(part for part in (author.get("given", ""), author.get("family", "")) if part)
            for author in item.get("author") or []
        ],
        "abstract": clean_markup(item.get("abstract", "")),
        "subjects": item.get("subject") or [],
        "publisher": item.get("publisher", ""),
        "query_topics": [topic],
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
            items = fetch(query, args.per_query)
            admitted = 0
            for raw in items:
                item = compact(raw, topic, query)
                evidence_text = f"{item['title']} {item['abstract']}"
                if not args.include_weak and not BOARD_TERMS.search(evidence_text):
                    continue
                key = item["doi"] or normalized_title(item["title"])
                if not key:
                    continue
                if key in candidates:
                    merge(candidates[key], item)
                else:
                    candidates[key] = item
                admitted += 1
            query_log.append(
                {"topic": topic, "query": query, "returned": len(items), "board_term_hits": admitted}
            )
            time.sleep(0.15)

    records = sorted(
        candidates.values(),
        key=lambda item: (
            -(item.get("year") or 0),
            -len(item.get("query_topics") or []),
            item.get("title", "").casefold(),
        ),
    )
    payload = {
        "source": "Crossref REST API",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "query_log": query_log,
        "candidate_count": len(records),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(records)} candidates to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
