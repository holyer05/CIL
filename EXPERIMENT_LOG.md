# EXPERIMENT_LOG.md

> 实验与研究审计事实日志。只追加或更正有证据的错误，不删除失败记录。最后更新：2026-06-27。

## 记录规范

每个正式实验必须记录：

- 唯一实验 ID；
- 日期、Git commit 和代码工作区是否干净；
- 方法、配置文件、数据集、任务划分和随机种子；
- 环境、启动命令、日志与产物路径；
- 主要指标、运行状态和结论；
- 失败也必须记录直接错误和下一步处理。

实验结果必须来自真实日志或结果文件，不得凭终端片段或记忆补写。研究审计条目必须区分“代码事实”“论文结论”和“推断”。

## 实验与审计索引

| ID | 日期 | Commit | 方法/目的 | 数据集与协议 | Seed | 状态 | 关键结果 |
|---|---|---|---|---|---:|---|---|
| SETUP-001 | 2026-06-25 | `909b5d0` | 初始化 GitHub 版本管理 | 不适用 | - | 完成 | 尚未运行模型实验 |
| SETUP-002 | 2026-06-25 | `e112fd0` | 初始化持续维护的科研 workspace 文档 | 不适用 | - | 完成 | 建立五份状态文档 |
| RESEARCH-001 | 2026-06-25 | `26887c0` | 全项目代码、论文与研究路线审计 | 不适用 | - | 完成 | 未修改 Python；主问题收敛为漂移可观测性 |
| RESEARCH-002 | 2026-06-25 | `5974a56` | EFCIL 隐含假设挖掘 | 不适用 | - | 完成 | 记录 20 项假设；优先 A01、A05、A07 |
| RESEARCH-003 | 2026-06-27 | `6021b01` | 近期 cold-start EFCIL 文献补充与假设严格筛选 | 不适用 | - | 完成 | 只保留 A05、A03；A01 降级为控制变量；A07 降级为支撑诊断 |
| RESEARCH-004 | 2026-06-27 | `440cd1f` | 固化 A05/A03 诊断协议 | 不适用 | - | 完成 | 明确变量、oracle 指标、失败条件和最小实验矩阵；未写代码 |
| RESEARCH-005 | 2026-06-27 | `e4cf3e6` | PI 级反向审稿 A05/A03 诊断协议 | 不适用 | - | 完成 | 结论 Revise before experiments；指出阈值、oracle split、矩阵和替代解释问题 |
| RESEARCH-006 | 2026-06-27 | `c927e4a` | 修订 A05/A03 诊断协议 v1.1 | 不适用 | - | 完成 | 补齐 oracle split、A05 主比较器、预算匹配、A03 连续 retention、指标预注册、三阶段矩阵 |
| RESEARCH-007 | 2026-06-27 | `0f1af06` | PyCIL baseline 覆盖映射 | 不适用 | - | 完成 | SimpleCIL/LwF 可作 Sanity 轨迹；v1.1 指标和 Screen 阶段不能直接支持 |
| SETUP-003 | 2026-06-27 | `5e2fb4f` | 建立可信实验底座 `experiment_base/` | CIFAR-100 loader smoke 准备 | 1993 | 完成 | 锁定依赖、配置数据路径、seed/device/manifest 基础能力；未修改 PyCIL |
| SETUP-004 | 2026-06-27 | `d516d08`/`fb1c38d` | 完善 smoke manifest 与 GPU 显存记录 | CIFAR-100 loader smoke | 1993 | 完成 | manifest 增加运行时间、metrics、GPU memory；首次 GPU reset 失败后已修复 |
| BASE-001 | 2026-06-27 | `fb1c38d` | 最小 smoke test | CIFAR-100；loader/repro/manifest | 1993 | 完成 | manifest 绑定 clean commit；train=50000、test=10000、classes=100；same seed True、different seed True |

## 详细记录

### SETUP-001：项目版本管理与研究日志初始化

- 日期：2026-06-25
- Commit：`909b5d0c973126be5cc818d8bd85e3d07c3eb2aa`
- 环境：AutoDL，Ubuntu 22.04，NVIDIA GeForce RTX 3080 Ti
- 操作：建立根 Git 仓库、仓库级 deploy key、自动推送 hook、安全忽略规则和同步脚本。
- 验证：本地与远端 `main` HEAD 一致；工作区干净；未跟踪凭据、论文 PDF、权重或数据集。
- 结果：项目具备基础版本追踪能力。
- 限制：尚未固化训练环境，尚未完成任何 baseline 复现。

