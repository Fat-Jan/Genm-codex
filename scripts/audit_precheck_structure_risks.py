#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit structure-level precheck risks from chapter_meta.chapter_structure.")
    parser.add_argument("project_root", help="Novel project root")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sorted_structures(chapter_meta: dict) -> list[tuple[str, dict]]:
    rows = []
    for chapter, payload in chapter_meta.items():
        if not isinstance(payload, dict):
            continue
        structure = payload.get("chapter_structure", {})
        if isinstance(structure, dict) and structure:
            rows.append((str(chapter), structure))
    return sorted(rows, key=lambda item: int(item[0]))


def audit_precheck_structure_risks(project_root: Path) -> dict:
    state = read_json(project_root / ".mighty" / "state.json")
    chapter_meta = state.get("chapter_meta", {})
    rows = _sorted_structures(chapter_meta if isinstance(chapter_meta, dict) else {})
    findings: list[dict] = []

    repeated_run = 1
    zero_cost_run = 0
    non_valley_run = 0
    previous_shape = None
    valley_arcs = {"suppress", "cost", "choice"}

    for chapter, structure in rows:
        shape = (
            structure.get("conflict_type"),
            structure.get("opponent_mode"),
            structure.get("gain_type"),
            structure.get("chapter_end_style"),
        )
        if previous_shape and shape == previous_shape:
            repeated_run += 1
        else:
            repeated_run = 1
        if repeated_run >= 2:
            findings.append({
                "code": "repeated-structure-run",
                "chapter": chapter,
                "severity": "warn",
            })

        if structure.get("protagonist_arc") == "breakthrough" and structure.get("cost_visibility") == "none":
            zero_cost_run += 1
        else:
            zero_cost_run = 0
        if zero_cost_run >= 2:
            findings.append({
                "code": "zero-cost-breakthrough-run",
                "chapter": chapter,
                "severity": "warn",
            })

        if structure.get("protagonist_arc") not in valley_arcs:
            non_valley_run += 1
        else:
            non_valley_run = 0
        if non_valley_run >= 3:
            findings.append({
                "code": "no-valley-run",
                "chapter": chapter,
                "severity": "warn",
            })

        previous_shape = shape

    return {
        "project": str(project_root),
        "status": "warn" if findings else "pass",
        "findings": findings,
    }


def main() -> None:
    args = parse_args()
    payload = audit_precheck_structure_risks(Path(args.project_root))
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
