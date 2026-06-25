# TODO.md

> 当前可执行任务列表。任务必须包含验收条件。最后更新：2026-06-25。

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

## P0：Assumption Mining 下一阶段

- [ ] `ASSUME-DIAG-001` 固化 A01 第一任务表示覆盖诊断。
  - 只定义变量、数据切分、oracle 指标和失败标准，不提出方法。
  - 必须区分第一任务类别数、语义覆盖、视觉域覆盖和随机顺序。
  - 验收：能够判断 base coverage 对最终性能的解释量是否超过方法增益。

- [ ] `ASSUME-DIAG-002` 固化 A05 prototype sufficiency 诊断。
  - 比较 stale prototype、oracle current prototype、hidden-old linear probe、kNN 和多中心 oracle。
  - 必须按 coarse/fine-grained、类内散度和多模态度分组。
  - 验收：明确 prototype 误差与 representation 误差的可观测分界。

- [ ] `ASSUME-DIAG-003` 固化 A07 pseudo-feature fidelity 诊断。
  - 定义真实/伪特征二样本可分性、最近邻纯度、分布 precision/recall、边界覆盖和跨分布泛化。
  - 旧类真实特征只能作为隐藏评价，不参与 pseudo-feature 生成或调参。
  - 验收：能够区分“伪特征真实”“伪特征仅有正则化作用”和“伪特征有害”。

- [ ] `ASSUME-PROTOCOL-001` 固化共同诊断协议。
  - 数据集至少覆盖 CIFAR-100、ImageNet-100、CUB-200。
  - 类顺序必须包含随机、语义集中和语义分散三类。
  - 指标除 `A_inc`、`A_last` 外，必须包含 per-class trajectory、old/new accuracy、oracle probes 和置信区间。
  - 验收：三项诊断共享同一数据划分、模型快照和日志口径。

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
  - 至少一个假设必须在多数据集、多顺序下被稳定证伪。
  - 证伪结果必须改变对现有方法或 benchmark 结论的解释，而不只是报告一个相关性。
  - 若三项均无稳定证据，回到 A02-A20 重新排序，不强行设计算法。
- [ ] `PAPER-GATE-001` 只有在 `ASSUME-GATE-001` 通过后，才允许确定题目、摘要主张和后续方法需求。

## 维护规则

- 完成任务时勾选，并在相应实验或提交记录中给出证据。
- 新任务使用稳定 ID，不复用已完成或已取消 ID。
- 被取消的任务保留并标注原因，不直接删除。
- 每次工作结束前重新排序优先级，确保下一步明确。
