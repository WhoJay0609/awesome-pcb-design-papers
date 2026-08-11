#!/usr/bin/env python3
"""Discover PCB literature through DBLP, with a read-only Jina fallback.

DBLP is used to verify publication metadata. Final catalog links still point to
the publisher/DOI/arXiv page whenever DBLP exposes one.
"""

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

from discover_openalex import normalized_title


DIRECT_API = "https://dblp.org/search/publ/api"
JINA_PREFIX = "https://r.jina.ai/http://dblp.org/search/publ/api?"
QUERIES = [
    "pcb",
    '"printed circuit board"',
    '"printed wiring board"',
    "pcba",
    '"board-level" pcb',
]
TOPIC_RULES = {
    "placement": ("placement", "floorplan", "component arrangement"),
    "routing": ("routing", "router", "wirelength", "escape", "length matching", "pin assignment"),
    "ai-eda": ("machine learning", "deep learning", "reinforcement learning", "neural", "llm", "agent"),
    "schematic-design": ("schematic", "netlist", "component library", "migration", "reverse engineering"),
    "si-pi-emc": ("signal integrity", "power integrity", "electromagnetic", "emc", "emi", "crosstalk"),
    "thermal-reliability": ("thermal", "reliability", "fatigue", "vibration", "warpage", "lifetime"),
    "dfm-manufacturing": ("manufactur", "assembly", "solder", "fabrication", "drill", "yield"),
    "testing-inspection": ("test", "inspection", "defect", "fault", "authentication"),
    "benchmarks-tools": ("benchmark", "dataset", "tool", "framework", "open-source", "challenge"),
}


def strip_markup(value) -> str:
    if isinstance(value, list):
        value = "; ".join(str(part) for part in value)
    return html.unescape(re.sub(r"<[^>]+>", "", str(value or ""))).strip()


def request_payload(query: str, hits: int) -> tuple[dict, str]:
    params = urllib.parse.urlencode({"q": query, "h": hits, "format": "json"})
    headers = {"User-Agent": "awesome-pcb-design-papers/1.0 (metadata audit)"}
    try:
        request = urllib.request.Request(f"{DIRECT_API}?{params}", headers=headers)
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.load(response), "DBLP direct API"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        request = urllib.request.Request(f"{JINA_PREFIX}{params}", headers=headers)
        with urllib.request.urlopen(request, timeout=60) as response:
            text = response.read().decode("utf-8", "replace")
        start = text.find("{")
        if start < 0:
            raise ValueError("Jina DBLP fallback did not return JSON")
        sanitized = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text[start:])
        return json.loads(sanitized), "DBLP API via Jina read-only fallback"


def as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def compact(hit: dict, query: str) -> dict:
    info = hit.get("info") or {}
    title = strip_markup(info.get("title", ""))
    ee = as_list(info.get("ee"))
    primary = next((url for url in ee if "doi.org/" in url), ee[0] if ee else info.get("url", ""))
    authors = []
    for author in as_list((info.get("authors") or {}).get("author")):
        authors.append(strip_markup(author.get("text", "") if isinstance(author, dict) else str(author)))
    lower = title.casefold()
    topics = sorted(
        topic for topic, terms in TOPIC_RULES.items() if any(term in lower for term in terms)
    )
    return {
        "dblp_key": info.get("key", ""),
        "title": title,
        "authors": authors,
        "year": int(info["year"]) if str(info.get("year", "")).isdigit() else None,
        "venue": strip_markup(info.get("venue", "")),
        "type": info.get("type", ""),
        "url": primary,
        "verification_urls": [url for url in ee if url],
        "dblp_url": info.get("url", ""),
        "topics_suggested": topics,
        "queries": [query],
    }


def merge(existing: dict, incoming: dict) -> None:
    existing["queries"] = sorted(set(existing["queries"] + incoming["queries"]))
    existing["verification_urls"] = sorted(
        set(existing["verification_urls"] + incoming["verification_urls"])
    )
    existing["topics_suggested"] = sorted(
        set(existing["topics_suggested"] + incoming["topics_suggested"])
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--hits", type=int, default=1000)
    args = parser.parse_args()

    candidates: dict[str, dict] = {}
    log = []
    sources = set()
    for query in QUERIES:
        payload, source = request_payload(query, args.hits)
        sources.add(source)
        hits_block = payload["result"]["hits"]
        hits = hits_block.get("hit") or []
        for hit in hits:
            item = compact(hit, query)
            key = item["dblp_key"] or normalized_title(item["title"])
            if not key:
                continue
            if key in candidates:
                merge(candidates[key], item)
            else:
                candidates[key] = item
        log.append({"query": query, "reported_total": int(hits_block.get("@total", 0)), "returned": len(hits)})
        time.sleep(0.2)

    records = sorted(
        candidates.values(),
        key=lambda item: (-(item.get("year") or 0), item.get("title", "").casefold()),
    )
    payload = {
        "source": sorted(sources),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "query_log": log,
        "candidate_count": len(records),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(records)} candidates to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
