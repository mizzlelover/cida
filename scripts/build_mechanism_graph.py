#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MECHANISMS = ROOT / "knowledge" / "mechanisms"
ANTI_PATTERNS = ROOT / "knowledge" / "anti_patterns"
# 根文档：机制节点可以合法地关联到它们（不带 `knowledge/` 前缀，故单独登记）
ROOT_DOCS = {"STYLE_SYSTEM.md", "EVIDENCE.md"}

# 关联类型：跨命名空间时用不同边类型，避免把"反模式"与"机制"混为一谈
EDGE_MECHANISM = "RELATED_TO"
EDGE_ANTI_PATTERN = "OVERUSE_CAUSES"
EDGE_ROOT_DOC = "GOVERNED_BY"


def parse_node(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    head = text.split("## ", 1)[0]
    values = {}
    for key in ("id", "name", "function"):
        match = re.search(rf"^\s*{key}:\s*(.+?)\s*$", head, re.MULTILINE)
        if match:
            values[key] = match.group(1).strip().strip('"')
    # related_nodes：**取该小节内全部 `*.md` 目标**。
    # 2026-09-16 修正：旧版正则 `## related_nodes\s+`([^`]+)`` 只捕获**第一段反引号**，
    # 于是"`a.md`（说明）、`b.md`、`c.md`"这类写法只生成 1 条边，其余**静默丢弃**
    # （实测作者写下 129 条关联，旧脚本只生成 106 条）。
    related: list[str] = []
    match = re.search(r"## related_nodes\s*\n+(.+?)\n## ", text, re.MULTILINE | re.DOTALL)
    if match:
        for name in re.findall(r"([A-Za-z_]+\.md)", match.group(1)):
            if name not in related:
                related.append(name)
    sources = []
    match = re.search(r"## sources\s+(.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    if match:
        sources = [x.strip(" -\n") for x in match.group(1).splitlines() if x.strip(" -\n")]
    values.update({"file": str(path.relative_to(ROOT)), "related": related, "sources": sources})
    return values


def main() -> int:
    nodes = [parse_node(p) for p in sorted(MECHANISMS.glob("*.md")) if p.name not in {"README.md", "GRAPH.md"}]
    by_file = {Path(n["file"]).name: n.get("id", "") for n in nodes}
    anti_files = {p.name for p in ANTI_PATTERNS.glob("*.md") if p.name != "README.md"}
    edges = []
    unresolved: list[dict] = []
    for node in nodes:
        for relation in node.get("related", []):
            name = Path(relation).name
            if name in by_file:
                edges.append({"source": node.get("id", ""), "target": by_file[name], "type": EDGE_MECHANISM})
            elif name in anti_files:
                edges.append({"source": node.get("id", ""), "target": name, "type": EDGE_ANTI_PATTERN})
            elif name in ROOT_DOCS:
                edges.append({"source": node.get("id", ""), "target": name, "type": EDGE_ROOT_DOC})
            else:
                # 悬空关联：**登记进图，不静默丢弃**（并由 check_source_trace.py 判错）
                unresolved.append({"source": node.get("id", ""), "target": relation})
    graph = {
        "version": "0.2",
        "generated_by": "scripts/build_mechanism_graph.py",
        "nodes": nodes,
        "edges": edges,
        "unresolved_references": unresolved,
    }
    (MECHANISMS / "GRAPH.yaml").write_text(yaml.safe_dump(graph, allow_unicode=True, sort_keys=False), encoding="utf-8")
    lines = [
        "# Mechanism Graph · 话语机制图谱",
        "",
        "> 本文件是**任务检索入口**（人读）：按 `function` 选机制，按 `file` 取节点正文；",
        "> 节点正文含证据、边界、滥用风险与修复动作。",
        "> 机器可读版 `GRAPH.yaml` 同目录（由本脚本写出的维护侧生成物）。",
        "",
        f"节点：{len(nodes)}；关系：{len(edges)}"
        f"（机制 {sum(1 for e in edges if e['type'] == EDGE_MECHANISM)}"
        f" / 反模式 {sum(1 for e in edges if e['type'] == EDGE_ANTI_PATTERN)}"
        f" / 根文档 {sum(1 for e in edges if e['type'] == EDGE_ROOT_DOC)}）；"
        f"悬空关联：{len(unresolved)}。",
        "",
        "## 节点",
        "",
        "| id | name | function | file |",
        "|---|---|---|---|",
    ]
    lines.extend(f"| {n.get('id','')} | {n.get('name','')} | {n.get('function','')} | `{n['file']}` |" for n in nodes)
    lines.extend(["", "## 关系", "", "| source | type | target |", "|---|---|---|"])
    lines.extend(f"| {e['source']} | {e['type']} | {e['target']} |" for e in edges)
    (MECHANISMS / "GRAPH.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"机制图谱完成：{len(nodes)} 节点，{len(edges)} 条关系"
        f"（机制 {sum(1 for e in edges if e['type'] == EDGE_MECHANISM)}"
        f" / 反模式 {sum(1 for e in edges if e['type'] == EDGE_ANTI_PATTERN)}"
        f" / 根文档 {sum(1 for e in edges if e['type'] == EDGE_ROOT_DOC)}），悬空关联 {len(unresolved)}"
    )
    for item in unresolved:
        print(f"  悬空关联：{item['source']} -> {item['target']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
