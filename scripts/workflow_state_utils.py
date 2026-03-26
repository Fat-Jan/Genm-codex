from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


TRANSACTION_STEPS = ["gate-check", "draft", "close", "maintenance", "snapshot"]


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def workflow_state_path(project_root: Path) -> Path:
    return project_root / ".mighty" / "workflow_state.json"


def template_path(repo_root: Path) -> Path:
    return repo_root / "shared" / "templates" / "workflow-state-v2.json"


def load_or_initialize_workflow_state(project_root: Path, repo_root: Path) -> dict:
    existing = load_json(workflow_state_path(project_root))
    if isinstance(existing, dict):
        payload = deepcopy(existing)
    else:
        payload = deepcopy(load_json(template_path(repo_root)) or {})
        payload.setdefault("version", "2.0")
        payload.setdefault("transaction_contract", "chapter-transaction-v1")
        payload.setdefault("current_task", None)
        payload.setdefault("history", [])
    payload.setdefault("history", [])
    payload.setdefault("transaction_contract", "chapter-transaction-v1")
    return payload


def ensure_current_task(payload: dict, *, command: str, args: dict, timestamp: str) -> dict:
    current_task = payload.get("current_task")
    if not isinstance(current_task, dict):
        current_task = {
            "command": command,
            "args": args,
            "status": "running",
            "current_step": "maintenance",
            "completed_steps": [],
            "failed_steps": [],
            "pending_steps": ["maintenance", "snapshot"],
            "last_successful_checkpoint": None,
            "started_at": timestamp,
            "last_heartbeat": timestamp,
            "error_message": None,
        }
        payload["current_task"] = current_task
    else:
        current_task.setdefault("command", command)
        current_task.setdefault("args", args)
        current_task.setdefault("status", "running")
        current_task.setdefault("current_step", "maintenance")
        current_task.setdefault("completed_steps", [])
        current_task.setdefault("failed_steps", [])
        current_task.setdefault("pending_steps", TRANSACTION_STEPS.copy())
        current_task.setdefault("last_successful_checkpoint", None)
        current_task.setdefault("started_at", timestamp)
        current_task.setdefault("last_heartbeat", timestamp)
        current_task.setdefault("error_message", None)
        if not isinstance(current_task.get("args"), dict):
            current_task["args"] = args
    return current_task


def mark_maintenance_complete(
    *,
    project_root: Path,
    repo_root: Path,
    timestamp: str,
    command: str,
    trigger: str,
    report_file: str,
) -> dict:
    payload = load_or_initialize_workflow_state(project_root, repo_root)
    current_task = ensure_current_task(
        payload,
        command=command,
        args={"trigger": trigger},
        timestamp=timestamp,
    )

    current_task["status"] = "running"
    current_task["last_heartbeat"] = timestamp
    current_task["error_message"] = None
    current_task["args"]["trigger"] = trigger
    current_task["args"]["maintenance_report_file"] = report_file

    completed_steps = [step for step in current_task.get("completed_steps", []) if step != "maintenance"]
    completed_steps.append("maintenance")
    current_task["completed_steps"] = [step for step in TRANSACTION_STEPS if step in completed_steps]

    failed_steps = [step for step in current_task.get("failed_steps", []) if step != "maintenance"]
    current_task["failed_steps"] = failed_steps

    pending_steps = [step for step in current_task.get("pending_steps", []) if step != "maintenance"]
    if "snapshot" not in pending_steps:
        pending_steps.append("snapshot")
    current_task["pending_steps"] = [step for step in TRANSACTION_STEPS if step in pending_steps]

    current_task["current_step"] = "snapshot"
    current_task["last_successful_checkpoint"] = "maintenance"
    current_task["transaction_phase"] = "snapshot"
    current_task["next_transaction_step"] = "snapshot"
    current_task["maintenance_completed_at"] = timestamp

    save_json(workflow_state_path(project_root), payload)
    return payload


def mark_snapshot_complete(
    *,
    project_root: Path,
    repo_root: Path,
    timestamp: str,
    command: str,
    trigger: str,
    report_file: str,
    snapshot_file: str,
) -> dict:
    payload = load_or_initialize_workflow_state(project_root, repo_root)
    current_task = ensure_current_task(
        payload,
        command=command,
        args={"trigger": trigger},
        timestamp=timestamp,
    )

    current_task["status"] = "completed"
    current_task["last_heartbeat"] = timestamp
    current_task["error_message"] = None
    current_task["args"]["trigger"] = trigger
    current_task["args"]["maintenance_report_file"] = report_file
    current_task["args"]["snapshot_file"] = snapshot_file

    completed_steps = set(current_task.get("completed_steps", []))
    completed_steps.update(TRANSACTION_STEPS)
    current_task["completed_steps"] = [step for step in TRANSACTION_STEPS if step in completed_steps]
    current_task["failed_steps"] = [step for step in current_task.get("failed_steps", []) if step not in {"maintenance", "snapshot"}]
    current_task["pending_steps"] = []
    current_task["current_step"] = None
    current_task["last_successful_checkpoint"] = "snapshot"
    current_task["transaction_phase"] = "completed"
    current_task["next_transaction_step"] = None
    current_task["snapshot_completed_at"] = timestamp

    save_json(workflow_state_path(project_root), payload)
    return payload