### SETUP-002：持续维护的科研 workspace 初始化

- 日期：2026-06-25
- Commit：`e112fd0`
- 操作：创建 `PROJECT.md`、`IDEA_POOL.md`、`EXPERIMENT_LOG.md`、`TODO.md` 和 `PAPER_OUTLINE.md`，并将同步维护要求写入 `AGENTS.md`。
- 验证：五份文件均为有效 UTF-8，必需章节齐全，`git diff --check` 通过。
- 结果：项目目标、想法、实验、任务和论文证据开始分别维护。
- 限制：候选研究方向尚未完成文献新颖性审计或实验验证。

### RESEARCH-001：全项目 Research Mode 审计

- 日期：2026-06-25
- 审计前 Commit：`26887c0dc396720eadc67050d40788da1cdca1d8`
- 工作区：审计开始时 clean。
- 操作范围：
  - 阅读根目录和 workspace 全部 Markdown；
  - 盘点 94 个受版本控制文件；
  - 静态阅读训练入口、数据管理、BaseLearner、网络封装、25 个方法实现和全部 JSON 配置；
  - 全文提取并阅读 8 篇本地论文，共 135 页；
  - 检索 2024-2026 年 EFCIL/NECIL 相关工作。
- 本地论文：LwF、SDC、EFC、ADC、LDC、IR、PRL、APR。
- 代码事实：仓库是 PyCIL baseline 工具箱，没有当前项目自研方法；本地近期论文中的 EFC、LDC、ADC、IR、PRL、APR 未实现。
- 环境事实：Python 3.10.8；PyTorch 2.1.2+cu118；单卡 RTX 3080 Ti；缺失 scipy、scikit-learn、POT、quadprog。
- 数据事实：公共目录存在 CIFAR-10/100、ImageNet100、ImageNet-mini、CUB200-2011。
- 主要复现风险：ImageNet 路径占位、seed 被固定为 1、Python 内硬编码超参数、`.cuda()` 硬编码、多 GPU 配置与单 GPU 环境不符、无结构化结果 manifest。
- 研究结论：最有价值的问题不是再设计无条件漂移映射，而是刻画当前数据对旧类漂移的可观测性并拒绝不可靠补偿。
- 代码修改：无 Python、JSON 或 shell 代码修改；仅计划更新 workspace Markdown。
- 模型实验：未运行。

### RESEARCH-002：EFCIL Assumption Mining

- 日期：2026-06-25
- 审计前 Commit：`5974a56de01dccce167c9a8fd3ea106b9e74c40f`
- 工作区：存在用户自己的 `AGENTS.md` 未提交改动；本轮不修改、不暂存、不覆盖。
- 操作范围：
  - 重新核对 8 篇本地论文全文提取结果；
  - 检查 PyCIL 的 task loop、class order、NME、prototype、memory 和 forgetting 实现；
  - 复核 LwF、PASS、IL2A、SSRE、FeTrIL、SimpleCIL、ACIL、DS-AL 等已实现 EFCIL 路线；
  - 将 SDC、EFC、ADC、LDC、IR、PRL、APR 及近期 AdaGauss、BiCyc 等未实现路线纳入假设映射。
- 研究产物：`IDEA_POOL.md` 中记录 20 项隐含假设，每项包含依赖方法、失效原因、预期现象、诊断实验和论文主线潜力。
- 优先假设：
  1. `A01` 第一任务表示覆盖是否决定大部分 EFCIL 上限；
  2. `A05` 单 prototype 是否足以代表旧类；
  3. `A07` pseudo-feature 是否“统计正确但流形错误”。
- 关键决策：
  - IDEA-001 保持 `Weak Reject/暂缓`，本轮没有继续优化；
  - 没有提出新 Loss、新模块或新网络；
  - 下一阶段只能固化诊断协议，不能进入方法开发。
- 代码修改：无 Python、JSON、shell 或配置代码修改；仅更新 workspace Markdown。
- 模型实验：未运行；本条是研究审计，不包含实验结论。

### RESEARCH-003：近期 cold-start 文献补充与假设严格筛选

