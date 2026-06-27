# IDEA_POOL.md

> 研究想法池。这里记录的是待验证假设，不代表项目结论。最后更新：2026-06-27。

## 状态定义

- `候选`：只有初步动机，尚未完成文献和可证伪性检查。
- `调研`：正在检查相关工作、理论依据和差异点。
- `待实现`：假设清晰，已定义最小实验和关闭开关。
- `实验中`：已有实现，正在进行受控实验。
- `采纳`：机制和收益得到充分证据支持。
- `暂缓`：方向有价值，但当前新颖性、成本或主线匹配度不足。
- `淘汰`：创新性、有效性或可解释性不足；保留淘汰原因。

## 文献审计后的方向判断

当前 EFCIL 已形成几条拥挤路线：

1. 各向同性蒸馏或空间维护：LwF、PASS、IR；
2. prototype/pseudo-feature rehearsal：PASS、IL2A、FeTrIL、EFC；
3. 漂移补偿：SDC、EFC、ADC、LDC、AdaGauss、APR；
4. prospective/orthogonal geometry：PRL、DCNet；
5. 冻结 backbone 或解析学习：FeTrIL、FeCAM、ACIL、DS-AL、Muheal；
6. 生成或对抗伪回放：model inversion、ADC、APR、diffusion replay。

仅提出“共享漂移映射”“局部几何保持”或“预留空间”已不足以构成清晰创新。

## 重点审计方向

### IDEA-001：可观测子空间上的保守漂移补偿

- 状态：`暂缓（PI 评审：Weak Reject）`
- 原始问题：给定当前任务数据、旧模型和新模型，旧类 prototype 漂移的哪些方向是可识别的？
- 原始假设：当前任务数据只覆盖旧特征空间的一部分；漂移在该支持子空间内较可靠，正交残差不可辨识，因此只应补偿高支持分量。
- PI 结论：问题有诊断价值，但目前不足以作为 AAAI/CVPR 主线。禁止直接进入方法实现；必须先通过下述可证伪检查。

#### 1. 为什么该方向可能是错误方向

1. **把覆盖度当作可观测性，概念可能不成立。** 当前类别特征张成的子空间，只描述新类样本位于哪里；它不等价于旧类在网络更新后的运动规律。旧类漂移取决于参数更新、激活边界和类条件 Jacobian，而不是仅由当前特征的 SVD 决定。
2. **旧类真实漂移在无旧数据条件下原则上不可验证。** 两个更新后的模型可以在全部当前数据上表现相同，却在未观测旧类区域产生不同映射。若不增加关于平滑性、共享变换或局部线性的强假设，就无法从当前数据唯一识别旧类漂移。
3. **存在一个很窄的有效区间。** 如果新旧类共享一个稳定、近似线性的全局变换，LDC 一类简单映射已经足够；如果变换高度类条件化，当前数据又无法识别旧类映射。IDEA-001 只有在“部分共享但又不能被现有映射处理”的中间区域才可能有效。
4. **低支持不代表不应更新。** 网络参数更新是全局的。一个旧 prototype 即使远离当前特征子空间，也可能经历稳定且可预测的旋转、缩放或归一化变化；将其锚定反而会保留过时坐标。
5. **高支持也不代表可以安全更新。** 当前样本附近的映射可能受类别判别训练驱动，具有强烈的新类偏置；局部覆盖充分仍可能把旧 prototype 推向错误类别。
6. **项目可能误诊主要误差来源。** 旧类下降不一定主要来自 prototype 均值漂移，还可能来自协方差变化、维度坍缩、任务近期偏置、新旧类别重叠或分类器校准。只研究均值 transport 可能优化了次要因素。
7. **“保守门控”容易退化成普通正则化。** 如果收益主要来自少更新或不更新，Reviewer 会认为它只是 shrinkage、early stopping 或 no-compensation baseline 的重新包装，而不是新的研究发现。

#### 2. 现有工作是否已经隐含处理

- **SDC**：距离加权本身就是局部支持假设；远离当前样本的旧 prototype 获得较弱、较间接的漂移估计。
- **LDC**：通过当前样本在旧/新模型下的成对特征学习映射，并用受限 projector 控制外推；其失败分析已经指出当前数据偏置造成旧类映射误差。
- **ADC**：不是接受当前数据缺乏旧类覆盖，而是把当前图像对抗移动到旧 prototype 附近，再依据迁移性估计类特定漂移。这在功能上直接针对“旧类区域未被观测”。
- **APR**：进一步用在线对抗伪回放和 transfer matrix 校准均值/协方差，同样试图补足不可见区域。
- **EFC**：经验特征矩阵识别对旧任务重要的方向，并只对这些方向施加强约束；虽然对象不是 transport 可辨识性，但“方向选择”并非新概念。
- **AdaGauss**：指出均值补偿不足，并显式处理 covariance drift 与 dimensional collapse，削弱了只围绕 prototype 均值建立论文的充分性。
- **CUBER 等子空间方法**：已经使用输入子空间或任务相关性来决定哪些旧知识可以被选择性更新，概念上接近“只在有证据的子空间操作”。
- **BiCyc（2026）**：使用双向映射和 cycle consistency 处理单向 projector 的系统偏差与任务间累积不一致。循环残差天然可以被解释为映射可靠性信号，与 IDEA-001 的审稿重叠风险很高。

