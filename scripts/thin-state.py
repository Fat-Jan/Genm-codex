#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_volume_summaries import build_volume_summaries


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Thin state.json by archiving old chapter metadata.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--retain-recent-chapters", type=int, default=8)
    parser.add_argument("--timestamp", default="")
    return parser.parse_args(argv)


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def sort_keys(mapping: dict) -> list[str]:
    return sorted(mapping.keys(), key=lambda x: int(x))


def merge_sorted(a: dict, b: dict) -> dict:
    merged = dict(a)
    merged.update(b)
    return dict(sorted(merged.items(), key=lambda kv: int(kv[0])))


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    root = Path(args.project_root)
    state_path = root / ".mighty" / "state.json"
    archive_path = root / ".mighty" / "state-archive.json"

    state = json.loads(state_path.read_text())
    chapter_meta = state.get("chapter_meta", {})
    chapter_snapshots = state.get("chapter_snapshots", {})
    summaries_index = state.get("summaries_index", {})

    keys = sort_keys(chapter_meta)
    if len(keys) <= args.retain_recent_chapters:
        print(json.dumps({
            "action": "noop",
            "reason": "chapter count within retain window",
            "chapter_count": len(keys),
            "retain_recent_chapters": args.retain_recent_chapters,
            "active_context_retained": bool(state.get("active_context")),
        }, ensure_ascii=False, indent=2))
        return

    keep = keys[-args.retain_recent_chapters:]
    archive = keys[:-args.retain_recent_chapters]

    archive_doc = {
        "$schema": "state-archive-v1.json",
        "version": "1.0",
        "archived_at": args.timestamp or "",
        "retained_recent_chapters": keep,
        "chapter_meta": {},
        "chapter_snapshots": {},
        "summaries_index": {},
    }
    if archive_path.exists():
        try:
            archive_doc = json.loads(archive_path.read_text())
        except Exception:
            pass

    archive_doc["archived_at"] = args.timestamp or archive_doc.get("archived_at", "")
    archive_doc["retained_recent_chapters"] = keep
    archive_doc["chapter_meta"] = merge_sorted(
        archive_doc.get("chapter_meta", {}),
        {k: chapter_meta[k] for k in archive if k in chapter_meta},
    )
    archive_doc["chapter_snapshots"] = merge_sorted(
        archive_doc.get("chapter_snapshots", {}),
        {k: chapter_snapshots[k] for k in archive if k in chapter_snapshots},
    )
    archive_doc["summaries_index"] = merge_sorted(
        archive_doc.get("summaries_index", {}),
        {k: summaries_index[k] for k in archive if k in summaries_index},
    )

    state["chapter_meta"] = {k: chapter_meta[k] for k in keep if k in chapter_meta}
    state["chapter_snapshots"] = {k: chapter_snapshots[k] for k in keep if k in chapter_snapshots}
    state["summaries_index"] = {k: summaries_index[k] for k in keep if k in summaries_index}

    atomic_write_json(archive_path, archive_doc)
    atomic_write_json(state_path, state)
    volume_payload = build_volume_summaries(root, timestamp=args.timestamp or "")
    volume_path = root / ".mighty" / "volume-summaries.json"
    atomic_write_json(volume_path, volume_payload)

    print(json.dumps({
        "action": "thinned",
        "retained_recent_chapters": keep,
        "archived_chapters": archive,
        "archive_file": str(archive_path),
        "active_context_retained": bool(state.get("active_context")),
        "volume_summaries_file": str(volume_path),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
