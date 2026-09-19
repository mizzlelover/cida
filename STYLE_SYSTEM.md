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

`platforms/*/README.md` 的参数块与 `workflows/diagnose_text.md` 的动作表会用到四类名字，
**必须各归其类**：名字混用会让读者无法判断它是什么、基线在哪。
（2026-09-16 核出 14 个"被当作参数使用、却不在任何命名空间内"的名字，已登记或改名，见下。）

| 类别 | 唯一权威 | 例 |
|---|---|---|
| ① 十维语言参数 | 上表的 10 个英文键（与 `schemas/style_profile.yaml` 逐字一致） | `orality`、`rhythmic_variation` |
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
| `preparedness` | **语料标注字段**（`schemas/corpus_item.yaml`），不是语言参数 | 播客：`semi_prepared`——有大纲、留即兴空间 |

**引用纪律**：十维参数一律用上表①的英文键，不用近义词（"节奏"写 `rhythmic_variation`，
不写 `rhythm`）；引用机制写②的机制名并注明"机制"；呈现层参数只在③内取值。
`check_source_trace.py` 的"参数命名空间"闸门按本表校验（含十维表与 `style_profile.yaml` 的一致性）。

**已知的同名跨类（以所在表格归类，不得跨表推断）**：`concreteness` 既是③呈现层参数
（小红书参数块）又是④诊断动作名（`workflows/diagnose_text.md` Raise 表）——两处语义一致（补具体）；
`rhythm` 既是②机制节点名（`knowledge/mechanisms/rhythm.md`）又出现在④的动作表里——
凡写参数一律用 `rhythmic_variation`，`rhythm` 只在引用机制时使用。

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

**校准状态（2026-09-10）**：以上数字已经过 10 个项目自有高模板控制的实际质量跑、
同题多语域核验和 Pairwise 本地预筛首轮迭代。由于其中 9 个控制文本短于压缩适用阈值，
全局数值暂不漂移；本轮把六项 Preservation、短文本适用性和人工评审边界固化为行为闸门，
仍标记为 `contextual`，不得视作跨体裁最终真理。本轮校准的可复核记录存于评测档案（`evals/style_calibration/`，随开发仓分发）。

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
- 每次校准保留依据与证据，登记到实践者假说登记处（随开发仓分发）。

## 语料校准记录（corpus-derived）

> **档案位置**：本节所引语料档案（统计原始数据、逐条阅读记录）随开发仓分发，不在发布包内；
> 发布包保留的是校准**结论与限定**。
>
> 第一批真实语料统计（2026-09-08，n=82 期阮一峰周刊，2018-04 ~ 2026-08，
> 每隔 5 期抽样，机器特征 state=READ）。
> **体裁限定：编辑体科技周刊；仅校准书面解释体一隅，不外推对话体。**

| 观察 | 数据 | 对参数空间的含义 |
|---|---|---|
| 平均句长中位 38.2 字 | p25=36.7 / p75=39.6 | 高 Information Density 不等于短句；列举与铺陈允许长句存在 |
| 句长峰值中位 112 字 | p75=131 | Rhythmic Variation 体现在段内长短对比，而非全文中句化 |
| 话语标记密度中位 1.78/千字 | p25=1.49 / p75=2.47 | 功能标记"低但不归零"；Logical Explicitness 高≠连接词堆砌 |
| "但是"覆盖率 82/82 期 | "更重要的是"仅 4/82 | 转折标记是刚需；峰值标记是稀缺资源，滥用即模板 |
| 问句均值 7.0 个/期 | — | Reader Interaction 可通过真实问句实现，不靠"你可能会问"模板 |

局限：单作者、单体裁、机器特征未经人工精读复核（Quantitative ≠ Quality）；
跨作者/跨体裁验证见研究侧语料覆盖率矩阵（随开发仓分发）。

### 准备型公共表达的 contextual 校准（2026-09-10）

新增 9 条官方完整演讲的逐条阅读记录存于语料标注档案（随开发仓分发）。样本反复出现“共同情境 → 判断分解 →
行动单元”的组织关系，提示高信息密度文本可用有限结构标记降低听觉跟随成本；但样本均为
外交、经济或公共议题的准备型讲话，当前只登记为
研究侧假说登记档案中 `prepared_speech_structure` 的
`contextual` 假说，不调整默认 Profile，也不把典礼式排比、国家立场或动员结尾迁移到一般写作。
