# PROJECT.md

> 项目事实与决策的主索引。最后更新：2026-06-27。

## 项目真正的研究目标

本项目不是“在 PyCIL 中再加入一个模块”，而是要完成一项可投稿、可证伪、可复现的无样例类增量学习（Exemplar-Free Class-Incremental Learning, EFCIL）研究。

经过代码、论文和 PI 审稿式审计，当前目标不再绑定某个算法方向，而是：

> 识别 EFCIL 领域被广泛依赖、但缺少系统验证的核心假设；先用可证伪诊断确定真正限制性能和结论可信度的因素，再决定是否存在足够强的论文主线。

当前首先回答：

1. 单 prototype 是否真的足以代表旧类？
2. 当前任务数据是否真的能代理旧任务函数？
3. 现有结果有多少由第一任务表示覆盖和类顺序决定？
4. pseudo-feature 是否位于真实旧类流形，而不仅是能用于正则化分类器？
5. 平均准确率、forgetting、存储和隐私口径是否支持现有论文结论？

IDEA-001“可观测性驱动的漂移补偿”已被 PI 审计评为 `Weak Reject`，保持暂缓，不再作为默认主线。

## 当前阶段

- 阶段：可信实验底座建设已完成第一阶段。完成 20 项领域隐含假设审计，并在 2026-06-27 严格筛选为 2 个活跃候选；A05/A03 诊断协议已修订为 v1.1，并完成 PyCIL baseline 覆盖映射；`experiment_base/` 已通过最小 smoke test。尚未选定论文主线，禁止方法编码。
- 代码基线：`PyCIL/`，当前没有项目自研算法实现。
- 实验底座：`experiment_base/`，独立于 PyCIL，复用 PyCIL 可用的数据统计和类顺序思想，不搬运旧训练器或硬编码 `.cuda()` 路径。
- 默认分支：`main`
- 远端仓库：`holyer05/CIL`
- 服务器工作区：`/root/autodl-tmp/CIL`
- 公共数据目录：`/root/autodl-pub`
- 算力：单卡 NVIDIA GeForce RTX 3080 Ti，12 GB 显存。
- 当前结果：尚无本项目正式模型实验结果；已有 `BASE-001` 基础设施 smoke 结果，manifest 为 `experiment_base/runs/20260627T051735Z_smoke_cifar100_loader_repro_manifest/manifest.json`。

## 当前代码库实现了什么

代码库是通用 PyCIL 工具箱快照，提供统一的类顺序、任务划分、训练循环、CNN/NME 评价、遗忘计算、样例内存管理和多种网络头。

新增 `experiment_base/` 是本项目可信实验底座，不直接修改 PyCIL。当前已实现：

- `requirements.txt` 与 `requirements.lock`：锁定 `scipy==1.11.4`、`scikit-learn==1.3.2`、`POT==0.9.5`、`quadprog==0.1.12` 等核心依赖。
- `configs/smoke_cifar100.json` 与 `configs/datasets.example.json`：CIFAR-100 使用公共归档和项目内可写缓存；ImageNet100 通过显式配置路径声明，不在 Python 中写死服务器路径。
- `core/repro.py`：配置 seed 控制 Python、NumPy、PyTorch、CUDA 和 class order；统一单 GPU device 解析。
- `core/env.py` 与 `core/manifest.py`：记录 Git commit、dirty 状态、环境、CUDA/GPU、配置快照、类顺序、指标容器、运行时间和显存。
- `run_smoke.py`：完成 CIFAR-100 loader/repro/manifest 最小 smoke test。

### 通用训练基础设施

- `main.py`：读取 JSON 配置并启动训练。
- `trainer.py`：按任务顺序训练、评估 CNN/NME、记录平均准确率与 forgetting。
- `utils/data_manager.py`：类顺序重映射、任务切分、训练/测试数据集构造和 replay append。
- `models/base.py`：统一 learner 接口、NME、prototype/class mean、herding exemplar memory。
- `utils/inc_net.py`：普通、余弦、动态扩展、MEMO、ACIL/DS-AL、TagFex 等网络封装。
- `convs/`：CIFAR/ImageNet ResNet、cosine ResNet、CBAM、adapter ResNet、MEMO 子网络和解析随机缓冲层。

