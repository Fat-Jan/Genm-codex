#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


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


def min_chars_threshold(state: dict) -> int:
    platform = state.get("meta", {}).get("platform")
    target_chapters = int(state.get("meta", {}).get("target_chapters") or 0)
    if platform == "番茄" and target_chapters >= 10:
        return 1500
    return 900


def evaluate(state: dict, metrics: list[dict], batch_count: int, baseline: float | None) -> dict:
    issues = []
    warnings = []
    min_chars = min_chars_threshold(state)

    if batch_count > SAFE_MAX_BATCH:
        issues.append({
            "code": "batch-too-large",
            "message": f"一次性批量生成 {batch_count} 章，超过安全上限 {SAFE_MAX_BATCH} 章。",
        })

    short_run = 0
    for item in metrics:
        if item["chars"] < min_chars:
            issues.append({
                "code": "chapter-too-short",
                "chapter": item["chapter"],
                "message": f"第{item['chapter']:03d}章仅 {item['chars']} 字符，低于当前安全阈值 {min_chars}。",
            })
        if baseline and item["chars"] < baseline * 0.55:
            issues.append({
                "code": "sharp-length-drop",
                "chapter": item["chapter"],
                "message": f"第{item['chapter']:03d}章长度相对前序基线跌破 55%，疑似提纲化压缩。",
            })
        if item["chars"] < 1200:
            short_run += 1
        else:
            short_run = 0
        if short_run >= 2:
            issues.append({
                "code": "summary-like-run",
                "chapter": item["chapter"],
                "message": "连续两章以上明显过短，已接近剧情摘要/提纲化风险。",
            })
        if item["dialogue_marks"] == 0 and item["chars"] < 1500:
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
        "issues": issues,
        "warnings": warnings,
        "recommendation": recommendation,
    }


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    state = read_state(root)
    nums, batch_count = chapter_range(state, args)
    metrics = collect_metrics(root, nums)
    baseline = prior_baseline(root, nums[0]) if nums else None
    result = {
        "project": str(root),
        "chapters": nums,
        "batch_count": batch_count,
        "baseline_avg_chars": baseline,
        "metrics": metrics,
    }
    result.update(evaluate(state, metrics, batch_count, baseline))

    if args.write_report:
        report_path = root / ".mighty" / "batch-quality-gate.json"
        report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        result["report_file"] = str(report_path)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
