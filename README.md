<h1 align="center">

<img src="docs/assets/readme-banner.svg" width="100%" alt="辞达 Cídá · 辞达而已矣 · 现代中文高质量对话型表达引擎">

</h1>

<div align="center">

<br>

让 AI 把一个值得表达的思想，用现代中文说得<br>
**清楚、自然、漂亮、亲近，而且有分量。**

不做「去 AI 味」——追求真正的表达质量。

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-a63a2e?style=flat-square)](LICENSE)
[![版本](https://img.shields.io/badge/版本-1.1.0-33453f?style=flat-square)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-✓-a63a2e?style=flat-square)](#安装)
[![Codex](https://img.shields.io/badge/Codex-✓-33453f?style=flat-square)](#安装)

<br>

[官网](https://mizzlelover.github.io/cida)　·　[快速上手](#安装)　·　[下载 Skill 包](dist/cida.skill)　·　[English](README_EN.md)

</div>

---

## 辞达的表达立场

一个工具的边界，就是它的立场。辞达对六类流行做法**说不**：

| | 拒绝 | 理由 |
|:-:|---|---|
| ✕ | **不做「去 AI 味」** | 工整、分点、逻辑清楚不是 AI 的专利。辞达优化的是可读性、对话感、节奏与思想密度本身。 |
| ✕ | **不骗检测器** | 目标不是「让人看不出是 AI 写的」，而是让文字值得被读完。 |
| ✕ | **不假装不完美** | 不随机加错别字、不故意插口误。像人 ≠ 不完美。 |
| ✕ | **不模仿活人** | 不复刻在世作者或主持人的个人风格；可按语境调整正式度、语气和节奏。 |
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
| 05 | 事实先于修辞 | Facts before Flourish |
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
| **快速优化** Quick Rewrite | 轻诊断、直接改；保留关键任务契约与保真检查。适合短文本与明确场景。 |
| **深度重写** Deep Rewrite | 完整十二项诊断，比较实质候选后按 P0→P4 重建：先定意义与素材，再定平台结构与价值兑现，最后打磨语言。 |
| **解释改动** Explain | 展开任务假设、候选取舍、文本依据、机制节点与适用边界。质量方向由任务目标和证据支撑，不由个人偏好单独决定。 |
| **风格校准** Calibrate | 从真实样本区分稳定声音、场景策略与偶发习惯。学参数和机制，不抄句子，也不把个人 Profile 当成所有平台的统一滤镜。 |

---

## 语域与平台 · 先任务，后风格

「现代中文高质量对话型」只是未指定发布场景时的回退 Profile，不是所有平台共同的起点。

- **平台前置**：先确定平台、内容形态、入口、读者关系、目标和格式，再比较切入与结构；
- **表达可重建**：平台可以改变首份材料、信息顺序、详略和互动，不能改变事实、证据与核心立场；
- **价值要兑现**：开头建立真实相关性，前段给一次真实获得，中段有新增值，结尾完成综合、行动或讨论；
- **语域有来源**：口述整理为文章时保留声音、具体细节与自然承接，但不把直陈开头强加给视频、播客或所有文章；
- **形式看功能**：直陈、场景、疑问、叙事和冲突都可使用；只反对没有功能的标题装置、虚假钩子和价值拖欠。

完整写作与平台适配经过「文本质量＋平台适配」双自检，不用平台腔或传播想象代替真实材料。

---

## 安装

### Claude Code

```bash
# 克隆并安全复制安装到 ~/.claude/skills/cida
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
├── SKILL.md                  ← 核心路由（主流程 + 铁律 + 双重自检）
├── workflows/                ← 8 条任务工作流＋平台任务契约
│   ├── platform_task_contract.md 平台、入口、候选与价值路线
│   ├── topic_to_article.md       主题 → 成文
│   ├── rewrite_article.md        整篇重写
│   ├── rewrite_paragraph.md      段落优化
│   ├── oral_to_article.md        口述 → 文章
│   ├── deep_rewrite.md           深度重写
│   ├── diagnose_text.md          十二项诊断
│   ├── platform_adaptation.md    平台适配
│   └── style_calibration.md      风格校准
├── knowledge/                ← 43 个话语机制、反模式与表达参考
│   ├── register/                 语域与口表表达
│   ├── mechanisms/               话语机制与图谱
│   ├── anti_patterns/            常见表达问题
│   ├── rhetoric/                 修辞表达
│   ├── pragmatics/               语境、立场与礼貌
│   ├── discourse/                篇章组织
│   ├── conversation/             对话感与衔接
│   ├── hosting/                  现场表达与主持能力
│   └── writing/                  中文写作
├── platforms/                ← 8 个发布场景适配器
├── dist/                     ← 可安装 Skill 包
├── docs/                     ← 项目宣传页与品牌素材
├── STYLE_SYSTEM.md           ← 十维语言参数＋平台任务参数
├── AGENTS.md                 ← AI agent 使用指引
├── README.md                 ← 项目与安装说明
└── install.sh                ← 安装脚本
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

**谁是专家**

内容创作者，长期关注表达、语言与 AI 写作。
辞达是其对「什么样的中文值得被读」这一问题的一次系统作答。

[小红书](https://www.xiaohongshu.com/user/profile/64dd6c680000000001011d25) ·
[X @dboy_yi2025](https://x.com/dboy_yi2025)

<img src="docs/assets/wechat-qr-square.png?v=2" width="280" alt="微信搜一搜「谁是专家」">

</div>

---

<div align="center">

**辞达** · CÍDÁ · *Say it well, in Chinese*

[官网](https://mizzlelover.github.io/cida) ·
[GitHub](https://github.com/mizzlelover/cida) ·
[English](README_EN.md) ·
[更新日志](CHANGELOG.md) ·
[MIT License](LICENSE)

辞达而已矣。

</div>
