# Question Framing · 问题框定

```yaml
id: mech.question_framing
name: 问题框定
function: 把宽泛主题收束为可回答的表达任务
confidence: contextual
```

## definition

问题框定决定文本到底回答什么，不让主题名词替代判断。好的框定包含对象、范围、冲突或判断标准。

## mechanism

先区分‘发生了什么’‘为什么’‘应该怎么做’和‘谁承担责任’，再选择主问题；必要时把一个大问题拆成主问题与支问题。

## realizations

文章标题或首段显式框定；访谈用首问限定对象；播客用主持复述确认共同问题；公文用事项、范围和时限限定。

## boundary_conditions

探索性谈话允许暂不收束，但要明确未知是研究对象，不是表达遗漏。

## overuse_risk

问题拆得过细会把文章写成问卷，削弱自然推进。

## repair_strategy

把每段删到只服务一个可回答的问题，并检查结尾是否回到最初问题。

## related_nodes

`topic_opening.md, reader_anticipation.md, coherence.md`

## sources

- src.discourse.xu-jiujiu-pianzhang; src.pragmatics.he-ziran; `corpus/interviews/`
- 命名主持人分段样本：王志（水均益、柴静、鲁健、窦文涛、杨澜）`corpus/hosting/` 下的 `named-*` 条目，仅用于问题任务与边界的跨来源比较
- Austin 的言语行为分层（`src.intl.austin-speech-acts`，review_only）提示先区分命题内容与当前表达动作；不能将讲义级概述直接当作中文问句规则。
- Searle 的言语行为章节（`src.intl.searle-speech-acts`，review_only）补充“表达形式与行动条件”的问题边界；不把英语分类直接套入中文问答。
- 刘娅琼、陶红印《汉语谈话中否定反问句的事理立场功能及类型》（`src.conversation.liuyaqiong-2011-fanwen`，review_only，摘要级）：会话证据显示否定反问句表达负面事理立场（提醒/意外/反对/斥责四层级）而非询问——为"真问句 vs Fake Hook"与"反问承担立场"的判定边界提供中文原生依据；摘要级不外推为全文结论。
- 和菜头《抒情的基础》精读（`corpus/blogs/hecaitou_the-groundwork-for-romance.yaml`，ANNOTATED，2026-09-11）：第四位表达者样本——1500 字随笔含 10 个问句（四作者最高档），每个问句均承担真实转轴功能（设问转轴/情境反问/归谬反问/预答辩反问），无 Fake Hook；与阮一峰 ESSAY（1.8 问/篇）对照说明问句密度与文体可靠性可解耦，判据是"每问是否承担推进功能"而非数量。

## 跨来源验证（§121）

- 状态：`validated`（2026-09-12 登记）。
- 证据结构：理论证据（刘娅琼、陶红印 2011 否定反问句的事理立场功能，review_only 摘要级；
  Austin/Searle 言语行为，review_only）+ **5 位表达者**的问句使用互证：
  1. 阮一峰（周刊 n=82）：问句 7.0 个/篇（ESSAY 体 1.8 个/篇）——设问承担节转轴；
  2. 陈皓（n=56）：问句均值 4.9 个/篇——反问式预答辩；
  3. 和菜头（抒情的基础，ANNOTATED）：10 问/1500 字，全部承担转轴/情境反问/归谬/预答辩，
     无 Fake Hook——问句密度与文体可靠性解耦的首个极端样本；
  4. 刘未鹏（永恒的金色对角线，ANNOTATED）：69 问/2.3 万字——自问自答推进推理链
    （"如何来证明这个停机问题呢？反证。""是不是很熟悉这个结构？"），
     问句承担推导步进而非装饰；
  5. 云风（rftg-strategy，ANNOTATED）：句级问号自标不确定（"（德州？）"）——
     问号作为 confidence 标记。
- 跨来源比较：三份对照表（`corpus/annotations/codingnow-rftg-strategy-20260910.md`、
  `hecaitou-groundwork-20260911.md`、`mindhacks-diagonal-20260912.md`）显示：问句
  密度跨作者差 5 倍以上（阮 ESSAY 1.8 vs 和菜头 10/1500 字），但"每问承担真实推进
  功能"的纪律跨作者一致——判定问句看功能不看数量。
- 边界：否定反问句的立场四层级证据为摘要级，不外推全文结论；主持/访谈中的问句
  功能需人工听校；`validated` 不改变 Fake Hook 的逐句甄别流程。
