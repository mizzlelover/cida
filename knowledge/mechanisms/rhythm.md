# Rhythm · 节奏引擎

```yaml
id: mech.rhythm
name: 节奏
function: 让句子的长短呼吸由意义推动，而不是随机分布
confidence: validated
```

## definition

现代中文的节奏单位是句子的长短、停顿的深浅、段落的大小。节奏的目的不是
"模拟人类的随机性"，而是**让形式与意义同频**：重点砸实，铺陈展开，转折换气。

## mechanism 工具库

```
短句       判断、落锤、峰值。短句有重量。
中句       叙述与解释的主力。
长句       铺陈、列举、营造语势——但必须一口气能读完。
单句段     强调、转折、收束。一段一句，一行千钧，慎用。
分号       并列结构内的浅停顿。
破折号     插入、递进、语气转向。
冒号       预告——后面有东西要来。
问句       真实疑问、修辞问、转场问——区分使用，禁止滥用（Fake Hook）。
长短交替   由意义密度决定：难的地方慢（短），熟的地方快（长）。
```

## 诊断方法

重写时做一次"朗读测试"（默读即可）：

- 哪里喘不上气？→ 长句拆；
- 哪里拖沓犯困？→ 合并或删；
- 重点句是否被埋在一堆同样长度的句子里？→ 让它变短、独立；
- 全文句长是否均匀？→ 均匀不是节奏，均匀是平。

**禁止：通过随机打乱句长来模拟人类。** 节奏必须由意义推动。

## 统计的态度

句长分布等统计特征只能辅助诊断（`scripts/` 提供分析工具），
**不得定义好坏**。"优秀文本平均句长15字"推不出"所有句子必须15字"——
所有统计都必须结合 Function + Context 解读（Quantitative ≠ Quality）。

## 语料校准（corpus-derived）

> 来源：`corpus/metadata/ruanyifeng_weekly_features.json`，n=82 期阮一峰周刊
> （2018-04 ~ 2026-08，每隔 5 期抽样，state=READ 机器特征）。
> **体裁限定：编辑体科技周刊（含大量列举项），不可外推到对话体/口播体。**

- 篇均字符中位数 ≈ 5981；平均句长中位数 38.2 字（p25=36.7，p75=39.6）；
- 句长峰值中位数 112 字（p75=131）——长句承担列举与铺陈功能，并未被消灭；
- 印证本页立场：节奏的好坏不在"平均句长短"，而在长短是否由意义驱动。
  该作者句长分布高度稳定（均值集中于 37–40 字），靠的是**段内长短交替**，
  不是全文中句化。

## realizations

- **written**：视觉段落也是节奏——短段落给读者换气；
- **spoken**：口播稿的节奏要落到**可发音性**：一口气说完一句，顿号处能换气
  （见 `platforms/video_script/`）；
- **formal**：长句容忍度更高，但超长依存仍要拆；
- **informal**：允许更碎的短句，但不允许聊天记录式碎片化。

## boundary_conditions

句长目标必须服从功能、媒介和读者；数据表、法条和诗性文本不能用同一节奏标准。

## overuse_risk

为了制造节奏而随机拆句、堆短句或强行单句成段，会损失逻辑和自然呼吸。

## repair_strategy

先标出判断、证据和转折，再让短句承担落点、长句承担铺陈；朗读后只修复真正的呼吸障碍。

## related_nodes

`compression.md`、`rhetorical_peak.md`、`../anti_patterns/structural_monotony.md`

## sources

- 现代汉语句式的节奏研究（`knowledge/rhetoric/`）
- 王希杰《修辞学通论》（句式的选择与调整）
- 余光中《怎样改进英式中文》（中文弹性句法 vs 西式长句）
- 和菜头、阮一峰文本的句长抽样对比（`corpus/blogs/`，分析用）
- 刘勰《文心雕龙·情采》《隐秀》（`src.rhetoric.liu-xie-wenxin`，key_chapters；内容先于装饰，峰值稀缺，古典命题不直接外推）
- Aristotle《修辞学》第三卷相关章节（`src.intl.aristotle-rhetoric`，key_chapters；清楚、合宜、自然且有节制的散文节奏）
- Stivers 等的跨文化话轮研究与 Gumperz 的语境线索研究（`src.intl.stivers-turntaking`、`src.intl.gumperz-contextualization`，review_only）；只作“节奏依受众和语境而变”的边界证据，不设统一停顿秒数。
- Biber/Conrad 的语域比较与 Tannen 的会话风格页（`src.intl.biber-register`、`src.intl.tannen-conversational`，review_only）提醒节奏参数须随体裁、互动关系和受众迁移，不把英语语域统计当中文目标值。
- 阮一峰《站在未来的十字路口》与陈皓《感染新冠的经历》精读样本
  （`corpus/annotations/ruanyifeng-essay-survivor-preface-20260910.md`、
  `corpus/annotations/coolshell-22341-20260910.md`，均 ANNOTATED）

- **可追溯性补写（2026-09-16）**：句长抽样与精读样本此前只写 `corpus/blogs/`，**无显式 `corpus_id`**。现分两层写清：①**精读层**（承担机制结论）——`corpus.blogs.ruanyifeng-essay-survivor-preface`、`corpus.blogs.coolshell-22341`；②**统计层**（承担数值基线）——`corpus/blogs/` 下的阮一峰周刊批（ruanyifeng_weekly_*，n=82）、陈皓批（coolshell_*，n=56）、和菜头批（hecaitou_*，特征档 `corpus/metadata/hecaitou_features.json`）与 `corpus/metadata/mindhacks_features.json`。对照文档：`corpus/contrast/ruanyifeng_vs_coolshell_20260908.md`、`corpus/contrast/narrative_vs_argument_20260910.md`。**口径声明**：数值基线是**批量统计口径**（条目多为 `READ` 级，**不逐条列 corpus_id**），机制结论只由精读层两条承担。

## 跨来源验证（§121）

- 状态：`validated`（2026-09-10 登记）。
- 证据结构：理论证据（刘勰、Aristotle 均 key_chapters；Stivers、Gumperz、
  Biber、Tannen、余光中均 review_only）+ ≥2 位表达者的机器特征与精读样本
  （阮一峰周刊 n=82 + ESSAY 精读、陈皓 CoolShell n=56 + 叙事文精读）。
- 跨来源比较：`corpus/contrast/ruanyifeng_vs_coolshell_20260908.md` 与
  `corpus/contrast/narrative_vs_argument_20260910.md`——同作者句长跨体裁
  稳定（阮 37–42 字）但长句功能迁移（列举 vs 推演链），段内长短交替
  取代"全文中句化"；印证"节奏由意义驱动，不由平均句长定义"。
- 边界：平均句长/峰值数值基线只限已测体裁（编辑体/论证体/随笔体）；
  对话体与口播转写需人工听校后补测；`validated` 指机制可进入核心方法论
  引用，不等于为所有体裁设定了数值目标。
