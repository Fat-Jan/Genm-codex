#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from trace_log import append_trace


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a state-centric chapter snapshot artifact.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--chapter", default="")
    parser.add_argument("--timestamp", default="")
    return parser.parse_args(argv)


def determine_target_chapter(state: dict[str, Any], explicit_chapter: str | None = None) -> str:
    if explicit_chapter:
        return f"{int(explicit_chapter):03d}"
    progress = state.get("progress", {})
    last_write = progress.get("last_write_chapter")
    if last_write:
        return f"{int(last_write):03d}"
    current = progress.get("current_chapter", 0)
    return f"{int(current):03d}"


def build_snapshot_payload(project_root: Path, *, chapter: str, timestamp: str) -> dict[str, Any]:
    state = read_json(project_root / ".mighty" / "state.json")
    chapter_int = int(chapter)
    chapter_meta = state.get("chapter_meta", {}).get(chapter, {})
    protagonist = state.get("entities", {}).get("characters", {}).get("protagonist", {})
    active_characters = state.get("entities", {}).get("characters", {}).get("active", [])
    foreshadowing = state.get("plot_threads", {}).get("foreshadowing", {})
    summary = chapter_meta.get("summary") or state.get("summaries_index", {}).get(chapter, {}).get("summary")
    chapter_path = project_root / "chapters" / f"第{chapter}章.md"
    chapter_text = chapter_path.read_text(encoding="utf-8") if chapter_path.exists() else ""

    snapshot = {
        "chapter": chapter_int,
        "path": str(chapter_path.relative_to(project_root)).replace("\\", "/") if chapter_path.exists() else "",
        "created_at": timestamp,
        "updated_at": timestamp,
        "word_count": len(chapter_text),
        "protagonist_state": protagonist,
        "active_characters": active_characters[:5] if isinstance(active_characters, list) else [],
        "active_foreshadowing": foreshadowing.get("active", []) if isinstance(foreshadowing.get("active", []), list) else [],
        "knowledge_state": state.get("knowledge_base", {}),
        "key_events": chapter_meta.get("key_events", []),
        "summary": summary or "",
    }
    return snapshot


def write_filesystem_snapshot(project_root: Path, *, chapter: str, timestamp: str, snapshot: dict[str, Any]) -> Path:
    snapshot_dir = project_root / ".mighty" / "snapshots" / f"chapter-{chapter}" / timestamp.replace(":", "-")
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    path = snapshot_dir / "snapshot.json"
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def generate_snapshot(project_root: Path, *, chapter: str | None = None, timestamp: str = "") -> dict[str, Any]:
    project_root = Path(project_root)
    ts = timestamp or now_iso()
    state_path = project_root / ".mighty" / "state.json"
    state = read_json(state_path)
    chapter_key = determine_target_chapter(state, chapter)
    payload = build_snapshot_payload(project_root, chapter=chapter_key, timestamp=ts)

    state.setdefault("chapter_snapshots", {})
    state["chapter_snapshots"][chapter_key] = payload
    state["meta"]["updated_at"] = ts
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    filesystem_path = write_filesystem_snapshot(project_root, chapter=chapter_key, timestamp=ts, snapshot=payload)
    log_path = append_trace(
        project_root,
        event="snapshot.generated",
        skill="generate_snapshot",
        result="success",
        details={"chapter": chapter_key, "filesystem_snapshot": str(filesystem_path)},
        timestamp=ts,
    )

    return {
        "project": str(project_root),
        "chapter": chapter_key,
        "timestamp": ts,
        "state_snapshot_written": True,
        "filesystem_snapshot_file": str(filesystem_path),
        "trace_log_file": str(log_path),
    }


def main(argv: list[str] | None = None) -> dict[str, Any]:
    args = parse_args(argv)
    payload = generate_snapshot(Path(args.project_root), chapter=args.chapter or None, timestamp=args.timestamp)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    main()
