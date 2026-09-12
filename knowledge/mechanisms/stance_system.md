# Stance System · 立场系统

```yaml
id: mech.stance_system
name: 立场系统
function: 让读者感到有一个具体的人在思考，并对思考负责
confidence: validated
```

## definition

好文章里有一个"人"。这个"人"不一定靠"我认为""我觉得"刷存在感——
立场可以显式，也可以隐式；可以坚定，也可以坦诚地不确定。
立场系统管理的是：**作者在场的方式与浓度**。

## mechanism 立场的实现层级

```
explicit stance   显式立场："我的判断是……""我反对"
implicit stance   隐式立场：通过选材、语序、措辞倾向体现（更高级，更难）
hedging           限定："至少目前来看""在这个条件下"——智识诚实
certainty         确信度分级：断言 > 判断 > 倾向 > 猜想，必须与实际证据匹配
personal          个人经验：作为证据的合法来源之一，但不冒充普遍规律
judgment          判断：观点（opinion）与无支撑断言（unsupported assertion）的分界
```

## Intellectual Honesty

鼓励真实的限定表达："这并不意味着……""换个场景可能不同……""至少目前来看……"。
但**禁止机械加限定词**——每句都"可能也许大概"是另一种失职：逃避判断。

判断质量检验：

- 这个判断有取舍吗？（两边都对等于没有判断）
- 这个判断的依据在文中吗？
- 这个判断的边界说清了吗？

## realizations

- **written**：判断句压阵；第一人称克制使用（全文"我"不超过必要密度）；
- **spoken**：主持人的"我个人认为"类标记 + 表情语气（转文字时改为措辞承担）；
- **formal**：立场藏于处置与详略（"值得注意的是"后必是真值得注意的）；
- **informal**：可以更直给，"这事的本质就是……"。

## counterexamples

- 全文没有一句有人负责的话 → 维基腔/通稿腔；
- 满篇"我觉得"但无一个真判断 → 虚假在场；
- 观点骑墙到失去信息（"一方面……另一方面……大家怎么看？"）→ Over-balanced
  Argument，见 `../anti_patterns/`。

## boundary_conditions

- 客观报道类文本立场应后置且克制；
- 机构署名文章不代表个人时，立场表达要匹配主体；
- 用户有强烈个人声音时，优先保留其立场习惯（Preserve Voice）。

## overuse_risk

显式自我定位过密会让文本自我中心，过度限定又会让读者无法判断作者到底承担什么结论。

## repair_strategy

保留最能说明证据位置的一处显式立场，其余通过选材、语序和边界条件呈现；发现无依据时回到证据而不是加强语气。

## related_nodes

`reader_anticipation.md`（预期读者的反驳）、`rhetorical_peak.md`（峰值承载判断）、
`uncertainty`（路线图）

## sources

- 汉语立场表达研究（`knowledge/pragmatics/`；`src.pragmatics.ran-yongping` 冉永平《语用学：现象与分析》含人际交往原则/礼貌与面子章，review_only 摘要级）
- 何自然、冉永平语用学论著中的立场与预设研究
- 白岩松、康辉评论语料的判断表达分析（`corpus/commentary/`，分析用）
- Douglas Biber 的 stance 研究（补强）
- Biber/Conrad 的语域与风格框架（`src.intl.biber-register`，review_only）补充“体裁变化不等于立场强度变化”的比较边界。
- Toulmin 的论证分层与 Hyland 的元话语研究作为 review_only 外部参照（`src.intl.toulmin-uses-argument`、`src.intl.hyland-tse-metadiscourse`、`src.intl.hyland-jiang-metadiscourse`）；仍需中文语料与人工评测校准断言强度。
- 精读样本：阮一峰周刊 406（假说归因标记"大概"）、阮一峰 ESSAY（让步转折+"提出问题不给答案"）、陈皓 22298（强判断+体裁局限声明）、云风《银河竞逐的乐趣和策略》（不利数字自证+问号自标不确定）——见 `corpus/annotations/`

## 跨来源验证（§121）

- 状态：`validated`（2026-09-10 登记）。
- 证据结构：理论证据（冉永平《语用学：现象与分析》人际交往原则/礼貌与面子章、
  Biber stance 研究、Toulmin 论证分层——均 review_only）+ ≥2 位表达者样本
  （阮一峰×2、陈皓×2、云风×1，共 5 篇人工精读，覆盖三种立场实现风格）。
- 跨来源比较：`corpus/contrast/narrative_vs_argument_20260910.md` 与
  `corpus/annotations/codingnow-rftg-strategy-20260910.md`——立场**必然在场**
  （三位作者无一例外管理自己的在场方式），但实现风格随 persona 迁移：
  阮一峰"假说归因+出处纪律"、陈皓"强判断+自我披露边界"、云风"不利数字
  自证+句级问号标记"。印证本页核心主张：立场系统管理的是"作者在场的方式
  与浓度"，不是统一的第一人称密度。
- 边界：精读样本均为技术写作者书面体；口语立场（主持/播客）仍以结构级证据
  为主，需人工听校后补强；`validated` 不等于给出各 persona 的立场浓度数值，
  那属于 Style Control Space 的分体裁校准（待人工评测）。
- `src.conversation.wangxuanting-nihai-bieshuo` 王璇婷《言语类话语标记"你还别说"探究》（full_text，2026-09-11 全文实读）：口语立场实现的反预期路径——"你还别说"作为**预设-反预期标记**，参照系三分（说话人预期/听话人预期/言语社会共享预期），并承担提醒与立场表达；为 stance 的口语 realization（反预期接题）提供理论+变体证据。
