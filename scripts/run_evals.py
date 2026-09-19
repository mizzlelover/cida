#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STATE_ORDER = ["PLANNED", "FOUND", "ACQUIRED", "READ", "ANNOTATED", "VALIDATED", "DISTILLED"]
REQUIRED = ["case_id", "category", "task", "source_type", "source_ref", "input_locator", "expected_properties", "common_failures", "evaluation_status", "license_boundary"]


def state_rank(value: str) -> int:
    return STATE_ORDER.index(value) if value in STATE_ORDER else -1


def main() -> int:
    cases = []
    errors = []
    seen = set()
    for path in sorted((ROOT / "evals" / "benchmark" / "cases").glob("*_case.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: YAML 解析失败 {exc}")
            continue
        cases.append(data)
        label = str(path.relative_to(ROOT))
        missing = [key for key in REQUIRED if key not in data]
        if missing:
            errors.append(f"{label}: 缺少 {', '.join(missing)}")
        case_id = data.get("case_id")
        if case_id in seen:
            errors.append(f"{label}: case_id 重复 {case_id}")
        seen.add(case_id)
        ref = ROOT / str(data.get("source_ref", ""))
        if not ref.exists():
            errors.append(f"{label}: source_ref 不存在 {data.get('source_ref')}")
            continue
        if data.get("source_type") == "corpus_reference":
            try:
                source = yaml.safe_load(ref.read_text(encoding="utf-8")) or {}
            except Exception as exc:
                errors.append(f"{label}: 来源 YAML 无法读取 {exc}")
                continue
            if state_rank(str(source.get("state", ""))) < state_rank("READ"):
                errors.append(f"{label}: 来源尚未 READ")
            if not source.get("source_url") or not source.get("content_obtained"):
                errors.append(f"{label}: 来源缺少 source_url 或 content_obtained")
            if not source.get("selected_segments"):
                errors.append(f"{label}: 来源缺少 selected_segments")
        elif data.get("source_type") == "project_authored_control":
            if ref.suffix != ".txt":
                errors.append(f"{label}: 自有控制文本必须是 .txt")
            if not ref.read_text(encoding="utf-8").strip():
                errors.append(f"{label}: 自有控制文本为空")
        elif data.get("source_type") == "official_public_document":
            # 官方文件层：法律、法规，以及国家机关具有立法/行政/司法性质的文件
            # （《著作权法》第五条第一项），可合法纳入全文作为评测输入。
            # 使用依据必须逐案写明在 license_boundary，不接受空泛声明。
            if ref.suffix != ".txt":
                errors.append(f"{label}: 官方文件正文必须是 .txt")
            elif not ref.read_text(encoding="utf-8").strip():
                errors.append(f"{label}: 官方文件正文为空")
            if not str(data.get("license_boundary", "")).strip():
                errors.append(f"{label}: 官方文件层必须写明 license_boundary（使用依据与来源）")
        else:
            errors.append(f"{label}: source_type 不支持 {data.get('source_type')}")
        if not isinstance(data.get("expected_properties"), list) or len(data["expected_properties"]) < 2:
            errors.append(f"{label}: expected_properties 少于 2 项")
        if not isinstance(data.get("common_failures"), list) or not data["common_failures"]:
            errors.append(f"{label}: common_failures 为空")
    counts = Counter(data.get("category", "?") for data in cases)
    lines = ["# Benchmark Inventory Run · 基准库登记验收", "", f"本次检查 {len(cases)} 个 YAML benchmark case。", "", "## 分类", "", "| category | count |", "|---|---:|"]
    lines.extend(f"| {key} | {value} |" for key, value in sorted(counts.items()))
    lines.extend(["", "## 证据模式", "", "- `corpus_reference`：检查来源条目已达到 READ、具有来源 URL、取得方式和分析定位。", "- `project_authored_control`：检查项目自有控制文本可读取，并保留其非外部真实稿的边界。", "- `official_public_document`：检查官方文件正文（法律、法规等《著作权法》第五条第一项所列文件）可读取，并逐案写明使用依据；该层是为解除第三方授权阻塞而设的可合法纳入全文的正例层。", "- 本脚本验收的是 benchmark inventory 与证据链，不把登记通过冒充人工盲评或模型质量评测。", "", f"结果：{'通过' if not errors and len(cases) >= 150 else '未通过'}。"])
    if errors:
        lines.extend(["", "## 问题", "", *[f"- {error}" for error in errors]])
    out = ROOT / "evals" / "benchmark" / "results" / "benchmark_inventory_20260910.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"benchmark cases: {len(cases)}")
    print(f"categories: {dict(counts)}")
    print(f"report: {out.relative_to(ROOT)}")
    if errors or len(cases) < 150:
        for error in errors:
            print(f"  ✗ {error}")
        if len(cases) < 150:
            print(f"  ✗ benchmark inventory 数量 {len(cases)} 低于基线 150")
        return 1
    print(f"benchmark inventory {len(cases)} 案通过（基线 150，允许按正例层扩充）✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
