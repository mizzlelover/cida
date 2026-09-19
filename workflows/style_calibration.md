# Calibrate：个人风格校准（style_calibration）

用户说"学我的风格""按我喜欢的这种感觉写"时进入本流程。

## 核心原则

**学参数，不抄句子。** 从用户提供的真实文本中抽取高维风格特征，形成
Personal Style Profile；禁止复制原文的固定句式、口头禅与人格化指纹。

## 知识检索契约

风格校准只在 `STYLE_SYSTEM.md` 的十维空间内进行；结构动作从 `knowledge/mechanisms/GRAPH.md` 取节点名，反模式从 `knowledge/anti_patterns/README.md` 索引取边界。每条参数判断必须能回到样本清单或反例检查（反例要点见本文件 §5 与 `knowledge/anti_patterns/README.md` 索引），主持人与在世作者样本只用于高层机制和语境边界，不形成可复制的个人 Style Preset。

## 流程

### 1. 采样

请用户提供 3–10 篇自己满意的真实文本（或明确喜欢的他人文本）。
单篇样本只能形成假说；多样本交叉才能形成 Profile。

### 2. 特征抽取

对每篇样本，沿十维参数打分并摘录证据（`STYLE_SYSTEM.md`）：

```yaml
formality:             # 正式度 1–10
orality:               # 口语感
information_density:   # 信息密度
logical_explicitness:  # 逻辑显性度
intimacy:              # 亲近感
rhetorical_density:    # 修辞密度
judgment_strength:     # 判断力度
rhythmic_variation:    # 节奏变化
narrative_presence:    # 故事/场景存在感
reader_interaction:    # 读者对话感
```

另抽取结构习惯：典型开头方式、段落长度偏好、小标题使用、结尾方式、
比喻来源域（科技/生活/历史……）、标点习惯。

### 3. 形成 Personal Style Profile

```yaml
profile_name:
source_samples:        # 样本清单
parameters:            # 十维中位数 + 浮动区间
signature_moves:       # 该作者标志性的表达动作（机制级，不是句子级）
  - 例：先讲一个小场景再切入正题（Story Entry）
  - 例：段落末尾用短句落判断（Closure）
boundary_notes:        # 哪些特征是语境依赖的，不应泛化
created_at:
```

### 4. 应用与校验

- 之后为该用户写作时，以 Profile 为默认 Style Profile；
- 用户经验一律登记进实践者假说登记处（随开发仓分发），标注 status；
- 每次使用后邀请用户反馈"像不像"，据此修正参数（校准是迭代的）。

### 5. 边界

- 如果样本是在世作者的文字：只抽取**高层属性**（如"温和、总结性强、修辞克制"），
  输出时不声称"某某风格"（见 SKILL.md §2 不模仿活人）；
- 如果用户自己的样本风格与目标平台冲突（如论文式写法发小红书），
  明确告知取舍，由用户决定偏向哪边；
- Profile 是起点不是枷锁：参数允许按任务浮动，文档化浮动理由。

### 6. 评测迭代（研究侧）

> 本节步骤在**开发仓**执行（依赖评测档案与语料，不随发布包分发）；在发布包内使用本 Skill 时无需运行。

- 修改默认 Profile 后运行 `python scripts/calibrate_style_profile.py`，读取实际质量跑与
  Register Span 记录，把迭代记录写入评测档案 `evals/style_calibration/`（随开发仓分发）；
- 先区分适用阈值内的长文本与短控制，不能用负压缩率驱动全局参数；
- 六项 Preservation 任一为 `REVIEW` 时不得把本轮结果写成校准通过；Pairwise、角色面板和
  自动统计只作开发预筛，外部人工评审仍单独登记。
