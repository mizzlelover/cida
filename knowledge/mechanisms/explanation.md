# Explanation · 渐进式解释

```yaml
id: mech.explanation
name: 渐进式解释
function: 把复杂事物按读者的认知坡度讲清楚
confidence: validated
```

## definition

解释是辞达最核心的动作（"把复杂事情自然地讲清楚"）。渐进式解释的关键：
**不是把知识倾倒出来，而是为读者铺一条坡度合理的上坡路。**

## mechanism

```
Anchor         锚点：从读者已知的东西出发（"你手机里的……"）
Single Step    单步推进：每一步只引入一个新概念
Layering       分层：先讲对整体有用的近似，再修正精确性
Check-in       回检：关键节点用一句话收拢（"所以到这里，我们知道了……"）
Landing        落地：抽象概念配具体实例（Concrete Example）
```

常见失败有两种方向：

```
Over-explanation    过度解释：把读者当小白，讲已知的常识 → 侮辱感
Under-explanation   解释不足：跳步，默认读者懂专业概念 → 弃读
```

校准依据永远是**目标读者的实际知识背景**，不是作者的背景（知识的诅咒）。

## 操作规范

1. 写下目标读者已知的**最后一步**（锚点），从那里开始；
2. 列出从锚点到结论的所有认知台阶，检查每级台阶的高度
   （一次只跨一个新概念）；
3. 每个抽象概念配一个具体例子或类比（`metaphor_analogy.md`）；
4. 技术内容通俗化的参照系：阮一峰式"低修辞高解释"——逻辑显式、
   段落控制、简单中文（`corpus/blogs/` 分析）。

## realizations

- **written**：例子先行或概念先行均可，视读者而定；段落短，一步一段；
- **spoken**：口播解释靠"回检"防滑落（听众不能倒带）；
- **formal**：允许定义式写法（"所谓X，是指……"），但仍要落地；
- **informal**：可以用"说白了"收一层，但全文至多一两次。

## boundary_conditions

解释坡度由受众知识决定；专家读者不需要重复常识，陌生读者也不能用类比替代关键定义。

## overuse_risk

解释过多会产生居高临下，解释过少会让读者在术语和跳步处掉队。

## repair_strategy

标出读者已知的最后一步，只补从那里到结论之间会改变判断的台阶，并在每层用一个例子回检。

## related_nodes

`metaphor_analogy.md`、`compression.md`、`reader_anticipation.md`、
`../anti_patterns/over_under_explanation.md`、`../anti_patterns/abstract_inflation.md`

## sources

- **关联补登（2026-09-16）**：`../anti_patterns/abstract_inflation.md` 为**镜像补登**——
  该反模式文件的 repair 第 3 条本就以本节点为参照（术语密度与读者水平匹配），
  但本节点此前未列该反模式，属双向登记缺口。核查见 `corpus/annotations/spotcheck-20260916h.md`。

- 阮一峰网络日志的解释性写作分析（`corpus/blogs/`，分析用）
- CoolShell/陈皓的技术对话式写作分析（`corpus/blogs/`，分析用）
- Steven Pinker, *The Sense of Style*（`src.intl.pinker-sense-of-style`，review_only；补强知识的诅咒）
- 夏丏尊、叶圣陶《文心》（`src.writing.wenxin`，review_only；**面向读者的文章学**，故事体国文读本、"对话式讲写作"的先驱文本——本节点"为读者铺坡度"的写作学根基）
- **ANNOTATED 语料样本（2026-09-16 补，此前本节点无具体条目）**：①**博客体·白话重讲专业内容**——刘未鹏《快排为什么那么快》（`corpus.blogs.mindhacks-quicksort-so-quick`，ANNOTATED）：**Anchor**＝"我们先来玩一个猜数字游戏"；**Single Step**＝二分；**Layering**＝先给"策略是平衡的"这一近似，再给"信息论并不是因，而是果"的精确化；**Check-in**＝"说到这里，剩下的事情就实在很简单了"；**Landing**＝基排"理顺一副牌"的实例。作者并明示定位："这篇文章相当于 MacKay 原文的白话文版……我用大白话解释了一通"；②**答问体·定义式解释并纠偏**——王辰（`corpus.interviews.bai-20200205-wangchen-cabin`，ANNOTATED）：以"临床诊断病例，**也就是**在流行病学史和临床表现上和确诊病例高度吻合"给出定义式解释；再以"并非所有患病者都能检出核酸阳性"（检出率约 30%–50%）修正读者对检测的既有预期，随后落地建议。

## 跨来源验证（§121）

- 状态：`validated`（2026-09-16 登记）。本批把该节点从"仅目录说明"落到**具体条目＋具体引文**，并补上写作学理论来源的确切 id。
- 依据（§121 二选一取后者）：**理论**＝夏丏尊·叶圣陶《文心》（`src.writing.wenxin`，面向读者的文章学）、Pinker《The Sense of Style》（"知识的诅咒"）、阮一峰／陈皓解释性写作分析（`corpus/blogs/`）；**语料样本**＝刘未鹏（博客体）、王辰（答问体），**2 位表达者、2 语域**。
- 跨来源比较——**"为读者铺一条坡度合理的上坡路"跨语域收敛，差异在坡度控制手法**：
  1. **游戏锚点 → 术语 → 迁移**（刘未鹏，博客体）：锚点取自读者日常（猜数字），逐步逼近形式化结论，并用"回检句"防滑落——**五步（Anchor/Single Step/Layering/Check-in/Landing）在单篇内可逐条指认**；
  2. **定义 → 边界 → 建议**（王辰，答问体）：以定义式解释给术语划界，再修正读者的既有预期（检出率），最后落地建议——**坡度由"读者既有误解"决定**。
  两者共同落点＝本页 definition「不是把知识倾倒出来，而是为读者铺一条坡度合理的上坡路」与 mechanism 五步；差异在**坡度起点**（日常游戏／读者的既有误解）。
- 边界：① 《新闻1+1》20081009 的科普段（绿色荧光蛋白）**未逐段精读**，故**未纳入本批**；② `boundary_conditions`（专家读者不需重复常识、陌生读者不能用类比替代关键定义）**未被语料验证**；③ over-explanation 与 under-explanation **两个方向的反例均未抽样**（`anti_patterns/over_under_explanation.md` 仍是经验描述）。