结论：现有论文未必使用“observability”这个词，但已经分别用局部权重、受限映射、对抗覆盖、重要方向、任务相关性和循环一致性处理相同症状。仅更换术语不能形成创新。

#### 3. 新颖性判断

- **问题命名的新颖性：中等。** 在 EFCIL 中显式讨论“何时不应补偿”有一定价值。
- **技术对象的新颖性：偏低。** 若最终只是 SVD、leverage score、邻域密度、projector residual 或阈值门控，这些都容易被视为现有工具的直接组合。
- **方法层面的新颖性：当前不可判断，但默认不足。** 必须先证明现有可靠性代理无法解释目标现象，并证明“可观测性”具有独立、可计算且跨任务泛化的定义。
- **截至 2026-06-25 的投稿风险：高。** LDC、ADC、APR、AdaGauss 和 2026 年 BiCyc 已使漂移补偿赛道进一步拥挤。

#### 4. AAAI/CVPR Reviewer 最可能的质疑

1. 你们如何形式化 observability？它与样本密度、domain overlap、leverage、projection residual 或 cycle consistency 有什么本质差异？
2. 在不能访问旧数据时，所谓置信度如何校准？阈值是否使用旧类测试数据或 oracle drift 调过？
3. 为什么当前类的特征子空间能够代表旧类的参数响应？是否有理论条件或反例分析？
4. 相比 `LDC + spectral truncation`、`LDC + ridge`、`LDC + cycle residual` 或 `SDC + neighborhood count`，贡献在哪里？
5. 增益是否只是来自更少地移动 prototype？简单 no-compensation、固定 shrinkage 或随机门控是否同样有效？
6. 为什么只处理均值，不处理 covariance drift、dimensional collapse 和 task-recency bias？
7. 是否在同一批任务和数据集上同时设计分数、调阈值并报告相关性，造成循环验证？
8. 结果是否依赖类别语义相似度、任务顺序、基础任务大小或 backbone？
9. 方法是否真的 exemplar-free？保存的旧模型、prototype、子空间基、映射矩阵和校准信息占多少长期存储？
10. 是否遗漏 2025--2026 年最强基线，尤其 APR、AdaGauss、BiCyc 及新的 prototype rehearsal 工作？

#### 5. 最脆弱的假设

1. 当前数据的特征 span 与旧类漂移的可识别方向一致。
2. 旧类和新类共享足够稳定的局部或低秩变换。
3. 支持度可以在完全无旧样本条件下校准，并跨任务、数据集和 backbone 泛化。
4. 正交残差不可识别，因此保持不动比错误更新更安全。
5. prototype 均值漂移是主要误差，而非 covariance、坍缩或分类边界偏置。
6. 线性子空间和欧氏距离能够描述深网的非线性特征演化。
7. oracle 分析只用于评价，不会通过超参数、阈值或设计迭代泄露到方法选择。

#### 6. 即使成功也无法证明贡献的实验

以下结果只能作为初步现象，不能支撑论文主张：

- 在一个 CIFAR-100 划分上观察到支持度与补偿误差相关。
- 在相同任务序列上调阈值后，门控 LDC 比原始 LDC 高若干百分点。
- oracle prototype 明显优于估计 prototype。
- t-SNE/UMAP 显示高支持类别看起来更集中。
- 低秩映射优于全秩映射；这可能只是正则化效应。
- 高支持类别的漂移预测更准；如果支持度直接由回归残差定义，这属于近似同义反复。
- 仅比较 full mapping、gating 和 no compensation，没有简单 shrinkage、随机 gate、邻域密度及 cycle residual。
- 只报告平均准确率，没有验证置信度是否真的能识别“补偿有害”的类别或任务。
- 在旧类数据参与阈值选择后获得更好结果；这不再证明部署时可用。

#### 7. 论文成立前必须增加的实验或分析

这些是 IDEA-001 继续保留为候选研究问题的最低门槛，不是新方法设计：

1. **不可识别性检查**：构造当前数据观测相同、但旧类真实漂移不同的反例，明确问题在哪些附加假设下才可识别。
2. **代理有效性检查**：使用旧数据仅作隐藏评价，测试候选支持度能否预测“补偿相对不补偿是否有害”，报告 AUROC、AUPRC、可靠性图和校准误差，而不只报告 Pearson 相关系数。
3. **跨任务校准**：在一组任务或数据集上确定分数/阈值，在未参与设计的任务顺序、数据集和 backbone 上直接测试，禁止使用目标旧类数据重新调参。
4. **简单代理对照**：必须包括样本密度、到当前类距离、邻域数量、回归残差、leverage、奇异值截断、cycle residual、固定 shrinkage、随机 gate 和完全不补偿。
5. **最新强基线**：至少覆盖 SDC、LDC、ADC、AdaGauss、APR、BiCyc；若代码不可用，必须明确说明并避免声称全面 SOTA。
6. **机制分解**：分别测量 prototype mean drift、covariance drift、特征坍缩、分类器偏置和新旧类混淆，证明目标现象不是其他问题的代理。
7. **可控覆盖压力测试**：系统改变新旧类别语义重叠、任务顺序、基础任务大小和增量步数，验证“支持不足时估计失效”是稳定规律。
8. **非线性反例与变换测试**：比较平移、旋转、缩放、各向异性和类条件非线性漂移，证明结论不只适用于预设的低秩线性世界。
9. **多数据集多随机种子**：至少 CIFAR-100、ImageNet-100、CUB-200，覆盖 cold-start 与常规大基础任务协议，并报告显著性。
10. **资源与泄露审计**：报告旧模型、prototype、统计量和映射存储；严格记录 oracle 数据只参与最终分析，不参与方法选择。

