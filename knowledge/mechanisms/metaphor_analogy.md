# Metaphor & Analogy · 比喻系统

```yaml
id: mech.metaphor_analogy
name: 比喻与类比
function: 用熟悉的事物降低陌生事物的理解成本
```

## definition

比喻必须承担功能，三条出路，至少居其一：

```
help understanding   帮助理解（解释型比喻）
help memory          帮助记忆（锚定型比喻）
help emotion         帮助情感（共鸣型比喻）
```

一条都不占的比喻是装饰品。**禁止为了文采强行比喻。**

## 质量维度

```
Analogy Fit        贴切度：喻体与本体在关键属性上真的相似吗？
Metaphor Distance  距离感：太远读者接不住，太近没有新信息
Novelty            新鲜度："像一把双刃剑"已死——陈喻不产生理解增量
Clarity            清晰度：比喻本身比本体更难懂 = 负资产
Cultural Fit       文化贴合：目标读者熟悉这个喻体吗？
```

## 操作规范

1. 解释复杂概念时，**先想直白解释够不够**，够了就不用比喻；
2. 必须用比喻时，从**目标读者的生活域**取材，不从作者的炫技域取材；
3. 一个比喻只用一次；同一个喻体在全文中要保持一致；
4. 比喻之后必须回到本体：比喻是桥，不是家。

## examples

- 好（解释型）：向非技术读者解释缓存——"就像把常用的调料放在灶台边，
  而不是每道菜都跑一趟储藏室。"贴切、熟悉、帮助理解。
- 坏（装饰型）："时间如白驹过隙，转瞬即逝。"——无理解增量，无情感增量，陈喻。

## boundary_conditions

- 科技与财经写作中，错误类比比没有类比更糟（Analogy Fit 优先）；
- 抒情文本可放宽 Novelty 要求，但不能突破 Clarity 底线；
- 比喻密度受 Rhetorical Density 参数约束，峰值位置的比喻待遇最高。

## repair_strategy

文本"花哨但空洞"：列出全部比喻，逐一过三功能检验，装饰品全删，
留下的检查 Fit 与 Distance。文本"正确但难懂"：为最抽象的概念配一个
读者生活域的类比。

## overuse_risk

陈喻、跨域过远的喻体和连续比喻会增加理解成本，把解释变成装饰。

## related_nodes

`explanation.md`（解释是比喻的主战场）、`rhetorical_peak.md`、
`../anti_patterns/abstract_inflation.md`

## sources

- 陈望道《修辞学发凡》（譬喻格的类型与适用）
- George Lakoff 概念隐喻研究（`src.intl.lakoff-metaphors`，review_only；补强比喻的认知功能）
- 刘未鹏《Mind Hacks》类比写作分析（`corpus/blogs/`，分析用）
