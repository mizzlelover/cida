#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


def load(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def walk(left, right, prefix=""):
    changes = []
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(set(left) | set(right)):
            name = f"{prefix}.{key}" if prefix else str(key)
            if key not in left:
                changes.append((name, None, right[key]))
            elif key not in right:
                changes.append((name, left[key], None))
            else:
                changes.extend(walk(left[key], right[key], name))
    elif isinstance(left, list) and isinstance(right, list):
        if left != right:
            changes.append((prefix, left, right))
    elif left != right:
        changes.append((prefix, left, right))
    return changes


def main() -> int:
    if len(sys.argv) != 3:
        print("用法：python scripts/compare_versions.py OLD NEW")
        return 2
    left_path, right_path = map(Path, sys.argv[1:])
    changes = walk(load(left_path), load(right_path))
    print(f"比较：{left_path} -> {right_path}")
    print(f"差异路径：{len(changes)}")
    for name, left, right in changes[:100]:
        print(f"- {name}: {left!r} -> {right!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
