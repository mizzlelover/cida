#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    seen: dict[str, Path] = {}
    errors: list[str] = []
    for path in sorted((ROOT / "knowledge" / "mechanisms").glob("*.md")):
        if path.name in {"README.md", "GRAPH.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^id:\s*(\S+)", text, re.MULTILINE)
        if not match:
            errors.append(f"{path.relative_to(ROOT)}: 缺少 id")
            continue
        node_id = match.group(1)
        if node_id in seen:
            errors.append(f"重复机制 id: {node_id} -> {seen[node_id].relative_to(ROOT)}, {path.relative_to(ROOT)}")
        seen[node_id] = path
    if errors:
        print("\n".join(errors))
        return 1
    print(f"机制节点唯一性通过：{len(seen)} 个节点")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
