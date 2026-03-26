#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from trace_log import append_trace


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a safe project-local memory context for MCP sync.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--timestamp", default="")
    return parser.parse_args(argv)


def build_memory_context(project_root: Path, *, timestamp: str) -> dict[str, Any]:
    mighty = project_root / ".mighty"
    state = read_json(mighty / "state.json")
    gate = read_json(mighty / "setting-gate.json")
    workflow = read_json(mighty / "workflow_state.json")
    active_context = read_json(mighty / "active-context.json")

    workflow_task = workflow.get("current_task", {}) if isinstance(workflow.get("current_task"), dict) else {}
    active_summary = active_context.get("summary_window", {}) if isinstance(active_context.get("summary_window"), dict) else {}

    return {
        "version": "1.0",
        "generated_at": timestamp,
        "safe_for_mcp_memory": True,
        "project_root": str(project_root),
        "title": state.get("meta", {}).get("title", ""),
        "current_chapter": state.get("progress", {}).get("current_chapter", 0),
        "total_words": state.get("progress", {}).get("total_words", 0),
        "workflow": {
            "status": workflow_task.get("status"),
            "current_step": workflow_task.get("current_step"),
            "last_successful_checkpoint": workflow_task.get("last_successful_checkpoint"),
        },
        "gate": {
            "status": gate.get("status"),
            "blocking_gap_keys": [item.get("key") for item in gate.get("blocking_gaps", []) if isinstance(item, dict)],
            "minimal_next_action": gate.get("minimal_next_action", {}).get("action"),
            "minimal_next_reason": gate.get("minimal_next_action", {}).get("reason"),
        },
        "launch_stack": {
            "phase": state.get("launch_stack_phase", ""),
            "drift_signal": state.get("launch_stack_drift_signal", "none"),
        },
        "active_context_summary": {
            "hook_count": state.get("active_context", {}).get("hook_count", 0),
            "guardrail_count": state.get("active_context", {}).get("guardrail_count", 0),
            "latest_summary_chapter": active_summary.get("latest_chapter"),
        },
        "memory_contract": {
            "truth_source": "local_files",
            "allowed_sync": [
                "workflow_summary",
                "gate_summary",
                "launch_stack_drift",
                "active_context_summary",
                "next_action_hint",
            ],
            "forbidden_sync": [
                "full_state_json",
                "chapter_prose",
                "sidecar_full_bodies",
                "setting_markdown_fulltext",
            ],
        },
    }


def main(argv: list[str] | None = None) -> dict[str, Any]:
    args = parse_args(argv)
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    payload = build_memory_context(root, timestamp=ts)
    output_path = root / ".mighty" / "memory-context.json"
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path = append_trace(
        root,
        event="memory_context.built",
        skill="build_memory_context",
        result="success",
        details={"output_file": str(output_path)},
        timestamp=ts,
    )
    result = {
        "project": str(root),
        "memory_context_file": str(output_path),
        "trace_log_file": str(log_path),
        "safe_for_mcp_memory": True,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
