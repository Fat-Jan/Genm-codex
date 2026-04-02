#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_PATH = REPO_ROOT / "shared" / "templates" / "sample-manifest-v1.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a compact summary for the current sample manifest.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST_PATH))
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser.parse_args()


def read_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_sample_manifest_summary(path: Path) -> dict:
    payload = read_manifest(path)
    samples = payload.get("samples", [])
    tier_counts: Counter[str] = Counter()
    sample_ids: list[str] = []
    if isinstance(samples, list):
        for item in samples:
            if not isinstance(item, dict):
                continue
            tier = item.get("trust_tier")
            sample_id = item.get("sample_id")
            if isinstance(tier, str) and tier:
                tier_counts[tier] += 1
            if isinstance(sample_id, str) and sample_id:
                sample_ids.append(sample_id)
    return {
        "version": payload.get("version", ""),
        "sample_count": len(sample_ids),
        "tier_counts": dict(sorted(tier_counts.items())),
        "sample_ids": sample_ids,
    }


def render_sample_manifest_summary_markdown(path: Path) -> str:
    payload = build_sample_manifest_summary(path)
    lines = [
        "## Sample Manifest Summary",
        f"- sample-count: `{payload['sample_count']}`",
    ]
    for tier, count in payload["tier_counts"].items():
        lines.append(f"- {tier}: `{count}`")
    if payload["sample_ids"]:
        lines.append(f"- sample-ids: `{', '.join(payload['sample_ids'])}`")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    path = Path(args.manifest)
    if args.format == "json":
        print(json.dumps(build_sample_manifest_summary(path), ensure_ascii=False, indent=2))
        return
    print(render_sample_manifest_summary_markdown(path))


if __name__ == "__main__":
    main()
