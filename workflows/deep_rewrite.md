# Deep Rewrite · 深度重写工作流

适用于高模板、长篇或结构失衡文本。它是 `rewrite_article.md` 的显式执行入口，
与 Quick Rewrite 的区别在于：先建立可回溯的论证地图，再重建结构，最后用压缩率、
Preservation 和语域检查决定是否返工。

## 输入与输出

```yaml
input:           # 原文或可访问的授权转录
audience:        # 目标读者；缺省时记录推断
platform:        # article / wechat / zhihu / video_script / podcast ...
purpose:         # 说服 / 解释 / 记录 / 连接
rewrite_level: deep
```

输出：重写稿、三行以内改动摘要，以及一份可复核的评测记录（不复制受版权保护的原文）。

## 0. 取证契约

1. 读取 `knowledge/anti_patterns/README.md` 索引，只登记文本中有证据的症状；
2. 从 `knowledge/mechanisms/GRAPH.md` 取 1–3 个最小机制集合，并读取节点的边界与修复动作；
3. 用 `STYLE_SYSTEM.md` 记录目标十维参数，平台任务再读取 `platforms/<平台>/README.md`；
4. 输入来自口述、访谈或公开转写时，先确认 `transcript_quality` 与授权边界；
5. 记录 `source → diagnosis → mechanism → transformation → preservation`，没有证据的判断降级为假说。

## 1. P0：提取与修复意义

建立一张只供内部使用的论证地图：

```text
主判断 → 支撑事实/例子 → 推理桥 → 限定条件 → 反方疑问 → 可执行结论
```

- 标出空话、同义重复和“只有好处没有代价”的断点；
- 先修错误归因、跳步和证据错配，再考虑句式；
- 原文没有可反驳判断时，停止“润色”，告知用户需要先补判断。

## 2. P1：重建结构

- 按读者认知顺序重排，不按原文段落顺序搬运；
- 让每段承担不同职责，禁止机械三点、等长段落和每段同一语法开头；
- 读者可能反驳的地方提前补限定或例子；
- 保留必要的证据、数字和作者位置，不为了“自然”删除现实复杂度。

## 3. P2–P4：表达、节奏与峰值

- 连接词只保留真实转折、因果、让步或共同注意功能；
- 名词化、长定语和被动堆积按受众与媒介拆解；
- 句长变化由意义推动，朗读检查呼吸；
- 通过 `rhetorical_peak` 的 Quote-worthiness Filter，全文只留少量有论证承重的峰值句；
- 结尾选择一个动作（判断、行动、留问或回扣），不重复前文或强行升华。

## 4. 量化自检（仅作辅助）

对项目自有测试文本可以计算：

- 去空白字符压缩率：`1 - len(output) / len(input)`；
- 机械标记计数（“首先/其次/最后/总之”等）；
- 关键实体、数字、限定词保留率；
- 段落和句长分布变化。

压缩率不是质量目标。若压缩导致 Meaning、Argument、Author Position、Evidence、Nuance 或 Personal Voice 任一项下降，
即使达到阈值也判失败并回退到较轻改写。

## 5. 强制评测记录

> **适用场景**：本节的并列存档与 Pairwise 用于**开发／评测**场景；日常重写只需交付
> 成稿 + 改动摘要（见「输入与输出」），不必生成下列全套记录。

并列保存：

1. Original；
2. Baseline Rewrite（只做轻度整理）；
3. New Skill Rewrite（本流程）；
4. Preservation 表（Meaning / Argument / Author Position / Evidence / Nuance / Personal Voice）；
5. Pairwise 问题（易读、自然、思想、交流感、继续阅读意愿）。

Pairwise 结果若来自模型预筛，必须明确标注；需要人工或模拟四类评审时，保存角色、评分、
理由与分歧，不能把自动指标写成人工结论。

## 6. 交付前闸门

```text
□ 原意、立场、证据、分寸均保留
□ 结构变化解决了已诊断的问题，而非为了变化而变化
□ 压缩率与标记计数已核算（适用时）
□ 目标平台和十维 Profile 对齐
□ 机制、来源与版权边界可回溯
□ Pairwise / Preservation 记录已分开
```

任一项不通过，返工对应优先级；不把一份报告或一次库存检查当作质量完成。
