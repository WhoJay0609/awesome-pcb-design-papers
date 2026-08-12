# Schematic and design-chain automation

[Back to README](../../README.md) · [Catalog table](#catalog) · [Paper cards](#paper-cards)

14 papers are assigned to this primary topic; 20 PCB-core papers carry it as a primary or additional tag. Detailed fields come from `data/papers.json`; `not_reported` means that the accessible evidence does not state the field. Not reported does not mean absent.

## Catalog

| Year | Paper | Venue | Code | Evidence |
|---:|---|---|---|---|
| 2026 | [OmniSch: A Multimodal PCB Schematic Benchmark For Structured Diagram Visual Reasoning](#omnisch-a-multimodal-pcb-schematic-benchmark-for-structured-diagram-visual-reasoning) | arXiv | not found | project-page |
| 2026 | [PCB-Migrator: Automated PCB PnR Migration](#pcb-migrator-automated-pcb-pnr-migration) | Design, Automation and Test in Europe · **DATE** | not found | abstract |
| 2026 | [PCB-QA: A Task-Specific Question Answering Framework for Text-Centric Chip Datasheet Queries in PCB Design](#pcb-qa-a-task-specific-question-answering-framework-for-text-centric-chip-datasheet-queries-in-pcb-design) | ACM Transactions on Design Automation of Electronic Systems | not found | abstract |
| 2026 | [pcbGPT: Automatic PCB Schematic Synthesis from Natural Language Requirements](#pcbgpt-automatic-pcb-schematic-synthesis-from-natural-language-requirements) | arXiv | not found | full-text |
| 2026 | [PCBSchemaGen: Reward-Guided LLM Code Synthesis for Printed Circuit Boards (PCB) Schematic Design with Structured Verification](#pcbschemagen-reward-guided-llm-code-synthesis-for-printed-circuit-boards-pcb-schematic-design-with-structured-verification) | arXiv | open | project-page |
| 2026 | [SchGen: PCB Schematic Generation with Semantic-Grounded Code Representations](#schgen-pcb-schematic-generation-with-semantic-grounded-code-representations) | arXiv | open | project-page |
| 2026 | [Smart-PCLib: A LLM-based Multi-Agent Framework for Automated PCB Component Library Generation](#smart-pclib-a-llm-based-multi-agent-framework-for-automated-pcb-component-library-generation) | Design, Automation and Test in Europe · **DATE** | not found | abstract |
| 2025 | [PCBSmith: An Effective Schematic Generator for Testing PCB Design Tool Chain](#pcbsmith-an-effective-schematic-generator-for-testing-pcb-design-tool-chain) | IEEE Transactions on Reliability | not found | abstract |
| 2024 | [AEM-PCB Reverser: Circuit Schematic Generation in PCB Reverse Engineering Using Reinforcement Learning Based on Aesthetic Evaluation Metric](#aem-pcb-reverser-circuit-schematic-generation-in-pcb-reverse-engineering-using-reinforcement-learning-based-on-aesthetic-evaluation-metric) | IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems | not found | abstract |
| 2024 | [Impact of Line Length and Component Selection on RF Performance for a PCB-based Ferromagnetic Nonlinear Transmission Line](#impact-of-line-length-and-component-selection-on-rf-performance-for-a-pcb-based-ferromagnetic-nonlinear-transmission-line) | IEEE International Power Modulator and High Voltage Conference | not found | metadata-only |
| 2024 | [Multi-modal printed circuit board netlist extraction with x-ray and optical imaging](#multi-modal-printed-circuit-board-netlist-extraction-with-x-ray-and-optical-imaging) | Optical Engineering + Applications | not found | abstract |
| 2016 | [A Novel Modular Design and Modeling Methodology for High Speed High Density Die Package PCB Co-Simulation and Model Library Creation](#a-novel-modular-design-and-modeling-methodology-for-high-speed-high-density-die-package-pcb-co-simulation-and-model-library-creation) | 2016 IEEE 66th Electronic Components and Technology Conference (ECTC) · **ECTC** | not reported | metadata-only |
| 2013 | [Modeling methodologies for multi level PCB-package co-simulation & co-design](#modeling-methodologies-for-multi-level-pcb-package-co-simulation--co-design) | 2013 IEEE 22nd Conference on Electrical Performance of Electronic Packaging and Systems · **EPEPS** | not reported | metadata-only |
| 1978 | [An Integrated System for Interactive Editing of Schematics, Logic Simulation and PCB Layout Design](#an-integrated-system-for-interactive-editing-of-schematics-logic-simulation-and-pcb-layout-design) | Design Automation Conference · **DAC** | not found | metadata-only |

## Paper cards

### OmniSch: A Multimodal PCB Schematic Benchmark For Structured Diagram Visual Reasoning

- **Metadata:** 2026 · arXiv · Taiting Lu, Kaiyuan Lin, Yuxin Tian, Yubo Wang, Muchuan Wang, Mahanth Gowda · [paper](https://arxiv.org/abs/2604.00270)
- **Scope and topics:** `pcb-core` · `schematic-design`, `benchmarks-tools`, `ai-eda`
- **Code:** not_found: The project page publishes a data download, but no complete code repository was verified.
- **Dataset or data source:** [open](https://omnisch.com/): [OmniSch](https://omnisch.com/)
- **Application scenario:** Multimodal PCB schematic understanding, visual localization, schematic-to-netlist graph construction, and tool use.
- **Problem addressed:** `reported`: Establishes unified tasks and an annotated benchmark for structured visual reasoning over real PCB schematics.
- **Final evaluation:** `reported`: Tests symbol, pin, and text recognition, net graphs, and agent tasks separately, using an 80/10/10 split to evaluate classical pipelines. Metrics: F1, IoU, graph edit distance, Kendall tau, pass rate.
- **Baselines:** `named`: YOLO11, PaddleOCR, GPT-5.2, GPT-5-mini, Claude Sonnet 4.6, Gemini, Qwen, human engineers
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### PCB-Migrator: Automated PCB PnR Migration

- **Metadata:** 2026 · Design, Automation and Test in Europe · Yaohui Han, Beichen Li, Rongliang Fu, Qunsong Ye, Zhiyuan Lu, Junchen Liu, Bei Yu, Tsung-Yi Ho, et al. · [paper](https://doi.org/10.23919/date69613.2026.11539307)
- **Scope and topics:** `pcb-core` · `placement`, `routing`, `schematic-design`, `thermal-reliability`, `benchmarks-tools`
- **Code:** not_found: No verified public code repository was found.
- **Dataset or data source:** `not_reported_in_accessible_source`: The accessible metadata or abstract does not report this field.
- **Application scenario:** Schematic and design-chain automation.
- **Problem addressed:** `reported_in_abstract`: The abstract describes the PCB design problem.
- **Final evaluation:** `reported_in_abstract`: The abstract reports an experiment or evaluation; the metric field lists only items explicitly mentioned in the abstract. Metrics: not explicitly listed in the accessible sources.
- **Baselines:** `reported_but_unnamed_in_abstract`: The abstract mentions a comparison but does not name the baseline.
- **Evidence boundary:** `abstract`; checked on 2026-08-11.

### PCB-QA: A Task-Specific Question Answering Framework for Text-Centric Chip Datasheet Queries in PCB Design

- **Metadata:** 2026 · ACM Transactions on Design Automation of Electronic Systems · Binwu Zhu, Bei Yu · [paper](https://doi.org/10.1145/3811922)
- **Scope and topics:** `pcb-core` · `placement`, `schematic-design`, `testing-inspection`, `benchmarks-tools`
- **Code:** not_found: No verified public code repository was found.
- **Dataset or data source:** `reported_in_abstract`: The abstract mentions a dataset, benchmark, or real, industrial, or simulated data; only names that can be identified are retained.
- **Application scenario:** Schematic and design-chain automation.
- **Problem addressed:** `reported_in_abstract`: The abstract describes the PCB design problem.
- **Final evaluation:** `reported_in_abstract`: The abstract reports an experiment or evaluation; the metric field lists only items explicitly mentioned in the abstract. Metrics: accuracy.
- **Baselines:** `reported_but_unnamed_in_abstract`: The abstract mentions a comparison but does not name the baseline.
- **Evidence boundary:** `abstract`; checked on 2026-08-11.

### pcbGPT: Automatic PCB Schematic Synthesis from Natural Language Requirements

- **Metadata:** 2026 · arXiv · Tobias King, Steven Kehrberg, Michael Beigl, Tobias Röddiger · [paper](https://arxiv.org/abs/2606.01188)
- **Scope and topics:** `pcb-core` · `schematic-design`, `ai-eda`
- **Code:** not_found: No public code or data repository was verified.
- **Dataset or data source:** `reported`: pcbGPT-20 tasks
- **Application scenario:** Converts natural-language requirements for embedded, IoT, and wearable systems into editable KiCad projects.
- **Problem addressed:** `reported`: Combines a DSL, component-library retrieval, datasheet grounding, and execution checks to generate usable schematics.
- **Final evaluation:** `reported`: The best model reports pass@1 = 0.90 and pass@5 = 1.00; pass@1 is 0.72 on hard tasks. Metrics: pass@1, pass@5.
- **Baselines:** `reported_but_unnamed`: Compares model variants and task-difficulty strata; no external baseline is reported.
- **Evidence boundary:** `full-text`; checked on 2026-08-11.

### PCBSchemaGen: Reward-Guided LLM Code Synthesis for Printed Circuit Boards (PCB) Schematic Design with Structured Verification

- **Metadata:** 2026 · arXiv · Huanghaohe Zou, Peng Han, Emad Nazerian, Mafu Zhang, Zhicheng Guo, Alex Q. Huang · [paper](https://arxiv.org/abs/2602.00510)
- **Scope and topics:** `pcb-core` · `schematic-design`, `benchmarks-tools`, `ai-eda`
- **Code:** [open](https://github.com/HZou9/PCBSchemaGen_v2): The MIT repository contains benchmarks, a knowledge graph, validators, and configuration.
- **Dataset or data source:** [open](https://github.com/HZou9/PCBSchemaGen_v2): [PCBBench](https://github.com/HZou9/PCBSchemaGen_v2), [Open-Schematics-Eval](https://github.com/HZou9/PCBSchemaGen_v2)
- **Application scenario:** Generates PCB schematics from natural-language requirements and repairs them with a datasheet knowledge graph and deterministic validators.
- **Problem addressed:** `reported`: Generates verifiable, editable PCB schematics without training a dedicated large model.
- **Final evaluation:** `reported`: Five-layer structural validation; Gemma-4-31B passes 81.3% on average and is tested on held-out public schematics. Metrics: pass rate.
- **Baselines:** `named`: Circuitron-style prompting
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### SchGen: PCB Schematic Generation with Semantic-Grounded Code Representations

- **Metadata:** 2026 · arXiv · Qinpei Luo, Ruichun Ma, Xinyu Zhang, Lili Qiu · [paper](https://arxiv.org/abs/2605.30345)
- **Scope and topics:** `pcb-core` · `schematic-design`, `benchmarks-tools`, `ai-eda`
- **Code:** [open](https://github.com/microsoft/SchGen): The Microsoft repository publishes model and dataset links and a KiCad generation workflow.
- **Dataset or data source:** [open](https://github.com/microsoft/SchGen): [SchGen_dataset](https://github.com/microsoft/SchGen)
- **Application scenario:** Semantic code generation from natural language to editable KiCad schematics.
- **Problem addressed:** `reported`: Uses a semantically grounded representation to improve the executability of wiring and functional structure.
- **Final evaluation:** `reported`: Compares wiring correctness and functional correctness; the public abstract does not give complete numerical results. Metrics: wire-connectivity accuracy, functional correctness.
- **Baselines:** `reported_but_unnamed`: Compares other schematic representations with larger general-purpose LLMs; the abstract does not list all names.
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### Smart-PCLib: A LLM-based Multi-Agent Framework for Automated PCB Component Library Generation

- **Metadata:** 2026 · Design, Automation and Test in Europe · Zhaohai Di, Jindong Tu, Zhiyuan He, Yuan Pu, Jiawei Liu, Chong Tong, Tsung-Yi Ho, Bei Yu, et al. · [paper](https://doi.org/10.23919/date69613.2026.11539310)
- **Scope and topics:** `pcb-core` · `schematic-design`, `thermal-reliability`, `testing-inspection`, `benchmarks-tools`, `ai-eda`
- **Code:** not_found: No verified public code repository was found.
- **Dataset or data source:** `reported_in_abstract`: The abstract mentions a dataset, benchmark, or real, industrial, or simulated data; only names that can be identified are retained.
- **Application scenario:** Schematic and design-chain automation.
- **Problem addressed:** `reported_in_abstract`: The abstract describes the PCB design problem.
- **Final evaluation:** `reported_in_abstract`: The abstract reports an experiment or evaluation; the metric field lists only items explicitly mentioned in the abstract. Metrics: accuracy.
- **Baselines:** `reported_but_unnamed_in_abstract`: The abstract mentions a comparison but does not name the baseline.
- **Evidence boundary:** `abstract`; checked on 2026-08-11.

### PCBSmith: An Effective Schematic Generator for Testing PCB Design Tool Chain

- **Metadata:** 2025 · IEEE Transactions on Reliability · Xu Zhao, He Jiang, Xiaochen Li, Shikai Guo, Zhilei Ren, Peiyu Zou, Huijiang Liu · [paper](https://doi.org/10.1109/tr.2025.3529303)
- **Scope and topics:** `pcb-core` · `schematic-design`, `thermal-reliability`, `testing-inspection`, `benchmarks-tools`
- **Code:** not_found: No verified public code repository was found.
- **Dataset or data source:** `reported_in_abstract`: The abstract mentions a dataset, benchmark, or real, industrial, or simulated data; only names that can be identified are retained.
- **Application scenario:** Schematic and design-chain automation.
- **Problem addressed:** `reported_in_abstract`: The abstract describes the PCB design problem.
- **Final evaluation:** `reported_in_abstract`: The abstract reports an experiment or evaluation; the metric field lists only items explicitly mentioned in the abstract. Metrics: not explicitly listed in the accessible sources.
- **Baselines:** `reported_but_unnamed_in_abstract`: The abstract mentions a comparison but does not name the baseline.
- **Evidence boundary:** `abstract`; checked on 2026-08-11.

### AEM-PCB Reverser: Circuit Schematic Generation in PCB Reverse Engineering Using Reinforcement Learning Based on Aesthetic Evaluation Metric

- **Metadata:** 2024 · IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems · Jie Yang, Kai Qiao, S. Shi, Baojie Song, Jian Chen, B. Yan · [paper](https://doi.org/10.1109/tcad.2023.3340869)
- **Scope and topics:** `pcb-core` · `schematic-design`, `thermal-reliability`, `testing-inspection`, `benchmarks-tools`, `ai-eda`
- **Code:** not_found: No verified public code repository was found.
- **Dataset or data source:** `not_reported_in_accessible_source`: The accessible metadata or abstract does not report this field.
- **Application scenario:** Schematic and design-chain automation.
- **Problem addressed:** `reported_in_abstract`: The abstract describes the PCB design problem.
- **Final evaluation:** `reported_in_abstract`: The abstract reports an experiment or evaluation; the metric field lists only items explicitly mentioned in the abstract. Metrics: not explicitly listed in the accessible sources.
- **Baselines:** `reported_but_unnamed_in_abstract`: The abstract mentions a comparison but does not name the baseline.
- **Evidence boundary:** `abstract`; checked on 2026-08-11.

### Impact of Line Length and Component Selection on RF Performance for a PCB-based Ferromagnetic Nonlinear Transmission Line

- **Metadata:** 2024 · IEEE International Power Modulator and High Voltage Conference · T. Wright, D. Saheb, J. Schrock, E. Schrock, J. Mankowski, James Dickens, A. Neuber, Jacob Stephens · [paper](https://doi.org/10.2172/2565141)
- **Scope and topics:** `pcb-core` · `schematic-design`
- **Code:** not_found: No public code repository was found in the sources checked.
- **Dataset or data source:** `not_reported_in_accessible_source`: The accessible metadata do not report a dataset or data source.
- **Application scenario:** Schematic and design-chain automation.
- **Problem addressed:** `not_reported_in_accessible_source`: The accessible metadata do not report the specific problem statement.
- **Final evaluation:** `not_reported_in_accessible_source`: The accessible metadata do not report final tests, metrics, or numerical results. Metrics: not explicitly listed in the accessible sources.
- **Baselines:** `not_reported_in_accessible_source`: The accessible metadata do not list a baseline.
- **Evidence boundary:** `metadata-only`; checked on 2026-08-11.

### Multi-modal printed circuit board netlist extraction with x-ray and optical imaging

- **Metadata:** 2024 · Optical Engineering + Applications · Patrick J. Craig, Nitin Varshney, Antika Roy, Shajib Ghosh, C. Patil, H. Dalir, N. Asadizanjani · [paper](https://doi.org/10.1117/12.3027170)
- **Scope and topics:** `pcb-core` · `schematic-design`, `testing-inspection`, `benchmarks-tools`
- **Code:** not_found: No verified public code repository was found.
- **Dataset or data source:** `not_reported_in_accessible_source`: The accessible metadata or abstract does not report this field.
- **Application scenario:** Schematic and design-chain automation.
- **Problem addressed:** `reported_in_abstract`: The abstract describes the PCB design problem.
- **Final evaluation:** `reported_in_abstract`: The abstract reports an experiment or evaluation; the metric field lists only items explicitly mentioned in the abstract. Metrics: not explicitly listed in the accessible sources.
- **Baselines:** `not_reported_in_accessible_source`: The accessible metadata or abstract does not list a baseline.
- **Evidence boundary:** `abstract`; checked on 2026-08-11.

### A Novel Modular Design and Modeling Methodology for High Speed High Density Die Package PCB Co-Simulation and Model Library Creation

- **Metadata:** 2016 · 2016 IEEE 66th Electronic Components and Technology Conference (ECTC) · Jenny Xiaohong Jiang, Chit Zhung Tan, Xinyun Guo, Lei Hua, Yee Huan Yew, Nate Unger, Hui Liu, Pheak Ti Teh · [paper](https://doi.org/10.1109/ectc.2016.237)
- **Scope and topics:** `pcb-core` · `schematic-design`, `benchmarks-tools`
- **Code:** not_reported_in_accessible_source: The accessible DOI and Crossref metadata do not report a verifiable code repository.
- **Dataset or data source:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not report a dataset or data source.
- **Application scenario:** The title concerns PCB or board-level design, interconnects, package-to-board SI/PI, or manufacturing and testing. This classification is inferred from the title and the ECTC DOI record; it is not treated as an experimental finding.
- **Problem addressed:** `inferred_from_title`: The paper addresses the PCB or board-level task described by its title. The precise problem boundary requires the full paper.
- **Final evaluation:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not report final tests, metrics, or numerical results. Metrics: not explicitly listed in the accessible sources.
- **Baselines:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not list a baseline.
- **Evidence boundary:** `metadata-only`; checked on 2026-08-11.

### Modeling methodologies for multi level PCB-package co-simulation & co-design

- **Metadata:** 2013 · 2013 IEEE 22nd Conference on Electrical Performance of Electronic Packaging and Systems · Antonio Ciccomancini Scogna, ChunTong Chiang, Linus Lau, LianKheng Teoh, HsuenYen Lee · [paper](https://doi.org/10.1109/epeps.2013.6703466)
- **Scope and topics:** `pcb-core` · `schematic-design`, `benchmarks-tools`
- **Code:** not_reported_in_accessible_source: The accessible DOI and Crossref metadata do not report a verifiable code repository.
- **Dataset or data source:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not report a dataset or data source.
- **Application scenario:** The title concerns PCB or board-level design, interconnects, package-to-board SI/PI, or manufacturing and testing. This classification is inferred from the title and the EPEPS DOI record; it is not treated as an experimental finding.
- **Problem addressed:** `inferred_from_title`: The paper addresses the PCB or board-level task described by its title. The precise problem boundary requires the full paper.
- **Final evaluation:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not report final tests, metrics, or numerical results. Metrics: not explicitly listed in the accessible sources.
- **Baselines:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not list a baseline.
- **Evidence boundary:** `metadata-only`; checked on 2026-08-11.

### An Integrated System for Interactive Editing of Schematics, Logic Simulation and PCB Layout Design

- **Metadata:** 1978 · Design Automation Conference · H. Bayegan, E. Aas · [paper](https://doi.org/10.1109/dac.1978.1585140)
- **Scope and topics:** `pcb-core` · `schematic-design`
- **Code:** not_found: No public code repository was found in the sources checked.
- **Dataset or data source:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not report a dataset or data source.
- **Application scenario:** Schematic and design-chain automation.
- **Problem addressed:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not report the specific problem statement.
- **Final evaluation:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not report final tests, metrics, or numerical results. Metrics: not explicitly listed in the accessible sources.
- **Baselines:** `not_reported_in_accessible_source`: The accessible DOI and Crossref metadata do not list a baseline.
- **Evidence boundary:** `metadata-only`; checked on 2026-08-11.
