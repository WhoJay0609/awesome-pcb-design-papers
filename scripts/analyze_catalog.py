#!/usr/bin/env python3
"""Reproduce topic, year, and controlled-keyword distributions."""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


KEYWORDS = {
    "routing": r"\brout(?:e|er|ing)\b",
    "placement": r"\bplac(?:e|er|ement)\b",
    "optimization": r"\boptimi[sz](?:e|ed|ation)\b",
    "signal-integrity": r"\bsignal integrity\b",
    "power-integrity": r"\bpower integrity\b",
    "emc-emi": r"\b(?:EMC|EMI|electromagnetic compatibility|electromagnetic interference)\b",
    "thermal": r"\bthermal\b|thermo-mechanical",
    "reliability": r"\breliab(?:ility|le)\b|fatigue|lifetime|vibration|warpage",
    "manufacturing": r"manufactur|fabricat|assembly|solder|drill|yield",
    "testing-inspection": r"\btest(?:ing)?\b|inspect|defect|fault|quality",
    "machine-learning": r"\bmachine learning\b",
    "deep-learning": r"\bdeep learning\b|\bYOLO\b",
    "reinforcement-learning": r"\breinforcement learning\b|\bDQN\b|actor-critic",
    "llm-agent": r"\bLLM\b|large language model|multi-agent|agentic",
    "graph-learning": r"graph neural|graph attention|\bGNN\b",
    "transformer": r"\btransformer\b|\bDETR\b",
    "benchmark-dataset": r"\bbenchmark\b|\bdataset\b",
    "open-source": r"open.source|\bKiCad\b|\bFreeRouting\b",
    "co-design": r"co.design|joint optimization|simultaneous",
}
PATTERNS = {name: re.compile(pattern, re.I) for name, pattern in KEYWORDS.items()}


