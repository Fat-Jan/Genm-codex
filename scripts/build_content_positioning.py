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

import sidecar_freshness
from trace_log import append_trace
import profile_contract


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
    normalized = loaded_path.replace("\\", "/").strip()
    if not normalized:
        return ""
    parts = normalized.split("/")
    if len(parts) >= 3 and parts[-1].startswith("profile"):
        return parts[-2]
    if "/" not in normalized and "." not in normalized:
        return normalized
    return ""


def normalize_platform(platform: str) -> str:
    if platform == "番茄":
        return "fanqie"
    return platform.strip().lower().replace(" ", "-")


def fallback_reader_motive(primary_bucket: str) -> list[str]:
    mapping = {
        "职场婚恋": ["想看关系绑定如何改写工作局面"],
        "都市脑洞": ["想看反差设定如何快速兑现"],
        "青春甜宠": ["想看关系如何快速升温"],
        "历史脑洞": ["想看权谋与反差设定持续升级"],
        "豪门总裁": ["想看身份压制下的关系反转"],
        "都市日常": ["想看日常关系网慢慢变热"],
        "科幻末世": ["想看生存压力下的换账与反打"],
        "宫斗宅斗": ["想看高门压制下的反咬翻盘"],
        "现实情感": ["想看现实困局如何被主动切账"],
        "玄幻脑洞": ["想看金手指与成长兑现"],
        "传统玄幻": ["想看宗门成长与突破兑现"],
    }
    return mapping.get(primary_bucket, [])


def build_content_positioning(project_root: Path, *, timestamp: str) -> dict[str, Any]:
    repo_root = SCRIPT_DIR.parent
    state = read_json(project_root / ".mighty" / "state.json")
    mapping_registry = load_mapping_registry(project_root)
    genre_profile = state.get("genre_profile", {}) if isinstance(state.get("genre_profile"), dict) else {}
    primary_profile = infer_primary_profile(str(genre_profile.get("loaded", "")))
    platform_key = normalize_platform(str(state.get("meta", {}).get("platform", "")))
    raw_profile: dict[str, Any] = {}
    profile_positioning = {}
    loaded_path = str(genre_profile.get("loaded", "")).strip()
    if loaded_path:
        profile_path = project_root / loaded_path
        if not profile_path.exists():
            profile_path = Path(__file__).resolve().parents[1] / loaded_path
        if profile_path.exists():
            raw_profile = profile_contract.load_profile_with_overlays(
                profile_path,
                platform=platform_key,
                bucket=str(genre_profile.get("bucket", "")),
            )
            profile_positioning = profile_contract.resolve_platform_positioning(raw_profile, platform=platform_key)
    profile_mapping = (
        mapping_registry.get("profiles", {})
        .get(primary_profile, {})
        .get(platform_key, {})
        if primary_profile
        else {}
    )
    bucket_defaults = mapping_registry.get("bucket_defaults", {})
    bucket_mapping = (
        bucket_defaults.get(str(genre_profile.get("bucket", "")), {})
        if isinstance(bucket_defaults, dict)
        else {}
    )
    positioning_initialized = bool(genre_profile.get("positioning_initialized"))

    def choose_mapping_value(key: str):
        if key in profile_positioning:
            return profile_positioning.get(key)
        if key in profile_mapping:
            return profile_mapping.get(key)
        if key in bucket_mapping:
            return bucket_mapping.get(key)
        return None

    def prefer_list(key: str) -> list[str]:
        live = genre_profile.get(key, [])
        if positioning_initialized and isinstance(live, list):
            return live
        if isinstance(live, list) and live:
            return live
        mapped = choose_mapping_value(key)
        return mapped if isinstance(mapped, list) else []

    if positioning_initialized and "bucket" in genre_profile:
        primary_bucket = str(genre_profile.get("bucket") or "")
    else:
        primary_bucket = str(genre_profile.get("bucket") or choose_mapping_value("primary_bucket") or "")
    tagpacks = prefer_list("tagpacks")
    strong_tags = prefer_list("strong_tags")
    narrative_modes = prefer_list("narrative_modes")
    tone_guardrails = prefer_list("tone_guardrails")
    raw_progression = raw_profile.get("progression_constraints", {}) if isinstance(raw_profile.get("progression_constraints"), dict) else {}
    raw_golden_three = raw_profile.get("golden_three", {}) if isinstance(raw_profile.get("golden_three"), dict) else {}
    opening_hook = raw_golden_three.get("opening_hook")
    opening_hook_cues = [opening_hook] if isinstance(opening_hook, str) and opening_hook.strip() else []
    payoff_cadence = str(raw_progression.get("partial_payoff_rule") or "").strip()
    reader_motive = choose_mapping_value("reader_motive")
    if not isinstance(reader_motive, list):
        reader_motive = fallback_reader_motive(primary_bucket)
    package_cues = choose_mapping_value("package_cues")
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
        "opening_hook_cues": opening_hook_cues,
        "payoff_cadence": payoff_cadence,
        "reader_motive": reader_motive,
        "compiler_output": {
            "outline_overlays": [f"narrative_mode:{item}" for item in narrative_modes],
            "write_overlays": [f"tone_guardrail:{item}" for item in tone_guardrails],
            "review_lenses": [f"strong_tag:{item}" for item in strong_tags],
            "package_cues": [f"tagpack:{item}" for item in tagpacks] + [f"cue:{item}" for item in package_cues],
        },
        "freshness": sidecar_freshness.build_freshness(
            repo_root=repo_root,
            artifact_key="content-positioning",
            timestamp=timestamp,
            project_root=project_root,
            inputs={
                "state.json": {
                    "path": ".mighty/state.json",
                    "updated_at": state.get("meta", {}).get("updated_at"),
                    "loaded_profile": loaded_path,
                    "bucket": genre_profile.get("bucket", ""),
                },
                "content-positioning-map-v1.json": {
                    "path": "shared/templates/content-positioning-map-v1.json",
                    "mapped_profile_count": len(mapping_registry.get("profiles", {})),
                    "bucket_default_count": len(mapping_registry.get("bucket_defaults", {})),
                },
            },
        ),
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