- 日期：2026-06-27
- 操作范围：
  - 使用公开论文页面补充核查 2024--2026 年 EFCIL / cold-start 相关工作；
  - 重点复核 EFC、EFC++、ADC、LDC、AdaGauss、APR、BiCyc、CIRCLE 对 first-task coverage、drift compensation、prototype/covariance、pseudo-replay 和 long-horizon cold-start 的覆盖；
  - 对 A01--A20 按新颖性、可证伪性、实验成本、与现有工作的区分度、发展成方法的潜力五项评分。
- 主要事实：
  - 近期 EFC/EFC++、ADC、LDC、APR、CIRCLE 等工作已经显式讨论 cold start、small first task 或 first-task-biased backbone，因此 A01 作为独立主线的新颖性不足；
  - prototype、Gaussian/covariance、pseudo-feature 和 current-data proxy 仍是多条路线共同依赖但未充分证伪的基础。
- 筛选结果：
  - 活跃研究候选：`A05` 单 prototype 是否足以代表旧类；`A03` 当前任务数据是否能代理旧任务函数；
  - `A01` 降级为 cold-start 控制变量；
  - `A07` 降级为 A05 的支撑性诊断。
- 代码修改：无 Python、JSON、shell 或配置代码修改；仅计划更新 workspace Markdown。
- 模型实验：未运行；本条是研究审计，不包含实验结果。

### RESEARCH-004：A05/A03 诊断协议固化

- 日期：2026-06-27
- 操作范围：
  - 为 `A05` 单 prototype 充分性定义共同控制变量、自变量、oracle 对照、主指标、支持条件、拒绝条件和无效证据；
  - 为 `A03` 当前任务数据代理旧任务函数定义当前数据可观测指标、隐藏 oracle 指标、预测性判据、分层解释、支持条件和拒绝条件；
  - 固化筛选矩阵与论文门矩阵；
  - 更新 `PROJECT.md`、`IDEA_POOL.md`、`TODO.md` 和 `PAPER_OUTLINE.md` 的阶段状态。
- 关键约束：
  - 不提出新 Loss、新模块、新网络或新训练方法；
  - hidden old data 只允许作为 oracle evaluation，不允许参与训练、调参、阈值选择或方法设计；
  - `A01` 作为 first-task coverage 控制变量，`A07` 作为 A05 支撑诊断。
- 代码修改：无 Python、JSON、shell 或配置代码修改；仅更新 Markdown。
- 模型实验：未运行；本条是协议设计，不包含实验结果。

### RESEARCH-005：A05/A03 诊断协议 PI 级反向审稿

- 日期：2026-06-27
- 审稿对象：`IDEA_POOL.md` 与 `PAPER_OUTLINE.md` 中的 A05/A03 诊断协议 v1。
- 审稿重点：
  - 阈值是否武断；
  - hidden old oracle 是否可能泄露；
  - 最小实验矩阵是否过大或过小；
  - 是否遗漏关键替代解释；
  - A03 的 baseline 轨迹覆盖是否足以支撑 broad claim。
- 结论：`Revise before experiments`。
- 主要问题：
  1. A05/A03 阈值目前是启发式，不能作为最终论文 claim 的唯一依据；
  2. hidden old data 必须拆分为 oracle-fit、oracle-eval 和 final-audit，否则 oracle probe 会泄露；
  3. A05 的 `max(kNN, linear probe, multi-center)` 会造成 winner's curse，只能作为 exploratory upper envelope；
  4. A03 若只覆盖 LwF，主张必须收窄，不能代表所有 current-data proxy 方法；
  5. 实验矩阵应分为 Sanity、Screen、Paper gate 三阶段。
- 代码修改：无 Python、JSON、shell 或配置代码修改；仅更新 Markdown。
- 模型实验：未运行；本条是协议审稿，不包含实验结果。

### RESEARCH-006：A05/A03 诊断协议 v1.1 修订

- 日期：2026-06-27
- 操作范围：
  - 将 hidden old oracle 明确拆分为 `oracle-fit`、`oracle-eval` 和 `final-audit`；
  - 为 A05 明确 primary comparator：mean prototype vs one-center medoid、mean prototype vs 2-center oracle；
  - 为 A05 增加 sample-budget matched 与 capacity-matched / capacity-accounted 对照；
  - 为 A03 明确 primary continuous retention：hidden-old all-seen margin retention；
  - 为 A03 预注册 output consistency、teacher confidence、feature response、support/coverage 和 controls 五类当前数据指标；
  - 将实验矩阵修订为 Sanity、Screen、Paper gate 三阶段。
