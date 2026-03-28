#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit adjacent chapter structure repetition from chapter_meta.chapter_structure.")
    parser.add_argument("project_root", help="Novel project root")
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sorted_chapter_items(chapter_meta: dict) -> list[tuple[str, dict]]:
    items = []
    for chapter, payload in chapter_meta.items():
        if isinstance(payload, dict):
            chapter_key = str(chapter)
            if chapter_key.isdigit():
                items.append((chapter_key, payload))
    return sorted(items, key=lambda item: int(item[0]))


def audit_chapter_structure_repetition(project_root: Path) -> dict:
    state = read_json(project_root / ".mighty" / "state.json")
    chapter_meta = state.get("chapter_meta", {})
    findings: list[dict] = []

    items = _sorted_chapter_items(chapter_meta if isinstance(chapter_meta, dict) else {})
    previous_conflict_key = None
    previous_gain_key = None
    for chapter, payload in items:
        structure = payload.get("chapter_structure", {})
        if not isinstance(structure, dict):
            continue

        conflict_key = (
            structure.get("conflict_type"),
            structure.get("opponent_mode"),
        )
        gain_key = (
            structure.get("gain_type"),
            structure.get("chapter_end_style"),
        )

        if previous_conflict_key and conflict_key == previous_conflict_key:
            findings.append({
                "code": "repeated-conflict-opponent",
                "chapter": chapter,
                "severity": "warn",
            })
        if previous_gain_key and gain_key == previous_gain_key:
            findings.append({
                "code": "repeated-gain-ending",
                "chapter": chapter,
                "severity": "warn",
            })

        previous_conflict_key = conflict_key
        previous_gain_key = gain_key

    status = "pass"
    if findings:
        status = "warn"

    return {
        "project": str(project_root),
        "status": status,
        "findings": findings,
    }


def main() -> None:
    args = parse_args()
    payload = audit_chapter_structure_repetition(Path(args.project_root))
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
