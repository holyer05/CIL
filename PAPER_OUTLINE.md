# PAPER_OUTLINE.md

> 论文结构与“主张-证据”映射。当前处于 Assumption Mining Mode，没有选定论文主线，也没有方法章节。最后更新：2026-06-27。

## 当前写作状态

- IDEA-001 已经 PI 审计并评为 `Weak Reject`，原 observability-aware drift compensation 提纲停止使用。
- 当前不设正式题目，不写确定性摘要，不预设新方法。
- 论文方向必须由可证伪诊断结果选择，而不是先确定叙事再寻找支持实验。

## 候选问题池

`IDEA_POOL.md` 已记录 20 项 EFCIL 隐含假设。经 2026-06-27 严格筛选后，只保留两个活跃研究候选：

1. `A05`：单 prototype 是否足以代表旧类；
2. `A03`：当前任务数据是否能代理旧任务函数。

`A01` 降级为 cold-start 控制变量；`A07` 降级为 A05 的支撑诊断。这些都不是论文结论。

## 降级方向：第一任务覆盖决定 EFCIL 上限

### 降级后的作用

第一任务覆盖仍必须记录和控制，但不再作为主线。原因是近期 cold-start EFCIL 已经显式把 small first task / low-quality first-task backbone 作为核心难点；只证明 first-task coverage 影响性能，不足以构成新颖投稿主张。

### 必须具备的证据

- 第一任务类别数固定，仅改变类别组成和覆盖度。
- 第一任务后、任何增量训练前，对未来类别做冻结 linear probe、kNN 和可分性评价。
- 多种类顺序、多 seed、至少三个数据集。
- 方差分解证明 base coverage 的解释量显著高于随机噪声和常见方法增益。
- 方法排名在不同 coverage 条件下发生稳定变化，而非单次异常。
- 与已有 pre-training/base-task sensitivity 工作的差异明确。

### 不能支撑该主张的结果

- 只比较 small-base 与 large-base。
- 只在一个 CIFAR-100 顺序上报告相关性。
- 用最终准确率反向定义 coverage。
- 第一任务训练预算、类别数和语义覆盖同时变化。

### 当前状态

`降级为控制变量`

## 条件性论文主线 A：单 prototype 不是旧类充分表示

### 可能成立的核心主张

> prototype-centric EFCIL 的主要误差在部分场景中不是 prototype 位置估计不准，而是单均值表示本身无法表达旧类判别结构。

### 必须具备的证据

- 比较 stale prototype、oracle current prototype、隐藏旧数据 linear probe、kNN 和多中心 oracle。
- 证明 oracle current prototype 仍存在显著且稳定的不可恢复差距。
- 差距能被类内多模态度、散度、边界复杂度或 fine-grained 属性解释。
- 覆盖 SDC/LDC/ADC 类漂移方法和 PASS/FeTrIL/SimpleCIL 类 prototype 方法。
- coarse-grained 与 fine-grained 数据集结论一致或具有可解释差异。
- 旧数据只作为隐藏 oracle，不参与训练和方法选择。

### 不能支撑该主张的结果

- stale prototype 不如 oracle prototype。
- NCM 不如某个训练预算更大的 classifier。
- 只展示 t-SNE/UMAP。
- 只在一个类别或一个任务上观察到多模态。

### 当前状态

`未开始诊断`

## 条件性论文主线 B：当前任务数据不能可靠代理旧任务函数

### 可能成立的核心主张

> 在 exemplar-free CIL 中，当前任务数据上的蒸馏一致性、漂移拟合或代理距离并不能可靠预测隐藏旧类函数保持；这会系统性影响 LwF、drift compensation 和 adversarial proxy 类方法的适用边界。

### 必须具备的证据

- 比较新类数据上的 teacher-student 一致性、old/new feature mapping error、proxy distance 与隐藏旧类上的输出保持、排序保持、特征保持和分类保持。
- 覆盖普通当前数据蒸馏、LDC 类 projector 训练、ADC/APR 类 adversarial proxy 思路的代表性诊断。
- 按新旧类语义距离、first-task coverage、任务粒度、数据集和 backbone 分层。
- 证明失效不是单一模型训练失败，而是“新类观测无法约束旧类区域”的稳定现象。
- 旧类数据只用于隐藏 oracle 评价，不参与训练、阈值或方法选择。