- 关键约束：
  - 不设计新方法，不写代码；
  - hidden old data 只用于 analysis-only oracle；
  - A03 的 broad claim 必须等待 `BASELINE-SCOPE-001` 后决定。
- 代码修改：无 Python、JSON、shell 或配置代码修改；仅更新 Markdown。
- 模型实验：未运行；本条是协议修订，不包含实验结果。

### RESEARCH-007：BASELINE-SCOPE-001 PyCIL baseline 覆盖映射

- 日期：2026-06-27
- 操作范围：
  - 只读检查 `PyCIL/exps/simplecil.json`、`PyCIL/exps/fetril.json`、`PyCIL/exps/lwf.json`；
  - 只读检查 `PyCIL/models/simplecil.py`、`PyCIL/models/fetril.py`、`PyCIL/models/lwf.py`、`PyCIL/models/base.py`；
  - 只读检查 `PyCIL/trainer.py`、`PyCIL/utils/data_manager.py`、`PyCIL/utils/data.py`、`PyCIL/utils/factory.py`；
  - 核对当前 Python 依赖和 `/root/autodl-pub` 数据目录。
- 代码事实：
  - `simplecil`、`fetril`、`lwf` 已实现并在 factory 注册；
  - baseline 覆盖审计时环境缺失 `scipy`、`sklearn`、`ot`、`quadprog`；后续 `ENV-001` 已补齐并锁定；
  - `models/base.py` 顶层导入 `scipy`，会阻塞当前直接运行；
  - CUB-200 数据目录存在，但 PyCIL 无 CUB dataset class；
  - ImageNet100 数据目录存在，但 `utils/data.py` 中 `iImageNet100.download_data()` 仍 assert；
  - DataManager 不支持显式 semantic class order；
  - 现有日志不保存 v1.1 所需 logits/features/oracle split/continuous retention。
- 覆盖结论：
  - A05 Sanity 首选轨迹：SimpleCIL；
  - A03 Sanity 首选轨迹：LwF；
  - FeTrIL 可作为 Screen 候选，但当前 sklearn 缺失且 config/实现不匹配 v1.1；
  - A03 当前只能支撑 narrow LwF/new-data distillation claim，不能支撑 broad current-data proxy claim；
  - v1.1 正式指标需要后续实验底座建设，不应直接跑训练。
- 代码修改：无 Python、JSON、shell 或配置代码修改；仅更新 Markdown。
- 模型实验：未运行；本条是只读 baseline 映射，不包含实验结果。

### SETUP-003：建立可信实验底座 experiment_base

- 日期：2026-06-27
- Commit：`5e2fb4f5354eae860fbe9158f9bae344d9325c1a`
- 工作区：提交前仅新增 `experiment_base/` 与 `.gitignore` 预期改动；PyCIL 原始代码未修改。
- 目的：在 PyCIL 之外建立可信实验底座，先解决环境、数据路径、复现控制、结构化日志和最小 smoke，不进入方法设计。
- 主要文件：
  - `experiment_base/requirements.txt`
  - `experiment_base/requirements.lock`
  - `experiment_base/configs/smoke_cifar100.json`
  - `experiment_base/configs/datasets.example.json`
  - `experiment_base/core/config.py`
  - `experiment_base/core/data.py`
  - `experiment_base/core/env.py`
  - `experiment_base/core/manifest.py`
  - `experiment_base/core/repro.py`
  - `experiment_base/run_smoke.py`
- 依赖事实：远程新 shell 可导入 `scipy==1.11.4`、`scikit-learn==1.3.2`、`POT==0.9.5`、`quadprog`、`numpy==1.26.4`、`torch==2.1.2+cu118`、`torchvision==0.16.2+cu118`。
- 数据事实：
  - CIFAR-100 公共目录存在只读归档 `/root/autodl-pub/cifar-100/cifar-100-python.tar.gz`；
  - `experiment_base` 使用该公共归档，但抽取到项目内可写缓存 `experiment_base/data/cifar-100`；
  - ImageNet100 通过 `configs/datasets.example.json` 显式配置 `train_dir` 和 `val_dir`，Python 中不写死服务器路径。
- 复现控制：
  - `core/repro.py` 控制 Python、NumPy、PyTorch、CUDA seed；
  - `build_class_order()` 支持配置 seed 下的 deterministic random class order；
  - `resolve_device()` 统一单 GPU device 解析，底座路径不使用硬编码 `.cuda()`。
