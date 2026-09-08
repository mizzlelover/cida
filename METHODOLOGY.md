# METHODOLOGY · 辞达方法论

## 问题定义

市面上大量工具把问题定义为"去AI味"。辞达不接受这个定义：
工整、分点、逻辑清楚、使用排比与总结句，并不天然属于 AI——
人类优秀作者同样这样表达。

辞达要优化的是：**Readability、Clarity、Flow、Rhythm、Audience Fit、
Conversationality、Information Density、Logical Coherence、
Rhetorical Quality、Human Presence、Thought Quality、Emotional Distance。**

最终目标不是"让人看不出是 AI 写的"，而是：

> 让一段有价值的思想，以现代中文中自然、清楚、亲近、有逻辑、
> 有品质、有判断、愿意让人继续读下去的方式表达出来。

## 文体定位：Conversation-informed Chinese Prose

不是纯书面语（距离感、名词化、阅读负荷高），也不是完全口语
（零散、啰嗦、思想密度低），而是**高完成度的中文对话型书面表达**：

> 一个知识水平较高、思考能力很强、表达能力成熟的人坐在读者对面，
> 把复杂事情自然地讲清楚。

## 基础哲学（十一条军规）

```
Quality before Humanization        先质量，不像不像 AI 为目标
Audience before Style              受众先于风格
Function before Phrase             功能先于措辞
Mechanism before Rule              机制先于规则
Evidence before Heuristic          证据先于经验
Chinese before Translation         中文原生优先
Conversation-informed, not Spoken-like  借鉴会话机制，不照搬聊天记录
Structure is not AI                结构不是罪
Rhetoric is not Decoration         修辞必须承担意义
Natural ≠ Casual                   自然不等于随意
Clear ≠ Simple-minded              清楚不等于浅薄
```

核心：**Lower the Language Barrier, Not the Intellectual Bar.**
降低语言门槛，不降低思想门槛。

## 双母库并行（Twin Pipelines）

- **Pipeline A — Theory & Method Corpus**：一期 100 项来源
  （70 中文原生 / 30 国际补强），组织为 Source Registry，
  最终蒸馏为机制节点而非书目摘要；
- **Pipeline B — Chinese Exemplar Corpus**：一期 650+ 真实中文样本，
  八大类别（见 CORPUS.md），长期 2000+ / 5000+。

两者互相校正：Theory explains Corpus. Corpus corrects Theory.

## 知识蒸馏链路（Evidence-Aware Knowledge Distillation）

```
Sources → Claims → Mechanisms → Evidence → Boundaries
        → Examples → Chinese Realization → Repair Strategy
```

- 不追求收集全部理论：优先深挖 30–40 个核心机制，再扩展；
- 不要求 100 项来源全部全文：按"原论文 > 系统综述 > 专著关键章节 >
  作者公开材料 > 高校资料 > 出版社介绍 > 专业论文 > 学术书评 >
  权威案例 > 公开课程"的优先级取证，证据等级如实标注（见 EVIDENCE.md）；
- 每个语料样本记录 strengths / weaknesses / overuse_risks——
  优秀语料不等于全盘学习；
- 跨语料功能比较（Cross-Corpus Comparison）：同一话语功能
  （如"提出不同意见"）横向比较主持人、播客、博客、评论的实现，
  抽象为机制（如 Disagreement without Distance），而非"某人爱用某句"。

## 文体控制

十维连续参数空间（STYLE_SYSTEM.md），参数映射到语言行为概率与策略；
修辞密度曲线保证文章有起伏；Quote-worthiness Filter 保证金句稀缺。

## 执行原则

- P0 意义逻辑 → P1 结构清晰 → P2 流转语域 → P3 节奏修辞 → P4 打磨；
- Delete before Rewrite：没有价值的句子，删除；
- 每次重写问：这句话真的是更好吗？——不是"变化是不是更大"；
- Preservation Test 强制执行：原意、立场、证据、分寸一个都不能丢；
- Simplify Expression, Not Reality.

## 验收

最终验收的不是"像不像人写"，而是：真正理解现代中文里，
怎样把一个值得表达的思想，说得清楚、自然、漂亮、亲近，而且有分量。
具体场景见 EVALS.md §9。
