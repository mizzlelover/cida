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

**注意**：以上数字是初始假设（Practitioner Hypothesis 级别），
需经真实评测与用户校准持续修正，不得视作最终真理。

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
- 每次校准保留依据与证据，登记到 `knowledge/practitioner_hypotheses/`。
