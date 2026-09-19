# Explanation · 渐进式解释

```yaml
id: mech.explanation
name: 渐进式解释
function: 把复杂事物按读者的认知坡度讲清楚
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
   段落控制、简单中文。

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

