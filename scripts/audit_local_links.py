from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCED_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)


def strip_fenced_code_blocks(text: str) -> str:
    return FENCED_BLOCK_RE.sub("", text)


def iter_markdown_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.md") if ".git" not in p.parts]


def find_broken_links(root: Path) -> list[tuple[str, int, str]]:
    broken: list[tuple[str, int, str]] = []
    for path in iter_markdown_files(root):
        text = strip_fenced_code_blocks(path.read_text(encoding="utf-8", errors="ignore"))
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "file://", "#")):
                continue
            if target.startswith("/"):
                resolved = Path(target)
            else:
                resolved = (path.parent / target).resolve()
            if not resolved.exists():
                line = text.count("\n", 0, match.start()) + 1
                broken.append((str(path.relative_to(root)), line, target))
    return broken


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit local markdown links and ignore fenced code blocks.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    broken = find_broken_links(root)
    if not broken:
        print("NO_BROKEN_LOCAL_MARKDOWN_LINKS")
        return 0

    for file, line, target in broken:
        print(f"{file}:{line}: {target}")
    print(f"TOTAL_BROKEN={len(broken)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
