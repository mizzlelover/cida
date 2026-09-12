#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(command):
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    tail = result.stdout.strip().splitlines()[-4:]
    if result.stderr.strip():
        tail.extend(result.stderr.strip().splitlines()[-2:])
    print(f"$ {' '.join(command)}")
    print("\n".join(tail))
    return result.returncode


def main() -> int:
    commands = [
        [sys.executable, "scripts/validate_schemas.py"],
        [sys.executable, "scripts/audit_research.py"],
        [sys.executable, "scripts/detect_duplicate_nodes.py"],
        [sys.executable, "scripts/detect_uncited_claims.py"],
        [sys.executable, "scripts/check_source_trace.py"],
        [sys.executable, "scripts/build_mechanism_graph.py"],
        [sys.executable, "scripts/run_evals.py"],
        [sys.executable, "scripts/run_benchmark_quality.py"],
        [sys.executable, "scripts/calibrate_style_profile.py"],
        [sys.executable, "scripts/build_human_review_queue.py"],
        [sys.executable, "scripts/build_corpus_index.py"],
        [sys.executable, "scripts/check_links.py"],
    ]
    failures = []
    outcomes = []
    for command in commands:
        code = run(command)
        outcomes.append((command, code))
        if code:
            failures.append(" ".join(command))
    if not failures:
        report_command = [sys.executable, "scripts/generate_report.py"]
        code = run(report_command)
        outcomes.append((report_command, code))
        if code:
            failures.append(" ".join(report_command))
    history = ROOT / "evals" / "regression" / "history" / f"{date.today():%Y%m%d}.md"
    history.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Regression Record · {date.today():%Y-%m-%d}",
        "",
        "统一回归由 `scripts/run_regression.py` 执行；质量实跑与盲评队列的证据边界保留在各自报告。",
        "",
        "| 检查 | 结果 |",
        "|---|---|",
    ]
    for command, code in outcomes:
        label = " ".join(command)
        lines.append(f"| `{label}` | {'通过' if code == 0 else '失败'} |")
    lines += [
        "",
        f"结论：{'PASS' if not failures else 'FAIL'}。",
        "",
        "本记录只反映自动检查结果；150 案中 corpus_reference 的外部盲评、第三方转写听校与机制 VALIDATED 升级仍按各自台账执行。",
    ]
    history.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"regression: {'PASS' if not failures else 'FAIL'}")
    if failures:
        print("失败命令：")
        print("\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
