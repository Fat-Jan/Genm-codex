#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from writing_core_smoke import default_output_path, load_state, run_smoke, sample_date


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run writing-core smoke for multiple projects from a manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--mode", choices=("draft", "writeback"), default="draft")
    parser.add_argument("--writeback", action="store_true")
    parser.add_argument("--save-packaging", action="store_true")
    parser.add_argument("--summary-report")
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def aggregate_outputs(outputs: list[dict]) -> dict:
    bucket_counts: dict[str, int] = {}
    packaging_status_counts: dict[str, int] = {}
    writeback_status_counts: dict[str, int] = {}
    for item in outputs:
        bucket = item.get("bucket") or "unknown"
        bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1
        packaging_status = item.get("packaging_status") or "unknown"
        packaging_status_counts[packaging_status] = packaging_status_counts.get(packaging_status, 0) + 1
        writeback_status = item.get("writeback_status") or "unknown"
        writeback_status_counts[writeback_status] = writeback_status_counts.get(writeback_status, 0) + 1
    return {
        "bucket_counts": bucket_counts,
        "packaging_status_counts": packaging_status_counts,
        "writeback_status_counts": writeback_status_counts,
    }


def run_batch(
    *,
    manifest_path: str | Path,
    output_dir: str | Path,
    mode: str = "draft",
    writeback: bool = False,
    save_packaging: bool = False,
    summary_report: str | Path | None = None,
    date_str: str | None = None,
) -> dict:
    manifest_path = Path(manifest_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = load_manifest(manifest_path)
    projects = payload.get("projects", [])
    outputs = []
    failed_projects = []
    effective_date = sample_date(date_str)
    for item in projects:
        project_root = Path(item["project_root"])
        chapters = item["chapters"]
        try:
            state_path = project_root / ".mighty" / "state.json"
            if not state_path.exists():
                raise FileNotFoundError(f"Missing state file: {state_path}")
            state = load_state(project_root)
            title = (state.get("meta") or {}).get("title") or project_root.name
            default_path = default_output_path(project_root, title, effective_date)
            output_path = output_dir / default_path.name
            result = run_smoke(
                project_root=project_root,
                chapters=chapters,
                mode=mode,
                output_path=output_path,
                date_str=effective_date,
                writeback=writeback,
                save_packaging=save_packaging,
            )
            outputs.append(result)
        except Exception as exc:  # noqa: BLE001
            failed_projects.append(
                {
                    "project_root": str(project_root),
                    "chapters": chapters,
                    "error": str(exc),
                }
            )
    aggregates = aggregate_outputs(outputs)
    result = {
        "generated_at": now_iso(),
        "mode": mode,
        "count": len(projects),
        "success_count": len(outputs),
        "failure_count": len(failed_projects),
        "outputs": outputs,
        "failed_projects": failed_projects,
        **aggregates,
    }
    if summary_report:
        summary_path = Path(summary_report)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_batch(
        manifest_path=args.manifest,
        output_dir=args.output_dir,
        mode=args.mode,
        writeback=args.writeback,
        save_packaging=args.save_packaging,
        summary_report=args.summary_report,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
