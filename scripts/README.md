# scripts/ · 辞达自动化脚本

| 脚本 | 用途 |
|---|---|
| `validate_schemas.py` | 校验来源登记处与语料条目是否符合 schemas/ 模板（字段、枚举、必填项、重复 ID） |
| `build_corpus_index.py` | 扫描 corpus/ 生成 INDEX.md 与 index.yaml（分类/转录质量/准备度统计） |
| `check_links.py` | 检查全仓 Markdown 相对链接与 source_id 引用的完整性 |

依赖：Python 3.9+ 与 PyYAML。

```bash
pip install pyyaml
python scripts/validate_schemas.py
python scripts/build_corpus_index.py
python scripts/check_links.py
```

## 路线图（需求文档 §94–95 的后续工具）

`detect_uncited_claims`（未标注来源的断言扫描）、`build_mechanism_graph`
（机制知识图谱构建）、`run_evals`、`compare_versions`、`generate_report`，
以及语料统计工具（句长分布、话语标记频率、词汇多样性、重复度分析）。
统计特征只能辅助诊断，不得定义好坏（Quantitative ≠ Quality）。
