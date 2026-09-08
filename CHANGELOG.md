# CHANGELOG

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与语义化版本。

## [0.2.0] - 2026-09-08

研究诚信层（需求文档第二部分 §111–131 并入）。

### 新增

- **语料状态机**：PLANNED → FOUND → ACQUIRED → READ → ANNOTATED →
  VALIDATED → DISTILLED；VALIDATED 以下不得支撑知识蒸馏；
- **候选池** `corpus/candidates/`：metadata_only 线索的唯一合法归宿；
- **对照语料库** `corpus/contrast/`（Negative Corpus，§124）；
- **四层研究目录** `corpus/{raw,normalized,annotations,metadata}/`（§125，
  原文与分析分离）；
- **Evidence Package Schema**（§113）：正式语料条目的完整字段集；
- **Research Gates**（§117）与自动覆盖率报告 `CORPUS_COVERAGE.md`（§118）；
- **审计脚本** `scripts/audit_research.py`：metadata_only 入库检测、
  未核验转录检测、provenance 缺失检测、人物样本不足检测、
  来源阅读深度统计、覆盖率报告生成（§127）；
- **真实采集示范**：实际读取阮一峰周刊第 409 期全文并完成结构化标注
  （`corpus/blogs/ruanyifeng_weekly_409.yaml` +
  `corpus/annotations/ruanyifeng-weekly-409.md`，state: ANNOTATED）。

### 变更

- v0.1 的两条元数据示范条目**降级为候选池**（未实际取得内容，
  不得冒充正式语料）；
- 主持人能力表与机制节点的语料类引用标注为「待验证假说」，
  禁止根据名气推断语言特征（§119–121）；
- `validate_schemas.py` 支持候选池/正式库双模式校验。

## [0.1.0] - 2026-09-08

种子版（Seed Release）。品牌定名「辞达 Cídá」，语出《论语·卫灵公》。

### 新增

- 核心 `SKILL.md`：任务识别 → 诊断 → 知识检索 → 重写 → 自检的路由体系；
- 六条工作流：主题成文 / 整篇重写 / 段落优化 / 口述成文 / 书面自然化 /
  平台适配，外加风格校准（Calibrate）；
- 十维文体参数空间与默认 Profile（`STYLE_SYSTEM.md`）；
- 机制节点库首批 10 节点：修辞峰值、话语标记、读者预期、压缩、立场系统、
  节奏、比喻、话题推进、异议而不疏远、渐进式解释；
- 反模式库：21 项索引，7 项完整条目（结构单调性、语义重复、模板过渡、
  金句通胀、虚假亲昵、抽象通胀、解释失配）；
- 七领域知识要点：修辞 / 语体 / 语用 / 篇章 / 会话 / 播音主持 / 写作；
- Source Registry 种子（35 中文原生 + 13 国际补强），证据等级如实标注；
- 评测体系：15 质量维度、Benchmark 种子、成对评测、三层回归、反向测试；
- 平台适配器：通用 / 公众号 / 小红书 / 知乎 / 微博 / 视频口播 / 播客；
- 自动化脚本：schema 校验、语料索引、链接与引用完整性检查；
- Harness 支持：Claude Code（install.sh）、Codex / OpenCode（AGENTS.md）；
- 项目宣传页 `docs/`（GitHub Pages，承载于 cida.mizzlelover.xyz）。

### 路线图

- 机制节点扩展至 30–40 个核心节点（Phase 2）；
- 语料库扩充至 650+ 条登记（八类别配额见 CORPUS.md）；
- Benchmark 扩充至 150 案；
- 反模式库补齐剩余 14 项完整条目；
- 语料统计工具（句长分布 / 话语标记频率 / 重复度分析）。
