# Mechanism Nodes · 话语机制节点库

辞达的知识节点不是"某人喜欢用某句"，而是**可迁移的话语机制**。
抽取路径固定为：

```
Speaker/文本 → Observed Ability → Discourse Mechanism → Cross-speaker Comparison → Transferable Pattern
```

## 节点 Schema

每个节点一个文件，遵循 `schemas/mechanism.yaml`：

```yaml
id, name, function, definition, mechanism,
realizations,
examples, counterexamples, boundary_conditions, overuse_risk, repair_strategy,
related_nodes
```

## 已建节点

| 节点 | 文件 | 一句话功能 |
|---|---|---|
| Rhetorical Peak | `rhetorical_peak.md` | 修辞峰值的稀缺性管理 |
| Discourse Markers | `discourse_markers.md` | 话语标记的功能判断 |
| Reader Anticipation | `reader_anticipation.md` | 模拟读者追问推进文章 |
| Compression | `compression.md` | 观点与语言的压缩 |
| Stance System | `stance_system.md` | 作者在场与立场表达 |
| Rhythm | `rhythm.md` | 由意义推动的句长节奏 |
| Metaphor & Analogy | `metaphor_analogy.md` | 承担功能的比喻 |
| Topic Progression | `topic_progression.md` | 话题推进与回环 |
| Disagreement without Distance | `disagreement_without_distance.md` | 表达异议而不制造距离 |
| Explanation | `explanation.md` | 渐进式解释复杂事物 |
| Topic Opening | `topic_opening.md` | 迅速建立读者与问题的关系 |
| Question Framing | `question_framing.md` | 把宽泛主题收束为可回答任务 |
| Argument Pivot | `argument_pivot.md` | 把材料转成新的判断层级 |
| Clarification | `clarification.md` | 消除多义而不打断流动 |
| Restatement | `restatement.md` | 换层重述而不改命题 |
| Reframing | `reframing.md` | 改变观察单位而不偷换问题 |
| Contrast | `contrast.md` | 用有边界的差异显出判断 |
| Concession | `concession.md` | 承认有效部分后限定范围 |
| Softening | `softening.md` | 调节社会距离而不逃避判断 |
| Emphasis | `emphasis.md` | 用稀缺形式托起重点 |
| Concrete Example | `concrete_example.md` | 让抽象判断可观察、可检验 |
| Story Entry/Exit | `story_entry_exit.md` | 用故事进入并回到主线 |
| Summary | `summary.md` | 在认知节点收拢信息 |
| Closure | `closure.md` | 以判断、行动或问题完成结尾 |
| Topic Return | `topic_return.md` | 让旁支重新服务主线 |
| Reader Address | `reader_address.md` | 把读者疑问纳入设计 |
| Self-positioning | `self_positioning.md` | 说明作者证据位置 |
| Uncertainty | `uncertainty.md` | 标注未知和证据边界 |
| Confidence | `confidence.md` | 使语言强度匹配证据等级 |
| Empathy | `empathy.md` | 对齐处境而不牺牲判断 |
| Turn Projection | `turn_projection.md` | 预示下一步降低跟随成本 |
| Repair | `repair.md` | 发现故障后恢复共同理解 |
| Information Density | `information_density.md` | 控制有效信息与阅读努力 |
| Audience Design | `audience_design.md` | 按受众调入口、坡度和距离 |
| Coherence | `coherence.md` | 让局部组成可追踪整体 |
| Narrative Arc | `narrative_arc.md` | 让事件顺序产生理解变化 |
| Expansion | `expansion.md` | 在不稀释判断的前提下补足必要背景 |
| Humor | `humor.md` | 以低威胁错位打开理解入口 |
| Irony | `irony.md` | 以可回收的语境落差揭示矛盾 |
| Emotional Distance | `emotional_distance.md` | 调整亲近、克制与共情的空间 |
| Topic Transition | `topic_transition.md` | 交代换题动因并把读者带回主线 |

## 使用方式

节点正文按三层用途组织：

- **生成约束**（`definition`／`mechanism`／`realizations`／`boundary_conditions`／
  `overuse_risk`／`repair_strategy`／`related_nodes`）——执行写作任务时按这一层操作；
- **判据与边界**——写与改都先看边界条件和滥用风险，再动语言；
- **关联**——`related_nodes` 指向协同或互斥的节点，`GRAPH.md` 给出全局检索表。

`examples`／`counterexamples` 视证据可得，**不作强制**。
