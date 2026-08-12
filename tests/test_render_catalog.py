#!/usr/bin/env python3
"""Focused reader-view regression tests for the catalog renderer."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_renderer():
    path = ROOT / "scripts" / "render_catalog.py"
    spec = importlib.util.spec_from_file_location("render_catalog", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_paper(*, identifier: str = "paper-1", data_url: str = "") -> dict:
    return {
        "id": identifier,
        "title": "Example PCB paper",
        "authors": ["A. Author"],
        "year": 2026,
        "venue": "Example Venue",
        "primary_url": "https://example.test/paper",
        "scope": "pcb-core",
        "topics": ["placement", "routing"],
        "primary_topic": "placement",
        "top_venue": None,
        "evidence_level": "abstract",
        "urls": {"code": "https://example.test/code", "data": data_url},
        "code": {
            "status": "open",
            "summary": "Code summary.",
            "url": "https://example.test/code",
        },
        "dataset": {
            "status": "open" if data_url else "not_reported_in_accessible_source",
            "summary": "Dataset summary.",
            "names": ["ExampleData"],
        },
        "application_scenario": {"status": "reported", "summary": "Scenario."},
        "problem_solved": {"status": "reported", "summary": "Problem."},
        "evaluation": {
            "status": "reported",
            "summary": "Evaluation.",
            "metrics_mentioned": ["wirelength"],
        },
        "baselines": {"status": "named", "summary": "Baseline.", "names": ["SA"]},
        "verification": {"checked_on": "2026-08-11"},
    }


class RenderCatalogReaderTests(unittest.TestCase):
    def test_recent_priority_uses_the_reader_artifact_status_sets(self) -> None:
        renderer = load_renderer()
        reusable = sample_paper()
        reusable["code"]["status"] = "open_archived"
        reusable["dataset"]["status"] = "public_benchmarks"
        unavailable = sample_paper(identifier="unavailable")
        unavailable["code"]["status"] = "not_found"
        unavailable["dataset"]["status"] = "reported"
        self.assertLess(
            renderer.latest_priority(reusable),
            renderer.latest_priority(unavailable),
        )

    def test_dataset_url_is_distinct_and_clickable(self) -> None:
        renderer = load_renderer()
        paper = sample_paper(data_url="https://example.test/data")
        card = renderer.paper_card(paper)
        dataset_line = next(line for line in card.splitlines() if "Dataset or data source" in line)
        self.assertIn("[open](https://example.test/data)", dataset_line)
        self.assertIn("[ExampleData](https://example.test/data)", dataset_line)
        self.assertNotIn("https://example.test/code", dataset_line)

    def test_topic_intro_keeps_disclaimer_and_cards_do_not_repeat_it(self) -> None:
        renderer = load_renderer()
        rendered = renderer.render_topic(
            {"id": "placement", "name": "Placement"},
            [sample_paper(data_url="https://example.test/data")],
            tagged_count=2,
        )
        self.assertEqual(rendered.count("Not reported does not mean absent."), 1)
        self.assertIn("1 papers are assigned to this primary topic; 2 PCB-core papers", rendered)
        self.assertIn("[Back to README]", rendered)
        self.assertIn("[Catalog table](#catalog)", rendered)
        self.assertIn("[Paper cards](#paper-cards)", rendered)
        card = rendered.split("## Paper cards", 1)[1]
        self.assertNotIn("Not reported does not mean absent.", card)

    def test_open_artifact_admission_is_status_based_and_deduplicated(self) -> None:
        renderer = load_renderer()
        code_only = sample_paper(identifier="code-only")
        data_only = sample_paper(identifier="data-only", data_url="https://example.test/data")
        data_only["code"]["status"] = "not_found"
        duplicate = dict(data_only)
        duplicate["title"] = "Duplicate row"
        inaccessible = sample_paper(identifier="inaccessible")
        inaccessible["code"]["status"] = "announced_or_mentioned_unverified"
        inaccessible["dataset"]["status"] = "reported"
        rows = renderer.open_artifact_papers([code_only, data_only, duplicate, inaccessible])
        self.assertEqual([paper["id"] for paper in rows], ["data-only", "code-only"])

    def test_open_artifact_view_exposes_both_live_catalog_scopes(self) -> None:
        renderer = load_renderer()
        payload = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        rendered = renderer.render_open_artifacts(
            payload["papers"],
            {topic["id"]: topic for topic in payload["topics"]},
        )
        rows = [
            line
            for line in rendered.splitlines()
            if line.startswith("| ") and line[2:6].isdigit()
        ]
        scopes = Counter(line.split(" | ")[2] for line in rows)
        self.assertEqual(len(rows), 27)
        self.assertEqual(scopes, {"PCB core": 13, "Related EDA": 14})
        self.assertIn("both PCB-core and related-EDA catalog records", rendered)

    def test_recent_heading_adapts_to_2027_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            payload = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
            future = copy.deepcopy(next(paper for paper in payload["papers"] if paper["scope"] == "pcb-core"))
            future["id"] = "future-2027-reader-test"
            future["title"] = "Future 2027 PCB reader test"
            future["year"] = 2027
            future["primary_url"] = "https://example.test/future-2027"
            payload["papers"].append(future)
            catalog_path = output / "catalog.json"
            catalog_path.write_text(json.dumps(payload), encoding="utf-8")
            readme = output / "README.md"
            topics = output / "docs" / "topics"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "render_catalog.py"),
                    "--catalog",
                    str(catalog_path),
                    "--analysis",
                    str(ROOT / "analysis" / "summary.json"),
                    "--readme",
                    str(readme),
                    "--topics-dir",
                    str(topics),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rendered = readme.read_text(encoding="utf-8")
            self.assertIn("## Selected recent PCB-core papers (2024-2027)", rendered)
            self.assertIn("complete 2024-2027 PCB-core corpus contains 122 papers", rendered)

    def test_generated_readme_exposes_reader_tables_and_counts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            readme = output / "README.md"
            topics = output / "docs" / "topics"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "render_catalog.py"),
                    "--catalog",
                    str(ROOT / "data" / "papers.json"),
                    "--analysis",
                    str(ROOT / "analysis" / "summary.json"),
                    "--readme",
                    str(readme),
                    "--topics-dir",
                    str(topics),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rendered = readme.read_text(encoding="utf-8")
            self.assertIn("## Selected recent PCB-core papers (2024-2026)", rendered)
            self.assertIn("complete 2024-2026 PCB-core corpus contains 121 papers", rendered)
            self.assertIn("up to two per primary topic", rendered)
            self.assertIn("| Topic | Primary papers | All tagged papers |", rendered)
            self.assertIn("| [Placement and legalization](docs/topics/placement.md) | 35 | 43 |", rendered)
            self.assertIn("| Venue | Included | Metadata-only | Evidence-enriched |", rendered)
            self.assertIn("| DAC | 63 | 57 | 6 |", rendered)
            self.assertIn("[open code and data view](docs/open-artifacts.md)", rendered)
            artifact_page = (output / "docs" / "open-artifacts.md").read_text(encoding="utf-8")
            self.assertEqual(artifact_page.count("| 2026 |"), 7)


if __name__ == "__main__":
    unittest.main()
