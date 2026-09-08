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
spoken_realization, written_realization, formal_realization, informal_realization,
examples, counterexamples, boundary_conditions, overuse_risk, repair_strategy,
related_nodes, sources
```

## 第一批节点（Phase 1 优先，对应需求文档 §93）

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

## 路线图（Phase 2+ 待建）

Topic Opening、Question Framing、Argument Pivot、Clarification、Restatement、
Reframing、Contrast、Concession、Softening、Emphasis、Expansion、Concrete Example、
Story Entry/Exit、Summary、Closure、Topic Return、Reader Address、Self-positioning、
Uncertainty、Confidence、Humor、Irony、Emotional Distance、Empathy。

## 来源原则

- 中文原生理论与语料优先（约 70%），国际理论补强（约 30%）；
- 每个节点的 sources 必须落到 `knowledge/sources/` 登记处，可追溯；
- 证据不足时降低置信度并标注，不强行断言。

> **Provenance 诚实声明（§126）**：当前各节点 sources 中引用的语料分析
> （如主持人点评、博客文本抽样）来自项目任务书设定的研究方向，
> 对应语料尚处于候选池阶段（`corpus/candidates/`），**未经实际采集与标注**。
> 在对应语料达到 VALIDATED 状态前，这些引用仅表示"验证计划"，
> 不构成已完成的语料证据。节点机制的理论部分不受影响。

