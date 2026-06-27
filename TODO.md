# TODO.md

> 当前可执行任务列表。任务必须包含验收条件。最后更新：2026-06-27。

## 已完成

- [x] `AUDIT-001` 完成整个代码库与配置审计。
  - 证据：`EXPERIMENT_LOG.md` 的 `RESEARCH-001`。

- [x] `LIT-001` 阅读本地 8 篇论文并核查 2024-2026 年相关工作。
  - 证据：`PROJECT.md` 的文献覆盖表与 `IDEA_POOL.md` 的方向判断。

- [x] `ROUTE-001` 确定首选研究问题。
  - 历史结果：曾优先研究“漂移可观测性与保守补偿”。
  - 后续状态：经 PI 审计评为 Weak Reject，已降级，不再作为默认路线。

- [x] `PI-001` 完成 IDEA-001 的 AAAI/CVPR 审稿式反向评估。
  - 证据：`IDEA_POOL.md` 的 IDEA-001 PI 决策。
  - 结果：IDEA-001 暂缓，不继续优化。

- [x] `ASSUME-001` 完成 EFCIL 隐含假设挖掘。
  - 范围：8 篇本地论文、PyCIL 方法、已实现与未实现 EFCIL 路线。
  - 结果：记录 20 项可证伪假设，优先级为 A01、A05、A07。
  - 证据：`IDEA_POOL.md` 的 `ASSUMPTION-MINING-001`。

- [x] `ASSUME-SCREEN-001` 完成 20 项假设的严格筛选。
  - 评分维度：新颖性、可证伪性、实验成本、与现有工作的区分度、发展成方法的潜力。
  - 结果：仅保留 A05、A03 为活跃研究候选；A01 降级为 cold-start 控制变量；A07 降级为 A05 支撑诊断。
  - 证据：`IDEA_POOL.md` 的 `2026-06-27 严格筛选`。

- [x] `ASSUME-DIAG-002` 固化 A05 prototype sufficiency 诊断协议。
  - 范围：变量、oracle 对照、主指标、支持条件、拒绝条件和不能作为证据的结果。
  - 证据：`IDEA_POOL.md` 的 `A05 诊断协议` 与 `PAPER_OUTLINE.md` 的 `A05/A03 共同诊断协议 v1`。

- [x] `ASSUME-DIAG-004` 固化 A03 current-data proxy 诊断协议。
  - 范围：当前数据可观测指标、隐藏 oracle 指标、预测性判据、支持条件、拒绝条件和分层解释。
  - 证据：`IDEA_POOL.md` 的 `A03 诊断协议` 与 `PAPER_OUTLINE.md` 的 `A05/A03 共同诊断协议 v1`。

- [x] `ASSUME-PROTOCOL-001` 固化共同诊断协议。
  - 结果：明确 CIFAR-100、ImageNet-100、CUB-200；random/semantic-clustered/semantic-diverse；A01 作为控制变量；A07 作为 A05 支撑诊断；筛选矩阵与论文门矩阵。
  - 证据：`IDEA_POOL.md` 的 `最小实验矩阵`。

- [x] `ASSUME-REVIEW-001` 对 A05/A03 诊断协议做 PI 级反向审稿。
  - 不设计方法，不写代码。
  - 结论：`Revise before experiments`。A05 保留但需修订；A03 保留为次候选但需要 baseline 覆盖映射后决定 claim scope。
  - 证据：`IDEA_POOL.md` 的 `PI Review：A05/A03 诊断协议 v1`。

- [x] `ASSUME-PROTOCOL-REV-001` 将 A05/A03 协议修订为 v1.1。
  - 不设计方法，不写代码。
  - 已补齐 oracle-fit / oracle-eval / final-audit 分割、A05 primary comparator、sample-budget/capacity matched 对照、A03 continuous retention 主指标、指标族预注册、三阶段矩阵。
  - 证据：`IDEA_POOL.md` 和 `PAPER_OUTLINE.md` 的 `诊断协议 v1.1`。

## P0：Assumption Mining 下一阶段

- [x] `BASELINE-SCOPE-001` 将现有 PyCIL 方法映射到 A05/A03 最小实验矩阵。
  - 不修改代码，只读配置和方法实现。
  - 结果：SimpleCIL 可作 A05 Sanity 轨迹来源；LwF 可作 A03 Sanity 轨迹来源；FeTrIL 可作 Screen 候选但当前依赖和配置不满足；A03 只能 narrow 到 LwF/new-data distillation。
  - 证据：`IDEA_POOL.md` 的 `BASELINE-SCOPE-001：PyCIL baseline 覆盖映射`。

- [ ] `SANITY-PLAN-001` 制定 v1.1 Sanity 阶段运行计划。
  - 不写代码，不启动训练。
  - 明确 CIFAR-100 上 random + semantic-clustered、1 seed、SimpleCIL/NCM + LwF 的配置来源、预计产物、oracle split 文件口径和日志字段。
  - 验收：形成可执行但尚未执行的 sanity checklist。

