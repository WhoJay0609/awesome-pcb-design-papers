#!/usr/bin/env python3
"""Render the JSON catalog into an Awesome-style README and topic pages."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path


def anchor(text: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "", re.sub(r"\s+", "-", text.casefold()))


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def status_text(block: dict) -> str:
    status = block.get("status", "not_reported")
    url = block.get("url", "")
    return f"[{status}]({url})" if url else status


def relative_link(path: Path, readme: Path) -> str:
    return Path(os.path.relpath(path.resolve(), start=readme.parent.resolve())).as_posix()


def latest_priority(paper: dict) -> tuple:
    """Prefer high-evidence, reusable and top-venue work in the README sampler."""
    evidence_score = {"project-page": 4, "full-text": 4, "abstract": 2, "metadata-only": 0}.get(
        paper.get("evidence_level"), 1
    )
    reusable = int(paper["code"].get("status") in {"open", "partial_open", "utility_open"})
    reusable += int(paper["dataset"].get("status") == "open")
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
        "“顶会全部覆盖”采用封闭、可审计的操作性集合：**DAC, ICCAD, DATE, ASP-DAC, "
        f"ISPD, ECTC, EPEPS**。它不是对任何排名体系的价值判断。{total} 条 admitted DOI "
        "逐行绑定目录；这是以穷尽为目标的封闭清单，但受不可访问/限流 proceedings 影响，"
        "不作数学完备性承诺。Related EDA 只做代表性参考。"
    )


def paper_card(paper: dict) -> str:
    dataset_names = paper["dataset"].get("names") or []
    dataset = ", ".join(dataset_names) if dataset_names else paper["dataset"]["summary"]
    baselines = ", ".join(paper["baselines"].get("names") or []) or paper["baselines"]["summary"]
    metrics = ", ".join(paper["evaluation"].get("metrics_mentioned") or []) or "未在可访问来源中明确列出"
    tags = ", ".join(f"`{topic}`" for topic in paper["topics"])
    authors = ", ".join(paper["authors"][:8])
    if len(paper["authors"]) > 8:
        authors += ", et al."
    return "\n".join(
        [
            f"### {paper['title']}",
            "",
            f"- **元数据：** {paper['year']} · {paper['venue']} · {authors or 'authors not reported'} · [paper]({paper['primary_url']})",
            f"- **范围/主题：** `{paper['scope']}` · {tags}",
            f"- **代码：** {status_text(paper['code'])} — {paper['code']['summary']}",
            f"- **数据集/数据来源：** `{paper['dataset']['status']}` — {dataset}",
            f"- **应用场景：** {paper['application_scenario']['summary']}",
            f"- **解决问题：** `{paper['problem_solved']['status']}` — {paper['problem_solved']['summary']}",
            f"- **最终测试：** `{paper['evaluation']['status']}` — {paper['evaluation']['summary']} 指标：{metrics}。",
            f"- **Baselines：** `{paper['baselines']['status']}` — {baselines}",
            f"- **证据边界：** `{paper['evidence_level']}`；核验日期 {paper['verification']['checked_on']}。未报告不等于不存在。",
            "",
        ]
    )


def render_topic(topic: dict, papers: list[dict]) -> str:
    papers = sorted(papers, key=lambda paper: (-paper["year"], paper["title"].casefold()))
    lines = [
        f"# {topic['name_zh']} / {topic['name_en']}",
        "",
        f"共 {len(papers)} 篇主分类论文。详细字段均来自 `data/papers.json`；`not_reported` 表示当前可访问证据未说明。",
        "",
        "| Year | Paper | Venue | Code | Evidence |",
        "|---:|---|---|---|---|",
    ]
    for paper in papers:
        top = f" · **{paper['top_venue']}**" if paper.get("top_venue") else ""
        lines.append(
            f"| {paper['year']} | [{md_escape(paper['title'])}](#{anchor(paper['title'])}) | "
            f"{md_escape(paper['venue'])}{top} | {paper['code']['status']} | {paper['evidence_level']} |"
        )
    lines.extend(["", "## Paper cards", ""])
    for paper in papers:
        lines.append(paper_card(paper))
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
        path.write_text(render_topic(topic, topic_papers), encoding="utf-8")
        nav_rows.append((topic_id, topic, len(topic_papers), path))
    related_link = relative_link(related_path, args.readme)
    if related:
        related_topic = {"name_zh": "相关 EDA 自动化参考", "name_en": "Related EDA References"}
        related_path.write_text(render_topic(related_topic, related), encoding="utf-8")

    pcb_analysis = analysis["scopes"]["pcb-core"]
    top_keywords = list(pcb_analysis["keyword_document_frequency"].items())[:12]
    top_counts = Counter(paper["top_venue"] for paper in core if paper.get("top_venue"))
    latest = []
    for topic_id in topic_map:
        candidates = [
            paper
            for paper in core
            if paper["year"] >= 2024 and paper["primary_topic"] == topic_id
        ]
        latest.extend(sorted(candidates, key=latest_priority)[:2])
    latest = sorted(latest, key=latest_priority)
    readme = [
        "# Awesome PCB Design Papers",
        "",
        "> A source-checked, evidence-card catalog for PCB design automation and transferable EDA research.",
        "",
        f"**检索截止：{payload['cutoff_date']}** · **PCB core：{len(core)} 篇** · **Related EDA：{len(related)} 篇** · **主题：{len(nav_rows)} 个**",
        "",
        "本仓库模仿 Awesome 列表的可浏览性，但不只保存链接：每篇论文都明确记录代码状态、数据集/数据来源、应用场景、解决的问题、最终测试和 baselines，并给出证据边界。",
        "",
        "## Scope",
        "",
        "- **PCB core**：PCB/PWB/PCBA 是论文的设计、布局、布线、SI/PI/EMC、可靠性、DFX 或测试对象。",
        "- **Related EDA References**：芯片、封装、Chiplet、LLM/agentic EDA 等可迁移方法；单独统计，不冒充 PCB 论文。",
        "- **排除**：PCB 仅作为实验载板的应用论文、电子垃圾/污染物研究、专利、书籍章节、勘误，以及缺乏独立任务/数据贡献的重复模型变体。",
        "",
        "## Browse by topic",
        "",
        "| Topic | Papers | Description |",
        "|---|---:|---|",
    ]
    for topic_id, topic, count, topic_path in nav_rows:
        readme.append(
            f"| [{topic['name_zh']}]({relative_link(topic_path, args.readme)}) | {count} | {topic['name_en']} |"
        )
    if related:
        readme.append(f"| [相关 EDA 自动化参考]({related_link}) | {len(related)} | Transferable non-PCB methods |")
    readme.extend(
        [
            "",
            "## Latest PCB-core papers (2024–2026)",
            "",
        ]
    )
    for paper in latest:
        venue = f" · **{paper['top_venue']}**" if paper.get("top_venue") else ""
        readme.append(
            f"- **{paper['year']}** · [{paper['title']}]({paper['primary_url']}) — {paper['venue']}{venue}"
        )
    readme.extend(
        [
            "",
            "## Operational top-venue coverage",
            "",
            operational_coverage_text(top_counts),
            "",
            "| Venue | Included PCB papers |",
            "|---|---:|",
        ]
    )
    for venue in ("DAC", "ICCAD", "DATE", "ASP-DAC", "ISPD", "ECTC", "EPEPS"):
        readme.append(f"| {venue} | {top_counts.get(venue, 0)} |")
    readme.extend(
        [
            "",
            "## Keyword and trend analysis",
            "",
            "关键词采用受控正则词表，对每篇题名与本仓库原创摘要做 **document frequency**：一个关键词在同一论文中最多计一次。PCB core 与 Related EDA 分开统计。",
            "",
            f"![PCB keyword distribution]({relative_link(Path('assets/pcb_core_keyword_distribution.svg'), args.readme)})",
            "",
            f"![PCB publication trend]({relative_link(Path('assets/pcb_core_year_trend.svg'), args.readme)})",
            "",
            f"![PCB topic distribution]({relative_link(Path('assets/pcb_core_topic_distribution.svg'), args.readme)})",
            "",
            "Top controlled keywords: " + ", ".join(f"`{key}` ({value})" for key, value in top_keywords) + ".",
            "",
            "Reproduce with:",
            "",
            "```bash",
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
            "This is a structured, cutoff-dated catalog—not a claim of absolute global exhaustiveness. Publisher indexing delays, title changes, inaccessible proceedings, and papers that never use board-specific terms can still create gaps. Please open an issue or PR with a primary source and the required evidence fields.",
            "",
            "## Contributing",
            "",
            f"See [CONTRIBUTING.md]({relative_link(Path('CONTRIBUTING.md'), args.readme)}). New records must include a DOI/publisher/arXiv link and explicit status for code, data, scenario, problem, evaluation, and baselines.",
        ]
    )
    args.readme.write_text("\n".join(readme).rstrip() + "\n", encoding="utf-8")
    print(f"rendered README and {len(nav_rows)} topic pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
