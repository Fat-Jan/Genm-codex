#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_workflow_health_summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a compact project status dashboard for status/query and MCP consumers.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser.parse_args()


def read_json_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_project_status_dashboard(project_root: Path) -> dict:
    mighty = project_root / ".mighty"
    state = read_json_if_exists(mighty / "state.json")
    workflow_health = read_json_if_exists(mighty / "workflow-health.json")
    setting_gate = read_json_if_exists(mighty / "setting-gate.json")
    active_context = read_json_if_exists(mighty / "active-context.json")

    meta = state.get("meta", {}) if isinstance(state.get("meta"), dict) else {}
    progress = state.get("progress", {}) if isinstance(state.get("progress"), dict) else {}
    active_context_fallback = state.get("active_context", {}) if isinstance(state.get("active_context"), dict) else {}
    active_context = active_context or active_context_fallback

    minimal_next_action = setting_gate.get("minimal_next_action", {}) if isinstance(setting_gate.get("minimal_next_action"), dict) else {}

    return {
        "project_title": meta.get("title", ""),
        "platform": meta.get("platform", ""),
        "current_chapter": progress.get("current_chapter", 0),
        "total_words": progress.get("total_words", 0),
        "workflow_health": workflow_health,
        "setting_gate": {
            "status": setting_gate.get("status", "unknown"),
            "blocking_gaps": setting_gate.get("blocking_gaps", []),
            "review_items": setting_gate.get("review_items", []),
            "minimal_next_action_summary": minimal_next_action.get("summary", ""),
            "suggested_commands": minimal_next_action.get("suggested_commands", []),
        },
        "current_writing_slice": {
            "last_built": active_context.get("last_built"),
            "latest_chapter": (
                active_context.get("summary_window", {}).get("latest_chapter")
                if isinstance(active_context.get("summary_window"), dict)
                else None
            ),
            "hook_count": active_context.get("hook_count", 0),
            "guardrail_count": active_context.get("guardrail_count", 0),
        },
    }


def render_project_status_dashboard_markdown(project_root: Path) -> str:
    payload = build_project_status_dashboard(project_root)
    workflow_block = render_workflow_health_summary.render_workflow_health_status_block(project_root)
    gate = payload["setting_gate"]
    current = payload["current_writing_slice"]

    lines = [
        "## Project Status Dashboard",
        f"- project: `{payload['project_title']}`",
        f"- platform: `{payload['platform'] or 'unknown'}`",
        f"- current-chapter: `{payload['current_chapter']}`",
        f"- total-words: `{payload['total_words']}`",
        "",
        workflow_block,
        "",
        "### Setting Gate",
        f"- status: `{gate['status']}`",
    ]

    blocking_gaps = gate.get("blocking_gaps", [])
    if isinstance(blocking_gaps, list) and blocking_gaps:
        lines.append(f"- blocking-gaps: `{', '.join(str(item) for item in blocking_gaps)}`")
    review_items = gate.get("review_items", [])
    if isinstance(review_items, list) and review_items:
        lines.append(f"- review-items: `{', '.join(str(item) for item in review_items)}`")
    next_action_summary = gate.get("minimal_next_action_summary")
    if isinstance(next_action_summary, str) and next_action_summary:
        lines.append(f"- next-action: `{next_action_summary}`")
    suggested_commands = gate.get("suggested_commands", [])
    if isinstance(suggested_commands, list) and suggested_commands:
        lines.append(f"- suggested-commands: `{'; '.join(str(item) for item in suggested_commands)}`")

    lines.extend(
        [
            "",
            "### Current Writing Slice",
            f"- last-built: `{current['last_built'] or 'unknown'}`",
            f"- latest-chapter: `{current['latest_chapter']}`",
            f"- hook-count: `{current['hook_count']}`",
            f"- guardrail-count: `{current['guardrail_count']}`",
        ]
    )
    return "\n".join(lines)


def render_project_status_query_answer(project_root: Path) -> str:
    payload = build_project_status_dashboard(project_root)
    workflow = payload["workflow_health"]
    gate = payload["setting_gate"]
    return ", ".join(
        [
            f"project-status: chapter=`{payload['current_chapter']}`",
            f"workflow-truth=`{workflow.get('workflow_truth_status', 'unknown')}`",
            f"quality-audit=`{workflow.get('quality_audit_status', 'unknown')}`",
            f"workflow-action=`{workflow.get('recommended_next_action', 'none')}`",
            f"gate=`{gate.get('status', 'unknown')}`",
        ]
    )


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    if args.format == "json":
        print(json.dumps(build_project_status_dashboard(root), ensure_ascii=False, indent=2))
        return
    print(render_project_status_dashboard_markdown(root))


if __name__ == "__main__":
    main()
