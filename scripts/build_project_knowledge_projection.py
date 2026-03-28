#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import sidecar_freshness


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a compact project-local knowledge projection for agent consumption.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def count_reviewed_chapters(payload: dict) -> int:
    chapter_meta = payload.get("chapter_meta", {})
    if not isinstance(chapter_meta, dict):
        return 0
    return sum(1 for value in chapter_meta.values() if isinstance(value, dict) and value.get("review_score") is not None)


def count_active_hooks(state: dict) -> int:
    hooks = state.get("plot_threads", {}).get("foreshadowing", {}).get("active", [])
    return len(hooks) if isinstance(hooks, list) else 0


def build_workflow_truth(mighty: Path, workflow_state: dict) -> dict:
    current_task = workflow_state.get("current_task", {}) if isinstance(workflow_state.get("current_task"), dict) else {}
    args = current_task.get("args", {}) if isinstance(current_task.get("args"), dict) else {}
    claimed_status = current_task.get("status")
    claimed_checkpoint = current_task.get("last_successful_checkpoint")

    checks = {
        "active_context_exists": (mighty / "active-context.json").exists(),
        "memory_context_exists": (mighty / "memory-context.json").exists(),
        "quality_audit_exists": (mighty / "quality-audit.json").exists(),
        "content_positioning_exists": (mighty / "content-positioning.json").exists(),
        "maintenance_report_exists": Path(args["maintenance_report_file"]).exists()
        if isinstance(args.get("maintenance_report_file"), str) and args.get("maintenance_report_file")
        else False,
        "snapshot_file_exists": Path(args["snapshot_file"]).exists()
        if isinstance(args.get("snapshot_file"), str) and args.get("snapshot_file")
        else False,
    }

    missing_artifacts: list[str] = []
    if claimed_status == "completed" and claimed_checkpoint == "snapshot":
        for key, ok in checks.items():
            if not ok:
                missing_artifacts.append(key)

    status = "pass"
    if claimed_status == "completed" and claimed_checkpoint == "snapshot" and missing_artifacts:
        status = "fail"
    elif claimed_status:
        status = "pass" if not missing_artifacts else "warn"

    return {
        "status": status,
        "claimed_status": claimed_status,
        "claimed_checkpoint": claimed_checkpoint,
        "missing_artifacts": missing_artifacts,
        "checks": checks,
    }


def build_project_knowledge_projection(project_root: Path, *, timestamp: str) -> dict:
    mighty = project_root / ".mighty"
    repo_root = Path(__file__).resolve().parent.parent
    state = read_json(mighty / "state.json")
    state_archive = read_json(mighty / "state-archive.json")
    workflow_state = read_json(mighty / "workflow_state.json")
    setting_gate = read_json(mighty / "setting-gate.json")
    content_positioning = read_json(mighty / "content-positioning.json")
    learned_patterns = read_json(mighty / "learned-patterns.json")

    learned_data = learned_patterns.get("data", {}) if isinstance(learned_patterns.get("data"), dict) else learned_patterns
    recent_guardrails = learned_data.get("recent_guardrails", {}) if isinstance(learned_data, dict) else {}

    return {
        "version": "1.0",
        "generated_at": timestamp,
        "project_root": str(project_root),
        "project_title": state.get("meta", {}).get("title", ""),
        "truth_boundary": {
            "truth_source": "local_files",
            "repo_truth_layers": [
                "docs",
                "skills",
                "scripts",
                "projects/*/设定集",
                "projects/*/大纲",
                "projects/*/.mighty/*.json",
            ],
            "projection_role": "agent-readable summary only",
        },
        "workflow_contract": {
            "transaction_contract": workflow_state.get("transaction_contract", "chapter-transaction-v1"),
            "current_command": workflow_state.get("current_task", {}).get("command"),
            "current_status": workflow_state.get("current_task", {}).get("status"),
            "last_successful_checkpoint": workflow_state.get("current_task", {}).get("last_successful_checkpoint"),
            "repo_owned_tail_steps": ["maintenance", "snapshot"],
        },
        "workflow_truth": build_workflow_truth(mighty, workflow_state),
        "sidecar_health": {
            "setting_gate_status": setting_gate.get("status", "unknown"),
            "has_active_context": (mighty / "active-context.json").exists(),
            "active_context_last_built": state.get("active_context", {}).get("last_built"),
            "active_context_hook_count": state.get("active_context", {}).get("hook_count", 0),
            "active_context_guardrail_count": state.get("active_context", {}).get("guardrail_count", 0),
            "has_content_positioning": bool(content_positioning),
            "has_recent_guardrails": isinstance(recent_guardrails, dict) and bool(recent_guardrails),
            "recent_guardrails_expires_after_chapter": (
                recent_guardrails.get("expires_after_chapter")
                if isinstance(recent_guardrails, dict)
                else None
            ),
        },
        "story_index": {
            "current_chapter": state.get("progress", {}).get("current_chapter", 0),
            "active_hook_count": count_active_hooks(state),
            "live_reviewed_chapters": count_reviewed_chapters(state),
            "archived_reviewed_chapters": count_reviewed_chapters(state_archive),
        },
        "freshness": sidecar_freshness.build_freshness(
            repo_root=repo_root,
            artifact_key="knowledge-projection",
            timestamp=timestamp,
            project_root=project_root,
            inputs={
                "state.json": {
                    "path": ".mighty/state.json",
                    "current_chapter": state.get("progress", {}).get("current_chapter"),
                },
                "state-archive.json": {
                    "path": ".mighty/state-archive.json",
                    "reviewed_chapters": count_reviewed_chapters(state_archive),
                },
                "workflow_state.json": {
                    "path": ".mighty/workflow_state.json",
                    "last_successful_checkpoint": workflow_state.get("current_task", {}).get("last_successful_checkpoint"),
                },
                "setting-gate.json": {
                    "path": ".mighty/setting-gate.json",
                    "status": setting_gate.get("status"),
                },
                "content-positioning.json": {
                    "path": ".mighty/content-positioning.json",
                    "has_payload": bool(content_positioning),
                },
                "learned-patterns.json": {
                    "path": ".mighty/learned-patterns.json",
                    "has_recent_guardrails": isinstance(recent_guardrails, dict) and bool(recent_guardrails),
                },
            },
        ),
    }


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    payload = build_project_knowledge_projection(root, timestamp=ts)
    if args.write:
        output_path = root / ".mighty" / "knowledge-projection.json"
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        payload["knowledge_projection_file"] = str(output_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
