# Reader Anticipation · 读者预期

```yaml
id: mech.reader_anticipation
name: 读者预期
function: 在读者产生疑问、不信、反驳之前，于文本中自然回应
```

## definition

把文章理解为作者与**想象读者**共同完成的认知过程（Imagined Dialogue Layer）。
写作时持续模拟：读者读到这里，下一秒会问什么？哪里可能不信？
哪里没听懂？哪里会反驳？然后在下一个表达动作里回应它。

## mechanism

优秀访谈的追问机制移植到独白写作：访谈中主持人替观众问（陈鲁豫的 Short Follow-up、
王志的 Precision Questioning），文章里没有主持人，作者必须自己兼任。
回应方式**不必是问句**——更多时候是直接补一个解释、一个例子、一个限定。

## 操作清单

写作/重写时逐段自问：

```
- 读者此刻最大的疑问是什么？（What/Why/How/凭什么）
- 这个论断的反例，读者想得到吗？想到了我先回应
- 这个概念，目标读者真的懂吗？要不要落地一层
- 这个数据/说法的可信度，读者会买账吗？给出处或限定
```

## realizations

- **written**：自然的设问（"那企业为什么不直接涨薪呢？"）+ 紧接回答；
  或直接给限定（"当然，这有个前提……"）；
- **spoken**：主持人的追问、自我追问（"这事儿奇怪在哪呢？奇怪在……"）；
- **formal**：以"需要说明的是"类限定句式出现，密度低；
- **informal**：可以更直接，"你可能要说了——"。

## counterexamples

- 每两段一个"那么问题来了"——假追问，真模板（Fake Hook）；
- 自问自答的问题读者根本不关心——伪预期，真灌水；
- 全文写成"你可能会问……我会答……"——Imagined Dialogue Layer 是内部机制，
  **不是表层格式**。

## boundary_conditions

- 读者知识水平越高，需要回应的预期越少（专家读者不需要被解释基础概念）；
- 说服性文本（评论）需要最强的反驳预期；记录性文本最弱；
- 预期回应过多会让文章啰嗦——只回应**真实概率高**的疑问。

## repair_strategy

文本显得"自说自话"时：在核心论断后插入一步读者视角检验，
补一句回应或限定。文本显得"讨好啰嗦"时：删掉低概率疑问的回应。

## overuse_risk

把内部模拟显式写成连续的自问自答，会让文章像问卷或话术脚本。

## related_nodes

`discourse_markers.md`（设问与呼应的标记）、`stance_system.md`（限定与hedging）、
`explanation.md`

## sources

- 互动语言学：回应与序列组织（`knowledge/conversation/`）
- Allan Bell, Audience Design（补强：说话人为受众设计表达）
- Herbert Clark, Grounding（补强：共同基础的建立）
- 陈鲁豫/王志访谈语料的追问功能分析（`corpus/interviews/`、`corpus/hosting/`，分析用）
- 水均益、柴静、鲁健等命名主持人分段样本用于边界比较：问题必须指向事实缺口，不能把主持姿态移植进文章
- Hyland、Jiang、Myhill 的元话语研究与 Clark 的共同基础章节（`src.intl.hyland-tse-metadiscourse`、`src.intl.hyland-jiang-metadiscourse`、`src.intl.myhill-metadiscourse`、`src.intl.clark-common-ground`，review_only）；作为读者预期候选机制，不能替代中文跨体裁评测。
- Sperber/Wilson 的关联理论（`src.intl.sperber-wilson-relevance`，review_only）补充“读者处理努力—语境效果”的候选解释；不把关联原则简化成固定句长或标记词表。
- 和菜头《抒情的基础》精读（`corpus/blogs/hecaitou_the-groundwork-for-romance.yaml`，ANNOTATED，2026-09-11）：第四位表达者样本——"双否定立靶"（"不是说…不是说…"先封常见误区）与**假想读者情境反问**（"但你的卧室有根隆起的梁呢？"）两种 realization；后者示范 Imagined Dialogue Layer 的高阶形态（不写"你可能会问"也能实现想象对话）。纠偏机制家族现为三类：平直陈述（云风）/反问预答辩（陈皓）/双否定立靶（和菜头）。

## 跨来源验证（§121）

- 状态：`validated`（2026-09-12 登记）。
- 证据结构：理论证据（互动语言学回应与序列组织；Bell 受众设计；Clark 共同基础；
  Hyland/Myhill 元话语与 Sperber-Wilson 关联理论均 review_only）+ **5 位表达者**
  的精读互证，远超"理论+≥2 位表达者"门槛：
  1. 阮一峰（周刊 406 / ESSAY，VALIDATED/ANNOTATED）：设问转轴与信息自足型预期管理；
  2. 陈皓（22298 / 22341，VALIDATED/ANNOTATED）：反问式预答辩（"你可能会说X，其实不一样"）；
  3. 云风（rftg-strategy，ANNOTATED）：平直陈述纠偏（"新手则往往理解成X"）+问号自标不确定；
  4. 和菜头（抒情的基础，ANNOTATED，2026-09-11）：双否定立靶 + 假想读者情境反问；
  5. 刘未鹏（永恒的金色对角线，ANNOTATED，2026-09-12）：**篇级统一线**（预告→逐节回收）
     与分层跳读指令——机制从句级扩展到篇级的实现。
- 跨来源比较：`corpus/annotations/codingnow-rftg-strategy-20260910.md`（三作者对照表）、
  `corpus/annotations/hecaitou-groundwork-20260911.md`（四作者对照）、
  `corpus/annotations/mindhacks-diagonal-20260912.md`（五作者对照）——纠偏/预期管理
  的实现形态随作者与篇幅迁移（平直/反问/双否定/统一线），但"预测并回应读者下一秒
  的疑问"这一核心功能跨作者、跨篇幅、跨体裁一致。
- 边界：主持/访谈语料（第三方整理）中的预期回应仍为结构级证据，逐句机制需人工听校；
  `validated` 不改变诊断时的逐句判定流程——假追问（Fake Hook）仍须逐句甄别；
  本升级不涉及 Style Control Space 数值调整。
