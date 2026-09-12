# Contributing

Thank you for improving the catalog.

The canonical source is `data/papers.json`; `README.md`, `docs/topics/*.md`,
`docs/related-eda.md`, and `docs/open-artifacts.md` are generated reader views.
You can read and compare paper records from the catalog and their primary URLs
without installing any linked implementation.

## Add or correct a paper

Before editing, search the existing DOI and normalized title so that a version
alias or duplicate is updated instead of added. Then edit `data/papers.json` and
keep every evidence-card block complete:

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

An entry remains useful as a paper or reference record when code or data is not
available: open its primary URL and keep the corresponding status explicit. Only
describe an implementation or dataset as open when its verified URL and status
are present; contributors do not need to install a linked project to add a
source-checked paper record.

## Run the checks

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_catalog.py data/papers.json --require-audit
python3 scripts/analyze_catalog.py
python3 scripts/render_catalog.py
git diff --check
```

The validation command checks the evidence-card and audit contracts. The analysis
and render commands refresh `analysis/`, `assets/`, `README.md`, and the topic
pages from `data/papers.json`; generated output must be included with the catalog
change.

## Pull request checklist

- [ ] The paper is in scope and not a duplicate/version alias.
- [ ] Venue/year come from an official or DOI-backed source.
- [ ] Code/data links resolve and release status is not inferred.
- [ ] Evaluation and baseline statements stay inside the cited evidence.
- [ ] A paper/reference entry can be read from its primary source even when no installable artifact is listed.
- [ ] Generated files are current and validation passes.