#### PI 决策

- 评级：**Weak Reject（方向一般）**。
- 原因：问题直觉合理，但核心等价关系未经证明，现有工作已经隐含覆盖大部分动机，且最新漂移补偿工作使方法空间拥挤。当前版本更像一套诊断视角，而不是足以支撑 AAAI/CVPR 的独立贡献。
- 项目动作：从“主方向”降级为`暂缓`。只有当不可识别性分析和跨任务代理验证同时通过，并能证明其区别于简单 residual/density/cycle-consistency 指标时，才重新评估；否则转为实验诊断工具，不作为论文主贡献。

## ASSUMPTION-MINING-001：EFCIL 领域隐含假设审计

- 状态：`调研完成，等待诊断优先级确认`
- 范围：8 篇本地论文、PyCIL 全部方法结构、已实现 EFCIL 方法和本地未实现方法。
- 原则：以下内容只提出可证伪假设和诊断实验，不提出新 Loss、新模块或新网络。
- 证据边界：旧类数据可以作为隐藏 oracle 评价集，但不能参与训练、阈值选择或方法调参。

### A01：第一任务学到的表示足以支撑全部未来类别

- **依赖者**：LwF；PASS、IL2A、SSRE、FeTrIL、SimpleCIL、ACIL、DS-AL；IR、PRL；多数 warm-start 或冻结 backbone 方法。
- **为什么可能不成立**：第一任务类别可能只覆盖未来视觉因素的一小部分。相同类别数下，不同语义组成、纹理复杂度和域覆盖会产生完全不同的可迁移表示。
- **失效现象**：最终性能和方法排名主要由第一任务类别决定；后续算法改进很小；在 semantic-far 类上所有方法同时失败。
- **诊断实验**：固定类别数和训练预算，构造高覆盖、低覆盖、语义集中和随机第一任务；在尚未增量训练前，测量第一任务 backbone 对未来各任务的冻结 linear probe、kNN 和类内/类间可分性，再与最终增量性能相关。
- **若证伪后的主线潜力**：`高`。可形成“EFCIL 的隐藏瓶颈是初始表示覆盖而非遗忘算法”的协议与因果分析论文；但需与已有 pre-training/base-task 研究明确区分。

### A02：随机类顺序可以代表真实难度，方法排名对顺序稳定

- **依赖者**：PyCIL `DataManager` 的随机重排；本地 8 篇论文及几乎全部标准 CIL benchmark。
- **为什么可能不成立**：类顺序控制新旧类语义相似度、任务间域差异和第一任务覆盖。少量随机 seed 不能代表这些结构因素。
- **失效现象**：同一方法跨顺序方差大于论文增益；方法排名反转；“cold-start 优势”只出现在特定类别排列。
- **诊断实验**：按语义相似度、预训练特征距离、视觉域和随机顺序分层采样；报告排序稳定性、排名相关系数、方差分解以及方法增益相对顺序效应的比例。
- **若证伪后的主线潜力**：`高`。可以发展为 EFCIL 协议可靠性或 benchmark robustness 论文，不需要新方法。

### A03：当前任务数据能够作为旧任务函数的有效代理

- **依赖者**：LwF 的 new-data distillation；SDC、LDC 的当前数据漂移估计；EFC 的当前任务约束；部分 PASS/SSRE 蒸馏流程。
- **为什么可能不成立**：新旧类别分布不重叠时，旧模型在新类输入上的响应只是 OOD 行为，未必约束旧类决策区域。
- **失效现象**：新数据上的 teacher-student 一致性很高，但隐藏旧数据上的输出、排序和特征严重变化；语义距离越远的旧类遗忘越大。
- **诊断实验**：逐任务比较新类数据上的蒸馏一致性与隐藏旧类数据上的真实功能保持；按新旧类语义距离分组，并使用无关图像或噪声作为蒸馏支持对照。
- **若证伪后的主线潜力**：`高`。可形成“new-data distillation 到底保留了什么”的机制分析；该问题比单一漂移补偿更广。

### A04：相邻任务特征空间之间存在可共享、平滑且可外推的变换

- **依赖者**：SDC 的局部平移；LDC 的 learned projector；ADC/APR 的跨模型迁移和 transfer matrix；FeTrIL 的类间平移。
- **为什么可能不成立**：深网更新可能产生类条件化、分段非线性或激活边界切换，同一映射不能同时描述旧类和新类。
- **失效现象**：当前类配对特征拟合误差低，但旧类 oracle 映射误差高；不同旧类需要相反变换；后期任务误差快速增长。
- **诊断实验**：使用隐藏旧数据分别拟合和评价平移、线性、局部及类条件 oracle 映射；比较 current-to-current 泛化误差与 current-to-old 泛化误差，而不据此设计新映射。
- **若证伪后的主线潜力**：`中高`。可形成漂移补偿适用边界论文，但与 IDEA-001、LDC、BiCyc 的重叠风险较高。

