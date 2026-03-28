#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a compact workflow-health summary for human or agent consumption.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser.parse_args()


def read_workflow_health(project_root: Path) -> dict:
    path = project_root / ".mighty" / "workflow-health.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _fallback_next_action(payload: dict) -> tuple[str, str]:
    action = payload.get("recommended_next_action")
    reason = payload.get("recommended_reason")
    if isinstance(action, str) and action:
        return action, reason if isinstance(reason, str) else ""

    workflow_truth = payload.get("workflow_truth_status")
    quality_audit = payload.get("quality_audit_status")
    if workflow_truth != "pass":
        return "reconcile-workflow-artifacts", "workflow truth 未通过，先对齐 workflow_state 与实际 artifact。"
    if quality_audit != "pass":
        return "repair-review-artifacts", "review/close artifact 仍存在假阳性或空写回问题，应先修复质量产物。"
    return "none", "当前 workflow-health 未发现需要立即处理的阻断项。"


def render_workflow_health_markdown(project_root: Path) -> str:
    payload = read_workflow_health(project_root)
    next_action, next_reason = _fallback_next_action(payload)
    lines = [
        "## Workflow Health",
        f"- project: `{payload.get('project_title', '')}`",
        f"- quality-audit: `{payload.get('quality_audit_status', 'unknown')}`",
        f"- workflow-truth: `{payload.get('workflow_truth_status', 'unknown')}`",
        f"- setting-gate: `{payload.get('setting_gate_status', 'unknown')}`",
        f"- repo-owned tail: `{' -> '.join(payload.get('repo_owned_tail_steps', []))}`",
    ]

    missing = payload.get("workflow_truth_missing_artifacts", [])
    if isinstance(missing, list) and missing:
        lines.append(f"- missing-artifacts: `{', '.join(missing)}`")

    top_codes = payload.get("top_finding_codes", [])
    if isinstance(top_codes, list) and top_codes:
        lines.append(f"- top-findings: `{', '.join(top_codes)}`")

    has_guardrails = payload.get("has_recent_guardrails")
    if isinstance(has_guardrails, bool):
        lines.append(f"- recent-guardrails: `{'yes' if has_guardrails else 'no'}`")
    lines.append(f"- next-action: `{next_action}` ({next_reason})")

    return "\n".join(lines)


def render_workflow_health_status_block(project_root: Path) -> str:
    payload = read_workflow_health(project_root)
    next_action, next_reason = _fallback_next_action(payload)
    lines = [
        "### Workflow 健康",
        f"- workflow-truth: `{payload.get('workflow_truth_status', 'unknown')}`",
        f"- quality-audit: `{payload.get('quality_audit_status', 'unknown')}`",
        f"- repo-owned tail: `{' -> '.join(payload.get('repo_owned_tail_steps', []))}`",
    ]
    missing = payload.get("workflow_truth_missing_artifacts", [])
    if isinstance(missing, list) and missing:
        lines.append(f"- missing-artifacts: `{', '.join(missing)}`")
    top_codes = payload.get("top_finding_codes", [])
    if isinstance(top_codes, list) and top_codes:
        lines.append(f"- top-findings: `{', '.join(top_codes)}`")
    lines.append(f"- next-action: `{next_action}` ({next_reason})")
    return "\n".join(lines)


def render_workflow_health_query_answer(project_root: Path) -> str:
    payload = read_workflow_health(project_root)
    next_action, _ = _fallback_next_action(payload)
    parts = [
        f"workflow-health: workflow-truth=`{payload.get('workflow_truth_status', 'unknown')}`",
        f"quality-audit=`{payload.get('quality_audit_status', 'unknown')}`",
    ]
    missing = payload.get("workflow_truth_missing_artifacts", [])
    if isinstance(missing, list) and missing:
        parts.append(f"missing-artifacts=`{', '.join(missing)}`")
    top_codes = payload.get("top_finding_codes", [])
    if isinstance(top_codes, list) and top_codes:
        parts.append(f"top-findings=`{', '.join(top_codes)}`")
    parts.append(f"next-action=`{next_action}`")
    return ", ".join(parts)


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    if args.format == "json":
        print(json.dumps(read_workflow_health(root), ensure_ascii=False, indent=2))
        return
    print(render_workflow_health_markdown(root))


if __name__ == "__main__":
    main()
