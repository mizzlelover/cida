# Topic Progression · 话题推进

```yaml
id: mech.topic_progression
name: 话题推进
function: 让文章的话题链在表层自然流动、底层结构成立
```

## definition

好的对话型文本"表层自然松散，底层话题结构仍然成立"（窦文涛式知识谈话的
核心特征）。话题推进管理三件事：**往前走（Topic Shift）、回得来（Topic Return）、
读者跟得上（Cohesion）**。

## mechanism

```
Topic Chain      话题链：相邻段落共享话题或自然交接，主语不无谓跳跃
Topic Shift      话题转换：需要明确信号（"再说一件相关的事"）或语义桥梁
Topic Return     话题回环：岔出去后回到主线，给读者"收拢"的信号
Foreground/Background  前景后景：主线前景推进，背景信息压缩后置
```

文章与谈话的差别：谈话可以靠对方的反应现场纠偏，文章只能一次走对——
所以文章的话题转换信号要**比谈话更显性**，但又不能变成路牌堆砌
（Over-signposting）。

## 操作规范

1. 每段开头检查：这段和上一段是什么关系？（递进/转折/并列/补充）
   读者能在两秒内看出这个关系吗？
2. 岔开话题前给预告，回来后给收束（"说回正题"类信号可以自然，
   不必刻板）；
3. 段间主语跳跃超过一次时，检查是否丢了衔接；
4. 结尾回到开头的话题或意象（Return to Opening）是最可靠的收束之一。

## realizations

- **written**：段落衔接依赖话题链与逻辑词的组合；
- **spoken**：谈话节目中的"哎说到这个"式自然转换——转成文字时
  要显性化半档；
- **formal**：允许使用结构化标记（"其一""其二"），但避免机械；
- **informal**：可以更跳，但跳出去必须回得来。

## repair_strategy

文本"读着乱"：画出段落话题链，找出断裂点补衔接。
文本"像说明书"：减少路牌式过渡，改用语义关系衔接。

## related_nodes

`discourse_markers.md`、`reader_anticipation.md`、
`../anti_patterns/template_transition.md`

## sources

- 徐赳赳《现代汉语篇章语言学》（话题链与篇章组织）
- 胡壮麟《语篇的衔接与连贯》
- 窦文涛《锵锵三人行》话题流分析（`corpus/podcasts/` 旁注，分析用）
- 会话分析中的序列组织研究（`knowledge/conversation/`）