### A05：一个 class mean/prototype 足以代表旧类

- **依赖者**：PyCIL NME；PASS、FeTrIL、SimpleCIL、SSRE；SDC、EFC、ADC、LDC、IR、PRL、APR；大多数 prototype-centric EFCIL。
- **为什么可能不成立**：真实类分布可能多模态、长尾、非凸，类别判别由边界或少数子簇决定，均值可能落在低密度甚至错误类别区域。
- **失效现象**：即使使用当前模型重新计算 oracle prototype，NCM 仍远低于隐藏旧数据上的 linear probe、kNN 或多中心 oracle；细粒度类别和高类内差异类别尤其严重。
- **诊断实验**：每个任务比较 stale prototype、oracle current prototype、隐藏旧数据 linear probe、kNN 和多中心 oracle；用多模态度、类内散度和 prototype density 预测误差差距。
- **若证伪后的主线潜力**：`很高`。这是 prototype-centric EFCIL 的共同基础，系统证伪可重新解释大量结果；诊断本身即可构成主线。

### A06：均值和协方差构成足够准确的 Gaussian 类分布

- **依赖者**：IL2A；FeCAM、EFC、AdaGauss、APR；所有基于 Gaussian pseudo-feature 或 Mahalanobis 分类的方法。
- **为什么可能不成立**：深度特征常具有偏态、重尾、多模态和低维流形结构；高维小样本 covariance 估计不稳定。
- **失效现象**：协方差更新更准确但分类不改善；Gaussian pseudo-feature 可被轻易识别；Mahalanobis 置信度失准；细粒度数据集性能下降。
- **诊断实验**：对隐藏旧类特征做正态性、谱稳定性和 bootstrap 分析；比较 Gaussian held-out likelihood、真实/伪特征可分性及 oracle Mahalanobis 与非参数 oracle 的误差。
- **若证伪后的主线潜力**：`高`。可以形成“低阶统计是否足以支撑 EFCIL”的系统研究；避免直接跳到新的分布模型。

### A07：由 prototype/covariance 生成的 pseudo-feature 位于真实旧类流形上

- **依赖者**：PASS 的 prototype 加噪；IL2A 的统计校正；FeTrIL 的特征平移；EFC 的 Gaussian prototype rehearsal；AdaGauss、APR 及其他 pseudo-feature replay。
- **为什么可能不成立**：高维空间中围绕均值采样很容易落入训练分布外；匹配一二阶统计不保证局部密度、边界和语义结构正确。
- **失效现象**：分类器在伪特征上训练良好却在真实旧类上下降；真实与伪特征可被简单 probe 高精度区分；伪特征增加后收益饱和或反向。
- **诊断实验**：使用隐藏旧类特征，仅作评价，测量真实/伪特征二样本可分性、最近邻纯度、precision/recall、边界覆盖和分类器在两者之间的泛化差距。
- **若证伪后的主线潜力**：`很高`。pseudo-replay 是多条 EFCIL 路线的共同支柱，系统验证其“统计正确但流形错误”可能形成独立论文。

### A08：对抗扰动后的新类图像是有效的旧类代理，并能跨任务模型迁移

- **依赖者**：ADC、APR。
- **为什么可能不成立**：靠近旧 prototype 只是在旧模型特征中的优化结果，图像语义仍可能属于新类或完全离开自然图像流形；迁移性可能依赖攻击强度和架构。
- **失效现象**：旧空间距离很近但新空间不接近真实旧类；攻击参数轻微变化就导致漂移估计波动；跨 backbone 或长任务序列失效。
- **诊断实验**：比较 adversarial proxy 与隐藏真实旧类在旧/新模型中的距离、邻域类别、分类一致性和跨 backbone 迁移；分离“靠近 prototype”与“接近真实分布”。
- **若证伪后的主线潜力**：`中高`。可形成 adversarial pseudo-replay 的有效性边界研究，但覆盖方法较少。

### A09：旧模型在新类图像上的 soft target 含有可用旧知识

- **依赖者**：LwF；PyCIL 中 LwF、iCaRL、WA、BiC、PASS、SSRE 等蒸馏式实现；LDC/ADC 的训练底座。
- **为什么可能不成立**：旧模型对新类通常低置信或错误高置信，soft target 可能主要反映类先验和偶然纹理，而非旧类决策结构。
- **失效现象**：蒸馏损失下降但旧类保持不变或更差；随机 teacher、温度和新类组成对结果影响异常大；teacher 熵与保留效果无关。
- **诊断实验**：统计 teacher 在新数据上的熵、margin、类覆盖和稳定性，并与隐藏旧类 retention 关联；加入标签打乱、随机 teacher 或无关数据的诊断对照。
- **若证伪后的主线潜力**：`高`。LwF 假设历史悠久但在 cold-start EFCIL 中缺少系统检验。

