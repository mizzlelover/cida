# Compression · 压缩

```yaml
id: mech.compression
name: 压缩
function: 用最小的读者努力，承载最大的意义
```

## definition

压缩不是"写短"。压缩是 **Maximum Meaning per Unit of Reader Effort**：
删掉不增加信息的成分，让保留下来的每个成分都承重。白岩松式的新闻评论
是压缩的典范语料：30 秒内完成切题、判断、解释、收束（Commentary Compression）。

## mechanism

读者的注意力是稀缺资源。每多一个不承重的句子，核心信息的抵达率就下降一分。
压缩的三个层次：

```
1. 删   —— 同义反复、空修饰、自我指涉（"我认为我觉得"）
2. 合   —— 三个短句说一件事 → 合成一个有力的句子
3. 提   —— 具体罗列 → 提炼为判断（细节保留一个最典型的）
```

## realizations

- **written**：从"在很大的程度上对……产生了一定的影响"到"改变了"；
- **spoken**：口语的压缩靠重音与停顿，转成文字时改为语序与断句；
- **formal**：公文允许更多程式成分，但也不允许同义反复；
- **informal**：口语的"强调式重复"（说三遍）在文中改为位置强调或短句独立。

## examples

- 原："这本书给了我很大的启发，让我对这个问题有了更加深入和全面的认识与理解。"
- 压："这本书把这个问题的根子讲透了。"
- 判断：若后文要展开"哪些启发"，原句整句可删，直接进入内容。

## boundary_conditions

- 压缩不能压掉**分寸**：限定词（"至少目前""在这个条件下"）承重，不是废话；
- 压缩不能压掉**证据**：论断可以短，证据链不能断；
- 需要安抚、共情的语段（致歉、安慰）允许"冗余"——冗余在那里承担情绪功能。

## overuse_risk

过度压缩 → 电报腔、干巴巴、失去呼吸感。压缩的终点是"清楚"，
不是"字少"。另一风险：把口语中的情绪冗余全删光，人味随之消失
（见 `../../workflows/oral_to_article.md` 的 Preserve Voice）。

## repair_strategy

文本臃肿时：逐句问"删掉这句，读者会损失什么？"——什么都不损失的，删。
文本干硬时：检查是否误删了承重的限定与必要的缓冲。

## related_nodes

`rhetorical_peak.md`（峰值常由压缩产生）、`rhythm.md`、
`../anti_patterns/ai_semantic_repetition.md`

## sources

- 白岩松《新闻1+1》评论语料的压缩分析（`corpus/commentary/`，分析用）
- 马少华《新闻评论教程》（评论语言的效率）
- 叶圣陶《文章例话》（删繁就简的具体示范）
- Joseph Williams, *Style: Lessons in Clarity and Grace*（补强：concision 原则）
