#!/usr/bin/env python3
"""Build a deterministic review queue from Crossref discovery candidates.

The output is a queue for human/evidence review. It is never treated as an
automatic admission decision.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


BOARD = re.compile(r"\b(?:PCB|PCBs|PCBA|printed[ -]circuit board|printed wiring board|circuit board)\b", re.I)
EXCLUDE = re.compile(
    r"\b(?:figure|supplement|decision letter|reviewer report|correction|corrigendum|"
    r"retraction|erratum|waste|recycl|recovery of|holder|motor|antenna|education|"
    r"course|patent|bibliometric)\b",
    re.I,
)
TOP_VENUES = {
    "ASP-DAC": re.compile(r"Asia and South Pacific Design Automation Conference|ASP.?DAC", re.I),
    "ICCAD": re.compile(r"International Conference on Computer.Aided Design|\bICCAD\b", re.I),
    "DATE": re.compile(r"Design, Automation (?:&|and) Test in Europe|\bDATE\b", re.I),
    "ISPD": re.compile(r"International Symposium on Physical Design|\bISPD\b", re.I),
    "ECTC": re.compile(r"Electronic Components and Technology Conference|\bECTC\b", re.I),
    "EPEPS": re.compile(r"Electrical Performance of Electronic Packaging(?: and Systems)?|\bEPEP(?:S)?\b", re.I),
}
TOPICS = {
    "placement": re.compile(r"plac(?:e|ement|er)|floorplan|component arrangement", re.I),
    "routing": re.compile(r"rout|wirelength|length.match|escape|pin assignment|via minim|layer minim", re.I),
    "schematic-design": re.compile(
        r"schematic|netlist|component librar|migration|reverse engineering|datasheet|component select", re.I
    ),
    "si-pi-emc": re.compile(
        r"signal integrity|power integrity|electromagnetic|\bEMC\b|\bEMI\b|crosstalk|decoupl|"
        r"simultaneous switching|high.speed|millimeter.wave|mmwave|radiated emission",
        re.I,
    ),
    "thermal-reliability": re.compile(
        r"thermal|reliab|fatigue|vibrat|warpage|lifetime|thermo.mechanical|deformation", re.I
    ),
    "dfm-manufacturing": re.compile(
        r"manufactur|assembl|solder|fabricat|drill|yield|dummy pad|panel|pick.and.place|feeder|"
        r"insertion sequence|machine scheduling",
        re.I,
    ),
    "testing-inspection": re.compile(
        r"test|inspect|defect|fault|authentic|counterfeit|quality|anomaly detection", re.I
    ),
    "benchmarks-tools": re.compile(
        r"benchmark|dataset|tool|framework|open.source|challenge|automation|automatic|design guide", re.I
    ),
}
AI = re.compile(
    r"machine learning|deep learning|reinforcement learning|neural|\bLLM\b|multi.agent|"
    r"generative|\bMCTS\b|GAN|YOLO|transformer|graph attention",
    re.I,
)
QUALITY = re.compile(
    r"ACM Transactions|IEEE Transactions|IEEE Access|Expert Systems with Applications|"
    r"Integration|Scientific Reports|Microelectronics Reliability|Journal of Electronic Packaging|"
    r"PeerJ Computer Science|PLOS One|Sensors|Electronics|Applied Sciences",
    re.I,
)
PRIMARY_ORDER = (
    "placement",
    "routing",
    "schematic-design",
    "si-pi-emc",
    "thermal-reliability",
    "dfm-manufacturing",
    "testing-inspection",
    "benchmarks-tools",
)
QUOTAS = {
    "placement": 14,
    "routing": 20,
    "schematic-design": 9,
    "si-pi-emc": 16,
    "thermal-reliability": 11,
    "dfm-manufacturing": 14,
    "testing-inspection": 14,
    "benchmarks-tools": 9,
}


def top_venue(venue: str, doi: str) -> str | None:
    for name, pattern in TOP_VENUES.items():
        if pattern.search(venue):
            return name
    if (
        re.search(r"(?:ACM/IEEE|annual conference on|proceedings of the).*Design Automation Conference", venue, re.I)
        or doi.casefold().startswith("10.1109/dac")
    ) and "EURO-DAC" not in venue.upper():
        return "DAC"
    return None


def classify(title: str) -> list[str]:
    return [topic for topic, pattern in TOPICS.items() if pattern.search(title)]


def primary_topic(topics: list[str]) -> str:
    return next((topic for topic in PRIMARY_ORDER if topic in topics), "benchmarks-tools")


def score(record: dict, topics: list[str], top: str | None) -> int:
    title = record["title"]
    year = record.get("year") or 0
    value = 20 if top else 0
    value += 6 if year >= 2024 else 0
    value += 4 if QUALITY.search(record.get("venue", "")) else 0
    value += 3 if record.get("abstract") else 0
    value += 2 * len(topics)
    value += 4 if re.search(r"placement|routing|schematic|design automation", title, re.I) else 0
    value += 2 if AI.search(title) else 0
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    raw_records = json.loads(args.input.read_text(encoding="utf-8"))["records"]
    candidates = []
    for record in raw_records:
        title = record.get("title", "")
        if not BOARD.search(title) or EXCLUDE.search(title):
            continue
        if (record.get("year") or 0) > 2026:
            continue
        if record.get("type") not in {"journal-article", "proceedings-article", "posted-content"}:
            continue
        topics = classify(title)
        if not topics and not re.search(r"design|layout|simulat|optim|analys|model|co-design", title, re.I):
            continue
        top = top_venue(record.get("venue", ""), record.get("doi", ""))
        item = dict(record)
        item["topics_suggested"] = topics or ["benchmarks-tools"]
        item["primary_topic_suggested"] = primary_topic(item["topics_suggested"])
        item["ai_assisted"] = bool(AI.search(title))
        item["top_venue_suggested"] = top
        item["selection_score"] = score(item, item["topics_suggested"], top)
        candidates.append(item)

    candidates.sort(
        key=lambda item: (
            -item["selection_score"],
            -(item.get("year") or 0),
            item["title"].casefold(),
        )
    )
    selected = []
    seen_titles = set()

    def admit(item: dict, reason: str) -> None:
        key = re.sub(r"[^a-z0-9]+", "", item["title"].casefold())
        if key in seen_titles:
            return
        item = dict(item)
        item["selection_reason"] = reason
        selected.append(item)
        seen_titles.add(key)

    for item in candidates:
        if item["top_venue_suggested"]:
            admit(item, "top-venue coverage queue")

    counts = Counter(item["primary_topic_suggested"] for item in selected)
    for topic, quota in QUOTAS.items():
        for item in candidates:
            if counts[topic] >= quota:
                break
            if item["primary_topic_suggested"] != topic:
                continue
            before = len(selected)
            admit(item, f"topic quota: {topic}")
            if len(selected) > before:
                counts[topic] += 1

    for item in candidates:
        if len(selected) >= 120:
            break
        if (item.get("year") or 0) >= 2024:
            admit(item, "recent coverage fill")

    payload = {
        "source": str(args.input),
        "record_count": len(selected),
        "primary_topic_counts": dict(Counter(item["primary_topic_suggested"] for item in selected)),
        "top_venue_counts": dict(Counter(item["top_venue_suggested"] for item in selected if item["top_venue_suggested"])),
        "records": selected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in payload.items() if key != "records"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
