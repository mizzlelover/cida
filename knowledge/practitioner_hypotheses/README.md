# Practitioner Hypotheses · 实践者假说登记处

用户的写作经验（"我喜欢分点""我不喜欢太书面""希望偶尔有金句"……）
**一律登记为假说，不直接进入规则**。

## 为什么

经验来自特定语境。把特定语境的经验上升为普遍规则，是写作建议
最常见的失败。登记制的意义：尊重经验，同时给经验标定边界与证据等级。

## Schema

```yaml
claim: ""                # 假说内容，如"分点让读者更容易读完"
source:
  practitioner: ""       # 提出者（用户/作者/编辑）
observed_context: ""     # 观察到的语境（平台、文体、受众）
desired_effect: ""       # 期望的效果
possible_mechanism: ""   # 可能的机制解释
supporting_evidence: []  # 支持证据
conflicting_evidence: [] # 冲突证据
boundary_conditions: ""  # 边界条件
status: ""               # validated / contextual / unverified / contradicted
```

## 流转规则

```
unverified   → 有证据支持且边界清楚 → validated（限于边界内）
unverified   → 部分语境成立 → contextual（标注语境）
任何状态     → 发现冲突证据 → 记录冲突，不强行调和；
               被否定 → contradicted，明确记录，保留存档
```

## 当前登记（种子）

```yaml
- claim: 目标文体的默认参数（formality 4–5, orality 6–7, 等）
  source: { practitioner: 项目任务书 }
  observed_context: 现代中文互联网高质量长文场景
  desired_effect: 自然、清楚、有判断、有品质
  possible_mechanism: 中间语域同时保留书面语的结构与口语的亲近
  supporting_evidence: [ 需求文档 §39 ]
  conflicting_evidence: []
  boundary_conditions: 需经 evals/ 真实评测修正；平台适配时允许偏移
  status: unverified
```

新增假说请在本目录下单独立 YAML 文件，并在本 README 追加索引行。