- [ ] `INFRA-GAP-001` 列出 v1.1 指标落地前的最小实验底座缺口。
  - 不启动训练。
  - 覆盖 semantic class order、oracle split、A05 medoid/2-center、A03 feature/logit dump、continuous retention、metric recompute、PyCIL legacy seed/device 对接。
  - 验收：明确哪些已有 `experiment_base/` 支持，哪些必须新增诊断脚本或最小 trainer hook。

## 暂缓或取消

- [ ] `DIAG-001` 漂移可观测性诊断。
  - 状态：`暂缓`。
  - 原因：IDEA-001 已被 PI 审计评为 Weak Reject，本轮不继续优化。

- [ ] `NOVELTY-001` IDEA-001 最近工作差异表。
  - 状态：`暂停`。
  - 原因：不再以 IDEA-001 为默认投稿方向。

- [ ] `METHOD-GATE-001` IDEA-001 方法准入。
  - 状态：`取消当前排期`。
  - 原因：尚未选择任何方法主线。

- [ ] `ASSUME-DIAG-001` A01 第一任务表示覆盖诊断。
  - 状态：`降级为控制变量`。
  - 原因：近期 cold-start EFCIL 工作已经显式关注 small first task / first-task-biased backbone；独立作为主线的新颖性不足。

- [ ] `ASSUME-DIAG-003` A07 pseudo-feature fidelity 诊断。
  - 状态：`降级为 A05 支撑诊断`。
  - 原因：与 A05/A06 强耦合，且需要覆盖多种 pseudo-feature 方法，当前实验成本高于 A03/A05。

## P1：建立可信实验底座

以下任务已在独立 `experiment_base/` 中完成第一阶段；PyCIL 原始代码未修改。

- [x] `ENV-001` 固化运行环境
  - 补齐并锁定 scipy、scikit-learn、POT、quadprog 等依赖。
  - 验收：新 shell 中核心依赖可导入，版本记录可复现。
  - 证据：`experiment_base/requirements.lock`；远程新 shell 已验证 scipy 1.11.4、sklearn 1.3.2、POT 0.9.5、quadprog 可导入。

- [x] `DATA-001` 配置数据路径
  - CIFAR 优先使用公共缓存；ImageNet100 使用明确路径配置，不在 Python 中写死服务器路径。
  - 验收：loader 报告正确类别数与样本规模。
  - 证据：`experiment_base/configs/smoke_cifar100.json` 使用公共 CIFAR-100 tar 与项目内缓存；`configs/datasets.example.json` 显式声明 ImageNet100 路径；smoke loader 报告 train=50000、test=10000、classes=100。

- [x] `REPRO-001` 修复复现控制
  - 让配置 seed 真正控制 Python、NumPy、PyTorch、CUDA 和 class order。
  - 统一单 GPU 设备处理；消除必要路径上的硬编码 `.cuda()`。
  - 验收：同 seed 可复现，不同 seed 确实改变类顺序/随机过程。
  - 证据：`experiment_base/core/repro.py` 与 `run_smoke.py`；manifest 记录 `same_seed_reproducible=True`、`different_seed_changes_order=True`。

- [x] `LOG-001` 建立结构化运行 manifest
  - 保存 commit、配置快照、环境、类顺序、指标矩阵、运行时间和显存。
  - 验收：任何表格数值都能追溯到唯一实验 ID 和原始文件。
  - 证据：`experiment_base/runs/20260627T051735Z_smoke_cifar100_loader_repro_manifest/manifest.json` 记录 commit `fb1c38d`、dirty=false、配置快照、环境、class order、metrics、elapsed_seconds 和 GPU memory。

- [x] `BASE-001` 完成最小 smoke test。
  - 证据：clean commit `fb1c38d` 下执行 `python -m experiment_base.run_smoke --config experiment_base/configs/smoke_cifar100.json` 成功。

- [ ] `BASE-002` 复现 LwF+NCM 和 FeTrIL cold-start baseline。
- [ ] `BASE-003` 复现与假设诊断直接相关的 baseline；具体集合在诊断协议完成后确定。

## P2：论文主线选择门

- [ ] `ASSUME-GATE-001` 根据 A01、A05、A07 诊断结果选择或放弃论文主线。
  - 更新：根据 2026-06-27 筛选，主门槛改为 A05 与 A03。
  - 至少一个活跃候选必须在多数据集、多顺序下被稳定证伪。
  - 证伪结果必须改变对现有方法或 benchmark 结论的解释，而不只是报告一个相关性。
  - 若三项均无稳定证据，回到 A02-A20 重新排序，不强行设计算法。
- [ ] `PAPER-GATE-001` 只有在 `ASSUME-GATE-001` 通过后，才允许确定题目、摘要主张和后续方法需求。

## 维护规则

- 完成任务时勾选，并在相应实验或提交记录中给出证据。
- 新任务使用稳定 ID，不复用已完成或已取消 ID。
- 被取消的任务保留并标注原因，不直接删除。
- 每次工作结束前重新排序优先级，确保下一步明确。