def write_csv(path: Path, headers: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def bar_svg(path: Path, title: str, rows: list[tuple[str, int]], width: int = 1000) -> None:
    rows = rows[:20]
    left, right, top, row_h = 240, 50, 70, 34
    height = top + row_h * len(rows) + 45
    max_value = max((value for _, value in rows), default=1)
    chart_width = width - left - right
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
        f'<text x="{width / 2}" y="38" text-anchor="middle" fill="#f0f6fc" font-family="sans-serif" font-size="22">{html.escape(title)}</text>',
    ]
    for index, (label, value) in enumerate(rows):
        y = top + index * row_h
        bar_width = chart_width * value / max_value
        body.extend(
            [
                f'<text x="{left - 12}" y="{y + 20}" text-anchor="end" fill="#c9d1d9" font-family="sans-serif" font-size="14">{html.escape(label)}</text>',
                f'<rect x="{left}" y="{y + 5}" width="{bar_width:.1f}" height="20" rx="3" fill="#58a6ff"/>',
                f'<text x="{left + bar_width + 8:.1f}" y="{y + 20}" fill="#f0f6fc" font-family="sans-serif" font-size="14">{value}</text>',
            ]
        )
    body.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def line_svg(path: Path, title: str, year_counts: dict[int, int], width: int = 1000, height: int = 420) -> None:
    years = list(range(min(year_counts or {2026: 0}), max(year_counts or {2026: 0}) + 1))
    left, right, top, bottom = 70, 40, 65, 65
    chart_w, chart_h = width - left - right, height - top - bottom
    max_value = max(year_counts.values(), default=1)
    points = []
    for index, year in enumerate(years):
        x = left + (chart_w * index / max(len(years) - 1, 1))
        y = top + chart_h * (1 - year_counts.get(year, 0) / max_value)
        points.append((x, y, year_counts.get(year, 0), year))
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#0d1117"/>',
        f'<text x="{width / 2}" y="36" text-anchor="middle" fill="#f0f6fc" font-family="sans-serif" font-size="22">{html.escape(title)}</text>',
        f'<line x1="{left}" y1="{top + chart_h}" x2="{width - right}" y2="{top + chart_h}" stroke="#8b949e"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_h}" stroke="#8b949e"/>',
        f'<polyline fill="none" stroke="#58a6ff" stroke-width="3" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in points)}"/>',
    ]
    label_step = max(1, math.ceil(len(years) / 12))
    for index, (x, y, value, year) in enumerate(points):
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#58a6ff"><title>{year}: {value}</title></circle>')
        if index % label_step == 0 or index == len(points) - 1:
            body.append(f'<text x="{x:.1f}" y="{height - 32}" text-anchor="middle" fill="#c9d1d9" font-family="sans-serif" font-size="12">{year}</text>')
    body.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def analyze_scope(papers: list[dict]) -> dict:
    keyword_counts = Counter()
    keyword_by_year = defaultdict(Counter)
    for paper in papers:
        text = " ".join(
            [
                paper.get("title", ""),
                paper.get("problem_solved", {}).get("summary", ""),
                paper.get("application_scenario", {}).get("summary", ""),
            ]
        )
        for keyword, pattern in PATTERNS.items():
            if pattern.search(text):
                keyword_counts[keyword] += 1
                keyword_by_year[paper["year"]][keyword] += 1
    return {
        "paper_count": len(papers),
        "year_counts": dict(sorted(Counter(paper["year"] for paper in papers).items())),
        "topic_counts": dict(sorted(Counter(paper["primary_topic"] for paper in papers).items())),
        "keyword_document_frequency": dict(keyword_counts.most_common()),
        "keyword_by_year": {str(year): dict(counts) for year, counts in sorted(keyword_by_year.items())},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--analysis-dir", type=Path, default=Path("analysis"))
    parser.add_argument("--assets-dir", type=Path, default=Path("assets"))
    args = parser.parse_args()
    payload = json.loads(args.catalog.read_text(encoding="utf-8"))
    papers = payload["papers"]
    scopes = {
        "pcb-core": [paper for paper in papers if paper["scope"] == "pcb-core"],
        "related-eda": [paper for paper in papers if paper["scope"] == "related-eda"],
    }
    result = {
        "cutoff_date": payload["cutoff_date"],
        "method": (
            "Document frequency over controlled case-insensitive regex terms applied to titles and original "
            "catalog summaries. Each keyword counts at most once per paper; scopes are computed separately."
        ),
        "scopes": {scope: analyze_scope(items) for scope, items in scopes.items()},
    }
    args.analysis_dir.mkdir(parents=True, exist_ok=True)
    (args.analysis_dir / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    for scope, summary in result["scopes"].items():
        prefix = scope.replace("-", "_")
        write_csv(
            args.analysis_dir / f"{prefix}_keywords.csv",
            ["keyword", "paper_count"],
            [[key, value] for key, value in summary["keyword_document_frequency"].items()],
        )
        write_csv(
            args.analysis_dir / f"{prefix}_years.csv",
            ["year", "paper_count"],
            [[year, value] for year, value in summary["year_counts"].items()],
        )
        write_csv(
            args.analysis_dir / f"{prefix}_topics.csv",
            ["topic", "paper_count"],
            [[key, value] for key, value in summary["topic_counts"].items()],
        )
        keyword_rows = list(summary["keyword_document_frequency"].items())
        bar_svg(args.assets_dir / f"{prefix}_keyword_distribution.svg", f"{scope}: keyword document frequency", keyword_rows)
    pcb = result["scopes"]["pcb-core"]
    line_svg(
        args.assets_dir / "pcb_core_year_trend.svg",
        "PCB-core publication coverage by year",
        {int(year): value for year, value in pcb["year_counts"].items()},
    )
    bar_svg(
        args.assets_dir / "pcb_core_topic_distribution.svg",
        "PCB-core primary-topic distribution",
        sorted(pcb["topic_counts"].items(), key=lambda item: (-item[1], item[0])),
    )
    print(json.dumps({scope: data["paper_count"] for scope, data in result["scopes"].items()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