### 已实现方法

| 类别 | 方法 |
|---|---|
| 朴素/正则化 | FineTune、LwF、EWC |
| 样例回放 | Replay、GEM、iCaRL、BiC、WA、PODNet、Coil、RMM |
| 动态结构/压缩 | DER、FOSTER、MEMO、BEEF |
| 无样例或可配置为无样例 | LwF、PASS、IL2A、SSRE、FeTrIL、SimpleCIL、ACIL、DS-AL |
| 预训练/扩展路线 | Aper、TagFex |

### 与本项目文献的对应关系

已在代码中出现：LwF、PASS、IL2A、SSRE、FeTrIL。

本地论文中但当前代码未实现：SDC、EFC、LDC、ADC、IR、PRL、APR。近期重要工作 AdaGauss、DCNet、Muheal 等也未实现。

因此，当前仓库是“基线工具箱”，不是“已完成的研究项目”。

## 当前复现准备度

### 已有资源

- `/root/autodl-pub/cifar-100`
- `/root/autodl-pub/cifar-10`
- `/root/autodl-pub/ImageNet100`
- `/root/autodl-pub/ImageNet-mini`
- `/root/autodl-pub/CUB200-2011`

### 已完成的基础设施修复

1. 当前环境为 Python 3.10.8、PyTorch 2.1.2+cu118、torchvision 0.16.2+cu118；已安装并锁定 `scipy==1.11.4`、`scikit-learn==1.3.2`、`POT==0.9.5`、`quadprog==0.1.12`。
2. `experiment_base/` 已支持 CIFAR-100 公共归档读取与项目内可写缓存抽取；ImageNet100 路径由配置显式声明。
3. `experiment_base/` 已实现配置 seed 到 Python、NumPy、PyTorch、CUDA 和 class order 的统一控制。
4. `experiment_base/` 已实现结构化 manifest，记录 commit、配置、环境、类顺序、指标容器、运行时间和显存。
5. `BASE-001` smoke test 已在 clean commit `fb1c38d` 通过：CIFAR-100 train=50000、test=10000、classes=100；same seed 可复现，different seed 改变类顺序。

### 仍存在的阻塞与风险

1. PyCIL 原始 `utils/data.py` 的 ImageNet 路径仍是 `[DATA-PATH]` 占位符；底座已经避免写死路径，但 PyCIL legacy 代码尚未全面迁移。
2. PyCIL 原始 `trainer.py` 将随机种子固定为 1，没有实际使用配置中的 seed；底座已修复，但 legacy trainer 未改。
3. 多个旧方法把超参数硬编码在 Python 文件中，JSON 不能完整控制实验。
4. PyCIL 部分代码直接调用 `.cuda()`，设备选择不完全统一；底座路径已避免硬编码 `.cuda()`。
5. 多个 PyCIL 配置默认 4 GPU，但当前服务器只有 1 GPU。
6. v1.1 所需 oracle split、A05 medoid/2-center、A03 continuous retention、feature/logit dump 和 semantic class order 尚未实现。
7. README 的历史依赖版本与当前运行环境差异很大，尚未验证完整 PyCIL 训练兼容性。

这些问题意味着：当前不应直接开始新方法编码，必须先建立可信 baseline。

## 本地论文覆盖方向

