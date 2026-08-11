# 相关 EDA 自动化参考 / Related EDA References

共 16 篇主分类论文。详细字段均来自 `data/papers.json`；`not_reported` 表示当前可访问证据未说明。

| Year | Paper | Venue | Code | Evidence |
|---:|---|---|---|---|
| 2025 | [VerilogCoder: Autonomous Verilog Coding Agents with Graph-based Planning and AST-based Waveform Tracing Tool](#verilogcoder-autonomous-verilog-coding-agents-with-graph-based-planning-and-ast-based-waveform-tracing-tool) | AAAI 2025 | open | project-page |
| 2024 | [ATPlace2.5D: Analytical Thermal-Aware Chiplet Placement Framework for Large-Scale 2.5D-IC](#atplace25d-analytical-thermal-aware-chiplet-placement-framework-for-large-scale-25d-ic) | ICCAD 2024 | not_found | full-text |
| 2024 | [ChatEDA: A Large Language Model Powered Autonomous Agent for EDA](#chateda-a-large-language-model-powered-autonomous-agent-for-eda) | IEEE TCAD | open | project-page |
| 2024 | [CircuitNet 2.0: An Advanced Dataset for Promoting Machine Learning Innovations in Realistic Chip Design Environment](#circuitnet-20-an-advanced-dataset-for-promoting-machine-learning-innovations-in-realistic-chip-design-environment) | ICLR 2024 | open | project-page |
| 2024 | [RoutePlacer: An End-to-End Routability-Aware Placer with Graph Neural Network](#routeplacer-an-end-to-end-routability-aware-placer-with-graph-neural-network) | KDD 2024 | open | project-page |
| 2024 | [RTLFixer: Automatically Fixing RTL Syntax Errors with Large Language Models](#rtlfixer-automatically-fixing-rtl-syntax-errors-with-large-language-models) | DAC 2024 | open | project-page |
| 2023 | [ChiPFormer: Transferable Chip Placement via Offline Decision Transformer](#chipformer-transferable-chip-placement-via-offline-decision-transformer) | ICML 2023 | open | project-page |
| 2023 | [Circuit as Set of Points](#circuit-as-set-of-points) | NeurIPS 2023 | open | project-page |
| 2022 | [The Policy-gradient Placement and Generative Routing Neural Networks for Chip Design](#the-policy-gradient-placement-and-generative-routing-neural-networks-for-chip-design) | NeurIPS 2022 | open | project-page |
| 2021 | [A Graph Placement Methodology for Fast Chip Design](#a-graph-placement-methodology-for-fast-chip-design) | Nature | partial_open | project-page |
| 2020 | [AutoCkt: Deep Reinforcement Learning of Analog Circuit Designs](#autockt-deep-reinforcement-learning-of-analog-circuit-designs) | DATE 2020 | open | project-page |
| 2019 | [DREAMPlace: Deep Learning Toolkit-Enabled GPU Acceleration for Modern VLSI Placement](#dreamplace-deep-learning-toolkit-enabled-gpu-acceleration-for-modern-vlsi-placement) | DAC 2019 | open | project-page |
| 2019 | [RePlAce: Advancing Solution Quality and Routability Validation in Global Placement](#replace-advancing-solution-quality-and-routability-validation-in-global-placement) | IEEE TCAD | open_archived | project-page |
| 2019 | [Toward an Open-Source Digital Flow: First Learnings from the OpenROAD Project](#toward-an-open-source-digital-flow-first-learnings-from-the-openroad-project) | DAC 2019 | open | project-page |
| 2018 | [RouteNet: Routability Prediction for Mixed-Size Designs Using Convolutional Neural Network](#routenet-routability-prediction-for-mixed-size-designs-using-convolutional-neural-network) | ICCAD 2018 | not_found | full-text |
| 2014 | [ePlace: Electrostatics Based Placement Using Nesterov's Method](#eplace-electrostatics-based-placement-using-nesterovs-method) | DAC 2014 | not_found | full-text |

## Paper cards

### VerilogCoder: Autonomous Verilog Coding Agents with Graph-based Planning and AST-based Waveform Tracing Tool

- **元数据：** 2025 · AAAI 2025 · Chia-Tung Ho, Haoxing Ren, Brucek Khailany · [paper](https://doi.org/10.1609/aaai.v39i1.32007)
- **范围/主题：** `related-eda` · `schematic-design`, `testing-inspection`, `ai-eda`
- **代码：** [open](https://github.com/NVlabs/VerilogCoder) — 公开 multi-agent coding、planner 与 waveform tracer。
- **数据集/数据来源：** `public_benchmark` — VerilogEval-Human v2
- **应用场景：** 图规划加 syntax checker、simulator 和 AST waveform tracing 的硬件 coding agent。
- **解决问题：** `reported` — 让 LLM 通过外部 verifier 定位功能错误并迭代修复。
- **最终测试：** `reported` — 达到 94.2% correctness，比此前 SOTA 高 33.9%；含 planner/tracer ablations。 指标：syntactic and functional correctness。
- **Baselines：** `reported` — prior Verilog coding SOTA
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### ATPlace2.5D: Analytical Thermal-Aware Chiplet Placement Framework for Large-Scale 2.5D-IC

- **元数据：** 2024 · ICCAD 2024 · Qipan Wang, Xueqing Li, Tianyu Jia, Yibo Lin, Runsheng Wang, Ru Huang · [paper](https://doi.org/10.1145/3676536.3676648)
- **范围/主题：** `related-eda` · `placement`, `thermal-reliability`
- **代码：** not_found — 未找到官方代码仓库。
- **数据集/数据来源：** `benchmark_suite` — 60+ chiplet benchmarks
- **应用场景：** 大型 2.5D chiplet/interposer 的 thermal-aware analytical placement。
- **解决问题：** `reported` — 联合合法方向、density、wirelength 与快速物理 thermal model。
- **最终测试：** `reported` — 约 1.2C thermal MAE、2575x thermal-evaluation speedup、5% max-T 改善、42% wirelength 改善、23x acceleration。 指标：maximum temperature, wirelength, thermal MAE, runtime。
- **Baselines：** `named` — TAP-2.5D, HotSpot
- **证据边界：** `full-text`；核验日期 2026-08-11。未报告不等于不存在。

### ChatEDA: A Large Language Model Powered Autonomous Agent for EDA

- **元数据：** 2024 · IEEE TCAD · Haoyuan Wu, Zhuolun He, Xinyun Zhang, Xufeng Yao, Su Zheng, Haisheng Zheng, Bei Yu · [paper](https://doi.org/10.1109/tcad.2024.3383347)
- **范围/主题：** `related-eda` · `benchmarks-tools`, `ai-eda`, `placement`, `routing`
- **代码：** [open](https://github.com/wuhy68/ChatEDA) — 公开 agent、benchmark 与工具调用数据。
- **数据集/数据来源：** `open` — ChatEDA-Bench
- **应用场景：** 自然语言分解任务、生成脚本并执行 OpenROAD APIs，从 RTL 到 GDSII。
- **解决问题：** `reported` — 把 LLM 变为可执行、可反馈、可调参的 EDA agent。
- **最终测试：** `reported` — AutoMage2 Grade A 82%，对比 GPT-4 62%、Claude2 46%、GPT-3.5 28%。 指标：Grade A/B/C, executable script rate。
- **Baselines：** `named` — GPT-4, Claude2, GPT-3.5, AutoMage
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### CircuitNet 2.0: An Advanced Dataset for Promoting Machine Learning Innovations in Realistic Chip Design Environment

- **元数据：** 2024 · ICLR 2024 · Xun Jiang, Zhuomin Chai, Yuxiang Zhao, Yibo Lin, Runsheng Wang, Ru Huang · [paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/464917b6103e074e1f9df7a2bf3bf6ba-Abstract-Conference.html)
- **范围/主题：** `related-eda` · `benchmarks-tools`, `routing`, `si-pi-emc`, `thermal-reliability`, `ai-eda`
- **代码：** [open](https://github.com/circuitnet/CircuitNet) — 官方仓库公开数据与任务入口。
- **数据集/数据来源：** `open_with_upstream_terms` — CircuitNet 2.0
- **应用场景：** 真实 chip design environment 的多任务 ML benchmark。
- **解决问题：** `reported` — 用统一 realistic dataset 支持拥塞、时序、功耗等预测/优化研究。
- **最终测试：** `benchmark` — 按任务提供多种基线和评测；此卡不复述全部表格。 指标：congestion metrics, timing metrics, power metrics。
- **Baselines：** `task_specific` — 各任务 baseline 见官方 benchmark；非单一比较集。
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### RoutePlacer: An End-to-End Routability-Aware Placer with Graph Neural Network

- **元数据：** 2024 · KDD 2024 · Yunbo Hou, Haoran Ye, Yingxue Zhang, Siyuan Xu, Guojie Song · [paper](https://doi.org/10.1145/3637528.3671895)
- **范围/主题：** `related-eda` · `placement`, `routing`, `ai-eda`
- **代码：** [open](https://github.com/sorarain/RoutePlacer) — 公开 RouteGNN/RoutePlacer 实现。
- **数据集/数据来源：** `public_benchmarks` — DAC2012, ISPD2011
- **应用场景：** 把 GNN 预测的 congestion 作为 differentiable placement penalty。
- **解决问题：** `reported` — 端到端优化布局，而不是完成布局后才发现路由溢出。
- **最终测试：** `reported` — matched wirelength 下最高减少 16% overflow；插入 two-stage placers 时减少 44%。 指标：Total Overflow, routed wirelength。
- **Baselines：** `named` — DREAMPlace, NCTUgr, two-stage placers
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### RTLFixer: Automatically Fixing RTL Syntax Errors with Large Language Models

- **元数据：** 2024 · DAC 2024 · Yun-Da Tsai, Mingjie Liu, Haoxing Ren · [paper](https://doi.org/10.1145/3649329.3657353)
- **范围/主题：** `related-eda` · `testing-inspection`, `ai-eda`, `benchmarks-tools`
- **代码：** [open](https://github.com/NVlabs/RTLFixer) — 公开 RAG/ReAct repair agent。
- **数据集/数据来源：** `public_benchmarks` — VerilogEval-Syntax, VerilogEval-Simulate
- **应用场景：** 利用 compiler feedback 迭代修复生成的 Verilog；可类比 DRC/ERC 反馈修复 PCB scripts。
- **解决问题：** `reported` — 通过检索和工具执行闭环降低 LLM 生成 RTL 的语法错误。
- **最终测试：** `reported` — 约 98.5% compilation-error correction；两个 VerilogEval split 的 pass@1 分别提高 32.3 与 10.1 percentage points。 指标：correction rate, pass@1。
- **Baselines：** `named` — baseline prompting, VerilogEval baselines
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### ChiPFormer: Transferable Chip Placement via Offline Decision Transformer

- **元数据：** 2023 · ICML 2023 · Yao Lai, Jinxin Liu, Zhentao Tang, Bin Wang, Jianye Hao, Ping Luo · [paper](https://proceedings.mlr.press/v202/lai23c.html)
- **范围/主题：** `related-eda` · `placement`, `ai-eda`, `benchmarks-tools`
- **代码：** [open](https://github.com/laiyao1/chipformer) — 公开代码、offline trajectories 和 deliverables。
- **数据集/数据来源：** `partial_open` — 32 circuits, 12 circuits x 500 expert placements
- **应用场景：** 从固定 expert trajectories 学习可迁移的 offline placement policy。
- **解决问题：** `reported` — 减少新 design 上昂贵的在线模拟与 RL 交互。
- **最终测试：** `reported` — PMLR 记录报告更好的 placement quality 和约 10x runtime reduction。 指标：HPWL, runtime, overlap, congestion。
- **Baselines：** `named` — AlphaChip, MaskPlace, DeepPR, PRNet
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### Circuit as Set of Points

- **元数据：** 2023 · NeurIPS 2023 · Jialv Zou, Xinggang Wang, Jiahao Guo, Wenyu Liu, Qian Zhang, Chang Huang · [paper](https://papers.neurips.cc/paper_files/paper/2023/file/6697bb267dc517379bc8aa326e844f8d-Paper-Conference.pdf)
- **范围/主题：** `related-eda` · `routing`, `ai-eda`
- **代码：** [open](https://github.com/hustvl/circuitformer) — 公开 CircuitFormer 代码与预训练模型。
- **数据集/数据来源：** `public_benchmarks` — CircuitNet, ISPD2015
- **应用场景：** 把电路元件表示为 raw point sets，预测 congestion 与 DRC violations。
- **解决问题：** `reported` — 避免手工 rasterization/graph preprocessing 丢失几何和连接信息。
- **最终测试：** `reported` — 相对 CNN/GNN/painting baselines 在 CircuitNet 与 ISPD2015 平均改善约 3.8%/1.5%。 指标：Pearson, Spearman, Kendall, DRC metrics。
- **Baselines：** `reported` — CNN baselines, GNN baselines, painting-based baselines
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### The Policy-gradient Placement and Generative Routing Neural Networks for Chip Design

- **元数据：** 2022 · NeurIPS 2022 · Ruoyu Cheng, Xianglong Lyu, Yang Li, Junjie Ye, Jianye Hao, Junchi Yan · [paper](https://proceedings.neurips.cc/paper_files/paper/2022/hash/a8b8c1ad51df1b93d9e3d1fca75debbf-Abstract-Conference.html)
- **范围/主题：** `related-eda` · `placement`, `routing`, `ai-eda`
- **代码：** [open](https://github.com/Thinklab-SJTU/EDA-AI) — EDA-AI 仓库公开相关实现，复现依赖需单独准备。
- **数据集/数据来源：** `public_benchmarks` — ISPD2005, ISPD2007, ISPD1998, Route-small, Route-large
- **应用场景：** PPO mixed-size placement 加 conditional generative global routing。
- **解决问题：** `reported` — 联合学习 placement 和 route generation，减少串行优化带来的目标错配。
- **最终测试：** `reported` — 评估布局、global routing quality 与 concurrent variant 3.36–7.98x speedup。 指标：HPWL, overlap, wirelength, routing congestion, runtime。
- **Baselines：** `named` — DeepPlace, CVAE, cGAN, U-Net, ResNet, NTHU-Route2.0, BoxRouter2.0, FastRoute3.0
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### A Graph Placement Methodology for Fast Chip Design

- **元数据：** 2021 · Nature · Azalia Mirhoseini, Anna Goldie, Mustafa Yazgan, Joe Wenjie Jiang, Jeff Dean · [paper](https://doi.org/10.1038/s41586-021-03544-w)
- **范围/主题：** `related-eda` · `placement`, `ai-eda`
- **代码：** [partial_open](https://github.com/google-research/circuit_training) — 公开训练框架；TPU cases 与训练数据仍是专有。
- **数据集/数据来源：** `mixed_public_private` — Ariane RISC-V, TPU blocks
- **应用场景：** 图状态强化学习 sequential macro floorplanning，后接商业 EDA 完成标准单元。
- **解决问题：** `reported` — 用 GCN policy 和工具反馈自动生成 macro placement。
- **最终测试：** `reported` — 评估代理线长/拥塞与最终 PPA。 指标：wirelength, congestion, density, PPA。
- **Baselines：** `named` — RePlAce, commercial flow, human layouts
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### AutoCkt: Deep Reinforcement Learning of Analog Circuit Designs

- **元数据：** 2020 · DATE 2020 · Keertana Settaluri, Ameer Haj-Ali, Qijing Huang, Kourosh Hakhamaneshi, Borivoje Nikolic · [paper](https://doi.org/10.23919/date48585.2020.9116200)
- **范围/主题：** `related-eda` · `schematic-design`, `ai-eda`
- **代码：** [open](https://github.com/ksettaluri6/AutoCkt) — 公开 analog circuit RL optimization code。
- **数据集/数据来源：** `simulation_flow` — Berkeley Analog Generator, op-amp topologies
- **应用场景：** analog schematic/post-layout sizing；作为 PCB BOM/参数优化的可迁移参考。
- **解决问题：** `reported` — 在稀疏采样下满足多项模拟电路规格，并纳入 parasitic-aware simulation。
- **最终测试：** `reported` — 至少 96.3% schematic goals、约 40x 比 GA 快，并在 68 小时生成 40 个 LVS-passed op-amps。 指标：goal satisfaction, runtime, LVS pass。
- **Baselines：** `named` — genetic algorithm, prior parasitic-aware method
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### DREAMPlace: Deep Learning Toolkit-Enabled GPU Acceleration for Modern VLSI Placement

- **元数据：** 2019 · DAC 2019 · Yibo Lin, Shounak Dhar, Wuxi Li, Haoxing Ren, Brucek Khailany, David Z. Pan · [paper](https://doi.org/10.1145/3316781.3317803)
- **范围/主题：** `related-eda` · `placement`, `benchmarks-tools`, `ai-eda`
- **代码：** [open](https://github.com/limbo018/DREAMPlace) — 公开 PyTorch/CUDA placement toolkit。
- **数据集/数据来源：** `public_and_industrial` — ISPD2005, ISPD2015
- **应用场景：** GPU-accelerated differentiable IC placement；作为大规模 PCB 并行优化内核参考。
- **解决问题：** `reported` — 把 wirelength/density objectives 映射到深度学习框架的自动微分与 GPU kernels。
- **最终测试：** `reported` — 官方页面报告相对 RePlAce 约 40x global-placement speedup，质量不下降。 指标：runtime, placement quality。
- **Baselines：** `named` — RePlAce, NTUPlace3
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### RePlAce: Advancing Solution Quality and Routability Validation in Global Placement

- **元数据：** 2019 · IEEE TCAD · Chung-Kuan Cheng, Andrew B. Kahng, Ilgweon Kang, Lutong Wang · [paper](https://doi.org/10.1109/tcad.2018.2859220)
- **范围/主题：** `related-eda` · `placement`, `routing`, `benchmarks-tools`
- **代码：** [open_archived](https://github.com/The-OpenROAD-Project/RePlAce) — BSD-3-Clause 归档仓库，功能已并入 OpenROAD。
- **数据集/数据来源：** `public_benchmarks` — ISPD2005, ISPD2006, MMS, DAC2012, ICCAD2012
- **应用场景：** 带 routing feedback 的 IC mixed-size global placement；可迁移到 PCB routability-aware placement。
- **解决问题：** `reported` — 用局部 density smoothing、动态步长和路由反馈提高合法性与可布通性。
- **最终测试：** `reported` — 在 ISPD/MMS/contest suites 上评估线长、拥塞和 CPU。 指标：HPWL, scaled HPWL, routing congestion, runtime。
- **Baselines：** `named` — Polar 2.0, NTUplace4h, Ripple 2.0, contest-best
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### Toward an Open-Source Digital Flow: First Learnings from the OpenROAD Project

- **元数据：** 2019 · DAC 2019 · Tutu Ajayi, Vidya A. Chhabria, Andrew B. Kahng, Sachin S. Sapatnekar, Lutong Wang · [paper](https://doi.org/10.1145/3316781.3326334)
- **范围/主题：** `related-eda` · `benchmarks-tools`, `placement`, `routing`
- **代码：** [open](https://github.com/The-OpenROAD-Project/OpenROAD) — 活跃的开放 RTL-to-GDS flow。
- **数据集/数据来源：** `tool_flow` — OpenROAD flow
- **应用场景：** 自动完成 synthesis、floorplanning、placement、CTS、routing 与 signoff。
- **解决问题：** `reported` — 提供可复现的全流程工具执行与集成框架。
- **最终测试：** `system_report` — 论文重点是 flow integration 与 tapeout lessons，不是单一 ML benchmark。 指标：flow completion, tapeout evidence。
- **Baselines：** `not_applicable` — 系统/经验论文，无统一算法 baseline。
- **证据边界：** `project-page`；核验日期 2026-08-11。未报告不等于不存在。

### RouteNet: Routability Prediction for Mixed-Size Designs Using Convolutional Neural Network

- **元数据：** 2018 · ICCAD 2018 · Zhiyao Xie, Yu-Hung Huang, Guan-Qi Fang, Haoxing Ren, Shao-Yun Fang, Yiran Chen, Jiang Hu · [paper](https://doi.org/10.1145/3240765.3240843)
- **范围/主题：** `related-eda` · `placement`, `routing`, `ai-eda`
- **代码：** not_found — 未找到官方仓库。
- **数据集/数据来源：** `generated_from_public` — ISPD2015
- **应用场景：** global routing 前预测总 DRV 和 DRC hotspots。
- **解决问题：** `reported` — 用快速 CNN oracle 代替高成本 trial routing。
- **最终测试：** `reported` — 报告 hotspot accuracy 相对 global routing 提升约 50%，推理少于 1 秒。 指标：DRV accuracy, top-10 rank, TPR, FPR, inference time。
- **Baselines：** `named` — SVM, logistic regression, trial routing, global routing
- **证据边界：** `full-text`；核验日期 2026-08-11。未报告不等于不存在。

### ePlace: Electrostatics Based Placement Using Nesterov's Method

- **元数据：** 2014 · DAC 2014 · Jingwei Lu, Pengwen Chen, Chin-Chih Chang, Lu Sha, Dennis J.-H. Huang, Chung-Kuan Cheng · [paper](https://doi.org/10.1145/2593069.2593133)
- **范围/主题：** `related-eda` · `placement`
- **代码：** not_found — 未找到维护中的官方仓库。
- **数据集/数据来源：** `public_benchmarks` — ISPD2005, ISPD2006, MMS
- **应用场景：** IC mixed-size global placement；作为 PCB 连续优化与密度建模参考。
- **解决问题：** `reported` — 以 electrostatic density 和 Nesterov optimization 联合最小化线长与重叠。
- **最终测试：** `reported` — 在三个 benchmark families 上报告 2.83%–7.13% 线长改善和 1.05x–3.05x speedup。 指标：HPWL, runtime。
- **Baselines：** `named` — BonnPlace, MAPLE, NTUplace3-unified
- **证据边界：** `full-text`；核验日期 2026-08-11。未报告不等于不存在。
