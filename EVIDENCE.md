# EVIDENCE · 证据标准

辞达是**可追溯的表达知识系统**，不是观点的集合。
任何重要结论都必须带着证据等级出生。

## 取证优先级

```
原论文 > 系统综述 > 专著关键章节 > 作者公开材料 > 高校资料
> 出版社介绍 > 专业论文 > 学术书评 > 权威案例 > 公开课程
```

## 研究笔记格式

每个重要知识节点保存：

```yaml
claim: ""           # 断言
evidence: ""        # 证据
source: ""          # → knowledge/sources/registry.yaml 的 source_id
counterevidence: "" # 反证
boundary: ""        # 边界条件
confidence: ""      # high / medium / low
```

## 规则

1. **执行项目时禁止只凭模型已有知识。** 必须主动检索、核验、
   交叉验证，并更新 Source Registry——尤其中文材料；
2. `access_status` 如实标注：`review_only` / `metadata_only` 级别的
   来源只能支撑假说，不能支撑强断言；
3. 资料冲突 → 记录冲突，双方并列；不强行调和；
4. 证据不足 → 降低置信度并标注，不硬写；
5. 用户经验被否定 → 明确记录为 contradicted，保留存档
   （`knowledge/practitioner_hypotheses/`）；
6. 统计特征只能辅助，不得定义好坏（Quantitative ≠ Quality）——
   所有统计结果必须结合 Function + Context 解读。

## 当前证据等级的诚实声明

v0.1 种子版中，`knowledge/sources/registry.yaml` 的大部分中文专著
条目标注为 `metadata_only`：这意味着其中的论点目前以
**学界公知 + 需求文档转述**为依据，置信度 medium，
待逐源核验关键章节后升级。这是刻意的诚实，不是疏漏。
