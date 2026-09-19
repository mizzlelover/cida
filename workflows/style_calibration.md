# Calibrate：个人风格校准（style_calibration）

用户说"学我的风格""按我喜欢的这种感觉写"时进入本流程。

## 核心原则

**学参数，不抄句子。** 从用户提供的真实文本中抽取高维风格特征，形成
Personal Style Profile；禁止复制原文的固定句式、口头禅与人格化指纹。

## 参考文件

使用 `STYLE_SYSTEM.md` 的十维空间描述文体；需要调整结构时，再按任务查阅相关机制节点和平台说明。

## 流程

### 1. 采样

请用户提供几篇自己满意的真实文本，或指出希望接近的高层表达特点。
样本越丰富，越容易区分稳定偏好与场景差异；材料有限时先形成可调整的初稿。

### 2. 特征抽取

结合样本，按十维参数概括表达倾向（`STYLE_SYSTEM.md`）：

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
parameters:            # 十维文体倾向与适用范围
signature_moves:       # 可复用的表达动作，不复制原句
  - 例：先讲一个小场景再切入正题（Story Entry）
  - 例：段落末尾用短句落判断（Closure）
boundary_notes:        # 哪些特征依赖具体语境
```

### 4. 应用与校验

- 之后为该用户写作时，以 Profile 为默认 Style Profile；
- 将 Profile 作为当前偏好的参考，而不是固定模板；
- 使用后可请用户指出偏差，再按反馈调整参数。

### 5. 边界

- 如果样本是在世作者的文字：只抽取**高层属性**（如"温和、总结性强、修辞克制"），
  输出时不声称"某某风格"（见 SKILL.md §2 不模仿活人）；
- 如果用户自己的样本风格与目标平台冲突（如论文式写法发小红书），
  明确告知取舍，由用户决定偏向哪边；
- Profile 是起点不是枷锁：参数允许按任务浮动，并向用户说明重要取舍。
