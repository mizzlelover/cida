# scripts/ · 辞达自动化脚本

> **面向维护者**：本目录脚本服务于**开发仓**（依赖语料 `corpus/` 与评测档案 `evals/`，二者不随发布包分发）。
> 使用发布包写作时**无需运行任何脚本**；`run_regression.py` 在缺少研究侧档案时会跳过相应检查并打印跳过项。
> 下表中提到的内部过程文档（`HANDOFF.md`／`COMPLETION_MATRIX.md`／`CORPUS.md`／`PROJECT_STATUS.md` 等）同样随开发仓分发。

| 脚本 | 用途 |
|---|---|
| `validate_schemas.py` | 校验来源登记处与语料条目是否符合 schemas/ 模板（候选池/正式库双模式）。只查"模板必备字段是否齐全"，**字段覆盖**由 `check_source_trace.py` 的"schema 字段覆盖"闸门负责；对 YAML 解析失败给出可操作提示（文件名、行号、原文预览与改法）。 |
| `audit_research.py` | 研究诚信审计 + 生成覆盖率报告，并输出命名主持人独立样本表。 |
| `build_corpus_index.py` | 扫描 corpus/ 生成 INDEX.md 与 index.yaml（分类/转录质量/准备度统计）。 |
| `check_links.py` | 检查全仓 Markdown 相对链接与 source_id 引用的完整性。 |
| `build_mechanism_graph.py` | 从机制节点生成 `knowledge/mechanisms/GRAPH.{md,yaml}`；解析 `related_nodes` 内全部目标、按命名空间分类型成边，无法解析的目标写入 `unresolved_references` 并打印，不静默丢弃。 |
| `detect_duplicate_nodes.py` | 检查机制节点 id 唯一性。 |
| `detect_uncited_claims.py` | 检查机制节点是否具备定义、边界、修复与来源结构；强制状态一致性（`validated` ⇔ 存在「跨来源验证」小节）与重复小节检测。 |
| `check_source_trace.py` | 来源与结构追溯**总闸门**（维护者向）：机制节点引用、语料⇄标注档可追溯性、关联目标与反模式双向登记、对照库区间、盲评配对⇄揭盲钥、参数命名空间，以及各类"当前值 ⇄ 实际"一致性（当前状态文档／对外页面／README／回归说明档／交付物清单／进度数字／深读读数），另有 `install.sh` 可执行性、库内路径引用、字段级乱码与字段卫生等检查。**逐条判据与正负验证记录见脚本内注释**。 |
| `run_evals.py` | 验收 benchmark inventory 的来源链与期望属性（支持 `corpus_reference`、`project_authored_control` 与官方文件正例层 `official_public_document`；数量以 150 为基线、允许按正例层扩充）。 |
| `run_benchmark_quality.py` | 实跑 10 个项目自有高模板控制，生成 Original/Baseline/Skill、六项 Preservation、Pairwise 本地预筛与四角色模拟预筛；不伪造受版权保护来源文本。 |
| `calibrate_style_profile.py` | 读取质量跑与语域核验，生成默认十维 Profile 的评测迭代台账；区分长文本适用性与短控制，不自动外推全局数值。 |
| `build_human_review_queue.py` | 生成 benchmark 盲评队列，区分可直接盲评与等待授权原文的 case（正例层按 `input_file` 实存且非空判定 ready）。 |
| `audit_host_duration.py` | 复核官方 CCTV/CNTV 视频时长元数据，生成命名主持人时长审计；不把节目总长冒充有效表达时长。 |
| `run_regression.py` | 统一运行 schema、审计、机制、benchmark、索引与链接回归；自动识别开发仓／发布包环境。 |
| `compare_versions.py` | 比较 YAML/JSON 状态快照，输出字段级差异。 |
| `generate_report.py` | 生成当前工程规模、来源深度和状态快照。 |
| `blind_keys.py` | 盲评揭盲钥的统一读取：解析 `pending_pairs/keys_*.md` 里的 `pair_NNN … A = Skill/Baseline` 声明，返回 `{pair号: Skill 所在侧}` 与钥所在册；由 `process_blind_review.py`／`audit_pair_preservation.py`／`check_source_trace.py` 共用。同一对冲突映射时抛错，不静默取舍。 |
| `process_blind_review.py` | 盲评答卷结构校验 + 揭盲 + 分维度/分角色汇总；揭盲一律读 `blind_keys.py`，缺钥的行直接判错中止，不用奇偶公式推断。 |
| `audit_pair_preservation.py` | 配对 Preservation 机械预筛（旁观项加粗口径在 A/B 版的 presence check）；配对无钥时记为 `no_unmask_key` 而不猜侧。 |

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
