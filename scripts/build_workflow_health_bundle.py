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

import audit_project_quality_state
import build_project_knowledge_projection
import sidecar_freshness


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a compact workflow-health bundle sidecar for agent and workflow consumption.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def top_finding_codes(audit: dict, limit: int = 3) -> list[str]:
    findings = audit.get("findings", [])
    if not isinstance(findings, list):
        return []
    out: list[str] = []
    for item in findings:
        if not isinstance(item, dict):
            continue
        code = item.get("code")
        if isinstance(code, str) and code and code not in out:
            out.append(code)
        if len(out) >= limit:
            break
    return out


def summarize_maintenance(report: dict) -> tuple[str, list[str]]:
    result = report.get("result", "unknown")
    steps = report.get("steps", [])
    failed: list[str] = []
    if isinstance(steps, list):
        for item in steps:
            if not isinstance(item, dict) or item.get("status") != "failed":
                continue
            cmd = item.get("cmd", [])
            if isinstance(cmd, list) and len(cmd) >= 2:
                failed.append(Path(cmd[1]).name)
    return result, failed


def recommend_next_action(*, workflow_truth_status: str, maintenance_result: str, quality_audit_status: str) -> tuple[str, str]:
    if workflow_truth_status != "pass":
        return (
            "reconcile-workflow-artifacts",
            "workflow truth 未通过，先对齐 workflow_state 与实际 artifact。",
        )
    if maintenance_result == "partial":
        return (
            "repair-maintenance-tail",
            "snapshot 之后的维护尾段存在失败步骤，应先修复尾段 sidecar 构建。",
        )
    if quality_audit_status != "pass":
        return (
            "repair-review-artifacts",
            "review/close artifact 仍存在假阳性或空写回问题，应先修复质量产物。",
        )
    return ("none", "当前 workflow-health 未发现需要立即处理的阻断项。")


def build_workflow_health_bundle(project_root: Path, *, timestamp: str) -> dict:
    repo_root = SCRIPT_DIR.parent
    mighty = project_root / ".mighty"
    projection_path = mighty / "knowledge-projection.json"
    audit_path = mighty / "quality-audit.json"
    maintenance_report_path = mighty / "maintenance-report.json"
    if projection_path.exists():
        projection = json.loads(projection_path.read_text(encoding="utf-8"))
    else:
        projection = build_project_knowledge_projection.build_project_knowledge_projection(project_root, timestamp=timestamp)
    if audit_path.exists():
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    else:
        audit = audit_project_quality_state.audit_project_quality_state(project_root)
    maintenance_report = json.loads(maintenance_report_path.read_text(encoding="utf-8")) if maintenance_report_path.exists() else {}
    workflow_truth_status = projection.get("workflow_truth", {}).get("status", "unknown")
    quality_audit_status = audit.get("status", "unknown")
    maintenance_result, failed_maintenance_steps = summarize_maintenance(maintenance_report)
    next_action, next_reason = recommend_next_action(
        workflow_truth_status=workflow_truth_status,
        maintenance_result=maintenance_result,
        quality_audit_status=quality_audit_status,
    )
    return {
        "version": "1.0",
        "generated_at": timestamp,
        "project_root": str(project_root),
        "project_title": projection.get("project_title", ""),
        "quality_audit_status": quality_audit_status,
        "top_finding_codes": top_finding_codes(audit),
        "workflow_truth_status": workflow_truth_status,
        "workflow_truth_missing_artifacts": projection.get("workflow_truth", {}).get("missing_artifacts", []),
        "maintenance_result": maintenance_result,
        "failed_maintenance_steps": failed_maintenance_steps,
        "repo_owned_tail_steps": projection.get("workflow_contract", {}).get("repo_owned_tail_steps", []),
        "setting_gate_status": projection.get("sidecar_health", {}).get("setting_gate_status", "unknown"),
        "has_recent_guardrails": projection.get("sidecar_health", {}).get("has_recent_guardrails", False),
        "recommended_next_action": next_action,
        "recommended_reason": next_reason,
        "freshness": sidecar_freshness.build_freshness(
            repo_root=repo_root,
            artifact_key="workflow-health",
            timestamp=timestamp,
            project_root=project_root,
            inputs={
                "quality-audit.json": {
                    "path": ".mighty/quality-audit.json",
                    "status": audit.get("status"),
                },
                "maintenance-report.json": {
                    "path": ".mighty/maintenance-report.json",
                    "result": maintenance_result,
                },
                "knowledge-projection.json": {
                    "path": ".mighty/knowledge-projection.json",
                    "workflow_truth_status": projection.get("workflow_truth", {}).get("status"),
                },
            },
        ),
    }


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    payload = build_workflow_health_bundle(root, timestamp=ts)
    if args.write:
        output_path = root / ".mighty" / "workflow-health.json"
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        payload["workflow_health_file"] = str(output_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
