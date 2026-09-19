# 辞达十维文体参数空间（Style Control Space）

文体不是预设（Preset），是连续空间。任何一篇产出都可以沿十个维度定位；
参数映射的是**一组语言行为的概率与策略**，不是关键词替换器。

## 十个维度（均 1–10）

| 维度 | 低 | 高 |
|---|---|---|
| Formality 正式度 | 朋友聊天 | 公文/典礼 |
| Orality 口语感 | 纯书面 | 现场说话感 |
| Information Density 信息密度 | 闲笔多 | 每句承重 |
| Logical Explicitness 逻辑显性 | 逻辑隐含 | 推理全显式 |
| Intimacy 亲近感 | 公共距离 | 促膝而谈 |
| Rhetorical Density 修辞密度 | 零装饰 | 处处讲究 |
| Judgment Strength 判断力度 | 只陈述 | 强判断、敢取舍 |
| Rhythmic Variation 节奏变化 | 均匀 | 长短强烈对比 |
| Narrative Presence 叙事存在 | 纯论述 | 场景故事贯穿 |
| Reader Interaction 读者对话感 | 独白 | 高频预期与回应 |

## 参数命名空间（四类，不得混用）

平台适配、文本诊断和个人风格校准会用到不同类型的参数。按下表区分，避免把表达机制、
文体倾向和平台要求混为一谈。

| 类别 | 唯一权威 | 例 |
|---|---|---|
| ① 十维语言参数 | 上表的 10 个英文键 | `orality`、`rhythmic_variation` |
| ② 机制节点名 | `knowledge/mechanisms/<name>.md` 的文件名 | `compression`、`topic_return` |
| ③ 呈现层／平台要求参数 | 下表登记；**只调呈现层**，逻辑、判断、证据不打折 | `entry_speed`、`block_length` |
| ④ 诊断动作名 | `workflows/diagnose_text.md` 的 Lower／Raise 动作表 | `concreteness`、`natural transition` |

**呈现层参数登记表**（平台适配只从十维参数与本表取值）：

| 参数 | 含义 | 平台侧现行用法 |
|---|---|---|
| `opening` | 开头切入位置：多少字内建立读者与问题的关系 | 微信：前 60 字；通用：前 100 字 |
| `entry_speed` | 切入速度：第一句即主题/结果，还是留铺垫 | 微博：最快；小红书：第一句即主题或结果 |
| `block_length` | 块长：段落与视觉块的大小 | 小红书：短块——视觉上要轻 |
| `paragraph_length` | 段落长度（以句计） | 微信：2–3 句为主；通用：2–4 句、最长 6 句 |
| `subheading` | 小标题密度与写法（导航 + 扫读钩子） | 微信：每 300–500 字一个；通用：800 字以上 |
| `structure` | 结构层数上限 | 微博：≤ 2 层 |
| `signposting` | 过渡与导航标记的显性度 | 口播：比文章更显性（"先说结论"合法） |
| `sentence_length` | 单句上限与换气点 | 口播：以一口气为上限，顿号处必须能换气 |
| `pronounceability` | 可发音性检查（拗口组合） | 口播：连续仄声、绕口辅音堆叠要改 |
| `listener_memory` | 关键信息重复（听众不能倒带） | 口播：关键信息重复出现 |
| `recap` | 定期收拢（"我们说到哪了"） | 播客：每 10–15 分钟一个 30 秒小结 |
| `concreteness` | 具体性：抽象处补数字、场景、动作 | 小红书：显著上调 |
| `evidence` | 论断的支撑要求（**是底线，不是"偏移"**） | 知乎：数据、出处、经验须注明 |

描述十维文体时使用表①中的英文键；引用表达机制时使用对应节点名；平台要求按表③设置。

## 参数 → 行为映射（示例）

参数不是机械数字生成器。例如较高 Orality（6–7）意味着：

```
更自然的话题转换     更多读者预期回应      允许短句
允许省略式节奏       适量话语标记          更低名词化
```

而**不是**"每段加一个'其实'"。

## 默认 Profile：Modern Chinese High-Quality Conversational

```yaml
formality: 4–5
orality: 6–7
information_density: 6–8
logical_explicitness: 8
intimacy: 6–7
rhetorical_density: 4–5
judgment_strength: 6–8
rhythmic_variation: 7
narrative_presence: context-dependent
reader_interaction: 6
```

**默认 Profile 是起点，不是定论**：按平台、体裁和个人偏好调整参数。短文本与长文本的
需要不同，不要把某一种场景的偏好套到所有任务中。

## 修辞密度曲线（Rhetorical Density Curve）

任何单篇内部不许"全程一个强度"。标准曲线：

```
普通表达 → 解释 → 普通表达 → 具体例子 → Rhetorical Peak → 回落
```

- 峰值数量受 Rhetorical Density 与文本长度约束（见
  `knowledge/mechanisms/rhetorical_peak.md`）；
- 平处要"高质量的平"：平实≠敷衍，平处托峰处。

## 媒介 × 语域速查

| 媒介 | Formality | Orality | 备注 |
|---|---|---|---|
| 学术文章 | 8–9 | 2–3 | 修辞密度极低 |
| 政府/公文 | 9 | 1–2 | 程式成分为体例要求 |
| 完全口语 | 2 | 9 | 允许碎，不允许假 |
| 普通自媒体 | 4–6 | 6–8 | 依平台微调 |
| **辞达目标文体** | **4–5** | **6–7** | 见默认 Profile |
| 播客稿 | 3–4 | 8 | 回检密度高 |
| 视频口播 | 3–5 | 8–9 | 可发音性优先 |

## 校准

- 平台级：见 `platforms/<平台>/README.md` 的参数偏移；
- 个人级：见 `workflows/style_calibration.md`（Personal Style Profile）；
- 校准时区分稳定偏好与场景需要；遇到冲突时保留边界，并按当前任务调整。
