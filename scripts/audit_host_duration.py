#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
HOST_DIR = ROOT / "corpus" / "hosting"
OUT = ROOT / "corpus" / "annotations" / "host-duration-audit-20260910.md"


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(request, timeout=8).read().decode("utf-8", "ignore")


def parse_seconds(value: str | None) -> int | None:
    if not value or not re.fullmatch(r"\d{2}:\d{2}:\d{2}", value):
        return None
    hours, minutes, seconds = (int(part) for part in value.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def duration_for(url: str) -> tuple[int | None, str]:
    try:
        page = fetch(url)
    except Exception as exc:
        return None, f"page_error:{type(exc).__name__}"
    guid_match = re.search(r"guid(?:_Ad_VideoCode)?\s*=\s*[\"']([0-9a-f]{20,})", page, re.I)
    if not guid_match:
        return None, "page_read_no_guid"
    guid = guid_match.group(1)
    api = f"https://api.cntv.cn/video/videoinfoByGuid?guid={guid}&serviceId=tvcctv"
    try:
        raw = fetch(api)
        data = json.loads(raw)
    except Exception as exc:
        return None, f"api_error:{type(exc).__name__}"
    seconds = parse_seconds(data.get("len"))
    return seconds, "cntv_api" if seconds is not None else "api_no_duration"


def main() -> int:
    by_host: dict[str, list[dict]] = defaultdict(list)
    url_cache: dict[str, tuple[int | None, str]] = {}
    for path in sorted(HOST_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        host = data.get("host_target")
        url = data.get("source_url")
        if not host or not url:
            continue
        if url not in url_cache:
            url_cache[url] = duration_for(url) if "tv.cctv.com/" in url else (None, "not_official_video_api")
        seconds, evidence = url_cache[url]
        by_host[str(host)].append({"file": path.name, "url": url, "seconds": seconds, "evidence": evidence})

    lines = [
        "# 命名主持人时长审计（2026-09-10）",
        "",
        "本表只把官方 CCTV 页面通过 CNTV video-info API 返回的 `len` 计入累计时长；",
        "文字实录、第三方页面和无法返回时长的文章不估算为分钟。数量门槛与时长门槛分开记录。",
        "",
        "| 主持人 | 独立条目 | 有官方时长 | 可核验累计分钟 | 时长证据覆盖 |",
        "|---|---:|---:|---:|---:|",
    ]
    for host in sorted(by_host):
        items = by_host[host]
        measured = [item for item in items if item["seconds"] is not None]
        total = sum(item["seconds"] for item in measured)
        coverage = f"{len(measured)}/{len(items)}"
        lines.append(f"| {host} | {len(items)} | {len(measured)} | {total / 60:.1f} | {coverage} |")
    lines += ["", "## 逐条证据", "", "| 主持人 | 条目 | 时长 | 证据 |", "|---|---|---:|---|"]
    for host in sorted(by_host):
        for item in by_host[host]:
            duration = f"{item['seconds'] // 60}:{item['seconds'] % 60:02d}" if item["seconds"] is not None else "—"
            lines.append(f"| {host} | `{item['file']}` | {duration} | {item['evidence']} |")
    lines += [
        "",
        "## 使用边界",
        "",
        "- 该审计证明的是页面/API 的时长元数据，不证明主持人整段均为有效表达；仍需按人抽取连续片段、回看原视频并记录有效表达区间。",
        "- 未返回官方时长的样本保留数量证据，不按字符数或节目总时长换算，避免把估算冒充 60 分钟达标。",
        "- 运行：`python scripts/audit_host_duration.py`。网络不可用时，报告会保留错误类型而不填猜测值。",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    measured_total = sum(item["seconds"] or 0 for items in by_host.values() for item in items)
    print(f"hosts: {len(by_host)}")
    print(f"entries: {sum(len(items) for items in by_host.values())}")
    print(f"measured_minutes: {measured_total / 60:.1f}")
    print(f"report: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