| 论文 | 核心方向 | 主要局限/开放点 |
|---|---|---|
| Learning without Forgetting | 用新任务图像上的旧模型输出做知识蒸馏 | 新旧分布差异大时，当前数据不能代表旧任务 |
| Semantic Drift Compensation | 用当前类样本的局部漂移插值旧类 prototype 漂移 | 假设局部平移；远离当前数据的旧类估计不可靠 |
| Elastic Feature Consolidation | EFM 选择性约束重要特征方向，配合非对称 prototype replay | prototype/covariance 漂移与线性存储增长仍未解决 |
| Resurrecting Old Classes / ADC | 将新图像对抗扰动到旧 prototype 附近，再估计漂移 | 后期估计质量下降；依赖任务边界与足量当前数据 |
| Learnable Drift Compensation | 用当前数据学习旧特征空间到新空间的 projector | 当前数据偏置导致部分旧类错误映射，缺少可靠性判断 |
| Incremental Representation | 数据增强扩大表示空间，L2 维护空间，1-NN 分类 | 强各向同性约束；对复杂冷启动漂移的解释有限 |
| Prospective Representation Learning | 基础阶段预留空间，增量阶段用旧 prototype 引导新类远离 | 未知未来类数量和分布，预留空间如何分配仍开放 |
| Adversarial Pseudo-Replay | 在线对抗伪回放稳定特征，并迁移均值/协方差 | 训练成本高；仍依赖 prototype/covariance 与任务边界 |

## 研究边界

- 不保存旧类训练样本作为回放数据。
- prototype、covariance、projector、旧模型、索引和增强参数均必须计入内存预算。
- 不破坏 PyCIL baseline；新增能力必须可通过配置关闭。
- 不以堆叠 Loss、Attention、Adapter 或生成器作为创新本身。
- 每项实现必须对应一个可证伪的研究假设。
- 允许在“诊断实验”中用旧数据计算 oracle 漂移，但旧数据不得参与方法训练或调参。
- 论文主张只能来自已记录、可复现的实验。
- 当前只允许设计诊断协议，不提出新 Loss、新模块或新网络。
- IDEA-001 保持暂缓，不继续包装或优化。

## 当前研究路线

### 假设优先，而不是方法优先

`IDEA_POOL.md` 已记录 20 个跨论文、跨方法的隐含假设。结合 2024--2026 近期 cold-start EFCIL 工作后，当前只保留两个活跃研究候选：

1. `A05`：单 prototype 是否真的是旧类充分表示；
2. `A03`：当前任务数据是否能代理旧任务函数。

选择理由：

- 两者覆盖的论文和已实现方法最广，不依赖某个特定 drift estimator。
- 可以通过 oracle 诊断、冻结评测和分布检验直接证伪，不需要先发明算法。
- 一旦被证伪，会改变对现有方法增益、benchmark 公平性和论文贡献的解释。

`A01` 从主线降级为 cold-start 协议控制变量：近期 EFC、EFC++、ADC、LDC、APR、CIRCLE 等工作已经显式关注 small first task / cold start，因此只证明第一任务覆盖影响性能的新颖性不足。后续所有实验仍必须分层记录 first-task coverage、first-task 类组成和未来类别 frozen probe。

`A07` 从主线降级为 A05 的支撑性诊断：若单 prototype 不充分，再检查 pseudo-feature 是真实旧类流形近似，还是只起分类器正则化作用。

当前已固化 A05 与 A03 的诊断变量、oracle 指标、失败条件和最小实验矩阵，并完成协议 v1.1 修订与 baseline 覆盖映射。v1.1 明确 oracle-fit / oracle-eval / final-audit、A05 primary comparator、sample-budget/capacity matched 对照、A03 continuous retention 主指标、指标族预注册和 Sanity/Screen/Paper gate 三阶段矩阵。`experiment_base/` 已完成 ENV/DATA/REPRO/LOG/BASE-001 的最小可信底座。下一阶段应进入 Sanity 阶段计划和 v1.1 诊断指标落地缺口清单；在完成这些前，不进入新方法设计或完整实验。如果 A05/A03 后续均未被证伪，再回到其余假设重新排序。

baseline 覆盖映射后的执行边界：

