#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CASE_DIR = ROOT / "evals" / "benchmark" / "cases"
OUT = ROOT / "evals" / "human_review" / "review_queue_20260910.csv"


def main() -> int:
    rows = []
    for path in sorted(CASE_DIR.glob("*_case.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        case_id = str(data.get("case_id", ""))
        suffix = case_id.rsplit(".", 1)[-1]
        case_file = data.get("input_file")
        if case_file:
            # 正例层（如 official_public_document）以 input_file 指向可合法纳入的正文；
            # 文件实际存在且非空才计为 ready，避免"登记即就绪"的虚报。
            input_path = ROOT / str(case_file)
            ready = input_path.exists() and bool(input_path.read_text(encoding="utf-8").strip())
            a = str(case_file) if ready else ""
        else:
            ready = data.get("source_type") == "project_authored_control"
            a = f"evals/benchmark/cases/high_template_{suffix}_input.txt"
        if ready:
            b = "generated baseline in evals/benchmark/results/runs/"
            c = f"evals/benchmark/results/runs/{case_id.replace('.', '_')}_quality.md"
            input_status = "ready"
        else:
            a = b = c = ""
            input_status = "await_source_text"
        rows.append(
            {
                "case_id": case_id,
                "category": data.get("category", ""),
                "input_status": input_status,
                "source_ref": data.get("source_ref", ""),
                "input_locator": data.get("input_locator", ""),
                "version_a": a,
                "version_b": b,
                "version_c": c,
                "pairwise_easier_to_read": "",
                "pairwise_more_natural": "",
                "pairwise_more_thoughtful": "",
                "pairwise_more_like_conversation": "",
                "pairwise_continue_reading": "",
                "ordinary_reader_score_1_to_5": "",
                "professional_reader_score_1_to_5": "",
                "content_creator_score_1_to_5": "",
                "editor_score_1_to_5": "",
                "meaning": "",
                "argument": "",
                "author_position": "",
                "evidence": "",
                "nuance": "",
                "personal_voice": "",
                "reviewer_id": "",
                "review_date": "",
                "notes": "",
            }
        )
    fieldnames = list(rows[0]) if rows else []
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"review queue: {len(rows)}")
    print(f"ready: {sum(row['input_status'] == 'ready' for row in rows)}")
    print(f"await_source_text: {sum(row['input_status'] == 'await_source_text' for row in rows)}")
    print(f"output: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
