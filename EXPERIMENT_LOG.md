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
| RESEARCH-003 | 2026-06-27 | 待提交 | 近期 cold-start EFCIL 文献补充与假设严格筛选 | 不适用 | - | 完成 | 只保留 A05、A03；A01 降级为控制变量；A07 降级为支撑诊断 |

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
