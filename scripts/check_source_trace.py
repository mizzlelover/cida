#!/usr/bin/env python3
from __future__ import annotations

import collections
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from blind_keys import declared_key_file, load_key_sources, load_keys  # noqa: E402

try:
    import process_blind_review  # noqa: E402
except Exception:  # pragma: no cover - 缺依赖时降级为"不校验揭盲函数"
    process_blind_review = None

# 走聚合分析文档、不要求逐条标注档的语料类别（约定豁免，脚本会如实计数上报）
EXEMPT_CATEGORIES = {"raw_edited_pairs", "contrast"}
# "记录/汇总"类文档：它们会提到条目 id，但不是该条目的精读标注档，
# 故不计入"已挂到标注档"的证据池（否则任何抽查记录提到一次就算通过，闸门失去意义）。
RECORD_DOC_PREFIXES = (
    "spotcheck", "url-liveness", "listening-checklist", "README", "pair-preservation-audit",
    "cctv-source-rot", "oral-register-recalibration", "host-", "hosting-", "prepared-speeches-",
    "shanghai-press-conferences-", "qa-sample-",
)
# 机制节点可合法关联到的根文档（与 build_mechanism_graph.py 的 ROOT_DOCS 保持一致）
ROOT_DOCS = {"STYLE_SYSTEM.md", "EVIDENCE.md"}


