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

## 研究诚信层（第二部分需求 §111–131，v0.2 并入）

**核心立场：Registry 不是参考书目清单，必须对应实际获取、实际阅读、
实际分析过的材料。**

### 禁止行为

只根据标题推测内容 / 只凭搜索摘要判断 / 只登记书名和 URL /
只引用二手介绍 / 只写"建议研究某某" / 只建空目录 / 只生成计划 /
未读内容却标记为已研究 / 根据模型记忆补全书籍内容。

### 语料状态机（§129）

```
PLANNED → FOUND → ACQUIRED → READ → ANNOTATED → VALIDATED → DISTILLED
```

- `metadata_only` 只能进候选池（`corpus/candidates/`）；
- 只有 VALIDATED 及以上才能支撑知识蒸馏；
- 来源只取得摘要时标记 `access_level: abstract_only`，
  不得把摘要结论扩写成全文结论；无法取得全文时明确写
  `FULL TEXT NOT AVAILABLE` 并转向替代材料交叉验证（§115–116）。

### Research Gates（§117，未达标不得宣称语料建设完成）

即兴评论 ≥100 · 主持点评 ≥60 · 访谈 ≥100 · 演讲 ≥100 ·
播客 ≥100 · 博客 ≥200 · Raw→Edited 对照 ≥50。
核心主持人 ≥10 有效长样本或 ≥60 分钟；专项人物 ≥5；不足标记
`INSUFFICIENT CORPUS`。

### 交叉验证（§121）

机制进入核心方法论前：≥3 个不同来源，或「理论证据 + ≥2 位表达者样本」；
否则标记 `speaker-specific`，不作通用规则。

### 能力检查（§130）

开工前先检查可用工具（Web 访问 / 长网页 / PDF / 字幕 / 下载 / 转录），
某项不可用：记录限制、调整方法、完成能完成的部分——不得假装完成。

### 审计与抽查

- `python scripts/audit_research.py`：七类审计 + 自动生成
  `CORPUS_COVERAGE.md`（覆盖率按 Found/Acquired/Read/Analyzed/Accepted 分列）；
- 每阶段随机抽查 5%–10% 语料：URL 真实性、正文存在性、转录可靠性、
  标注依据、是否过度推断；错误率超阈值 → 回滚该阶段（§128）。

### 研究完成的定义（§131）

不是"找到 100 个来源"，而是完整走过：
**Source → Acquire → Read → Annotate → Compare → Validate → Distill →
Evaluate**。缺任何一步，该材料不计为正式完成。
