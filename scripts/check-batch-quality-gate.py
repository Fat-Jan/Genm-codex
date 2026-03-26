#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import strong_quality_gate


SAFE_MAX_BATCH = 3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether a generated chapter batch still looks like full prose rather than compressed outline prose.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--batch-count", type=int)
    parser.add_argument("--last-n", type=int, default=3)
    parser.add_argument("--write-report", action="store_true")
    return parser.parse_args()


def read_state(project_root: Path) -> dict:
    return json.loads((project_root / ".mighty" / "state.json").read_text())


def load_length_policy() -> dict:
    return strong_quality_gate.load_policy()


def chapter_range(state: dict, args: argparse.Namespace) -> tuple[list[int], int]:
    current = int(state["progress"]["current_chapter"])
    if args.start and args.end:
        nums = list(range(args.start, args.end + 1))
    elif args.batch_count:
        nums = list(range(max(1, current - args.batch_count + 1), current + 1))
    else:
        nums = list(range(max(1, current - args.last_n + 1), current + 1))
    batch_count = args.batch_count or len(nums)
    return nums, batch_count


def collect_metrics(project_root: Path, nums: list[int]) -> list[dict]:
    result = []
    for num in nums:
        path = project_root / "chapters" / f"第{num:03d}章.md"
        if not path.exists():
            continue
        text = path.read_text()
        lines = text.count("\n") + 1
        chars = len(text)
        dialogue = text.count("“")
        bullet_lines = sum(1 for line in text.splitlines() if line.lstrip().startswith(("-", "*")))
        result.append({
            "chapter": num,
            "chars": chars,
            "lines": lines,
            "dialogue_marks": dialogue,
            "bullet_lines": bullet_lines,
            "text": text,
        })
    return result


def prior_baseline(project_root: Path, start: int, window: int = 3) -> float | None:
    nums = list(range(max(1, start - window), start))
    vals = []
    for num in nums:
        path = project_root / "chapters" / f"第{num:03d}章.md"
        if path.exists():
            vals.append(len(path.read_text()))
    if not vals:
        return None
    return sum(vals) / len(vals)


def current_length_policy(state: dict, policy: dict) -> dict:
    return strong_quality_gate.resolve_length_policy(state, policy)


def evaluate(state: dict, metrics: list[dict], batch_count: int, baseline: float | None, policy: dict) -> dict:
    issues = []
    warnings = []
    length_policy = current_length_policy(state, policy)
    hard_min = int(length_policy["hard_min_chars"])
    soft_min = int(length_policy["soft_min_chars"])
    preferred_max = int(length_policy["preferred_max_chars"])
    shrinkage_policy = policy.get("post_write_gate", {}).get("shrinkage", {})
    compressed_threshold = max(
        int(shrinkage_policy.get("compressed_floor_chars", 900) or 900),
        int(hard_min * float(shrinkage_policy.get("compressed_ratio_of_hard_min", 0.85) or 0.85)),
    )

    if batch_count > SAFE_MAX_BATCH:
        issues.append({
            "code": "batch-too-large",
            "message": f"一次性批量生成 {batch_count} 章，超过安全上限 {SAFE_MAX_BATCH} 章。",
        })

    short_run = 0
    for item in metrics:
        gate_result = strong_quality_gate.evaluate_post_write_gate(
            state=state,
            chapter_text=item["text"],
            baseline_avg_chars=baseline,
            policy=policy,
            chapter_number=item["chapter"],
        )
        issues.extend(gate_result["issues"])
        warnings.extend(gate_result["warnings"])
        if item["chars"] < compressed_threshold:
            short_run += 1
        else:
            short_run = 0
        if short_run >= 2:
            issues.append({
                "code": "summary-like-run",
                "chapter": item["chapter"],
                "message": "连续两章以上明显过短，已接近剧情摘要/提纲化风险。",
            })
        if item["dialogue_marks"] == 0 and item["chars"] < soft_min:
            warnings.append({
                "code": "low-scene-density",
                "chapter": item["chapter"],
                "message": f"第{item['chapter']:03d}章对话/场景密度过低，需警惕概述化。",
            })
        if item["bullet_lines"] >= 2:
            warnings.append({
                "code": "bullet-like-structure",
                "chapter": item["chapter"],
                "message": f"第{item['chapter']:03d}章出现较多列表式结构，需确认是否已偏向摘要态。",
            })

        if item["chars"] > preferred_max * 1.35:
            warnings.append({
                "code": "chapter-too-bloated",
                "chapter": item["chapter"],
                "message": f"第{item['chapter']:03d}章显著高于推荐上限 {preferred_max}，需警惕注水或单章过满。",
            })

    if issues:
        status = "fail"
        recommendation = f"把批量生成拆成最多 {SAFE_MAX_BATCH} 章一批，并在每批后强制 review / 质量门检查。"
    elif warnings:
        status = "warn"
        recommendation = f"当前批次未直接失败，但建议后续仍保持每批最多 {SAFE_MAX_BATCH} 章。"
    else:
        status = "pass"
        recommendation = f"当前批次通过质量门，但后续仍建议一次性最多 {SAFE_MAX_BATCH} 章。"

    return {
        "status": status,
        "safe_max_batch": SAFE_MAX_BATCH,
        "length_policy": length_policy,
        "issues": issues,
        "warnings": warnings,
        "recommendation": recommendation,
    }


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    state = read_state(root)
    policy = load_length_policy()
    length_policy = current_length_policy(state, policy)
    nums, batch_count = chapter_range(state, args)
    metrics = collect_metrics(root, nums)
    baseline = prior_baseline(root, nums[0]) if nums else None
    result = {
        "project": str(root),
        "chapters": nums,
        "batch_count": batch_count,
        "baseline_avg_chars": baseline,
        "metrics": [{k: v for k, v in item.items() if k != "text"} for item in metrics],
    }
    result.update(evaluate(state, metrics, batch_count, baseline, policy))

    if args.write_report:
        report_path = root / ".mighty" / "batch-quality-gate.json"
        report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        result["report_file"] = str(report_path)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
