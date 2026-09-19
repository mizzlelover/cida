# Rhetorical Peak · 修辞峰值

```yaml
id: mech.rhetorical_peak
name: 修辞峰值
function: 让全篇最值得记住的判断，获得最强的语言形式
confidence: validated
```

## definition

一篇文章不应全程一个强度。修辞峰值是文章中**密度最高、形式最讲究、
最值得被记住**的少数位置——通常落在核心判断、关键转折或结尾综合处。
峰值的价值来自稀缺：峰值一多，就全是平地。

## mechanism

读者对文本的记忆不是均匀的。认知上，人们记住的是**峰值与结尾**
（peak-end 效应在文本阅读中的对应物）。因此修辞资源应当集中投放到：

1. 核心判断第一次完整出现的位置；
2. 论证的关键转折处；
3. 结尾的综合处。

其余位置保持高质量的"普通表达"——平实不等于敷衍，平处托得起峰处。

## Quote-worthiness Filter（金句过滤器）

一句话是否值得强化为峰值，五项检验（满足三项以上才强化）：

```
□ 是否是核心判断？        —— 不是核心判断，不配峰值形式
□ 是否压缩了前文？        —— 峰值应当收束，而非凭空抒情
□ 是否有新的视角？        —— 重复已知常识的漂亮话是 Gold-quote Inflation
□ 是否可以独立成立？      —— 脱离上下文仍站得住，才值得被引用
□ 是否与上下文呼应？      —— 峰值要落在论证线上，不是贴上去的金箔
```

## realizations

- **written**：短句独立成段；对偶或排比收束；一个精准比喻；判断句式（"是……"）；
- **spoken**：语速放慢、重复关键词、停顿后给结论（口播/演讲中保留）；
- **formal**：峰值更少更收敛，靠措辞精度而非修辞花样；
- **informal**：峰值可以是一句大白话——形式服务判断，不是反过来。

## examples

- 好：前文用 800 字分析一个现象的多重原因，峰值句："所以真正的问题不是
  人懒，是系统把勤奋的回报拿走了。"——压缩前文、核心判断、可独立成立。
- 坏：每段结尾都来一句"这，就是 XX 的力量。"——峰值通胀，边际效用归零。

## boundary_conditions

- 信息型文本（技术解释、教程）峰值应极少，清晰本身就是美德；
- 短文本（500 字内）至多一个峰值；
- 峰值不用于没有判断的内容——先回到 P0 修内容。

## overuse_risk

Gold-quote Inflation（金句通胀）：每段制造结论、强行升华、知识服务腔
（"愿你……""愿你被这个世界温柔以待"式收尾）。见
`../anti_patterns/gold_quote_inflation.md`。

## repair_strategy

1. 找出全文所有"漂亮句"，逐一过 Quote-worthiness Filter；
2. 留 1–3 个，其余降级为普通表达或直接删除；
3. 检查保留的峰值是否落在论证线上。

## related_nodes

`compression.md`（峰值往往由压缩产生）、`stance_system.md`（峰值通常承载立场）、
`rhythm.md`（峰值常配短句）、`../anti_patterns/gold_quote_inflation.md`

## sources

- **官方致辞样本（2026-09-16 补）**：同条达沃斯致辞——篇末"任何以邻为壑的做法，任何单打独斗的思路，任何孤芳自赏的傲慢，最终都必然归于失败！"：**三连同构 + 感叹号**构成篇末峰值，且峰值落在**否定式排比**而非正向金句（与博客体"单句段转轴"峰值形态不同）。
- **同语域第二篇（2026-09-16 补）**：王毅联合国人权理事会讲话——峰值为**收尾短对偶**（"人权保障没有最好，只有更好"），不给结论加重；与达沃斯篇"任何…×3 + 感叹"的排比型峰值并列，说明**同语域内峰值实现可变**。

- 陈望道《修辞学发凡》（修辞与题旨情境的适配原则）
- 刘勰《文心雕龙·隐秀》（`src.rhetoric.liu-xie-wenxin`，key_chapters；“秀”是局部突出，不是全文装饰化）
- 董卿《主持人大赛》点评语料的功能分析（Abstract & Elevate 的位置规律，见 `corpus/hosting/`）
- Aristotle《修辞学》第三卷（`src.intl.aristotle-rhetoric`，key_chapters；清楚与合宜优先，隐喻和节奏须服从语体与主题）
- 阮一峰周刊 406、ESSAY《站在未来的十字路口》与陈皓 22298、22341 精读样本
  （`corpus/annotations/`，VALIDATED×2 + ANNOTATED×2；排版峰值/意象峰值/加粗小结的体裁变体）
- 和菜头《抒情的基础》精读（`corpus/blogs/hecaitou_the-groundwork-for-romance.yaml`，ANNOTATED，2026-09-11）：
  中段归位峰值（"这就是我说的基础……"）+ **元语言收尾**（"省脑子就会导致费钱，句号。"
  ——口说"句号"同时完成收束标记、去端着与压缩）；金句稀缺性由形式克制保证。

> 勘误（2026-09-10）：本页旧版曾列"和菜头《槽边往事》修辞密度抽样"；
> 经查 `corpus/blogs/` 无和菜头条目（采集期网络不可达），该引用无佐证，已删除。
> **闭环（2026-09-11）**：和菜头条目已实际取得（hecaitou.com 通道恢复），
> 上述引用为有据登记；旧版引用以本轮实际精读为准。

- **可追溯性补写（2026-09-16）**：①两条致辞样本此前写作"**同条达沃斯致辞**"，**未给 `corpus_id`**（与其他节点已修的同类缺陷一致），现补为 `corpus.speeches.xi-20210125-davos-agenda`、`corpus.speeches.wang-20240226-un-human-rights`；②博客侧补齐显式 id——`corpus.blogs.ruanyifeng-weekly-406`、`corpus.blogs.ruanyifeng-essay-survivor-preface`、`corpus.blogs.coolshell-22298`、`corpus.blogs.coolshell-22341`、`corpus.blogs.hecaitou-the-groundwork-for-romance`；③**主持语料仍为目录级**：董卿点评的可对位条目是 `corpus.hosting.dong-20191113-host-contest-yixinbin`（`READ` 级），只作**结构级**参照，**不计入峰值样本数**。

## 跨来源验证（§121）

- 状态：`validated`（2026-09-10 登记）。
- 证据结构：理论证据（刘勰、Aristotle 均 key_chapters；陈望道 review_only）
  + ≥2 位表达者的精读互证——阮一峰周刊 406（VALIDATED，短句独立成段的排版峰值）、
  阮一峰 ESSAY 随笔（ANNOTATED，意象峰值，全篇仅 1 处加粗）、
  陈皓 22298（VALIDATED，强判断承担峰值）、陈皓 22341（ANNOTATED，加粗小结峰值）、
  和菜头《抒情的基础》（ANNOTATED，2026-09-11 补，中段归位峰值+元语言收尾）。
- 跨来源比较：`corpus/contrast/ruanyifeng_vs_coolshell_20260908.md` 与
  `corpus/contrast/narrative_vs_argument_20260910.md`——峰值实现随体裁迁移
  （排版/意象/判断/小结），但"峰值稀缺"纪律跨作者跨体裁一致
  （阮全篇 1 处加粗；峰值后回落平实；和菜头短文全篇仅结尾一处峰值式收束）。
- 边界：峰值位置规律在主持语料（第三方整理）中仅为结构级证据；
  口播/播客的语音峰值需人工听校；`validated` 不改变 Quote-worthiness Filter
  的逐句判定流程。
