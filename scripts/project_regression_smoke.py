#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_project_quality_state
import audit_chapter_structure_repetition
import audit_precheck_structure_risks
import build_project_knowledge_projection
import build_workflow_health_bundle


def load_batch_gate_module():
    module_path = SCRIPT_DIR / "check-batch-quality-gate.py"
    spec = importlib.util.spec_from_file_location("check_batch_quality_gate", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a read-only regression smoke for workflow-health related project artifacts.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--batch-count", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    quality_audit = audit_project_quality_state.audit_project_quality_state(root)
    knowledge_projection = build_project_knowledge_projection.build_project_knowledge_projection(
        root,
        timestamp=build_project_knowledge_projection.now_iso(),
    )
    workflow_health = build_workflow_health_bundle.build_workflow_health_bundle(
        root,
        timestamp=build_workflow_health_bundle.now_iso(),
    )

    payload = {
        "project": str(root),
        "quality_audit": quality_audit,
        "knowledge_projection": knowledge_projection,
        "workflow_health": workflow_health,
        "chapter_structure_audit": audit_chapter_structure_repetition.audit_chapter_structure_repetition(root),
        "precheck_structure_risks": audit_precheck_structure_risks.audit_precheck_structure_risks(root),
    }

    if args.batch_count:
        check_batch_quality_gate = load_batch_gate_module()
        state = check_batch_quality_gate.read_state(root)
        policy = check_batch_quality_gate.load_length_policy()
        nums = list(range(max(1, int(state["progress"]["current_chapter"]) - args.batch_count + 1), int(state["progress"]["current_chapter"]) + 1))
        metrics = check_batch_quality_gate.collect_metrics(root, nums)
        baseline = check_batch_quality_gate.prior_baseline(root, nums[0]) if nums else None
        payload["batch_quality_gate"] = {
            "chapters": nums,
            **check_batch_quality_gate.evaluate(state, metrics, args.batch_count, baseline, policy),
        }

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
