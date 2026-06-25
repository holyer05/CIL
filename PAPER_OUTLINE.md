# PAPER_OUTLINE.md

> 论文结构与“主张-证据”映射。当前仅为研究路线提纲，不代表已有实验结论。最后更新：2026-06-25。

## 暂定题目方向

暂不固定正式题目。工作标题可使用：

> When Should Old Prototypes Move? Observability-Aware Drift Compensation for Exemplar-Free Class-Incremental Learning

该标题只表达研究问题，不应在核心诊断成立前作为最终包装。

## 一句话问题定义

无旧样本时，当前任务数据并不能完整观测旧类在新特征空间中的变化；现有漂移补偿方法通常默认估计结果应作用于所有旧类和所有方向，因此可能把不可辨识的漂移误当作可恢复信号。

## 暂定核心假设

以下均为待验证假设：

1. 相邻任务间的特征变化包含当前数据支持的低秩共享分量，以及无法由当前数据识别的残差。
2. 当前数据覆盖度或 leverage/uncertainty 分数能够预测旧类 prototype 补偿误差。
3. 只更新高支持分量、对低支持分量保守锚定，会优于无条件全空间映射。
4. 该收益来自补偿可靠性，而不是额外参数、更多训练轮次或更强正则化。

若诊断不支持，必须修改或放弃主张。

## 预期贡献形态

1. 提出 EFCIL 中“漂移可观测性”的问题定义和可测量诊断。
2. 证明或实证展示当前任务覆盖与旧类补偿误差的关系。
3. 提出轻量的 observability-aware conservative transport。
4. 建立统一的旧信息存储与额外计算预算报告。

贡献 1-2 比方法模块更重要；若机制不成立，不继续堆叠组件。

## 论文结构

### 1. Introduction

- EFCIL 的隐私与存储动机。
- cold-start 需要 backbone plasticity，因此 prototype/statistics 会漂移。
- SDC、LDC、ADC、AdaGauss、APR 已显著改进“如何估计漂移”。
- 未解决问题：当前数据对旧类漂移的支持不均匀，估计可能不可辨识。
- 核心观点：补偿应带有“证据范围”和拒绝机制。

### 2. Related Work

#### 2.1 Exemplar-Free CIL

LwF、PASS/IL2A/SSRE、FeTrIL/FeCAM、ACIL/DS-AL。

#### 2.2 Representation and Prototype Drift

SDC、EFC、ADC、LDC、FCS/ESSA、AdaGauss、APR。

需要按以下维度比较：

- 漂移对象：feature / mean / covariance / classifier；
- 估计数据：当前原图 / 对抗图 / pseudo-feature；
- 映射形式：局部平移 / 全局线性 / 非线性 / 每类迁移；
- 是否估计可靠性；
- 是否允许拒绝更新；
- 长期存储和计算成本。

#### 2.3 Future-Compatible Representation

IR、PRL、DCNet。说明本项目不主张再次设计空间分离 Loss，而是研究 transport 的可观测边界。

### 3. Problem Formulation

- 任务序列和无样例约束。
- 旧/新 feature extractor：`f_{t-1}` 与 `f_t`。
- 当前任务在旧空间和新空间中的配对特征。
- 旧类 prototype/covariance 状态。
- oracle drift 仅作为诊断真值。
- 定义支持子空间、不可观测残差和 compensation error。
- 定义 storage budget，prototype/covariance/旧模型/索引均计入。

### 4. Diagnostic Study

#### 4.1 How Much Drift Is Shared?

- 漂移矩阵谱、有效秩、跨类/跨任务稳定性。
- cold-start 与 warm-start 对比。

#### 4.2 Is Drift Observable from Current Data?

- 当前任务覆盖度与旧类 oracle drift 的关系。
- semantic-near 与 semantic-far old classes。
- 后期任务是否出现支持度下降。

#### 4.3 When Does Compensation Hurt?

- NCM、SDC、LDC 与 oracle 的每类误差。
- 错误补偿率和性能下降案例。

该章节是方法准入门槛。如果结论不成立，不进入第 5 节所设想的方法。

### 5. Method（条件性占位）

#### 5.1 Supported Low-Rank Transport

从当前任务的 paired old/new features 估计低秩 transport。

#### 5.2 Class/Direction Observability

为旧类 prototype 的每个分量计算支持度或置信度。

#### 5.3 Conservative Update

- 高支持分量：执行 transport；
- 低支持分量：锚定、收缩或拒绝更新；
- 可选：同一原则扩展到低秩 covariance。

#### 5.4 Complexity

目标为闭式 ridge/SVD 或单层线性计算，不引入生成器和复杂网络。

### 6. Experiments

#### 6.1 Protocol

- 主设置：from-scratch cold-start。
- 数据集：CIFAR-100、TinyImageNet、ImageNet100。
- 多 seed 和固定类顺序清单。
- 指标：`A_inc`、`A_last`、forgetting、old/new accuracy、per-class compensation error。

#### 6.2 Baselines

FineTune、LwF+Linear、LwF+NCM、SDC、LDC、FeTrIL；条件允许加入 EFC、ADC、AdaGauss、APR。

#### 6.3 Mechanism Validation

- 支持度-误差相关性和校准；
- oracle drift explained variance；
- 高/低支持类的分组结果；
- 错误补偿拒绝率。

#### 6.4 Main Results

只在机制诊断成立后报告。

#### 6.5 Ablation and Controls

- 无门控 / 随机门控 / 距离门控 / observability 门控；
- 全秩 / 低秩；
- 同参数量和同训练预算；
- mean-only 与 mean+covariance；
- task order、任务数和 domain shift。

#### 6.6 Cost and Privacy Accounting

报告模型副本、prototype、covariance、projector、索引、增强参数、训练时间和显存。

### 7. Limitations

预期限制包括：依赖任务边界、当前任务过小时估计不足、极端 domain shift 下可能拒绝大量更新、旧类统计仍可能泄露信息。

### 8. Conclusion

只总结被诊断和多 seed 实验支持的结论。

## 主张-证据表

| 主张 | 所需证据 | 当前状态 |
|---|---|---|
| 漂移含当前数据支持的低秩共享分量 | oracle drift 谱与跨 seed/数据集分析 | 未开始 |
| 支持度可预测补偿误差 | per-class 相关性、排序和校准 | 未开始 |
| 无条件补偿会伤害部分旧类 | SDC/LDC 每类负增益与案例 | 未开始 |
| 保守更新优于全映射 | 公平主实验和随机/距离门控对照 | 未开始 |
| 收益来自可靠性机制 | 同参数量、同训练预算、模块关闭实验 | 未开始 |
| 额外成本可控 | 参数、存储、显存、训练时间 | 未开始 |

## 写作准入条件

在撰写确定性摘要和贡献列表前，至少需要：

- baseline 复现可信；
- 漂移可观测性诊断在多个 seed/数据集成立；
- 与 LDC、ADC、AdaGauss、APR 的差异明确；
- 完整主实验和关键消融完成；
- 所有表格可追溯到 `EXPERIMENT_LOG.md` 中的实验 ID。
