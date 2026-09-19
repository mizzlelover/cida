#!/usr/bin/env python3
"""process_blind_review.py · 盲评答卷处理与揭盲统计

用途：人工评审在 `evals/human_review/answer_sheet.csv` 填写完成后，
本脚本机械完成 BLIND_REVIEW_PACK §6 的"揭盲-汇总"段：

  1. 校验答卷结构（选项枚举、分数范围、Preservation 违例标注）；
  2. 按**揭盲钥文件**（`pending_pairs/keys_*.md` + `pair_001_key.md`，经 `blind_keys.py` 读取）
     把 A/B 映射为 Skill/Baseline；**缺钥的行直接判错并中止**，不用公式推断；
  3. 分问题、分角色汇总裁决；输出配对级明细与总体统计；
  4.  Preservation 违例：Skill 版违例行直接列出（按 §6 触发修复-回归循环），
     Baseline 版违例行仅计数（属对照基线，无需修复）。

为何不以"奇偶公式"揭盲（2026-09-16 勘误）：公式（偶数 A=Skill、奇数 B=Skill）源自首批
20 对，但 `keys_ready10.md` 早写明 **pair_012/014/016/018/020 的 A 侧是 Baseline**；
按公式处理这五对会把 Baseline 的答卷记成 Skill。映射现以 keys 文件为唯一权威。

边界（不得违反）：
- 本脚本只处理人工填写的答卷，不生成、不补全、不猜测任何评分；
- 空行按"未评审"统计并跳过，不进入均值；脚本输出中必须保留
  "reviewed/total"口径，禁止把部分评审写成完整验收；
- 模型生成的"模拟评审"不得写入 answer_sheet.csv（诚信边界见 HANDOFF §5）。

用法：
  python3 scripts/process_blind_review.py \
      --answers evals/human_review/answer_sheet.csv \
      --out evals/pairwise/summary_YYYYMMDD.md [--json out.json]
"""
import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blind_keys import load_keys  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAIRS_DIR = ROOT / "evals" / "human_review" / "pending_pairs"
_KEYS: dict[int, str] | None = None

CHOICES = {"A", "B", "平", ""}
SCORE_COLS = ["readability_score_A", "readability_score_B",
              "credibility_score_A", "credibility_score_B"]
PAIR_COLS = ["easier_to_read", "more_natural", "more_thoughtful",
             "more_like_conversation", "more_continue_reading"]
ROLE_COLS = ["ordinary_reader_choice", "professional_reader_choice",
             "content_creator_choice", "editor_choice"]


