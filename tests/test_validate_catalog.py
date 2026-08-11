#!/usr/bin/env python3
"""Regression tests for acceptance-critical catalog and audit invariants."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_catalog.py"


class CatalogValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
        cls.audit = json.loads((ROOT / "data" / "top_venue_audit.json").read_text(encoding="utf-8"))

    def validate(self, catalog: dict, audit: dict) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            catalog_path = directory_path / "papers.json"
            audit_path = directory_path / "audit.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            audit_path.write_text(json.dumps(audit), encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    str(catalog_path),
                    "--audit",
                    str(audit_path),
                    "--require-audit",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

    def test_current_catalog_passes(self) -> None:
        result = self.validate(self.catalog, self.audit)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_schema_version_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        del catalog["schema_version"]
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema_version must be 2.0.0", result.stdout)

    def test_old_schema_version_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["schema_version"] = "1.0.0"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema_version must be 2.0.0", result.stdout)

    def test_missing_schema_required_fields_fail(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        del catalog["topics"][0]["name"]
        del catalog["papers"][0]["top_venue"]
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("topic 0 name must be a non-empty string", result.stdout)
        self.assertIn("missing required fields top_venue", result.stdout)

    def test_missing_nested_evidence_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        del catalog["papers"][0]["code"]["evidence"]["source_url"]
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("code evidence source must be HTTPS", result.stdout)

    def test_invalid_authors_fail(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["papers"][0]["authors"] = [""]
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("authors must be a non-empty string list", result.stdout)

    def test_invalid_evidence_level_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["papers"][0]["evidence_level"] = "unknown"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid evidence_level", result.stdout)

    def test_primary_topic_must_be_listed_in_topics(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        paper = catalog["papers"][0]
        paper["topics"] = [topic for topic in paper["topics"] if topic != paper["primary_topic"]]
        if not paper["topics"]:
            paper["topics"] = [next(topic["id"] for topic in catalog["topics"] if topic["id"] != paper["primary_topic"])]
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("primary_topic must be included in topics", result.stdout)

    def test_invalid_verification_structure_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["papers"][0]["verification"]["sources"] = []
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("verification.sources must be a non-empty string list", result.stdout)

    def test_invalid_date_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["papers"][0]["code"]["checked_on"] = "2026-99-99"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("code.checked_on must be a YYYY-MM-DD date", result.stdout)

    def test_non_string_nested_list_item_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["papers"][0]["dataset"]["names"] = [123]
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dataset.names must be a string list", result.stdout)

    def test_non_object_evidence_fails_without_crashing(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["papers"][0]["code"]["evidence"] = "not-an-object"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("code evidence must be an object", result.stdout)

    def test_non_string_status_and_summary_fail(self) -> None:
        for field, value, expected in (
            ("status", [1], "code status must be a non-empty string"),
            ("summary", 123, "code summary must be a non-empty string"),
        ):
            with self.subTest(field=field):
                catalog = copy.deepcopy(self.catalog)
                catalog["papers"][0]["code"][field] = value
                result = self.validate(catalog, self.audit)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)

    def test_non_string_locator_and_sources_fail_without_crashing(self) -> None:
        mutations = [
            lambda catalog: catalog["papers"][0]["application_scenario"]["evidence"].__setitem__("locator", ["title"]),
            lambda catalog: catalog["papers"][0]["verification"].__setitem__("sources", 123),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                catalog = copy.deepcopy(self.catalog)
                mutate(catalog)
                result = self.validate(catalog, self.audit)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_malformed_supported_values_fail_without_traceback(self) -> None:
        mutations = [
            lambda catalog: catalog["topics"].__setitem__(0, []),
            lambda catalog: catalog["papers"][0].__setitem__("year", "2026"),
            lambda catalog: catalog["papers"][0]["code"].__setitem__("url", []),
            lambda catalog: catalog["papers"][0]["code"].__setitem__("status", []),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                catalog = copy.deepcopy(self.catalog)
                mutate(catalog)
                result = self.validate(catalog, self.audit)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_nonexistent_audit_catalog_id_fails(self) -> None:
        audit = copy.deepcopy(self.audit)
        audit["admitted"][0]["catalog_id"] = "doi:10.invalid/not-in-catalog"
        result = self.validate(self.catalog, audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("catalog_id not found", result.stdout)

    def test_wrong_audit_year_fails(self) -> None:
        audit = copy.deepcopy(self.audit)
        audit["admitted"][0]["year"] += 1
        result = self.validate(self.catalog, audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("year mismatch", result.stdout)

    def test_fictitious_audit_doi_fails(self) -> None:
        audit = copy.deepcopy(self.audit)
        audit["admitted"][0]["doi"] = "10.9999/fictitious-doi"
        audit["admitted"][0]["verification_sources"] = ["https://doi.org/10.9999/fictitious-doi"]
        result = self.validate(self.catalog, audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DOI is not bound", result.stdout)

    def test_duplicate_venue_search_fails(self) -> None:
        audit = copy.deepcopy(self.audit)
        audit["venue_searches"].append(copy.deepcopy(audit["venue_searches"][0]))
        result = self.validate(self.catalog, audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly one venue_searches row per venue", result.stdout)

    def test_open_dataset_without_url_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        paper = next(paper for paper in catalog["papers"] if paper["dataset"]["status"] == "open")
        paper["urls"]["data"] = ""
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("open dataset status requires a verified data URL", result.stdout)

    def test_open_dataset_url_must_be_in_acceptable_snapshot(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        paper = next(paper for paper in catalog["papers"] if paper["dataset"]["status"] == "open")
        paper["urls"]["data"] = "https://example.invalid/not-a-real-dataset"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("link report: URL set does not match catalog", result.stdout)

    def test_metadata_only_reported_claim_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        paper = next(paper for paper in catalog["papers"] if paper["evidence_level"] == "metadata-only")
        paper["application_scenario"]["status"] = "reported"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata-only application_scenario has an unsupported status", result.stdout)

    def test_title_and_abstract_status_requires_abstract_evidence(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        paper = next(paper for paper in catalog["papers"] if paper["evidence_level"] == "metadata-only")
        paper["application_scenario"]["status"] = "classified_from_title_and_abstract"
        paper["application_scenario"]["evidence"]["locator"] = "title"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("title-and-abstract classification requires abstract evidence", result.stdout)

    def test_metadata_only_locator_cannot_claim_abstract(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        paper = next(paper for paper in catalog["papers"] if paper["evidence_level"] == "metadata-only")
        paper["code"]["evidence"]["locator"] = "abstract and metadata"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata-only code locator cannot claim abstract evidence", result.stdout)

    def test_abstract_level_locator_cannot_claim_full_text(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        paper = next(paper for paper in catalog["papers"] if paper["evidence_level"] == "abstract")
        paper["code"]["evidence"]["locator"] = "abstract or full text"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("abstract-level code locator cannot claim full-text evidence", result.stdout)

    def test_html_entity_in_title_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["papers"][0]["title"] = "A &amp; B"
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("title contains an HTML entity", result.stdout)

    def test_non_english_catalog_prose_fails(self) -> None:
        for prose in (
            "\u672a\u62a5\u544a\u3002",
            "\u03a4\u03b1 \u03b4\u03b5\u03b4\u03bf\u03bc\u03ad\u03bd\u03b1 \u03b4\u03b5\u03bd \u03b1\u03bd\u03b1\u03c6\u03ad\u03c1\u03bf\u03bd\u03c4\u03b1\u03b9.",
            "\u30c7\u30fc\u30bf\u306f\u672a\u5831\u544a\u3067\u3059\u3002",
            "\ub370\uc774\ud130\uac00 \ubcf4\uace0\ub418\uc9c0 \uc54a\uc558\uc2b5\ub2c8\ub2e4.",
            "\u1100",
            "\uff76",
            "\ufa11",
            "\u0414",
            "\U00017000",
            "\U00018d00",
            "\U00030000",
            "\U00031350",
        ):
            with self.subTest(prose=prose):
                catalog = copy.deepcopy(self.catalog)
                catalog["papers"][0]["code"]["summary"] = prose
                result = self.validate(catalog, self.audit)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("code summary must be English", result.stdout)

    def test_humanizer_punctuation_fails(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["papers"][0]["evaluation"]["summary"] = "Measured on two boards \u2014 both passed."
        result = self.validate(catalog, self.audit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evaluation summary contains disallowed punctuation", result.stdout)


if __name__ == "__main__":
    unittest.main()
