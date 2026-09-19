# Stance System · 立场系统

```yaml
id: mech.stance_system
name: 立场系统
function: 让读者感到有一个具体的人在思考，并对思考负责
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

