#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_project_quality_state
import build_project_knowledge_projection
import build_workflow_health_bundle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a read-only smoke summary for quality-audit / knowledge-projection / workflow-health.")
    parser.add_argument("project_root", help="Novel project root")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    payload = {
        "project": str(root),
        "quality_audit": audit_project_quality_state.audit_project_quality_state(root),
        "knowledge_projection": build_project_knowledge_projection.build_project_knowledge_projection(
            root,
            timestamp=build_project_knowledge_projection.now_iso(),
        ),
        "workflow_health": build_workflow_health_bundle.build_workflow_health_bundle(
            root,
            timestamp=build_workflow_health_bundle.now_iso(),
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
