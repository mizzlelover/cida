<h1 align="center">

<img src="docs/assets/readme-banner.svg" width="100%" alt="Cídá 辞达 · 辞达而已矣 · A modern Chinese expression Skill">

</h1>

<div align="center">

<br>

**A modern Chinese expression Skill, rooted in the idea of 辞达.**

Let AI help a worthwhile thought find clear, natural, warm, and resonant words in modern Chinese.

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-a63a2e?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-33453f?style=flat-square)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-✓-a63a2e?style=flat-square)](#install)
[![Codex](https://img.shields.io/badge/Codex-✓-33453f?style=flat-square)](#install)

<br>

[中文 README](README.md)　·　[Project Site](https://mizzlelover.github.io/cida)　·　[Download .skill](dist/cida.skill)

</div>

---

## What it is

Cídá (辞达) is an open AI Skill that makes AI assistants write and rewrite
**modern Chinese** at the level of a thoughtful human interlocutor:
clear, natural, warm, logical, and worth reading to the end.

It is deliberately **not** an "AI-flavor remover". Neat structure, bullet
points, parallelism, and summary sentences are not AI's invention — they are
the craft of good human writers. Instead of chasing "undetectability",
Cídá optimizes what actually matters: readability, clarity, flow, rhythm,
audience fit, conversationality, information density, coherence, rhetorical
quality, human presence, thought quality, and emotional distance.

**The prime directive: lower the language barrier, never the intellectual bar.**

## What it refuses to do

- ✗ No AI-detector evasion, no "beat the detector" promises
- ✗ No fake imperfections (random typos ≠ human voice)
- ✗ No imitation of living authors' personal styles — it extracts
  transferable *mechanisms*, never personal fingerprints
- ✗ No "banned AI words" lists — every word is judged by its function
- ✗ No structural iconoclasm — structure is not a crime; monotony is

## Capabilities

| Capability | Description |
|---|---|
| Topic → Article | Boundaries → platform task contract → candidates → value route → draft → dual review |
| Full Rewrite | Twelve-part diagnosis, then P0 meaning/materials → P1 platform structure/value → P4 polish |
| Paragraph Polish | Clarify → compress → reorder → connect → rhythm → polish, with the paragraph's task intact |
| Oral → Article | Transcripts/interviews → publishable prose, distinctive materials and voice preserved |
| De-formalization | Reduce nominalization & bureaucratese without forcing every text into casual speech |
| Platform Adaptation | Generic / WeChat / Xiaohongshu / Zhihu / Weibo / video / podcast / community, split by surface and entry route |
| Style Calibration | Separates stable voice, situational strategy and one-off habits from your own texts |
| Quick Rewrite | A light diagnosis with the essential task contract, preservation checks and concise rationale |
| Deep Rewrite | Compares 2–3 substantive candidates before reconstruction, with text-quality and platform-fit review |
| Explain Mode | Expand key changes with textual evidence, rationale, mechanism nodes, and their limits; quality decisions follow task goals and evidence rather than personal taste alone |

## Install

**Claude Code**

```bash
git clone https://github.com/mizzlelover/cida.git
bash cida/install.sh        # installs to ~/.claude/skills/cida
```

**Codex / OpenCode** — clone the repo into your project; the root
`AGENTS.md` routes the agent into `SKILL.md` automatically.

**Any other harness** — Cídá is pure prompt engineering plus file
structure. Point your agent at `SKILL.md`; it routes itself through
`workflows/` and `knowledge/`.

## Why "Cídá"?

From the *Analects*: "辞达而已矣" — language need only *carry* the meaning.
Su Shi later completed the thought: to grasp a thing clearly in the mind is
rare enough; to make it clear **in speech and on paper** — that is *cídá*,
and writing that achieves it cannot fail. That is the whole ambition of
this project.

## Status

v1.1.0 — platform-native expression and reader-value upgrade. Cídá ships as a router
(`SKILL.md`), eight task workflows plus a platform task contract, eight publishing-context
adapters, a ten-dimension language space with platform task parameters, and a knowledge
base of 43 discourse mechanisms and common writing pitfalls. Platform, surface, entry route,
reader relation, candidate structures and value payoff are decided before drafting; the same
facts are never treated as a licence to reskin one generic draft for every platform.

## Author

**谁是专家 (Shuíshì Zhuānjiā)** — content creator focused on language,
expression, and AI writing.

- Xiaohongshu (RED): [@谁是专家](https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25)
- X (Twitter): [@dboy_yi2025](https://x.com/dboy_yi2025)
- WeChat Official Account: 谁是专家 (QR on the [project site](https://cida.mizzlelover.xyz))

## License

[MIT](LICENSE) © 谁是专家 (mizzlelover)
