#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    script_dir = Path(__file__).resolve().parent

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

    report = {
        "project": str(root),
        "run_at": ts,
        "transaction_contract": "chapter-transaction-v1",
        "transaction_phase": "maintenance",
        "next_transaction_step": "snapshot",
        "steps": steps,
    }
    report_path = root / ".mighty" / "maintenance-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({
        "project": str(root),
        "report_file": str(report_path),
        "transaction_contract": "chapter-transaction-v1",
        "transaction_phase": "maintenance",
        "next_transaction_step": "snapshot",
        "steps": [Path(step["cmd"][1]).name for step in steps],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
