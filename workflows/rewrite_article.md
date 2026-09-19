# Workflow B：整篇重写（rewrite_article）

输入一篇已有文章，输出真正更好的版本。**先诊断，后动手。不得直接换词。**

长篇、高模板或结构失衡文本进入 `workflows/deep_rewrite.md`；本文件保留通用整篇重写流程。

## 流程

### 0. Knowledge Retrieval Contract — 诊断必须有回溯

- 诊断前读取 `knowledge/anti_patterns/README.md` 索引，只选择与文本症状相符的反模式；
- 依据问题所在段落，从 `knowledge/mechanisms/GRAPH.md` 取对应机制节点，连同“边界、滥用风险、修复动作”一起读取；
- 语域和节奏参数以 `STYLE_SYSTEM.md` 为坐标，必要时对照 `knowledge/anti_patterns/README.md` 索引做反向校准；
- 口述来源必须按 `workflows/oral_to_article.md` 的保真边界核对，主持/访谈来源只借鉴任务机制，不复制个人句式；
- Explain 模式记录机制节点和来源条目，无法回溯的判断降级为工作假说，不写成已验证规律。

### 1. 诊断（内部完成，默认不输出）

按 `workflows/diagnose_text.md` 完成十项诊断。诊断结论决定改什么、不改什么。

特别检查**结构单调性**（Structural Monotony）——结构清晰不是罪，机械才是：

- 每一节长度完全一样；
- 每段都先结论后解释；
- 每个一级标题都是同一语法结构；
- 永远是三点。

命中两条以上 → 结构重建进入 P1。

### 2. 分级执行

```
P0 意义与逻辑
   - Claim Extraction：把全文真正的观点列出来
   - Argument Repair：找出断裂的推理（跳步、循环论证、论据不支撑结论）
   - Redundancy Removal：删掉同义反复的段落（AI Semantic Repetition）
   - 输入没有观点 → 停下来告诉用户：这篇文章缺的不是润色，是判断

P1 结构与清晰
   - 重排顺序：按读者的认知顺序，不是按作者写稿的顺序
   - 调整详略：重要的展开，次要的压缩
   - 打破机械对称：各节长度、写法允许不同

P2 流转与语域
   - Transition：优先通过论证关系自然转场，而不是"接下来我们来看"
   - Register：对照受众与平台，整体校准正式度/口语感

P3 节奏与修辞
   - Rhythm Repair：长句拆或短句合，由意义推动
   - Rhetorical Control：删掉不承担功能的修辞；把真正的好句子放在峰值位置
   - 口表硬规则（用户裁定，2026-09-12）：开头必须"能说出口"——正常语序直陈；
     禁止倒装悬念标题与元叙述框架句（"先拆某词""从这个细节开始"）；
     念出来不像人开口的，重写（`knowledge/anti_patterns/feature_headline_opening.md`）

P4 打磨
   - 措辞精度、删繁就简、统一术语
```

### 3. Preservation Test（强制执行）

重写完成后逐项核对：

```
□ Meaning preserved?         原意保留了吗？
□ Argument preserved?        推理关系、论证方向保留了吗？
□ Author Position preserved? 作者的立场、分寸、不确定性保留了吗？
□ Evidence preserved?        证据、数据、引语一个没少吗？
□ Nuance preserved?          那些"在某种条件下""至少目前来看"的限定还在吗？
□ Personal Voice preserved?  用户已有的语气和人格线索是否被抹平？
```

任何一项丢失 → 视为重写失败，恢复并改从更轻的级别重新处理。

### 4. 例外：好文章的权利

如果诊断结论是"这篇文章本来就写得很好"：

> 明确输出：当前文章已经足够好，只需极少调整。
> 列出至多 3 处可选微调，并说明为什么其余部分不动。

**禁止**为了显得"做了工作"而打乱结构、删除分点、增加随意语气。

## 输出格式

默认：重写稿 + 改动摘要（按 P0–P4 分组，每条一行，说明改了什么、为什么）。
Explain 模式：附完整十项诊断 + 每处改动的机制引用（`knowledge/mechanisms/` 节点名）。
