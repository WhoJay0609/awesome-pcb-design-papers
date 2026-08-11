# GLM and DeepSeek consultation notes

The catalog schema and coverage protocol were finalized after consultations on 2026-08-11. These notes record design recommendations, not evidence for any paper-level claim.

## Shared recommendations adopted

- Use a closed operational top-venue set and publish an admitted/excluded audit matrix rather than make the untestable global claim that the catalog covers all top venues.
- Retrieve broadly from Crossref, OpenAlex, DBLP, publisher proceedings, arXiv/OpenReview, Semantic Scholar, and project repositories; de-duplicate by DOI and normalized title.
- Separate PCB-core work from transferable non-PCB EDA references in both the catalog and trend analysis.
- Attach field-level evidence to code status, data source, scenario, problem, evaluation, and baselines.
- Preserve explicit missing states such as `not_found` and `not_reported_in_accessible_source`; do not infer absent experimental details.
- Compute keyword counts as document frequency from a version-controlled vocabulary and keep PCB/related-EDA scopes separate.

## Resulting repository decisions

- Operational top-venue set: DAC, ICCAD, DATE, ASP-DAC, ISPD, ECTC, and EPEPS.
- Machine-readable authority: `data/papers.json`; all Markdown paper cards are generated from it.
- Reproducible trend analysis: `scripts/analyze_catalog.py` and `analysis/summary.json`.
- Evidence policy and access limitations: `docs/methodology.md`.
