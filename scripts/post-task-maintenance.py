#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SUPPORTED_TRIGGERS = {"write", "batch", "workflow"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automatic post-task maintenance hook for novel projects.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--trigger", choices=sorted(SUPPORTED_TRIGGERS), required=True)
    parser.add_argument("--recent-chapters", type=int, default=8)
    parser.add_argument("--retain-recent-chapters", type=int, default=8)
    parser.add_argument("--batch-count", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    state_path = root / ".mighty" / "state.json"
    if not state_path.exists():
        print(json.dumps({
            "project": str(root),
            "trigger": args.trigger,
            "action": "skip",
            "reason": "state-missing",
        }, ensure_ascii=False, indent=2))
        return

    script_dir = Path(__file__).resolve().parent
    cmd = [
        sys.executable,
        str(script_dir / "project-maintenance.py"),
        str(root),
        "--recent-chapters",
        str(args.recent_chapters),
        "--retain-recent-chapters",
        str(args.retain_recent_chapters),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    result = {
        "project": str(root),
        "trigger": args.trigger,
        "action": "ran-maintenance",
        "maintenance_stdout": proc.stdout.strip(),
    }

    if args.trigger == "batch":
        gate_cmd = [
            sys.executable,
            str(script_dir / "check-batch-quality-gate.py"),
            str(root),
            "--batch-count",
            str(args.batch_count or 0),
            "--write-report",
        ]
        gate_proc = subprocess.run(gate_cmd, capture_output=True, text=True, check=True)
        result["batch_quality_gate"] = json.loads(gate_proc.stdout)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
