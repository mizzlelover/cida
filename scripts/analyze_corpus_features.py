#!/usr/bin/env python3
"""analyze_corpus_features.py · 语料特征分析工具（需求 §95）

对输入文本文件计算统计特征，用于语料采集期的量化辅助。
统计特征只能辅助，不得定义好坏（§96）：所有输出必须结合功能与语境解读。

用法：
    python3 scripts/analyze_corpus_features.py <text1.txt> [text2.txt ...]
    python3 scripts/analyze_corpus_features.py --json <out.json> <text1.txt> ...

输出指标：
- 句长分布（均值/中位/P25/P75/最大值）
- 话语标记频次（与 coolshell/hecaitou 特征文件同尺的 10 标记集，密度/千字）
- 问句频次（？计数与每千字密度）
- 代词分布（我/你/他/她/我们/你们/他们/大家/你们 等，区分第一/二人称密度）
- 词汇多样性（字符二元组 TTR 与实词粗估；中文无分词，采用 bigram 近似并注明）
- 重复分析（≥4 字符串片段在文内重复率 top5）

注意：输入应为已清洗的纯文本；工具不判断优劣，只给出可复核的量化事实。
"""
import sys
import json
import re
import statistics
from collections import Counter

MARKERS = ['但是', '所以', '其实', '不过', '首先', '也就是说',
           '你会发现', '问题是', '总之', '更重要的是']

PRONOUNS = {
    'first_singular': ['我'],
    'first_plural': ['我们', '咱们'],
    'second': ['你', '您', '你们'],
    'third': ['他', '她', '他们', '她们'],
    'indefinite': ['大家', '有些人', '很多人', '人们'],
}


def sentences(text):
    parts = re.split(r'[。！？]', re.sub(r'\s+', '。', text))
    return [s for s in parts if s.strip()]


def analyze(text):
    lens = [len(s) for s in sentences(text)]
    n_chars = max(len(re.sub(r'\s', '', text)), 1)
    qs = len(re.findall(r'？', text))
    markers = {m: len(re.findall(m, text)) for m in MARKERS}
    markers = {k: v for k, v in markers.items() if v}
    pron = {}
    for group, words in PRONOUNS.items():
        pron[group] = sum(len(re.findall(w, text)) for w in words)
    # lexical diversity: character-bigram TTR（中文无分词的近似，注明口径）
    chars = re.sub(r'\s', '', text)
    bigrams = [chars[i:i + 2] for i in range(len(chars) - 1)]
    bigram_ttr = round(len(set(bigrams)) / max(len(bigrams), 1), 3)
    # repetition analysis: 4-gram repeats（≥4 字片段重复，top5）
    four = [chars[i:i + 4] for i in range(len(chars) - 3)]
    counts = Counter(four)
    repeats = [(frag, n) for frag, n in counts.most_common(8)
               if n > 1 and not re.fullmatch(r'[，。、；：的了是在和与]', frag or 'x')]
    return {
        'chars': n_chars,
        'sentences': len(lens),
        'sent_len_mean': round(sum(lens) / max(len(lens), 1), 1),
        'sent_len_median': statistics.median(lens) if lens else 0,
        'sent_len_p25': round(sorted(lens)[max(0, int(len(lens) * .25))], 1) if lens else 0,
        'sent_len_p75': round(sorted(lens)[min(len(lens) - 1, int(len(lens) * .75))], 1) if lens else 0,
        'sent_len_max': max(lens) if lens else 0,
        'questions': qs,
        'question_density_per_kilochar': round(qs / n_chars * 1000, 2),
        'marker_total': sum(markers.values()),
        'marker_density_per_kilochar': round(sum(markers.values()) / n_chars * 1000, 2),
        'markers': markers,
        'pronouns': pron,
        'pronoun_density_per_kilochar': {
            k: round(v / n_chars * 1000, 2) for k, v in pron.items()},
        'bigram_ttr': bigram_ttr,
        'repeat_4gram_top5': repeats[:5],
    }


def main():
    args = sys.argv[1:]
    as_json = False
    if args and args[0] == '--json':
        as_json = True
        args = args[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    out = {}
    for path in args:
        try:
            text = open(path, encoding='utf-8', errors='ignore').read()
        except OSError as exc:
            print(f'skip {path}: {exc}', file=sys.stderr)
            continue
        out[path] = analyze(text)
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        for path, r in out.items():
            print(f"== {path}")
            for k, v in r.items():
                print(f"  {k}: {v}")


if __name__ == '__main__':
    main()
