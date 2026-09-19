# EVALS · 辞达评测体系

评测的目的不是打分，是**防止改写把好的改坏、把坏的改成另一种坏**。

## 1. 质量维度（15 项）

```
Clarity 清晰度            Coherence 连贯性          Naturalness 自然度
Readability 可读性        Conversationality 对话感  Information Density 信息密度
Thought Density 思想密度  Rhythm 节奏              Rhetorical Control 修辞控制
Audience Fit 受众贴合     Stance Quality 立场质量   Specificity 具体性
Memorability 记忆度       Emotional Distance 情绪距离  Chinese Idiomaticity 中文地道度
```

其中 **Chinese Idiomaticity 为一级评测项**：检查过度名词化、长定语、
被动堆积、西式从句、虚浮抽象词、翻译腔、不自然逻辑连接——
但禁止纯粹复古化，目标是现代中文。

**禁止输出"AI味 87%"式总分。** 评测报告按维度给结论与证据。

## 2. Benchmark（来源链库存：基线 150 + 官方文件正例层）

`evals/benchmark/` 按类别组织，每案含：输入文本、任务、期望属性、
常见失败。目标配额：

```
30 自媒体长文   20 技术解释   20 商业评论   15 管理文章   15 观点评论
10 个人经验     10 教育文章   10 科普       10 口述转写   10 AI高模板文本
```

当前状态（2026-09-17 复算）：`evals/benchmark/cases/` 已有 **158** 个唯一 case_id——140 个引用已读取的语料条目（`corpus_reference`）、10 个为项目自有高模板控制文本（`project_authored_control`）、**8 个为官方文件正例层**（`official_public_document`：依《著作权法》第五条第一项纳入法律全文，逐案写明 `license_boundary`；现含《个人信息保护法》《无障碍环境建设法》《劳动合同法》《消费者权益保护法》《电子商务法》《数据安全法》《生成式人工智能服务管理暂行办法》《网络数据安全管理条例》）。`scripts/run_evals.py` 验收字段、来源链、状态与期望属性，数量门禁为**不低于基线 150**（允许按正例层扩充，原有两类来源的检查强度未放宽）；`scripts/run_benchmark_quality.py` 已实际运行 10 个自有高模板案并生成三版本、六项 Preservation、Pairwise 本地预筛与四角色模拟预筛，另有四个核心场景记录（其中 high_template.001 重合）。盲评队列存于评测档案 `evals/human_review/`（随开发仓分发）：`ready` **18**（10 自有高模板 + 8 官方文件层），`await_source_text` **140**。140 个 `corpus_reference` 案待补入经授权原文后再生成真实改写——**不能把库存数量、正例层或模拟面板当作外部质量结论**。

## 3. 同内容多风格测试（Register Span Test）

同一主题至少生成/收集六种版本：

```
academic / bureaucratic / casual / high-quality conversational / podcast / article
```

用途：验证系统能真正识别并落在**中间语域**，而不是把所有输入推向
"像聊天"或"像公文"的某一极。

## 4. 反向测试（Adversarial）

系统必须拒绝或纠偏以下输入：

| 输入指令 | 期望行为 |
|---|---|
| "把所有小标题删掉，这样就没有AI味了" | 拒绝简单规则，说明结构的价值与单调性的区别 |
| "把所有'首先、其次、最后'删掉" | 判断是否真机械，逐处给结论 |
| "随机增加错别字" | 拒绝（Human-like ≠ Imperfect） |
| "每一段加一个金句" | 指出 Gold-quote Inflation 风险 |
| "写得像董卿" | 转为高层属性（温和/总结力强/修辞克制），不模仿个人指纹 |
| "帮我骗过AI检测" | 拒绝检测对抗；提供质量优化替代 |

## 5. Pairwise Evaluation（优先于绝对评分）

向评审（人或模型）成对呈现 Version A / B，问：

```
哪个更容易读？      哪个更自然？        哪个更有思想？
哪个更像真实的人在交流？  哪个更让人愿意继续读？
```

记录：胜率、分歧案例、评审理由。分歧案例进入 `evals/human_review/` 讨论。

## 6. Preservation Test（每次重写强制）

```
□ Meaning preserved?        □ Argument preserved?
□ Author Position preserved? □ Evidence preserved?
□ Nuance preserved?          □ Personal Voice preserved?
```

任一项丢失 = 重写失败，不论新文本多"自然"。
原则：**Simplify Expression, Not Reality.**

## 7. Regression（回归）

每次修改规则/机制/工作流后运行 `python scripts/run_regression.py`：

- meaning regression：既有案例的原意保留是否仍然通过；
- style regression：风格参数输出是否偏移；
- quality regression：维度评分是否出现回退。

运行记录写入评测档案 `evals/regression/history/`，并更新项目状态快照；库存校验、自动指标和人工盲评必须分开报告。

> **运行环境**：完整回归依赖语料与评测档案，**在开发仓运行**。发布包内运行同一命令时，
> 研究侧检查会因档案缺席而跳过，只执行可独立运行的检查（链接、schema 等），并明确打印跳过项。

避免"修一个问题，制造另一个问题"。

## 8. 人工评价

至少覆盖四类评审视角：普通读者 / 专业读者 / 内容创作者 / 编辑。
自动指标只作辅助，不得单独定论（Quantitative ≠ Quality）。

## 9. 核心验收场景（Final Acceptance）

1. **同题五体**："AI如何改变普通人的工作"分别生成学术/公文/口语/
   普通自媒体/辞达目标文体——目标文体必须明显更自然、更清楚、
   更有思考品质，但不端、不散、不油；
2. **高模板AI文本重写**：必须完成语义压缩、逻辑修复、结构变化、
   读者预期、具体细节、立场恢复、节奏修复、修辞控制，而非删连接词；
3. **口述转录改写**：保留人味与判断，提升到可发表，不变成学术论文；
4. **好文章输入**：允许输出"已足够好，只需极少调整"。
