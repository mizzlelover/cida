# Anti-pattern Library · 反模式库

反模式不是"AI 检测特征"，而是**伤害表达质量的具体病灶**。每个反模式记录：
症状（`symptom`）、伤害机理（`why_it_hurts`）、可能机制（`possible_mechanism`）、
修复策略（`repair`）、例外（`exceptions`）——以上五节为**必需小节**；
**实例**（`example`）**视证据可得**，不作强制。
Schema 见 `schemas/anti_pattern.yaml`。

**使用原则**：诊断时只报告有证据命中的反模式，并给出修复动作；
不输出"AI味87%"式百分比。

## 全库索引（23 项 = 已有完整条目 9 + 待建 14）

### 已有完整条目

| 反模式 | 文件 | 一句话症状 |
|---|---|---|
| Structural Monotony | `structural_monotony.md` | 结构清晰但机械：等长、同构、永远三点 |
| Listicle Tendency | `listicle_tendency.md` | 数量承诺冒充判断："三个原因告诉你"式并列清单 |
| AI Semantic Repetition | `ai_semantic_repetition.md` | 同一意思换着说法说三遍 |
| Template Transition | `template_transition.md` | 路牌式过渡堆砌 |
| Gold-quote Inflation | `gold_quote_inflation.md` | 每段一个金句，强行升华 |
| Fake Intimacy | `fake_intimacy.md` | 套近乎式假亲昵 |
| Abstract Inflation | `abstract_inflation.md` | 抽象大词堆叠，不落地 |
| Over / Under-explanation | `over_under_explanation.md` | 解释量与读者错配 |
| Feature Headline Opening | `feature_headline_opening.md` | 特稿标题法误用于口表开头（引语倒装钩子／破折号悬念／"抽象标签＋冒号"） |

### 待建条目（Phase 2，含一句话症状）

| 反模式 | 症状 |
|---|---|
| Artificial Completeness | 强行面面俱到的虚假完整 |
| Symmetry Bias | 为对称而对称的结构 |
| Fake Dialogue | 伪装的读者对话（"你可能会问"×5） |
| Over-questioning | 问句滥用，每两段一个"那么问题来了" |
| Over-rhetoric | 修辞过产，无处不花哨 |
| Empty Emotion | 没有事实支撑的情绪渲染 |
| Fake Story | 为观点杜撰的"我有个朋友" |
| Generic Example | 万能例子（爱迪生、爱因斯坦轮班） |
| Bureaucratic Register | 公文腔泄漏到所有文体 |
| Academic Leakage | 学术腔泄漏到大众文本 |
| Podcast Rambling | 播客式散漫进入文字 |
| Chat-log Fragmentation | 聊天记录式碎片化 |
| Knowledge-service Tone | 知识服务腔（"愿你……"式收尾） |
| Leadership-speech Tone | 领导讲话腔（排比+口号+升华） |

## 共同修复逻辑

```
1. 定位证据      —— 摘录命中位置，不凭感觉
2. 判断机制      —— 为什么会这样写？（模板惯性/填充KPI/规避判断……）
3. 选择修复      —— 删 / 合 / 改写 / 降级
4. 检查例外      —— 每个反模式都有合法使用场景，别误杀
```
