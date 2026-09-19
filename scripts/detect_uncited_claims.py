#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    errors: list[str] = []
    checked = 0
    allowed_conf = {"contextual", "validated"}
    for path in sorted((ROOT / "knowledge" / "mechanisms").glob("*.md")):
        if path.name in {"README.md", "GRAPH.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        checked += 1
        rel = path.relative_to(ROOT)
        aliases = {
            "definition": r"^## (definition|定义)\b",
            "mechanism": r"^## (mechanism|机制|操作规范|机制工具箱)\b",
            "boundary_conditions": r"^## (boundary_conditions|边界条件|边界)\b",
            "overuse_risk": r"^## (overuse_risk|overuse|滥用风险)\b",
            "repair_strategy": r"^## (repair_strategy|repair|修复策略)\b",
        }
        for section, pattern in aliases.items():
            if not re.search(pattern, text, re.MULTILINE):
                errors.append(f"{rel}: 缺少 {section} 段")
        if not re.search(r"^## sources\s*$", text, re.MULTILINE):
            errors.append(f"{rel}: 重要知识节点没有来源段")

        # §121 状态一致性（2026-09-16 固化；此前靠人工逐文件核对才发现多处不一致）
        # 规则：confidence 字段必须存在且取值受限；且 `validated` ⇔ 存在「跨来源验证（§121）」小节。
        m = re.search(r"^confidence:\s*(\S+)\s*$", text, re.MULTILINE)
        if not m:
            errors.append(f"{rel}: 缺少 confidence 字段")
            continue
        conf = m.group(1).strip()
        if conf not in allowed_conf:
            errors.append(f"{rel}: confidence 取值非法（{conf}；允许 {sorted(allowed_conf)}）")
        has_121 = re.search(r"^## 跨来源验证（§121）\s*$", text, re.MULTILINE) is not None
        if conf == "validated" and not has_121:
            errors.append(f"{rel}: 标为 validated 却缺少「跨来源验证（§121）」小节（状态先于证据）")
        if conf != "validated" and has_121:
            errors.append(f"{rel}: 存在「跨来源验证（§121）」小节但 confidence 仍为 {conf}（字段漏改）")

        # 重复小节检测（2026-09-16 固化）：并发写入曾两次造成同一小节被写两遍，
        # 使同一来源块/验证小节重复出现。此处按标题去重检查。
        headings = [h.strip() for h in re.findall(r"^## .*$", text, re.MULTILINE)]
        dups = sorted({h for h in headings if headings.count(h) > 1})
        if dups:
            errors.append(f"{rel}: 存在重复小节 {dups}（疑似并发写入或复制粘贴）")
    print(f"知识节点证据结构检查：{checked} 个节点")
    if errors:
        print("\n".join(f"  ✗ {e}" for e in errors))
        return 1
    print("知识节点证据结构通过 ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
