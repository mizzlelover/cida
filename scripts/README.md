# scripts/ · 辞达自动化脚本

| 脚本 | 用途 |
|---|---|
| `validate_schemas.py` | 校验来源登记处与语料条目是否符合 schemas/ 模板（候选池/正式库双模式） |
| `audit_research.py` | 研究诚信审计（§127）+ 生成 `CORPUS_COVERAGE.md` 覆盖率报告（§118），并输出 12+6 命名主持人 `host_target` 独立样本表 |
| `build_corpus_index.py` | 扫描 corpus/ 生成 INDEX.md 与 index.yaml（分类/转录质量/准备度统计） |
| `check_links.py` | 检查全仓 Markdown 相对链接与 source_id 引用的完整性 |
| `build_mechanism_graph.py` | 从机制节点生成 `knowledge/mechanisms/GRAPH.{md,yaml}` |
| `detect_duplicate_nodes.py` | 检查机制节点 id 唯一性 |
| `detect_uncited_claims.py` | 检查机制节点是否具备定义、边界、修复与来源结构 |
| `check_source_trace.py` | 检查机制节点引用的 `src.*` 是否存在于 Source Registry |
| `run_evals.py` | 验收 150 案 benchmark inventory 的来源链与期望属性 |
| `run_benchmark_quality.py` | 实跑 10 个项目自有高模板控制，生成 Original/Baseline/Skill、六项 Preservation、Pairwise 本地预筛与四角色模拟预筛；不伪造受版权保护来源文本 |
| `calibrate_style_profile.py` | 读取质量跑与语域核验，生成默认十维 Profile 的评测迭代台账；区分长文本适用性与短控制，不自动外推全局数值 |
| `build_human_review_queue.py` | 生成 150 案盲评队列，区分可直接盲评与等待授权原文的 case |
| `audit_host_duration.py` | 复核官方 CCTV/CNTV 视频时长元数据，生成命名主持人时长审计；不把节目总长冒充有效表达时长 |
| `run_regression.py` | 统一运行 schema、审计、机制、benchmark、索引与链接回归 |
| `compare_versions.py` | 比较 YAML/JSON 状态快照，输出字段级差异 |
| `generate_report.py` | 生成当前工程规模、来源深度和状态快照 |

依赖：Python 3.9+ 与 PyYAML。

```bash
pip install pyyaml
python scripts/validate_schemas.py
python scripts/build_corpus_index.py
python scripts/check_links.py
```

## 尚待扩展

语料统计工具（句长分布、话语标记频率、词汇多样性、重复度分析）仍需接入统一
回归；统计特征只能辅助诊断，不得定义好坏（Quantitative ≠ Quality）。
