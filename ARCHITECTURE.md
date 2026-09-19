# ARCHITECTURE · 辞达技术架构

## 一句话

SKILL.md 是路由器，知识全部分层存放在外围文件里，按需取阅
（Progressive Disclosure），**SKILL.md 不是巨型知识库**。

## 运行管线

```
用户输入
  │
  ▼
Task Detection ────────→ workflows/ 八条工作流之一
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
EVALS.md            评测体系
CHANGELOG.md        版本记录

knowledge/          知识库（机制节点 / 反模式 / 七领域）
schemas/            机制、反模式与文体参数的 YAML Schema
workflows/          八条任务工作流 + 诊断方法论
platforms/          平台呈现适配器（不改底层语言理论）
docs/               项目宣传页（GitHub Pages，cida.mizzlelover.xyz）
```

## 双母库（Twin Pipelines）

```
Pipeline A: Theory & Method Corpus（理论与方法）
      │  Theory explains Corpus
      ▼
Pipeline B: Chinese Exemplar Corpus（中文原生样本）
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

1. 中文优先：知识体系目标约 70% 中文原生 / 30% 国际补强；
2. 知识可追溯：每个机制的结论都能回到具体来源与样本；
3. 不模仿活人：只抽取机制，不复制个人语言指纹；
4. 版权安全：只登记元数据与分析，不分发受版权保护的全文；
5. 评测闭环：规则修改必须过三层回归（meaning / style / quality）。
