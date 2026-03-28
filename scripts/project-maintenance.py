#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from trace_log import append_trace
import workflow_state_utils


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return {
        "cmd": cmd,
        "stdout": proc.stdout.strip(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run post-write maintenance for a novel project")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--recent-chapters", type=int, default=8)
    parser.add_argument("--retain-recent-chapters", type=int, default=8)
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--workflow-trigger", default="maintenance")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    script_dir = SCRIPT_DIR

    steps = []
    steps.append(run([
        sys.executable,
        str(script_dir / "setting_gate.py"),
        str(root),
        "--stage",
        "write-post",
    ]))
    steps.append(run([
        sys.executable,
        str(script_dir / "sync-setting-assets.py"),
        str(root),
        "--mode",
        "all",
        "--recent-chapters",
        str(args.recent_chapters),
    ]))
    steps.append(run([
        sys.executable,
        str(script_dir / "split-runtime-guidance.py"),
        str(root),
        "--timestamp",
        ts,
    ]))
    steps.append(run([
        sys.executable,
        str(script_dir / "build_active_context.py"),
        str(root),
        "--timestamp",
        ts,
    ]))
    steps.append(run([
        sys.executable,
        str(script_dir / "thin-state.py"),
        str(root),
        "--retain-recent-chapters",
        str(args.retain_recent_chapters),
        "--timestamp",
        ts,
    ]))
    snapshot_step = run([
        sys.executable,
        str(script_dir / "generate_snapshot.py"),
        str(root),
        "--timestamp",
        ts,
    ])
    steps.append(snapshot_step)
    report_path = root / ".mighty" / "maintenance-report.json"
    snapshot_payload = json.loads(snapshot_step["stdout"])
    workflow_state = workflow_state_utils.mark_snapshot_complete(
        project_root=root,
        repo_root=script_dir.parent,
        timestamp=ts,
        command="project-maintenance",
        trigger=args.workflow_trigger,
        report_file=str(report_path),
        snapshot_file=snapshot_payload["filesystem_snapshot_file"],
    )
    memory_context_step = run([
        sys.executable,
        str(script_dir / "build_memory_context.py"),
        str(root),
        "--timestamp",
        ts,
    ])
    steps.append(memory_context_step)
    quality_audit_step = run([
        sys.executable,
        str(script_dir / "audit_project_quality_state.py"),
        str(root),
        "--write",
    ])
    steps.append(quality_audit_step)
    content_positioning_step = run([
        sys.executable,
        str(script_dir / "build_content_positioning.py"),
        str(root),
        "--timestamp",
        ts,
    ])
    steps.append(content_positioning_step)
    knowledge_projection_step = run([
        sys.executable,
        str(script_dir / "build_project_knowledge_projection.py"),
        str(root),
        "--timestamp",
        ts,
        "--write",
    ])
    steps.append(knowledge_projection_step)

    report = {
        "project": str(root),
        "run_at": ts,
        "transaction_contract": "chapter-transaction-v1",
        "transaction_phase": "snapshot",
        "next_transaction_step": None,
        "steps": steps,
    }
    report_path = root / ".mighty" / "maintenance-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    trace_log_path = append_trace(
        root,
        event="maintenance.completed",
        skill="project-maintenance",
        result="success",
        details={
            "trigger": args.workflow_trigger,
            "report_file": str(report_path),
            "snapshot_file": snapshot_payload["filesystem_snapshot_file"],
        },
        timestamp=ts,
    )
    print(json.dumps({
        "project": str(root),
        "report_file": str(report_path),
        "workflow_state_file": str(workflow_state_utils.workflow_state_path(root)),
        "transaction_contract": "chapter-transaction-v1",
        "trace_log_file": str(trace_log_path),
        "transaction_phase": "snapshot",
        "next_transaction_step": None,
        "workflow_current_step": workflow_state["current_task"]["current_step"],
        "last_successful_checkpoint": workflow_state["current_task"]["last_successful_checkpoint"],
        "workflow_status": workflow_state["current_task"]["status"],
        "steps": [Path(step["cmd"][1]).name for step in steps],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
