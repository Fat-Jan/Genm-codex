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
    parser.add_argument("--format", choices=["json", "tsv", "registry"], default="json")
    return parser.parse_args()


def read_merge_map() -> dict:
    return json.loads(MERGE_MAP_PATH.read_text(encoding="utf-8"))


def build_skill_registry() -> dict:
    payload = read_merge_map()
    skills: list[dict[str, object]] = []
    aliases: list[dict[str, str]] = []

    for item in payload.get("entries", []):
        if not isinstance(item, dict):
            continue

        skill = item.get("skill")
        decision = item.get("decision")
        reason = item.get("reason")
        if not isinstance(skill, str) or not skill:
            continue

        install_names: list[str] = []
        legacy_aliases: list[str] = []
        if decision in {"protected", "alias"}:
            install_names = [skill, f"genm-{skill}"]
            legacy_aliases = [f"genm-{skill}"]
            aliases.append(
                {
                    "source_skill": skill,
                    "install_name": skill,
                    "kind": "canonical",
                }
            )
            aliases.append(
                {
                    "source_skill": skill,
                    "install_name": f"genm-{skill}",
                    "kind": "compatibility",
                }
            )

        skills.append(
            {
                "skill": skill,
                "decision": decision,
                "reason": reason,
                "target": item.get("target"),
                "installable": bool(install_names),
                "directory": f"skills/{skill}",
                "canonical_install_name": skill if install_names else None,
                "legacy_aliases": legacy_aliases,
                "install_names": install_names,
            }
        )

    return {
        "version": payload.get("version", "1.0"),
        "generated_at": payload.get("generated_at"),
        "skills": skills,
        "aliases": aliases,
    }


def build_install_pairs() -> dict:
    payload = build_skill_registry()
    pairs: list[dict[str, str]] = []
    for item in payload["aliases"]:
        pairs.append(
            {
                "source": item["source_skill"],
                "target": item["install_name"],
            }
        )
    return {
        "version": payload.get("version", "1.0"),
        "pairs": pairs,
    }


def main() -> None:
    args = parse_args()
    if args.format == "registry":
        print(json.dumps(build_skill_registry(), ensure_ascii=False, indent=2))
        return
    payload = build_install_pairs()
    if args.format == "tsv":
        for item in payload["pairs"]:
            print(f"{item['source']}\t{item['target']}")
        return
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
