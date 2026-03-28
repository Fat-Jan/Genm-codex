#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a compact project scan summary for MCP and status/query consumers.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser.parse_args()


def read_json_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_project_scan_summary(project_root: Path) -> dict:
    mighty = project_root / ".mighty"
    market_data = read_json_if_exists(mighty / "market-data.json")
    market_adjustments = read_json_if_exists(mighty / "market-adjustments.json")
    research_candidates = read_json_if_exists(mighty / "research-candidates.json")

    recommended_buckets = market_data.get("findings", {}).get("recommended_content_buckets", [])
    top_bucket = ""
    if isinstance(recommended_buckets, list) and recommended_buckets:
        first = recommended_buckets[0]
        if isinstance(first, dict):
            top_bucket = str(first.get("bucket_name") or "")

    hot_tags = market_data.get("findings", {}).get("hot_tags", [])
    top_tag = ""
    if isinstance(hot_tags, list) and hot_tags:
        first = hot_tags[0]
        if isinstance(first, dict):
            top_tag = str(first.get("tag") or "")

    adjustments = market_adjustments.get("adjustments", [])
    adjustment_ids: list[str] = []
    if isinstance(adjustments, list):
        for item in adjustments:
            if not isinstance(item, dict):
                continue
            adjustment_id = item.get("id")
            if isinstance(adjustment_id, str) and adjustment_id:
                adjustment_ids.append(adjustment_id)

    candidates = research_candidates.get("candidates", [])
    candidate_names: list[str] = []
    if isinstance(candidates, list):
        for item in candidates:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            if isinstance(name, str) and name:
                candidate_names.append(name)

    confidence = market_data.get("confidence", {})
    confidence_level = confidence.get("overall", "unknown") if isinstance(confidence, dict) else "unknown"

    return {
        "scan_mode": market_data.get("mode", "unknown"),
        "report_kind": market_data.get("report_kind", "unknown"),
        "confidence": confidence_level,
        "top_bucket": top_bucket,
        "top_tag": top_tag,
        "adjustment_ids": adjustment_ids,
        "research_candidates": candidate_names,
        "source_count": len(market_data.get("sources", [])) if isinstance(market_data.get("sources", []), list) else 0,
    }


def render_project_scan_summary_markdown(project_root: Path) -> str:
    payload = build_project_scan_summary(project_root)
    lines = [
        "## Project Scan Summary",
        f"- scan-mode: `{payload['scan_mode']}`",
        f"- report-kind: `{payload['report_kind']}`",
        f"- confidence: `{payload['confidence']}`",
        f"- source-count: `{payload['source_count']}`",
    ]
    if payload["top_bucket"]:
        lines.append(f"- top-bucket: `{payload['top_bucket']}`")
    if payload["top_tag"]:
        lines.append(f"- top-tag: `{payload['top_tag']}`")
    if payload["adjustment_ids"]:
        lines.append(f"- adjustments: `{', '.join(payload['adjustment_ids'])}`")
    if payload["research_candidates"]:
        lines.append(f"- research-candidates: `{', '.join(payload['research_candidates'])}`")
    return "\n".join(lines)


def render_project_scan_query_answer(project_root: Path) -> str:
    payload = build_project_scan_summary(project_root)
    parts = [
        "scan-summary",
        f"mode=`{payload['scan_mode']}`",
        f"confidence=`{payload['confidence']}`",
    ]
    if payload["top_bucket"]:
        parts.append(f"top-bucket=`{payload['top_bucket']}`")
    if payload["adjustment_ids"]:
        parts.append(f"adjustments=`{','.join(payload['adjustment_ids'])}`")
    return ", ".join(parts)


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    if args.format == "json":
        print(json.dumps(build_project_scan_summary(root), ensure_ascii=False, indent=2))
        return
    print(render_project_scan_summary_markdown(root))


if __name__ == "__main__":
    main()