def main() -> int:
    registry = yaml.safe_load((ROOT / "knowledge" / "sources" / "registry.yaml").read_text(encoding="utf-8")) or []
    source_ids = {str(x.get("source_id")) for x in registry}
    # 语料 id 索引（2026-09-16 新增闸门）：此前只检查 `corpus/` 路径是否存在，
    # 节点里写的 `corpus.<category>.<slug>` 若拼错（如 named- 与 named. 之差）不会被发现。
    corpus_ids: set[str] = set()
    for item in (ROOT / "corpus").rglob("*.yaml"):
        # 2026-09-17 第三十九批：`corpus_id` 后若带内联注释，旧写法会把注释并进 id
        # （表现为"语料库不存在"的**假失败**）；此处先去注释再取 id。
        m = re.search(r"^corpus_id:\s*(.+)$", item.read_text(encoding="utf-8"), re.MULTILINE)
        if m:
            corpus_ids.add(m.group(1).split("#", 1)[0].strip().strip('"'))
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0
    id_refs = 0
    linked = 0
    exempt = 0
    unlinked = 0
    state_comments = 0  # 2026-09-17 第三十九批：`state` 行带内联注释的条目数（已容错计数、显式上报）
    # corpus id 的书写形态（2026-09-16 第二十二批修正）：**必须包含汉字**——
    # 库内实测 **50 个 id 含汉字**（如 `corpus.hosting.gaokzx-82199-沈倩`），旧正则为
    # `[A-Za-z0-9_.-]+`，会把 `…-沈倩` **截断成 `…-`**：若节点引用了这类真实 id，闸门会报"语料库不存在"的
    # **假失败**；反之若把真 id 写错一个汉字，截断后也可能**恰好匹配不上**而漏报。
    # 与第十九批"README 结构树看不见 `└──`"同族：**判据的字符集写窄了**。
    ID_RE = r"\bcorpus\.[a-z_]+\.[A-Za-z0-9_.\-\u4e00-\u9fff]+"
    # 历史/探针语境里的 id 提及不算"当前引用"（撤销的重复条目、复算用的假 id、探针名），
    # 否则勘误文本与探针留痕会被闸门读成悬空引用——**范围写宽了会制造假失败**。
    HISTORICAL_MARKERS = ("撤销", "勘误", "去重", "探针", "probe", "no-such-entry", "probe-no-doc")
    for path in sorted((ROOT / "knowledge" / "mechanisms").glob("*.md")):
        if path.name in {"README.md", "GRAPH.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "## sources" not in text:
            errors.append(f"{path.relative_to(ROOT)}: 缺少 sources 段")
            continue
        checked += 1
        # 2026-09-16 第十九批：扫描范围由 `## sources` 段**放宽到整篇**——此前只在这个段里取
        # `src.*` 与 `corpus.*` 引用，节点在正文/`§121` 小节里写的引用**完全不在覆盖内**
        # （实测全篇 146 处 src. 引用、130 处 corpus 引用，均存在；宽松化后覆盖面变大而不产生假失败）。
        ids = re.findall(r"\bsrc\.[A-Za-z0-9_.-]+", text)
        for source_id in ids:
            if source_id not in source_ids:
                errors.append(f"{path.relative_to(ROOT)}: registry 不存在 {source_id}")
        for corpus_id in sorted(set(re.findall(ID_RE, text))):
            id_refs += 1
            if corpus_id not in corpus_ids:
                errors.append(f"{path.relative_to(ROOT)}: 语料库不存在 {corpus_id}")
        source_block = text.split("## sources", 1)[1].split("## ", 1)[0]
        refs = re.findall(r"`([^`]+)`", source_block)
        for ref in refs:
            if ref.startswith("corpus/"):
                target = ROOT / ref
                if not target.exists():
                    warnings.append(f"{path.relative_to(ROOT)}: corpus 引用不存在 {ref}")
    # 语料 id 存在性：**跨载体**收口（2026-09-16 第二十二批扩展）——原判据只扫机制节点，
    # 于是另两处最常写 id 的地方**完全不在覆盖内**：①语料条目之间的互相引用（实测 51 处，
    # 如 `raw_edited_pairs/pair-041` 指回 `corpus.hosting.gaokzx-82199-沈倩`）；
    # ②`corpus/annotations/*.md` 标注档正文（实测 32 处，非 spotcheck 文档）。
    # 抽查/探针类文档（`spotcheck*`，21 处引用）**沿用第十二批的证据池排除**并计数上报。
    cross_refs = 0
    cross_skipped = 0
    for carrier, files in (
        ("语料条目", [p for p in (ROOT / "corpus").rglob("*.yaml") if p.name != "index.yaml"]),
        ("标注档", [p for p in sorted((ROOT / "corpus" / "annotations").glob("*.md"))
                    if not p.name.startswith(RECORD_DOC_PREFIXES)]),
    ):
        for path in files:
            text = path.read_text(encoding="utf-8")
            for line in text.splitlines():
                if any(mark in line for mark in HISTORICAL_MARKERS):
                    cross_skipped += len(re.findall(ID_RE, line))
                    continue
                for corpus_id in sorted(set(re.findall(ID_RE, line))):
                    if re.match(r"^\s*corpus_id:\s*[\"']?" + re.escape(corpus_id), line):
                        continue
                    cross_refs += 1
                    if corpus_id not in corpus_ids:
                        errors.append(
                            f"{path.relative_to(ROOT)}: 语料库不存在 {corpus_id}"
                            f"（{carrier}内引用，原判据只扫机制节点）"
                        )
    print(f"跨载体语料 id 引用：{cross_refs} 处受检（语料条目互引 + 非抽查类标注档），"
          f"历史/探针语境跳过 {cross_skipped} 处，`{sorted(RECORD_DOC_PREFIXES)}` 类文档不纳入（沿用证据池排除）")
    # 语料 ⇄ 标注档 可追溯性（2026-09-16 第十二批新增闸门）：非豁免类别中，凡 state 为
    # ANNOTATED / VALIDATED 的条目，必须被至少一份 corpus/annotations/*.md **以 corpus_id 引用**，
    # 否则"已精读"这一状态没有可机读的证据落点。raw_edited_pairs 与 contrast 走聚合分析文档
    # （raw_edited_official_pairs_20260910.md、20260910-negative-corpus.md 等），按约定豁免并如实计数。
    annotation_text = " ".join(
        p.read_text(encoding="utf-8")
        for p in (ROOT / "corpus" / "annotations").glob("*.md")
        if not p.name.startswith(RECORD_DOC_PREFIXES)
    )
    # 配对结构字段（2026-09-17 第二十九批新增闸门）：`schemas/raw_edited_pair.yaml` 定义的
    # 配对结构字段**此前从未被任何检查读到**——`validate_schemas.py` 把 `corpus/**/*.yaml`
    # 一律按 `corpus_item.yaml` 模板校验，配对模板不在其取值路径上，于是 pair-066..068
    # 长期缺 `raw_text`／`edited_text`／`edit_operations` 等字段而回归全绿（"缺了但全绿"同族）。
    # 现按模板要求**字段齐备**，并对承载证据与分析的字段要求非空；`meaning_preserved` 为布尔，`False` 是合法值。
    pair_template = yaml.safe_load(
        (ROOT / "schemas" / "raw_edited_pair.yaml").read_text(encoding="utf-8")
    )
    pair_keys = list(pair_template.keys())
    # 「必须非空」只对承载配对证据与转换分析的字段；`rhetorical_features`／`counterexamples`
    # 等**允许为空**（本批实测 pair-056..064 有多条为 `[]`，含义是"无辞格／无边界正例"），
    # 但**必须显式声明**——沿用"如实记录、不强制"的既有口径，不为求全绿制造假失败。
    pair_must_nonempty = (
        "pair_id", "corpus_id", "state", "title", "speaker_or_author", "date",
        "source_url", "source_owner", "raw_text", "edited_text", "raw_provenance",
        "authorization", "edited_by", "edit_operations", "meaning_preserved",
        "analysis_notes", "boundary", "content_obtained", "copyright_notes",
    )
    pair_checked = 0
    pair_missing = 0
    for item in sorted((ROOT / "corpus" / "raw_edited_pairs").glob("*.yaml")):
        data = yaml.safe_load(item.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            errors.append(f"{item.relative_to(ROOT)}: 不是有效的 YAML 映射")
            continue
        absent = [k for k in pair_keys if k not in data]
        empty = [k for k in pair_must_nonempty if k in data and data[k] in ("", [], None)]
        if data.get("meaning_preserved") is False:
            empty = [k for k in empty if k != "meaning_preserved"]
        pair_checked += 1
        if absent or empty:
            pair_missing += 1
            detail = []
            if absent:
                detail.append(f"缺字段 {absent}")
            if empty:
                detail.append(f"字段为空 {empty}")
            errors.append(
                f"{item.relative_to(ROOT)}: 配对结构不完整 -> {'；'.join(detail)}"
                "（模板 schemas/raw_edited_pair.yaml）"
            )
    print(f"配对结构字段：{pair_checked} 份配对受检，结构不完整 {pair_missing} 份")
    for item in (ROOT / "corpus").rglob("*.yaml"):
        text = item.read_text(encoding="utf-8")
        # 2026-09-17 第三十九批：`state` 行**允许尾随内联注释**（旧正则用 `$` 锚定，
        # 把带注释的条目**静默排除出"标注档挂载"闸门**——实测漏掉 `ruanyifeng_weekly_409` 1 条，
        # 该条其实已被标注档以 `corpus_id` 引用）。现改为容错计数，并**显式上报**带注释条数。
        state = re.search(r'^state:\s*"?(\w+)"?\s*(?:#.*)?$', text, re.MULTILINE)
        if state and re.search(r'^state:\s*"?\w+"?\s+#', text, re.MULTILINE):
            state_comments += 1
        cid = re.search(r"^corpus_id:\s*(.+)$", text, re.MULTILINE)
        if not state or state.group(1) not in {"ANNOTATED", "VALIDATED"} or not cid:
            continue
        corpus_id = cid.group(1).split("#", 1)[0].strip().strip('"')
        category = item.relative_to(ROOT / "corpus").parts[0]
        if category in EXEMPT_CATEGORIES:
            exempt += 1
        elif corpus_id in annotation_text:
            linked += 1
        else:
            unlinked += 1
            errors.append(
                f"{item.relative_to(ROOT)}: {corpus_id} 已标 ANNOTATED/VALIDATED，"
                "但无标注档以 corpus_id 引用它（状态先于证据）"
            )
    # related_nodes 目标必须可解析（2026-09-16 新增闸门）：旧图脚本对无法解析的关联**静默丢弃**，
    # 于是"悬空关联"与"大小写不符"都能长期潜伏（实测因此少记 23 条关系）。
    mechanism_files = {
        p.name for p in (ROOT / "knowledge" / "mechanisms").glob("*.md") if p.name not in {"README.md", "GRAPH.md"}
    }
    anti_pattern_files = {
        p.name for p in (ROOT / "knowledge" / "anti_patterns").glob("*.md") if p.name != "README.md"
    }
    related_ok = 0
    related_bad = 0
    related_no_section = 0
    for path in sorted((ROOT / "knowledge" / "mechanisms").glob("*.md")):
        if path.name in {"README.md", "GRAPH.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        section = re.search(r"## related_nodes\s*\n+(.+?)\n## ", text, re.MULTILINE | re.DOTALL)
        if not section:
            related_no_section += 1
            errors.append(f"{path.relative_to(ROOT)}: 缺少 related_nodes 段")
            continue
        for name in re.findall(r"([A-Za-z_]+\.md)", section.group(1)):
            if name in mechanism_files or name in anti_pattern_files or name in ROOT_DOCS:
                related_ok += 1
            else:
                related_bad += 1
                errors.append(
                    f"{path.relative_to(ROOT)}: related_nodes 指向不存在的文件 {name}"
                    "（旧版图脚本会静默丢弃此类悬空关联）"
                )
    # 机制 ⇄ 反模式 双向登记（2026-09-16 新增闸门）：机制节点在 related_nodes 里列为"过度风险"的
    # 反模式，其文件必须以 `../mechanisms/x.md` 反指该机制；反之亦然。否则读任一侧都找不到另一侧。
    # 只按两种**可靠模式**取引用：机制侧只看 related_nodes 段内的 `*.md`；反模式侧只看
    # `../mechanisms/x.md` 形式的相对路径（避免把日期型文件名等无关 token 误判为引用）。
    anti_texts = {}
    for path in (ROOT / "knowledge" / "anti_patterns").glob("*.md"):
        if path.name != "README.md":
            anti_texts[path.name] = path.read_text(encoding="utf-8")
    forward: dict[str, set[str]] = {}
    for path in sorted((ROOT / "knowledge" / "mechanisms").glob("*.md")):
        if path.name in {"README.md", "GRAPH.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        section = re.search(r"## related_nodes\s*\n+(.+?)\n## ", text, re.MULTILINE | re.DOTALL)
        if not section:
            continue
        for name in set(re.findall(r"([a-z_]+\.md)", section.group(1))) & set(anti_texts):
            forward.setdefault(path.name, set()).add(name)
    backward: dict[str, set[str]] = {}
    asymmetry = 0
    for anti_name, text in anti_texts.items():
        refs = set(re.findall(r"\.\./mechanisms/([A-Za-z0-9_.-]+\.md)", text))
        backward[anti_name] = refs
        for ref in refs:
            if ref not in mechanism_files:
                asymmetry += 1
                errors.append(f"knowledge/anti_patterns/{anti_name}: 反指机制不存在 {ref}")
    pairs = 0
    for mech_name, anti_names in forward.items():
        for anti_name in anti_names:
            pairs += 1
            if mech_name not in backward.get(anti_name, set()):
                asymmetry += 1
                errors.append(
                    f"knowledge/anti_patterns/{anti_name}: 未反指机制 {mech_name}"
                    "（机制侧 related_nodes 已登记，反模式侧缺反指——双向登记缺口）"
                )
    for anti_name, mech_names in backward.items():
        for mech_name in mech_names:
            if anti_name not in forward.get(mech_name, set()):
                asymmetry += 1
                errors.append(
                    f"knowledge/mechanisms/{mech_name}: 未在 related_nodes 登记反模式 {anti_name}"
                    "（该反模式已反指本节点——双向登记缺口）"
                )
    # 机制节点结构 ⇄ `schemas/mechanism.yaml` 声明（2026-09-16 第十九批新增）：
    # `mechanism.yaml` 与 `knowledge/mechanisms/README.md` 都把"节点 = definition／mechanism／
    # realizations／boundary_conditions／overuse_risk／repair_strategy／related_nodes／sources"
    # 当作节点结构，但**没有任何检查**过它：`detect_uncited_claims.py` 只查定义／边界／修复／来源四块，
    # 于是 `metaphor_analogy.md` 长期没有 `## mechanism` 与 `## realizations`、
    # `discourse_markers.md` 长期没有 `## realizations`——**又一处"缺了但全绿"**。
    # 判据：以**实际形态**为准——凡 ≥90% 节点都有的小节，每个节点都必须有；
    # `examples`／`counterexamples` 在节点里**只有 3/41 以小节形式出现**（内容多由
    # `§121` 小节与正文样本块承载），故**不强制**，如实记录而不设假闸门。
    section_required = ["definition", "mechanism", "realizations", "boundary_conditions",
                        "overuse_risk", "repair_strategy", "related_nodes", "sources"]
    section_gap = 0
    for path in sorted((ROOT / "knowledge" / "mechanisms").glob("*.md")):
        if path.name in {"README.md", "GRAPH.md"}:
            continue
        heads = set(re.findall(r"^## (\S+)", path.read_text(encoding="utf-8"), re.MULTILINE))
        missing = [s for s in section_required if s not in heads]
        if missing:
            section_gap += 1
            errors.append(
                f"{path.relative_to(ROOT)}: 缺小节 {missing}"
                "（`schemas/mechanism.yaml` 与本目录 README 均声明为节点结构）"
            )
    print(f"机制节点结构：{len(section_required)} 个小节 × {len(mechanism_files)} 个节点受检，缺小节 {section_gap} 个")
    # schema ⇄ 受检小节一致性（2026-09-19 补，N9）：上面 8 小节清单**硬编码**，
    # 而 `schemas/mechanism.yaml` 独立声明同一结构——第六十五批实测二者已漂移
    # （schema 写 4 个独立 realization 键，节点实际统一 `## realizations`，**全绿存活**）。
    # 判据：受检小节必须都在 schema 顶层键中；schema 中除 front-matter 键
    # （`id`／`name`／`function`）与可选键（`examples`／`counterexamples`）外的顶层键，
    # 也必须都在受检小节内——两侧任一漂移即报错。
    mech_schema_keys = [
        line.split(":", 1)[0].strip()
        for line in (ROOT / "schemas" / "mechanism.yaml").read_text(encoding="utf-8").splitlines()
        if line and not line.lstrip().startswith("#") and ":" in line
    ]
    front_keys = {"id", "name", "function", "examples", "counterexamples"}
    schema_sections = [k for k in mech_schema_keys if k not in front_keys]
    only_gate = [s for s in section_required if s not in mech_schema_keys]
    only_schema = [s for s in schema_sections if s not in section_required]
    if only_gate or only_schema:
        errors.append(
            "schemas/mechanism.yaml 与第 ⑭ 条受检小节不一致："
            f"仅受检有 {only_gate}；仅 schema 有 {only_schema}"
            "（结构声明不得漂移）"
        )
    print(f"机制 schema 一致性：受检 {len(section_required)} 小节 ⇄ schema {len(schema_sections)} 键，"
          f"漂移 {len(only_gate) + len(only_schema)} 处")
    # 对照库区间声明 ⇄ 实际条目（2026-09-16 第十五批新增闸门）：`workflows/` 与
    # `corpus/contrast/` 的聚合文档会声明"某区间为真实双侧对照""本文件覆盖 pair-051..0NN"。
    # 这类声明随对照库增长会**静默过期**：工作流曾长期写"pair-051..056 为真实双侧对照""源自
    # pair-051..065，跨三会场"，而库里已到 pair-068（跨四会场）——任何既有闸门都不查这个。
    # 判据（只取可靠模式，避免把举例性的子区间误判为声明）：
    #   1) "真实双侧对照"的判定不看文档自述，只看 pair 条目标题前缀「真实双侧对照」；
    #   2) `workflows/*.md` 中带声明标记（其后 25 字含"真实双侧对照/流程与保真示范/源自/跨"，
    #      或其前 10 字含"源自"）的 `pair-A..B` 区间：A 落在真实区间内时 B 必须等于真实末条；
    #      区间完全早于真实起点时 B 必须等于真实起点-1（项目自有改写批的右界）；
    #   3) 聚合文档 `corpus/contrast/raw_edited_official_pairs_*.md` 必须逐一提到每个真实双侧条目。
    pair_dir = ROOT / "corpus" / "raw_edited_pairs"
    real_pairs: set[int] = set()
    for item in sorted(pair_dir.glob("pair-*.yaml")):
        title = re.search(r"^title:\s*(.+)$", item.read_text(encoding="utf-8"), re.MULTILINE)
        if title and title.group(1).strip().startswith("真实双侧对照"):
            real_pairs.add(int(re.search(r"pair-(\d{3})", item.name).group(1)))
    range_decls = 0
    real_min = real_max = 0
    if not real_pairs:
        errors.append("corpus/raw_edited_pairs/: 未找到任何标题为「真实双侧对照」的条目（基准缺失）")
    else:
        real_min, real_max = min(real_pairs), max(real_pairs)
        for path in sorted((ROOT / "workflows").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for m in re.finditer(r"pair-(\d{3})\.\.(\d{3})", text):
                after = text[m.end():m.end() + 25]
                before = text[max(0, m.start() - 10):m.start()]
                if not (re.search(r"真实双侧对照|流程与保真示范|源自|跨", after) or "源自" in before):
                    continue
                range_decls += 1
                a, b = int(m.group(1)), int(m.group(2))
                if a >= real_min and b != real_max:
                    errors.append(
                        f"{path.relative_to(ROOT)}: 区间 pair-{a:03d}..{b:03d} 陈旧——真实双侧对照"
                        f"实际末条为 pair-{real_max:03d}"
                    )
                if a < real_min and b != real_min - 1:
                    errors.append(
                        f"{path.relative_to(ROOT)}: 区间 pair-{a:03d}..{b:03d} 陈旧——项目自有改写批"
                        f"右界应为 pair-{real_min - 1:03d}"
                    )
    item_cover = 0
    for path in sorted((ROOT / "corpus" / "contrast").glob("raw_edited_official_pairs_*.md")):
        text = path.read_text(encoding="utf-8")
        nums: set[int] = set()
        for m in re.finditer(r"pair-(\d{3})\.\.(\d{3})", text):
            nums.update(range(int(m.group(1)), int(m.group(2)) + 1))
        for m in re.finditer(r"pair-(\d{3})((?:\s*/\s*\d{3})+)?", text):
            nums.add(int(m.group(1)))
            if m.group(2):
                nums.update(int(x) for x in re.findall(r"\d{3}", m.group(2)))
        missing = sorted(real_pairs - nums)
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)}: 聚合文档未覆盖真实双侧对照条目 "
                + "、".join(f"pair-{n:03d}" for n in missing)
            )
        else:
            item_cover += len(real_pairs)
    print(f"对照库区间声明：{range_decls} 处受检（真实双侧对照实际区间 pair-{real_min:03d}..{real_max:03d}），聚合文档覆盖 {item_cover} 条真实条目")
    # 盲评配对 ⇄ 揭盲钥（2026-09-16 第十六批新增闸门）：`pending_pairs/` 下的每份配对都必须
    # 有一把揭盲钥，否则"能评不能揭盲"；且**揭盲函数必须与钥一致**——此前 process_blind_review
    # 用"偶数 A=Skill、奇数 B=Skill"的公式，而 pair_012/014/016/018/020 的实际 A 侧是 Baseline，
    # 按公式处理会把 Baseline 的答卷记成 Skill；另有 6 对（133..138）长期无钥。
    # 配对文件若自称"请勿查看 keys（X）"，X 必须就是实际登记该钥的文件。
    pairs_dir = ROOT / "evals" / "human_review" / "pending_pairs"
    pair_files = sorted(p for p in pairs_dir.glob("pair_*.md") if not p.name.endswith("_key.md"))
    keyed = 0
    try:
        keys = load_keys(pairs_dir)
        key_sources = load_key_sources(pairs_dir)
    except ValueError as exc:
        keys, key_sources = {}, {}
        errors.append(f"evals/human_review/pending_pairs/: 揭盲钥解析失败 —— {exc}")
    pair_nos = {int(re.search(r"pair_(\d+)", p.name).group(1)): p for p in pair_files}
    for no, path in sorted(pair_nos.items()):
        if no not in keys:
            errors.append(f"{path.relative_to(ROOT)}: 无揭盲钥（keys_*.md 未登记该对，评审后无法揭盲）")
            continue
        keyed += 1
        declared = declared_key_file(path.read_text(encoding="utf-8"))
        if declared and declared != key_sources.get(no):
            errors.append(
                f"{path.relative_to(ROOT)}: 自称揭盲钥在 {declared}，实际登记在 {key_sources.get(no)}"
            )
    for no in sorted(set(keys) - set(pair_nos)):
        errors.append(f"evals/human_review/pending_pairs/: 揭盲钥 pair_{no:03d} 没有对应配对文件")
    mismatch = 0
    if process_blind_review is not None:
        for no in sorted(keys):
            try:
                if process_blind_review.skill_side(f"pair_{no:03d}") != keys[no]:
                    mismatch += 1
                    errors.append(
                        f"scripts/process_blind_review.py: skill_side(pair_{no:03d}) 与揭盲钥不一致"
                        f"（keys 记 Skill={keys[no]}）"
                    )
            except KeyError:
                mismatch += 1
                errors.append(f"scripts/process_blind_review.py: skill_side(pair_{no:03d}) 取不到揭盲钥")
    print(f"盲评配对：{keyed}/{len(pair_nos)} 对已登记揭盲钥，揭盲函数与 keys 不一致 {mismatch} 处")
    # 反模式索引 ⇄ 实际文件（2026-09-16 第十七批新增闸门）：`knowledge/anti_patterns/README.md`
    # 的「已有完整条目」表曾被当作"库的目录"，实际**少了 `feature_headline_opening.md`**
    # （文件存在、索引未列）——索引缺项不影响任何机制检查，但读目录的人找不到该反模式。
    # 判据：①索引表里列出的 `*.md` 必须存在；②目录里每个反模式文件必须出现在索引里（双向）。
    anti_index = ROOT / "knowledge" / "anti_patterns" / "README.md"
    index_text = anti_index.read_text(encoding="utf-8")
    listed = set(re.findall(r"`([a-z_]+\.md)`", index_text))
    actual = {p.name for p in (ROOT / "knowledge" / "anti_patterns").glob("*.md") if p.name != "README.md"}
    for name in sorted(listed - actual):
        errors.append(f"knowledge/anti_patterns/README.md: 索引列出不存在的 {name}")
    for name in sorted(actual - listed):
        errors.append(f"knowledge/anti_patterns/README.md: 实际文件 {name} 未进索引（目录缺项）")
    index_ok = len(listed & actual)
    print(f"反模式索引：{index_ok}/{len(actual)} 个反模式文件已进索引，缺项 {len(actual - listed)} 处")
    # 机制节点 ⇄ 本目录 README 索引（2026-09-16 第十九批新增，与上一条同族）：
    # `knowledge/mechanisms/README.md` 的「已建节点」表是**读目录的人的唯一索引**；
    # 新加一个节点而不登记，任何检查都不会变红（反向由上一段"反引号引用可解析"覆盖）。
    mech_readme = (ROOT / "knowledge" / "mechanisms" / "README.md").read_text(encoding="utf-8")
    mech_listed = set(re.findall(r"`([a-z_]+\.md)`", mech_readme))
    for name in sorted(set(mechanism_files) - mech_listed):
        errors.append(
            f"knowledge/mechanisms/README.md: 实际节点 {name} 未进「已建节点」索引（目录缺项）"
        )
    print(f"机制节点索引：{len(set(mechanism_files) & mech_listed)}/{len(mechanism_files)} 个节点已进本目录 README，"
          f"缺项 {len(set(mechanism_files) - mech_listed)} 处")
    # 重复登记 ⇄ 同一页面（2026-09-16 第二十一批新增）：实测两例——①同一篇讲话被登记两次
    # （URL 仅差 `/web/` 前缀，2026-09-16 实测两 URL 返回**同一页面**）；②同一期节目的
    # **分页**（自标 2/4、3/4、4/4 页）被登记为**三条独立语料**。**两者都不会让任何既有检查变红**，
    # 却直接抬高"数量 Gate"读数（commentary 101→99、speeches 100→99，双双跌破 100）。
    # 判据：同类别内 **URL 主干**（去 scheme、去 `/web`、去 `_N` 分页后缀）与**规范化标题**
    # 同时相同 ⇒ 同一内容单元被登记两次。
    # 排除 `raw_edited_pairs`／`contrast`：这两类是**派生**条目（同一条源条目对应多个改写档、
    # 合成负例共用占位 URL），同 URL 同标题属正常——排除理由显式写出并计数，不静默跳过。
    DERIVED_CATEGORIES = {"raw_edited_pairs", "contrast"}

    def url_stem(u: object) -> str:
        s = str(u or "").strip().rstrip("?").rstrip("/")
        s = re.sub(r"^https?://", "", s).replace("/web/", "/")
        return re.sub(r"_\d+(?=\.s?html|$)", "", s)

    dup_key: dict[tuple[str, str, str], list[str]] = {}
    dup_exempt = 0
    for item in (ROOT / "corpus").rglob("*.yaml"):
        rel = item.relative_to(ROOT / "corpus")
        if item.name == "index.yaml" or rel.parts[0] == "candidates":
            continue
        if rel.parts[0] in DERIVED_CATEGORIES:
            dup_exempt += 1
            continue
        record = yaml.safe_load(item.read_text(encoding="utf-8")) or {}
        if not isinstance(record, dict):
            continue
        title = re.sub(r'[\s\u3000“”"\'《》()（）]', "", str(record.get("title", "")))
        key = (rel.parts[0], url_stem(record.get("source_url")), title)
        if all(key):
            dup_key.setdefault(key, []).append(str(rel))
    dup_groups = 0
    for (category, stem, title), names in sorted(dup_key.items()):
        if len(names) > 1:
            dup_groups += 1
            errors.append(
                f"corpus/{category}/: 同一页面被登记 {len(names)} 次（URL 主干 `{stem}`、标题「{title[:24]}」）："
                + "、".join(names) + "（重复登记会抬高数量 Gate 读数）"
            )
    print(f"重复登记：{len(dup_key)} 个(类别,URL 主干,标题)组合受检，重复组 {dup_groups} 个"
          f"（派生类别豁免 {dup_exempt} 条：{sorted(DERIVED_CATEGORIES)} 系由其他条目派生，同 URL 同标题属正常）")
    # `knowledge/**/README.md` 的反引号文件引用必须可解析（2026-09-16 第十八批补充）：
    # `check_links.py` 只查 Markdown 链接，**反引号形式的名字它管不到**——`knowledge/rhetoric/README.md`
    # 因此长期写着目录内并不存在的 `metaphor_analogy.md`（实体在 `../mechanisms/` 下）。
    # 只取"看起来就是文件路径"的反引号内容；同一行含"计划/待建/未来/拟/将"的按规划项跳过。
    readme_refs = 0
    readme_missing = 0
    for readme in sorted((ROOT / "knowledge").rglob("README.md")):
        for line in readme.read_text(encoding="utf-8").splitlines():
            if re.search(r"计划|待建|未来|拟|将", line):
                continue
            for ref in re.findall(r"`([A-Za-z0-9_./\-]+\.(?:md|yaml|json))`", line):
                if ref.startswith(("http", "corpus/", "scripts/", "evals/")):
                    continue
                readme_refs += 1
                if not any((candidate).exists() for candidate in
                           (readme.parent / ref, ROOT / ref)):
                    readme_missing += 1
                    errors.append(
                        f"{readme.relative_to(ROOT)}: 反引号引用 `{ref}` 解析不到文件"
                        "（Markdown 链接检查不管这类引用）"
                    )
    print(f"knowledge README 引用：{readme_refs} 处反引号文件引用，解析不到 {readme_missing} 处")
    # 参数命名空间（2026-09-16 第十八批新增闸门）：`platforms/*/README.md` 的「参数偏移」块
    # 会把**十维语言参数**、**机制节点名**、**呈现层参数**三类名字混在一起写。实测
    # `concreteness`／`block_length`／`entry_speed` 被当作参数使用，却不在十维空间、也不在
    # `schemas/style_profile.yaml` 里——读者无法判断它是什么、基线在哪。
    # 判据：①STYLE_SYSTEM 十维表与 `schemas/style_profile.yaml` 的参数键**逐字一致**；
    # ②`platforms/*/README.md` 里形如 `key:` 的每一项，必须落在
    #   十维键 ∪ 机制节点名 ∪ STYLE_SYSTEM「呈现层参数登记表」之内。
    style_text = (ROOT / "STYLE_SYSTEM.md").read_text(encoding="utf-8")
    dims = set()
    for line in style_text.splitlines():
        m = re.match(r"\|\s*([A-Za-z][A-Za-z]*(?: [A-Za-z]+)*)\s+\S*\s*\|", line)
        if not m:
            continue
        english = m.group(1)
        if len(english.split()) <= 3:
            dims.add("_".join(w.lower() for w in english.split()))
    schema_text = (ROOT / "schemas" / "style_profile.yaml").read_text(encoding="utf-8")
    schema_params = set(re.findall(r"^\s{2}([a-z_]+):", schema_text, re.MULTILINE))
    dims &= schema_params
    registry = set(re.findall(r"^\|\s*`([a-z_]+)`\s*\|", style_text, re.MULTILINE))
    mechanisms = {p.stem for p in (ROOT / "knowledge" / "mechanisms").glob("*.md")
                  if p.name not in {"README.md", "GRAPH.md"}}
    allowed = dims | registry | mechanisms
    platform_keys = 0
    unclassified = 0
    for path in sorted((ROOT / "platforms").glob("*/README.md")):
        for key in re.findall(r"^([a-z_]+):", path.read_text(encoding="utf-8"), re.MULTILINE):
            platform_keys += 1
            if key not in allowed:
                unclassified += 1
                errors.append(
                    f"{path.relative_to(ROOT)}: 参数 `{key}` 不在命名空间内——须是十维键"
                    "／机制节点名／STYLE_SYSTEM「呈现层参数登记表」登记项"
                )
    if dims != schema_params:
        errors.append(
            "STYLE_SYSTEM.md 十维表与 schemas/style_profile.yaml 参数键不一致："
            f"仅十维有 {sorted(dims - schema_params)}；仅 schema 有 {sorted(schema_params - dims)}"
        )
    consistent = "一致" if dims == schema_params else f"**不一致**（十维 {len(dims)}／schema {len(schema_params)}）"
    calib_keys = set(re.findall(r"^([a-z_]+):", (ROOT / "workflows" / "style_calibration.md")
                                .read_text(encoding="utf-8"), re.MULTILINE))
    missing_dims = sorted(dims - calib_keys)
    if missing_dims:
        errors.append(
            "workflows/style_calibration.md: 校准模板未列出十维参数 " + "、".join(missing_dims)
            + "（模板漏维会让校准结果缺项而不自知）"
        )
    print(f"参数命名空间：十维 {len(dims)} 键与 schema {consistent}，呈现层登记 {len(registry)} 项，"
          f"平台参数引用 {platform_keys} 处（不可归类 {unclassified} 处）")
    # schema ⇄ 记录字段覆盖（2026-09-16 第十八批新增闸门）：`validate_schemas.py` 只校验
    # "模板必备字段是否齐全"，于是**记录里的结构性字段可以完全不在模板里**——实测
    # `raw_edited_pair.yaml` 声明 15 键，而 68 条记录每条约 44 键（29 个字段 100% 出现却不在模板），
    # `benchmark_case.yaml` 同样漏 3 个（150/156 出现）。模板因此名不副实，而校验全绿。
    # 判据（配对关系是显式声明的，不自动推导，避免把生成物当成样本）：
    #   ①凡在 ≥90% 记录中出现的字段，必须出现在对应模板里（结构性字段）；
    #   ②模板里声明却从未出现的字段，报为"死字段"（多半是拼写漂移）。
    schema_pairs = [
        ("corpus_item", "corpus"),
        ("raw_edited_pair", "corpus/raw_edited_pairs"),
        ("benchmark_case", "evals/benchmark/cases"),
    ]
    schema_gap = 0
    schema_checked = 0
    for schema_name, category in schema_pairs:
        tpl = set(re.findall(r"^([a-z_]+):", (ROOT / "schemas" / f"{schema_name}.yaml")
                            .read_text(encoding="utf-8"), re.MULTILINE))
        counters: dict[str, int] = {}
        records = 0
        for item in sorted((ROOT / category).rglob("*.yaml")):
            if item.name == "index.yaml":
                continue
            data = yaml.safe_load(item.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            records += 1
            for key in data:
                counters[key] = counters.get(key, 0) + 1
        if not records:
            continue
        schema_checked += records
        structural = sorted(k for k, n in counters.items() if n >= 0.9 * records and k not in tpl)
        dead = sorted(k for k in tpl if counters.get(k, 0) == 0)
        for key in structural:
            schema_gap += 1
            errors.append(
                f"schemas/{schema_name}.yaml: 结构性字段 `{key}` 未进模板"
                f"（{counters[key]}/{records} 条记录都有它——模板名不副实）"
            )
        for key in dead:
            errors.append(f"schemas/{schema_name}.yaml: 模板字段 `{key}` 在 {category} 中从未出现（死字段）")
    print(f"schema 字段覆盖：{schema_checked} 条记录受检，结构性缺失 {schema_gap} 处")
    # 当前状态文档的数字 ⇄ 实际（2026-09-16 第十八批新增闸门）：`ARCHITECTURE.md` 曾写
    # "当前 registry 为 120 条（中文 86、国际 34）"（实为 137／103／34），`METHODOLOGY.md` 同处
    # 也是旧值——**都写着"当前"却不随库增长更新**，而此前没有任何检查比对文档数字与实际。
    # 只查**当前状态文档**（README/README_EN/SKILL/EVALS/METHODOLOGY/ARCHITECTURE/STYLE_SYSTEM/AGENTS）；
    # 版本台账（CHANGELOG）与分轮记录（HANDOFF/FINAL_REPORT/CORPUS 等）**合法引用历史值**，故排除。
    current_docs = ["README.md", "README_EN.md", "SKILL.md", "EVALS.md",
                    "METHODOLOGY.md", "ARCHITECTURE.md", "STYLE_SYSTEM.md", "AGENTS.md"]
    mechanism_nodes = sorted(p for p in (ROOT / "knowledge" / "mechanisms").glob("*.md")
                             if p.name not in {"README.md", "GRAPH.md"})
    graph = yaml.safe_load((ROOT / "knowledge" / "mechanisms" / "GRAPH.yaml").read_text(encoding="utf-8"))
    graph_edges = len(graph.get("edges", [])) if isinstance(graph, dict) else 0
    registry_count = len(yaml.safe_load((ROOT / "knowledge" / "sources" / "registry.yaml")
                                        .read_text(encoding="utf-8")) or [])
    inventory = len(list((ROOT / "evals" / "benchmark" / "cases").glob("*_case.yaml")))
    formal = 0
    for item in (ROOT / "corpus").rglob("*.yaml"):
        if item.name == "index.yaml" or item.relative_to(ROOT / "corpus").parts[0] == "candidates":
            continue
        text = item.read_text(encoding="utf-8")
        if re.search(r"^corpus_id:", text, re.MULTILINE):
            formal += 1
    expected = {
        "registry": (rf"(?:registry|来源登记)[^。\n]{{0,40}}?(\d{{2,4}})[^\d\n]{{0,4}}条", registry_count),
        "节点": (r"(\d{1,3})[^\d\n]{0,4}个?机制节点", len(mechanism_nodes)),
        "关系": (r"(\d{1,3})[^\d\n]{0,4}条关系", graph_edges),
        "inventory": (r"benchmark inventory[^。\n]{0,20}?(\d{2,4})[^\d\n]{0,4}案", inventory),
        "正式语料": (r"正式语料[^。\n]{0,20}?(\d{2,4})[^\d\n]{0,4}条", formal),
    }
    doc_claims = 0
    for name in current_docs:
        path = ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for label, (pattern, actual) in expected.items():
            for m in re.finditer(pattern, text):
                doc_claims += 1
                if int(m.group(1)) != actual:
                    line_no = text[:m.start()].count("\n") + 1
                    errors.append(
                        f"{name}:{line_no}: 文档断言 `{m.group(1)}`（{label}）与实际 {actual} 不符"
                        "（当前状态文档的数字必须随库更新）"
                    )
    print(f"当前状态文档数字：{len(current_docs)} 份受检、{doc_claims} 处数字断言，"
          f"实际值 registry {registry_count}／机制节点 {len(mechanism_nodes)}／图谱关系 {graph_edges}／"
          f"benchmark {inventory}／正式语料 {formal}")
    # 已发布宣传页的数字 ⇄ 权威记录（2026-09-16 第十九批新增）：`docs/index.html` 是 GitHub Pages
    # 对外页面，同样写着"当前"数字（"138 对盲评配对就绪""首批人工盲评 Skill 胜率 75%（15:5）"），
    # 但它**不是 .md**，上面那条"当前状态文档数字"闸门读不到它（两条**都**由上一批手工核对过，
    # 核对本身没错——缺的是**能复查**它的检查）。对外页面写着旧的数字比内部文档写旧更糟。
    # 判据：配对数照 `pending_pairs/` 实际文件数（排除 `*_key.md`）；胜率与 a:b 照
    # `evals/pairwise/summary_*.md` 最新一册的"更愿意继续读"行——**读记录，不用公式重算**。
    promo = ROOT / "docs" / "index.html"
    if promo.exists():
        promo_text = promo.read_text(encoding="utf-8")
        pair_docs = len({p.name for p in (ROOT / "evals" / "human_review" / "pending_pairs").glob("pair_*.md")
                         if not p.name.endswith("_key.md")})
        summaries = sorted((ROOT / "evals" / "pairwise").glob("summary_*.md"))
        skill_wins = base_wins = None
        if summaries:
            latest = summaries[-1].read_text(encoding="utf-8")
            row = re.search(r"更愿意继续读：Skill版\s*(\d+)\s*/\s*Baseline版\s*(\d+)", latest)
            if row:
                skill_wins, base_wins = int(row.group(1)), int(row.group(2))
        promo_claims = 0
        for m in re.finditer(r"(\d{2,3})\s*对盲评配对", promo_text):
            promo_claims += 1
            if int(m.group(1)) != pair_docs:
                errors.append(
                    f"docs/index.html: 对外页面写 `{m.group(1)} 对盲评配对就绪`，"
                    f"实际 `pending_pairs/` 有 {pair_docs} 份（对外数字必须与库一致）"
                )
        for m in re.finditer(r"Skill 胜率\s*(\d{1,3})%\s*（(\d+):(\d+)）", promo_text):
            promo_claims += 1
            if skill_wins is None:
                errors.append(
                    "docs/index.html: 写有胜率，但 `evals/pairwise/summary_*.md` 里读不到"
                    "「更愿意继续读」行——无从核实（不得凭公式重算）"
                )
                continue
            total = skill_wins + base_wins
            pct = round(100 * skill_wins / total) if total else 0
            if (int(m.group(1)), int(m.group(2)), int(m.group(3))) != (pct, skill_wins, base_wins):
                errors.append(
                    f"docs/index.html: 对外页面写 `胜率 {m.group(1)}%（{m.group(2)}:{m.group(3)}）`，"
                    f"而最新盲评汇总记 `{pct}%（{skill_wins}:{base_wins}）`"
                    f"（{summaries[-1].name if summaries else '无汇总册'}）"
                )
        # ㉖ 对外页面「理论库构成」百分比 ⇄ registry 实际语言分布（2026-09-17 第五十九批新增）：
        # `docs/index.html` 的 Pipeline A 列表原写"**70% 中文原生 + 30% 国际补强**"，
        # 而 registry 实为 中文 103／国际 34（= 75.2%／24.8%）——**该断言此前不在任何闸门内**
        # （第 ⑫ 条只覆盖"配对份数"与"胜率"两处）。判据：两数各 ＝ `round(100*zh/total)`／`round(100*en/total)`。
        reg_items = yaml.safe_load((ROOT / "knowledge" / "sources" / "registry.yaml")
                                   .read_text(encoding="utf-8")) or []
        reg_total = len(reg_items)
        reg_zh = sum(1 for x in reg_items if str(x.get("language")) == "zh")
        reg_en = sum(1 for x in reg_items if str(x.get("language")) == "en")
        for m in re.finditer(r"(\d{1,3})%\s*中文原生\s*\+\s*(\d{1,3})%\s*国际补强", promo_text):
            promo_claims += 1
            if reg_total:
                wz = round(100 * reg_zh / reg_total)
                we = round(100 * reg_en / reg_total)
                if (int(m.group(1)), int(m.group(2))) != (wz, we):
                    errors.append(
                        f"docs/index.html: 对外页面写 `{m.group(1)}% 中文原生 + {m.group(2)}% 国际补强`，"
                        f"而 registry 实为 中文 {reg_zh}／国际 {reg_en}（= {wz}%／{we}%）"
                        "（对外数字必须与库一致）"
                    )
        print(f"已发布宣传页数字：docs/index.html {promo_claims} 处断言，"
              f"实际配对 {pair_docs} 份／"
              + (f"胜率 {round(100 * skill_wins / (skill_wins + base_wins))}%（{skill_wins}:{base_wins}）"
                 if skill_wins is not None else "胜率记录不可读"))
    # "最新版本"类断言 ⇄ CHANGELOG 台账首条（2026-09-16 第十九批新增）：`HANDOFF.md` 曾写
    # "版本台账（**最新 v1.0.8**）"而 CHANGELOG 已到 v1.0.11——**同一条"当前值留在旧轮次"缺陷**，
    # 只因 HANDOFF 合法引用大量历史值而被"当前状态文档"闸门整体排除，于是无人复查。
    # 判据：全仓 .md 里凡写"最新 vX.Y.Z"，必须等于 `CHANGELOG.md` 的第一个 `## vX.Y.Z`。
    changelog_head = re.search(r"^## v(\d+\.\d+\.\d+)", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
                               re.MULTILINE)
    version_claims = 0
    if changelog_head:
        want = changelog_head.group(1)
        for path in sorted(ROOT.glob("*.md")):
            if path.name == "CHANGELOG.md":
                continue
            text = path.read_text(encoding="utf-8")
            for m in re.finditer(r"最新\s*v(\d+\.\d+\.\d+)", text):
                version_claims += 1
                if m.group(1) != want:
                    line_no = text[:m.start()].count("\n") + 1
                    errors.append(
                        f"{path.name}:{line_no}: 写 `最新 v{m.group(1)}`，"
                        f"而 CHANGELOG 台账首条是 v{want}（「最新」断言必须随台账更新）"
                    )
        print(f"最新版本断言：{version_claims} 处受检，CHANGELOG 台账首条 v{want}")
    # EXTERNAL_INPUT_TODO 文件头 ⇄ 当前轮次 + 配套证据清单（2026-09-17 第五十三批新增）：
    # 该清单是本项目**对外可审计的"剩余项"交付物**，其文件头写"末次更新：（第N批）· 对应版本：vX.Y.Z"
    # 与"配套证据：… `spotcheck-…o.md`"。第四十八批曾手工修过一次"头过期"，但**该断言本身
    # 从未被闸门覆盖**——批 49—52 过去后版本戳停在 v1.0.40、`配套证据` 的 spotcheck 上界停在 `…o.md`
    # （实际已有 `…s.md`），"当前值留在旧轮次"这一族在**第三处对象**再次重现。
    # 判据：①"对应版本"＝CHANGELOG 台账首条版本；②"（第N批）"＝台账首条批号；
    # ③`配套证据` 里引用的 spotcheck 文件号上界＝`corpus/annotations/` 实际最大号（证据清单不得落后）。
    todo_path = ROOT / "EXTERNAL_INPUT_TODO.md"
    if todo_path.exists() and changelog_head:
        todo_text = todo_path.read_text(encoding="utf-8")
        head_line = next((l for l in todo_text.splitlines() if l.startswith("生成日期")), "")
        cl_head_line = next((l for l in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
                             if l.startswith("## v")), "")
        cl_batch = re.search(r"第([0-9一二三四五六七八九十百]+)批", cl_head_line)
        head_batch = re.search(r"（第([0-9一二三四五六七八九十百]+)批）", head_line)
        head_ver = re.search(r"对应版本：v([0-9.]+)", head_line)
        if head_ver and head_ver.group(1) != changelog_head.group(1):
            errors.append(f"EXTERNAL_INPUT_TODO.md: 头写 `对应版本：v{head_ver.group(1)}`，"
                          f"而 CHANGELOG 台账首条是 v{changelog_head.group(1)}（头必须随台账更新）")
        if cl_batch and head_batch and head_batch.group(1) != cl_batch.group(1):
            errors.append(f"EXTERNAL_INPUT_TODO.md: 头写 `（第{head_batch.group(1)}批）`，"
                          f"而 CHANGELOG 台账首条是第{cl_batch.group(1)}批（头必须随台账更新）")
        actual_sc = sorted(p.name for p in (ROOT / "corpus" / "annotations").glob("spotcheck-*.md"))
        ref_sc = sorted(set(re.findall(r"spotcheck-[0-9]{8}[a-z]?\.md", todo_text)))
        if actual_sc and ref_sc and ref_sc[-1] != actual_sc[-1]:
            errors.append(f"EXTERNAL_INPUT_TODO.md: `配套证据` 引用的最新 spotcheck 是 `{ref_sc[-1]}`，"
                          f"而实际已有 `{actual_sc[-1]}`（证据清单不得落后于实际留痕）")
        # ④`配套证据` 里"COMPLETION_MATRIX「当前最短路径」第 a—b 条"的 b ＝ 该节实际最大条目号；
        # ⑤"HANDOFF §7（含第…—N批）"的 N ＝ CHANGELOG 台账首条批号（批号用汉字，直接比 token）。
        cm_path = ROOT / "COMPLETION_MATRIX.md"
        if cm_path.exists():
            cm_text = cm_path.read_text(encoding="utf-8")
            sec = cm_text.split("## 当前最短路径", 1)[1] if "## 当前最短路径" in cm_text else ""
            items = [int(m.group(1)) for m in re.finditer(r"^(\d+)\. ", sec, re.MULTILINE)]
            rng = re.search(r"第\s*(\d+)—(\d+)\s*条", todo_text)
            if items and rng and int(rng.group(2)) != max(items):
                errors.append(f"EXTERNAL_INPUT_TODO.md: `配套证据` 写「当前最短路径」第…—{rng.group(2)} 条，"
                              f"而该节实际最大条目号是 {max(items)}（证据清单不得落后）")
        hb = re.search(r"（含第[^—）]*—([0-9一二三四五六七八九十百]+)批）", todo_text)
        if cl_batch and hb and hb.group(1) != cl_batch.group(1):
            errors.append(f"EXTERNAL_INPUT_TODO.md: `配套证据` 写 HANDOFF §7「含第…—{hb.group(1)}批」，"
                          f"而 CHANGELOG 台账首条是第{cl_batch.group(1)}批（证据清单不得落后）")
        print(f"交付物清单文件头：对应版本 v{head_ver.group(1) if head_ver else '?'}／"
              f"第{head_batch.group(1) if head_batch else '?'}批，配套 spotcheck 上界 "
              f"{ref_sc[-1] if ref_sc else '?'}（实际 {actual_sc[-1] if actual_sc else '?'}）")
    # 「最新…为准/见」指针 ⇄ 实际最新（2026-09-17 第五十四批新增）：`FINAL_REPORT.md` 等文档里有
    # "最新可审计清单以 `COMPLETION_MATRIX.md`「当前最短路径」第 N 条与 `HANDOFF.md` 第X批条目为准"
    # 这类**指向当前最新**的指针——它们**不是历史值引用**（与"分轮记录"不同），却**从未被任何闸门覆盖**：
    # 实测 3 处全部停在旧轮次（第 41 条／第 7 条／第八轮条目）。判据：指针里的 N ＝
    # `COMPLETION_MATRIX.md`「当前最短路径」实际最大条目号；X ＝ CHANGELOG 台账首条批号。
    # 边界：只认"第N批条目"（"第N轮条目"式**不映射台账批号**，已改写措辞、不设假闸门）。
    latest_pointer = 0
    cm_path2 = ROOT / "COMPLETION_MATRIX.md"
    cm_max = 0
    if cm_path2.exists():
        cm_text2 = cm_path2.read_text(encoding="utf-8")
        sec2 = cm_text2.split("## 当前最短路径", 1)[1] if "## 当前最短路径" in cm_text2 else ""
        nums2 = [int(m.group(1)) for m in re.finditer(r"^(\d+)\. ", sec2, re.MULTILINE)]
        cm_max = max(nums2) if nums2 else 0
    cl_batch2 = re.search(r"第([0-9一二三四五六七八九十百]+)批",
                          next((l for l in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
                                if l.startswith("## v")), ""))
    for path in sorted(ROOT.glob("*.md")):
        flat = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
        for m in re.finditer(r"最新[^。]{0,120}?「当前最短路径」第 ?(\d+) ?条", flat):
            latest_pointer += 1
            if cm_max and int(m.group(1)) != cm_max:
                errors.append(f"{path.name}: 「最新…当前最短路径」指针写第 {m.group(1)} 条，"
                              f"而该节实际最大条目号是 {cm_max}（指针须指向当前最新）")
        for m in re.finditer(r"最新[^。]{0,120}?HANDOFF\.md`?\s*第\s*([0-9一二三四五六七八九十百]+)\s*批条目", flat):
            latest_pointer += 1
            if cl_batch2 and m.group(1) != cl_batch2.group(1):
                errors.append(f"{path.name}: 「最新…HANDOFF」指针写第{m.group(1)}批条目，"
                              f"而 CHANGELOG 台账首条是第{cl_batch2.group(1)}批（指针须指向当前最新）")
    print(f"「最新…为准」指针：{latest_pointer} 处受检（当前最短路径最大条目 {cm_max}／"
          f"台账首条批号 第{cl_batch2.group(1) if cl_batch2 else '?'}批）")
    # 当前进度数字 ⇄ 实际（2026-09-16 第二十批新增）：`HANDOFF.md` §2（该节自称"当前值"）与
    # `EXTERNAL_INPUT_TODO.md` 的"现状／已有 N 案"会随每次扩容变旧——**本轮实测两处又旧了**
    # （benchmark 156、正例层 6→7、ready 16），是同一缺陷族在**第三处对象**上重现。
    # 判据：①HANDOFF 只扫 §2 区间（其余各轮记录**合法引用历史值**）；②TODO 只按"现状"行与
    # 能力表"官方文件正例层"行取数。**不读生成物**（`check_source_trace.py` 在回归里跑在
    # `build_human_review_queue.py`／`build_corpus_index.py` **之前**，读生成物会拿上一轮的数比对）。
    case_dir = ROOT / "evals" / "benchmark" / "cases"
    ready = await_text = official_public = 0
    for case_path in sorted(case_dir.glob("*_case.yaml")):
        case = yaml.safe_load(case_path.read_text(encoding="utf-8")) or {}
        if case.get("source_type") == "official_public_document":
            official_public += 1
        case_file = case.get("input_file")
        if case_file:
            fp = ROOT / str(case_file)
            ok = fp.exists() and bool(fp.read_text(encoding="utf-8").strip())
        else:
            ok = case.get("source_type") == "project_authored_control"
        ready += 1 if ok else 0
        await_text += 0 if ok else 1
    progress_checks: list[tuple[str, str, int, str, str]] = []
    handoff_text = (ROOT / "HANDOFF.md").read_text(encoding="utf-8")
    sec2 = re.search(r"^## 2\..*?(?=^## 3\.)", handoff_text, re.MULTILINE | re.DOTALL)
    if sec2:
        progress_checks += [
            ("HANDOFF.md §2", r"Benchmark inventory \*\*(\d+)\*\* 案", inventory, "benchmark inventory",
             sec2.group(0)),
            ("HANDOFF.md §2", r"官方文件正例层 (\d+)", official_public, "官方文件正例层案数", sec2.group(0)),
        ]
    todo_text = (ROOT / "EXTERNAL_INPUT_TODO.md").read_text(encoding="utf-8")
    progress_checks += [
        ("EXTERNAL_INPUT_TODO.md", r"已建 \*\*(\d+) 案\*\*", official_public, "官方文件正例层案数", todo_text),
        ("EXTERNAL_INPUT_TODO.md", r"\| 官方文件正例层扩容 \| 已有 (\d+) 案", official_public,
         "官方文件正例层案数（能力表）", todo_text),
    ]
    progress_claims = 0
    for name, pattern, actual, label, haystack in progress_checks:
        for m in re.finditer(pattern, haystack):
            progress_claims += 1
            if int(m.group(1)) != actual:
                line_no = haystack[:m.start()].count("\n") + 1
                errors.append(f"{name}:{line_no}: 写 `{m.group(1)}`（{label}）与实际 {actual} 不符"
                              "（进度类数字每次扩容都会变旧，必须随之更新）")
    for m in re.finditer(r"`ready (\d+) / await_source_text (\d+)`", todo_text):
        progress_claims += 2
        if int(m.group(1)) != ready:
            errors.append(f"EXTERNAL_INPUT_TODO.md: 「现状」写 ready {m.group(1)}，实际 {ready}")
        if int(m.group(2)) != await_text:
            errors.append(f"EXTERNAL_INPUT_TODO.md: 「现状」写 await_source_text {m.group(2)}，实际 {await_text}")
    # 配对数量断言（2026-09-17 第四十八批新增）：`EXTERNAL_INPUT_TODO.md` A4「现状」写有
    # "匿名配对就绪 N 份，揭盲钥 N/N 全覆盖"——该数字此前**未被任何闸门覆盖**（本批实测已旧：
    # 写 145、实际 146），与 `docs/index.html` 属**同一缺陷族**（"当前值留在旧轮次"）。
    # 判据：配对数照 `pending_pairs/` 实际文件数（排除 `*_key.md`）、钥数照本脚本上文 `keyed`。
    pair_docs_actual = len({p.name for p in (ROOT / "evals" / "human_review" / "pending_pairs").glob("pair_*.md")
                            if not p.name.endswith("_key.md")})
    for m in re.finditer(r"匿名配对就绪\s*\*\*(\d+)\*\*\s*份，\s*揭盲钥\s*\*\*(\d+)/(\d+)\*\*\s*全覆盖", todo_text):
        progress_claims += 3
        if int(m.group(1)) != pair_docs_actual:
            errors.append(f"EXTERNAL_INPUT_TODO.md: 写 `匿名配对就绪 {m.group(1)} 份`，"
                          f"实际 {pair_docs_actual} 份（当前值必须随库更新）")
        if int(m.group(2)) != keyed or int(m.group(3)) != len(pair_nos):
            errors.append(f"EXTERNAL_INPUT_TODO.md: 写 `揭盲钥 {m.group(2)}/{m.group(3)}`，"
                          f"实际 {keyed}/{len(pair_nos)}")
    if sec2:
        for m in re.finditer(r"人工复核队列 \*\*(\d+)\*\* 案：`ready` \*\*(\d+)\*\*，"
                             r"`await_source_text` \*\*(\d+)\*\*", sec2.group(0)):
            progress_claims += 3
            for got, actual, label in ((int(m.group(1)), inventory, "复核队列总案数"),
                                       (int(m.group(2)), ready, "ready"),
                                       (int(m.group(3)), await_text, "await_source_text")):
                if got != actual:
                    errors.append(f"HANDOFF.md §2: 复核队列写 {label} {got}，实际 {actual}")
    # HANDOFF §2 的其余"当前值" ⇄ 实际（2026-09-17 第四十八批新增）：§2 自称"当前值"，
    # 但此前只有 inventory／正例层／ready／await 四项被闸门覆盖，**其余十几项全靠人工核对**
    # （本项目历史上"当前值留在旧轮次"已在 HANDOFF §2、`docs/index.html`、`EXTERNAL_INPUT_TODO`
    # 三处对象重现）。本批把 §2 的**可机读当前值**全部纳入：正式语料／候选／index／Schema 总记录／
    # registry 总数与中英拆分与 access_status 分布／图谱节点与关系／validated 数／八类深读分布／
    # 配对与揭盲钥／质量实跑报告数。**参考值一律现场复算、不读生成物**（本脚本跑在生成器之前）。
    if sec2:
        s2 = sec2.group(0)
        reg_doc = yaml.safe_load((ROOT / "knowledge" / "sources" / "registry.yaml").read_text(encoding="utf-8"))
        reg_list = reg_doc["sources"] if isinstance(reg_doc, dict) and "sources" in reg_doc else reg_doc
        lang_c = collections.Counter(s.get("language") for s in reg_list)
        acc_c = collections.Counter(s.get("access_status") for s in reg_list)
        cat_state: dict[str, collections.Counter] = {}
        for cat in ("blogs", "commentary", "speeches", "hosting", "interviews",
                    "podcasts", "contrast", "raw_edited_pairs"):
            c = collections.Counter()
            for fp in (ROOT / "corpus" / cat).glob("*.yaml"):
                dd = yaml.safe_load(fp.read_text(encoding="utf-8"))
                if isinstance(dd, dict):
                    c[dd.get("state")] += 1
            cat_state[cat] = c
        cand_n = len(list((ROOT / "corpus" / "candidates").glob("*.yaml")))
        validated_n = 0
        for p in mechanism_nodes:
            mt = p.read_text(encoding="utf-8")
            if re.search(r"^confidence:\s*\"?validated\"?\s*$", mt, re.MULTILINE):
                validated_n += 1
        quality_n = len(list((ROOT / "evals" / "benchmark" / "results" / "runs").glob("*")))
        s2_checks: list[tuple[str, object, object, str]] = [
            (r"正式语料 \*\*(\d+)\*\* 条", formal, formal, "正式语料"),
            (r"候选 (\d+) 条；corpus index \*\*([\d,]+)\*\* 条",
             None, (cand_n, formal + cand_n), "候选／index"),
            (r"Schema 总校验记录 \*\*([\d,]+)\*\* 条", None, (formal + registry_count,), "Schema 总记录"),
            (r"Source Registry \*\*(\d+)\*\* 条：中文 (\d+)、英文 (\d+)",
             None, (registry_count, lang_c["zh"], lang_c["en"]), "registry／中英"),
            (r"`full_text (\d+) / key_chapters (\d+) / review_only (\d+) / metadata_only (\d+)",
             None, (acc_c["full_text"], acc_c["key_chapters"], acc_c["review_only"], acc_c["metadata_only"]),
             "registry access_status 分布"),
            (r"机制图谱 (\d+) 个节点、\*\*(\d+) 条关系\*\*",
             None, (len(mechanism_nodes), graph_edges), "图谱节点／关系"),
            (r"`confidence: validated` \*\*(\d+)\*\*", validated_n, validated_n, "validated 节点数"),
            (r"质量实跑报告 (\d+) 份", quality_n, quality_n, "质量实跑报告数"),
            (r"匿名配对就绪 \*\*(\d+)\*\* 份、揭盲钥 \*\*(\d+)/(\d+)\*\*",
             None, (pair_docs_actual, keyed, len(pair_nos)), "配对／揭盲钥"),
        ]
        for pat, single, actual, label in s2_checks:
            for m in re.finditer(pat, s2):
                if single is not None:
                    progress_claims += 1
                    if int(m.group(1).replace(",", "")) != single:
                        errors.append(f"HANDOFF.md §2: 写 `{m.group(1)}`（{label}）与实际 {single} 不符"
                                      "（§2 自称当前值，必须随库更新）")
                else:
                    got = tuple(int(g.replace(",", "")) for g in m.groups())
                    progress_claims += len(got)
                    if got != tuple(actual):
                        errors.append(f"HANDOFF.md §2: 写 `{got}`（{label}）与实际 `{tuple(actual)}` 不符"
                                      "（§2 自称当前值，必须随库更新）")
        # 八类深读分布（逐类独立匹配，避免跨类串位）
        dist_checks = [
            ("blogs", r"blogs\s*`VALIDATED (\d+) / ANNOTATED (\d+)`", ("VALIDATED", "ANNOTATED")),
            ("commentary", r"commentary\s*`ANNOTATED (\d+) / READ (\d+)`", ("ANNOTATED", "READ")),
            ("speeches", r"speeches\s*`ANNOTATED (\d+) / READ (\d+)`", ("ANNOTATED", "READ")),
            ("hosting", r"hosting\s*`ANNOTATED (\d+) / READ (\d+)`", ("ANNOTATED", "READ")),
            ("interviews", r"interviews\s*`ANNOTATED (\d+) / READ (\d+)`", ("ANNOTATED", "READ")),
            ("podcasts", r"podcasts\s*`ANNOTATED (\d+) / READ (\d+)`", ("ANNOTATED", "READ")),
            ("contrast", r"contrast\s*`ANNOTATED (\d+)`", ("ANNOTATED",)),
            ("raw_edited_pairs", r"raw_edited_pairs\s*`ANNOTATED (\d+)`", ("ANNOTATED",)),
        ]
        for cat, pat, keys in dist_checks:
            for m in re.finditer(pat, s2):
                got = tuple(int(g) for g in m.groups())
                actual = tuple(cat_state[cat][k] for k in keys)
                progress_claims += len(got)
                if got != actual:
                    errors.append(f"HANDOFF.md §2: 深读分布写 `{cat} {got}`，实际 `{actual}`"
                                  "（§2 自称当前值，必须随库更新）")
    # 另两份"当前状态"文档的数字（2026-09-17 第四十九批新增）：`EVALS.md` §2 与
    # `evals/benchmark/README.md` 都写着"当前已建立／已有 **N**"这类**当前值**，但它们
    # **既不在 8 份 current_docs 的模式覆盖内**（那 5 个模式只认 registry／机制节点／图谱关系／
    # `benchmark inventory`／正式语料），**也不在 §2 区间**——实测两处都已过期
    # （EVALS.md 写 154／4／ready 14，benchmark/README.md 写 150；实际 158／8／18／158）。
    src_type_c = collections.Counter()
    for case_path in sorted(case_dir.glob("*_case.yaml")):
        case = yaml.safe_load(case_path.read_text(encoding="utf-8")) or {}
        src_type_c[case.get("source_type")] += 1
    # registry 的语言拆分（本处独立复算，不依赖上文 `if sec2:` 分支内的局部量）
    _reg_doc = yaml.safe_load((ROOT / "knowledge" / "sources" / "registry.yaml").read_text(encoding="utf-8"))
    _reg_list = _reg_doc["sources"] if isinstance(_reg_doc, dict) and "sources" in _reg_doc else _reg_doc
    _lang_c = collections.Counter(s.get("language") for s in _reg_list)
    doc_num_checks: list[tuple[str, str, object, str]] = [
        ("EVALS.md", r"已有 \*\*(\d+)\*\* 个唯一 case_id", inventory, "唯一 case_id 数"),
        ("EVALS.md", r"(\d+) 个引用已读取的语料条目（`corpus_reference`）",
         src_type_c["corpus_reference"], "corpus_reference 案数"),
        ("EVALS.md", r"\*\*(\d+) 个为官方文件正例层\*\*", official_public, "官方文件正例层案数"),
        ("EVALS.md", r"`ready` \*\*(\d+)\*\*（10 自有高模板", ready, "ready 案数"),
        ("evals/benchmark/README.md", r"已建立 \*\*(\d+) 个可追溯 benchmark inventory case\*\*",
         inventory, "inventory 案数"),
        ("evals/benchmark/README.md", r"其中 (\d+) 个引用已 READ 的真实语料条目",
         src_type_c["corpus_reference"], "corpus_reference 案数"),
        ("evals/benchmark/README.md", r"\*\*(\d+) 个为官方文件正例层\*\*",
         official_public, "官方文件正例层案数"),
        # 2026-09-17 第五十批追加：`evals/human_review/README.md` 的「当前队列」曾写"包含 150 个 case"
        # （实际 158，且**完全漏列 8 个官方文件正例层案**）——同属"闸门模式覆盖不到"的当前值。
        ("evals/human_review/README.md", r"包含 \*\*(\d+)\*\* 个 case", inventory, "case 总数"),
        ("evals/human_review/README.md", r"`ready` \*\*(\d+)\*\* / `await_source_text` \*\*(\d+)\*\*",
         (ready, await_text), "ready／await"),
        # `CORPUS.md` 的纪律正文里也写着"当前为 137 条（中文 103、国际 34）"。
        ("CORPUS.md", r"理论来源登记\*\*当前为 (\d+) 条（中文 (\d+)、国际 (\d+)）",
         (registry_count, _lang_c["zh"], _lang_c["en"]), "registry／中英"),
    ]
    for doc_name, pat, actual, label in doc_num_checks:
        dp = ROOT / doc_name
        if not dp.exists():
            continue
        dtext = dp.read_text(encoding="utf-8")
        for m in re.finditer(pat, dtext):
            got = tuple(int(g.replace(",", "")) for g in m.groups())
            progress_claims += len(got)
            want = (actual,) if isinstance(actual, int) else tuple(actual)
            if got != want:
                line_no = dtext[:m.start()].count("\n") + 1
                errors.append(f"{doc_name}:{line_no}: 写 `{got}`（{label}）与实际 `{want}` 不符"
                              "（当前状态文档的数字必须随库更新）")
    print(f"进度类数字：HANDOFF §2 与 EXTERNAL_INPUT_TODO {progress_claims} 处断言受检，"
          f"实际 inventory {inventory}／正例层 {official_public}／ready {ready}／await {await_text}")
    # benchmark case 的 source_state／source_access_level ⇄ 被引语料条目（2026-09-17 第五十二批新增）：
    # `*_case.yaml` 会声明所引语料的 `source_state` 与 `source_access_level`，但**语料条目后来升级
    # （READ → ANNOTATED、substantial → full）时 case 侧从不自动跟随**——实测 **9 例漂移**
    # （8 例 `source_state` 停在 `READ`、1 例 `source_access_level` 停在 `substantial`），
    # 而**任何既有闸门都不比对这两个字段**（`run_evals.py` 只验来源链与期望属性）。
    case_state_bad = 0
    case_state_checked = 0
    case_ref_bad = 0
    case_url_checked = 0
    case_locator_checked = 0
    for case_path in sorted(case_dir.glob("*_case.yaml")):
        case = yaml.safe_load(case_path.read_text(encoding="utf-8")) or {}
        if case.get("source_type") != "corpus_reference":
            continue
        sref = case.get("source_ref")
        if not sref:
            continue
        ep = ROOT / str(sref)
        if not ep.exists():
            errors.append(f"{case_path.relative_to(ROOT)}: `source_ref` 指向不存在的 {sref}")
            case_state_bad += 1
            continue
        entry = yaml.safe_load(ep.read_text(encoding="utf-8"))
        if not isinstance(entry, dict):
            continue
        case_state_checked += 1
        for field, entry_key in (("source_state", "state"), ("source_access_level", "access_level")):
            want = entry.get(entry_key)
            got = case.get(field)
            if want and got and got != want:
                errors.append(f"{case_path.relative_to(ROOT)}: `{field}` 写 `{got}`，"
                              f"而 {sref} 为 `{want}`（语料升级后 case 侧必须跟随）")
                case_state_bad += 1
        # ㉓ benchmark case 的"引用面"⇄ 被引语料条目（2026-09-17 第五十三批新增）：
        # 同族缺陷的第二、三条不变量——`source_url` 与 `input_locator`。
        # `input_locator` 声明"用条目的哪一段"，理应**精确命中**被引条目的 `selected_segments`
        # （实测 140/140 命中）；若语料条目改写段落文字而 case 侧不跟随，本闸门会报出。
        # 边界：被引条目无 `selected_segments` 时不适用（如实计数、不制造假失败）。
        ent_url = str(entry.get("source_url") or "").strip()
        case_url = str(case.get("source_url") or "").strip()
        if case_url and ent_url:
            case_url_checked += 1
            if case_url != ent_url:
                errors.append(f"{case_path.relative_to(ROOT)}: `source_url` 与被引条目 {sref} 不一致"
                              f"（case `{case_url}` vs 条目 `{ent_url}`）")
                case_ref_bad += 1
        locator = str(case.get("input_locator") or "").strip()
        segs = entry.get("selected_segments")
        if locator and isinstance(segs, list) and segs:
            case_locator_checked += 1
            if locator not in [str(s).strip() for s in segs]:
                errors.append(f"{case_path.relative_to(ROOT)}: `input_locator` 在被引条目 {sref} 的 "
                              f"`selected_segments` 中无精确对应（段落文字改写后 case 侧必须跟随）")
                case_ref_bad += 1
    print(f"benchmark case 来源状态：{case_state_checked} 份 corpus_reference 案受检，"
          f"与被引语料不符 {case_state_bad} 处")
    print(f"benchmark case 引用面：`source_url` {case_url_checked} 份受检、`input_locator` "
          f"{case_locator_checked} 份受检（须精确命中被引条目 `selected_segments`），不符 {case_ref_bad} 处")
    # README 项目结构树 ⇄ 实际目录（2026-09-16 第十八批新增）：`README.md` 的「项目结构」树
    # 曾漏列 `scripts/`、`docs/` 与 `knowledge/conversation/`、`knowledge/hosting/`
    # （都是**随仓库发布**的目录）。判据：凡**未被 `.gitignore` 排除**的顶层目录与 `knowledge/`
    # 子目录，都必须出现在该树里；被排除的（corpus/、evals/、knowledge/sources/、
    # knowledge/practitioner_hypotheses/）是研究数据，不外显，合法缺席。
    ignore_lines = {
        line.strip().rstrip("/")
        for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith("*")
    }

    def gitignored(rel: str) -> bool:
        return rel in ignore_lines or f"{rel}/" in ignore_lines

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    tree_blocks = [b for b in readme_text.split("```") if "├──" in b or "└──" in b]
    tree_entries = set()
    for block in tree_blocks:
        # 判据必须同时认 `├` 与 `└` 两种连线符（`├──` 是中间项、`└──` 是每组最后一条），
        # 只认 `├──` 会让"树里明明列了"的目录被判成漏列（2026-09-16 第十九批：
        # 该闸门曾据 `knowledge/writing/` 报出假失败——树的末条正是 `└── writing/`）。
        tree_entries.update(
            m.group(1).strip().rstrip("/")
            for m in re.finditer(r"^[\s│]*[├└]──\s*([^\s]+)", block, re.MULTILINE)
        )
    tree_missing = 0
    for child in sorted(ROOT.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name == "__pycache__":
            continue
        if gitignored(child.name) or child.name in tree_entries:
            continue
        tree_missing += 1
        errors.append(f"README.md: 项目结构树未列出顶层目录 `{child.name}/`（该目录随仓库发布）")
    for child in sorted((ROOT / "knowledge").iterdir()):
        if not child.is_dir() or gitignored(f"knowledge/{child.name}") or child.name in tree_entries:
            continue
        tree_missing += 1
        errors.append(f"README.md: 项目结构树未列出 `knowledge/{child.name}/`（该目录随仓库发布）")
    print(f"README 项目结构树：{len(tree_entries)} 个条目，未列出的发布目录 {tree_missing} 个")
    # 归属字段卫生（2026-09-17 第三十一批新增闸门）：`hosting/` 8 条与派生 `raw_edited_pairs/`
    # 6 条把**说话人标签的冒号**写进了字段值（`speaker_or_author: ：伊拉娜`），标题也出现双冒号
    # （`…（二）：：伊拉娜片段`）——**任何既有闸门都不校验字段值的形态**，于是这类"从「XX：」
    # 标签里截错半边"的残留可以长期存在（读者无法判断是排版还是内容）。
    # 判据只看**会由标签误截产生的标点**（冒号／逗号／顿号／分号），不碰书名号与括号等
    # 合法起首字符（如 `《今日关注》主持人…`），避免制造假失败。
    field_punct = "：:，,；;、"
    field_records = 0
    field_bad = 0
    for item in (ROOT / "corpus").rglob("*.yaml"):
        if item.name == "index.yaml" or item.relative_to(ROOT / "corpus").parts[0] == "candidates":
            continue
        record = yaml.safe_load(item.read_text(encoding="utf-8")) or {}
        if not isinstance(record, dict):
            continue
        field_records += 1
        value = str(record.get("speaker_or_author", "")).strip()
        title = str(record.get("title", ""))
        problems = []
        if value and (value[0] in field_punct or value[-1] in field_punct):
            problems.append(f"speaker_or_author 首尾含标签标点「{value}」")
        if "：：" in value or "::" in value:
            problems.append("speaker_or_author 含双冒号")
        if "：：" in title or "::" in title:
            problems.append("title 含双冒号")
        if problems:
            field_bad += 1
            errors.append(
                f"{item.relative_to(ROOT)}: " + "；".join(problems)
                + "（多为从「XX：」说话者标签截取时把标点带入，须写名称本体）"
            )
    print(f"归属字段卫生：{field_records} 条语料受检，speaker_or_author／title 形态异常 {field_bad} 条")
    # 字段级乱码（2026-09-17 第四十六批新增闸门）：`commentary/` 实测 3 条条目的
    # `title`／`topic`／`analysis_notes`／`selected_segments` **整片为 GBK 字节按 Latin-1 存成的乱码**
    # （如 `[½ñÈÕ¹Ø×¢]´ïÀµ¼¯ÍÅÓëÎ÷·½·´»ªÊÆÁ¦`），而**任何既有闸门都不看字段的字符集**——
    # `validate_schemas` 只看键是否齐备、`check_links` 只看链接、归属字段卫生只看标点。
    # 判据：任意**字符串字段**中出现 **≥3 个连续的 Latin-1 高位/替换字符**（含 `\x80-\xff` 段与常见 mojibake 标点）
    # ⇒ 判为疑似乱码；这类串**可用 `latin-1 → gb18030` 精确还原**（实测 3/3 还原后与源页标题逐字一致）。
    # 只报"连续 ≥3 个"，避免把合法重音字母（如 `Zoë`）误判。
    mojibake = re.compile(
        r"[\u00a0-\u00ff\u0152\u0153\u0160\u0161\u0178\u017d\u017e\u0192\u02c6\u02dc"
        r"\u2020-\u2022\u2026\u2030\u2039\u203a\u20ac\u2122\ufffd]{3,}"
    )
    enc_records = 0
    enc_bad = 0

    def scan_strings(obj, path):
        if isinstance(obj, dict):
            for k, v in obj.items():
                scan_strings(v, f"{path}.{k}" if path else str(k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                scan_strings(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            hit = mojibake.search(obj)
            if hit:
                yield path, hit.group(0)[:40]

    for item in (ROOT / "corpus").rglob("*.yaml"):
        if item.name == "index.yaml":
            continue
        try:
            record = yaml.safe_load(item.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue  # 解析失败已由 validate_schemas 的解析守卫报出
        if not isinstance(record, dict):
            continue
        enc_records += 1
        for path, preview in scan_strings(record, ""):
            enc_bad += 1
            errors.append(
                f"{item.relative_to(ROOT)}: 字段 `{path}` 疑似**乱码**（`{preview}`）"
                "——多为 GBK 字节按 Latin-1 存成；可用 `latin-1 → gb18030` 还原后与源页核对"
            )
    print(f"字段乱码：{enc_records} 条语料受检，疑似乱码字段 {enc_bad} 处"
          f"（判据：连续 ≥3 个 Latin-1 高位／替换字符；可用 latin-1→gb18030 还原）")
    # 库内文件路径引用 ⇄ 实际存在（2026-09-17 第四十三批新增闸门）：条目里会写
    # `corpus/annotations/xxx.md` 这类**库内路径**作为"详档"指针；实测第四十二批曾写下一个
    # **当时并不存在**的标注档名（`named-hosting-deepread-20260917e.md`）——**任何既有闸门都拦不下**：
    # `check_links.py` 只查 Markdown 的 `[](...)` 链接，**管不到 YAML 文本里的路径**；
    # 而该条同时又因 `state: ANNOTATED` 无标注档引用报错，两者叠加时**先报的是别的错**，
    # 悬空引用极易被"已修好主症状"的错觉掩盖。判据：`corpus/**/*.yaml` 正文里的
    # `corpus/....md` 路径必须真实存在；**历史/探针语境**（沿用 HISTORICAL_MARKERS）跳过并计数。
    path_refs = 0
    path_missing = 0
    path_skipped = 0
    for item in (ROOT / "corpus").rglob("*.yaml"):
        if item.name == "index.yaml":
            continue
        for line in item.read_text(encoding="utf-8").splitlines():
            found = set(re.findall(r"corpus/[A-Za-z0-9_./\-\u4e00-\u9fff]+\.md", line))
            if not found:
                continue
            if any(mark in line for mark in HISTORICAL_MARKERS):
                path_skipped += len(found)
                continue
            for ref in sorted(found):
                path_refs += 1
                if not (ROOT / ref).exists():
                    path_missing += 1
                    errors.append(
                        f"{item.relative_to(ROOT)}: 库内路径引用不存在 `{ref}`"
                        "（Markdown 链接检查不管 YAML 文本里的路径）"
                    )
    print(f"库内路径引用：{path_refs} 处受检，解析不到 {path_missing} 处（历史/探针语境跳过 {path_skipped} 处）")
    # ㉗ 交付物安装脚本 `install.sh` ⇄ 可执行性与引用文件（2026-09-17 第六十批新增）：
    # `install.sh` 是**用户安装本 skill 的唯一入口**（默认链接到 `~/.claude/skills/cida`），
    # 但**此前不在任何检查内**——既无语法检查，也无冒烟测试；脚本被改坏（shell 语法错、
    # 提示语引用的 `SKILL.md`／`AGENTS.md` 被改名、链接目标写错）**不会让任何闸门变红**（"缺了但全绿"同族）。
    # 判据：①`bash -n` 语法通过；②提示语引用的根文件存在；③**链接模式冒烟**（临时目录内 `--dir`）：
    # 安装后 `cida/SKILL.md` 可读、**重复安装必须拒绝**（exit≠0）。
    # 边界：`--copy` 依赖 `rsync`，为免在缺 rsync 的机器上**假失败**，**不入闸门**（本批已手工双模式验证）。
    install_sh = ROOT / "install.sh"
    install_checks = 0
    if install_sh.exists():
        syntax = subprocess.run(["bash", "-n", str(install_sh)], capture_output=True, text=True)
        if syntax.returncode != 0:
            errors.append(f"install.sh: `bash -n` 语法检查失败：{(syntax.stderr or '').strip()[:200]}")
        else:
            install_checks += 1
        install_text = install_sh.read_text(encoding="utf-8")
        for name in ("SKILL.md", "AGENTS.md"):
            if name in install_text:
                if (ROOT / name).exists():
                    install_checks += 1
                else:
                    errors.append(f"install.sh: 提示语引用 `{name}`，但根目录不存在该文件（安装说明会指向空文件）")
        with tempfile.TemporaryDirectory() as tmp:
            first = subprocess.run(["bash", str(install_sh), "--dir", tmp],
                                   capture_output=True, text=True)
            if first.returncode != 0 or not (Path(tmp) / "cida" / "SKILL.md").exists():
                errors.append(
                    f"install.sh: 链接模式冒烟失败（exit={first.returncode}；"
                    f"{(first.stderr or first.stdout).strip()[:160]}）"
                )
            else:
                install_checks += 1
            again = subprocess.run(["bash", str(install_sh), "--dir", tmp],
                                   capture_output=True, text=True)
            if again.returncode == 0:
                errors.append("install.sh: 目标已存在时**未拒绝**重装（应 exit≠0）")
            else:
                install_checks += 1
        print(f"交付物安装脚本：install.sh {install_checks} 项检查（语法／引用文件／链接冒烟／拒绝重装）")
    # ㉘ 回归说明档 `evals/regression/README.md` 的当前值 ⇄ 实际（2026-09-17 第六十一批新增）：
    # 该文件描述"统一入口会依次执行 …"，其中写有"**N 案 benchmark inventory**"与"**N 案人工盲评队列**"。
    # 它**既不在 8 份 `current_docs` 的 5 个模式内**（⑩ 只认 registry／机制节点／图谱关系／
    # `benchmark inventory`／正式语料，且只扫那 8 份），**也不在 ⑯ 覆盖的 `EVALS.md`／
    # `evals/benchmark/README.md`／`evals/human_review/README.md`／`CORPUS.md` 之内**——
    # 实测两处均停在旧值 **150**，而实际 inventory **158**、盲评队列（`ready`＋`await_source_text`）**158**，
    # 属"当前值留在旧轮次"族在**第五处对象**重现（前四处：`HANDOFF` §2／`docs/index.html`／
    # `EXTERNAL_INPUT_TODO`／`EVALS.md` 与两份 README）。
    # 判据：`N 案 benchmark inventory` ＝ `*_case.yaml` 实际份数；`N 案人工盲评队列` ＝ `ready`＋`await_source_text`。
    reg_readme = ROOT / "evals" / "regression" / "README.md"
    if reg_readme.exists():
        reg_text = reg_readme.read_text(encoding="utf-8")
        queue_total = ready + await_text
        reg_claims = 0
        for m in re.finditer(r"(\d+)\s*案 benchmark inventory", reg_text):
            reg_claims += 1
            if int(m.group(1)) != inventory:
                errors.append(
                    f"evals/regression/README.md: 写 `{m.group(1)} 案 benchmark inventory`，"
                    f"实际 `*_case.yaml` 有 {inventory} 份（当前值必须随库更新）"
                )
        for m in re.finditer(r"(\d+)\s*案人工盲评队列", reg_text):
            reg_claims += 1
            if int(m.group(1)) != queue_total:
                errors.append(
                    f"evals/regression/README.md: 写 `{m.group(1)} 案人工盲评队列`，"
                    f"实际 `ready`＋`await_source_text` ＝ {queue_total}（当前值必须随库更新）"
                )
        print(f"回归说明档数字：evals/regression/README.md {reg_claims} 处断言"
              f"（实际 inventory {inventory}／盲评队列 {queue_total}）")
    # ㉙ 反模式条目结构 ⇄ `schemas/anti_pattern.yaml` 声明（2026-09-17 第六十二批新增）：
    # `knowledge/anti_patterns/README.md` 一直写着"每个反模式记录：症状、实例、伤害机理、修复策略、例外。
    # **Schema 见 `schemas/`（anti_pattern 条目）**"——但 `schemas/` 里**从来没有 anti_pattern.yaml**
    # （只有 source／corpus_item／candidate／mechanism／raw_edited_pair／benchmark_case／
    # style_profile／diagnosis 八个），且**没有任何检查读反模式条目的小节结构**：
    # 机制节点有 `mechanism.yaml` ＋ 第 ⑭ 条结构闸门，**反模式侧两者皆无**——属"**声明了却没落地**"＋
    # "**缺了但全绿**"复合族（与第十九批 `metaphor_analogy.md` 缺小节同族）。
    # 判据：①`schemas/anti_pattern.yaml` 必须存在（README 指向的 schema 不得悬空）；
    # ②该 schema 中**未注释**的顶层键＝必需小节，`knowledge/anti_patterns/*.md`（除 README）逐条必须含 `## <key>`。
    # **边界（不制造假失败）**：`example` 为可选（8 条中 4 条单列，其余以「真实样本验证」承载同类证据），
    # schema 中以注释登记，**不入必需集**。
    anti_schema = ROOT / "schemas" / "anti_pattern.yaml"
    anti_checked = 0
    anti_gap = 0
    if not anti_schema.exists():
        errors.append("knowledge/anti_patterns/README.md: 指向 `schemas/anti_pattern.yaml`，"
                      "但该 schema 文件不存在（声明悬空）")
    else:
        anti_required = [
            line.split(":", 1)[0].strip()
            for line in anti_schema.read_text(encoding="utf-8").splitlines()
            if line and not line.lstrip().startswith("#") and ":" in line
        ]
        for path in sorted((ROOT / "knowledge" / "anti_patterns").glob("*.md")):
            if path.name == "README.md":
                continue
            anti_checked += 1
            heads = set(re.findall(r"^##\s+(\S+)", path.read_text(encoding="utf-8"), re.MULTILINE))
            missing = [key for key in anti_required if key not in heads]
            if missing:
                anti_gap += 1
                errors.append(
                    f"{path.relative_to(ROOT)}: 缺必需小节 {missing}"
                    "（结构声明见 schemas/anti_pattern.yaml 与 knowledge/anti_patterns/README.md）"
                )
        print(f"反模式条目结构：{anti_checked} 条受检，必需小节 {len(anti_required)} 个"
              f"（{ '／'.join(anti_required) }），缺小节 {anti_gap} 条")
    # ㉚ `EXTERNAL_INPUT_TODO.md` §E「深读续做」行的逐类 `READ` 数 ⇄ 实际（2026-09-17 第六十四批新增）：
    # 该行写"`speeches` READ N、`commentary` READ N、`blogs` READ N、`interviews` READ N、
    # `hosting` READ **N**、`podcasts` READ N"——是**自称当前值**，但**此前不在任何闸门内**
    # （⑯ 只覆盖 §「现状」行与能力表行的 inventory／正例层／ready／await）。第六十三／六十四批
    # 各升 2 条 `ANNOTATED` 后，该行 `speeches`／`interviews` 当场变旧（"当前值留在旧轮次"族同源）。
    # 判据：逐类 `READ` 数 ＝ `corpus/<cat>/*.yaml` 中 `state: READ` 的实际条数（现场复算）。
    # 边界：只扫 `## E.` 之后的小节，避免把正文别处的 `` `x` READ `` 误当断言。
    e_table = 0
    if todo_path.exists():
        todo_e = todo_path.read_text(encoding="utf-8")
        todo_e = todo_e.split("## E.", 1)[1] if "## E." in todo_e else ""
        cat_read: collections.Counter = collections.Counter()
        for item in (ROOT / "corpus").glob("*/*.yaml"):
            if item.name == "index.yaml":
                continue
            st = re.search(r'^state:\s*"?(\w+)"?\s*(?:#.*)?$',
                           item.read_text(encoding="utf-8"), re.MULTILINE)
            if st and st.group(1) == "READ":
                cat_read[item.relative_to(ROOT / "corpus").parts[0]] += 1
        for m in re.finditer(r"`(\w+)` READ (?:\*\*)?(\d+)", todo_e):
            e_table += 1
            cat, n = m.group(1), int(m.group(2))
            if cat_read.get(cat, 0) != n:
                errors.append(
                    f"EXTERNAL_INPUT_TODO.md: §E「深读续做」行写 `{cat}` READ {n}，"
                    f"实际 {cat_read.get(cat, 0)} 条（当前值必须随库更新）"
                )
        print(f"待办清单深读行：§E 逐类 READ 数 {e_table} 处受检"
              f"（实际 { '／'.join(f'{c} {cat_read.get(c, 0)}' for c in ('speeches','commentary','blogs','interviews','hosting','podcasts')) }）")
    # ㉛ 对外 README（中／英）的"当前值" ⇄ 实际（2026-09-17 第六十五批新增，发布前收口）：
    # 发布面最严重的一类陈旧——`README_EN.md` 的 §Status 整段停在 **v0.6.9**（935 条语料／150 案／
    # 80 对配对／"8 of 41 validated"／registry 130 条），而**第 ⑩ 条的模式是纯中文写法**
    # （`registry…条`／`机制节点`／`条关系`／`benchmark inventory…案`／`正式语料…条`）——
    # **英文写法（`entries`／`Chinese / international`／`-case`／`All N … validated`）完全不在覆盖内**，
    # 属"**闸门模式写得比实际写法窄**"（project_memory 已记该根因）；同时 `README.md` 的**版本徽章**
    # （`badge/版本-1.0.0-`）**也从未与 CHANGELOG 台账比对**。判据：逐条按英文写法取数、现场复算比对。
    zh_readme = ROOT / "README.md"
    en_readme = ROOT / "README_EN.md"
    readme_claims = 0
    if changelog_head and zh_readme.exists():
        for m in re.finditer(r"badge/版本-(\d+\.\d+\.\d+)-", zh_readme.read_text(encoding="utf-8")):
            readme_claims += 1
            if m.group(1) != changelog_head.group(1):
                errors.append(
                    f"README.md: 版本徽章写 `{m.group(1)}`，而 CHANGELOG 台账首条是 "
                    f"v{changelog_head.group(1)}（徽章须随台账更新）"
                )
    if changelog_head and en_readme.exists():
        en_text = en_readme.read_text(encoding="utf-8")
        reg2 = yaml.safe_load((ROOT / "knowledge" / "sources" / "registry.yaml")
                              .read_text(encoding="utf-8")) or []
        acc2 = collections.Counter(str(x.get("access_status")) for x in reg2)
        lang2 = collections.Counter(str(x.get("language")) for x in reg2)
        validated2 = sum(1 for p in mechanism_nodes
                         if "confidence: validated" in p.read_text(encoding="utf-8"))
        pairs2 = len({p.name for p in (ROOT / "evals" / "human_review" / "pending_pairs").glob("pair_*.md")
                      if not p.name.endswith("_key.md")})
        en_checks = [
            (r"^v(\d+\.\d+\.\d+): the corpus", changelog_head.group(1), "版本号"),
            (r"formal corpus contains \*\*([\d,]+)\*\* positive items", formal, "正式语料条数"),
            (r"The \*\*(\d+)-case\*\* benchmark inventory", inventory, "benchmark inventory"),
            (r"\*\*(\d+) anonymous blind-review pairs", pairs2, "匿名配对数"),
            (r"\*\*All (\d+) mechanism nodes", len(mechanism_nodes), "机制节点数"),
            (r"registry: (\d+) entries", len(reg2), "registry 条数"),
            (r"(\d+)\s+Chinese\s*/\s*(\d+)\s+international",
             (lang2.get("zh", 0), lang2.get("en", 0)), "registry 语言拆分"),
            (r"`full_text (\d+)`,\s*`key_chapters (\d+)`,\s*`review_only (\d+)`,\s*`metadata_only (\d+)`",
             (acc2.get("full_text", 0), acc2.get("key_chapters", 0),
              acc2.get("review_only", 0), acc2.get("metadata_only", 0)), "registry access_status 拆分"),
        ]
        for pat, actual, label in en_checks:
            for m in re.finditer(pat, en_text, re.MULTILINE):
                readme_claims += 1
                got = m.groups()
                if len(got) == 1:
                    ok = got[0].replace(",", "") == str(actual)
                else:
                    ok = tuple(int(x.replace(",", "")) for x in got) == actual
                if not ok:
                    errors.append(
                        f"README_EN.md: 写 `{' / '.join(got)}`（{label}），与实际 {actual} 不符"
                        "（对外 README 的数字必须随库更新）"
                    )
        if (re.search(r"\*\*All \d+ mechanism nodes", en_text)
                and validated2 != len(mechanism_nodes)):
            errors.append(
                f"README_EN.md: 声称「All … mechanism nodes … validated」，"
                f"而实际 validated {validated2}／{len(mechanism_nodes)}"
                "（不得用 All 掩盖未升级节点）"
            )
        # 同族**假绿**（本批探针当场发现）：英文数词写法「Eight of the 41 mechanism nodes … validated」
        # **无法被 `(\d+)` 匹配**（"Eight" 是词不是数字），若只按数字写模式，这类表述会**静默不匹配**
        # ——与"批号用汉字、正则只写 `[0-9]+` 会假绿"完全同族。故本闸门**不猜数词**，
        # 而是**禁止不可机读的表述**：凡出现「<词或数> of the <数> mechanism nodes … validated」，直接判错并要求
        # 改写为可机读的「All N mechanism nodes」（N ＝ 实际节点数）。
        m_word = re.search(r"([A-Za-z]+|\d+)\s+of the (\d+) mechanism nodes\s+have been upgraded to `validated`",
                           en_text)
        if m_word:
            errors.append(
                f"README_EN.md: 用「{m_word.group(1)} of the {m_word.group(2)}」表述 validated 节点数——"
                "**不可机读**（英文数词无法直接比对）；须改写为「All N mechanism nodes」且 N ＝ 实际节点数"
                "（与「批号用汉字」同族：判据字符集写窄会假绿）"
            )
    print(f"对外 README 数字：{readme_claims} 处受检（README.md 版本徽章 + README_EN §Status 英文写法）")
    print(f"来源追踪检查：{checked} 个机制节点，{len(corpus_ids)} 条语料 id 索引，{id_refs} 处 corpus_id 引用")
    print(f"语料标注档：{linked} 条 ANNOTATED/VALIDATED 已按 corpus_id 挂到标注档，"
          f"未挂 {unlinked} 条，豁免类别 {exempt} 条（{sorted(EXEMPT_CATEGORIES)}：走聚合分析文档）")
    print(f"state 行内联注释：{state_comments} 条（**已按容错计数**；为免静默漏计，"
          f"建议改写为独立字段——见 2026-09-17 第三十九批说明）")
    print(f"关联目标：{related_ok} 处 related_nodes 引用可解析"
          f"（机制 {len(mechanism_files)} / 反模式 {len(anti_pattern_files)} / 根文档 {len(ROOT_DOCS)}）；"
          f"悬空 {related_bad} 处、缺 related_nodes 段 {related_no_section} 处")
    print(f"机制反模式：{pairs} 对双向登记（机制侧 related_nodes ↔ 反模式侧 `../mechanisms/` 反指），"
          f"双向登记缺口 {asymmetry} 处")
    for warning in warnings:
        print(f"  ℹ {warning}")
    if errors:
        for error in errors:
            print(f"  ✗ {error}")
        return 1
    print("来源追踪通过 ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
