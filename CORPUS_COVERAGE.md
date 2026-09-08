# CORPUS_COVERAGE · 语料覆盖报告

由 `scripts/audit_research.py` 自动生成，请勿手改。
状态机：PLANNED → FOUND → ACQUIRED → READ → ANNOTATED → VALIDATED → DISTILLED

| Corpus | Target(Gate) | Found(候选) | Acquired | Read | Analyzed | Accepted(VALIDATED+) |
|---|---:|---:|---:|---:|---:|---:|
| commentary | 100 | 1 | 0 | 0 | 0 | 0 |
| interviews | 100 | 0 | 0 | 0 | 0 | 0 |
| hosting | 60 | 0 | 0 | 0 | 0 | 0 |
| speeches | 100 | 0 | 0 | 0 | 0 | 0 |
| podcasts | 100 | 0 | 0 | 0 | 0 | 0 |
| blogs | 200 | 1 | 245 | 245 | 3 | 2 |
| articles | — | 0 | 0 | 0 | 0 | 0 |
| raw_edited_pairs | 50 | 0 | 0 | 0 | 0 | 0 |
| contrast | — | 0 | 0 | 0 | 0 | 0 |

## Gate 判定（§117：未达标不得宣称 Corpus Construction 完成）

- commentary: 0 / 100 ❌ 未达标
- hosting: 0 / 60 ❌ 未达标
- interviews: 0 / 100 ❌ 未达标
- speeches: 0 / 100 ❌ 未达标
- podcasts: 0 / 100 ❌ 未达标
- blogs: 245 / 200 ✅
- raw_edited_pairs: 0 / 50 ❌ 未达标

## 诚信审计备注

- 来源登记处：52 条中 46 条为 metadata_only（未读全文，结论限假说级）
