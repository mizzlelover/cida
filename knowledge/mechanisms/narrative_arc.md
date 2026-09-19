# Narrative Arc · 叙事弧

```yaml
id: mech.narrative_arc
name: 叙事弧
function: 让事件顺序产生理解变化而非只排列经历
confidence: validated
```

## definition

叙事弧至少包含起点、变化和回看；它服务于判断或解释，不以戏剧性替代证据。

## mechanism

选择一个改变理解的事件，控制背景与细节，设置转折后回到主题；叙事结束时给边界。

## realizations

演讲用个人经历进入公共判断；播客保留追问和修正；文章用一个事件作为论点的证据入口。

## boundary_conditions

时间顺序不等于因果顺序；个人叙事不能自动证明普遍规律。

## overuse_risk

把所有说明都故事化会拖慢信息获取。

## repair_strategy

只保留改变读者判断的事件，其余改成一句背景或数据。

## related_nodes

`story_entry_exit.md, concrete_example.md, topic_return.md`

## sources

- src.writing.qishier-tang; src.hosting.yao-xishuang-boyin-fengge; src.intl.labov-narrative; corpus/podcasts/
- 阮一峰《站在未来的十字路口》与陈皓《感染新冠的经历》精读样本
  （`corpus/annotations/ruanyifeng-essay-survivor-preface-20260910.md`、
  `corpus/annotations/coolshell-22341-20260910.md`，均 ANNOTATED）

- **可追溯性补写与勘误（2026-09-16）**：①样本补显式 `corpus_id`——`corpus.blogs.ruanyifeng-essay-survivor-preface`、`corpus.blogs.coolshell-22341`；②**勘误**：sources 首行原列的 `corpus/podcasts/` **核对后无条目支撑本文本节点**——现有两条 `ANNOTATED` 播客（`corpus.podcasts.ted-zhouyijun-2017`、`corpus.podcasts.ted-chenxiaoqing-2020`）的产出节点为 `uncertainty`／`confidence`／`audience_design`／`concrete_example`／`closure`，**均非叙事弧样本**（`scripted` 演讲体不以 Labov 式个人叙事为主线），故该目录引用**缩窄删除**，本节点样本仍为两条博客；**口语叙事样本缺口保持开放**（见 boundary）。

## 跨来源验证（§121）

- 状态：`validated`（2026-09-10 登记）。
- 证据结构：理论证据（Labov 叙事结构，`src.intl.labov-narrative`，review_only）
  + ≥2 位表达者样本（阮一峰 ESSAY 随笔、陈皓生活叙事，均人工精读 ANNOTATED），
  满足 §121「理论证据 + ≥2 位表达者样本」。
- 跨来源比较：`corpus/contrast/narrative_vs_argument_20260910.md`——两位作者
  的叙事都服务于叙事之外的判断或行动，Labov 六要素均可标注，evaluation 的
  实现方式随目标（世界观论证 vs 实用指南）迁移。
- 边界：两样本均为男性技术写作者的书面编辑体叙事；口语叙事（播客/转写）
  尚需人工听校样本；`validated` 指机制可进入核心方法论引用，
  不等于逐体裁参数已标定或人工盲评完成。