### 不能支撑该主张的结果

- 只显示 LwF 或某个蒸馏方法最终准确率低。
- 只比较当前数据和旧数据的输入分布距离，没有连接到函数保持。
- 只在一个类顺序上观察到 teacher entropy 与 forgetting 弱相关。
- 使用旧类 oracle 信息设计代理或调参后再声称当前数据代理有效。

### 当前状态

`未开始诊断`

## 支撑性诊断：pseudo-feature 统计正确但流形错误

### 可能成立的核心主张

> 多种 EFCIL pseudo-replay 方法能够匹配旧类均值或协方差，却没有恢复真实旧类流形；其收益可能来自分类器正则化，而不是旧类数据分布重建。

### 必须具备的证据

- 覆盖 PASS、IL2A、FeTrIL、EFC、AdaGauss、APR 中至少三种不同 pseudo-feature 机制。
- 对真实隐藏旧特征与伪特征做二样本可分性、最近邻纯度、distribution precision/recall 和边界覆盖。
- 比较在伪特征上训练、在真实旧特征上测试的跨分布泛化。
- 区分一二阶统计匹配、流形匹配和最终分类收益。
- 证明结论跨任务、数据集、backbone 和伪特征数量稳定。
- 不把“可以区分真实/伪特征”单独当作失败，必须连接到分类或决策边界后果。

### 不能支撑该主张的结果

- 伪特征的 t-SNE 与真实特征看起来不同。
- 伪特征均值或协方差存在误差。
- 某一种采样超参数表现不好。
- 只比较最终平均准确率，不分析分布和跨分布泛化。

### 当前状态

`降级为 A05 支撑诊断`

## 共同诊断章节模板

无论最终选择哪条主线，证据结构应保持一致：

### 1. Problem Audit

- 明确被领域依赖但未验证的假设。
- 列出依赖该假设的本地论文、PyCIL 方法和近期方法。
- 区分论文显式声明、代码隐式选择和本项目推断。

### 2. Controlled Protocol

- 固定训练预算、类别数、任务数和 backbone。
- 将待检查变量与类顺序、随机种子、预训练和任务规模解耦。
- 旧类数据仅用于隐藏 oracle 评价。

### 3. Falsification Tests

- 预先写出支持条件和证伪条件。
- 报告效应量、置信区间和跨数据集稳定性。
- 包含能够推翻本项目解释的简单反例和替代解释。

### 4. Consequence Analysis

- 说明假设失效后，哪些现有结论需要重解释。
- 区分表示问题、分类器问题、统计近似问题和评测问题。
- 不把诊断现象直接包装成新算法需求。

### 5. Limitations

- 说明 oracle 旧数据只适用于分析，不是部署条件。
- 说明结论是否依赖 benchmark、backbone、任务边界或标签设定。
- 报告长期存储、训练算力和潜在隐私风险。

## 主张-证据门槛

| 候选主张 | 最低证据 | 当前状态 |
|---|---|---|
| 单 prototype 不是充分统计 | oracle prototype 仍显著落后其他 oracle 表示，且差距可解释 | 活跃候选 |
| 当前任务数据不能代理旧任务函数 | 当前数据一致性/漂移指标不能预测隐藏旧类函数保持，且失效可解释 | 活跃候选 |
| 第一任务 coverage 主导最终性能 | 多顺序方差分解、未来任务 probe、跨数据集复现 | 降级为控制变量 |
| pseudo-feature 偏离真实流形 | 多方法二样本与跨分布证据，并连接到分类后果 | A05 支撑诊断 |
| 现有平均指标掩盖真实机制 | per-class、old/new、oracle probe 与标准指标产生系统性冲突 | 未开始 |
| 无样例具有真实资源与隐私优势 | byte-matched 成本和隐私风险审计 | 未开始 |

## 题目与摘要准入条件

只有满足以下条件后，才能恢复正式论文 outline：

- A05 或 A03 至少一项在多数据集、多类顺序下被稳定证伪；
- 结果改变对现有方法或 benchmark 的解释，而不仅是一个相关性；
- 替代解释已通过受控实验排除；
- 与最近工作的差异能够在问题定义和证据层面说明；
- 所有结论可追溯到 `EXPERIMENT_LOG.md` 的正式实验记录。
