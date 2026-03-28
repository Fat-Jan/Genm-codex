#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit project quality artifacts for review/close false positives.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def has_nonzero_dimension_scores(payload: dict | None) -> bool:
    if not isinstance(payload, dict):
        return False
    return any(value not in (0, 0.0, None, "") for value in payload.values())


def audit_project_quality_state(project_root: Path) -> dict:
    state_path = project_root / ".mighty" / "state.json"
    state = read_json(state_path)

    findings: list[dict] = []
    chapter_meta = state.get("chapter_meta", {})
    reviewed_chapters = 0

    for chapter, meta in chapter_meta.items():
        if not isinstance(meta, dict):
            continue
        if meta.get("review_score") is None:
            continue
        reviewed_chapters += 1

        issue_clusters = meta.get("issue_clusters")
        if isinstance(issue_clusters, list) and not issue_clusters:
            findings.append({
                "code": "empty-issue-clusters-with-score",
                "chapter": chapter,
                "severity": "warn",
            })

        route = meta.get("recommended_next_action")
        if not isinstance(route, str) or not route:
            findings.append({
                "code": "missing-route-decision",
                "chapter": chapter,
                "severity": "warn",
            })

        if "needs_fix" not in meta:
            findings.append({
                "code": "missing-needs-fix-flag",
                "chapter": chapter,
                "severity": "warn",
            })

        if not has_nonzero_dimension_scores(meta.get("dimension_scores")):
            findings.append({
                "code": "missing-dimension-scores",
                "chapter": chapter,
                "severity": "warn",
            })

        if not meta.get("anti_flattening_flags") and not meta.get("anti_flattening_summary"):
            findings.append({
                "code": "missing-anti-flattening-artifacts",
                "chapter": chapter,
                "severity": "warn",
            })

    project_dimensions = state.get("quality_metrics", {}).get("dimension_scores", {})
    if reviewed_chapters and not has_nonzero_dimension_scores(project_dimensions):
        findings.append({
            "code": "empty-project-dimension-scores",
            "severity": "fail",
        })

    status = "pass"
    if findings:
        status = "fail" if any(item["severity"] == "fail" for item in findings) else "warn"

    return {
        "project": str(project_root),
        "reviewed_chapter_count": reviewed_chapters,
        "status": status,
        "findings": findings,
    }


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    payload = audit_project_quality_state(root)
    if args.write:
        output_path = root / ".mighty" / "quality-audit.json"
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        payload["quality_audit_file"] = str(output_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
