#!/usr/bin/env python3
"""辞达 · Schema 校验器

校验 knowledge/sources/registry.yaml 与 corpus/**/*.yaml 是否符合
schemas/ 中对应模板定义的必备字段与枚举取值。

用法：
    python scripts/validate_schemas.py

退出码：0 = 全部通过；1 = 存在违规。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    import yaml
except ImportError:
    print("需要 PyYAML：pip install pyyaml")
    sys.exit(2)


def template_keys(schema_path: Path) -> list[str]:
    """从 schema 模板中提取顶层字段名。"""
    data = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return []
    return list(data.keys())


def check_entry(entry: dict, required: list[str], label: str) -> list[str]:
    errors = []
    for key in required:
        if key not in entry:
            errors.append(f"{label}: 缺少字段 `{key}`")
    return errors


def main() -> int:
    errors: list[str] = []
    checked = 0

    # 1. 来源登记处
    registry = ROOT / "knowledge" / "sources" / "registry.yaml"
    source_keys = template_keys(ROOT / "schemas" / "source.yaml")
    if registry.exists() and source_keys:
        entries = yaml.safe_load(registry.read_text(encoding="utf-8")) or []
        seen_ids: set[str] = set()
        valid_domains = {
            "rhetoric", "register", "pragmatics", "discourse",
            "conversation", "hosting", "writing", "international",
        }
        valid_access = {"full_text", "key_chapters", "review_only", "metadata_only"}
        for e in entries:
            label = f"registry[{e.get('source_id', '?')}]"
            errors += check_entry(e, source_keys, label)
            sid = e.get("source_id")
            if sid in seen_ids:
                errors.append(f"{label}: source_id 重复")
            seen_ids.add(sid)
            if e.get("domain") not in valid_domains:
                errors.append(f"{label}: domain 非法 -> {e.get('domain')}")
            if e.get("access_status") not in valid_access:
                errors.append(f"{label}: access_status 非法 -> {e.get('access_status')}")
            checked += 1

    # 2. 语料条目（候选池与正式库分别校验，§112–113）
    corpus_keys = template_keys(ROOT / "schemas" / "corpus_item.yaml")
    candidate_keys = template_keys(ROOT / "schemas" / "candidate.yaml")
    valid_quality = {"official", "edited_official", "manual",
                     "auto_verified", "auto_unverified"}
    valid_prep = {"spontaneous", "semi_prepared", "prepared", "scripted", "edited"}
    valid_level = {"full", "substantial", "partial", "metadata_only"}
    for f in sorted((ROOT / "corpus").rglob("*.yaml")):
        if f.name == "index.yaml":  # 生成的索引文件不是语料条目
            continue
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            errors.append(f"{f}: 不是有效的 YAML 映射")
            continue
        label = str(f.relative_to(ROOT))
        is_candidate = "candidates" in f.parts
        errors += check_entry(data, candidate_keys if is_candidate else corpus_keys, label)
        if data.get("access_level") not in valid_level:
            errors.append(f"{label}: access_level 非法 -> {data.get('access_level')}")
        if is_candidate:
            continue  # 候选池条目不做正式库校验
        if data.get("transcript_quality") not in valid_quality:
            errors.append(f"{label}: transcript_quality 非法 -> {data.get('transcript_quality')}")
        if data.get("preparedness") not in valid_prep:
            errors.append(f"{label}: preparedness 非法 -> {data.get('preparedness')}")
        # 优秀语料 ≠ 全盘学习：三项必填
        for field in ("strengths", "weaknesses", "overuse_risks"):
            if not data.get(field):
                errors.append(f"{label}: `{field}` 不能为空（必须记录优缺点与滥用风险）")
        checked += 1

    print(f"校验 {checked} 条记录")
    if errors:
        print(f"\n发现 {len(errors)} 处违规：")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("全部通过 ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
