#!/usr/bin/env python3
"""Regression tests for merge identity and renderer output routing."""

from __future__ import annotations

import importlib.util
import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PipelineContractTests(unittest.TestCase):
    @staticmethod
    def curated_record(identifier: str, title: str, authors: list[str], year: int) -> dict:
        return {
            "id": identifier,
            "title": title,
            "authors": authors,
            "year": year,
            "venue": "Example Venue",
            "publication_state": "peer-reviewed",
            "primary_url": f"https://doi.org/{identifier.removeprefix('doi:')}",
            "scope": "pcb-core",
            "topics": ["routing"],
            "primary_topic": "routing",
            "evidence_level": "metadata-only",
            "application_scenario": "Example scenario",
            "problem_solved": "Example problem",
        }

    def test_title_collision_requires_year_and_author_corroboration(self) -> None:
        module = load_script("complete_top_venue_catalog")
        catalog = {
            "papers": [
                {
                    "id": "doi:10.1000/existing",
                    "title": "Same normalized title",
                    "authors": ["Alice Smith"],
                    "year": 2020,
                    "scope": "pcb-core",
                    "primary_topic": "routing",
                    "top_venue": None,
                }
            ]
        }
        fetched = {
            "10.1000/new": (
                "DAC",
                {
                    "title": ["Same normalized title"],
                    "author": [{"given": "Bob", "family": "Jones"}],
                    "published": {"date-parts": [[2021]]},
                    "container-title": ["DAC"],
                },
            )
        }
        with self.assertRaisesRegex(RuntimeError, "Unsafe normalized-title collision"):
            module.merge_catalog(catalog, fetched)

    def test_top_venue_generator_preserves_reproducibility_boundary(self) -> None:
        module = load_script("complete_top_venue_catalog")
        self.assertEqual(
            module.AUDIT_REPRODUCIBILITY_LIMIT,
            "The fixed admitted DOI inventory supports metadata regeneration and row-level falsification, "
            "but is not a replayable discovery log or a mathematical claim of global bibliographic completeness.",
        )

    def test_producers_do_not_copy_title_punctuation_into_authored_summaries(self) -> None:
        top_module = load_script("complete_top_venue_catalog")
        top_record = top_module.make_metadata_record(
            {
                "title": ["PCB routing \u2014 a case study"],
                "published": {"date-parts": [[2025]]},
                "container-title": ["Example conference"],
                "author": [{"given": "Alice", "family": "Smith"}],
            },
            "10.1000/example-top",
            "DAC",
        )
        build_module = load_script("build_catalog")
        built_record = build_module.make_record(
            {"topics_suggested": ["routing"], "primary_topic_suggested": "routing"},
            {
                "externalIds": {"DOI": "10.1000/example-build"},
                "title": "PCB routing \u2014 a second case",
                "abstract": "We propose a routing method.",
                "authors": [{"name": "Alice Smith"}],
                "year": 2025,
                "venue": "Example conference",
            },
            "doi:10.1000/example-build",
        )
        for record in (top_record, built_record):
            self.assertIn("\u2014", record["title"])
            for field in ("code", "dataset", "application_scenario", "problem_solved", "evaluation", "baselines"):
                self.assertNotRegex(record[field]["summary"], r"[\u2013\u2014\u2018\u2019\u201c\u201d]")

    def test_metadata_only_status_boundary_matches_live_catalog(self) -> None:
        module = load_script("complete_top_venue_catalog")
        audit = json.loads((ROOT / "data" / "top_venue_audit.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        self.assertIn(module.METADATA_ONLY_STATUS_LIMIT, audit["limitations"])
        metadata_only = [paper for paper in catalog["papers"] if paper["evidence_level"] == "metadata-only"]
        self.assertEqual({paper["code"]["status"] for paper in metadata_only}, {"not_found", "not_reported_in_accessible_source"})
        for field in ("dataset", "evaluation", "baselines"):
            self.assertEqual(
                {paper[field]["status"] for paper in metadata_only},
                {"not_reported_in_accessible_source"},
            )

    def test_related_eda_respects_custom_topics_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            topics_dir = output / "generated" / "cards"
            readme = output / "site" / "index.md"
            readme.parent.mkdir(parents=True)
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
                    str(topics_dir),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((output / "generated" / "related-eda.md").is_file())
            rendered = readme.read_text(encoding="utf-8")
            self.assertIn("(../generated/related-eda.md)", rendered)
            self.assertIn("(../generated/cards/placement.md)", rendered)

    def test_curated_merger_rejects_unsafe_title_collision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            catalog_path = directory_path / "catalog.json"
            records_path = directory_path / "records.json"
            catalog_path.write_text(
                json.dumps(
                    {
                        "papers": [
                            {
                                "id": "doi:10.1000/existing",
                                "title": "Same normalized title",
                                "authors": ["Alice Smith"],
                                "year": 2020,
                                "scope": "pcb-core",
                                "primary_topic": "routing",
                                "top_venue": None,
                                "verification": {"sources": []},
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            records_path.write_text(
                json.dumps(
                    {
                        "records": [
                            {
                                "id": "doi:10.1000/new",
                                "title": "Same normalized title",
                                "authors": ["Bob Jones"],
                                "year": 2021,
                                "venue": "Example Venue",
                                "publication_state": "peer-reviewed",
                                "primary_url": "https://doi.org/10.1000/new",
                                "scope": "pcb-core",
                                "topics": ["routing"],
                                "primary_topic": "routing",
                                "evidence_level": "metadata-only",
                                "application_scenario": "Example scenario",
                                "problem_solved": "Example problem"
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "merge_curated_records.py"),
                    "--catalog",
                    str(catalog_path),
                    "--records",
                    str(records_path),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unsafe normalized-title collision", result.stderr)

    def test_curated_merger_rejects_same_id_rename_collision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            catalog_path = directory_path / "catalog.json"
            records_path = directory_path / "records.json"
            catalog_path.write_text(
                json.dumps(
                    {
                        "papers": [
                            {"id": "doi:10.1000/a", "title": "Original A", "authors": ["Alice Smith"], "year": 2020, "top_venue": None, "verification": {"sources": []}},
                            {"id": "doi:10.1000/b", "title": "Owned title", "authors": ["Bob Jones"], "year": 2021, "top_venue": None, "verification": {"sources": []}},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            records_path.write_text(
                json.dumps({"records": [self.curated_record("doi:10.1000/a", "Owned title", ["Alice Smith"], 2020)]}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "merge_curated_records.py"), "--catalog", str(catalog_path), "--records", str(records_path)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unsafe normalized-title collision", result.stderr)

    def test_curated_merger_removes_stale_title_mapping_after_rename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            catalog_path = directory_path / "catalog.json"
            records_path = directory_path / "records.json"
            catalog_path.write_text(
                json.dumps(
                    {
                        "papers": [
                            {
                                "id": "doi:10.1000/a",
                                "title": "Original title",
                                "authors": ["Alice Smith"],
                                "year": 2020,
                                "top_venue": None,
                                "verification": {"sources": []},
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            records_path.write_text(
                json.dumps(
                    {
                        "records": [
                            self.curated_record("doi:10.1000/a", "Renamed title", ["Alice Smith"], 2020),
                            self.curated_record("doi:10.1000/c", "Original title", ["Carol Chen"], 2022),
                        ]
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "merge_curated_records.py"), "--catalog", str(catalog_path), "--records", str(records_path)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            papers = json.loads(catalog_path.read_text(encoding="utf-8"))["papers"]
            self.assertEqual({paper["id"] for paper in papers}, {"doi:10.1000/a", "doi:10.1000/c"})

    def test_metadata_only_merge_output_passes_catalog_validator(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            catalog = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
            paper = next(
                paper
                for paper in catalog["papers"]
                if paper["evidence_level"] == "metadata-only"
                and paper["top_venue"] is None
                and not paper["urls"]["code"]
                and not paper["urls"]["data"]
            )
            catalog_path = output / "catalog.json"
            records_path = output / "records.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            record = self.curated_record(paper["id"], paper["title"], paper["authors"], paper["year"])
            record.update(
                {
                    "venue": paper["venue"],
                    "publication_state": paper["publication_state"],
                    "primary_url": paper["primary_url"],
                    "scope": paper["scope"],
                    "topics": paper["topics"],
                    "primary_topic": paper["primary_topic"],
                    "application_scenario": paper["application_scenario"]["summary"],
                    "problem_solved": paper["problem_solved"]["summary"],
                }
            )
            records_path.write_text(json.dumps({"records": [record]}), encoding="utf-8")
            merge = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "merge_curated_records.py"), "--catalog", str(catalog_path), "--records", str(records_path)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(merge.returncode, 0, merge.stdout + merge.stderr)
            validate = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_catalog.py"),
                    str(catalog_path),
                    "--audit",
                    str(ROOT / "data" / "top_venue_audit.json"),
                    "--require-audit",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)

    def test_operational_coverage_count_is_derived(self) -> None:
        module = load_script("render_catalog")
        self.assertIn("3 admitted DOIs", module.operational_coverage_text({"DAC": 2, "ICCAD": 1}))

    def test_keyword_analysis_ignores_metadata_only_templates(self) -> None:
        module = load_script("analyze_catalog")
        papers = [
            {
                "title": "PCB placement method",
                "year": 2026,
                "primary_topic": "placement",
                "evidence_level": "metadata-only",
                "application_scenario": {"summary": "Manufacturing and testing."},
                "problem_solved": {"summary": "Inspection quality."},
            },
            {
                "title": "Board method",
                "year": 2026,
                "primary_topic": "testing-inspection",
                "evidence_level": "abstract",
                "application_scenario": {"summary": "Manufacturing."},
                "problem_solved": {"summary": "Testing and inspection."},
            },
        ]
        counts = module.analyze_scope(papers)["keyword_document_frequency"]
        self.assertEqual(counts["placement"], 1)
        self.assertEqual(counts["manufacturing"], 1)
        self.assertEqual(counts["testing-inspection"], 1)

    def test_link_checker_falls_back_to_get_after_head_error(self) -> None:
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: object) -> None:
                return

            def do_HEAD(self) -> None:
                self.send_response(404)
                self.end_headers()

            def do_GET(self) -> None:
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            module = load_script("check_links")
            result = module.check(f"http://127.0.0.1:{server.server_port}/artifact", 2)
        finally:
            server.shutdown()
            thread.join()
            server.server_close()
        self.assertEqual(result["status"], "reachable")
        self.assertEqual(result["method"], "GET")

    def test_renderer_rejects_stale_topic_page(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            topics_dir = output / "topics"
            topics_dir.mkdir()
            (topics_dir / "obsolete.md").write_text("stale", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "render_catalog.py"),
                    "--catalog",
                    str(ROOT / "data" / "papers.json"),
                    "--analysis",
                    str(ROOT / "analysis" / "summary.json"),
                    "--readme",
                    str(output / "README.md"),
                    "--topics-dir",
                    str(topics_dir),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("stale generated topic pages", result.stderr)

    def test_renderer_rejects_stale_related_page_when_scope_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            topics_dir = output / "topics"
            topics_dir.mkdir()
            catalog = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
            catalog["papers"] = [paper for paper in catalog["papers"] if paper["scope"] == "pcb-core"]
            catalog_path = output / "catalog.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            (output / "related-eda.md").write_text("stale", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "render_catalog.py"),
                    "--catalog",
                    str(catalog_path),
                    "--analysis",
                    str(ROOT / "analysis" / "summary.json"),
                    "--readme",
                    str(output / "README.md"),
                    "--topics-dir",
                    str(topics_dir),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("stale generated related-EDA page", result.stderr)


if __name__ == "__main__":
    unittest.main()
