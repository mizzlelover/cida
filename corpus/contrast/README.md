# Contrast Corpus · 对照语料库（Negative Corpus）

研究「什么有效」必须同时研究「什么失效」（§123–124）。
本库收集反面样本，用于对照分析与反模式库的证据支撑。

## 收录范围

```
过度书面      过度口语      AI模板化      领导讲话腔    知识服务腔
过度金句      营销腔        鸡汤腔        流水账        播客式啰嗦
```

## 采样原则

- 与主语料一样遵守版权原则：只存元数据、短分析片段与标注；
- 必须实际阅读/取得内容（§112 同样适用），禁止凭印象定性；
- 抽样覆盖 excellent / good / average / problematic 四档，
  不得只收"金句最多、传播最好"的文本（§123）；
- 每条记录：失效点是什么 → 为什么失效 → 对应哪个反模式
  （`knowledge/anti_patterns/`）→ 修复示范（可选）。

## 条目模板

沿用 `schemas/corpus_item.yaml`，`source_type` 标注 `contrast`，
并在 `overuse_risks` / `analysis_notes` 中记录失效机理。
