#!/usr/bin/env python3
"""Render the JSON catalog into an Awesome-style README and topic pages."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path


PUBLIC_CODE_STATUSES = frozenset(
    {"open", "partial_open", "open_archived", "utility_open"}
)
ACCESSIBLE_DATA_STATUSES = frozenset(
    {
        "open",
        "partial_open",
        "open_with_upstream_terms",
        "public_benchmark",
        "public_benchmarks",
    }
)

RECENT_START_YEAR = 2024

SCOPE_LABELS = {
    "pcb-core": "PCB core",
    "related-eda": "Related EDA",
}

STATUS_LABELS = {
    "not_reported_in_accessible_source": "not reported",
    "announced_or_mentioned_unverified": "announced/unverified",
    "announced_unverified": "announced/unverified",
    "reported_link_unreachable": "link unreachable",
    "not_found": "not found",
    "open_archived": "open (archived)",
    "open_with_upstream_terms": "open (upstream terms)",
    "public_benchmark": "public benchmark",
    "public_benchmarks": "public benchmarks",
}


def anchor(text: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "", re.sub(r"\s+", "-", text.casefold()))


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def humanize_status(status: str) -> str:
    return STATUS_LABELS.get(status, status.replace("_", " "))


def humanize_scope(scope: str) -> str:
    return SCOPE_LABELS.get(scope, scope.replace("-", " ").title())


def recent_year_range(core: list[dict], cutoff_date: str, start_year: int = RECENT_START_YEAR) -> tuple[int, int]:
    cutoff_year = int(cutoff_date[:4])
    max_core_year = max((paper["year"] for paper in core), default=start_year)
    return start_year, max(start_year, cutoff_year, max_core_year)


def status_text(block: dict, *, url: str | None = None, compact: bool = False) -> str:
    status = block.get("status", "not_reported")
    label = humanize_status(status) if compact else status
    artifact_url = url if url is not None else block.get("url", "")
    return f"[{label}]({artifact_url})" if artifact_url else label


def dataset_detail_text(paper: dict) -> str:
    dataset = paper["dataset"]
    dataset_names = dataset.get("names") or []
    description = ", ".join(dataset_names) if dataset_names else dataset["summary"]
    data_url = paper.get("urls", {}).get("data", "")
    if not data_url:
        return f"`{dataset['status']}`: {description}"
    linked_description = ", ".join(f"[{name}]({data_url})" for name in dataset_names)
    if not linked_description:
        linked_description = f"[{description}]({data_url})"
    return f"[{dataset['status']}]({data_url}): {linked_description}"


def compact_artifact_text(block: dict, url: str = "") -> str:
    return status_text(block, url=url, compact=True)


def relative_link(path: Path, readme: Path) -> str:
    return Path(os.path.relpath(path.resolve(), start=readme.parent.resolve())).as_posix()


def latest_priority(paper: dict) -> tuple:
    """Prefer high-evidence, reusable and top-venue work in the README sampler."""
    evidence_score = {"project-page": 4, "full-text": 4, "abstract": 2, "metadata-only": 0}.get(
        paper.get("evidence_level"), 1
    )
    reusable = int(paper["code"].get("status") in PUBLIC_CODE_STATUSES)
    reusable += int(paper["dataset"].get("status") in ACCESSIBLE_DATA_STATUSES)
    return (
        -paper["year"],
        -int(bool(paper.get("top_venue"))),
        -evidence_score,
        -reusable,
        paper["title"].casefold(),
    )


def operational_coverage_text(top_counts: Counter) -> str:
    total = sum(top_counts.values())
    return (
        "In this repository, complete top-venue coverage means a closed, auditable set: **DAC, ICCAD, DATE, ASP-DAC, "
        f"ISPD, ECTC, EPEPS**. This is an operational definition, not a judgment about conference rankings. Each of the {total} admitted DOIs "
        "is bound to a catalog row. The inventory aims to account for every matching paper in that set, but inaccessible or rate-limited proceedings "
        "prevent a mathematical completeness claim. Related EDA is included only as a representative reference set."
    )


def paper_card(paper: dict) -> str:
    baselines = ", ".join(paper["baselines"].get("names") or []) or paper["baselines"]["summary"]
    metrics = ", ".join(paper["evaluation"].get("metrics_mentioned") or []) or "not explicitly listed in the accessible sources"
    tags = ", ".join(f"`{topic}`" for topic in paper["topics"])
    authors = ", ".join(paper["authors"][:8])
    if len(paper["authors"]) > 8:
        authors += ", et al."
    return "\n".join(
        [
            f"### {paper['title']}",
            "",
            f"- **Metadata:** {paper['year']} · {paper['venue']} · {authors or 'authors not reported'} · [paper]({paper['primary_url']})",
            f"- **Scope and topics:** `{paper['scope']}` · {tags}",
            f"- **Code:** {status_text(paper['code'])}: {paper['code']['summary']}",
            f"- **Dataset or data source:** {dataset_detail_text(paper)}",
            f"- **Application scenario:** {paper['application_scenario']['summary']}",
            f"- **Problem addressed:** `{paper['problem_solved']['status']}`: {paper['problem_solved']['summary']}",
            f"- **Final evaluation:** `{paper['evaluation']['status']}`: {paper['evaluation']['summary']} Metrics: {metrics}.",
            f"- **Baselines:** `{paper['baselines']['status']}`: {baselines}",
            f"- **Evidence boundary:** `{paper['evidence_level']}`; checked on {paper['verification']['checked_on']}.",
            "",
        ]
    )


def render_topic(
    topic: dict,
    papers: list[dict],
    tagged_count: int | None = None,
    *,
    readme_link: str = "../../README.md",
) -> str:
    papers = sorted(papers, key=lambda paper: (-paper["year"], paper["title"].casefold()))
    is_related_page = topic["name"] == "Related EDA references"
    if is_related_page:
        introduction = (
            f"{len(papers)} related EDA references are listed here. Detailed fields come from `data/papers.json`; "
            "`not_reported` means that the accessible evidence does not state the field. Not reported does not mean absent."
        )
    else:
        tagged_count = len(papers) if tagged_count is None else tagged_count
        introduction = (
            f"{len(papers)} papers are assigned to this primary topic; {tagged_count} PCB-core papers carry it as a primary or additional tag. "
            "Detailed fields come from `data/papers.json`; `not_reported` means that the accessible evidence does not state the field. "
            "Not reported does not mean absent."
        )
    lines = [
        f"# {topic['name']}",
        "",
        f"[Back to README]({readme_link}) · [Catalog table](#catalog) · [Paper cards](#paper-cards)",
        "",
        introduction,
        "",
        "## Catalog",
        "",
        "| Year | Paper | Venue | Code | Evidence |",
        "|---:|---|---|---|---|",
    ]
    for paper in papers:
        top = f" · **{paper['top_venue']}**" if paper.get("top_venue") else ""
        lines.append(
            f"| {paper['year']} | [{md_escape(paper['title'])}](#{anchor(paper['title'])}) | "
            f"{md_escape(paper['venue'])}{top} | {compact_artifact_text(paper['code'])} | {humanize_status(paper['evidence_level'])} |"
        )
    lines.extend(["", "## Paper cards", ""])
    for paper in papers:
        lines.append(paper_card(paper))
    return "\n".join(lines).rstrip() + "\n"


def open_artifact_papers(papers: list[dict]) -> list[dict]:
    admitted = [
        paper
        for paper in papers
        if paper["code"].get("status") in PUBLIC_CODE_STATUSES
        or paper["dataset"].get("status") in ACCESSIBLE_DATA_STATUSES
    ]
    rows = []
    seen: set[str] = set()
    for paper in sorted(admitted, key=lambda item: (-item["year"], item["title"].casefold())):
        key = str(paper.get("id") or f"{paper['year']}::{paper['title']}")
        if key in seen:
            continue
        seen.add(key)
        rows.append(paper)
    return rows


def render_open_artifacts(
    papers: list[dict],
    topic_map: dict[str, dict],
    *,
    readme_link: str = "../README.md",
) -> str:
    rows = open_artifact_papers(papers)
    lines = [
        "# Open code and data",
        "",
        f"[Back to README]({readme_link})",
        "",
        "This page includes both PCB-core and related-EDA catalog records with publicly reusable code and/or "
        "reader-accessible data statuses. It is a generated view of the catalog, not a completeness claim.",
        "",
        "| Year | Paper | Scope | Primary topic | Code | Data | Evidence |",
        "|---:|---|---|---|---|---|---|",
    ]
    for paper in rows:
        topic = topic_map.get(paper["primary_topic"], {}).get("name", paper["primary_topic"])
        lines.append(
            f"| {paper['year']} | [{md_escape(paper['title'])}]({paper['primary_url']}) | {humanize_scope(paper['scope'])} | "
            f"{md_escape(topic)} | "
            f"{compact_artifact_text(paper['code'], paper.get('urls', {}).get('code', ''))} | "
            f"{compact_artifact_text(paper['dataset'], paper.get('urls', {}).get('data', ''))} | "
            f"{humanize_status(paper['evidence_level'])} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--analysis", type=Path, default=Path("analysis/summary.json"))
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--topics-dir", type=Path, default=Path("docs/topics"))
    args = parser.parse_args()
    payload = json.loads(args.catalog.read_text(encoding="utf-8"))
    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    papers = payload["papers"]
    core = [paper for paper in papers if paper["scope"] == "pcb-core"]
    related = [paper for paper in papers if paper["scope"] == "related-eda"]
    topic_map = {topic["id"]: topic for topic in payload["topics"]}
    expected_topic_paths = {
        args.topics_dir / f"{topic_id}.md"
        for topic_id in topic_map
        if any(paper["primary_topic"] == topic_id for paper in core)
    }
    stale_topic_paths = set(args.topics_dir.glob("*.md")) - expected_topic_paths
    if stale_topic_paths:
        stale = ", ".join(sorted(path.name for path in stale_topic_paths))
        raise RuntimeError(f"stale generated topic pages: {stale}")
    related_path = args.topics_dir.parent / "related-eda.md"
    if not related and related_path.exists():
        raise RuntimeError(f"stale generated related-EDA page: {related_path}")
    args.topics_dir.mkdir(parents=True, exist_ok=True)
    nav_rows = []
    for topic_id, topic in topic_map.items():
        topic_papers = [paper for paper in core if paper["primary_topic"] == topic_id]
        if not topic_papers:
            continue
        path = args.topics_dir / f"{topic_id}.md"
        tagged_count = sum(topic_id in paper.get("topics", []) for paper in core)
        path.write_text(
            render_topic(
                topic,
                topic_papers,
                tagged_count,
                readme_link=relative_link(args.readme, path),
            ),
            encoding="utf-8",
        )
        nav_rows.append((topic_id, topic, len(topic_papers), tagged_count, path))
    related_link = relative_link(related_path, args.readme)
    if related:
        related_topic = {"name": "Related EDA references"}
        related_path.write_text(
            render_topic(
                related_topic,
                related,
                readme_link=relative_link(args.readme, related_path),
            ),
            encoding="utf-8",
        )

    open_artifacts_path = args.topics_dir.parent / "open-artifacts.md"
    open_artifacts_path.write_text(
        render_open_artifacts(
            papers,
            topic_map,
            readme_link=relative_link(args.readme, open_artifacts_path),
        ),
        encoding="utf-8",
    )

    pcb_analysis = analysis["scopes"]["pcb-core"]
    top_keywords = list(pcb_analysis["keyword_document_frequency"].items())[:12]
    top_counts = Counter(paper["top_venue"] for paper in core if paper.get("top_venue"))
    recent_start_year, recent_end_year = recent_year_range(core, payload["cutoff_date"])
    recent_year_label = f"{recent_start_year}-{recent_end_year}"
    recent_core_count = sum(
        recent_start_year <= paper["year"] <= recent_end_year for paper in core
    )
    latest = []
    for topic_id in topic_map:
        candidates = [
            paper
            for paper in core
            if (
                recent_start_year <= paper["year"] <= recent_end_year
                and paper["primary_topic"] == topic_id
            )
        ]
        latest.extend(sorted(candidates, key=latest_priority)[:2])
    latest = sorted(latest, key=latest_priority)
    readme = [
        "# Awesome PCB Design Papers",
        "",
        "> A source-checked, evidence-card catalog for PCB design automation and transferable EDA research.",
        "",
        f"**Cutoff date:** {payload['cutoff_date']} · **PCB core:** {len(core)} papers · **Related EDA:** {len(related)} papers · **Topics:** {len(nav_rows)}",
        "",
        "The repository follows the familiar Awesome-list layout. Each paper also has fields for code status, datasets or data sources, application scenario, problem addressed, final evaluation, baselines, and the evidence boundary.",
        "",
        "## Scope",
        "",
        "- **PCB core:** PCB, PWB, or PCBA is the object of design, placement, routing, SI/PI/EMC, reliability, DFX, or testing.",
        "- **Related EDA references:** Transferable methods for chips, packages, chiplets, and LLM or agentic EDA are counted separately and are not presented as PCB papers.",
        "- **Excluded:** Application papers that use a PCB only as an experimental carrier, electronic-waste or pollution studies, patents, book chapters, errata, and repeated model variants without an independent task or data contribution.",
        "",
        "## Start here",
        "",
        f"Begin with the [open code and data view]({relative_link(open_artifacts_path, args.readme)}), then [browse by topic](#browse-by-topic), [inspect top-venue coverage](#operational-top-venue-coverage), or [read the evidence and status semantics](#evidence-and-status-semantics).",
        "",
        "## First use",
        "",
        f"Open the [machine-readable catalog]({relative_link(args.catalog, args.readme)}) to read or compare records without installing any linked project. Each record keeps its primary paper URL, scope, topics, code/data status, application scenario, problem, evaluation, baselines, evidence level, and verification date.",
        "",
        "Run this from the repository root; the read-only command counts current PCB-core records whose primary topic is routing (observed locally on 2026-09-12):",
        "",
        "```console",
        "$ python3 -c 'import json; p=json.load(open(\"data/papers.json\")); print(sum(x[\"scope\"] == \"pcb-core\" and x[\"primary_topic\"] == \"routing\" for x in p[\"papers\"]))'",
        str(sum(paper["scope"] == "pcb-core" and paper["primary_topic"] == "routing" for paper in papers)),
        "```",
        "",
        f"To inspect a linked implementation or dataset, use the [open code and data view]({relative_link(open_artifacts_path, args.readme)}) and follow only entries whose status and URL are marked as verified.",
        "",
        "## Browse by topic",
        "",
        "| Topic | Primary papers | All tagged papers |",
        "|---|---:|---:|",
    ]
    for topic_id, topic, primary_count, tagged_count, topic_path in nav_rows:
        readme.append(
            f"| [{topic['name']}]({relative_link(topic_path, args.readme)}) | {primary_count} | {tagged_count} |"
        )
    if related:
        readme.append(f"| [Related EDA references]({related_link}) | {len(related)} | {len(related)} |")
    readme.extend(
        [
            "",
            f"## Selected recent PCB-core papers ({recent_year_label})",
            "",
            f"The complete {recent_year_label} PCB-core corpus contains {recent_core_count} papers. This selected view applies the rule: from {recent_start_year} onward, up to two per primary topic, ranked by year, top-venue, evidence depth, and reusable artifacts.",
            "",
            "| Year | Paper | Primary topic | Code | Data | Evidence |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for paper in latest:
        readme.append(
            f"| {paper['year']} | [{md_escape(paper['title'])}]({paper['primary_url']}) | "
            f"{md_escape(topic_map[paper['primary_topic']]['name'])} | "
            f"{compact_artifact_text(paper['code'], paper.get('urls', {}).get('code', ''))} | "
            f"{compact_artifact_text(paper['dataset'], paper.get('urls', {}).get('data', ''))} | "
            f"{humanize_status(paper['evidence_level'])} |"
        )
    metadata_top_counts = Counter(
        paper["top_venue"]
        for paper in core
        if paper.get("top_venue") and paper.get("evidence_level") == "metadata-only"
    )
    evidence_top_counts = Counter(
        paper["top_venue"]
        for paper in core
        if paper.get("top_venue") and paper.get("evidence_level") != "metadata-only"
    )
    readme.extend(
        [
            "",
            "## Operational top-venue coverage",
            "",
            operational_coverage_text(top_counts),
            "",
            "| Venue | Included | Metadata-only | Evidence-enriched |",
            "|---|---:|---:|---:|",
        ]
    )
    for venue in ("DAC", "ICCAD", "DATE", "ASP-DAC", "ISPD", "ECTC", "EPEPS"):
        readme.append(
            f"| {venue} | {top_counts.get(venue, 0)} | {metadata_top_counts.get(venue, 0)} | "
            f"{evidence_top_counts.get(venue, 0)} |"
        )
    readme.extend(
        [
            "",
            "## Keyword and trend analysis",
            "",
            "Keyword counts use a controlled regular-expression vocabulary over every title. Scenario and problem summaries are included only for records supported by an abstract, full text, or project page. **Document frequency** counts a keyword at most once per paper. PCB core and Related EDA are analyzed separately.",
            "",
            f"![PCB keyword distribution]({relative_link(Path('assets/pcb_core_keyword_distribution.svg'), args.readme)})",
            "",
            f"![PCB publication trend]({relative_link(Path('assets/pcb_core_year_trend.svg'), args.readme)})",
            "",
            f"![PCB topic distribution]({relative_link(Path('assets/pcb_core_topic_distribution.svg'), args.readme)})",
            "",
            "Top controlled keywords: " + ", ".join(f"`{key}` ({value})" for key, value in top_keywords) + ".",
            "",
            "## Data source and refresh",
            "",
            f"Canonical source: [{relative_link(args.catalog, args.readme)}]({relative_link(args.catalog, args.readme)}). README, topic pages, and the open-artifacts view are generated by [`scripts/render_catalog.py`]({relative_link(Path('scripts/render_catalog.py'), args.readme)}). Update the catalog source first, then run:",
            "",
            "```console",
            "python3 scripts/validate_catalog.py data/papers.json --require-audit",
            "python3 scripts/analyze_catalog.py",
            "python3 scripts/render_catalog.py",
            "```",
            "",
            "## Evidence and status semantics",
            "",
            "- `open` means a code/data URL resolved during verification; `announced_or_mentioned_unverified` is not counted as released.",
            "- `not_found` means no repository was found in the inspected paper/project sources; it does **not** prove that code does not exist.",
            "- `not_reported_in_accessible_source` means the accessible metadata/abstract/full text did not state the field.",
            "- `reported_link_unreachable` means the paper names an artifact URL, but the cutoff-date link check could not retrieve it.",
            "- `metadata-only`, `abstract`, `full-text`, and `project-page` expose how deep the extraction went.",
            "",
            "See "
            f"[methodology]({relative_link(Path('docs/methodology.md'), args.readme)}), "
            f"[GLM/DeepSeek consultation notes]({relative_link(Path('docs/consultation-notes.md'), args.readme)}), "
            f"[top-venue audit]({relative_link(Path('data/top_venue_audit.json'), args.readme)}), "
            f"[machine-readable catalog]({relative_link(Path('data/papers.json'), args.readme)}), "
            f"[trend outputs]({relative_link(Path('analysis/summary.json'), args.readme)}), and the "
            f"[URL-check snapshot]({relative_link(Path('analysis/link_check.json'), args.readme)}).",
            "",
            "## Coverage boundary",
            "",
            "This is a structured, cutoff-dated catalog: it is not a claim of absolute global exhaustiveness. Publisher indexing delays, title changes, inaccessible proceedings, and papers that never use board-specific terms can still create gaps. Please open an issue or PR with a primary source and the required evidence fields.",
            "",
            "## Contributing",
            "",
            f"See [CONTRIBUTING.md]({relative_link(Path('CONTRIBUTING.md'), args.readme)}). Add or correct records in [{relative_link(args.catalog, args.readme)}]({relative_link(args.catalog, args.readme)}) with a DOI/publisher/arXiv primary link, scope/topics, explicit code/data/scenario/problem/evaluation/baseline statuses, and source/locator/check date. Run the validation, analysis, and render commands above; generated pages should change only as a consequence of the source edit.",
        ]
    )
    args.readme.write_text("\n".join(readme).rstrip() + "\n", encoding="utf-8")
    print(f"rendered README and {len(nav_rows)} topic pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
