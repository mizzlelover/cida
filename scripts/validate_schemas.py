#!/usr/bin/env python3
"""辞达 · Schema 校验器

校验 knowledge/sources/registry.yaml 与 corpus/**/*.yaml 是否符合
schemas/ 中对应模板定义的必备字段与枚举取值。

用法：
    python scripts/validate_schemas.py

退出码：0 = 全部通过；1 = 存在违规。
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
    # YAML 解析前置守卫（2026-09-17 第四十四批新增）：语料条目里的**块列表项若以 YAML 保留字符
    # （`*`／`&`／`!`）起首**，`yaml.safe_load` 会直接抛 ScannerError——但**旧实现的失败形态是一段栈回溯**，
    # 只说明"scanning an alias"，**既不指明可修的写法，也不提示同类行**。该缺陷已**连续两批**出现
    # （第四十二批残留 1 条、第四十四批新写 3 条共 10 行），故此处把失败改为**可操作提示**：
    # 报出文件、解析器首行信息、**行首保留字符的具体行号**，并给出改法。
    reserved_init = re.compile(r"^\s*-\s+[*&!]")
    yaml_checked = 0
    yaml_broken = 0
    for f in sorted((ROOT / "corpus").rglob("*.yaml")):
        if f.name == "index.yaml":  # 生成的索引文件不是语料条目
            continue
        text = f.read_text(encoding="utf-8")
        yaml_checked += 1
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            yaml_broken += 1
            label = str(f.relative_to(ROOT))
            first = str(exc).splitlines()[0] if str(exc) else "YAML 解析失败"
            hits = [i for i, line in enumerate(text.splitlines(), 1) if reserved_init.match(line)]
            hint = ""
            if hits:
                preview = text.splitlines()[hits[0] - 1].strip()[:60]
                hint = (f" -> 第 {hits} 行以 YAML 保留字符起首（`*`／`&`／`!`）；"
                        f"如 `{preview}`——**加粗只能写在值内部，不能写在行首**")
            errors.append(f"{label}: YAML 解析失败（{first}）{hint}")
            continue
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
    print(f"YAML 解析：{yaml_checked} 条语料文件受检，解析失败 {yaml_broken} 条"
          f"（失败时给出**行首保留字符**行号与改法；见本脚本 2026-09-17 第四十四批说明）")
    if errors:
        print(f"\n发现 {len(errors)} 处违规：")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("全部通过 ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
