#!/usr/bin/env python3
"""Check catalog paper/code/data URLs concurrently and emit a machine-readable report."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


def check(url: str, timeout: int) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 awesome-pcb-design-papers-link-check/1.0"}
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return {
                    "url": url,
                    "status": "reachable",
                    "http_status": response.status,
                    "final_url": response.geturl(),
                    "method": method,
                }
        except urllib.error.HTTPError as exc:
            if exc.code in {401, 403}:
                return {
                    "url": url,
                    "status": "access-controlled",
                    "http_status": exc.code,
                    "final_url": exc.geturl(),
                    "method": method,
                }
            if method == "HEAD":
                continue
            return {
                "url": url,
                "status": "http-error",
                "http_status": exc.code,
                "final_url": exc.geturl(),
                "method": method,
            }
        except Exception as exc:  # Network errors are report data, not hidden failures.
            if method == "HEAD":
                continue
            return {
                "url": url,
                "status": "network-error",
                "http_status": None,
                "final_url": "",
                "method": method,
                "error_type": type(exc).__name__,
            }
    return {"url": url, "status": "network-error", "http_status": None, "final_url": ""}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--output", type=Path, default=Path("analysis/link_check.json"))
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    payload = json.loads(args.catalog.read_text(encoding="utf-8"))
    urls = []
    for paper in payload["papers"]:
        urls.append(paper["primary_url"])
        for key in ("code", "data"):
            if paper.get("urls", {}).get(key):
                urls.append(paper["urls"][key])
    urls = sorted(set(urls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda url: check(url, args.timeout), urls))
    report = {
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "url_count": len(urls),
        "acceptable_count": sum(item["status"] in {"reachable", "access-controlled"} for item in results),
        "results": sorted(results, key=lambda item: item["url"]),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "results"}, indent=2))
    bad = [item for item in results if item["status"] not in {"reachable", "access-controlled"}]
    for item in bad:
        print(f"{item['status']}: {item['url']} ({item.get('http_status')})")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