### A10：旧类判别信息仍在当前 backbone 中，主要问题只是 classifier/prototype 失配

- **依赖者**：LDC 的核心分析；SDC、ADC 等 prototype correction；NCM/SimpleCIL；部分 classifier calibration 方法。
- **为什么可能不成立**：backbone 可能真正丢失旧类可分特征，均值校准无法恢复被压缩或混合的类内结构。
- **失效现象**：oracle prototype 仍表现差；隐藏旧类上的 linear probe、kNN 和类间 margin 同步下降；补偿只能短期改善。
- **诊断实验**：每个任务保存模型快照，用隐藏旧类数据计算 oracle NCM、linear probe、kNN、Fisher ratio、类内/类间散度和表示相似性，分解“表示丢失”与“统计失配”。
- **若证伪后的主线潜力**：`很高`。可直接挑战“not all forgetting is catastrophic”的普适性，并决定领域是否过度聚焦 prototype correction。

### A11：通用数据增强对所有类别都保持标签，并为未来类别扩展有效空间

- **依赖者**：IR 的 rotation/mixup/augmentation；PRL 的基础表示塑形；PASS、SSRE；PyCIL 固定 crop/flip 管线；APR 的 augmentation search。
- **为什么可能不成立**：旋转、裁剪、翻转在细粒度或方向敏感类别中可能改变判别属性；扩大增强轨迹不等于扩大未来可分空间。
- **失效现象**：CIFAR 有效但 CUB/ImageNet 子类失效；特定类别系统性受损；增强线性可分性提高但真实测试准确率下降。
- **诊断实验**：按类别测量增强前后 oracle label consistency、teacher consistency、特征位移和未来 linear probe；比较通用增强在 coarse 与 fine-grained 数据上的作用。
- **若证伪后的主线潜力**：`中高`。可形成 future-compatible representation 的假设审计，但数据增强研究本身较拥挤。

### A12：冻结或预训练表示对未来域已经足够

- **依赖者**：FeTrIL、FeCAM、SimpleCIL、ACIL、DS-AL；Aper、TagFex；多数 pretrained CIL 路线。
- **为什么可能不成立**：预训练域覆盖不均，第一任务训练又可能进一步偏向当前类别；“不遗忘”可能只是“不学习新表征”。
- **失效现象**：方法在语义接近预训练域时很强，在 domain-shift 或细粒度数据上明显落后；新类性能随任务推进下降但 forgetting 指标很好看。
- **诊断实验**：在增量训练前测量 frozen backbone 对每个未来任务的 linear probe；比较不同预训练来源、from-scratch 第一任务和域偏移下的 old/new accuracy。
- **若证伪后的主线潜力**：`中高`。问题重要，但近期已有 pre-training reality-check 类工作，新颖性需要额外审计。

### A13：任务边界已知，且每个任务有足量批量数据可统计

- **依赖者**：PyCIL 统一 task loop；SDC、LDC、ADC、APR；prototype/covariance 构建；所有按 task 更新旧模型的方法。
- **为什么可能不成立**：真实流中边界可能模糊，新类渐进出现，当前数据量不足以稳定估计 prototype、covariance 或映射。
- **失效现象**：缩小 batch 或延迟边界后性能骤降；相同样本按不同 chunk 划分得到不同结果；统计量在小批次下高方差。
- **诊断实验**：不改模型，仅改变同一数据流的 chunk 大小、边界噪声和每类样本量；报告结果对分块方式的敏感性和统计置信区间。
- **若证伪后的主线潜力**：`中`。可转为 task-free/online EFCIL 设定，但会扩大问题范围。

### A14：类别互斥、标签稳定，测试集只包含已见类别

- **依赖者**：PyCIL 类索引重映射；本地全部论文；NCM、softmax 和 prototype pool。
- **为什么可能不成立**：现实中类别可能重现、细化、合并或语义重叠，旧类数据也可能再次出现但没有旧标签。
- **失效现象**：重复类被当作新类学习；层级相近类别之间的错误被计为遗忘；prototype pool 出现冲突或重复。
- **诊断实验**：构造少量 recurring、overlapping 和 hierarchical class streams，观察标准指标和模型行为是否仍可解释。
- **若证伪后的主线潜力**：`中高`。现实意义强，但会从标准 EFCIL 转为更开放的类别演化问题。

### A15：类别与任务近似平衡，统一阈值和分类规则足够

- **依赖者**：PyCIL 的标准均衡切分；NCM、cosine classifier；PASS/IL2A/SSRE 的 pseudo-feature 采样；多数论文平均准确率。
- **为什么可能不成立**：真实数据常长尾，旧类统计来自历史全量而新类训练量不等；任务先验随时间变化。
- **失效现象**：task-recency bias 或 old-class bias 被错误解释为表示遗忘；方法排名随类频率改变；统一 prototype 规则失准。
- **诊断实验**：固定类别与顺序，只改变每类样本数、任务规模和测试先验；分解表示准确率、校准和 prior-shift 影响。
- **若证伪后的主线潜力**：`中`。已有 long-tailed CIL 文献，需证明 EFCIL 中存在不同机制。

