#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
MERGE_MAP_PATH = REPO_ROOT / "shared" / "templates" / "skill-merge-map-v1.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render install alias pairs from the current skill merge map.")
    parser.add_argument("--format", choices=["json", "tsv"], default="json")
    return parser.parse_args()


def read_merge_map() -> dict:
    return json.loads(MERGE_MAP_PATH.read_text(encoding="utf-8"))


def build_install_pairs() -> dict:
    payload = read_merge_map()
    pairs: list[dict[str, str]] = []
    for item in payload.get("entries", []):
        if not isinstance(item, dict):
            continue
        skill = item.get("skill")
        decision = item.get("decision")
        if not isinstance(skill, str) or not skill:
            continue
        if decision not in {"protected", "alias"}:
            continue
        pairs.append({"source": skill, "target": skill})
        pairs.append({"source": skill, "target": f"genm-{skill}"})
    return {
        "version": payload.get("version", "1.0"),
        "pairs": pairs,
    }


def main() -> None:
    args = parse_args()
    payload = build_install_pairs()
    if args.format == "tsv":
        for item in payload["pairs"]:
            print(f"{item['source']}\t{item['target']}")
        return
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
