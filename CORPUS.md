# CORPUS · 语料库规划与登记

语料库是辞达最重要的资产之一。原则：**Theory explains Corpus, Corpus corrects
Theory**——语料库与理论库并行建设、互相校正，禁止"先把理论做完再补语料"。

## 版权原则（先读这条）

- 公开语料仅用于**分析语言机制**（usage: analysis_only）；
- 不存储、不分发受版权保护的完整访谈或文章全文；
- 本仓库只保存：来源元数据、短分析片段、特征标注、机制抽取；
- 自动转录文本必须降级标注（transcript_quality），未核对的自动转录
  不得用于句法与措辞精细分析。

## 类别与配额（第一期目标 650+）

| 类别 | 目录 | 一期目标 | 重点 |
|---|---|---|---|
| 即兴评论 | `commentary/` | 100 | 白岩松《新闻1+1》《东方时空》：切题、判断、压缩 |
| 主持人现场点评 | `hosting/` | 60+ | 《主持人大赛》：董卿/康辉/撒贝宁完整点评（非金句合集） |
| 深度访谈 | `interviews/` | 100 | 杨澜/王志/鲁豫/柴静/董倩：问题链与追问 |
| 知识谈话 | `podcasts/` 等 | 100 | 窦文涛《锵锵三人行》及中文知识型播客 |
| 准备型演讲 | `speeches/` | 100 | 《开讲啦》《一席》、学者演讲；TED 仅作 scripted 补充 |
| 播客 | `podcasts/` | 100 | 声东击西、忽左忽右等（按筛选原则，不因热门入库） |
| 博客/自媒体 | `blogs/` | 200 | 阮一峰、和菜头、CoolShell、刘未鹏等 |
| Raw→Edited 对照 | `raw_edited_pairs/` | 50 组 | 字幕 vs 官方整理稿的编辑学 |

长期目标：2000+，再 5000+。

## 主持人名单（第一批 12+6）

核心 12：董卿、白岩松、康辉、撒贝宁、窦文涛、杨澜、敬一丹、王志、
鲁健、崔永元、水均益、柴静。
专项扩展 6：陈鲁豫、倪萍、周涛、何炅、董倩、邹韵。

**明确排除**：许知远。原因：本项目筛选"高质量口头表达示范"，
不是"有思想的人"——思想质量与口头表达质量分开评估。

## 铁律

1. 主持人不是 Style Preset：Speaker → Ability → Mechanism →
   Cross-speaker Comparison → Transferable Pattern；
2. 每个样本必须同时记录 strengths / weaknesses / overuse_risks
   （优秀语料 ≠ 全盘学习）；
3. TED 类一律标注 `preparedness: scripted`（Crafted Speech，非即兴会话）；
4. 金句合集不入库——只收完整或相对完整的样本；
5. 扩充博客/专栏作者须满足七条中至少三条（见需求文档 §30：
   长期稳定写作、公开完整文本、明显个人判断、非 SEO、非软文、
   持续读者认可、可分析价值）。

## 技术规范

- 语料分两层：`corpus/candidates/`（候选池，只登记线索与采集计划）与
  `corpus/<类别>/`（正式库，必须实际取得内容并附 Evidence Package）；
- 正式条目遵循 `schemas/corpus_item.yaml`（§113 证据包 + §129 状态机），
  候选条目遵循 `schemas/candidate.yaml`；
- 原文与分析分离：`raw/`（合法可存的原始材料）、`normalized/`（清洗文本）、
  `annotations/`（机制分析）、`metadata/`（登记信息）四层（§125）；
- 对照语料（Negative Corpus）入 `corpus/contrast/`（§124）；
- 用 `python scripts/validate_schemas.py` 校验结构；
- 用 `python scripts/audit_research.py` 做诚信审计并生成
  `CORPUS_COVERAGE.md`（覆盖率报告，§118）；
- 用 `python scripts/build_corpus_index.py` 重建 `corpus/INDEX.md`。

## 当前状态（诚实声明）

截至 v0.2：正式库含 1 条真实采集并标注的样本（阮一峰周刊 409 期，
state: ANNOTATED），其余线索均在候选池。**各 Gate 均未达标，
语料建设不得宣称完成。** 覆盖率实况见 `CORPUS_COVERAGE.md`。