### A16：归一化后的 Euclidean/cosine 几何跨任务保持可比

- **依赖者**：PyCIL NME；cosine heads；PASS、SSRE、FeTrIL、SimpleCIL；SDC/LDC/ADC；IR、PRL。
- **为什么可能不成立**：特征可能各向异性、出现 norm drift、hubness 和距离集中；归一化会丢失有用尺度信息。
- **失效现象**：角度 margin 看似稳定但类别错误增加；少数 prototype 成为 hub；raw 与 normalized classifier 排名反转。
- **诊断实验**：逐任务测量 norm 分布、各向异性、hubness、距离集中、类内/类间角度；比较 raw、normalized、whitened oracle 几何，仅用于分析。
- **若证伪后的主线潜力**：`高`。NCM/cosine 是 EFCIL 的基础设施，系统证伪具有广泛影响。

### A17：逐任务估计和修正可以稳定组合，长期误差不会路径依赖

- **依赖者**：SDC、LDC、ADC、APR 的递归 prototype/statistics 更新；所有只保留上一任务模型和旧统计的方法。
- **为什么可能不成立**：每步小偏差会累积；映射组合不满足结合性；同一数据按不同任务粒度划分可能产生不同最终统计。
- **失效现象**：后期任务误差超线性增长；直接 old-to-current oracle 与 chained estimate 差距扩大；任务拆分越细越差。
- **诊断实验**：保持类别总量和训练样本不变，改变任务粒度与分组路径；比较直接 oracle 漂移、逐步估计漂移、循环误差和最终 prototype 路径差异。
- **若证伪后的主线潜力**：`高`。长期组合性是漂移补偿论文常被平均准确率掩盖的基础假设；但需考虑 BiCyc 的相关工作。

### A18：平均准确率和标准 forgetting 能准确反映研究机制

- **依赖者**：PyCIL `trainer.py`；本地全部论文的 `A_inc`、`A_last` 或 forgetting 报告。
- **为什么可能不成立**：平均值混合旧类表示损失、新类学习不足、分类器校准和任务先验；少数类别完全崩溃可被平均值隐藏。
- **失效现象**：两个方法平均准确率相近，但旧/新平衡、最差类、校准和表示可恢复性完全不同；方法排名随指标改变。
- **诊断实验**：同时报告 per-class trajectory、old/new accuracy、worst-group、balanced accuracy、校准、oracle head 和表示 probe；对指标做误差来源分解。
- **若证伪后的主线潜力**：`高`。可形成 EFCIL evaluation paper，且会改变现有结论解释。

### A19：保存 prototype、covariance、旧模型等仍然具有明确的隐私和存储优势

- **依赖者**：所有 exemplar-free 方法；尤其 EFC、FeCAM、AdaGauss、APR、ACIL/DS-AL 和保存旧网络的蒸馏方法。
- **为什么可能不成立**：高维统计量和模型参数可能泄露成员、属性或可重建信息；完整 covariance 或模型副本的字节数可能超过小型 exemplar memory。
- **失效现象**：在 byte-matched 比较中“无样例”方法不再省内存；prototype/statistics 支持成员推断或属性泄露；隐私论证只停留在不存图像。
- **诊断实验**：统一计算长期存储、峰值显存和训练算力；进行 byte-matched exemplar 对照，并对存储统计做标准 membership/property/reconstruction 风险审计。
- **若证伪后的主线潜力**：`很高`。可形成资源与隐私 reality-check 论文，不依赖新模型；需要严格安全实验设计。

### A20：论文超参数和训练预算能跨任务序列、数据集和方法公平迁移

- **依赖者**：PyCIL 中大量 Python 硬编码超参数；本地论文使用固定增强、学习率、first-task epoch 和方法特定验证协议。
- **为什么可能不成立**：超参数可能针对固定类顺序、任务数或测试集调优；不同方法使用不同训练轮次、预训练和额外计算。
- **失效现象**：官方数字无法在统一预算下复现；换顺序后增益消失；方法排名主要由训练预算或调参自由度决定。
- **诊断实验**：建立 held-out class-order/dataset 的 nested validation；在 matched epoch、FLOPs、预训练和存储预算下复评，并报告超参数敏感性。
- **若证伪后的主线潜力**：`高`。可以形成 EFCIL reproducibility/fair-comparison 论文，并直接解释 PyCIL 现有配置风险。

## 2026-06-27 严格筛选：只保留两个活跃研究候选

本轮筛选新增 2024--2026 近期工作审计，重点覆盖 cold-start EFCIL 与近期顶会/强相关论文：

- EFC / EFC++：明确把 small first task / cold start 作为问题设定，并围绕特征漂移、重要方向约束和 prototype re-balancing 展开；
- ADC / APR：用当前图像的对抗代理靠近旧类 prototype，并估计均值/协方差漂移；
- LDC / BiCyc：围绕 prototype drift、projection bias、cycle inconsistency 和长期漂移补偿展开；
- AdaGauss：指出 covariance drift 与 dimensional collapse 会造成 task-recency bias；
- CIRCLE：进一步质疑 trained-backbone 与 first-task-biased frozen-backbone 的 cold-start 代价，提出固定随机特征和 streaming head 的强对照。

