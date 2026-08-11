# Methodology and evidence boundary

## Scope

The catalog has two deliberately separate layers:

1. `pcb-core`: the printed circuit board is the object being designed, placed, routed, modeled, manufactured, tested, or inspected.
2. `related-eda`: non-PCB automation whose method can transfer to PCB work. These records are representative references, not an exhaustive EDA survey.

The retrieval cutoff is **2026-08-11**. The catalog includes peer-reviewed papers and clearly labeled preprints. Patents, book chapters, corrections, data fragments, PCB recycling/pollutant work, and papers where a PCB is merely incidental hardware are excluded.

## Search and discovery

The discovery connectors use the query families defined in [`scripts/discover_openalex.py`](../scripts/discover_openalex.py); the Crossref connector reuses them. The queries combine PCB synonyms with:

- placement, legalization, and floorplanning;
- routing, escape routing, layer assignment, length matching, and pin assignment;
- ML, RL, GNN, LLM, and agentic design;
- schematic, netlist, component library, and design migration;
- signal integrity, power integrity, EMC/EMI, and crosstalk;
- thermal, vibration, warpage, fatigue, and reliability;
- DFM/DFA/DFT, fabrication, assembly, and process optimization;
- inspection, testing, datasets, benchmarks, and open tools.

Candidate retrieval is broader than admission by design. The repository does not commit raw API response caches or use their transient hit counts as coverage evidence. The review queue used Semantic Scholar's batch API for metadata and abstract corroboration; DOI, publisher, conference, or arXiv pages remain the primary record.

OpenAlex and DBLP connectors are optional discovery aids. A source may be unavailable or rate-limited on a given run. The catalog does not silently treat an unavailable connector as proof of completeness.

## De-duplication and version policy

1. Prefer DOI as the identity key.
2. Otherwise normalize the title to lowercase ASCII alphanumerics.
3. Merge arXiv and conference versions when the title/authors identify the same work; retain the peer-reviewed version as primary and preserve the arXiv URL.
4. Keep a later journal extension only when it is a materially different paper; do not collapse it into a short conference result.
5. Resolve conflicting years using the actual conference year or formal issue year, not the Crossref deposit year.

## Operational top-venue audit

The audit makes "all top-conference papers" falsifiable by using the closed set: **DAC, ICCAD, DATE, ASP-DAC, ISPD, ECTC, and EPEPS**. This is an operational coverage definition, not a universal ranking claim.

For each venue, the audit searches proceedings/metadata with `PCB`, `printed circuit board`, `printed wiring board`, `board-level`, `placement`, `routing`, `layout`, `signal integrity`, `power integrity`, `EMC`, `DFM`, and `testability`. The audit file records:

- search surfaces and cutoff;
- each PCB-specific admitted hit;
- excluded hits and reasons;
- the machine-readable exclusion log in `data/exclusions.json`, including low-evidence records and repeated detector variants without a distinct task, dataset, or evaluation contribution;
- duplicate/version normalization;
- known access or indexing gaps.

The admitted DOI inventory is the coverage target for PCB-specific results in this closed surface. The inventory is individually auditable, but unavailable or rate-limited proceedings surfaces prevent a mathematical completeness claim. Non-PCB EDA papers are representative references only.

## Evidence-card extraction

Every record must state:

- code release status and verified URL when available;
- dataset, benchmark, industrial/private/synthetic data, or explicit `not_reported`;
- application scenario;
- problem solved;
- final evaluation/test content and explicitly mentioned metrics;
- named baselines, an unnamed-comparison status, or explicit `not_reported`.

The evidence depth is one of `metadata-only`, `abstract`, `full-text`, or `project-page`. `not_found` never means proven nonexistent; `not_reported_in_accessible_source` never means the authors did not use it.

Full abstracts are not redistributed. The catalog stores original short summaries and source/locator metadata.

## Keyword analysis

[`scripts/analyze_catalog.py`](../scripts/analyze_catalog.py) applies a controlled vocabulary tracked in version control to every title. It also uses scenario and problem summaries for records supported by an abstract, full text, or project page. Metadata-only summaries are excluded because their repeated templates would distort the distribution. Counts are **document frequency**: a keyword contributes at most one count per paper. PCB-core and related-EDA records are computed separately so reference papers cannot distort PCB trends.

## Limitations

- Some proceedings and full texts are paywalled.
- Publisher deposits can carry a deposit year rather than the publication year.
- Papers can avoid PCB/PWB terms in their titles and abstracts.
- Code can be released after the catalog's verification date.
- "Latest" is a moving boundary. The cutoff makes the time boundary explicit, but it does not make the catalog permanently current.
- The URL-check snapshot treats publisher `401/403` responses as access-controlled rather than dead links. On 2026-08-11, 348 of 351 unique paper/code/data URLs were reachable or access-controlled. Two dataset hosts returned network errors, and one author-reported Kaggle URL returned HTTP 404. The catalog retains these links as provenance and marks the Kaggle dataset `reported_link_unreachable` rather than open.

Corrections with a primary source are welcome.
