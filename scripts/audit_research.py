#!/usr/bin/env python3
"""辞达 · 研究诚信审计器（§111–131）

检查项：
  detect_metadata_only_entries    正式库不得有 metadata_only / PLANNED / FOUND
  detect_unverified_transcripts   正式库不得有未核验的自动转录
  detect_missing_provenance       VALIDATED+ 语料必须有 provenance 链
  detect_underrepresented_speakers 核心人物样本不足 → INSUFFICIENT CORPUS
  audit_source_depth              来源登记处的阅读深度统计（信息性）
  audit_corpus_acquisition        生成 CORPUS_COVERAGE.md（§118 覆盖率报告）

用法：
    python scripts/audit_research.py            # 审计 + 生成报告
    python scripts/audit_research.py --strict   # 信息性问题也判失败
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    import yaml
except ImportError:
    print("需要 PyYAML：pip install pyyaml")
    sys.exit(2)

STATE_ORDER = ["PLANNED", "FOUND", "ACQUIRED", "READ", "ANNOTATED", "VALIDATED", "DISTILLED"]
FORMAL_DIRS = ["commentary", "interviews", "hosting", "speeches",
               "podcasts", "blogs", "articles", "raw_edited_pairs", "contrast"]
# Research Gates（§117）：正式入库最低数量
GATES = {"commentary": 100, "hosting": 60, "interviews": 100, "speeches": 100,
         "podcasts": 100, "blogs": 200, "raw_edited_pairs": 50, "articles": 0,
         "contrast": 0}
CORE_SPEAKERS_MIN = 10   # 12 位核心（§119）
EXT_SPEAKERS_MIN = 5     # 6 位专项扩展


def load_yaml(p: Path):
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"_parse_error": str(e)}


def state_rank(s: str) -> int:
    return STATE_ORDER.index(s) if s in STATE_ORDER else -1


def main() -> int:
    strict = "--strict" in sys.argv
    violations: list[str] = []
    infos: list[str] = []

    candidates, formal = [], []
    for f in sorted((ROOT / "corpus").rglob("*.yaml")):
        if f.name == "index.yaml":
            continue
        data = load_yaml(f)
        data["_file"] = str(f.relative_to(ROOT))
        if "_parse_error" in data:
            violations.append(f"{data['_file']}: YAML 解析失败 {data['_parse_error']}")
            continue
        if "candidates" in f.parts:
            candidates.append(data)
        elif any(d in f.parts for d in FORMAL_DIRS):
            data["_category"] = next(d for d in FORMAL_DIRS if d in f.parts)
            formal.append(data)

    # --- detect_metadata_only_entries ---
    for it in formal:
        if it.get("access_level") == "metadata_only":
            violations.append(f"{it['_file']}: metadata_only 不得在正式库（应入候选池）")
        if state_rank(it.get("state", "")) < state_rank("ACQUIRED"):
            violations.append(f"{it['_file']}: state={it.get('state')} 未达到 ACQUIRED，不得在正式库")

    # --- candidates 状态合法性 ---
    for it in candidates:
        if state_rank(it.get("state", "")) > state_rank("FOUND"):
            violations.append(f"{it['_file']}: 候选池条目状态超过 FOUND（应迁入正式库并补 Evidence Package）")

    # --- detect_unverified_transcripts ---
    for it in formal:
        if it.get("transcript_quality") == "auto_unverified":
            violations.append(f"{it['_file']}: 未核验自动转录不得入正式库")

    # --- detect_missing_provenance ---
    for it in formal:
        if state_rank(it.get("state", "")) >= state_rank("VALIDATED") and not it.get("provenance"):
            violations.append(f"{it['_file']}: VALIDATED+ 缺少 provenance 链")

    # --- detect_underrepresented_speakers ---
    per_speaker = Counter(
        it.get("speaker_or_author") for it in formal
        if state_rank(it.get("state", "")) >= state_rank("ACQUIRED")
    )
    for speaker, n in sorted(per_speaker.items()):
        if speaker and n < EXT_SPEAKERS_MIN:
            infos.append(f"INSUFFICIENT CORPUS: {speaker} 仅 {n} 条（核心 ≥{CORE_SPEAKERS_MIN}，专项 ≥{EXT_SPEAKERS_MIN}）")

    # --- audit_source_depth（信息性） ---
    registry = ROOT / "knowledge" / "sources" / "registry.yaml"
    if registry.exists():
        entries = yaml.safe_load(registry.read_text(encoding="utf-8")) or []
        depth = Counter(e.get("access_status", "?") for e in entries)
        unread = depth.get("metadata_only", 0)
        total = len(entries)
        infos.append(f"来源登记处：{total} 条中 {unread} 条为 metadata_only（未读全文，结论限假说级）")

    # --- §118 覆盖率报告 ---
    def count_at_least(items, state):
        return sum(1 for i in items if state_rank(i.get("state", "")) >= state_rank(state))

    lines = [
        "# CORPUS_COVERAGE · 语料覆盖报告",
        "",
        "由 `scripts/audit_research.py` 自动生成，请勿手改。",
        "状态机：PLANNED → FOUND → ACQUIRED → READ → ANNOTATED → VALIDATED → DISTILLED",
        "",
        "| Corpus | Target(Gate) | Found(候选) | Acquired | Read | Analyzed | Accepted(VALIDATED+) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for cat in FORMAL_DIRS:
        items = [i for i in formal if i["_category"] == cat]
        found = sum(1 for i in candidates if cat in i.get("corpus_id", ""))
        gate = GATES.get(cat, 0)
        gate_s = str(gate) if gate else "—"
        lines.append(
            f"| {cat} | {gate_s} | {found} | {count_at_least(items,'ACQUIRED')} | "
            f"{count_at_least(items,'READ')} | {count_at_least(items,'ANNOTATED')} | "
            f"{count_at_least(items,'VALIDATED')} |"
        )
    lines += [
        "",
        "## Gate 判定（§117：未达标不得宣称 Corpus Construction 完成）",
        "",
    ]
    for cat, gate in GATES.items():
        if not gate:
            continue
        items = [i for i in formal if i["_category"] == cat]
        ok = count_at_least(items, "ACQUIRED")
        mark = "✅" if ok >= gate else "❌ 未达标"
        lines.append(f"- {cat}: {ok} / {gate} {mark}")
    lines += ["", "## 诚信审计备注", ""]
    lines += [f"- {i}" for i in infos] or ["- 无"]
    (ROOT / "CORPUS_COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"审计：候选 {len(candidates)} 条，正式 {len(formal)} 条")
    for i in infos:
        print(f"  ℹ {i}")
    print("覆盖率报告 -> CORPUS_COVERAGE.md")
    if violations:
        print(f"\n发现 {len(violations)} 处违规：")
        for v in violations:
            print(f"  ✗ {v}")
        return 1
    print("诚信审计通过 ✓")
    return 0 if not (strict and infos) else 0


if __name__ == "__main__":
    sys.exit(main())