结论：近期工作已经把“cold start 使第一任务 backbone 不足”作为显式问题。`A01` 仍有诊断意义，但若只证明 first-task coverage 影响结果，新颖性不足。它应降级为所有实验必须控制和分层报告的协议变量，而不是当前主线。

评分采用 1--5 分，分数越高越好；“实验成本”表示低成本和可执行性。

| ID | 假设 | 新颖性 | 可证伪性 | 实验成本 | 区分度 | 方法潜力 | 总分 | 决策 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| A01 | 第一任务表示覆盖足以支撑未来类别 | 2 | 5 | 5 | 2 | 3 | 17 | 降级为控制变量 |
| A02 | 随机类顺序代表真实难度 | 3 | 5 | 4 | 4 | 2 | 18 | 备选评测问题 |
| A03 | 当前任务数据可代理旧任务函数 | 4 | 4 | 4 | 4 | 4 | 20 | **保留候选** |
| A04 | 相邻任务存在可外推共享变换 | 3 | 4 | 3 | 3 | 4 | 17 | 被 LDC/BiCyc 挤压 |
| A05 | 单 prototype 足以代表旧类 | 4 | 5 | 4 | 4 | 5 | 22 | **保留候选** |
| A06 | 均值和协方差足以描述类分布 | 3 | 4 | 3 | 3 | 4 | 17 | 并入 A05/A07 支撑诊断 |
| A07 | pseudo-feature 位于真实旧类流形 | 4 | 4 | 2 | 4 | 5 | 19 | 支撑性诊断，暂不作主线 |
| A08 | 对抗新图像是有效旧类代理 | 3 | 4 | 2 | 3 | 3 | 15 | 覆盖面过窄 |
| A09 | 新图像 soft target 含有旧知识 | 3 | 4 | 4 | 3 | 3 | 17 | 并入 A03 |
| A10 | 旧类判别信息仍在当前 backbone | 3 | 4 | 3 | 3 | 4 | 17 | 被 LDC 主张覆盖，作为 A05 对照 |
| A11 | 通用增强保持标签并扩展未来空间 | 2 | 4 | 3 | 2 | 3 | 14 | 拥挤且偏增强领域 |
| A12 | 冻结/预训练表示足够 | 2 | 4 | 4 | 2 | 3 | 15 | 与 pretrained CIL 重叠高 |
| A13 | 任务边界已知且数据量足够统计 | 3 | 4 | 3 | 3 | 2 | 15 | 会偏离标准 EFCIL |
| A14 | 类别互斥、标签稳定 | 3 | 3 | 2 | 4 | 2 | 14 | 设定扩张过大 |
| A15 | 类别/任务平衡且统一分类规则足够 | 2 | 4 | 4 | 2 | 2 | 14 | long-tailed CIL 重叠高 |
| A16 | cosine/Euclidean 几何跨任务可比 | 3 | 4 | 3 | 3 | 4 | 17 | 可作为 A05 的几何分析 |
| A17 | 逐任务修正可稳定组合 | 3 | 4 | 3 | 2 | 4 | 16 | BiCyc 已直接切入 |
| A18 | 平均准确率/forgetting 反映机制 | 3 | 5 | 4 | 4 | 1 | 17 | 评测规范，不作方法主线 |
| A19 | 无样例统计仍有资源/隐私优势 | 4 | 4 | 3 | 5 | 1 | 17 | 支撑性贡献，不作主线 |
| A20 | 超参和训练预算可公平迁移 | 3 | 4 | 2 | 4 | 2 | 15 | 复现/公平性工作，成本偏高 |

### 保留候选 1：A05 单 prototype 是否足以代表旧类

- **保留原因**：它是 prototype-centric EFCIL 的共同接口，直接影响 SDC、LDC、ADC、BiCyc、PASS、FeTrIL、SimpleCIL、EFC/EFC++、AdaGauss、APR 等路线。
- **与近期工作的区分**：近期工作大多继续优化 prototype 的漂移、协方差或回放方式；A05 先问“即使 oracle prototype 可得，单均值是否仍是瓶颈”。这不是新的漂移补偿方法，而是对共同表示假设的证伪。
- **最低成立条件**：oracle current prototype 仍显著落后 hidden-old linear probe、kNN 或多中心 oracle；差距能被类内多模态、fine-grained 属性、hubness 或边界复杂度稳定解释。
- **失败条件**：oracle current prototype 与更强 oracle 表示差距很小，或差距只出现在少量类别/单一数据集；则 A05 不足以作为论文主线。

### 保留候选 2：A03 当前任务数据能否代理旧任务函数

- **保留原因**：它覆盖 LwF 蒸馏、当前数据漂移估计、EFC 约束、LDC projector 训练，以及 ADC/APR 试图构造旧类代理的动机。
- **与近期工作的区分**：ADC/APR 说明“普通当前数据不足”并提出代理；A03 的主问题不是再提出代理，而是系统回答当前数据上的一致性到底能否预测隐藏旧类函数保持，以及 adversarial proxy 是否真的解决了这个代理缺口。
- **最低成立条件**：新类数据上的 teacher-student 一致性、漂移拟合误差或代理距离，不能可靠预测隐藏旧类上的功能保持；该失效随新旧语义距离、任务粒度或 cold-start 程度稳定变化。
- **失败条件**：当前数据指标与隐藏旧类保持高度一致，且简单语义距离/密度控制后仍稳定；则该假设不能形成独立主线。

