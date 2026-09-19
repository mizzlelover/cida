#!/usr/bin/env python3
"""辞达 · 阮一峰 ESSAY（非周刊文章）语料采集器

合规声明：同 acquire_blog_corpus.py（该站 robots 信号 search=yes,
use=reference, ai-train=no；仅存元数据+特征+≤80 字摘录，不存全文）。

策略：按月存档页 /blog/YYYY/MM/ 收集非 weekly 文章链接，均匀抽样后抓取。
日期取 URL 的 YYYY/MM（月份级精度）。

用法：
    python scripts/acquire_essays_corpus.py --from 2018-01 --to 2026-09 --limit 65
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from acquire_blog_corpus import fetch, parse_article  # noqa: E402

import yaml  # noqa: E402


def month_range(start: str, end: str) -> list[str]:
    y, m = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    out = []
    while (y, m) <= (ey, em):
        out.append(f"{y}/{m:02d}")
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2018-01")
    ap.add_argument("--end", default="2026-09")
    ap.add_argument("--limit", type=int, default=65)
    ap.add_argument("--delay", type=float, default=0.5)
    args = ap.parse_args()

    out_dir = ROOT / "corpus" / "blogs"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. 收集全部 essay 链接（带缓存，超时可续跑）
    cache = ROOT / "corpus" / "metadata" / "essay_links.json"
    links: list[tuple[str, str]] = []
    done_months: set[str] = set()
    if cache.exists():
        saved = json.loads(cache.read_text(encoding="utf-8"))
        links = [tuple(x) for x in saved["links"]]
        done_months = set(saved["done_months"])
        print(f"续跑：缓存已有 {len(links)} 篇链接 / {len(done_months)} 个月")
    months = [m for m in month_range(args.start, args.end) if m not in done_months]
    for i, ym in enumerate(months):
        u = f"https://www.ruanyifeng.com/blog/{ym}/"
        html = fetch(u, retries=1)
        if not html:
            print(f"  ✗ 月存档 {ym} 未取得")
            continue
        for m in re.findall(r'href="(https://www\.ruanyifeng\.com/blog/\d{4}/\d{2}/([^"/]+)\.html)"', html):
            url, slug = m
            if slug.startswith("weekly-issue-"):
                continue
            pair = (ym.replace("/", "-"), url)
            if pair not in links:
                links.append(pair)
        done_months.add(ym)
        cache.write_text(json.dumps({"links": links, "done_months": sorted(done_months)},
                                    ensure_ascii=False), encoding="utf-8")
        if i % 12 == 0:
            print(f"  …已扫 {i+1}/{len(months)} 个月，累计 {len(links)} 篇")
        time.sleep(args.delay / 2)

    print(f"共发现 essay {len(links)} 篇，均匀抽样 {args.limit} 篇")
    if not links:
        return 1
    step = max(len(links) / args.limit, 1)
    sample = [links[int(i * step)] for i in range(min(args.limit, len(links)))]

    # 2. 抓取与解析
    agg: list[dict] = []
    fails = 0
    for ym, url in sample:
        slug = re.search(r"/([^/]+)\.html$", url).group(1)
        out_file = out_dir / f"ruanyifeng_essay_{slug}.yaml"
        if out_file.exists():
            continue
        html = fetch(url, retries=1)
        if not html or "404 Not Found" in html or len(html) < 20000:
            fails += 1
            print(f"  ✗ {slug} 未取得")
            if fails >= 8:
                print("连续失败过多，中止")
                break
            continue
        info = parse_article(html)
        if not info or info["chars"] < 400:
            fails += 1
            print(f"  ✗ {slug} 解析失败/正文过短")
            continue
        fails = 0

        item = {
            "corpus_id": f"corpus.blogs.ruanyifeng-essay-{slug}",
            "state": "READ",
            "title": info["title"],
            "speaker_or_author": "阮一峰",
            "source_url": url,
            "source_owner": "阮一峰",
            "date": ym,
            "access_date": date.today().isoformat(),
            "source_type": "blog",
            "access_level": "full",
            "transcript_quality": "official",
            "content_obtained": "D（可合法访问的完整文章）：机器完整读取正文并计算特征",
            "content_length": f"{info['chars']} 字 / {info['paragraphs']} 段 / {info['sentences']} 句",
            "selected_segments": [info["excerpt"]],
            "copyright_notes": "robots 信号 search=yes,use=reference；仅存元数据+特征+短摘录，不存全文",
            "medium": "article",
            "audience": "技术与泛知识读者",
            "topic": "随笔/评论",
            "topic_complexity": "medium",
            "preparedness": "edited",
            "analysis_notes": "特征统计见本条目；深度标注待人工精读（Quantitative ≠ Quality）",
            "discourse_functions": [],
            "language_features": [
                f"平均句长 {info['sent_len_mean']} 字（峰值 {info['sent_len_max']}）",
                f"话语标记密度 {info['marker_per_1000']}/千字",
                f"加粗 {info['bolds']} 处 / 小标题 {info['headings']} 处 / 编号项 {info['enumerations']} 处",
                f"问句 {info['questions']} 个",
            ],
            "rhetorical_features": [],
            "sentence_rhythm": f"mean={info['sent_len_mean']}, max={info['sent_len_max']}",
            "logical_structure": "",
            "reader_or_listener_engagement": "",
            "strengths": ["待人工精读标注"],
            "weaknesses": ["待人工精读标注"],
            "overuse_risks": ["待人工精读标注"],
            "transferable_patterns": [],
            "counterexamples": [],
            "not_transferable": [],
            "provenance": ["cand.blogs.ruanyifeng-essay"],
            "notes": f"日期为月份级精度（取自真实 URL）；话语标记分布: {json.dumps(info['markers'], ensure_ascii=False)}",
        }
        out_file.write_text(yaml.safe_dump(item, allow_unicode=True, sort_keys=False), encoding="utf-8")
        agg.append({"slug": slug, **info})
        print(f"  ✓ {slug}: {info['chars']}字 句长均值{info['sent_len_mean']} 标记/千字={info['marker_per_1000']}")
        time.sleep(args.delay)

    if agg:
        summary = {
            "n": len(agg),
            "chars_median": sorted(a["chars"] for a in agg)[len(agg) // 2],
            "sent_len_mean_overall": round(sum(a["sent_len_mean"] for a in agg) / len(agg), 1),
            "sent_len_max_overall": max(a["sent_len_max"] for a in agg),
            "marker_density_mean": round(sum(a["marker_per_1000"] for a in agg) / len(agg), 2),
            "questions_mean": round(sum(a["questions"] for a in agg) / len(agg), 1),
            "bolds_mean": round(sum(a["bolds"] for a in agg) / len(agg), 1),
            "top_markers": Counter(m for a in agg for m in a["markers"]).most_common(10),
        }
        (ROOT / "corpus" / "metadata" / "ruanyifeng_essay_features.json").write_text(
            json.dumps({"summary": summary, "items": agg}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("\n聚合：", json.dumps(summary, ensure_ascii=False))
    print(f"完成：{len(agg)} 篇入库（state=READ），失败 {fails}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
