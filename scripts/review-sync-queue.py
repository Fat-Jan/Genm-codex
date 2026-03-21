#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review and resolve sync-review queue items.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--resolve-alias", nargs=3, metavar=("KIND", "NAME", "TARGET"))
    parser.add_argument("--ignore", nargs=2, metavar=("KIND", "NAME"))
    parser.add_argument("--clear-reviewed", action="store_true")
    return parser.parse_args()


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def base_overrides() -> dict:
    return {
        "version": "1.0",
        "updated_at": "",
        "aliases": {
            "characters": {},
            "locations": {},
            "factions": {},
            "items": {},
        },
        "ignored": {
            "characters": [],
            "locations": [],
            "factions": [],
            "items": [],
        },
    }


def normalize_kind(kind: str) -> str:
    kind = kind.strip().lower()
    if kind in ("character", "characters", "角色"):
        return "characters"
    if kind in ("location", "locations", "地点"):
        return "locations"
    if kind in ("faction", "factions", "势力"):
        return "factions"
    if kind in ("item", "items", "物品"):
        return "items"
    raise ValueError(f"unsupported kind: {kind}")


def add_reviewed(queue: dict, payload: dict) -> None:
    reviewed = queue.setdefault("reviewed_entities", [])
    reviewed.append(payload)


def remove_from_queue(queue: dict, kind_key: str, name: str) -> None:
    singular = kind_key[:-1]
    queue["ambiguous_entities"] = [
        item for item in queue.get("ambiguous_entities", [])
        if not (item.get("kind") == singular and item.get("name") == name)
    ]


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    mighty = root / ".mighty"
    queue_path = mighty / "sync-review.json"
    overrides_path = mighty / "sync-overrides.json"

    queue = load_json(queue_path, {"version": "1.0", "generated_at": "", "chapters_window": [], "ambiguous_entities": [], "reviewed_entities": []})
    overrides = load_json(overrides_path, base_overrides())
    ts = now_iso()

    if args.clear_reviewed:
        queue["reviewed_entities"] = []

    if args.resolve_alias:
        kind, name, target = args.resolve_alias
        kind_key = normalize_kind(kind)
        overrides["aliases"].setdefault(kind_key, {})
        overrides["aliases"][kind_key][name] = target
        remove_from_queue(queue, kind_key, name)
        add_reviewed(queue, {
            "kind": kind_key[:-1],
            "name": name,
            "action": "resolve-alias",
            "target": target,
            "reviewed_at": ts,
        })

    if args.ignore:
        kind, name = args.ignore
        kind_key = normalize_kind(kind)
        ignored = overrides["ignored"].setdefault(kind_key, [])
        if name not in ignored:
            ignored.append(name)
        remove_from_queue(queue, kind_key, name)
        add_reviewed(queue, {
            "kind": kind_key[:-1],
            "name": name,
            "action": "ignore",
            "reviewed_at": ts,
        })

    if args.resolve_alias or args.ignore or args.clear_reviewed:
        overrides["updated_at"] = ts
        overrides_path.write_text(json.dumps(overrides, ensure_ascii=False, indent=2))
        queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2))

    if args.list or not (args.resolve_alias or args.ignore or args.clear_reviewed):
        print(json.dumps({
            "project": str(root),
            "queue_file": str(queue_path),
            "overrides_file": str(overrides_path),
            "pending": queue.get("ambiguous_entities", []),
            "reviewed": queue.get("reviewed_entities", []),
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
