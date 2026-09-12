#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MECHANISMS = ROOT / "knowledge" / "mechanisms"


def parse_node(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    head = text.split("## ", 1)[0]
    values = {}
    for key in ("id", "name", "function"):
        match = re.search(rf"^\s*{key}:\s*(.+?)\s*$", head, re.MULTILINE)
        if match:
            values[key] = match.group(1).strip().strip('"')
    related = []
    match = re.search(r"## related_nodes\s+`([^`]+)`", text, re.MULTILINE)
    if match:
        related = [x.strip() for x in match.group(1).split(",") if x.strip()]
    sources = []
    match = re.search(r"## sources\s+(.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    if match:
        sources = [x.strip(" -\n") for x in match.group(1).splitlines() if x.strip(" -\n")]
    values.update({"file": str(path.relative_to(ROOT)), "related": related, "sources": sources})
    return values


def main() -> int:
    nodes = [parse_node(p) for p in sorted(MECHANISMS.glob("*.md")) if p.name not in {"README.md", "GRAPH.md"}]
    by_file = {Path(n["file"]).name: n.get("id", "") for n in nodes}
    edges = []
    for node in nodes:
        for relation in node.get("related", []):
            target = by_file.get(Path(relation).name)
            if target:
                edges.append({"source": node.get("id", ""), "target": target, "type": "RELATED_TO"})
    graph = {"version": "0.1", "generated_by": "scripts/build_mechanism_graph.py", "nodes": nodes, "edges": edges}
    (MECHANISMS / "GRAPH.yaml").write_text(yaml.safe_dump(graph, allow_unicode=True, sort_keys=False), encoding="utf-8")
    lines = ["# Mechanism Graph · 话语机制图谱", "", f"节点：{len(nodes)}；关系：{len(edges)}。", "", "## 节点", "", "| id | name | function | file |", "|---|---|---|---|"]
    lines.extend(f"| {n.get('id','')} | {n.get('name','')} | {n.get('function','')} | `{n['file']}` |" for n in nodes)
    lines.extend(["", "## 关系", "", "| source | type | target |", "|---|---|---|"])
    lines.extend(f"| {e['source']} | {e['type']} | {e['target']} |" for e in edges)
    (MECHANISMS / "GRAPH.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"机制图谱完成：{len(nodes)} 节点，{len(edges)} 条关系")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
