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
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return {
        "cmd": cmd,
        "stdout": proc.stdout.strip(),
    }


def run_step(cmd: list[str], *, allow_failure: bool = False) -> dict:
    try:
        result = run(cmd)
        result["status"] = "success"
        return result
    except Exception as exc:
        if not allow_failure:
            raise
        return {
            "cmd": cmd,
            "stdout": "",
            "status": "failed",
            "error": str(exc),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run post-write maintenance for a novel project"
    )
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

    existing_workflow_state = workflow_state_utils.load_existing_workflow_state(root)
    if existing_workflow_state is not None:
        workflow_state_utils.assert_repo_owned_tail_ready(
            existing_workflow_state.get("current_task")
        )

    steps = []
    steps.append(run_step([
        sys.executable,
        str(script_dir / "setting_gate.py"),
        str(root),
        "--stage",
        "write-post",
    ]))
    steps.append(run_step([
        sys.executable,
        str(script_dir / "sync-setting-assets.py"),
        str(root),
        "--mode",
        "all",
        "--recent-chapters",
        str(args.recent_chapters),
    ]))
    steps.append(run_step([
        sys.executable,
        str(script_dir / "split-runtime-guidance.py"),
        str(root),
        "--timestamp",
        ts,
    ]))
    steps.append(run_step([
        sys.executable,
        str(script_dir / "build_active_context.py"),
        str(root),
        "--timestamp",
        ts,
    ]))
    steps.append(run_step([
        sys.executable,
        str(script_dir / "thin-state.py"),
        str(root),
        "--retain-recent-chapters",
        str(args.retain_recent_chapters),
        "--timestamp",
        ts,
    ]))
    snapshot_step = run_step([
        sys.executable,
        str(script_dir / "generate_snapshot.py"),
        str(root),
        "--timestamp",
        ts,
    ])
    steps.append(snapshot_step)
    report_path = root / ".mighty" / "maintenance-report.json"
    snapshot_payload = json.loads(snapshot_step["stdout"])

    def write_report(result: str, *, error: str | None = None) -> None:
        report = {
            "project": str(root),
            "run_at": ts,
            "result": result,
            "transaction_contract": "chapter-transaction-v1",
            "transaction_phase": "snapshot",
            "next_transaction_step": None,
            "steps": steps,
        }
        if error is not None:
            report["error"] = error
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def current_result_state() -> str:
        return (
            "partial"
            if any(step.get("status") == "failed" for step in steps)
            else "success"
        )

    write_report("running")

    try:
        workflow_state = workflow_state_utils.mark_snapshot_complete(
            project_root=root,
            repo_root=script_dir.parent,
            timestamp=ts,
            command="project-maintenance",
            trigger=args.workflow_trigger,
            report_file=str(report_path),
            snapshot_file=snapshot_payload["filesystem_snapshot_file"],
        )
    except Exception as exc:
        write_report("failed", error=str(exc))
        raise
    memory_context_step = run_step(
        [
            sys.executable,
            str(script_dir / "build_memory_context.py"),
            str(root),
            "--timestamp",
            ts,
        ],
        allow_failure=True,
    )
    steps.append(memory_context_step)
    memory_sync_step = run_step(
        [
            sys.executable,
            str(script_dir / "sync_memory_context_to_openmemory.py"),
            str(root),
            "--timestamp",
            ts,
        ],
        allow_failure=True,
    )
    steps.append(memory_sync_step)
    memory_summary_step = run_step(
        [
            sys.executable,
            str(script_dir / "render_memory_context_summary.py"),
            str(root),
            "--timestamp",
            ts,
            "--skip-refresh-memory-context",
            "--sync-openmemory",
            "off",
        ],
        allow_failure=True,
    )
    steps.append(memory_summary_step)
    quality_audit_step = run_step(
        [
            sys.executable,
            str(script_dir / "audit_project_quality_state.py"),
            str(root),
            "--write",
        ],
        allow_failure=True,
    )
    steps.append(quality_audit_step)
    content_positioning_step = run_step([
        sys.executable,
        str(script_dir / "build_content_positioning.py"),
        str(root),
        "--timestamp",
        ts,
    ], allow_failure=True)
    steps.append(content_positioning_step)

    result_state = current_result_state()
    write_report(result_state)

    knowledge_projection_step = run_step(
        [
            sys.executable,
            str(script_dir / "build_project_knowledge_projection.py"),
            str(root),
            "--timestamp",
            ts,
            "--write",
        ],
        allow_failure=True,
    )
    steps.append(knowledge_projection_step)
    result_state = current_result_state()
    write_report(result_state)

    workflow_health_step = run_step(
        [
            sys.executable,
            str(script_dir / "build_workflow_health_bundle.py"),
            str(root),
            "--timestamp",
            ts,
            "--write",
        ],
        allow_failure=True,
    )
    steps.append(workflow_health_step)

    result_state = current_result_state()
    write_report(result_state)

    memory_sync_report_path = root / ".mighty" / "memory-sync-report.json"
    memory_sync_report = (
        json.loads(memory_sync_report_path.read_text(encoding="utf-8"))
        if memory_sync_report_path.exists()
        else {}
    )
    trace_log_path = append_trace(
        root,
        event="maintenance.completed",
        skill="project-maintenance",
        result=result_state,
        details={
            "trigger": args.workflow_trigger,
            "report_file": str(report_path),
            "snapshot_file": snapshot_payload["filesystem_snapshot_file"],
        },
        timestamp=ts,
    )
    print(
        json.dumps(
            {
                "project": str(root),
                "report_file": str(report_path),
                "workflow_state_file": str(
                    workflow_state_utils.workflow_state_path(root)
                ),
                "transaction_contract": "chapter-transaction-v1",
                "trace_log_file": str(trace_log_path),
                "result": result_state,
                "transaction_phase": "snapshot",
                "next_transaction_step": None,
                "workflow_current_step": workflow_state["current_task"][
                    "current_step"
                ],
                "last_successful_checkpoint": workflow_state["current_task"][
                    "last_successful_checkpoint"
                ],
                "workflow_status": workflow_state["current_task"]["status"],
                "memory_sync_report_file": (
                    str(memory_sync_report_path)
                    if memory_sync_report_path.exists()
                    else None
                ),
                "memory_sync_status": memory_sync_report.get("status"),
                "steps": [Path(step["cmd"][1]).name for step in steps],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
