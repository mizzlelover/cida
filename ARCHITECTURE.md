# ARCHITECTURE · 辞达技术架构

## 一句话

SKILL.md 是路由器，知识全部分层存放在外围文件里，按需取阅
（Progressive Disclosure），**SKILL.md 不是巨型知识库**。

## 运行管线

```
用户输入
  │
  ▼
Task Detection ────────→ workflows/ 六条工作流之一
  │
  ▼
Audience / Medium Detection ──→ STYLE_SYSTEM.md 十维参数定位
  │
  ▼
Diagnosis ─────────────→ workflows/diagnose_text.md 十项诊断
  │                        （内部完成，Explain 模式才输出）
  ▼
Knowledge Retrieval ───→ knowledge/ 机制节点 + 反模式 + 领域要点
  │                        （按诊断结果取 1–3 个文件，不全读）
  ▼
Rewrite / Compose ─────→ P0 意义逻辑 → P1 结构清晰 → P2 流转语域
  │                        → P3 节奏修辞 → P4 打磨
  ▼
Evaluation ────────────→ SKILL.md §7 自检 + EVALS.md 维度
  │
  ▼
交付（默认：成稿 + 极简说明）
```

## 文件地图

```
SKILL.md            路由与铁律（加载即生效，保持精简）
STYLE_SYSTEM.md     十维文体参数空间与默认 Profile
ARCHITECTURE.md     本文件
METHODOLOGY.md      方法论：双母库、蒸馏、比较、验收
EVIDENCE.md         证据标准：研究笔记、置信度、冲突处理
CORPUS.md           语料规划、版权原则、名单
EVALS.md            评测体系
CHANGELOG.md        版本记录

knowledge/          知识库（机制节点 / 反模式 / 七领域 / 来源登记 / 假说登记）
corpus/             语料登记（元数据+分析，不存全文）
schemas/            全部数据结构的 YAML Schema
workflows/          六条任务工作流 + 诊断方法论
platforms/          平台呈现适配器（不改底层语言理论）
evals/              Benchmark / Pairwise / Regression / Human Review
scripts/            校验、索引、链接检查脚本
docs/               项目宣传页（GitHub Pages，cida.mizzlelover.xyz）
```

## 双母库（Twin Pipelines）

```
Pipeline A: Theory & Method Corpus（knowledge/ + sources registry）
      │  Theory explains Corpus
      ▼
Pipeline B: Chinese Exemplar Corpus（corpus/）
      │  Corpus corrects Theory
      ▼
Mechanism Distillation → knowledge/mechanisms/ 节点
```

蒸馏链路：Sources → Claims → Mechanisms → Evidence → Boundaries →
Examples → Chinese Realization → Repair Strategy。

## Harness 适配

辞达是**纯提示词工程 + 文件结构**的 Skill，不依赖特定模型的私有 API：

- **Claude Code**：整个 `cida/` 目录放入 `~/.claude/skills/`（或项目
  `.claude/skills/`），SKILL.md 的 frontmatter 即标准 Agent Skill 格式；
- **Codex / OpenCode**：仓库根的 `AGENTS.md` 自动生效，引导 agent 进入
  SKILL.md 的主流程；
- 一键安装：`bash install.sh`（见 README）。

## 设计约束

1. 中文优先：知识体系 70% 中文原生 / 30% 国际补强；语料 ≥85% 中文；
2. 知识可追溯：每个机制的 sources 落到 registry 的 source_id；
3. 不模仿活人：只抽取机制，不复制个人语言指纹；
4. 版权安全：语料只存元数据与分析，不存全文；
5. 评测闭环：规则修改必须过三层回归（meaning / style / quality）。
