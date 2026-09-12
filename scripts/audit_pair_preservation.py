#!/usr/bin/env python3
"""audit_pair_preservation.py · 盲评配对 Preservation 机械审计

对 pending_pairs/ 下每份配对，从「Preservation 旁观项」节提取 **加粗** 关键口径，
逐项核对是否出现在「版本 A」与「版本 B」正文（去除全部空白后精确匹配）。

用途与边界：
- 这是机械预筛（presence check），不替代人工评审（BLIND_REVIEW_PACK §6）；
- Baseline 版本按生成纪律允许弱化个别限定词，其缺失属"设计性对照"，
  Skill 版本缺失则需回溯修复；
- 短口径（≤3 字符）自动向后借 2 字上下文（如 "80"→"80周年"）以降低误报；
- 可选 --version-map 指定揭盲映射（pair号=A或B=Skill）用于区分设计性缺失；
  缺省时按项目统一规则：偶数 pair A=Skill，奇数 pair B=Skill（pair_001 例外 B）。

输出：逐缺失明细 + 汇总（JSON 到 stdout 或 --out 指定文件）。
"""
import argparse
import glob
import json
import os
import re
import sys

SECTION_RE = re.compile(
    r"## 版本 A\n\n(.*?)\n## 版本 B\n\n(.*?)\n## 五问", re.S)
PRESV_RE = re.compile(r"## Preservation 旁观项\n+(.*)\Z", re.S)
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def extract_items(presv: str):
    """提取旁观项中的加粗口径；短口径向后补上下文（截到标点，最多4字）。"""
    items = []
    for m in BOLD_RE.finditer(presv):
        span = m.group(1)
        span = re.sub(r"\*\*", "", span)
        if len(norm(span)) <= 3:
            tail = presv[m.end():m.end() + 5]
            tail = re.split(r"[，。；：——）」』\"'、（]", tail)[0][:4]
            if tail:
                items.append((span + tail, f"short+ctx:{tail}"))
                continue
        items.append((span, ""))
    return items


def skill_side(pair_no: int) -> str:
    if pair_no == 1:
        return "B"
    return "A" if pair_no % 2 == 0 else "B"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs-dir", default="evals/human_review/pending_pairs")
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--last", type=int, default=999)
    ap.add_argument("--out")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.pairs_dir, "pair_*.md")))
    files = [f for f in files if not f.endswith("_key.md")]
    report = []
    for f in files:
        base = os.path.basename(f)
        m = re.match(r"pair_(\d+)_", base)
        if not m:
            continue
        no = int(m.group(1))
        if not (args.first <= no <= args.last):
            continue
        if re.search(r"pair_\d+.*bench\.", base) is None and "real_material" not in base:
            continue
        text = open(f, encoding="utf-8").read()
        mv = SECTION_RE.search(text)
        mp = PRESV_RE.search(text)
        if not mv or not mp:
            report.append({"pair": base, "error": "section_missing"})
            continue
        va, vb = norm(mv.group(1)), norm(mv.group(2))
        items = extract_items(mp.group(1))
        in_a = [it for it, _ in items if norm(it) in va]
        in_b = [it for it, _ in items if norm(it) in vb]
        meta_or_neither = [it for it, _ in items
                           if norm(it) not in va and norm(it) not in vb]
        skill = skill_side(no)
        skill_v, base_v = (va, vb) if skill == "A" else (vb, va)
        skill_missing = [it for it in in_b + in_b if skill == "A" and it not in in_a]
        if skill == "A":
            skill_missing = [it for it in in_b if it not in in_a]
            base_missing = [it for it in in_a if it not in in_b]
        else:
            skill_missing = [it for it in in_a if it not in in_b]
            base_missing = [it for it in in_b if it not in in_a]
        report.append({
            "pair": base,
            "items": len(items),
            "skill_side": skill,
            "in_both": len([i for i in set(in_a) & set(in_b)]),
            "meta_or_neither": meta_or_neither,
            "skill_missing": skill_missing,
            "baseline_missing": base_missing,
        })

    n_pairs = len(report)
    n_items = sum(r.get("items", 0) for r in report)
    skill_misses = [r for r in report if r.get("skill_missing")]
    base_misses = [r for r in report if r.get("baseline_missing")]
    summary = {
        "pairs_checked": n_pairs,
        "watch_items": n_items,
        "pairs_with_skill_missing": len(skill_misses),
        "pairs_with_baseline_missing": len(base_misses),
        "detail": report,
    }
    out = json.dumps(summary, ensure_ascii=False, indent=1)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    print(f"pairs={n_pairs} items={n_items} "
          f"skill_missing_pairs={len(skill_misses)} "
          f"baseline_missing_pairs={len(base_misses)}")
    for r in skill_misses:
        print(f"  SKILL-MISS {r['pair']}: {r['skill_missing']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
