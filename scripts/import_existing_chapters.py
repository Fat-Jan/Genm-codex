#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import existing chapters into the current project conservatively.")
    parser.add_argument("project_root", help="Target novel project root")
    parser.add_argument("--from", dest="source_path", required=True, help="Source chapter directory or single text file")
    return parser.parse_args(argv)


def _chapter_filename(index: int) -> str:
    return f"第{index:03d}章.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_source_chapters(source_path: Path) -> tuple[str, list[dict]]:
    if source_path.is_dir():
        chapters: list[dict] = []
        for idx, path in enumerate(sorted(source_path.iterdir()), start=1):
            if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
                continue
            chapters.append(
                {
                    "chapter": f"{idx:03d}",
                    "title": path.stem,
                    "content": _read_text(path),
                    "source": str(path),
                }
            )
        return "directory", chapters

    text = _read_text(source_path)
    heading_pattern = re.compile(r"(?m)^(第[0-9一二三四五六七八九十百千零〇两]+章(?:\s+.*)?)$")
    matches = list(heading_pattern.finditer(text))
    chapters: list[dict] = []
    if matches:
        for idx, match in enumerate(matches, start=1):
            start = match.start()
            end = matches[idx].start() if idx < len(matches) else len(text)
            content = text[start:end].strip()
            chapters.append(
                {
                    "chapter": f"{idx:03d}",
                    "title": match.group(1).strip(),
                    "content": content,
                    "source": str(source_path),
                }
            )
    else:
        chapters.append(
            {
                "chapter": "001",
                "title": source_path.stem,
                "content": text.strip(),
                "source": str(source_path),
            }
        )
    return "single-file", chapters


def import_chapters(project_root: Path, source_path: Path) -> dict:
    source_kind, chapters = load_source_chapters(source_path)
    chapters_dir = project_root / "chapters"
    mighty = project_root / ".mighty"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    mighty.mkdir(parents=True, exist_ok=True)

    report_rows: list[dict] = []
    for idx, chapter in enumerate(chapters, start=1):
        target_path = chapters_dir / _chapter_filename(idx)
        status = "imported"
        if target_path.exists():
            existing = _read_text(target_path)
            if existing == chapter["content"]:
                status = "reused"
            else:
                status = "conflict"
        else:
            target_path.write_text(chapter["content"], encoding="utf-8")

        report_rows.append(
            {
                "chapter": chapter["chapter"],
                "target_file": str(target_path),
                "source": chapter["source"],
                "title": chapter["title"],
                "status": status,
            }
        )

    report = {
        "version": "1.0",
        "generated_at": now_iso(),
        "project_root": str(project_root),
        "source_path": str(source_path),
        "source_kind": source_kind,
        "chapter_count": len(report_rows),
        "chapters": report_rows,
        "limitations": [
            "does not reconstruct canon/state automatically",
            "requires novel-index build plus gate-facing follow-up",
        ],
        "next_actions": [
            "novel-index build",
            "setting gate",
            "novel-resume",
        ],
    }
    report_path = mighty / "import-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> dict:
    args = parse_args(argv)
    project_root = Path(args.project_root)
    source_path = Path(args.source_path)
    report = import_chapters(project_root, source_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    main()
