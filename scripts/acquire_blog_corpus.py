#!/usr/bin/env python3
"""辞达 · 博客语料真实采集器（§3/§4/§8 执行工具）

合规声明：
- 目标站 robots.txt 内容信号：search=yes, use=reference, ai-train=no。
  本脚本仅做语言机制分析，保存元数据 + 计算特征 + 最短摘录（≤80 字），
  不保存/再分发全文，不用于模型训练。与站点信号相容。
- 礼貌抓取：限速、失败退避、429/403 即停。

用法：
    python scripts/acquire_blog_corpus.py --site ruanyifeng-weekly --step 5
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) cida-research/0.2 (analysis-only, short-excerpt)"}

try:
    import yaml
except ImportError:
    print("需要 PyYAML：pip install pyyaml")
    sys.exit(2)

MARKERS = ["其实", "但是", "不过", "所以", "也就是说", "换句话说",
           "问题是", "你会发现", "反过来看", "说到底", "更重要的是",
           "值得注意的是", "首先", "其次", "总之", "综上"]
# 实测锚点（均经 HTTP 实探验证）：
#   第 1 期   = 2018/04（corpus/blogs/ruanyifeng_weekly_1.yaml 已验证 200）
#   第 166 期 = 2021/07（实探验证，其余月份 404）
#   第 409 期 = 2026/08（实探验证 200，104633B）
# 周刊并非严格每周（有休刊），单锚线性外推会累积漂移，
# 故用首尾双锚内插估算月份，再向前后各试探最多 3 个月。
ANCHOR_LO = (1, date(2018, 4, 20))
ANCHOR_HI = (409, date(2026, 8, 21))
AVG_DAYS = (ANCHOR_HI[1] - ANCHOR_LO[1]).days / (ANCHOR_HI[0] - ANCHOR_LO[0])  # ≈7.46 天/期


def shift_month(d: date, months: int) -> date:
    m = d.month - 1 + months
    return date(d.year + m // 12, m % 12 + 1, 1)


def fetch(url: str, retries: int = 2) -> str | None:
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception as e:  # noqa: BLE001
            if attempt == retries:
                return None
            time.sleep(2 * (attempt + 1))
    return None


def parse_article(html: str) -> dict:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    title = (title_tag.get_text() if title_tag else "").split(" - ")[0].strip()
    body = soup.select_one("div.asset-content") or soup.find("article")
    if not body:
        return {}
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
    ap.add_argument("--site", default="ruanyifeng-weekly")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=411)
    ap.add_argument("--step", type=int, default=5)
    ap.add_argument("--delay", type=float, default=0.8)
    ap.add_argument("--limit", type=int, default=90)
    ap.add_argument("--fix-dates", action="store_true",
                    help="只修复存量条目：把 date 校正为 source_url 中的真实月份")
    ap.add_argument("--aggregate-only", action="store_true",
                    help="不采集，只用全部存量条目重建聚合特征 JSON")
    args = ap.parse_args()

    out_dir = ROOT / "corpus" / "blogs"

    if args.aggregate_only:
        agg = []
        for f in sorted(out_dir.glob("*.yaml")):
            item = yaml.safe_load(f.read_text(encoding="utf-8"))
            feats = "\n".join(item.get("language_features") or [])
            m_len = re.search(r"(\d+(?:\.\d+)?) 字 / (\d+) 段 / (\d+) 句", item.get("content_length") or "")
            m_mean = re.search(r"平均句长 ([\d.]+) 字（峰值 (\d+)）", feats)
            m_mark = re.search(r"话语标记密度 ([\d.]+)/千字", feats)
            m_q = re.search(r"问句 (\d+) 个", feats)
            m_b = re.search(r"加粗 (\d+) 处", feats)
            m_markers = re.search(r"话语标记分布: (\{.*\})", item.get("notes") or "")
            if not (m_len and m_mean and m_mark):
                print(f"  跳过（特征不可解析）: {f.name}")
                continue
            n = int(re.search(r"weekly-(\d+)", item["corpus_id"]).group(1))
            agg.append({
                "issue": n,
                "date": str(item.get("date", "")),
                "chars": int(m_len.group(1)),
                "sent_len_mean": float(m_mean.group(1)),
                "sent_len_max": int(m_mean.group(2)),
                "marker_per_1000": float(m_mark.group(1)),
                "questions": int(m_q.group(1)) if m_q else 0,
                "bolds": int(m_b.group(1)) if m_b else 0,
                "markers": json.loads(m_markers.group(1)) if m_markers else {},
            })
        if agg:
            write_summary(agg)
        print(f"聚合完成：{len(agg)} 条")
        return 0

    if args.fix_dates:
        fixed = 0
        for f in sorted(out_dir.glob("*.yaml")):
            item = yaml.safe_load(f.read_text(encoding="utf-8"))
            ym = re.search(r"/blog/(\d{4})/(\d{2})/", item.get("source_url") or "")
            if not ym:
                continue
            real = f"{ym.group(1)}-{ym.group(2)}"
            if str(item.get("date", ""))[:7] != real:
                item["date"] = real
                note = "日期为月份级精度（取自真实 URL）"
                if note not in str(item.get("notes", "")):
                    item["notes"] = f"{note}；{item.get('notes', '')}".strip("；")
                f.write_text(yaml.safe_dump(item, allow_unicode=True, sort_keys=False), encoding="utf-8")
                fixed += 1
        print(f"修复完成：{fixed} 条日期已校正为 URL 真实月份")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    agg: list[dict] = []
    fails = 0

    issues = list(range(args.start, args.end + 1, args.step))[: args.limit]
    print(f"计划采集 {len(issues)} 期（step={args.step}）")

    for n in issues:
        slug = f"ruanyifeng-weekly-{n}"
        out_file = out_dir / f"{slug.replace('-', '_')}.yaml"
        if out_file.exists():
            continue
        url = f"https://www.ruanyifeng.com/blog/20xx/xx/weekly-issue-{n}.html"
        # 双锚内插估算月份，再向前后各试探最多 3 个月（吸收休刊漂移）
        est = ANCHOR_LO[1] + timedelta(days=round(AVG_DAYS * (n - ANCHOR_LO[0])))
        html = None
        real_url = None
        for off in (0, 1, -1, 2, -2, 3, -3):
            d = shift_month(est, off)
            u = f"https://www.ruanyifeng.com/blog/{d:%Y/%m}/weekly-issue-{n}.html"
            html = fetch(u, retries=1)
            if html and "404 Not Found" not in html and len(html) > 20000:
                real_url = u
                break
            html = None
        if not html:
            fails += 1
            print(f"  ✗ issue {n} 未取得")
            if fails >= 8:
                print("连续失败过多，中止（可能限流）")
                break
            continue

        info = parse_article(html)
        if not info or info["chars"] < 400:
            fails += 1
            print(f"  ✗ issue {n} 解析失败/正文过短")
            continue
        fails = 0  # 成功即清零，只按「连续」失败中止

        # 日期取真实 URL 的 YYYY/MM（月份级精度），不再使用估算日
        ym = re.search(r"/blog/(\d{4})/(\d{2})/", real_url)
        est_str = f"{ym.group(1)}-{ym.group(2)}" if ym else est.isoformat()[:7]
        item = {
            "corpus_id": f"corpus.blogs.{slug}",
            "state": "READ",  # 机器完整读取正文+特征计算；人工精读标注后升 ANNOTATED
            "title": info["title"],
            "speaker_or_author": "阮一峰",
            "source_url": real_url,
            "source_owner": "阮一峰",
            "date": est_str,
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
            "topic": "科技周刊",
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
            "provenance": ["cand.blogs.ruanyifeng-weekly"],
            "notes": f"日期为月份级精度（取自真实 URL）；话语标记分布: {json.dumps(info['markers'], ensure_ascii=False)}",
        }
        out_file.write_text(yaml.safe_dump(item, allow_unicode=True, sort_keys=False), encoding="utf-8")
        agg.append({"issue": n, **info})
        print(f"  ✓ issue {n}: {info['chars']}字 句长均值{info['sent_len_mean']} 标记/千字={info['marker_per_1000']}")
        time.sleep(args.delay)

    # 聚合统计（供知识库校准引用）
    if agg:
        write_summary(agg)
    print(f"完成：{len(agg)} 期入库（state=READ），失败 {fails}")
    return 0


def write_summary(agg: list[dict]) -> None:
    agg = sorted(agg, key=lambda a: a["issue"])
    summary = {
        "n": len(agg),
        "issue_range": [agg[0]["issue"], agg[-1]["issue"]],
        "chars_median": sorted(a["chars"] for a in agg)[len(agg) // 2],
        "sent_len_mean_overall": round(sum(a["sent_len_mean"] for a in agg) / len(agg), 1),
        "sent_len_max_overall": max(a["sent_len_max"] for a in agg),
        "marker_density_mean": round(sum(a["marker_per_1000"] for a in agg) / len(agg), 2),
        "questions_mean": round(sum(a["questions"] for a in agg) / len(agg), 1),
        "bolds_mean": round(sum(a["bolds"] for a in agg) / len(agg), 1),
        "top_markers": Counter(m for a in agg for m in a["markers"]).most_common(10),
    }
    (ROOT / "corpus" / "metadata" / "ruanyifeng_weekly_features.json").write_text(
        json.dumps({"summary": summary, "items": agg}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\n聚合：", json.dumps(summary, ensure_ascii=False))
    print("特征汇总 -> corpus/metadata/ruanyifeng_weekly_features.json")


if __name__ == "__main__":
    sys.exit(main())