- 结构化记录：
  - manifest 记录 commit、dirty 状态、配置快照、环境、seed 状态、device、dataset、class order、loader smoke 和 metrics 容器。
- 结果：可信实验底座第一版建立完成。
- 限制：尚未实现 v1.1 oracle split、A05 medoid/2-center、A03 continuous retention、feature/logit dump 或 PyCIL trainer 对接。

### SETUP-004：完善 smoke manifest 与 GPU 显存记录

- 日期：2026-06-27
- Commits：
  - `d516d083e504edd38bed32b833484ca02b0cf1bc`：为 smoke manifest 增加开始/结束时间、运行时间、metrics 容器和 GPU memory 字段；
  - `fb1c38d7db986984e320481878a1989c4aabf311`：修复 CUDA 未初始化时 `torch.cuda.reset_peak_memory_stats()` 崩溃问题。
- 工作区：两次提交前均只修改 `experiment_base/run_smoke.py`。
- 验证：
  - `python -m py_compile $(find experiment_base -name '*.py' -print)` 通过；
  - `git diff --check` 通过；
  - 两次提交均推送到 `main`。
- 失败记录：
  - 在 commit `d516d08` 下运行 smoke 时失败：
    - 命令：`python -m experiment_base.run_smoke --config experiment_base/configs/smoke_cifar100.json`
    - 直接错误：`RuntimeError: Invalid device argument 0: did you call init?`
    - 原因：CUDA 尚未初始化时直接调用 peak memory reset。
  - 处理：`fb1c38d` 将 GPU memory tracking 改为安全封装，先 `set_device/init/reset`，若失败则写入 manifest error 而不阻断 smoke。
- 结果：LOG-001 manifest 的运行时间、metrics 和显存字段可用。

### BASE-001：最小 smoke test

- 日期：2026-06-27
- Commit：`fb1c38d7db986984e320481878a1989c4aabf311`
- 工作区：clean；manifest 中 `dirty=false`。
- 方法与开关：`experiment_base.run_smoke`，只检查 loader、seed/class order、manifest；不训练模型。
- 配置文件：`experiment_base/configs/smoke_cifar100.json`
- 数据集与路径：
  - Dataset：CIFAR-100
  - 公共归档：`/root/autodl-pub/cifar-100/cifar-100-python.tar.gz`
  - 项目缓存：`experiment_base/data/cifar-100`
- 任务协议：基础设施 smoke，不是 CIL 训练协议。
- Seed：`1993`
- 环境：Python 3.10.8；PyTorch 2.1.2+cu118；torchvision 0.16.2+cu118；单卡 NVIDIA GeForce RTX 3080 Ti。
- 启动命令：`python -m experiment_base.run_smoke --config experiment_base/configs/smoke_cifar100.json`
- 产物路径：`experiment_base/runs/20260627T051735Z_smoke_cifar100_loader_repro_manifest/manifest.json`
- 状态：completed
- 指标：
  - CIFAR-100 train size：50000
  - CIFAR-100 test size：10000
  - num classes：100
  - `same_seed_reproducible=True`
  - `different_seed_changes_order=True`
  - `elapsed_seconds=1.37446`
  - GPU memory tracking：enabled；allocated/reserved/max allocated 均为 0 MiB，因为本 smoke 未执行 GPU 张量训练。
- 观察：
  - public CIFAR 目录不可写，直接让 torchvision 在 `/root/autodl-pub` 解压会失败；当前底座正确使用公共 tar + 项目内缓存。
  - manifest 绑定 clean commit `fb1c38d`，可用于追溯基础设施结果。
- 结论：ENV-001、DATA-001、REPRO-001、LOG-001 和 BASE-001 的最小验收通过。
- 下一步：不要直接跑正式训练；先做 `SANITY-PLAN-001` 和 `INFRA-GAP-001`，明确 v1.1 指标落地需要哪些最小诊断 hook。

## 新实验模板

复制以下模板并追加到文件末尾：

```markdown
### EXP-XXX：实验名称

- 日期：YYYY-MM-DD
- Commit：`<sha>`
- 工作区：clean / dirty（若 dirty，列出差异）
- 假设：对应 `IDEA-XXX`
- 方法与开关：
- 配置文件：
- 数据集与路径：
- 任务协议：
- Seed：
- 环境：
- 启动命令：
- 日志路径：
- 产物路径：
- 状态：planned / running / completed / failed / stopped
- 指标：
- 观察：
- 结论：
- 下一步：
```
