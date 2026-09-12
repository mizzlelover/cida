#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    registry = yaml.safe_load((ROOT / "knowledge" / "sources" / "registry.yaml").read_text(encoding="utf-8")) or []
    source_ids = {str(x.get("source_id")) for x in registry}
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0
    for path in sorted((ROOT / "knowledge" / "mechanisms").glob("*.md")):
        if path.name in {"README.md", "GRAPH.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "## sources" not in text:
            errors.append(f"{path.relative_to(ROOT)}: 缺少 sources 段")
            continue
        checked += 1
        source_block = text.split("## sources", 1)[1].split("## ", 1)[0]
        ids = re.findall(r"\bsrc\.[A-Za-z0-9_.-]+", source_block)
        for source_id in ids:
            if source_id not in source_ids:
                errors.append(f"{path.relative_to(ROOT)}: registry 不存在 {source_id}")
        refs = re.findall(r"`([^`]+)`", source_block)
        for ref in refs:
            if ref.startswith("corpus/"):
                target = ROOT / ref
                if not target.exists():
                    warnings.append(f"{path.relative_to(ROOT)}: corpus 引用不存在 {ref}")
    print(f"来源追踪检查：{checked} 个机制节点")
    for warning in warnings:
        print(f"  ℹ {warning}")
    if errors:
        for error in errors:
            print(f"  ✗ {error}")
        return 1
    print("来源追踪通过 ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
