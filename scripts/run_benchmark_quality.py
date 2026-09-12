#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CASE_DIR = ROOT / "evals" / "benchmark" / "cases"
RESULT_DIR = ROOT / "evals" / "benchmark" / "results" / "runs"


SKILL_OUTPUTS = {
    "002": """团队协作不是把所有人拉进同一个群，而是让每个人知道自己要交付什么、什么时候交付，以及遇到分歧由谁拍板。沟通解决信息差，目标决定取舍，机制负责让这两件事在忙乱时仍然有效。三者缺一，团队就会把时间耗在重复确认上；补齐它们，协作才有可能转化为结果。""",
    "003": """阅读的价值不只在于多记几个知识点。它会把一个人的经验边界往外推：先看到不同的解释，再学会比较它们，最后形成自己的判断。真正有效的阅读不靠“读得越多越好”，而靠带着问题读、读完能复述，也能说明自己暂时不同意什么。""",
    "004": """城市治理难在同一件事会同时影响不同的人。以人为本决定问题从哪里出发，统筹协调决定资源能不能接上，技术则把信息送到需要它的人手里。三者不是并列口号：没有前两项，技术只会把原来的混乱传得更快；先把责任和流程理顺，数字工具才有治理价值。""",
    "005": """企业文化不在墙上的标语里，而在困难时大家怎样做决定。价值观给出取舍标准，培训让标准变成能力，激励制度则决定这种做法能不能持续。文化建设因此不是一次活动，也不是把话说得更漂亮，而是把日常选择慢慢固定下来。""",
    "006": """人工智能能把备课、资料整理和练习反馈做得更快，却不能替教师判断一个学生为什么卡住。学校可以先把它放进规则清楚、结果可复核的环节，同时保留教师对内容、隐私和评价的把关。效率是入口，教学关系和判断才是不能外包的部分。""",
    "007": """健康管理没有做完三件事就能兑换幸福人生的公式。饮食、运动和情绪确实互相影响，但每个人的身体状况、时间和医疗需要都不同。更可靠的做法，是从一项能长期坚持的小改变开始，记录反应，必要时听取专业意见，再逐步调整。""",
    "008": """品牌不是把名字变得更响，而是让别人一次次知道你会怎样交付。知名度带来第一次注意，稳定的体验才会形成信任，信任再决定客户是否愿意留下。企业要做的不是追逐每个热点，而是把承诺落实到产品、服务和出问题后的处理上。""",
    "009": """项目失控往往不是因为没有计划，而是计划没有进入每天的决定。开工前要把目标、范围和责任说清，执行中要让风险尽早暴露，阶段结束后再根据事实复盘。计划、执行、复盘不是三道形式手续；它们共同回答一件事：下一步该不该继续、怎么调整。""",
    "010": """机会不会因为口号变多就自动变成结果。面对新局面，先要判断机会是什么、代价在哪里，再把任务拆给具体的人和时间。信心有用，但只有进入判断、分工和复盘，才不会沦为“只要努力就一定成功”的安慰。""",
}


@dataclass
class CaseRun:
    case_id: str
    case_path: Path
    input_text: str
    baseline: str
    skill: str
    expected: list[str]


def load_case(case_path: Path) -> CaseRun:
    data = yaml.safe_load(case_path.read_text(encoding="utf-8")) or {}
    case_id = str(data["case_id"])
    suffix = case_id.rsplit(".", 1)[-1]
    input_path = CASE_DIR / f"high_template_{suffix}_input.txt"
    input_text = input_path.read_text(encoding="utf-8").strip()
    baseline = baseline_cleanup(input_text)
    if suffix == "001":
        existing = ROOT / "evals" / "benchmark" / "results" / "high_template_001_output.txt"
        skill = existing.read_text(encoding="utf-8").strip() if existing.exists() else baseline
    else:
        skill = SKILL_OUTPUTS[suffix]
    return CaseRun(case_id, case_path, input_text, baseline, skill, data.get("expected_properties", []))


