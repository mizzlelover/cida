#!/usr/bin/env python3
"""辞达 · 内部链接与引用完整性检查

检查仓库内 Markdown 文件中的相对链接是否指向存在的文件，
以及文本中引用的 source_id（src.*）是否已在 registry.yaml 登记。

用法：
    python scripts/check_links.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    import yaml
except ImportError:
    print("需要 PyYAML：pip install pyyaml")
    sys.exit(2)

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SRCID_RE = re.compile(r"src\.[a-z0-9][a-z0-9.\-]*")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def main() -> int:
    errors: list[str] = []

    registry = ROOT / "knowledge" / "sources" / "registry.yaml"
    registered: set[str] = set()
    if registry.exists():
        for e in yaml.safe_load(registry.read_text(encoding="utf-8")) or []:
            registered.add(e.get("source_id", ""))

    md_files = sorted(ROOT.rglob("*.md"))
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(ROOT)

        for target in LINK_RE.findall(text):
            if target.startswith(SKIP_PREFIXES) or target.startswith("{{"):
                continue
            target = target.split("#")[0].strip()
            if not target:
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{rel}: 死链接 -> {target}")

        for srcid in SRCID_RE.findall(text):
            if registered and srcid not in registered:
                errors.append(f"{rel}: 引用了未登记的 source_id -> {srcid}")

    print(f"检查 {len(md_files)} 个 Markdown 文件")
    if errors:
        print(f"\n发现 {len(errors)} 处问题：")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("链接与引用完整 ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
