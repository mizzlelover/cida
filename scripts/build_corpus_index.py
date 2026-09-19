#!/usr/bin/env python3
"""辞达 · 语料索引构建器

扫描 corpus/ 下所有 YAML 条目，生成 corpus/INDEX.md（人类可读）
与 corpus/index.yaml（机器可读），含分类统计与转录质量分布。

用法：
    python scripts/build_corpus_index.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    import yaml
except ImportError:
    print("需要 PyYAML：pip install pyyaml")
    sys.exit(2)


def main() -> int:
    items = []
    for f in sorted((ROOT / "corpus").rglob("*.yaml")):
        if f.name in {"index.yaml"}:
            continue
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data["_file"] = str(f.relative_to(ROOT))
            data["_category"] = f.parent.name
            items.append(data)

    by_cat = Counter(i["_category"] for i in items)
    by_quality = Counter(i.get("transcript_quality", "?") for i in items)
    by_prep = Counter(i.get("preparedness", "?") for i in items)

    lines = [
        "# Corpus Index · 语料索引",
        "",
        f"共 {len(items)} 条。由 `scripts/build_corpus_index.py` 自动生成，请勿手改。",
        "",
        "## 分类统计",
        "",
        "| 类别 | 数量 |", "|---|---|",
        *[f"| {cat} | {n} |" for cat, n in sorted(by_cat.items())],
        "",
        "## 转录质量分布",
        "",
        "| transcript_quality | 数量 |", "|---|---|",
        *[f"| {k} | {n} |" for k, n in sorted(by_quality.items())],
        "",
        "## 准备度分布",
        "",
        "| preparedness | 数量 |", "|---|---|",
        *[f"| {k} | {n} |" for k, n in sorted(by_prep.items())],
        "",
        "## 明细",
        "",
        "| id | 作者/讲者 | 来源 | 媒介 | 准备度 | 转录质量 |",
        "|---|---|---|---|---|---|",
        *[
            "| {} | {} | {} | {} | {} | {} |".format(
                i.get("id", "?"), i.get("speaker_or_author", "?"),
                i.get("program_or_site", "?"), i.get("medium", "?"),
                i.get("preparedness", "?"), i.get("transcript_quality", "?"),
            )
            for i in items
        ],
        "",
    ]
    (ROOT / "corpus" / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")

    index_data = {
        "total": len(items),
        "by_category": dict(by_cat),
        "by_transcript_quality": dict(by_quality),
        "by_preparedness": dict(by_prep),
        "files": [i["_file"] for i in items],
    }
    (ROOT / "corpus" / "index.yaml").write_text(
        yaml.safe_dump(index_data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"索引完成：{len(items)} 条语料 -> corpus/INDEX.md, corpus/index.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
