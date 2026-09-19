# Coherence · 连贯

```yaml
id: mech.coherence
name: 连贯
function: 让局部句子组合成可追踪的整体意义
confidence: validated
```

## definition

连贯不只靠连接词，而靠话题链、因果、时间、证据和作者意图的共同对齐。

## mechanism

为每段标出话题、动作和与上一段的关系；缺口用最小衔接补，关系自明处不加路牌。

## realizations

文章用信息尾重和话题延续；访谈用复述接问题；口播用回检；正式文本用层级和事项编号。

## boundary_conditions

探索性文本可以保留跳跃，但要把跳跃作为意义或风格，而不是遗漏。

## overuse_risk

把所有关系显式化会僵硬。

## repair_strategy

先画话题链，再决定加词、换序还是删段。

## related_nodes

`topic_progression.md, discourse_markers.md, argument_pivot.md`

## sources

- src.discourse.xu-jiujiu-pianzhang; src.register.feng-shengli-gailun; src.intl.mann-thompson-rst; src.intl.taboada-mann-rst-review; src.intl.ernst-erst; corpus/blogs/
- **口语样本（2026-09-16 补）**：①**篇级回环**——周轶君（`corpus.podcasts.ted-zhouyijun-2017`，ANNOTATED）：开场以《青花瓷》"视角可被转换"起，结尾回到"把那个过于庞大的自我先放在一边"，**以同一命题闭合话题链**（详见 `corpus/annotations/ted-zhouyijun-2017-20260916.md` 结构地图）；②**话题链收窄**——王辰（`corpus.interviews.bai-20200205-wangchen-cabin`，ANNOTATED）：12 轮问答每轮锁定单一变量（初衷→理念→安全性→确诊标准→检测→医护→容量→拐点），**话题链由宏观逐级收窄到可回答的问题**。两例说明连贯不只靠连接词：一靠命题回环，一靠变量递进。边界：均为口语语域的结构级观察，副语言衔接（停顿、语气）需听校。

## 跨来源验证（§121）

- 状态：`validated`（2026-09-16 登记）。**本次升级不依赖新增证据**，而是按 §121 对既有来源结构做评估。
- 依据：**理论**＝徐赳赳篇章语言学、冯胜利语体语法、Mann & Thompson RST、Taboada & Mann RST 综述、Ernst ERST —— **5 个独立来源，满足「≥3 个不同来源」分支**（诚实说明：本条**主要靠此分支成立**，不是靠"表达者样本"分支，中文口语样本仅 2 条）。
- 跨来源比较——**"连贯不只靠连接词"跨语域收敛，差异在装置**：
  1. 演讲体（周轶君）：**命题回环**——开场以《青花瓷》"视角可被转换"起，结尾回到"把那个过于庞大的自我先放在一边"，以**同一命题**闭合话题链；
  2. 答问体（王辰）：**变量递进收窄**——12 轮每轮锁定单一变量（初衷→理念→安全性→确诊标准→检测→医护→容量→拐点），话题链由宏观**逐级收窄**到可回答的问题；
  3. 理论侧分工：RST（Mann & Thompson／Taboada & Mann）提供**关系类型**框架，中文侧由篇章语言学（徐赳赳）与语体语法（冯胜利）提供**语体差异**依据——两侧共同支持本页 definition「话题链、因果、时间、证据与意图的对齐」，而非"多接连接词"。
- 边界：① 中文口语样本仅 2 条（两位表达者），故**不主张表达者分支**；② 副语言衔接（停顿、语气）未听校；③ `boundary_conditions`（探索性文本可保留跳跃，但跳跃须作为意义而非遗漏）**未做反例抽样**，属经验判断。
