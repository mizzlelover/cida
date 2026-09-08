# Candidate Pool · 候选池

只登记**尚未实际取得内容**的潜在语料：节目名称、作者主页、线索来源、
采集计划。这里的条目**不是**正式语料（§112–113）。

## 铁律

- `access_level: metadata_only` 的条目只能待在本目录，不得进入正式库；
- 只根据标题/搜索摘要/百科介绍推测的内容，禁止写入任何知识结论；
- 进入正式库（`corpus/<类别>/`）的最低条件：实际取得 §112 所列
  A–F 六类内容之一，并完成 Evidence Package（`schemas/corpus_item.yaml`）。

## 状态机（§129）

```
PLANNED → FOUND → ACQUIRED → READ → ANNOTATED → VALIDATED → DISTILLED
```

只有 VALIDATED 及以上状态的语料，才能支撑知识蒸馏（机制节点的
sources 引用）。
