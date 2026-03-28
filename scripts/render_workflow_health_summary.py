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


def render_workflow_health_markdown(project_root: Path) -> str:
    payload = read_workflow_health(project_root)
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

    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    if args.format == "json":
        print(json.dumps(read_workflow_health(root), ensure_ascii=False, indent=2))
        return
    print(render_workflow_health_markdown(root))


if __name__ == "__main__":
    main()