- SimpleCIL 是 A05 Sanity 的首选轨迹来源；LwF 是 A03 Sanity 的首选轨迹来源。
- 现有 PyCIL 不能直接产出 v1.1 所需 oracle split、A05 medoid/2-center、A03 continuous retention 和指标族预注册结果。
- CUB-200、ImageNet-100、semantic class order、完整 seed 控制和 structured logging 都不是当前代码可直接支持的能力。
- A03 在当前 baseline 覆盖下只能支撑 narrow LwF/new-data distillation claim，不能支撑 broad current-data proxy claim。

## 关键决策

| 日期 | 决策 | 原因 | 状态 |
|---|---|---|---|
| 2026-06-25 | 使用根目录作为唯一 Git 仓库 | 统一管理代码、实验记录与论文材料 | 已执行 |
| 2026-06-25 | 第三方论文 PDF、数据集、权重和训练产物不进入 Git | 控制版权、容量和凭据风险 | 已执行 |
| 2026-06-25 | 每次有效修改后提交并推送 `main` | 保证可追溯和可回滚 | 已执行 |
| 2026-06-25 | 使用五个 workspace Markdown 维护研究状态 | 防止代码、实验与论文叙事脱节 | 已执行 |
| 2026-06-25 | 主研究问题曾收敛为漂移可观测性与保守补偿 | 初次研究审计后的候选方向 | 已被后续 PI 审计降级 |
| 2026-06-25 | IDEA-001 评为 Weak Reject 并暂缓 | 核心等价关系脆弱，且与现有工作重叠风险高 | 已执行 |
| 2026-06-25 | 进入 Assumption Mining Mode | 避免在未经验证的领域前提上继续设计方法 | 进行中 |
| 2026-06-25 | 优先诊断 A01、A05、A07 | 覆盖面广、可直接证伪、论文解释力强 | 待实验 |
| 2026-06-25 | 暂不编码新算法 | 当前 baseline、环境和评测协议尚不可信 | 已执行 |
| 2026-06-27 | 严格筛选后仅保留 A05、A03 为活跃研究候选 | A01 已被近期 cold-start 工作覆盖为常识性问题；A07 与 A05/A06 耦合且成本较高 | 已执行 |
| 2026-06-27 | 固化 A05/A03 诊断协议 v1 | 先定义变量、oracle 指标、失败条件和最小实验矩阵，避免直接滑向方法设计 | 已执行 |
| 2026-06-27 | A05/A03 协议反向审稿结论为 Revise before experiments | v1 阈值偏启发式，oracle split 不足，A03 轨迹覆盖偏窄，矩阵需分阶段 | 已执行 |
| 2026-06-27 | 修订 A05/A03 诊断协议为 v1.1 | 补齐 oracle split、A05 主比较器、预算匹配、A03 连续 retention、指标预注册和三阶段矩阵 | 已执行 |
| 2026-06-27 | 完成 PyCIL baseline 覆盖映射 | 明确 SimpleCIL/LwF 可作 Sanity 轨迹，但 v1.1 指标与 Screen 阶段仍需实验底座建设 | 已执行 |
| 2026-06-27 | 新建 `experiment_base/` 作为可信实验底座 | 保持 PyCIL 原始代码不动；只搬运可用思想和必要配置，先解决环境、数据路径、复现、manifest 和 smoke 验证 | 已执行 |

## 文档职责

- `PROJECT.md`：稳定事实、范围、阶段和关键决策。
- `IDEA_POOL.md`：研究假设、理论动机、风险与去留。
- `EXPERIMENT_LOG.md`：实验与研究审计事实，按时间追加，不覆盖失败记录。
- `TODO.md`：下一步可执行任务及验收条件。
- `PAPER_OUTLINE.md`：论文叙事、主张与证据映射。

## 更新规则

发生以下变化时必须更新本文件：目标、范围、阶段、基线、资源、协议或关键技术决策发生变化。实验数值写入 `EXPERIMENT_LOG.md`。
