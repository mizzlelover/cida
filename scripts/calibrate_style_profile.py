#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RUN_DIR = ROOT / "evals" / "benchmark" / "results" / "runs"
OUT_DIR = ROOT / "evals" / "style_calibration"

INITIAL_PARAMETERS = {
    "formality": "4–5",
    "orality": "6–7",
    "information_density": "6–8",
    "logical_explicitness": 8,
    "intimacy": "6–7",
    "rhetorical_density": "4–5",
    "judgment_strength": "6–8",
    "rhythmic_variation": 7,
    "narrative_presence": "context-dependent",
    "reader_interaction": 6,
}


def parse_report(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    marker = re.search(r"\| 模板标记 \| (\d+) → (\d+) \|", text)
    compression = re.search(r"\| 去空白压缩率 \| ([^（]+)（([^）]+)） \|", text)
    preservation = {
        key: value
        for key, value in re.findall(
            r"\| (meaning|argument|author_position|evidence|nuance|personal_voice) \| ([^|]+) \|",
            text,
        )
    }
    return {
        "case_id": path.stem.removesuffix("_quality").replace("_", "."),
        "marker_before": int(marker.group(1)) if marker else None,
        "marker_after": int(marker.group(2)) if marker else None,
        "compression_gate": compression.group(2).strip() if compression else "UNKNOWN",
        "preservation": {key: value.strip() for key, value in preservation.items()},
    }


def main() -> int:
    reports = sorted(RUN_DIR.glob("*_quality.md"))
    records = [parse_report(path) for path in reports]
    if not records:
        print("style calibration: no quality reports")
        return 1

    applicable = [record for record in records if record["compression_gate"] != "NOT_APPLICABLE_SHORT_CONTROL"]
    marker_reduction = [
        record
        for record in records
        if record["marker_before"] is not None
        and record["marker_after"] is not None
        and record["marker_after"] < record["marker_before"]
    ]
    preservation_ready = [
        record
        for record in records
        if record["preservation"]
        and all(value in {"PASS", "NOT_PRESENT_IN_SOURCE"} for value in record["preservation"].values())
    ]
    pairwise_path = ROOT / "evals" / "benchmark" / "results" / "pairwise_development_20260910.yaml"
    pairwise_data = yaml.safe_load(pairwise_path.read_text(encoding="utf-8")) if pairwise_path.exists() else []
    register_span_path = ROOT / "evals" / "benchmark" / "results" / "register_span_001_result.md"
    register_span_text = register_span_path.read_text(encoding="utf-8") if register_span_path.exists() else ""
    observations = {
        "quality_reports": len(records),
        "compression_applicable_controls": len(applicable),
        "compression_pass_controls": sum(record["compression_gate"] == "PASS" for record in applicable),
        "marker_reduction_controls": len(marker_reduction),
        "preservation_ready_controls": len(preservation_ready),
        "pairwise_entries": len(pairwise_data) if isinstance(pairwise_data, list) else 0,
        "register_span_check": "PASS" if "通过" in register_span_text else "MISSING_OR_REVIEW",
        "preservation_dimensions": [
            "meaning",
            "argument",
            "author_position",
            "evidence",
            "nuance",
            "personal_voice",
        ],
    }
    locally_observed = {"orality", "logical_explicitness", "rhetorical_density", "reader_interaction"}
    parameter_decisions = [
        {
            "dimension": dimension,
            "before": value,
            "after": value,
            "evidence_level": "local" if dimension in locally_observed else "insufficient",
            "decision": "retain_until_cross_genre_human_review",
        }
        for dimension, value in INITIAL_PARAMETERS.items()
    ]
    artifact = {
        "profile_name": "modern-chinese-conversational",
        "base": "initial_default_profile",
        "iteration_date": str(date.today()),
        "evaluation_inputs": [
            "evals/benchmark/results/runs/*_quality.md",
            "evals/benchmark/results/pairwise_development_20260910.yaml",
            "evals/benchmark/results/register_span_001_result.md",
        ],
        "observations": observations,
        "before_parameters": INITIAL_PARAMETERS,
        "after_parameters": dict(INITIAL_PARAMETERS),
        "parameter_decisions": parameter_decisions,
        "calibration_actions": [
            "保留 logical_explicitness 8 与 rhetorical_density 4–5 的初始区间；首轮可用长文本只有 1 案，不能据此做全局数值漂移。",
            "将 Meaning、Argument、Author Position、Evidence、Nuance、Personal Voice 六项设为发布前硬闸门；Evidence 不在原文时必须显式标记 NOT_PRESENT_IN_SOURCE。",
            "将短控制文本标为 NOT_APPLICABLE_SHORT_CONTROL，不用负压缩率惩罚口径迁移；短文本仍只比较标记、主题和保真。",
            "Pairwise 与四角色结果继续作为 local development pre-screen，不升级为外部人工结论。",
        ],
        "boundary_notes": "10 案为项目自有控制文本，9 案短于压缩阈值；本轮校准只形成行为闸门与适用性规则，不把局部结果外推为所有体裁的数值最优。",
        "status": "contextual",
        "source_artifact": "",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"profile_iteration_{date.today():%Y%m%d}.yaml"
    artifact["source_artifact"] = str(out.relative_to(ROOT))
    out.write_text(yaml.safe_dump(artifact, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"style calibration: {len(records)} reports -> {out.relative_to(ROOT)}")
    print(f"applicable compression: {len(applicable)}, pass: {observations['compression_pass_controls']}")
    print(f"preservation-ready: {len(preservation_ready)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