### 被降级但仍必须控制的假设

- `A01`：作为 cold-start 协议变量保留。必须在所有诊断中分层报告 first-task coverage、first-task 类组成和未来类 frozen probe，但不再作为主线。
- `A07`：作为 A05 的支撑诊断保留。若 A05 成立，再检查 pseudo-feature 是真实流形近似还是仅起分类器正则化作用；当前不单独立项，原因是实现成本较高且与 A05/A06 强耦合。

## 历史记录：上一轮最值得继续研究的三个假设

以下为 2026-06-25 Assumption Mining 的历史结论，已被 2026-06-27 严格筛选替代；保留用于追溯。

### Top 1：A01 第一任务表示覆盖是否决定了大部分 EFCIL 上限

- 覆盖方法最广，同时解释 cold-start/warm-start 巨大差异。
- 诊断成本低：不需要新方法，只需第一任务后冻结评测未来类别。
- 如果第一任务 coverage 能比算法名称更好地预测最终结果，现有比较协议需要重估。
- 风险：pre-training 与 base-task 影响已有相关研究，必须把“from-scratch 第一任务语义覆盖和方法排名稳定性”界定清楚。

### Top 2：A05 单 prototype 是否真的是旧类的充分表示

- prototype 是 SDC、LDC、ADC、IR、PRL、PASS、FeTrIL、SimpleCIL 等不同路线的共同接口。
- 可以用 oracle current prototype、linear probe、kNN 和多模态度直接证伪，不依赖任何新模块。
- 若 oracle prototype 本身不足，继续优化 prototype 漂移估计只能改善次要误差。
- 该问题对 coarse-grained 与 fine-grained 数据的差异尤其可能产生稳定结论。

### Top 3：A07 pseudo-feature 是否“统计正确但流形错误”

- 覆盖 PASS、IL2A、FeTrIL、EFC、AdaGauss、APR 等多条强路线。
- 现有论文常验证最终准确率或一二阶统计，却较少直接验证 pseudo-feature 与真实旧类流形的一致性。
- 诊断可以明确区分“伪特征有用”与“伪特征真实”，避免把分类器正则化效果误写成旧类重建。
- 若证伪，可形成跨方法的机制分析和评测标准，而不必立即提出替代生成机制。

## 本轮筛选结论

- 当前没有选定新的算法方向。
- IDEA-001 保持 `暂缓（Weak Reject）`，本轮不继续优化。
- 下一阶段只允许为 A01、A05、A07 固化诊断协议和失败标准；在诊断完成前，不进入方法设计。

### IDEA-002：低秩协方差漂移的可靠迁移

- 状态：`暂缓（等待 A06 诊断）`
- 研究问题：均值 transport 之外，旧类 covariance 的哪些低秩方向可以安全更新？
- 动机：EFC 明确指出 covariance drift 仍是开放问题；AdaGauss 与 APR 已表明 covariance adaptation 和 dimensional collapse 很重要。
- 主要风险：AdaGauss 和 APR 已直接覆盖 covariance 迁移，单纯增加低秩分解新颖性不足。
- 准入条件：只有当 A06 的独立诊断证明 Gaussian/covariance 近似既是主要误差来源、又存在尚未被 AdaGauss/APR 覆盖的问题时，才重新评估；当前不设计实现。

### IDEA-003：面向未来类别的表示空间预留

- 状态：`暂缓`
- 研究问题：能否在基础阶段为未知类别主动预留可分空间？
- 已有覆盖：IR 通过增强扩大空间；PRL 通过 intra-class concentration 和 inter-class separation 预留空间；DCNet 使用超球正交布局。
- 开放点：未知未来类别数量和分布时如何合理分配空间。
- 暂缓原因：方向已经拥挤，且容易退化为新的度量损失或正交正则，与项目“禁止堆 Loss”冲突。

### IDEA-004：EFCIL 的真实资源与隐私预算

- 状态：`候选（支撑性贡献）`
- 研究问题：不同“无样例”方法实际存储的旧模型、prototype、covariance、索引、增强策略和生成器参数是否公平？
- 动机：APR 显示 covariance 可占约百 MB；解析方法和生成方法也有不同隐性预算。
- 对应假设：A19。
- 用途：作为主方法的评测规范和附加贡献，不单独作为当前主论文问题。
- 验收：统一报告训练内存、长期存储、额外算力、是否需要 task boundary、是否存在数据泄露风险。

## 想法准入标准

进入编码前必须同时满足：

1. 有一句可证伪的核心假设；
2. 与最接近工作的差异可以用数学对象和实验设计表达；
3. 有不依赖完整训练的低成本诊断实验；
4. 新模块可关闭，关闭后严格回到 baseline；
5. 已定义失败条件，而不是只定义成功指标；
6. 已明确旧信息存储字节数和新增计算成本。

## 淘汰记录

当前无正式淘汰方向。IDEA-002 和 IDEA-003 暂缓，不删除。
