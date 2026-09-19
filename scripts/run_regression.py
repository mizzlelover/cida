#!/usr/bin/env python3
"""统一回归入口。

两种运行模式：
- **开发仓模式**（`corpus/` · `evals/` · `knowledge/sources/` 齐备）：跑全部检查并写回归记录；
- **发布包模式**（研究侧档案未随包分发）：只跑可独立执行的检查，明确打印跳过项。

研究侧档案随开发仓分发、不在发布包内（见 README「发布包不含研究侧档案」）。
"""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 研究侧检查：依赖语料 `corpus/`、评测档案 `evals/` 或来源登记处 `knowledge/sources/`。
RESEARCH_SCRIPTS = [
    "validate_schemas",
    "audit_research",
    "check_source_trace",
    "run_evals",
    "run_benchmark_quality",
    "calibrate_style_profile",
    "build_human_review_queue",
    "build_corpus_index",
]
# 发布包内可独立执行的检查：只依赖 knowledge/、schemas/ 与 Markdown 链接。
STANDALONE_SCRIPTS = [
    "detect_duplicate_nodes",
    "detect_uncited_claims",
    "build_mechanism_graph",
    "check_links",
]
# 依赖研究侧档案、仅开发仓执行的收尾报告。
REPORT_SCRIPT = "generate_report"


def research_archive_present() -> bool:
    return all((ROOT / part).is_dir() for part in ("corpus", "evals", "knowledge/sources"))


def run(script: str):
    command = [sys.executable, f"scripts/{script}.py"]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    tail = result.stdout.strip().splitlines()[-4:]
    if result.stderr.strip():
        tail.extend(result.stderr.strip().splitlines()[-2:])
    print(f"$ {' '.join(command)}")
    print("\n".join(tail))
    return command, result.returncode


def main() -> int:
    full = research_archive_present()
    scripts = RESEARCH_SCRIPTS + STANDALONE_SCRIPTS if full else list(STANDALONE_SCRIPTS)

    if not full:
        print("检测到研究侧档案缺席（corpus/ · evals/ · knowledge/sources/ 未随包分发）。")
        print("本次只运行发布包内可独立执行的检查；下列研究侧检查已跳过：")
        print("  " + "、".join(f"scripts/{s}.py" for s in RESEARCH_SCRIPTS))
        print()

    failures: list[str] = []
    outcomes: list[tuple[str, int]] = []
    for script in scripts:
        command, code = run(script)
        outcomes.append((" ".join(command), code))
        if code:
            failures.append(" ".join(command))
    if full and not failures:
        command, code = run(REPORT_SCRIPT)
        outcomes.append((" ".join(command), code))
        if code:
            failures.append(" ".join(command))

    if full:
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
        for label, code in outcomes:
            lines.append(f"| `{label}` | {'通过' if code == 0 else '失败'} |")
        lines += [
            "",
            f"结论：{'PASS' if not failures else 'FAIL'}。",
            "",
            "本记录只反映自动检查结果；benchmark inventory 中 corpus_reference 案的外部盲评、第三方转写听校与机制 VALIDATED 升级仍按各自台账执行。",
        ]
        history.write_text("\n".join(lines) + "\n", encoding="utf-8")

    suffix = "" if full else f"（发布包模式：{len(RESEARCH_SCRIPTS)} 项研究侧检查已跳过）"
    print(f"regression: {'PASS' if not failures else 'FAIL'}{suffix}")
    if failures:
        print("失败命令：")
        print("\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
