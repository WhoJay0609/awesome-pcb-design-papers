# Awesome PCB Design Papers

> A source-checked, evidence-card catalog for PCB design automation and transferable EDA research.

**检索截止：2026-08-11** · **PCB core：305 篇** · **Related EDA：16 篇** · **主题：8 个**

本仓库模仿 Awesome 列表的可浏览性，但不只保存链接：每篇论文都明确记录代码状态、数据集/数据来源、应用场景、解决的问题、最终测试和 baselines，并给出证据边界。

## Scope

- **PCB core**：PCB/PWB/PCBA 是论文的设计、布局、布线、SI/PI/EMC、可靠性、DFX 或测试对象。
- **Related EDA References**：芯片、封装、Chiplet、LLM/agentic EDA 等可迁移方法；单独统计，不冒充 PCB 论文。
- **排除**：PCB 仅作为实验载板的应用论文、电子垃圾/污染物研究、专利、书籍章节、勘误，以及缺乏独立任务/数据贡献的重复模型变体。

## Browse by topic

| Topic | Papers | Description |
|---|---:|---|
| [元件布局与合法化](docs/topics/placement.md) | 35 | Placement and legalization |
| [自动布线与约束满足](docs/topics/routing.md) | 92 | Routing and constraint handling |
| [原理图、网表与设计链自动化](docs/topics/schematic-design.md) | 14 | Schematic and design-chain automation |
| [信号/电源完整性与电磁兼容](docs/topics/si-pi-emc.md) | 70 | SI, PI, and EMC |
| [热、机械与可靠性协同设计](docs/topics/thermal-reliability.md) | 26 | Thermal and reliability co-design |
| [可制造性与装配优化](docs/topics/dfm-manufacturing.md) | 14 | DFM and assembly optimization |
| [测试、检测与质量反馈](docs/topics/testing-inspection.md) | 18 | Testing and inspection |
| [基准、数据集与开放工具](docs/topics/benchmarks-tools.md) | 36 | Benchmarks, datasets, and tools |
| [相关 EDA 自动化参考](docs/related-eda.md) | 16 | Transferable non-PCB methods |

## Latest PCB-core papers (2024–2026)

- **2026** · [PCB-Migrator: Automated PCB PnR Migration](https://doi.org/10.23919/date69613.2026.11539307) — Design, Automation and Test in Europe · **DATE**
- **2026** · [Smart-PCLib: A LLM-based Multi-Agent Framework for Automated PCB Component Library Generation](https://doi.org/10.23919/date69613.2026.11539310) — Design, Automation and Test in Europe · **DATE**
- **2026** · [DRLPlace: A Deep Reinforcement Learning-based Irregular and High-Density Printed Circuit Board Placement Method](https://doi.org/10.1109/asp-dac66049.2026.11420655) — 2026 31st Asia and South Pacific Design Automation Conference (ASP-DAC) · **ASP-DAC**
- **2026** · [Introduction to High-Speed LVDS Twisted Pair Transmission Across PCB and Chiplet RDL Interfaces](https://doi.org/10.1109/ectc51846.2026.00359) — 2026 IEEE 76th Electronic Components and Technology Conference (ECTC) · **ECTC**
- **2026** · [Warpage Prediction of PCB in Multi-Laminating Processes Considering Cure Shrinkage and Anisotropic Visco-Elastic Properties of Prepreg Core](https://doi.org/10.1109/ectc51846.2026.00258) — 2026 IEEE 76th Electronic Components and Technology Conference (ECTC) · **ECTC**
- **2026** · [A Graph-based Benchmark Dataset for Printed Circuit Netlist Partitioning](https://doi.org/10.1038/s41597-026-06818-y) — Scientific Data 13
- **2026** · [PCB-Bench: Benchmarking LLMs for Printed Circuit Board Placement and Routing](https://openreview.net/forum?id=Q5QLu7XTWx) — ICLR 2026
- **2026** · [Automation of PCB Autorouting via World-Model Reinforcement Learning and FreeRouting Integration](https://doi.org/10.1016/j.eswa.2026.131424) — Expert Systems with Applications
- **2026** · [OmniLayout: A Schematic-Coupled Multimodal Benchmark for Constraint-Aware Geometric Reasoning in PCB Layout](https://arxiv.org/abs/2607.03261) — arXiv
- **2026** · [Complete Flow for PCB Design Consideration and Power/Signal Integrity Analysis Based on Broadband Model of Parasitic Elements](https://doi.org/10.1002/cta.70260) — International Journal of Circuit Theory and Applications 54(2)
- **2026** · [Thermal Analysis of Component Placement in High-Power Electronics and LED Boards](https://doi.org/10.1016/j.pedc.2026.100148) — Power Electronic Devices and Components
- **2026** · [A Lightweight Model for PCB Surface Defect Detection](https://doi.org/10.3390/electronics15163500) — Electronics
- **2026** · [A multi-cognitive PCB defect detection model integrating Mamba](https://doi.org/10.1038/s41598-026-49734-2) — Scientific Reports
- **2026** · [A-star Algorithm-Based Automated Routing for Multilayer PCB](https://doi.org/10.1109/apec51134.2026.11516836) — Applied Power Electronics Conference
- **2026** · [AI-Driven PCB Assembly Defect Detection Using Hybrid Deep Learning Architectures](https://doi.org/10.5220/0013856700004052) — International Conference on Agents and Artificial Intelligence
- **2026** · [Intelligent Disassembly System for PCB Components Integrating Multimodal Large Language Model and Multi-Agent Framework](https://doi.org/10.3390/pr14020227) — Processes

## Operational top-venue coverage

“顶会全部覆盖”采用封闭、可审计的操作性集合：**DAC, ICCAD, DATE, ASP-DAC, ISPD, ECTC, EPEPS**。它不是对任何排名体系的价值判断。192 条 admitted DOI 逐行绑定目录；这是以穷尽为目标的封闭清单，但受不可访问/限流 proceedings 影响，不作数学完备性承诺。Related EDA 只做代表性参考。

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

关键词采用受控正则词表，对每篇题名与本仓库原创摘要做 **document frequency**：一个关键词在同一论文中最多计一次。PCB core 与 Related EDA 分开统计。

![PCB keyword distribution](assets/pcb_core_keyword_distribution.svg)

![PCB publication trend](assets/pcb_core_year_trend.svg)

![PCB topic distribution](assets/pcb_core_topic_distribution.svg)

Top controlled keywords: `routing` (65), `optimization` (35), `placement` (34), `testing-inspection` (30), `reliability` (25), `manufacturing` (24), `thermal` (21), `co-design` (21), `signal-integrity` (18), `emc-emi` (16), `benchmark-dataset` (12), `llm-agent` (9).

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

This is a structured, cutoff-dated catalog—not a claim of absolute global exhaustiveness. Publisher indexing delays, title changes, inaccessible proceedings, and papers that never use board-specific terms can still create gaps. Please open an issue or PR with a primary source and the required evidence fields.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New records must include a DOI/publisher/arXiv link and explicit status for code, data, scenario, problem, evaluation, and baselines.
