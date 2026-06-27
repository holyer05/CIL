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

## P0：Assumption Mining 下一阶段

- [ ] `ASSUME-DIAG-002` 固化 A05 prototype sufficiency 诊断。
  - 比较 stale prototype、oracle current prototype、hidden-old linear probe、kNN 和多中心 oracle。
  - 必须按 coarse/fine-grained、类内散度和多模态度分组。
  - 验收：明确 prototype 误差与 representation 误差的可观测分界。

- [ ] `ASSUME-DIAG-004` 固化 A03 current-data proxy 诊断。
  - 比较新类数据上的 teacher-student 一致性、漂移拟合误差、代理距离与隐藏旧类函数保持之间的关系。
  - 必须按新旧类语义距离、cold-start 程度、任务粒度和当前数据支持度分层。
  - 验收：能够判断当前任务数据是否能预测或约束旧任务函数保持，以及 ADC/APR 类代理是否真正弥补代理缺口。

- [ ] `ASSUME-PROTOCOL-001` 固化共同诊断协议。
  - 数据集至少覆盖 CIFAR-100、ImageNet-100、CUB-200。
  - 类顺序必须包含随机、语义集中和语义分散三类。
  - 指标除 `A_inc`、`A_last` 外，必须包含 per-class trajectory、old/new accuracy、oracle probes 和置信区间。
  - A01 first-task coverage 作为所有诊断的控制变量，必须记录并分层报告，但不作为独立主线。
  - A07 pseudo-feature fidelity 作为 A05 的支撑诊断，只有 A05 初步成立后再展开。
  - 验收：A05 与 A03 共享同一数据划分、模型快照和日志口径。

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

以下任务会涉及代码修改。当前 Assumption Mining Mode 禁止执行，只有用户明确允许后才能开始。

- [ ] `ENV-001` 固化运行环境
  - 补齐并锁定 scipy、scikit-learn、POT、quadprog 等依赖。
  - 验收：新 shell 中核心依赖可导入，版本记录可复现。

- [ ] `DATA-001` 配置数据路径
  - CIFAR 优先使用公共缓存；ImageNet100 使用明确路径配置，不在 Python 中写死服务器路径。
  - 验收：loader 报告正确类别数与样本规模。

- [ ] `REPRO-001` 修复复现控制
  - 让配置 seed 真正控制 Python、NumPy、PyTorch、CUDA 和 class order。
  - 统一单 GPU 设备处理；消除必要路径上的硬编码 `.cuda()`。
  - 验收：同 seed 可复现，不同 seed 确实改变类顺序/随机过程。

- [ ] `LOG-001` 建立结构化运行 manifest
  - 保存 commit、配置快照、环境、类顺序、指标矩阵、运行时间和显存。
  - 验收：任何表格数值都能追溯到唯一实验 ID 和原始文件。

- [ ] `BASE-001` 完成最小 smoke test。
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
