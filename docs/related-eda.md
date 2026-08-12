# Related EDA references

[Back to README](../README.md) · [Catalog table](#catalog) · [Paper cards](#paper-cards)

16 related EDA references are listed here. Detailed fields come from `data/papers.json`; `not_reported` means that the accessible evidence does not state the field. Not reported does not mean absent.

## Catalog

| Year | Paper | Venue | Code | Evidence |
|---:|---|---|---|---|
| 2025 | [VerilogCoder: Autonomous Verilog Coding Agents with Graph-based Planning and AST-based Waveform Tracing Tool](#verilogcoder-autonomous-verilog-coding-agents-with-graph-based-planning-and-ast-based-waveform-tracing-tool) | AAAI 2025 | open | project-page |
| 2024 | [ATPlace2.5D: Analytical Thermal-Aware Chiplet Placement Framework for Large-Scale 2.5D-IC](#atplace25d-analytical-thermal-aware-chiplet-placement-framework-for-large-scale-25d-ic) | ICCAD 2024 | not found | full-text |
| 2024 | [ChatEDA: A Large Language Model Powered Autonomous Agent for EDA](#chateda-a-large-language-model-powered-autonomous-agent-for-eda) | IEEE TCAD | open | project-page |
| 2024 | [CircuitNet 2.0: An Advanced Dataset for Promoting Machine Learning Innovations in Realistic Chip Design Environment](#circuitnet-20-an-advanced-dataset-for-promoting-machine-learning-innovations-in-realistic-chip-design-environment) | ICLR 2024 | open | project-page |
| 2024 | [RoutePlacer: An End-to-End Routability-Aware Placer with Graph Neural Network](#routeplacer-an-end-to-end-routability-aware-placer-with-graph-neural-network) | KDD 2024 | open | project-page |
| 2024 | [RTLFixer: Automatically Fixing RTL Syntax Errors with Large Language Models](#rtlfixer-automatically-fixing-rtl-syntax-errors-with-large-language-models) | DAC 2024 | open | project-page |
| 2023 | [ChiPFormer: Transferable Chip Placement via Offline Decision Transformer](#chipformer-transferable-chip-placement-via-offline-decision-transformer) | ICML 2023 | open | project-page |
| 2023 | [Circuit as Set of Points](#circuit-as-set-of-points) | NeurIPS 2023 | open | project-page |
| 2022 | [The Policy-gradient Placement and Generative Routing Neural Networks for Chip Design](#the-policy-gradient-placement-and-generative-routing-neural-networks-for-chip-design) | NeurIPS 2022 | open | project-page |
| 2021 | [A Graph Placement Methodology for Fast Chip Design](#a-graph-placement-methodology-for-fast-chip-design) | Nature | partial open | project-page |
| 2020 | [AutoCkt: Deep Reinforcement Learning of Analog Circuit Designs](#autockt-deep-reinforcement-learning-of-analog-circuit-designs) | DATE 2020 | open | project-page |
| 2019 | [DREAMPlace: Deep Learning Toolkit-Enabled GPU Acceleration for Modern VLSI Placement](#dreamplace-deep-learning-toolkit-enabled-gpu-acceleration-for-modern-vlsi-placement) | DAC 2019 | open | project-page |
| 2019 | [RePlAce: Advancing Solution Quality and Routability Validation in Global Placement](#replace-advancing-solution-quality-and-routability-validation-in-global-placement) | IEEE TCAD | open (archived) | project-page |
| 2019 | [Toward an Open-Source Digital Flow: First Learnings from the OpenROAD Project](#toward-an-open-source-digital-flow-first-learnings-from-the-openroad-project) | DAC 2019 | open | project-page |
| 2018 | [RouteNet: Routability Prediction for Mixed-Size Designs Using Convolutional Neural Network](#routenet-routability-prediction-for-mixed-size-designs-using-convolutional-neural-network) | ICCAD 2018 | not found | full-text |
| 2014 | [ePlace: Electrostatics Based Placement Using Nesterov's Method](#eplace-electrostatics-based-placement-using-nesterovs-method) | DAC 2014 | not found | full-text |

## Paper cards

### VerilogCoder: Autonomous Verilog Coding Agents with Graph-based Planning and AST-based Waveform Tracing Tool

- **Metadata:** 2025 · AAAI 2025 · Chia-Tung Ho, Haoxing Ren, Brucek Khailany · [paper](https://doi.org/10.1609/aaai.v39i1.32007)
- **Scope and topics:** `related-eda` · `schematic-design`, `testing-inspection`, `ai-eda`
- **Code:** [open](https://github.com/NVlabs/VerilogCoder): The multi-agent coding, planner, and waveform tracer components are publicly available.
- **Dataset or data source:** `public_benchmark`: VerilogEval-Human v2
- **Application scenario:** A hardware coding agent combines graph planning with a syntax checker, simulator, and AST waveform tracing.
- **Problem addressed:** `reported`: The approach lets an LLM locate functional errors through an external verifier and fix them iteratively.
- **Final evaluation:** `reported`: The paper reports 94.2% correctness and a 33.9% improvement over the previous SOTA; it also includes planner and tracer ablations. Metrics: syntactic and functional correctness.
- **Baselines:** `reported`: prior Verilog coding SOTA
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### ATPlace2.5D: Analytical Thermal-Aware Chiplet Placement Framework for Large-Scale 2.5D-IC

- **Metadata:** 2024 · ICCAD 2024 · Qipan Wang, Xueqing Li, Tianyu Jia, Yibo Lin, Runsheng Wang, Ru Huang · [paper](https://doi.org/10.1145/3676536.3676648)
- **Scope and topics:** `related-eda` · `placement`, `thermal-reliability`
- **Code:** not_found: No official code repository was found.
- **Dataset or data source:** `benchmark_suite`: 60+ chiplet benchmarks
- **Application scenario:** Thermal-aware analytical placement for large 2.5D chiplet/interposer designs.
- **Problem addressed:** `reported`: It jointly handles legal orientation, density, wirelength, and a fast physical thermal model.
- **Final evaluation:** `reported`: The reported results include about 1.2C thermal MAE, a 2575x speedup for thermal evaluation, 5% max-T improvement, 42% wirelength improvement, and 23x acceleration. Metrics: maximum temperature, wirelength, thermal MAE, runtime.
- **Baselines:** `named`: TAP-2.5D, HotSpot
- **Evidence boundary:** `full-text`; checked on 2026-08-11.

### ChatEDA: A Large Language Model Powered Autonomous Agent for EDA

- **Metadata:** 2024 · IEEE TCAD · Haoyuan Wu, Zhuolun He, Xinyun Zhang, Xufeng Yao, Su Zheng, Haisheng Zheng, Bei Yu · [paper](https://doi.org/10.1109/tcad.2024.3383347)
- **Scope and topics:** `related-eda` · `benchmarks-tools`, `ai-eda`, `placement`, `routing`
- **Code:** [open](https://github.com/wuhy68/ChatEDA): The repository provides the agent, benchmark, and tool-call data.
- **Dataset or data source:** [open](https://github.com/wuhy68/ChatEDA): [ChatEDA-Bench](https://github.com/wuhy68/ChatEDA)
- **Application scenario:** It decomposes natural-language tasks, generates scripts, and executes OpenROAD APIs across the RTL-to-GDSII flow.
- **Problem addressed:** `reported`: It turns an LLM into an EDA agent that can execute tools, use feedback, and tune parameters.
- **Final evaluation:** `reported`: AutoMage2 achieves 82% Grade A, compared with 62% for GPT-4, 46% for Claude2, and 28% for GPT-3.5. Metrics: Grade A/B/C, executable script rate.
- **Baselines:** `named`: GPT-4, Claude2, GPT-3.5, AutoMage
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### CircuitNet 2.0: An Advanced Dataset for Promoting Machine Learning Innovations in Realistic Chip Design Environment

- **Metadata:** 2024 · ICLR 2024 · Xun Jiang, Zhuomin Chai, Yuxiang Zhao, Yibo Lin, Runsheng Wang, Ru Huang · [paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/464917b6103e074e1f9df7a2bf3bf6ba-Abstract-Conference.html)
- **Scope and topics:** `related-eda` · `benchmarks-tools`, `routing`, `si-pi-emc`, `thermal-reliability`, `ai-eda`
- **Code:** [open](https://github.com/circuitnet/CircuitNet): The official repository provides the data and task entry points.
- **Dataset or data source:** [open_with_upstream_terms](https://github.com/circuitnet/CircuitNet): [CircuitNet 2.0](https://github.com/circuitnet/CircuitNet)
- **Application scenario:** A multitask ML benchmark for a realistic chip design environment.
- **Problem addressed:** `reported`: A unified, realistic dataset supports research on congestion, timing, power, and related prediction and optimization tasks.
- **Final evaluation:** `benchmark`: The benchmark provides task-specific baselines and evaluations; this entry does not reproduce all tables. Metrics: congestion metrics, timing metrics, power metrics.
- **Baselines:** `task_specific`: Baselines are task-specific and listed in the official benchmark; there is no single comparison set.
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### RoutePlacer: An End-to-End Routability-Aware Placer with Graph Neural Network

- **Metadata:** 2024 · KDD 2024 · Yunbo Hou, Haoran Ye, Yingxue Zhang, Siyuan Xu, Guojie Song · [paper](https://doi.org/10.1145/3637528.3671895)
- **Scope and topics:** `related-eda` · `placement`, `routing`, `ai-eda`
- **Code:** [open](https://github.com/sorarain/RoutePlacer): The RouteGNN/RoutePlacer implementations are publicly available.
- **Dataset or data source:** `public_benchmarks`: DAC2012, ISPD2011
- **Application scenario:** The method uses GNN-predicted congestion as a differentiable placement penalty.
- **Problem addressed:** `reported`: It optimizes placement end to end instead of discovering routing overflow after placement is complete.
- **Final evaluation:** `reported`: The evaluation reports up to 16% lower overflow at matched wirelength and a 44% reduction when two-stage placers are inserted. Metrics: Total Overflow, routed wirelength.
- **Baselines:** `named`: DREAMPlace, NCTUgr, two-stage placers
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### RTLFixer: Automatically Fixing RTL Syntax Errors with Large Language Models

- **Metadata:** 2024 · DAC 2024 · Yun-Da Tsai, Mingjie Liu, Haoxing Ren · [paper](https://doi.org/10.1145/3649329.3657353)
- **Scope and topics:** `related-eda` · `testing-inspection`, `ai-eda`, `benchmarks-tools`
- **Code:** [open](https://github.com/NVlabs/RTLFixer): The RAG/ReAct repair agent is publicly available.
- **Dataset or data source:** `public_benchmarks`: VerilogEval-Syntax, VerilogEval-Simulate
- **Application scenario:** It iteratively repairs generated Verilog with compiler feedback; this can be compared with using DRC/ERC feedback to repair PCB scripts.
- **Problem addressed:** `reported`: The method uses a retrieval and tool-execution loop to reduce syntax errors in LLM-generated RTL.
- **Final evaluation:** `reported`: The method corrects about 98.5% of compilation errors; pass@1 increases by 32.3 and 10.1 percentage points on the two VerilogEval splits, respectively. Metrics: correction rate, pass@1.
- **Baselines:** `named`: baseline prompting, VerilogEval baselines
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### ChiPFormer: Transferable Chip Placement via Offline Decision Transformer

- **Metadata:** 2023 · ICML 2023 · Yao Lai, Jinxin Liu, Zhentao Tang, Bin Wang, Jianye Hao, Ping Luo · [paper](https://proceedings.mlr.press/v202/lai23c.html)
- **Scope and topics:** `related-eda` · `placement`, `ai-eda`, `benchmarks-tools`
- **Code:** [open](https://github.com/laiyao1/chipformer): The repository provides the code, offline trajectories, and deliverables.
- **Dataset or data source:** `partial_open`: 32 circuits, 12 circuits x 500 expert placements
- **Application scenario:** It learns a transferable offline placement policy from fixed expert trajectories.
- **Problem addressed:** `reported`: It reduces costly online simulation and RL interaction on new designs.
- **Final evaluation:** `reported`: The PMLR record reports better placement quality and about a 10x runtime reduction. Metrics: HPWL, runtime, overlap, congestion.
- **Baselines:** `named`: AlphaChip, MaskPlace, DeepPR, PRNet
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### Circuit as Set of Points

- **Metadata:** 2023 · NeurIPS 2023 · Jialv Zou, Xinggang Wang, Jiahao Guo, Wenyu Liu, Qian Zhang, Chang Huang · [paper](https://papers.neurips.cc/paper_files/paper/2023/file/6697bb267dc517379bc8aa326e844f8d-Paper-Conference.pdf)
- **Scope and topics:** `related-eda` · `routing`, `ai-eda`
- **Code:** [open](https://github.com/hustvl/circuitformer): The CircuitFormer code and pretrained model are publicly available.
- **Dataset or data source:** `public_benchmarks`: CircuitNet, ISPD2015
- **Application scenario:** It represents circuit elements as raw point sets and predicts congestion and DRC violations.
- **Problem addressed:** `reported`: It avoids losing geometric and connectivity information during manual rasterization or graph preprocessing.
- **Final evaluation:** `reported`: Compared with CNN, GNN, and painting baselines, it reports average improvements of about 3.8% on CircuitNet and 1.5% on ISPD2015. Metrics: Pearson, Spearman, Kendall, DRC metrics.
- **Baselines:** `reported`: CNN baselines, GNN baselines, painting-based baselines
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### The Policy-gradient Placement and Generative Routing Neural Networks for Chip Design

- **Metadata:** 2022 · NeurIPS 2022 · Ruoyu Cheng, Xianglong Lyu, Yang Li, Junjie Ye, Jianye Hao, Junchi Yan · [paper](https://proceedings.neurips.cc/paper_files/paper/2022/hash/a8b8c1ad51df1b93d9e3d1fca75debbf-Abstract-Conference.html)
- **Scope and topics:** `related-eda` · `placement`, `routing`, `ai-eda`
- **Code:** [open](https://github.com/Thinklab-SJTU/EDA-AI): The EDA-AI repository provides related implementations; reproduction dependencies must be prepared separately.
- **Dataset or data source:** `public_benchmarks`: ISPD2005, ISPD2007, ISPD1998, Route-small, Route-large
- **Application scenario:** It combines PPO mixed-size placement with conditional generative global routing.
- **Problem addressed:** `reported`: Jointly learning placement and route generation reduces objective mismatch from sequential optimization.
- **Final evaluation:** `reported`: The evaluation covers placement and global routing quality; the concurrent variant reports a 3.36x to 7.98x speedup. Metrics: HPWL, overlap, wirelength, routing congestion, runtime.
- **Baselines:** `named`: DeepPlace, CVAE, cGAN, U-Net, ResNet, NTHU-Route2.0, BoxRouter2.0, FastRoute3.0
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### A Graph Placement Methodology for Fast Chip Design

- **Metadata:** 2021 · Nature · Azalia Mirhoseini, Anna Goldie, Mustafa Yazgan, Joe Wenjie Jiang, Jeff Dean · [paper](https://doi.org/10.1038/s41586-021-03544-w)
- **Scope and topics:** `related-eda` · `placement`, `ai-eda`
- **Code:** [partial_open](https://github.com/google-research/circuit_training): The training framework is public; TPU cases and training data remain proprietary.
- **Dataset or data source:** `mixed_public_private`: Ariane RISC-V, TPU blocks
- **Application scenario:** Graph-state reinforcement learning performs sequential macro floorplanning, followed by commercial EDA for standard-cell placement.
- **Problem addressed:** `reported`: A GCN policy uses tool feedback to generate macro placements automatically.
- **Final evaluation:** `reported`: The evaluation measures proxy wirelength/congestion and final PPA. Metrics: wirelength, congestion, density, PPA.
- **Baselines:** `named`: RePlAce, commercial flow, human layouts
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### AutoCkt: Deep Reinforcement Learning of Analog Circuit Designs

- **Metadata:** 2020 · DATE 2020 · Keertana Settaluri, Ameer Haj-Ali, Qijing Huang, Kourosh Hakhamaneshi, Borivoje Nikolic · [paper](https://doi.org/10.23919/date48585.2020.9116200)
- **Scope and topics:** `related-eda` · `schematic-design`, `ai-eda`
- **Code:** [open](https://github.com/ksettaluri6/AutoCkt): The analog-circuit RL optimization code is publicly available.
- **Dataset or data source:** `simulation_flow`: Berkeley Analog Generator, op-amp topologies
- **Application scenario:** The application is analog schematic and post-layout sizing; it is included as a transferable reference for PCB BOM and parameter optimization.
- **Problem addressed:** `reported`: It meets multiple analog-circuit specifications with sparse sampling and includes parasitic-aware simulation.
- **Final evaluation:** `reported`: It reports at least 96.3% schematic-goal satisfaction, about 40x faster than GA, and 40 LVS-passed op-amps generated in 68 hours. Metrics: goal satisfaction, runtime, LVS pass.
- **Baselines:** `named`: genetic algorithm, prior parasitic-aware method
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### DREAMPlace: Deep Learning Toolkit-Enabled GPU Acceleration for Modern VLSI Placement

- **Metadata:** 2019 · DAC 2019 · Yibo Lin, Shounak Dhar, Wuxi Li, Haoxing Ren, Brucek Khailany, David Z. Pan · [paper](https://doi.org/10.1145/3316781.3317803)
- **Scope and topics:** `related-eda` · `placement`, `benchmarks-tools`, `ai-eda`
- **Code:** [open](https://github.com/limbo018/DREAMPlace): The PyTorch/CUDA placement toolkit is publicly available.
- **Dataset or data source:** `public_and_industrial`: ISPD2005, ISPD2015
- **Application scenario:** The application is GPU-accelerated differentiable IC placement; it is included as a reference for parallel optimization kernels on large-scale PCBs.
- **Problem addressed:** `reported`: It maps wirelength/density objectives to automatic differentiation and GPU kernels in a deep-learning framework.
- **Final evaluation:** `reported`: The official page reports about a 40x global-placement speedup over RePlAce with no quality loss. Metrics: runtime, placement quality.
- **Baselines:** `named`: RePlAce, NTUPlace3
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### RePlAce: Advancing Solution Quality and Routability Validation in Global Placement

- **Metadata:** 2019 · IEEE TCAD · Chung-Kuan Cheng, Andrew B. Kahng, Ilgweon Kang, Lutong Wang · [paper](https://doi.org/10.1109/tcad.2018.2859220)
- **Scope and topics:** `related-eda` · `placement`, `routing`, `benchmarks-tools`
- **Code:** [open_archived](https://github.com/The-OpenROAD-Project/RePlAce): The repository is archived under BSD-3-Clause, and its functionality has been incorporated into OpenROAD.
- **Dataset or data source:** `public_benchmarks`: ISPD2005, ISPD2006, MMS, DAC2012, ICCAD2012
- **Application scenario:** The application is IC mixed-size global placement with routing feedback; the method may transfer to PCB routability-aware placement.
- **Problem addressed:** `reported`: It uses local density smoothing, dynamic step sizes, and routing feedback to improve legality and routability.
- **Final evaluation:** `reported`: The evaluation measures wirelength, congestion, and CPU use on the ISPD, MMS, and contest suites. Metrics: HPWL, scaled HPWL, routing congestion, runtime.
- **Baselines:** `named`: Polar 2.0, NTUplace4h, Ripple 2.0, contest-best
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### Toward an Open-Source Digital Flow: First Learnings from the OpenROAD Project

- **Metadata:** 2019 · DAC 2019 · Tutu Ajayi, Vidya A. Chhabria, Andrew B. Kahng, Sachin S. Sapatnekar, Lutong Wang · [paper](https://doi.org/10.1145/3316781.3326334)
- **Scope and topics:** `related-eda` · `benchmarks-tools`, `placement`, `routing`
- **Code:** [open](https://github.com/The-OpenROAD-Project/OpenROAD): The project provides an active, open RTL-to-GDS flow.
- **Dataset or data source:** `tool_flow`: OpenROAD flow
- **Application scenario:** It automates synthesis, floorplanning, placement, CTS, routing, and signoff.
- **Problem addressed:** `reported`: It provides a reproducible framework for full-flow tool execution and integration.
- **Final evaluation:** `system_report`: The paper focuses on flow integration and tapeout lessons, not a single ML benchmark. Metrics: flow completion, tapeout evidence.
- **Baselines:** `not_applicable`: This is a system and experience paper with no unified algorithm baseline.
- **Evidence boundary:** `project-page`; checked on 2026-08-11.

### RouteNet: Routability Prediction for Mixed-Size Designs Using Convolutional Neural Network

- **Metadata:** 2018 · ICCAD 2018 · Zhiyao Xie, Yu-Hung Huang, Guan-Qi Fang, Haoxing Ren, Shao-Yun Fang, Yiran Chen, Jiang Hu · [paper](https://doi.org/10.1145/3240765.3240843)
- **Scope and topics:** `related-eda` · `placement`, `routing`, `ai-eda`
- **Code:** not_found: No official repository was found.
- **Dataset or data source:** `generated_from_public`: ISPD2015
- **Application scenario:** It predicts total DRV and DRC hotspots before global routing.
- **Problem addressed:** `reported`: A fast CNN oracle replaces costly trial routing.
- **Final evaluation:** `reported`: It reports about 50% higher hotspot accuracy than global routing, with inference taking less than 1 second. Metrics: DRV accuracy, top-10 rank, TPR, FPR, inference time.
- **Baselines:** `named`: SVM, logistic regression, trial routing, global routing
- **Evidence boundary:** `full-text`; checked on 2026-08-11.

### ePlace: Electrostatics Based Placement Using Nesterov's Method

- **Metadata:** 2014 · DAC 2014 · Jingwei Lu, Pengwen Chen, Chin-Chih Chang, Lu Sha, Dennis J.-H. Huang, Chung-Kuan Cheng · [paper](https://doi.org/10.1145/2593069.2593133)
- **Scope and topics:** `related-eda` · `placement`
- **Code:** not_found: No maintained official repository was found.
- **Dataset or data source:** `public_benchmarks`: ISPD2005, ISPD2006, MMS
- **Application scenario:** The application is IC mixed-size global placement; it is included as a reference for continuous optimization and density modeling on PCBs.
- **Problem addressed:** `reported`: It jointly minimizes wirelength and overlap using electrostatic density and Nesterov optimization.
- **Final evaluation:** `reported`: It reports 2.83% to 7.13% wirelength improvement and 1.05x to 3.05x speedup across three benchmark families. Metrics: HPWL, runtime.
- **Baselines:** `named`: BonnPlace, MAPLE, NTUplace3-unified
- **Evidence boundary:** `full-text`; checked on 2026-08-11.
