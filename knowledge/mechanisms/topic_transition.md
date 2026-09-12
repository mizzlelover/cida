# Topic Transition · 话题转接

```yaml
id: mech.topic_transition
name: 话题转接
function: 在换话题时交代关系、动因和下一步，避免读者被突然抛离
confidence: contextual
```

## definition

话题转接是从一个局部问题进入另一个问题时，给出最小的桥：为什么现在换、前后有什么关系、
读者接下来应关注什么。它不同于用“首先/其次”装饰段落。

## mechanism

当前结论或缺口→转接理由→新话题入口→与主线的关系。转接桥的长度由距离和读者未知决定，
同一篇文章可有显性也可有隐性转接。

## realizations

访谈中用回答中的关键词承接下一问；评论中从事实的限制转到责任或行动；文章中用一个因果、
时间或观察角度说明换轨理由，再进入新段。

## boundary_conditions

若两个段落没有真实关系，应重排内容而不是补桥；短文本和高频互动可用停顿或复述完成隐性转接。

## overuse_risk

每段都声明“接下来谈”会增加导航噪声，形成播音稿式或教程式机械过渡。

## repair_strategy

删除所有过渡词后检查读者是否仍能理解关系；只有关系会丢失时，补一句说明动因或新问题，
不要重复标题。

## related_nodes

`topic_progression.md, topic_return.md, turn_projection.md, coherence.md`

## sources

- `src.discourse.xu-jiujiu-pianzhang`; `src.conversation.huayu-biaoji-yanjiu`
- `corpus/interviews/`、`corpus/commentary/` 与 `corpus/podcasts/` 的结构化分析