def skill_side(pair_id: str) -> str:
    """揭盲映射以 keys 文件为准（不再用奇偶公式：pair_012/014/016/018/020 的 A 侧是 Baseline，
    公式会把这五对反标）。缺钥时抛 KeyError——不猜、不静默回退。"""
    global _KEYS
    if _KEYS is None:
        _KEYS = load_keys(PAIRS_DIR)
    no = int(str(pair_id).replace("pair_", ""))
    if no not in _KEYS:
        raise KeyError(f"{pair_id}: keys_*.md 未登记揭盲钥")
    return _KEYS[no]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", default="evals/human_review/answer_sheet.csv")
    ap.add_argument("--out", required=True)
    ap.add_argument("--json")
    args = ap.parse_args()

    path = Path(args.answers)
    if not path.exists():
        print(f"answer sheet not found: {path}", file=sys.stderr)
        return 2
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    if not rows:
        print("answer sheet is empty", file=sys.stderr)
        return 2

    reviewed, incomplete, invalid = [], [], []
    for r in rows:
        pid = (r.get("pair_id") or "").strip()
        if not pid:
            continue
        errs = []
        for c in PAIR_COLS + ROLE_COLS:
            if (r.get(c) or "").strip() not in CHOICES:
                errs.append(f"{c}={r.get(c)!r} 非合法枚举")
        for c in SCORE_COLS:
            v = (r.get(c) or "").strip()
            if v == "":
                continue
            try:
                if not 0 <= float(v) <= 10:
                    errs.append(f"{c}={v} 超出 0-10")
            except ValueError:
                errs.append(f"{c}={v} 非数字")
        filled_pairs = [c for c in PAIR_COLS if (r.get(c) or "").strip()]
        if not filled_pairs and not any((r.get(c) or "").strip() for c in SCORE_COLS):
            continue  # 整行未评 → 未评审
        if errs:
            invalid.append((pid, errs))
            continue
        if len(filled_pairs) < len(PAIR_COLS):
            incomplete.append(pid)
        reviewed.append(r)

    # 揭盲汇总
    missing_keys = []
    side_of: dict[str, str] = {}
    for r in reviewed:
        pid = r["pair_id"].strip()
        try:
            side_of[pid] = skill_side(pid)
        except KeyError:
            missing_keys.append(pid)
    if missing_keys:
        print("缺揭盲钥（keys_*.md 未登记），无法揭盲——不按公式推断：", file=sys.stderr)
        for pid in missing_keys:
            print(f"  {pid}", file=sys.stderr)
        return 2
    verdict = {q: Counter() for q in PAIR_COLS}
    skill_wins = Counter()
    role_pref = {role: Counter() for role in ROLE_COLS}
    score_sum = {c: [0.0, 0] for c in SCORE_COLS}
    skill_score_sum = {"readability": [0.0, 0], "credibility": [0.0, 0]}
    base_score_sum = {"readability": [0.0, 0], "credibility": [0.0, 0]}
    skill_violations, base_violations = [], []

    for r in reviewed:
        pid = r["pair_id"].strip()
        side = side_of[pid]
        for q in PAIR_COLS:
            v = (r.get(q) or "").strip()
            verdict[q][v] += 1
            if v in ("A", "B"):
                (skill_wins if v == side else skill_wins)["Skill" if v == side else "Baseline"] += 1
        for role in ROLE_COLS:
            v = (r.get(role) or "").strip()
            if v in ("A", "B"):
                role_pref[role]["Skill" if v == side else "Baseline"] += 1
            elif v == "平":
                role_pref[role]["平"] += 1
        for c in SCORE_COLS:
            v = (r.get(c) or "").strip()
            if v:
                score_sum[c][0] += float(v)
                score_sum[c][1] += 1
        for metric in ("readability", "credibility"):
            vs, vb = (r.get(f"{metric}_score_A") or "").strip(), (r.get(f"{metric}_score_B") or "").strip()
            if vs:
                (skill_score_sum if side == "A" else base_score_sum)[metric][0] += float(vs)
                (skill_score_sum if side == "A" else base_score_sum)[metric][1] += 1
            if vb:
                (skill_score_sum if side == "B" else base_score_sum)[metric][0] += float(vb)
                (skill_score_sum if side == "B" else base_score_sum)[metric][1] += 1
        viol = (r.get("preservation_violation_version") or "").strip()
        note = (r.get("preservation_violation_note") or "").strip()
        if viol in ("A", "B"):
            entry = {"pair": pid, "note": note}
            (skill_violations if viol == side else base_violations).append(entry)

    total = len(rows)
    n = len(reviewed)
    lines = [
        f"# 盲评汇总 · {date.today().isoformat()}",
        "",
        f"- 答卷行数：{total}；已评审：**{n}/{total}**"
        f"（{'完整' if not incomplete else '存在五问不全的行：' + ', '.join(incomplete)}）",
        f"- 无效行（未进入统计）：{len(invalid)}",
        "",
        "## 五问 Pairwise（揭盲后）",
        "",
    ]
    label = {"Skill": "Skill 版", "Baseline": "Baseline 版", "平": "平"}
    qnames = {"easier_to_read": "更容易读", "more_natural": "更自然",
              "more_thoughtful": "更有思想", "more_like_conversation": "更像真实人在交流",
              "more_continue_reading": "更愿意继续读"}
    for q in PAIR_COLS:
        sk = sum(1 for r in reviewed if (r.get(q) or "").strip() == side_of[r["pair_id"].strip()])
        bl = sum(1 for r in reviewed if (r.get(q) or "").strip() and (r.get(q) or "").strip() != "平"
                 and (r.get(q) or "").strip() != side_of[r["pair_id"].strip()])
        tie = verdict[q].get("平", 0)
        lines.append(f"- {qnames[q]}：Skill版 {sk} / Baseline版 {bl} / 平 {tie}")
    lines += ["", "## 四类角色偏好（揭盲后）", ""]
    rnames = {"ordinary_reader_choice": "普通读者", "professional_reader_choice": "专业读者",
              "content_creator_choice": "内容创作者", "editor_choice": "编辑"}
    for role in ROLE_COLS:
        c = role_pref[role]
        lines.append(f"- {rnames[role]}：Skill版 {c.get('Skill', 0)} / Baseline版 {c.get('Baseline', 0)} / 平 {c.get('平', 0)}")
    lines += ["", "## 评分均值（0-10，已评部分）", ""]
    for metric in ("readability", "credibility"):
        s = skill_score_sum[metric]
        b = base_score_sum[metric]
        sa = f"{s[0]/s[1]:.2f}" if s[1] else "—"
        ba = f"{b[0]/b[1]:.2f}" if b[1] else "—"
        lines.append(f"- {metric}：Skill版 {sa}（n={s[1]}）/ Baseline版 {ba}（n={b[1]}）")
    lines += ["", "## Preservation 违例", ""]
    lines.append(f"- Skill 版违例：**{len(skill_violations)}**（按 BLIND_REVIEW_PACK §6 触发修复-回归循环）")
    for e in skill_violations:
        lines.append(f"  - {e['pair']}：{e['note']}")
    lines.append(f"- Baseline 版违例：{len(base_violations)}（对照基线，仅计数不修复）")
    lines += ["", "> 口径声明：以上统计仅覆盖人工已填行；未填行不计入均值，",
              "> 部分评审不得写成完整验收（HANDOFF §5 诚信边界）。", ""]
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")

    payload = {
        "total": total, "reviewed": n, "invalid": len(invalid),
        "incomplete": incomplete,
        "skill_violations": skill_violations,
        "baseline_violation_count": len(base_violations),
    }
    if args.json:
        Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"reviewed {n}/{total}; invalid={len(invalid)}; skill_violations={len(skill_violations)}")
    print(f"summary -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
