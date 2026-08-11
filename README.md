# Awesome PCB Design Papers

> A source-checked, evidence-card catalog for PCB design automation and transferable EDA research.

**Cutoff date:** 2026-08-11 · **PCB core:** 305 papers · **Related EDA:** 16 papers · **Topics:** 8

The repository follows the familiar Awesome-list layout. Each paper also has fields for code status, datasets or data sources, application scenario, problem addressed, final evaluation, baselines, and the evidence boundary.

## Scope

- **PCB core:** PCB, PWB, or PCBA is the object of design, placement, routing, SI/PI/EMC, reliability, DFX, or testing.
- **Related EDA references:** Transferable methods for chips, packages, chiplets, and LLM or agentic EDA are counted separately and are not presented as PCB papers.
- **Excluded:** Application papers that use a PCB only as an experimental carrier, electronic-waste or pollution studies, patents, book chapters, errata, and repeated model variants without an independent task or data contribution.

## Browse by topic

| Topic | Papers |
|---|---:|
| [Placement and legalization](docs/topics/placement.md) | 35 |
| [Routing and constraint handling](docs/topics/routing.md) | 92 |
| [Schematic and design-chain automation](docs/topics/schematic-design.md) | 14 |
| [SI, PI, and EMC](docs/topics/si-pi-emc.md) | 70 |
| [Thermal and reliability co-design](docs/topics/thermal-reliability.md) | 26 |
| [DFM and assembly optimization](docs/topics/dfm-manufacturing.md) | 14 |
| [Testing and inspection](docs/topics/testing-inspection.md) | 18 |
| [Benchmarks, datasets, and tools](docs/topics/benchmarks-tools.md) | 36 |
| [Related EDA references](docs/related-eda.md) | 16 |

## Latest PCB-core papers (2024-2026)

