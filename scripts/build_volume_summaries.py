#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build compressed volume summaries from archived chapter summaries.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--timestamp", default="")
    return parser.parse_args(argv)


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _summary_value(value: object) -> str:
    if isinstance(value, dict):
        summary = value.get("summary")
        if isinstance(summary, str):
            return summary
    if isinstance(value, str):
        return value
    return ""


def build_ranges(archive_summaries: dict) -> list[list[tuple[str, str]]]:
    rows = [(chapter, _summary_value(value)) for chapter, value in archive_summaries.items() if _summary_value(value)]
    rows.sort(key=lambda item: int(item[0]))
    if not rows:
        return []

    ranges: list[list[tuple[str, str]]] = [[rows[0]]]
    for chapter, summary in rows[1:]:
        last_chapter = ranges[-1][-1][0]
        if int(chapter) == int(last_chapter) + 1:
            ranges[-1].append((chapter, summary))
        else:
            ranges.append([(chapter, summary)])
    return ranges


def build_volume_summaries(project_root: Path, *, timestamp: str) -> dict:
    mighty = project_root / ".mighty"
    state = read_json(mighty / "state.json")
    archive = read_json(mighty / "state-archive.json")

    archive_summaries = archive.get("summaries_index", {}) if isinstance(archive.get("summaries_index", {}), dict) else {}
    live_summaries = state.get("summaries_index", {}) if isinstance(state.get("summaries_index", {}), dict) else {}

    ranges = []
    for items in build_ranges(archive_summaries):
        start = items[0][0]
        end = items[-1][0]
        chapter_summaries = [{"chapter": chapter, "summary": summary} for chapter, summary in items]
        summary_text = "\n".join([f"第{chapter}章：{summary}" for chapter, summary in items])
        ranges.append(
            {
                "id": f"{start}-{end}",
                "start_chapter": start,
                "end_chapter": end,
                "chapter_count": len(items),
                "chapters": [chapter for chapter, _ in items],
                "summary": summary_text,
                "chapter_summaries": chapter_summaries,
            }
        )

    return {
        "version": "1.0",
        "generated_at": timestamp,
        "project_root": str(project_root),
        "archive_file": str(mighty / "state-archive.json"),
        "live_summary_count": len(live_summaries),
        "archived_summary_count": len(archive_summaries),
        "ranges": ranges,
    }


def main(argv: list[str] | None = None) -> dict:
    args = parse_args(argv)
    project_root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    payload = build_volume_summaries(project_root, timestamp=ts)
    output_path = project_root / ".mighty" / "volume-summaries.json"
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    result = {
        "project": str(project_root),
        "volume_summaries_file": str(output_path),
        "archived_summary_count": payload["archived_summary_count"],
        "range_count": len(payload["ranges"]),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
