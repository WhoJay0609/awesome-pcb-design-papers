#!/usr/bin/env python3
"""Fetch abstract-level corroboration for a review queue in one batch."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
FIELDS = (
    "title,year,venue,abstract,openAccessPdf,externalIds,publicationDate,authors,"
    "publicationTypes,journal"
)


def fetch(ids: list[str]) -> list[dict | None]:
    query = urllib.parse.urlencode({"fields": FIELDS})
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "awesome-pcb-design-papers/1.0 (metadata corroboration)",
    }
    if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
    request = urllib.request.Request(
        f"{API_URL}?{query}",
        data=json.dumps({"ids": ids}).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 3:
                raise
            delay = min(int(exc.headers.get("Retry-After", str(5 * (attempt + 1)))), 30)
            time.sleep(delay)
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--extra-id", action="append", default=[])
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    ids = []
    for item in source["records"]:
        if item.get("doi"):
            ids.append(f"DOI:{item['doi']}")
    ids.extend(args.extra_id)
    ids = list(dict.fromkeys(ids))
    if len(ids) > 500:
        raise SystemExit("Semantic Scholar batch endpoint accepts at most 500 IDs")

    response = fetch(ids)
    records = []
    for requested_id, item in zip(ids, response):
        records.append({"requested_id": requested_id, "result": item})
    payload = {
        "source": "Semantic Scholar Academic Graph API",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "requested_count": len(ids),
        "resolved_count": sum(item["result"] is not None for item in records),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"resolved {payload['resolved_count']}/{payload['requested_count']} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
