# Cídá 辞达

> "Words should simply carry the meaning." — Confucius, *Analects* 15.41

**A Modern Chinese Conversational Writing Intelligence Skill for AI agents**

[中文 README](README.md) · [Project Site](https://cida.mizzlelover.xyz) · [Methodology](METHODOLOGY.md) · [Architecture](ARCHITECTURE.md)

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
| Topic → Article | Intent → thesis → argument flow → style profile → draft → review |
| Full Rewrite | Diagnosis first, then P0 meaning/logic → P4 polish |
| Paragraph Polish | Clarify → compress → reorder → connect → rhythm → polish |
| Oral → Article | Transcripts/interviews → publishable prose, voice preserved |
| De-formalization | Reduce nominalization & bureaucratese, raise clarity and rhythm |
| Platform Adaptation | WeChat / Xiaohongshu / Zhihu / Weibo / video scripts / podcasts |
| Style Calibration | Learns your personal style *parameters* from your own texts |
| Explain Mode | Every edit justified with its underlying discourse mechanism |

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

v0.6.9: the corpus acquisition and knowledge-distillation pipeline is real and
running. The formal corpus contains 935 positive items: 245 blogs, 100 prepared
speeches, 111 interviews/Q&A records, 101 commentary records, 225 hosting
samples, 103 podcast/knowledge-conversation records, and 50 raw-to-edited
pairs. The seven quantity gates are met; there are also 10 negative-corpus
controls and 2 candidates.

The 150-case benchmark inventory has passed source-chain validation. Ten
project-authored high-template controls have actual Original/Baseline/Skill
runs, plus three real-material evaluations. **80 anonymous blind-review pairs
(pair_001..080) are ready**, with a review workbench (`REVIEW_WORKBENCH.md`),
an answer sheet (`answer_sheet.csv`) and an unblinding/aggregation script
(`scripts/process_blind_review.py`) — the four-role human review required by
the requirements is the only open acceptance step. Eight of the 41 mechanism
nodes have been upgraded to `validated` under the cross-source bar, while named
host duration, third-party transcript listening checks, and remaining
authorizations stay explicitly open. See [FINAL_REPORT.md](FINAL_REPORT.md),
[COMPLETION_MATRIX.md](COMPLETION_MATRIX.md), and
[CORPUS_COVERAGE.md](CORPUS_COVERAGE.md). Source evidence levels remain explicit
in EVIDENCE.md and the source registry (`full_text 8`, `key_chapters 3`,
`review_only 117`, `metadata_only 2`; registry: 130 entries, 96 Chinese / 34
international).

## Author

**谁是专家 (Shuíshì Zhuānjiā)** — content creator focused on language,
expression, and AI writing.

- Xiaohongshu (RED): [@谁是专家](https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25)
- X (Twitter): [@dboy_yi2025](https://x.com/dboy_yi2025)
- WeChat Official Account: 谁是专家 (QR on the [project site](https://cida.mizzlelover.xyz))

## License

[MIT](LICENSE) © 谁是专家 (mizzlelover)