- **2026** · [PCB-Migrator: Automated PCB PnR Migration](https://doi.org/10.23919/date69613.2026.11539307): Design, Automation and Test in Europe · **DATE**
- **2026** · [Smart-PCLib: A LLM-based Multi-Agent Framework for Automated PCB Component Library Generation](https://doi.org/10.23919/date69613.2026.11539310): Design, Automation and Test in Europe · **DATE**
- **2026** · [DRLPlace: A Deep Reinforcement Learning-based Irregular and High-Density Printed Circuit Board Placement Method](https://doi.org/10.1109/asp-dac66049.2026.11420655): 2026 31st Asia and South Pacific Design Automation Conference (ASP-DAC) · **ASP-DAC**
- **2026** · [Introduction to High-Speed LVDS Twisted Pair Transmission Across PCB and Chiplet RDL Interfaces](https://doi.org/10.1109/ectc51846.2026.00359): 2026 IEEE 76th Electronic Components and Technology Conference (ECTC) · **ECTC**
- **2026** · [Warpage Prediction of PCB in Multi-Laminating Processes Considering Cure Shrinkage and Anisotropic Visco-Elastic Properties of Prepreg Core](https://doi.org/10.1109/ectc51846.2026.00258): 2026 IEEE 76th Electronic Components and Technology Conference (ECTC) · **ECTC**
- **2026** · [A Graph-based Benchmark Dataset for Printed Circuit Netlist Partitioning](https://doi.org/10.1038/s41597-026-06818-y): Scientific Data 13
- **2026** · [PCB-Bench: Benchmarking LLMs for Printed Circuit Board Placement and Routing](https://openreview.net/forum?id=Q5QLu7XTWx): ICLR 2026
- **2026** · [Automation of PCB Autorouting via World-Model Reinforcement Learning and FreeRouting Integration](https://doi.org/10.1016/j.eswa.2026.131424): Expert Systems with Applications
- **2026** · [OmniLayout: A Schematic-Coupled Multimodal Benchmark for Constraint-Aware Geometric Reasoning in PCB Layout](https://arxiv.org/abs/2607.03261): arXiv
- **2026** · [Complete Flow for PCB Design Consideration and Power/Signal Integrity Analysis Based on Broadband Model of Parasitic Elements](https://doi.org/10.1002/cta.70260): International Journal of Circuit Theory and Applications 54(2)
- **2026** · [Thermal Analysis of Component Placement in High-Power Electronics and LED Boards](https://doi.org/10.1016/j.pedc.2026.100148): Power Electronic Devices and Components
- **2026** · [A Lightweight Model for PCB Surface Defect Detection](https://doi.org/10.3390/electronics15163500): Electronics
- **2026** · [A multi-cognitive PCB defect detection model integrating Mamba](https://doi.org/10.1038/s41598-026-49734-2): Scientific Reports
- **2026** · [A-star Algorithm-Based Automated Routing for Multilayer PCB](https://doi.org/10.1109/apec51134.2026.11516836): Applied Power Electronics Conference
- **2026** · [AI-Driven PCB Assembly Defect Detection Using Hybrid Deep Learning Architectures](https://doi.org/10.5220/0013856700004052): International Conference on Agents and Artificial Intelligence
- **2026** · [Intelligent Disassembly System for PCB Components Integrating Multimodal Large Language Model and Multi-Agent Framework](https://doi.org/10.3390/pr14020227): Processes

## Operational top-venue coverage

In this repository, complete top-venue coverage means a closed, auditable set: **DAC, ICCAD, DATE, ASP-DAC, ISPD, ECTC, EPEPS**. This is an operational definition, not a judgment about conference rankings. Each of the 192 admitted DOIs is bound to a catalog row. The inventory aims to account for every matching paper in that set, but inaccessible or rate-limited proceedings prevent a mathematical completeness claim. Related EDA is included only as a representative reference set.

| Venue | Included PCB papers |
|---|---:|
| DAC | 63 |
| ICCAD | 7 |
| DATE | 7 |
| ASP-DAC | 11 |
| ISPD | 5 |
| ECTC | 46 |
| EPEPS | 53 |

## Keyword and trend analysis

Keyword counts use a controlled regular-expression vocabulary over every title. Scenario and problem summaries are included only for records supported by an abstract, full text, or project page. **Document frequency** counts a keyword at most once per paper. PCB core and Related EDA are analyzed separately.

![PCB keyword distribution](assets/pcb_core_keyword_distribution.svg)

![PCB publication trend](assets/pcb_core_year_trend.svg)

![PCB topic distribution](assets/pcb_core_topic_distribution.svg)

Top controlled keywords: `routing` (66), `placement` (36), `optimization` (35), `testing-inspection` (32), `manufacturing` (26), `reliability` (25), `thermal` (20), `co-design` (18), `signal-integrity` (18), `benchmark-dataset` (12), `emc-emi` (10), `llm-agent` (9).

Reproduce with:

```bash
python3 scripts/validate_catalog.py data/papers.json --require-audit
python3 scripts/analyze_catalog.py
python3 scripts/render_catalog.py
```

## Evidence and status semantics

- `open` means a code/data URL resolved during verification; `announced_or_mentioned_unverified` is not counted as released.
- `not_found` means no repository was found in the inspected paper/project sources; it does **not** prove that code does not exist.
- `not_reported_in_accessible_source` means the accessible metadata/abstract/full text did not state the field.
- `reported_link_unreachable` means the paper names an artifact URL, but the cutoff-date link check could not retrieve it.
- `metadata-only`, `abstract`, `full-text`, and `project-page` expose how deep the extraction went.

See [methodology](docs/methodology.md), [GLM/DeepSeek consultation notes](docs/consultation-notes.md), [top-venue audit](data/top_venue_audit.json), [machine-readable catalog](data/papers.json), [trend outputs](analysis/summary.json), and the [URL-check snapshot](analysis/link_check.json).

## Coverage boundary

This is a structured, cutoff-dated catalog: it is not a claim of absolute global exhaustiveness. Publisher indexing delays, title changes, inaccessible proceedings, and papers that never use board-specific terms can still create gaps. Please open an issue or PR with a primary source and the required evidence fields.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New records must include a DOI/publisher/arXiv link and explicit status for code, data, scenario, problem, evaluation, and baselines.
