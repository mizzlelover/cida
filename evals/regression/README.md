# Regression · 回归评测

每次修改 SKILL.md / workflows / knowledge / STYLE_SYSTEM.md 后运行。

## 三层回归

### meaning regression
对 `../benchmark/` 中带 Preservation 标注的案例重跑，核对：
原意、立场、证据、分寸是否仍然保留。任何案例失败 = 阻断合并。

### style regression
对固定输入重跑，比较输出的十维参数估计是否发生非预期偏移。
预期内的偏移（修改本来就为了调整参数）在 CHANGELOG 中说明。

### quality regression
十五维质量评分对比（见 ../../EVALS.md §1）。允许单项波动，
两项以上显著回退 = 需要人工复核。

## 记录

每次回归在 `history/` 下留档：日期、变更内容、三层结果、结论。
原则：**修一个问题，不能制造另一个问题。**
