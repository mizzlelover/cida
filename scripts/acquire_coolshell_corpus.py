#!/usr/bin/env python3
"""辞达 · CoolShell（陈皓）博客语料真实采集器

合规声明：
- 目标站 robots.txt 仅禁止 Baiduspider，未禁止其他抓取；无 ai-train 信号。
  本脚本仅做语言机制分析，保存元数据 + 计算特征 + 最短摘录（≤80 字），
  不保存/再分发全文，不用于模型训练。
- 礼貌抓取：限速、失败退避、连续失败即停。

用法：
    python scripts/acquire_coolshell_corpus.py --pages 8 --limit 60
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) cida-research/0.2 (analysis-only, short-excerpt)"}

sys.path.insert(0, str(ROOT / "scripts"))
from acquire_blog_corpus import MARKERS  # noqa: E402

import subprocess  # noqa: E402
import yaml  # noqa: E402


def fetch(url: str, retries: int = 2) -> str | None:
    """coolshell 对 Python TLS 指纹返回 500，curl 稳定 200 —— 改用 curl。"""
    for attempt in range(retries + 1):
        try:
            r = subprocess.run(
                ["curl", "-sL", "--max-time", "25", "-A",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X) cida-research/0.2", url],
                capture_output=True, timeout=30)
            if r.returncode == 0 and len(r.stdout) > 2000:
                return r.stdout.decode("utf-8", "ignore")
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2 * (attempt + 1))
    return None


def list_article_urls(pages: int, delay: float) -> list[str]:
    urls: list[str] = []
    seen = set()
    for p in range(1, pages + 1):
        u = "https://coolshell.cn/" if p == 1 else f"https://coolshell.cn/page/{p}"
        html = fetch(u, retries=1)
        if not html:
            print(f"  ✗ 列表页 {p} 未取得")
            continue
        for m in re.findall(r'href="(https://coolshell\.cn/articles/\d+\.html)"', html):
            if m not in seen:
                seen.add(m)
                urls.append(m)
        time.sleep(delay)
    return urls


def parse_article(html: str) -> dict:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    title = (title_tag.get_text() if title_tag else "").split(" | ")[0].strip()
    body = soup.select_one("div.entry-content")
    if not body:
        return {}
    # 去掉脚本/样式/分享按钮等噪音
    for junk in body.select("script, style, .sharedaddy, .jp-relatedposts"):
        junk.decompose()
    paras = [p.get_text(strip=True) for p in body.find_all(["p", "li"])]
    text = "\n".join(p for p in paras if p)
    sentences = [s for s in re.split(r"[。！？!?]+", text) if len(s.strip()) >= 2]
    lengths = [len(s.strip()) for s in sentences]
    chars = len(text)
    marker_counts = {m: text.count(m) for m in MARKERS if text.count(m) > 0}
    return {
        "title": title,
        "chars": chars,
        "paragraphs": len([p for p in paras if p]),
        "sentences": len(sentences),
        "sent_len_mean": round(sum(lengths) / max(len(lengths), 1), 1),
        "sent_len_max": max(lengths) if lengths else 0,
        "questions": text.count("？") + text.count("?"),
        "bolds": len(body.find_all(["strong", "b"])),
        "headings": len(body.find_all(["h2", "h3", "h4"])),
        "enumerations": len(re.findall(r"[（(]\d+[)）]|^\d+、", text, re.M)),
        "markers": marker_counts,
        "marker_per_1000": round(sum(marker_counts.values()) / max(chars, 1) * 1000, 2),
        "excerpt": text[:80].replace("\n", " "),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=8, help="抓取多少个列表页")
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--delay", type=float, default=0.5)
    args = ap.parse_args()

    out_dir = ROOT / "corpus" / "blogs"
    out_dir.mkdir(parents=True, exist_ok=True)

    urls = list_article_urls(args.pages, args.delay)
    print(f"列表页共发现 {len(urls)} 篇文章")

    agg: list[dict] = []
    fails = 0
    for url in urls[: args.limit]:
        aid = re.search(r"articles/(\d+)\.html", url).group(1)
        out_file = out_dir / f"coolshell_{aid}.yaml"
        if out_file.exists():
            continue
        html = fetch(url, retries=1)
        if not html or len(html) < 20000:
            fails += 1
            print(f"  ✗ {aid} 未取得")
            if fails >= 8:
                print("连续失败过多，中止")
                break
            continue
        info = parse_article(html)
        if not info or info["chars"] < 400:
            fails += 1
            print(f"  ✗ {aid} 解析失败/正文过短")
            continue
        fails = 0

        item = {
            "corpus_id": f"corpus.blogs.coolshell-{aid}",
            "state": "READ",
            "title": info["title"],
            "speaker_or_author": "陈皓（左耳朵耗子）",
            "source_url": url,
            "source_owner": "陈皓",
            "date": "",  # 列表页无可靠日期；待人工补录
            "access_date": __import__("datetime").date.today().isoformat(),
            "source_type": "blog",
            "access_level": "full",
            "transcript_quality": "official",
            "content_obtained": "D（可合法访问的完整文章）：机器完整读取正文并计算特征",
            "content_length": f"{info['chars']} 字 / {info['paragraphs']} 段 / {info['sentences']} 句",
            "selected_segments": [info["excerpt"]],
            "copyright_notes": "robots 仅禁 Baiduspider；仅存元数据+特征+短摘录，不存全文",
            "medium": "article",
            "audience": "技术读者",
            "topic": "技术观点/工程文化",
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
            "provenance": ["cand.blogs.coolshell"],
            "notes": f"话语标记分布: {json.dumps(info['markers'], ensure_ascii=False)}",
        }
        out_file.write_text(yaml.safe_dump(item, allow_unicode=True, sort_keys=False), encoding="utf-8")
        agg.append({"id": aid, **info})
        print(f"  ✓ {aid}: {info['chars']}字 句长均值{info['sent_len_mean']} 标记/千字={info['marker_per_1000']}")
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
        (ROOT / "corpus" / "metadata" / "coolshell_features.json").write_text(
            json.dumps({"summary": summary, "items": agg}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("\n聚合：", json.dumps(summary, ensure_ascii=False))
    print(f"完成：{len(agg)} 篇入库（state=READ），失败 {fails}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
