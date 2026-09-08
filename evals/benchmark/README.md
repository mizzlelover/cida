# Benchmark 语料库（种子框架）

目标 150 案（配额见 ../EVALS.md §2）。当前状态：**v0.1 种子版**，
先建规范与样例，持续扩充。

## 单案格式

```yaml
id: bench.<category>.<nnn>
category: ""          # self_media / tech_explainer / business / management /
                      # opinion / personal / education / science / oral / high_template
input_text: ""        # 输入（可指向文件）
task: ""              # rewrite / topic_to_article / oral_to_article / ...
expected_properties: []   # 期望属性（可检验的）
common_failures: []       # 已知常见失败
source: ""                # 来源与版权说明
```

## 种子案例

### bench.high_template.001（AI 高模板文本重写）

- **输入**：见 `cases/high_template_001_input.txt`——一篇"数字化转型重要性"
  的高模板文本（语义重复、空总结、永远三点、强行升华全中）；
- **任务**：Deep Rewrite；
- **期望属性**：语义压缩至少 40%；出现一个真判断；结构不再机械对称；
  无升华式结尾；
- **常见失败**：只删连接词；保留"重要性"空话；结尾换汤不换药的升华。

### bench.register_span.001（同题多语域）

- **输入**：主题"AI 如何改变普通人的工作"；
- **任务**：分别生成 academic / bureaucratic / casual /
  high-quality conversational / podcast / article 六版；
- **期望属性**：六版在十维参数上可区分；目标文体版落在默认 Profile 区间。

## 采集规范

- 真实文本须注明来源与版权状态；受版权保护文本只存元数据+短摘录；
- AI 生成文本须注明生成模型与提示词；
- 每案必须有至少一条**可检验的**期望属性（不接受"更好"这类描述）。
