#!/usr/bin/env python3
"""blind_keys.py · 盲评揭盲钥的统一读取（供 process_blind_review / audit_pair_preservation /
check_source_trace 共用）。

背景：揭盲映射原先只写在脚本里的"奇偶公式"（偶数 A=Skill、奇数 B=Skill）。实测该公式
**对 pair_012/014/016/018/020 是反的**（这五对的 A 侧是 Baseline，且 keys_ready10.md 早已
逐对写明）——凡按公式揭盲，都会把 Baseline 记成 Skill。故映射改以 keys 文件为唯一权威。

格式约定：`keys_*.md`（含 `pair_001_key.md`）中，每条目在同一个文本块内声明
`pair_NNN（...）：A = Skill/Baseline，B = ...`；一个块可含多对（如 `pair_076/077/078`）。
解析只认"块内出现 pair_NNN 且 A/B 各有赋值"的块，避免把正文里的描述性提及当成映射；
同一 pair 在两处给出冲突映射时**抛错**，不静默取舍。
"""
from __future__ import annotations

import re
from pathlib import Path

_BLOCK_SPLIT = re.compile(r"\n(?=#|\s*[-*]\s*pair_)")
_ID = re.compile(r"pair[_ ]?(\d{3})")
_A = re.compile(r"A\s*=\s*\*{0,2}(Skill|Baseline)")
_B = re.compile(r"B\s*=\s*\*{0,2}(Skill|Baseline)")
_DECLARED = re.compile(r"(keys[\w.\-]*\.md)")


def _parse(pairs_dir: Path) -> tuple[dict[int, str], dict[int, str]]:
    keys: dict[int, str] = {}
    sources: dict[int, str] = {}
    files = sorted(pairs_dir.glob("keys_*.md")) + sorted(pairs_dir.glob("pair_*_key.md"))
    for path in files:
        for block in _BLOCK_SPLIT.split(path.read_text(encoding="utf-8")):
            ids = {int(m.group(1)) for m in _ID.finditer(block)}
            if not ids:
                continue
            a, b = _A.search(block), _B.search(block)
            if not a or not b:
                continue
            if a.group(1) == b.group(1):
                raise ValueError(f"{path.name}: 同一块内 A/B 同为 {a.group(1)}（无法揭盲）")
            skill = "A" if a.group(1) == "Skill" else "B"
            for no in ids:
                if no in keys and keys[no] != skill:
                    raise ValueError(
                        f"{path.name}: pair_{no:03d} 的揭盲映射与 {sources[no]} 冲突"
                    )
                keys[no] = skill
                sources[no] = path.name
    return keys, sources


def load_keys(pairs_dir: Path) -> dict[int, str]:
    """{pair_no: 'A'|'B'}，值为 Skill 所在侧。"""
    return _parse(pairs_dir)[0]


def load_key_sources(pairs_dir: Path) -> dict[int, str]:
    """{pair_no: 记有该钥的文件名}，用于核对配对文件里的"请勿查看 keys（X）"指针。"""
    return _parse(pairs_dir)[1]


def declared_key_file(pair_text: str) -> str | None:
    """从配对正文的"评审前请勿查看……keys（X）"那一行取它自称的揭盲钥文件名。
    只认该提示行，避免把 provenance 等处对 keys 文件的顺带提及当成指针。"""
    for line in pair_text.splitlines():
        if "评审前" not in line:
            continue
        m = _DECLARED.search(line)
        if m:
            return m.group(1)
    return None