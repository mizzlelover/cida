<div align="center">

<img src="docs/assets/logo.svg" width="88" alt="辞达" onerror="this.style.display='none'">

# 辞 达

*CÍDÁ · Modern Chinese Conversational Expression Engine*

<br>

**「辞达而已矣。」**——《论语 · 卫灵公》

> 「能使是物了然于心者，盖千万人而不一遇也，
> 而况能使了然于口与手者乎？是之谓辞达。」
> ——苏轼《答谢民师书》

<br>

让 AI 把一个值得表达的思想，用现代中文说得
**清楚、自然、漂亮、亲近，而且有分量**。

不做「去 AI 味」——追求真正的表达质量。

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-a63a2e?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/版本-1.0.0-33453f?style=flat-square)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-✓-a63a2e?style=flat-square)](#安装)
[![Codex](https://img.shields.io/badge/Codex-✓-33453f?style=flat-square)](#安装)

<br>

[官网](https://mizzlelover.github.io/cida) · [快速上手](#安装) · [理念](#核心判断) · [English](README_EN.md)

</div>

---

## 它的拒绝

一个工具的边界，就是它的立场。辞达对六类流行做法**说不**：

| | 拒绝 | 理由 |
|:-:|---|---|
| ✕ | **不做「去 AI 味」** | 工整、分点、逻辑清楚不是 AI 的专利。辞达优化的是可读性、对话感、节奏与思想密度本身。 |
| ✕ | **不骗检测器** | 目标不是「让人看不出是 AI 写的」，而是让文字值得被读完。 |
| ✕ | **不假装不完美** | 不随机加错别字、不故意插口误。像人 ≠ 不完美。 |
| ✕ | **不模仿活人** | 没有「董卿风」「白岩松风」。只抽取可迁移的表达机制，不复制语言指纹。 |
| ✕ | **不设禁用词表** | 「其实」「所以」——每个词只看它有没有真实的话语功能。 |
| ✕ | **不判百分比** | 不输出「AI 味 87%」。诊断只给具体、可修复的问题清单。 |

> **最高原则：降低语言门槛，不降低思想门槛。**

---

## 基础哲学 · 十一条军规

| # | 中文 | English |
|:-:|---|:--|
| 01 | 先质量，再谈像不像人 | Quality before Humanization |
| 02 | 受众先于风格 | Audience before Style |
| 03 | 功能先于措辞 | Function before Phrase |
| 04 | 机制先于规则 | Mechanism before Rule |
| 05 | 证据先于经验 | Evidence before Heuristic |
| 06 | 中文原生优先 | Chinese before Translation |
| 07 | 借鉴会话，不照搬聊天 | Conversation-informed, not Spoken-like |
| 08 | 结构不是罪 | Structure is not AI |
| 09 | 修辞必须承担意义 | Rhetoric is not Decoration |
| 10 | 自然不等于随意 | Natural ≠ Casual |
| 11 | 清楚不等于浅薄 | Clear ≠ Simple-minded |

---

## 四种模式

| 模式 | 说明 |
|---|---|
| **快速优化** Quick Rewrite | 轻诊断、直接改。适合短文本与明确场景。 |
| **深度重写** Deep Rewrite | 完整十项诊断后按 P0→P4 重建：先修意义与逻辑，再调结构，最后才是语言。 |
| **解释改动** Explain | 每一处修改附理由与机制依据——不是黑箱润色，是可学习的表达课。 |
| **风格校准** Calibrate | 从你的真实文本抽取风格参数，形成个人文体档案。学参数，不抄句子。 |

---

## 语域行为 · 先达意，后风格

辞达的默认输出语域是「正常说话的达意中文」——口表语域行为清单：

- **开门即事**：第一句是事实或判断，没有标题装置
- **立场直陈**：第一人称立场跟着事实直接说出
- **具体词优先**：用可感的词，不用抽象词
- **判断落在实事上**：带对象和分寸，不喊口号
- **承接式推进**：回答从问题里长出来
- **限定词顺着说**：嵌在句流里，不单独挂牌

任何更书面或更花哨的处理都必须有**语境理由**。特稿技法（倒装钩子、元叙述框架、粗体标签脚手架）在无语境理由时禁用。

---

## 安装

### Claude Code

```bash
# 克隆并一键安装到 ~/.claude/skills/cida
git clone https://github.com/mizzlelover/cida.git
bash cida/install.sh

# 然后直接说：
# 「帮我把这篇文章改得更自然」
# 「把这段会议转录整理成可发表的文章」
```

### Codex / OpenCode

```bash
# 克隆到你的项目目录即可
git clone https://github.com/mizzlelover/cida.git

# 仓库根部的 AGENTS.md 会被自动读取，
# 引导 agent 进入 SKILL.md 的主流程。
```

### 其他 Harness

```bash
# 任何能读指令文件的 agent：
# 让它先读 SKILL.md，按路由表取用
# workflows/ 与 knowledge/ 下的文件。
git clone https://github.com/mizzlelover/cida.git
```

---

## 项目结构

```
cida/
├── SKILL.md                  ← 核心路由（主流程 + 铁律 + 自检）
├── workflows/                ← 8 条工作流
│   ├── topic_to_article.md       主题 → 成文
│   ├── rewrite_article.md        整篇重写
│   ├── rewrite_paragraph.md      段落优化
│   ├── oral_to_article.md        口述 → 文章
│   ├── deep_rewrite.md           深度重写
│   ├── diagnose_text.md          诊断
│   ├── platform_adaptation.md    平台适配
│   └── style_calibration.md      风格校准
├── knowledge/                ← 知识库
│   ├── register/                 语域行为清单（口表约束）
│   ├── mechanisms/               41 个话语机制节点
│   ├── anti_patterns/            反模式库
│   ├── rhetoric/                 修辞学
│   ├── pragmatics/               语用学
│   ├── discourse/                篇章语言学
│   └── writing/                  写作传统
├── platforms/                ← 7 个平台适配器
├── schemas/                  ← YAML Schema
├── STYLE_SYSTEM.md           ← 十维文体空间
├── METHODOLOGY.md            ← 方法论
├── ARCHITECTURE.md           ← 架构文档
└── EVALS.md                  ← 评测框架
```

---

## 品牌出处

<div align="center">

**「能使是物了然于心者，盖千万人而不一遇也，**
**而况能使了然于口与手者乎？是之谓辞达。」**

*苏轼《答谢民师书》*

把事物看得透彻，已是千万人中无一；
还能说清楚、写明白——孔子称之为「辞达」。
苏轼说：辞至于能达，则文不可胜用矣。

</div>

---

## 作者

<div align="center">

**水事专家**

内容创作者，长期关注表达、语言与 AI 写作。
辞达是其对「什么样的中文值得被读」这一问题的一次系统作答。

[小红书](https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25) ·
[X @dboy_yi2025](https://x.com/dboy_yi2025) ·
微信公众号「水事专家」

</div>

---

<div align="center">

**辞达** · CÍDÁ · *Say it well, in Chinese*

[官网](https://mizzlelover.github.io/cida) ·
[GitHub](https://github.com/mizzlelover/cida) ·
[English](README_EN.md) ·
[方法论](METHODOLOGY.md) ·
[更新日志](CHANGELOG.md) ·
[MIT License](LICENSE)

辞达而已矣。

</div>
