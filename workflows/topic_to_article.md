# Workflow A：主题 → 成文（topic_to_article）

从零写一个主题。输入可以是任何粗糙程度：一句话主题、几个要点、一份提纲。

## 输入

```yaml
topic:        # 主题
audience:     # 受众（可缺省，缺省时先推断再确认）
platform:     # 发布平台（决定 Adapter，见 platforms/）
purpose:      # 说服 / 解释 / 记录 / 连接
key_ideas:    # 必须出现的要点（可缺省）
style_hint:   # 用户给出的任何风格倾向（登记为 Practitioner Hypothesis）
```

## 流程

### 1. Intent — 先定交际意图

回答三个问题（内部完成）：

- 这篇文章希望读者读完后**知道/相信/去做**什么？
- 读者现在在哪？（已知、偏见、抵触点）
- 作者凭什么谈这个？（经验、专业、观察——决定 Stance 的合法来源）

### 2. Thesis — 形成主判断

把主题压缩成**一个有取舍的判断**。检验标准：这个判断是否可能有人不同意？
如果不可能有人不同意（"AI很重要"），继续往下压，直到有真正的观点。

### 3. Argument Flow — 安排论证流

把文章理解为**作者与想象读者共同完成的认知过程**。可用的推进动作：

```
提出 → 理解 → 质疑 → 澄清 → 深入 → 反转 → 解释 → 举例 → 总结
```

- 不同文章用不同动作序列，**禁止固定模板**；
- 每一步之间问：读者此刻会疑惑什么？在文本里自然回应，而不是假装没有疑问；
- 明确哪里需要**显性逻辑**（推理的关键节点），哪里可以**隐含**（读者能自己补的）。

### 4. Style Profile — 定文体参数

按受众与平台在 `STYLE_SYSTEM.md` 的十维空间定位，默认从
`Modern Chinese High-Quality Conversational` Profile 出发微调。

### 5. Opening — 开头

开头的唯一职责：**迅速建立读者与问题的关系**。

可用策略：具体场景 / 一个真实的疑问 / 一个反常的事实 / 直接的判断 / 一个冲突。

避免"随着时代发展""众所周知""在当今社会"——但**不做禁词处理**：
如果某个套话在具体语境里确实承担了功能，可以用；只是它几乎从不承担功能。

### 6. Draft — 成文

写作时保持**修辞密度曲线**：

```
普通表达 → 解释 → 普通表达 → 具体例子 → Rhetorical Peak → 回落
```

- 全篇金句不超过稀缺配额（参见 `knowledge/mechanisms/rhetorical_peak.md`）；
- 句子长短由意义推动：该断则断，该连则连；禁止为了"像人"随机打乱句长；
- 比喻必须承担功能：帮助理解 / 帮助记忆 / 帮助情感，三选一，否则删
  （`knowledge/mechanisms/metaphor_analogy.md`）。

### 7. Ending — 结尾

从以下方式中选**一种**，不要把全文再总结一遍：

```
Synthesis（综合升维）  Judgment（落回判断）  Open Question（留一个真问题）
Principle（提炼原则）  Action（给出行动）    Perspective Shift（换一个视角）
Return to Opening（回应开头）
```

### 8. Quality Review → Final

过 `SKILL.md` §7 自检清单；重点执行 Preservation Test 的反向版：
**Key Ideas 是否全部到场、没有被表达欲稀释？**

## 输出格式

默认输出：成文 + 三行以内说明（文体定位、关键取舍）。
Explain 模式下追加：Argument Flow 图、Style Profile、每处重要修辞的理由。
