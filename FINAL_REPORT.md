# FINAL_REPORT · 辞达语料实采与知识蒸馏阶段报告（v0.3.0）

日期：2026-09-08 · 执行：辞达主理 Agent · 范围：强制补丁（第三部分）要求的
语料实采、知识蒸馏、真实评测

## 一句话结论

博客语料实采与蒸馏链路**已真实跑通并校准进知识库**（139 篇入库、2 篇精读
VALIDATED、3 个知识文件被真实统计修订、1 个 benchmark 实跑并暴露流程缺陷）；
但总体覆盖率**远未达标**（Gate 判定 7 类中 7 类未达标），对话体语料在本环境
**无法合法规模化获取**，本报告按 §130 如实记录限制与替代路线。

## 一、真实完成量（全部可复核）

### 语料实采

| 来源 | 条数 | 状态 | 复核入口 |
|---|---:|---|---|
| 阮一峰周刊 | 82（期 1–411，每隔 5 期抽样；**261 期为作者跳号**，已实测 2022–2025 全月不存在） | READ×80 / VALIDATED×1（406 期精读） / ANNOTATED×1（409 期） | `corpus/blogs/ruanyifeng_weekly_*.yaml`、`corpus/metadata/ruanyifeng_weekly_features.json` |
| CoolShell（陈皓） | 56（列表页 1–8；1 篇 404、1 篇跳过） | READ×55 / VALIDATED×1（22298 精读） | `corpus/blogs/coolshell_*.yaml`、`corpus/metadata/coolshell_features.json` |
| 和菜头 / mindhacks | 0 | **本机网络不可达**（TCP/TLS 失败，已实测两种协议与 www 变体） | 本报告「能力限制」 |

合计 **139 条正式语料 + 2 条候选**，schema 校验 190 条记录全绿。

### 知识蒸馏（真实写回，非报告话术）

1. `knowledge/mechanisms/rhythm.md` 新增「语料校准」：平均句长中位 38.2 字
  （p25 36.7 / p75 39.6）、句长峰值中位 112 字——推翻"优秀=短句"直觉，
   确立"段内长短交替"为节奏本源（n=82，编辑体限定）。
2. `knowledge/mechanisms/discourse_markers.md` 新增「语料校准」：标记密度中位
   1.78/千字；"但是"覆盖 82/82 期（转折刚需），"更重要的是"仅 4/82（峰值标记
   是稀缺资源）。
3. `STYLE_SYSTEM.md` 新增「语料校准记录」表：5 条观察 → 参数空间含义，
   含跨作者对照（陈皓句长均值 66.8、标记密度 4.07/千字、加粗 20.7/篇，
   约为阮刊的 1.7 / 2.3 / 4 倍）。
4. `corpus/contrast/ruanyifeng_vs_coolshell_20260908.md`：跨来源对照分析，
   产出 3 条参数空间校准含义（含"高 Orality ≠ 必然短句"的修正）。

### 真实评测

`evals/benchmark/results/high_template_001_result.md`：Deep Rewrite 实跑。
**第一版压缩率 36.5% 未过线（≥40%），修订后 40.4% 通过（边际）**；
Preservation 四项全过；Pairwise 模型预筛五题全胜（按协议人工评审待补，
不作定论）。暴露并记录 2 条工作流缺陷（压缩率自检缺失、真判断判定无启发式）。

## 二、Gate 判定实况（摘自 CORPUS_COVERAGE.md，未达标不粉饰）

commentary 0/100 ❌ · interviews 0/100 ❌ · hosting 0/60 ❌ ·
speeches 0/100 ❌ · podcasts 0/100 ❌ · blogs 139/200 ❌ ·
raw_edited_pairs 0/50 ❌

**Corpus Construction 未达成，不得宣称完成。** 当前有效能力域：
**书面解释体/论证体（技术自媒体类）**，有实采统计与精读对照支撑；
对话体、口播体、主持体仍为假说级能力。

## 三、能力限制（§130 如实记录）

1. **TV/播客 transcript 无法规模化合法获取**：主流平台字幕有访问控制与
   版权限制，本环境无授权渠道。替代路线：用户提供自有转写 → 走
   `corpus/raw/` 授权通道；或改用 CC 协议/官方公开文字稿（如部分政府
   发布会实录、播客 shownotes 自愿公开文本），逐案核版权后入库。
2. **和菜头（hecaitou.net/.com）、mindhacks.cn 本机网络不可达**
  （连接级失败，非 403）。需在可访问网络环境补采，或换源
   （如阮一峰 essays 频道、公开 newsletter 存档）。
3. **coolshell.cn 对 Python TLS 指纹返回 500**：采集改走 curl 通道
   （已固化进 `scripts/acquire_coolshell_corpus.py`）。
4. **精读产能**：机器特征可批量，ANNOTATED 以上必须逐篇精读；
   当前 VALIDATED 仅 2 篇。升 DISTILLED 的模式已在知识库落地
   （机制级），条目级 DISTILLED 待下一轮。

## 四、下一轮路线（按边际价值排序）

1. 博客补到 200：阮一峰 essays 频道 + 可达的中文技术博客（先查 robots）。
2. raw_edited_pairs 50 对：从用户真实改写任务中经授权沉淀（最快合法路径）。
3. commentary 100：可公开访问的媒体评论存档（核验各站 robots 与版权页）。
4. 对话体来源：播客公开 shownotes、发布会官方实录，逐案核版权。
5. 人工评审补位：high_template.001 的 Pairwise 人工评审；精读 3–5 篇升
   ANNOTATED→VALIDATED。

## 五、合规与诚信声明

- 全部语料仅存元数据+计算特征+≤80 字摘录，不存全文、不再分发、
  不用于模型训练；各站 robots/内容信号已逐站核查并写入条目
  `copyright_notes`。
- 本报告所有数字可由 `scripts/audit_research.py`、`validate_schemas.py`、
  `build_corpus_index.py` 复算。