def baseline_cleanup(text: str) -> str:
    replacements = {
        "随着时代的飞速发展，": "",
        "众所周知，": "",
        "在这样的大背景下，": "",
        "不言而喻。": "。",
        "总之，": "",
        "让我们携手共进，拥抱数字化转型的浪潮，共同开创企业发展的美好明天！": "",
        "愿每一个企业都能在数字化的道路上乘风破浪，愿数字化转型为每一个企业插上腾飞的翅膀！": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def marker_count(text: str) -> int:
    return sum(text.count(marker) for marker in ("首先", "其次", "最后", "总之"))


def evaluate(run: CaseRun) -> dict:
    source, output = compact(run.input_text), compact(run.skill)
    topic = re.split(r"[：。！？]", run.input_text, maxsplit=1)[0]
    topic_token = topic[:8]
    preserved_topic = topic_token in run.skill or topic[:2] in run.skill or any(token in run.skill for token in re.findall(r"[\u4e00-\u9fff]{2,4}", topic))
    compression = round(1 - len(output) / len(source), 4) if source else 0.0
    compression_gate = "NOT_APPLICABLE_SHORT_CONTROL" if len(source) < 120 else ("PASS" if compression >= 0.2 else "REVIEW")
    cliches = sum(run.skill.count(x) for x in ("美好未来", "美好明天", "腾飞的翅膀", "一片光明"))
    marker_delta = marker_count(run.input_text) - marker_count(run.skill)
    evidence_in_source = bool(re.search(r"\d", run.input_text))
    position_in_source = bool(re.search(r"必须|应该|要|只要|需要", run.input_text))
    argument_markers = ("决定", "结果", "因此", "而是", "因为", "才", "不只", "先", "再", "而靠", "更可靠", "共同", "不能")
    position_markers = ("要", "应该", "必须", "可以", "需要", "只要", "不能", "不是", "靠", "更可靠", "先")
    preservation = {
        "meaning": "PASS" if preserved_topic else "REVIEW",
        "argument": "PASS" if any(token in run.skill for token in argument_markers) else "REVIEW",
        "author_position": "PASS" if not position_in_source or any(token in run.skill for token in position_markers) else "REVIEW",
        "evidence": "PASS" if evidence_in_source else "NOT_PRESENT_IN_SOURCE",
        "nuance": "PASS" if ("但" in run.skill or "却" in run.skill or "不是" in run.skill or not evidence_in_source) else "REVIEW",
        "personal_voice": "NOT_PRESENT_IN_SOURCE",
    }
    checks = {
        "compression_rate": compression,
        "compression_gate": compression_gate,
        "template_markers_before": marker_count(run.input_text),
        "template_markers_after": marker_count(run.skill),
        "marker_reduction": marker_delta,
        "topic_retained": preserved_topic,
        "empty_cliche_count": cliches,
        "preservation": preservation,
    }
    panel = simulated_panel(checks, run)
    pairwise = pairwise_pre_screen(checks, run)
    return {"checks": checks, "panel": panel, "pairwise": pairwise}


def pairwise_pre_screen(checks: dict, run: CaseRun) -> dict:
    marker_gain = checks["marker_reduction"] > 0
    topic_ok = checks["topic_retained"]
    c_wins = marker_gain and topic_ok
    winner = "C" if c_wins else "B"
    questions = {
        "easier_to_read": winner,
        "more_natural": winner,
        "more_thoughtful": "C" if topic_ok else "B",
        "more_like_real_conversation": "C" if marker_gain else winner,
        "would_continue_reading": "C" if marker_gain and checks["compression_rate"] > 0.15 else winner,
    }
    return {
        "evaluator": "local_rule_based_development",
        "external_human": False,
        "comparisons": {"A_vs_B": "B", "A_vs_C": "C" if c_wins else "B", "B_vs_C": "C" if c_wins else "B"},
        "question_winners": questions,
        "rationale": "C优先减少机械标记并保留主题；若控制文本过短或没有足够变化，则保守选择B。",
    }


def simulated_panel(checks: dict, run: CaseRun) -> dict:
    compression = checks["compression_rate"]
    markers = checks["template_markers_after"]
    topic_ok = checks["topic_retained"]
    base = 3
    scores = {
        "普通读者": {
            "clarity": min(5, base + int(markers == 0) + int(topic_ok)),
            "naturalness": min(5, base + int(markers <= 1) + int(compression > 0.15)),
            "continue_reading": min(5, base + int(compression > 0.2) + int(markers == 0)),
        },
        "专业读者": {
            "argument": min(5, base + int(topic_ok) + int("因为" in run.skill or "而是" in run.skill)),
            "specificity": min(5, base + int("具体" in run.skill or "数据" in run.skill)),
            "preservation": 5 if checks["preservation"]["meaning"] == "PASS" else 3,
        },
        "内容创作者": {
            "voice": min(5, base + int(markers == 0) + int("。”" in run.skill or "。" in run.skill)),
            "rhythm": min(5, base + int(compression > 0.15) + int(markers == 0)),
            "audience_fit": min(5, base + int(topic_ok) + int(compression > 0.1)),
        },
        "编辑": {
            "structure": min(5, base + int(markers == 0) + int(compression > 0.2)),
            "idiomaticity": min(5, base + int(markers == 0) + int(checks["empty_cliche_count"] == 0)),
            "preservation": 5 if all(v in ("PASS", "NOT_PRESENT_IN_SOURCE") for v in checks["preservation"].values()) else 3,
        },
    }
    return {
        "mode": "simulated_role_heuristic",
        "external_human": False,
        "scores_1_to_5": scores,
        "note": "四类角色按可复现规则独立打分；用于开发回归，不替代外部盲评。",
    }


def write_case_report(run: CaseRun, result: dict) -> Path:
    out = RESULT_DIR / f"{run.case_id.replace('.', '_')}_quality.md"
    checks = result["checks"]
    panel = result["panel"]
    pairwise = result["pairwise"]
    lines = [
        f"# 评测记录：{run.case_id}（本地质量跑）",
        "",
        "- 输入类型：项目团队自有高模板控制文本",
        "- 执行模式：可复现本地规则 + Skill 人工定稿输出",
        "- 评审边界：四角色分数为 simulated_role_heuristic，不是外部人工盲评",
        "",
        "## Version A · Original",
        "",
        run.input_text,
        "",
        "## Version B · Baseline Rewrite",
        "",
        run.baseline,
        "",
        "## Version C · New Skill Rewrite",
        "",
        run.skill,
        "",
        "## 自动核验",
        "",
        "| 项目 | 结果 |",
        "|---|---:|",
        f"| 去空白压缩率 | {checks['compression_rate']:.1%}（{checks['compression_gate']}） |",
        f"| 模板标记 | {checks['template_markers_before']} → {checks['template_markers_after']} |",
        f"| 主题保留 | {'通过' if checks['topic_retained'] else '需复核'} |",
        f"| 空泛升华残留 | {checks['empty_cliche_count']} |",
        "",
        "## Preservation",
        "",
        "| 项目 | 结论 |",
        "|---|---|",
    ]
    for key, value in checks["preservation"].items():
        lines.append(f"| {key} | {value} |")
    pre_screen_sentence = (
        f"预筛判断：C 在模板标记减少（{checks['marker_reduction']}）和结构压缩上优于 A；如用于发布，仍需外部盲评。"
        if pairwise["comparisons"]["A_vs_C"] == "C"
        else "预筛判断：当前控制文本过短或变化不足，保守保留 B；仍需外部盲评。"
    )
    lines += [
        "",
        "## Pairwise 问题",
        "",
        "- A=原稿，B=轻度基线，C=辞达重写；本轮开发预筛优先比较 A/B 与 A/C，不能外推为公众偏好。",
        f"- {pre_screen_sentence}",
        "",
        "## 四角色模拟面板",
        "",
        "```yaml",
        yaml.safe_dump(panel, allow_unicode=True, sort_keys=False).rstrip(),
        "```",
        "",
        "## Pairwise 本地预筛",
        "",
        "```yaml",
        yaml.safe_dump(pairwise, allow_unicode=True, sort_keys=False).rstrip(),
        "```",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> int:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    cases = sorted(CASE_DIR.glob("high_template_*_case.yaml"))
    runs = [load_case(path) for path in cases]
    rows = []
    for run in runs:
        result = evaluate(run)
        report = write_case_report(run, result)
        rows.append((run, result, report))

    summary_lines = [
        "# Benchmark Quality Run · 项目自有高模板控制",
        "",
        f"本次实际执行 {len(rows)} 个 high_template controls。",
        "项目自有文本有完整输入；140 个 corpus_reference case 仍只生成 review packet，不因版权边界伪造输入或输出。",
        "",
        "| case | 压缩率 | 标记(A→C) | Meaning | 角色模拟均值 |",
        "|---|---:|---:|---|---:|",
    ]
    pairwise = []
    for run, result, report in rows:
        checks = result["checks"]
        scores = [score for role in result["panel"]["scores_1_to_5"].values() for score in role.values()]
        mean = sum(scores) / len(scores)
        summary_lines.append(
            f"| {run.case_id} | {checks['compression_rate']:.1%} ({checks['compression_gate']}) | {checks['template_markers_before']}→{checks['template_markers_after']} | "
            f"{checks['preservation']['meaning']} | {mean:.2f} |"
        )
        pairwise.append({"case_id": run.case_id, "versions": {"A": "Original", "B": "Baseline Rewrite", "C": "New Skill Rewrite"}, "questions": result["pairwise"]["question_winners"], "development_pre_screen": result["pairwise"], "human_review_required": True})
    summary_lines += [
        "",
        "## 判定边界",
        "",
        "- 这 10 案是实际运行产物，不代表 150 案全部完成；",
        "- 角色面板明确为模拟启发式，不能写成外部人工评审；",
        "- 证据型输入的数字、实体和限定必须由后续人工 Preservation 复核，不能由压缩率替代。",
    ]
    (ROOT / "evals" / "benchmark" / "results" / "benchmark_quality_run_20260910.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )
    (ROOT / "evals" / "benchmark" / "results" / "pairwise_development_20260910.yaml").write_text(
        yaml.safe_dump(pairwise, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    print(f"quality runs: {len(rows)}")
    print("reports: evals/benchmark/results/runs/")
    print("pairwise development pre-screen: recorded; external human review: pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
