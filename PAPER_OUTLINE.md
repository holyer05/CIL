# PAPER_OUTLINE.md

> 论文结构与“主张—证据”映射。当前仅为工作提纲，不代表已有结论。最后更新：2026-06-25。

## 暂定题目

TBD：题目必须在核心机制和实验证据稳定后确定，避免先定包装再寻找结果。

## 一句话问题定义

在不保存旧类样本的类增量学习中，旧类表征变化不可直接观测；现有方法可能对漂移的可恢复性作出过强假设，需要区分可由当前任务识别的共享变化与不可可靠估计的变化。

## 暂定核心主张

以下均为待验证主张：

1. 跨任务表征漂移包含可迁移的共享结构，但并非所有变化都可由新类数据识别。
2. 只补偿可可靠识别的变化，比无差别漂移补偿更稳健。
3. 该机制可在无旧样本、较低额外复杂度下改善稳定性—可塑性权衡。

若实验不支持，必须修改或删除主张，不能反向筛选结果。

## 论文结构

### 1. Introduction

- 类增量学习与无样例约束的现实意义。
- 核心困难：旧数据缺失导致旧类漂移不可直接观测。
- 现有路线及其隐含假设。
- 研究缺口：未显式讨论漂移可辨识性或共享结构边界。
- 方法直觉和贡献概览。

### 2. Related Work

- Class-Incremental Learning
- Exemplar-Free Class-Incremental Learning
- Knowledge Distillation and Classifier Alignment
- Representation Drift Estimation/Compensation
- Stability–Plasticity and Selective Parameter Update

相关工作部分必须明确最接近方法的数学和实验差异，不能只按类别罗列。

### 3. Problem Formulation

- 任务序列、类别集合与无样例约束。
- 模型、特征提取器与分类器定义。
- 表征漂移和不可观测量定义。
- 评价协议与计算/存储约束。

### 4. Method

当前占位结构，待想法通过验证后确定：

- 4.1 Empirical motivation / diagnostic observation
- 4.2 Identifiable shared drift model
- 4.3 Conservative compensation or update rule
- 4.4 Training objective and algorithm
- 4.5 Complexity and memory analysis

### 5. Experiments

#### 5.1 Setup

- Datasets and task protocols
- Baselines
- Backbones and implementation details
- Metrics and statistical reporting

#### 5.2 Main Results

至少包含多个数据集、统一协议和多随机种子；报告均值与标准差。

#### 5.3 Mechanism Validation

- 共享漂移是否存在；
- 可辨识性估计是否预测补偿误差；
- 对旧类稳定性和新类可塑性的分别影响。

#### 5.4 Ablation and Controls

- 每个模块关闭实验；
- 参数量、计算量和训练轮数匹配；
- 关键超参数敏感性；
- 与最接近方法的公平对照。

#### 5.5 Robustness and Limitations

- 不同任务长度、类别顺序和骨干；
- 失败场景；
- 额外存储与计算成本。

### 6. Conclusion

只总结被实验支持的机制和贡献，并明确适用边界。

## 主张—证据表

| 主张 | 所需证据 | 当前状态 |
|---|---|---|
| 漂移存在可迁移共享结构 | 多数据集、跨类子空间和迁移诊断 | 未开始 |
| 可辨识性可预测补偿误差 | 相关性、校准与可控实验 | 未开始 |
| 方法优于无差别补偿 | 公平主实验与多 seed | 未开始 |
| 收益来自提出机制 | 关闭模块、随机/容量匹配对照 | 未开始 |
| 额外成本可控 | 参数、显存、训练和推理开销 | 未开始 |

## 写作准入条件

在撰写确定性摘要和贡献列表前，至少需要：

- 基线复现可信；
- 核心机制诊断成立；
- 完整主实验和关键消融完成；
- 多 seed 统计与失败案例可用；
- 所有表格可追溯到 `EXPERIMENT_LOG.md` 中的实验 ID。
