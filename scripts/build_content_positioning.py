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
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_mapping_registry(project_root: Path) -> dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[1]
    return read_json(repo_root / "shared" / "templates" / "content-positioning-map-v1.json")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a content-positioning sidecar from lightweight genre_profile fields.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--timestamp", default="")
    return parser.parse_args(argv)


def infer_primary_profile(loaded_path: str) -> str:
    parts = loaded_path.replace("\\", "/").split("/")
    if len(parts) >= 3 and parts[-1].startswith("profile"):
        return parts[-2]
    return ""


def normalize_platform(platform: str) -> str:
    if platform == "番茄":
        return "fanqie"
    return platform.strip().lower().replace(" ", "-")


def build_content_positioning(project_root: Path, *, timestamp: str) -> dict[str, Any]:
    state = read_json(project_root / ".mighty" / "state.json")
    mapping_registry = load_mapping_registry(project_root)
    genre_profile = state.get("genre_profile", {}) if isinstance(state.get("genre_profile"), dict) else {}
    primary_profile = infer_primary_profile(str(genre_profile.get("loaded", "")))
    platform_key = normalize_platform(str(state.get("meta", {}).get("platform", "")))
    profile_mapping = (
        mapping_registry.get("profiles", {})
        .get(primary_profile, {})
        .get(platform_key, {})
        if primary_profile
        else {}
    )

    def prefer_list(key: str) -> list[str]:
        live = genre_profile.get(key, [])
        if isinstance(live, list) and live:
            return live
        mapped = profile_mapping.get(key, [])
        return mapped if isinstance(mapped, list) else []

    primary_bucket = str(genre_profile.get("bucket") or profile_mapping.get("primary_bucket") or "")
    tagpacks = prefer_list("tagpacks")
    strong_tags = prefer_list("strong_tags")
    narrative_modes = prefer_list("narrative_modes")
    tone_guardrails = prefer_list("tone_guardrails")
    package_cues = profile_mapping.get("package_cues", [])
    if not isinstance(package_cues, list):
        package_cues = []

    return {
        "version": "1.0",
        "generated_at": timestamp,
        "primary_profile": primary_profile,
        "primary_bucket": primary_bucket,
        "tagpacks": tagpacks,
        "strong_tags": strong_tags,
        "narrative_modes": narrative_modes,
        "tone_guardrails": tone_guardrails,
        "compiler_output": {
            "outline_overlays": [f"narrative_mode:{item}" for item in narrative_modes],
            "write_overlays": [f"tone_guardrail:{item}" for item in tone_guardrails],
            "review_lenses": [f"strong_tag:{item}" for item in strong_tags],
            "package_cues": [f"tagpack:{item}" for item in tagpacks] + [f"cue:{item}" for item in package_cues],
        },
    }


def main(argv: list[str] | None = None) -> dict[str, Any]:
    args = parse_args(argv)
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    payload = build_content_positioning(root, timestamp=ts)
    output_path = root / ".mighty" / "content-positioning.json"
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path = append_trace(
        root,
        event="content_positioning.built",
        skill="build_content_positioning",
        result="success",
        details={"output_file": str(output_path)},
        timestamp=ts,
    )
    result = {
        "project": str(root),
        "content_positioning_file": str(output_path),
        "trace_log_file": str(log_path),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
