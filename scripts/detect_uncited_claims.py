#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    errors: list[str] = []
    checked = 0
    for path in sorted((ROOT / "knowledge" / "mechanisms").glob("*.md")):
        if path.name in {"README.md", "GRAPH.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        checked += 1
        aliases = {
            "definition": r"^## (definition|定义)\b",
            "mechanism": r"^## (mechanism|机制|操作规范|机制工具箱)\b",
            "boundary_conditions": r"^## (boundary_conditions|边界条件|边界)\b",
            "overuse_risk": r"^## (overuse_risk|overuse|滥用风险)\b",
            "repair_strategy": r"^## (repair_strategy|repair|修复策略)\b",
        }
        for section, pattern in aliases.items():
            if not re.search(pattern, text, re.MULTILINE):
                errors.append(f"{path.relative_to(ROOT)}: 缺少 {section} 段")
        if not re.search(r"^## sources\s*$", text, re.MULTILINE):
            errors.append(f"{path.relative_to(ROOT)}: 重要知识节点没有来源段")
    print(f"知识节点证据结构检查：{checked} 个节点")
    if errors:
        print("\n".join(f"  ✗ {e}" for e in errors))
        return 1
    print("知识节点证据结构通过 ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
