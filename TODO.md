# TODO.md

> 当前可执行任务列表。任务必须包含验收条件。最后更新：2026-06-25。

## 已完成

- [x] `AUDIT-001` 完成整个代码库与配置审计。
  - 证据：`EXPERIMENT_LOG.md` 的 `RESEARCH-001`。

- [x] `LIT-001` 阅读本地 8 篇论文并核查 2024-2026 年相关工作。
  - 证据：`PROJECT.md` 的文献覆盖表与 `IDEA_POOL.md` 的方向判断。

- [x] `ROUTE-001` 确定首选研究问题。
  - 结果：优先研究“漂移可观测性与保守补偿”，暂不编码。

## P0：编码前必须完成

- [ ] `PROTO-001` 固化主实验协议
  - 主协议：从头训练、cold-start、等量任务切分。
  - 首选 CIFAR-100 10-task；扩展 TinyImageNet/ImageNet100。
  - 明确 `A_inc`、`A_last`、forgetting、old/new accuracy 和内存/计算预算。
  - 验收：协议写入 `PROJECT.md`，所有 baseline 使用同一类顺序和训练预算。

- [ ] `BASESET-001` 确定最小可信 baseline 集合
  - 必须包含：FineTune、LwF+Linear、LwF+NCM、SDC、LDC、FeTrIL。
  - 条件允许再加入：EFC、ADC、AdaGauss、APR。
  - 验收：逐项确认官方协议、classifier、warm/cold start 和存储预算，禁止混用论文数字。

- [ ] `DIAG-001` 设计漂移可观测性诊断
  - 定义 oracle mean drift、covariance drift 和 compensation error。
  - 定义当前数据支持子空间、正交残差和每类支持度。
  - 明确旧数据仅用于诊断真值，不参与方法训练。
  - 验收：形成无需新方法代码即可执行的实验矩阵和失败判据。

- [ ] `NOVELTY-001` 对 IDEA-001 做最近工作差异表
  - 精读 LDC、ADC、EFC、AdaGauss、APR、FCS/ESSA、DCNet。
  - 验收：每项工作写出“估计对象、数据支持、是否门控、均值/协方差、复杂度、开放缺口”。

## P1：建立可信实验底座

以下任务会涉及代码修改，只有在用户明确允许结束 Research Mode 后执行。

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
- [ ] `BASE-003` 实现/复现 SDC 与 LDC 对照后再开始主方法。

## P2：诊断通过后才允许的方法开发

- [ ] `METHOD-GATE-001` 检查 IDEA-001 是否通过准入门槛。
  - 支持度必须在多个 seed/数据集上预测补偿误差。
  - 若不成立，转向“错误补偿检测/拒绝”，不强行设计新模块。

- [ ] 定义独立配置开关，默认关闭。
- [ ] 写出 baseline 等价性检查。
- [ ] 优先闭式或单层低秩 transport，不引入复杂模块。
- [ ] 先做单数据集、单 seed 机制验证，再扩展多 seed。
- [ ] 报告均值、标准差、显存、训练时间和长期存储字节数。

## 维护规则

- 完成任务时勾选，并在相应实验或提交记录中给出证据。
- 新任务使用稳定 ID，不复用已完成或已取消 ID。
- 被取消的任务保留并标注原因，不直接删除。
- 每次工作结束前重新排序优先级，确保下一步明确。
