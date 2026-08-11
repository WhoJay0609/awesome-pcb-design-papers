# 原理图、网表与设计链自动化 / Schematic and design-chain automation

共 14 篇主分类论文。详细字段均来自 `data/papers.json`；`not_reported` 表示当前可访问证据未说明。

| Year | Paper | Venue | Code | Evidence |
|---:|---|---|---|---|
| 2026 | [OmniSch: A Multimodal PCB Schematic Benchmark For Structured Diagram Visual Reasoning](#omnisch-a-multimodal-pcb-schematic-benchmark-for-structured-diagram-visual-reasoning) | arXiv | not_found | project-page |
| 2026 | [PCB-Migrator: Automated PCB PnR Migration](#pcb-migrator-automated-pcb-pnr-migration) | Design, Automation and Test in Europe · **DATE** | not_found | abstract |
| 2026 | [PCB-QA: A Task-Specific Question Answering Framework for Text-Centric Chip Datasheet Queries in PCB Design](#pcb-qa-a-task-specific-question-answering-framework-for-text-centric-chip-datasheet-queries-in-pcb-design) | ACM Transactions on Design Automation of Electronic Systems | not_found | abstract |
| 2026 | [pcbGPT: Automatic PCB Schematic Synthesis from Natural Language Requirements](#pcbgpt-automatic-pcb-schematic-synthesis-from-natural-language-requirements) | arXiv | not_found | full-text |
| 2026 | [PCBSchemaGen: Reward-Guided LLM Code Synthesis for Printed Circuit Boards (PCB) Schematic Design with Structured Verification](#pcbschemagen-reward-guided-llm-code-synthesis-for-printed-circuit-boards-pcb-schematic-design-with-structured-verification) | arXiv | open | project-page |
| 2026 | [SchGen: PCB Schematic Generation with Semantic-Grounded Code Representations](#schgen-pcb-schematic-generation-with-semantic-grounded-code-representations) | arXiv | open | project-page |
| 2026 | [Smart-PCLib: A LLM-based Multi-Agent Framework for Automated PCB Component Library Generation](#smart-pclib-a-llm-based-multi-agent-framework-for-automated-pcb-component-library-generation) | Design, Automation and Test in Europe · **DATE** | not_found | abstract |
| 2025 | [PCBSmith: An Effective Schematic Generator for Testing PCB Design Tool Chain](#pcbsmith-an-effective-schematic-generator-for-testing-pcb-design-tool-chain) | IEEE Transactions on Reliability | not_found | abstract |
| 2024 | [AEM-PCB Reverser: Circuit Schematic Generation in PCB Reverse Engineering Using Reinforcement Learning Based on Aesthetic Evaluation Metric](#aem-pcb-reverser-circuit-schematic-generation-in-pcb-reverse-engineering-using-reinforcement-learning-based-on-aesthetic-evaluation-metric) | IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems | not_found | abstract |
| 2024 | [Impact of Line Length and Component Selection on RF Performance for a PCB-based Ferromagnetic Nonlinear Transmission Line](#impact-of-line-length-and-component-selection-on-rf-performance-for-a-pcb-based-ferromagnetic-nonlinear-transmission-line) | IEEE International Power Modulator and High Voltage Conference | not_found | metadata-only |
| 2024 | [Multi-modal printed circuit board netlist extraction with x-ray and optical imaging](#multi-modal-printed-circuit-board-netlist-extraction-with-x-ray-and-optical-imaging) | Optical Engineering + Applications | not_found | abstract |
| 2016 | [A Novel Modular Design and Modeling Methodology for High Speed High Density Die Package PCB Co-Simulation and Model Library Creation](#a-novel-modular-design-and-modeling-methodology-for-high-speed-high-density-die-package-pcb-co-simulation-and-model-library-creation) | 2016 IEEE 66th Electronic Components and Technology Conference (ECTC) · **ECTC** | not_reported_in_accessible_source | metadata-only |
| 2013 | [Modeling methodologies for multi level PCB-package co-simulation & co-design](#modeling-methodologies-for-multi-level-pcb-package-co-simulation--co-design) | 2013 IEEE 22nd Conference on Electrical Performance of Electronic Packaging and Systems · **EPEPS** | not_reported_in_accessible_source | metadata-only |
| 1978 | [An Integrated System for Interactive Editing of Schematics, Logic Simulation and PCB Layout Design](#an-integrated-system-for-interactive-editing-of-schematics-logic-simulation-and-pcb-layout-design) | Design Automation Conference · **DAC** | not_found | metadata-only |

## Paper cards

### OmniSch: A Multimodal PCB Schematic Benchmark For Structured Diagram Visual Reasoning

- **元数据：** 2026 · arXiv · Taiting Lu, Kaiyuan Lin, Yuxin Tian, Yubo Wang, Muchuan Wang, Mahanth Gowda · [paper](https://arxiv.org/abs/2604.00270)
- **范围/主题：** `pcb-core` · `schematic-design`, `benchmarks-tools`, `ai-eda`
- **代码：** not_found — 项目页发布了数据下载，但未核验到完整代码仓库。
- **数据集/数据来源：** `open` — OmniSch
- **应用场景：** 多模态 PCB 原理图理解、视觉定位、原理图到网表图构建与工具调用。
- **解决问题：** `reported` — 建立面向真实 PCB 原理图结构化视觉推理的统一任务与标注基准。
- **最终测试：** `reported` — 按 symbol/pin/text、net graph 与 agent task 分层测试，并采用 80/10/10 划分评估经典管线。 指标：F1, IoU, graph edit distance, Kendall tau, pass rate。
- **Baselines：** `named` — YOLO11, PaddleOCR, GPT-5.2, GPT-5-mini, Claude Sonnet 4.6, Gemini, Qwen, human engineers
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### PCB-Migrator: Automated PCB PnR Migration

- **元数据：** 2026 · Design, Automation and Test in Europe · Yaohui Han, Beichen Li, Rongliang Fu, Qunsong Ye, Zhiyuan Lu, Junchen Liu, Bei Yu, Tsung-Yi Ho, et al. · [paper](https://doi.org/10.23919/date69613.2026.11539307)
- **范围/主题：** `pcb-core` · `placement`, `routing`, `schematic-design`, `thermal-reliability`, `benchmarks-tools`
- **代码：** not_found — 未发现经核验的公开代码仓库。
- **数据集/数据来源：** `not_reported_in_accessible_source` — 公开可访问的元数据/摘要未报告。
- **应用场景：** 原理图、网表与设计链自动化（Schematic and design-chain automation）。
- **解决问题：** `reported_in_abstract` — 论文围绕题名所述的 PCB 设计问题展开：PCB-Migrator: Automated PCB PnR Migration
- **最终测试：** `reported_in_abstract` — 摘要报告了实验或评估；指标字段仅列出摘要中明确出现的项目。 指标：未在可访问来源中明确列出。
- **Baselines：** `reported_but_unnamed_in_abstract` — 摘要提到比较但未点名 baseline。
- **证据边界：** `abstract`；核验日期 2026-08-11。未报告不等于不存在。

### PCB-QA: A Task-Specific Question Answering Framework for Text-Centric Chip Datasheet Queries in PCB Design

- **元数据：** 2026 · ACM Transactions on Design Automation of Electronic Systems · Binwu Zhu, Bei Yu · [paper](https://doi.org/10.1145/3811922)
- **范围/主题：** `pcb-core` · `placement`, `schematic-design`, `testing-inspection`, `benchmarks-tools`
- **代码：** not_found — 未发现经核验的公开代码仓库。
- **数据集/数据来源：** `reported_in_abstract` — 摘要提到数据集、基准或真实/工业/仿真数据；仅保留可确定的名称。
- **应用场景：** 原理图、网表与设计链自动化（Schematic and design-chain automation）。
- **解决问题：** `reported_in_abstract` — 论文围绕题名所述的 PCB 设计问题展开：PCB-QA: A Task-Specific Question Answering Framework for Text-Centric Chip Datasheet Queries in PCB Design
- **最终测试：** `reported_in_abstract` — 摘要报告了实验或评估；指标字段仅列出摘要中明确出现的项目。 指标：accuracy。
- **Baselines：** `reported_but_unnamed_in_abstract` — 摘要提到比较但未点名 baseline。
- **证据边界：** `abstract`；核验日期 2026-08-11。未报告不等于不存在。

### pcbGPT: Automatic PCB Schematic Synthesis from Natural Language Requirements

- **元数据：** 2026 · arXiv · Tobias King, Steven Kehrberg, Michael Beigl, Tobias Röddiger · [paper](https://arxiv.org/abs/2606.01188)
- **范围/主题：** `pcb-core` · `schematic-design`, `ai-eda`
- **代码：** not_found — 未核验到公开代码/数据仓库。
- **数据集/数据来源：** `reported` — pcbGPT-20 tasks
- **应用场景：** 把 embedded/IoT/wearable 自然语言需求转换为可编辑 KiCad projects。
- **解决问题：** `reported` — 结合 DSL、器件库检索、datasheet grounding 和执行检查生成可用原理图。
- **最终测试：** `reported` — 最佳模型 pass@1=0.90、pass@5=1.00；hard tasks 的 pass@1=0.72。 指标：pass@1, pass@5。
- **Baselines：** `reported_but_unnamed` — 比较模型变体和任务难度分层，未报告外部 baseline。
- **证据边界：** `full-text`；核验日期 2026-08-11。未报告不等于不存在。

### PCBSchemaGen: Reward-Guided LLM Code Synthesis for Printed Circuit Boards (PCB) Schematic Design with Structured Verification

- **元数据：** 2026 · arXiv · Huanghaohe Zou, Peng Han, Emad Nazerian, Mafu Zhang, Zhicheng Guo, Alex Q. Huang · [paper](https://arxiv.org/abs/2602.00510)
- **范围/主题：** `pcb-core` · `schematic-design`, `benchmarks-tools`, `ai-eda`
- **代码：** [open](https://github.com/HZou9/PCBSchemaGen_v2) — MIT 仓库含 benchmarks、知识图谱、验证器和配置。
- **数据集/数据来源：** `open` — PCBBench, Open-Schematics-Eval
- **应用场景：** 从自然语言需求生成 PCB 原理图，并用 datasheet KG 和确定性验证器修复。
- **解决问题：** `reported` — 在不训练专用大模型的前提下生成可验证、可编辑的 PCB schematic。
- **最终测试：** `reported` — 五层结构验证；Gemma-4-31B 平均通过 81.3%，并测试 held-out public schematics。 指标：pass rate。
- **Baselines：** `named` — Circuitron-style prompting
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### SchGen: PCB Schematic Generation with Semantic-Grounded Code Representations

- **元数据：** 2026 · arXiv · Qinpei Luo, Ruichun Ma, Xinyu Zhang, Lili Qiu · [paper](https://arxiv.org/abs/2605.30345)
- **范围/主题：** `pcb-core` · `schematic-design`, `benchmarks-tools`, `ai-eda`
- **代码：** [open](https://github.com/microsoft/SchGen) — Microsoft 仓库公开模型、数据集链接和 KiCad 生成流程。
- **数据集/数据来源：** `open` — SchGen_dataset
- **应用场景：** 自然语言到可编辑 KiCad 原理图的语义代码生成。
- **解决问题：** `reported` — 用语义 grounded representation 提高连线和功能结构的可执行性。
- **最终测试：** `reported` — 比较连线正确性与功能正确性；公开摘要未给完整数值。 指标：wire-connectivity accuracy, functional correctness。
- **Baselines：** `reported_but_unnamed` — 比较其他 schematic representations 与更大的通用 LLM，摘要未列全名称。
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### Smart-PCLib: A LLM-based Multi-Agent Framework for Automated PCB Component Library Generation

- **元数据：** 2026 · Design, Automation and Test in Europe · Zhaohai Di, Jindong Tu, Zhiyuan He, Yuan Pu, Jiawei Liu, Chong Tong, Tsung-Yi Ho, Bei Yu, et al. · [paper](https://doi.org/10.23919/date69613.2026.11539310)
- **范围/主题：** `pcb-core` · `schematic-design`, `thermal-reliability`, `testing-inspection`, `benchmarks-tools`, `ai-eda`
- **代码：** not_found — 未发现经核验的公开代码仓库。
- **数据集/数据来源：** `reported_in_abstract` — 摘要提到数据集、基准或真实/工业/仿真数据；仅保留可确定的名称。
- **应用场景：** 原理图、网表与设计链自动化（Schematic and design-chain automation）。
- **解决问题：** `reported_in_abstract` — 论文围绕题名所述的 PCB 设计问题展开：Smart-PCLib: A LLM-based Multi-Agent Framework for Automated PCB Component Library Generation
- **最终测试：** `reported_in_abstract` — 摘要报告了实验或评估；指标字段仅列出摘要中明确出现的项目。 指标：accuracy。
- **Baselines：** `reported_but_unnamed_in_abstract` — 摘要提到比较但未点名 baseline。
- **证据边界：** `abstract`；核验日期 2026-08-11。未报告不等于不存在。

### PCBSmith: An Effective Schematic Generator for Testing PCB Design Tool Chain

- **元数据：** 2025 · IEEE Transactions on Reliability · Xu Zhao, He Jiang, Xiaochen Li, Shikai Guo, Zhilei Ren, Peiyu Zou, Huijiang Liu · [paper](https://doi.org/10.1109/tr.2025.3529303)
- **范围/主题：** `pcb-core` · `schematic-design`, `thermal-reliability`, `testing-inspection`, `benchmarks-tools`
- **代码：** not_found — 未发现经核验的公开代码仓库。
- **数据集/数据来源：** `reported_in_abstract` — 摘要提到数据集、基准或真实/工业/仿真数据；仅保留可确定的名称。
- **应用场景：** 原理图、网表与设计链自动化（Schematic and design-chain automation）。
- **解决问题：** `reported_in_abstract` — 论文围绕题名所述的 PCB 设计问题展开：PCBSmith: An Effective Schematic Generator for Testing PCB Design Tool Chain
- **最终测试：** `reported_in_abstract` — 摘要报告了实验或评估；指标字段仅列出摘要中明确出现的项目。 指标：未在可访问来源中明确列出。
- **Baselines：** `reported_but_unnamed_in_abstract` — 摘要提到比较但未点名 baseline。
- **证据边界：** `abstract`；核验日期 2026-08-11。未报告不等于不存在。

### AEM-PCB Reverser: Circuit Schematic Generation in PCB Reverse Engineering Using Reinforcement Learning Based on Aesthetic Evaluation Metric

- **元数据：** 2024 · IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems · Jie Yang, Kai Qiao, S. Shi, Baojie Song, Jian Chen, B. Yan · [paper](https://doi.org/10.1109/tcad.2023.3340869)
- **范围/主题：** `pcb-core` · `schematic-design`, `thermal-reliability`, `testing-inspection`, `benchmarks-tools`, `ai-eda`
- **代码：** not_found — 未发现经核验的公开代码仓库。
- **数据集/数据来源：** `not_reported_in_accessible_source` — 公开可访问的元数据/摘要未报告。
- **应用场景：** 原理图、网表与设计链自动化（Schematic and design-chain automation）。
- **解决问题：** `reported_in_abstract` — 论文围绕题名所述的 PCB 设计问题展开：AEM-PCB Reverser: Circuit Schematic Generation in PCB Reverse Engineering Using Reinforcement Learning Based on Aesthetic Evaluation Metric
- **最终测试：** `reported_in_abstract` — 摘要报告了实验或评估；指标字段仅列出摘要中明确出现的项目。 指标：未在可访问来源中明确列出。
- **Baselines：** `reported_but_unnamed_in_abstract` — 摘要提到比较但未点名 baseline。
- **证据边界：** `abstract`；核验日期 2026-08-11。未报告不等于不存在。

### Impact of Line Length and Component Selection on RF Performance for a PCB-based Ferromagnetic Nonlinear Transmission Line

- **元数据：** 2024 · IEEE International Power Modulator and High Voltage Conference · T. Wright, D. Saheb, J. Schrock, E. Schrock, J. Mankowski, James Dickens, A. Neuber, Jacob Stephens · [paper](https://doi.org/10.2172/2565141)
- **范围/主题：** `pcb-core` · `schematic-design`
- **代码：** not_found — 未发现经核验的公开代码仓库。
- **数据集/数据来源：** `not_reported_in_accessible_source` — 公开可访问元数据未报告。
- **应用场景：** 原理图、网表与设计链自动化（Schematic and design-chain automation）。
- **解决问题：** `not_reported_in_accessible_source` — 公开可访问元数据未报告。
- **最终测试：** `not_reported_in_accessible_source` — 公开可访问元数据未报告。 指标：未在可访问来源中明确列出。
- **Baselines：** `not_reported_in_accessible_source` — 公开可访问元数据未列出 baseline。
- **证据边界：** `metadata-only`；核验日期 2026-08-11。未报告不等于不存在。

### Multi-modal printed circuit board netlist extraction with x-ray and optical imaging

- **元数据：** 2024 · Optical Engineering + Applications · Patrick J. Craig, Nitin Varshney, Antika Roy, Shajib Ghosh, C. Patil, H. Dalir, N. Asadizanjani · [paper](https://doi.org/10.1117/12.3027170)
- **范围/主题：** `pcb-core` · `schematic-design`, `testing-inspection`, `benchmarks-tools`
- **代码：** not_found — 未发现经核验的公开代码仓库。
- **数据集/数据来源：** `not_reported_in_accessible_source` — 公开可访问的元数据/摘要未报告。
- **应用场景：** 原理图、网表与设计链自动化（Schematic and design-chain automation）。
- **解决问题：** `reported_in_abstract` — 论文围绕题名所述的 PCB 设计问题展开：Multi-modal printed circuit board netlist extraction with x-ray and optical imaging
- **最终测试：** `reported_in_abstract` — 摘要报告了实验或评估；指标字段仅列出摘要中明确出现的项目。 指标：未在可访问来源中明确列出。
- **Baselines：** `not_reported_in_accessible_source` — 公开可访问的元数据/摘要未列出 baseline。
- **证据边界：** `abstract`；核验日期 2026-08-11。未报告不等于不存在。

### A Novel Modular Design and Modeling Methodology for High Speed High Density Die Package PCB Co-Simulation and Model Library Creation

- **元数据：** 2016 · 2016 IEEE 66th Electronic Components and Technology Conference (ECTC) · Jenny Xiaohong Jiang, Chit Zhung Tan, Xinyun Guo, Lei Hua, Yee Huan Yew, Nate Unger, Hui Liu, Pheak Ti Teh · [paper](https://doi.org/10.1109/ectc.2016.237)
- **范围/主题：** `pcb-core` · `schematic-design`, `benchmarks-tools`
- **代码：** not_reported_in_accessible_source — 可访问 DOI/Crossref 元数据未报告可核验代码仓库。
- **数据集/数据来源：** `not_reported_in_accessible_source` — 可访问 DOI/Crossref 元数据未报告可核验数据集或数据源。
- **应用场景：** 题名明确涉及 PCB/板级设计、互连、封装-板级 SI/PI 或制造测试；此场景归类由题名和 ECTC DOI 记录推断，未将推断当作实验事实。
- **解决问题：** `inferred_from_title` — 围绕题名所示的 PCB/板级任务：A Novel Modular Design and Modeling Methodology for High Speed High Density Die Package PCB Co-Simulation and Model Library Creation；具体问题边界需查阅论文全文。
- **最终测试：** `not_reported_in_accessible_source` — 可访问 DOI/Crossref 元数据未报告最终测试、指标或数值结果。 指标：未在可访问来源中明确列出。
- **Baselines：** `not_reported_in_accessible_source` — 可访问 DOI/Crossref 元数据未列出 baseline。
- **证据边界：** `metadata-only`；核验日期 2026-08-11。未报告不等于不存在。

### Modeling methodologies for multi level PCB-package co-simulation & co-design

- **元数据：** 2013 · 2013 IEEE 22nd Conference on Electrical Performance of Electronic Packaging and Systems · Antonio Ciccomancini Scogna, ChunTong Chiang, Linus Lau, LianKheng Teoh, HsuenYen Lee · [paper](https://doi.org/10.1109/epeps.2013.6703466)
- **范围/主题：** `pcb-core` · `schematic-design`, `benchmarks-tools`
- **代码：** not_reported_in_accessible_source — 可访问 DOI/Crossref 元数据未报告可核验代码仓库。
- **数据集/数据来源：** `not_reported_in_accessible_source` — 可访问 DOI/Crossref 元数据未报告可核验数据集或数据源。
- **应用场景：** 题名明确涉及 PCB/板级设计、互连、封装-板级 SI/PI 或制造测试；此场景归类由题名和 EPEPS DOI 记录推断，未将推断当作实验事实。
- **解决问题：** `inferred_from_title` — 围绕题名所示的 PCB/板级任务：Modeling methodologies for multi level PCB-package co-simulation & co-design；具体问题边界需查阅论文全文。
- **最终测试：** `not_reported_in_accessible_source` — 可访问 DOI/Crossref 元数据未报告最终测试、指标或数值结果。 指标：未在可访问来源中明确列出。
- **Baselines：** `not_reported_in_accessible_source` — 可访问 DOI/Crossref 元数据未列出 baseline。
- **证据边界：** `metadata-only`；核验日期 2026-08-11。未报告不等于不存在。

### An Integrated System for Interactive Editing of Schematics, Logic Simulation and PCB Layout Design

- **元数据：** 1978 · Design Automation Conference · H. Bayegan, E. Aas · [paper](https://doi.org/10.1109/dac.1978.1585140)
- **范围/主题：** `pcb-core` · `schematic-design`
- **代码：** not_found — 未发现经核验的公开代码仓库。
- **数据集/数据来源：** `not_reported_in_accessible_source` — 公开可访问元数据未报告。
- **应用场景：** 原理图、网表与设计链自动化（Schematic and design-chain automation）。
- **解决问题：** `not_reported_in_accessible_source` — 公开可访问元数据未报告。
- **最终测试：** `not_reported_in_accessible_source` — 公开可访问元数据未报告。 指标：未在可访问来源中明确列出。
- **Baselines：** `not_reported_in_accessible_source` — 公开可访问元数据未列出 baseline。
- **证据边界：** `metadata-only`；核验日期 2026-08-11。未报告不等于不存在。
