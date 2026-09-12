#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    counts = Counter()
    states = Counter()
    for path in sorted((ROOT / "corpus").rglob("*.yaml")):
        if path.name == "index.yaml":
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        counts[path.parent.name] += 1
        states[(path.parent.name, data.get("state", "?"))] += 1
    registry = yaml.safe_load((ROOT / "knowledge" / "sources" / "registry.yaml").read_text(encoding="utf-8")) or []
    depth = Counter(x.get("access_status", "?") for x in registry)
    languages = Counter(x.get("language", "?") for x in registry)
    case_count = len(list((ROOT / "evals" / "benchmark" / "cases").glob("*_case.yaml")))
    quality_runs = len(list((ROOT / "evals" / "benchmark" / "results" / "runs").glob("*_quality.md")))
    calibration_runs = len(list((ROOT / "evals" / "style_calibration").glob("profile_iteration_*.yaml")))
    queue_path = ROOT / "evals" / "human_review" / "review_queue_20260910.csv"
    queue_states = Counter()
    if queue_path.exists():
        with queue_path.open(encoding="utf-8", newline="") as handle:
            queue_states.update(row.get("input_status", "?") for row in csv.DictReader(handle))
    graph = yaml.safe_load((ROOT / "knowledge" / "mechanisms" / "GRAPH.yaml").read_text(encoding="utf-8")) if (ROOT / "knowledge" / "mechanisms" / "GRAPH.yaml").exists() else {}
    lines = ["# PROJECT_STATUS · 辞达工程状态快照", "", "由 `scripts/generate_report.py` 生成；它是当前状态快照，不替代人工研究结论。", "", "接力登记见 [HANDOFF.md](HANDOFF.md)；下一位 agent 应先复核该文件，再继续开放项。", "", "## 规模", "", "| 项目 | 数量 |", "|---|---:|", f"| 来源登记 | {len(registry)} |", f"| Benchmark inventory | {case_count} |", f"| 机制节点 | {len(graph.get('nodes', []))} |"]
    lines.extend([f"| Benchmark quality reports | {quality_runs} |", f"| Style calibration iterations | {calibration_runs} |", f"| Human review queue | {sum(queue_states.values())} |"])
    lines.extend(f"| Human review · {key} | {value} |" for key, value in sorted(queue_states.items()))
    lines.extend(f"| corpus/{key} | {value} |" for key, value in sorted(counts.items()))
    lines.extend(["", "## 来源证据深度", "", "| access_status | count |", "|---|---:|"])
    lines.extend(f"| {key} | {value} |" for key, value in sorted(depth.items()))
    lines.extend(["", "## 来源语言分布", "", "目标：中文原生优先，国际补强约占三成。", "", "| language | count |", "|---|---:|"])
    lines.extend(f"| {key} | {value} |" for key, value in sorted(languages.items()))
    lines.extend(["", "## 语料状态", "", "| category | state | count |", "|---|---|---:|"])
    lines.extend(f"| {category} | {state} | {count} |" for (category, state), count in sorted(states.items()))
    lines.extend(["", "## 证据边界", "", "- 数量、索引和 schema 通过不等于逐篇 VALIDATED。", "- 第三方自动转写、政民互动和项目自有对照文本继续按条目标注边界。", "- 机制节点的强结论必须回到来源追踪、跨来源比较和人工抽查。"])
    out = ROOT / "PROJECT_STATUS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"状态报告已生成：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
