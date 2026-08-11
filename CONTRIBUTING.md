# Contributing

Thank you for improving the catalog.

## Add or correct a paper

Please edit `data/papers.json` and keep every evidence-card block complete:

- DOI, publisher, conference, or arXiv primary link;
- publication year and venue;
- `pcb-core` or `related-eda` scope;
- primary and secondary topics;
- code status and a resolving URL when marked open;
- dataset/data-source status;
- application scenario and problem;
- evaluation/tests/metrics;
- named baselines or an explicit missing-evidence status;
- evidence depth, source, locator, and check date.

Do not infer absent facts. Use `not_reported_in_accessible_source` or `not_found` with the documented semantics.

## Run the checks

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_catalog.py data/papers.json --require-audit
python3 scripts/analyze_catalog.py
python3 scripts/render_catalog.py
git diff --check
```

Generated analysis and topic pages must be committed with the catalog change.

## Pull request checklist

- [ ] The paper is in scope and not a duplicate/version alias.
- [ ] Venue/year come from an official or DOI-backed source.
- [ ] Code/data links resolve and release status is not inferred.
- [ ] Evaluation and baseline statements stay inside the cited evidence.
- [ ] Generated files are current and validation passes.
