#!/usr/bin/env python3
"""Merge reviewed discovery records into the catalog's evidence-card schema."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TOPIC_NAMES = {
    "placement": "Placement and legalization",
    "routing": "Routing and constraint handling",
    "schematic-design": "Schematic and design-chain automation",
    "si-pi-emc": "SI, PI, and EMC",
    "thermal-reliability": "Thermal and reliability co-design",
    "dfm-manufacturing": "DFM and assembly optimization",
    "testing-inspection": "Testing and inspection",
    "benchmarks-tools": "Benchmarks, datasets, and tools",
}
AI_PATTERN = re.compile(
    r"machine learning|deep learning|reinforcement learning|neural|\bLLM\b|multi.agent|"
    r"generative|\bMCTS\b|GAN|YOLO|transformer|graph attention|XGBoost",
    re.I,
)
DATA_PATTERN = re.compile(
    r"dataset|benchmark|test ?case|real-world|industrial|synthetic|simulation|training data|"
    r"academic and industrial|board designs",
    re.I,
)
EVAL_PATTERN = re.compile(
    r"experiment|evaluation|results? show|demonstrat|validat|compar|outperform|surpass|"
    r"runtime|accuracy|wirelength|routability|violations?|quality|latency|throughput",
    re.I,
)
BASELINE_PATTERN = re.compile(
    r"baseline|compar|outperform|surpass|state-of-the-art|existing method|previous approach|"
    r"academic placer|human-level|Altium|FreeRouting|YOLO",
    re.I,
)
PROBLEM_PATTERN = re.compile(
    r"challenge|problem|limitation|address|aim|focus|essential|difficult|need|bottleneck|"
    r"we propose|we present|introduce",
    re.I,
)
METRICS = (
    "accuracy",
    "precision",
    "recall",
    "F1",
    "mAP",
    "runtime",
    "wirelength",
    "routability",
    "via count",
    "layer count",
    "violations",
    "power",
    "temperature",
    "lifetime",
    "latency",
    "throughput",
)
BASELINE_NAMES = (
    "Altium",
    "FreeRouting",
    "DeepPCB",
    "HRIPCB",
    "YOLOv5",
    "YOLOv8",
    "YOLOv11",
    "YOLOv12",
    "Mask R-CNN",
    "simulated annealing",
    "DQN",
    "actor-critic",
)
DATASET_NAMES = (
    "DeepPCB",
    "HRIPCB",
    "SolDef_AI",
    "OmniLayout",
    "OmniRouting",
    "PCB-Defect",
    "PKU-Market-PCB",
)
TOPIC_PATTERNS = {
    "placement": re.compile(r"plac(?:e|ement|er)|floorplan|component arrangement", re.I),
    "routing": re.compile(r"rout|wirelength|length.match|escape|pin assignment|via minim|layer minim", re.I),
    "schematic-design": re.compile(r"schematic|netlist|component librar|migration|datasheet", re.I),
    "si-pi-emc": re.compile(r"signal integrity|power integrity|electromagnetic|\bEMC\b|\bEMI\b|crosstalk|decoupl", re.I),
    "thermal-reliability": re.compile(r"thermal|reliab|fatigue|vibrat|warpage|lifetime|thermo.mechanical", re.I),
    "dfm-manufacturing": re.compile(r"manufactur|assembl|solder|fabricat|drill|yield|dummy pad|feeder", re.I),
    "testing-inspection": re.compile(r"test|inspect|defect|fault|authentic|counterfeit|quality", re.I),
    "benchmarks-tools": re.compile(r"benchmark|dataset|tool|framework|open.source|challenge", re.I),
}


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text or "") if part.strip()]


def matching_sentences(text: str, pattern: re.Pattern, limit: int = 2) -> list[str]:
    return [sentence for sentence in sentences(text) if pattern.search(sentence)][:limit]


def status_block(
    texts: list[str], evidence_url: str, reported_summary: str, *, has_abstract: bool
) -> dict:
    if not texts:
        return {
            "status": "not_reported_in_accessible_source",
            "summary": "The accessible metadata or abstract does not report this field." if has_abstract else "The accessible metadata does not report this field.",
            "evidence": {
                "source_url": evidence_url,
                "locator": "metadata or abstract" if has_abstract else "metadata",
            },
        }
    return {
        "status": "reported_in_abstract",
        "summary": reported_summary,
        "evidence": {"source_url": evidence_url, "locator": "abstract"},
    }


def semantic_map(payload: dict) -> dict[str, dict | None]:
    return {entry["requested_id"].casefold(): entry["result"] for entry in payload["records"]}


def publication_state(doi: str, external_ids: dict) -> str:
    lowered = doi.casefold()
    if external_ids.get("ArXiv") and (not doi or doi.startswith("10.48550/arxiv")):
        return "preprint"
    if any(fragment in lowered for fragment in ("ssrn", "researchsquare", "techrxiv", "preprints")):
        return "preprint"
    return "peer-reviewed"


def fallback_venue(doi: str, arxiv_id: str) -> str:
    lowered = doi.casefold()
    if arxiv_id or "arxiv" in lowered:
        return "arXiv"
    if "10.21203/rs." in lowered:
        return "Research Square"
    if "10.31224/" in lowered:
        return "engrXiv"
    if "techrxiv" in lowered:
        return "TechRxiv"
    if "ssrn" in lowered:
        return "SSRN"
    return "Unspecified preprint server"


def make_record(seed: dict, semantic: dict | None, requested_id: str) -> dict:
    semantic = semantic or {}
    external = semantic.get("externalIds") or {}
    doi = (external.get("DOI") or seed.get("doi") or "").lower()
    arxiv_id = external.get("ArXiv", "")
    primary_url = f"https://doi.org/{doi}" if doi else f"https://arxiv.org/abs/{arxiv_id}"
    title = semantic.get("title") or seed.get("title", "")
    abstract = semantic.get("abstract") or seed.get("abstract", "")
    topics = list(seed.get("topics_suggested") or ["benchmarks-tools"])
    title_topics = [topic for topic, pattern in TOPIC_PATTERNS.items() if pattern.search(title)]
    derived_topics = [topic for topic, pattern in TOPIC_PATTERNS.items() if pattern.search(f"{title} {abstract}")]
    topics = list(dict.fromkeys(derived_topics + topics))
    if AI_PATTERN.search(f"{title} {abstract}") and "ai-eda" not in topics:
        topics.append("ai-eda")
    seed_primary = seed.get("primary_topic_suggested")
    primary_topic = seed_primary if seed_primary and not (seed_primary == "benchmarks-tools" and derived_topics) else next(
        (topic for topic in title_topics if topic in TOPIC_NAMES and topic != "benchmarks-tools"),
        next((topic for topic in derived_topics if topic in TOPIC_NAMES and topic != "benchmarks-tools"), "benchmarks-tools"),
    )
    dataset_evidence = matching_sentences(abstract, DATA_PATTERN)
    evaluation_evidence = matching_sentences(abstract, EVAL_PATTERN, limit=3)
    baseline_evidence = matching_sentences(abstract, BASELINE_PATTERN, limit=2)
    problem_evidence = matching_sentences(abstract, PROBLEM_PATTERN, limit=2)
    metrics = [metric for metric in METRICS if re.search(rf"\b{re.escape(metric)}\b", " ".join(evaluation_evidence), re.I)]
    baseline_names = [
        name for name in BASELINE_NAMES if re.search(re.escape(name), " ".join(baseline_evidence), re.I)
    ]
    dataset_names = [name for name in DATASET_NAMES if re.search(re.escape(name), " ".join(dataset_evidence), re.I)]
    if baseline_evidence and not baseline_names:
        baseline_status = "reported_but_unnamed_in_abstract"
    elif baseline_names:
        baseline_status = "named_in_abstract"
    else:
        baseline_status = "not_reported_in_accessible_source"
    open_pdf = (semantic.get("openAccessPdf") or {}).get("url") or ""
    code_mentions = matching_sentences(abstract, re.compile(r"open.source|source code|github|code is available", re.I))
    code_status = "announced_or_mentioned_unverified" if code_mentions else "not_found"
    topic_label = TOPIC_NAMES[primary_topic]
    authors = [entry.get("name", "") for entry in semantic.get("authors") or [] if entry.get("name")]
    if not authors:
        authors = seed.get("authors") or []
    semantic_url = (
        f"https://www.semanticscholar.org/paper/{semantic.get('paperId')}" if semantic.get("paperId") else ""
    )
    verification_urls = [url for url in (primary_url, semantic_url) if url]
    return {
        "id": f"doi:{doi}" if doi else f"arxiv:{arxiv_id}",
        "title": title,
        "authors": authors,
        "year": semantic.get("year") or seed.get("year"),
        "venue": semantic.get("venue") or seed.get("venue", "") or fallback_venue(doi, arxiv_id),
        "publication_state": publication_state(doi, external),
        "primary_url": primary_url,
        "urls": {
            "doi": f"https://doi.org/{doi}" if doi else "",
            "arxiv": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else "",
            "open_access_pdf": open_pdf,
            "code": "",
            "data": "",
        },
        "scope": "pcb-core",
        "topics": topics,
        "primary_topic": primary_topic,
        "top_venue": seed.get("top_venue_suggested"),
        "code": {
            "status": code_status,
            "url": "",
            "summary": "The abstract mentions an open resource, but no direct code URL was verified." if code_mentions else "No verified public code repository was found.",
            "checked_on": "2026-08-11",
            "evidence": {
                "source_url": primary_url,
                "locator": "abstract and linked metadata" if abstract else "metadata and linked sources",
            },
        },
        "dataset": {
            **status_block(
                dataset_evidence,
                primary_url,
                "The abstract mentions a dataset, benchmark, or data from real, industrial, or simulated cases. Only identifiable names are retained.",
                has_abstract=bool(abstract),
            ),
            "names": dataset_names,
        },
        "application_scenario": {
            "status": "classified_from_title_and_abstract" if abstract else "classified_from_title",
            "summary": f"{topic_label}.",
            "evidence": {
                "source_url": primary_url,
                "locator": "title" if not abstract else "title and abstract",
            },
        },
        "problem_solved": status_block(
            problem_evidence,
            primary_url,
            "The abstract describes the PCB design problem.",
            has_abstract=bool(abstract),
        ),
        "evaluation": {
            **status_block(
                evaluation_evidence,
                primary_url,
                "The abstract reports an experiment or evaluation; the metric field lists only items explicitly mentioned in the abstract.",
                has_abstract=bool(abstract),
            ),
            "metrics_mentioned": metrics,
        },
        "baselines": {
            "status": baseline_status,
            "names": baseline_names,
            "summary": (
                f"Baselines explicitly named in the abstract: {', '.join(baseline_names)}."
                if baseline_names
                else "The abstract mentions a comparison but does not name the baseline."
                if baseline_evidence
                else "The accessible metadata or abstract does not list a baseline."
                if abstract
                else "The accessible metadata does not list a baseline."
            ),
            "evidence": {"source_url": primary_url, "locator": "abstract" if abstract else "metadata"},
        },
        "evidence_level": "abstract" if abstract else "metadata-only",
        "verification": {
            "checked_on": "2026-08-11",
            "sources": verification_urls,
            "requested_id": requested_id,
            "note": "Publisher/DOI is the primary record; Semantic Scholar is metadata corroboration only.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--semantic", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    seed = json.loads(args.seed.read_text(encoding="utf-8"))
    semantic_payload = json.loads(args.semantic.read_text(encoding="utf-8"))
    semantic = semantic_map(semantic_payload)
    seed_by_doi = {f"doi:{item['doi']}".casefold(): item for item in seed["records"] if item.get("doi")}
    records = []
    for requested_id, result in semantic.items():
        if requested_id.startswith("doi:"):
            seed_item = seed_by_doi.get(requested_id, {})
        else:
            seed_item = {
                "doi": "",
                "title": (result or {}).get("title", ""),
                "authors": [],
                "year": (result or {}).get("year"),
                "venue": (result or {}).get("venue", ""),
                "topics_suggested": ["benchmarks-tools"],
                "primary_topic_suggested": "benchmarks-tools",
                "top_venue_suggested": None,
            }
        if not seed_item and not result:
            continue
        records.append(make_record(seed_item, result, requested_id))

    records.sort(key=lambda item: (-(item.get("year") or 0), item["primary_topic"], item["title"].casefold()))
    payload = {
        "schema_version": "2.0.0",
        "title": "Awesome PCB Design Papers",
        "cutoff_date": "2026-08-11",
        "scope_note": (
            "PCB-core papers are the catalog authority. Non-PCB automated EDA papers, when admitted, "
            "use scope=related-eda and are analyzed separately."
        ),
        "topics": [{"id": key, "name": value} for key, value in TOPIC_NAMES.items()]
        + [{"id": "ai-eda", "name": "AI/ML-assisted EDA"}],
        "papers": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(records)} evidence cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
