# EXPERIMENT_LOG.md

> 实验与研究审计事实日志。只追加或更正有证据的错误，不删除失败记录。最后更新：2026-06-25。

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
