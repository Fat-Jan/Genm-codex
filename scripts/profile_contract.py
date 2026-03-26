#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


CORE_STRAND_KEYS = ("quest", "fire", "constellation")
ALLOWED_TOP_LEVEL_KEYS = {
    "name",
    "display_name",
    "description",
    "version",
    "template",
    "progression_constraints",
    "sub_genres",
    "golden_three",
    "pacing",
    "cool_points",
    "strand_weights",
    "constraints",
    "reader_expectations",
    "taboos",
    "checker_weights",
    "platform_positioning",
}


def list_reference_files(profile_dir: Path) -> list[str]:
    files: list[str] = []
    for path in sorted(profile_dir.iterdir()):
        if not path.is_file():
            continue
        name = path.name
        if name == "profile.yaml" or (name.startswith("profile-") and name.endswith(".yaml")):
            continue
        files.append(name)
    return files


def resolve_profile_layers(profile_dir: Path, *, platform: str | None = None, bucket: str | None = None) -> dict[str, Any]:
    platform_slug = (platform or "").strip().lower().replace(" ", "-")
    bucket_slug = (bucket or "").strip().lower().replace(" ", "-")
    platform_overlay = resolve_platform_overlay_path(profile_dir, platform_slug) if platform_slug else None
    bucket_overlay = profile_dir / f"bucket-{bucket_slug}.yaml" if bucket_slug else None

    return {
        "profile_dir": str(profile_dir),
        "core_profile": str(profile_dir / "profile.yaml"),
        "platform_overlay": str(platform_overlay) if platform_overlay and platform_overlay.exists() else None,
        "bucket_overlay": str(bucket_overlay) if bucket_overlay and bucket_overlay.exists() else None,
        "reference_files": list_reference_files(profile_dir),
    }


def _platform_aliases(platform_slug: str) -> list[str]:
    aliases: list[str] = []
    normalized = platform_slug.strip().lower().replace(" ", "-")
    if normalized:
        aliases.append(normalized)
    if normalized == "fanqie":
        aliases.append("tomato")
    return aliases


def resolve_platform_overlay_path(profile_dir: Path, platform_slug: str) -> Path | None:
    for candidate_slug in _platform_aliases(platform_slug):
        candidate = profile_dir / f"profile-{candidate_slug}.yaml"
        if candidate.exists():
            return candidate
    return None


def _filter_contract_sections(raw_text: str) -> str:
    kept: list[str] = []
    include_block = False

    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped:
            if include_block:
                kept.append(line)
            continue

        if not line.startswith((" ", "\t")):
            key = stripped.split(":", 1)[0]
            include_block = key in ALLOWED_TOP_LEVEL_KEYS
        if include_block:
            kept.append(line)

    return "\n".join(kept) + "\n"


def load_profile(path: Path) -> dict[str, Any]:
    raw_text = path.read_text(encoding="utf-8")
    payload = yaml.safe_load(_filter_contract_sections(raw_text))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} did not parse to a mapping")
    payload["__section_presence__"] = {
        "dialogue_templates": "\ndialogue_templates:" in f"\n{raw_text}",
        "scene_description": "\nscene_description:" in f"\n{raw_text}",
        "sub_genres": "\nsub_genres:" in f"\n{raw_text}",
        "progression_constraints": "\nprogression_constraints:" in f"\n{raw_text}",
    }
    return payload


def merge_profile_layers(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overlay.items():
        if key == "__section_presence__":
            base_presence = merged.get("__section_presence__", {})
            if not isinstance(base_presence, dict):
                base_presence = {}
            if isinstance(value, dict):
                merged["__section_presence__"] = {**base_presence, **value}
            continue
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    return merged


def load_profile_with_overlays(path: Path, *, platform: str | None = None, bucket: str | None = None) -> dict[str, Any]:
    profile_dir = path.parent
    payload = load_profile(path)
    platform_slug = (platform or "").strip().lower().replace(" ", "-")
    if platform_slug:
        overlay_path = resolve_platform_overlay_path(profile_dir, platform_slug)
        if overlay_path is not None:
            payload = merge_profile_layers(payload, load_profile(overlay_path))
    bucket_slug = (bucket or "").strip().lower().replace(" ", "-")
    if bucket_slug:
        bucket_overlay = profile_dir / f"bucket-{bucket_slug}.yaml"
        if bucket_overlay.exists():
            payload = merge_profile_layers(payload, load_profile(bucket_overlay))
    return payload


def _normalize_word_count(pacing: dict[str, Any]) -> dict[str, Any]:
    value = pacing.get("word_count")
    if isinstance(value, dict):
        return value

    alt = pacing.get("word_count_range")
    if isinstance(alt, dict):
        normalized: dict[str, Any] = {}
        mapping = {"min": "minimum", "standard": "standard", "long": "long"}
        for source_key, target_key in mapping.items():
            if source_key in alt:
                normalized[target_key] = alt[source_key]
        return normalized
    return {}


def _normalize_density(cool_points: dict[str, Any]) -> float | str | None:
    if "density" in cool_points:
        return cool_points["density"]
    return cool_points.get("density_required")


def _normalize_strand_weights(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    return {key: raw[key] for key in CORE_STRAND_KEYS if key in raw}


def _normalize_constraint(item: Any) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        return None
    normalized = {
        "id": item.get("id") or item.get("ID") or "",
        "description": item.get("description") or item.get("content") or "",
        "mandatory": bool(item.get("mandatory", False)),
        "checkpoint": item.get("checkpoint") or item.get("check_point") or "",
    }
    if not any(normalized.values()):
        return None
    return normalized


def _normalize_constraints(raw_profile: dict[str, Any]) -> list[dict[str, Any]]:
    rows = raw_profile.get("constraints")
    if not isinstance(rows, list):
        return []
    normalized = []
    for row in rows:
        item = _normalize_constraint(row)
        if item:
            normalized.append(item)
    return normalized


def _normalize_taboos(raw_profile: dict[str, Any]) -> list[dict[str, Any]]:
    rows = raw_profile.get("taboos")
    if not isinstance(rows, list):
        return []
    normalized = []
    for row in rows:
        item = _normalize_constraint(row)
        if item:
            severity = ""
            if isinstance(row, dict):
                severity = row.get("severity", "")
            item["severity"] = severity
            normalized.append(item)
    return normalized


def _normalize_reader_expectations(raw: dict[str, Any]) -> dict[str, list[str]]:
    if not isinstance(raw, dict):
        return {"must_satisfy": [], "optional_satisfy": [], "must_not": []}

    def list_or_empty(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, str)]

    return {
        "must_satisfy": list_or_empty(raw.get("must_satisfy")),
        "optional_satisfy": list_or_empty(raw.get("optional_satisfy")),
        "must_not": list_or_empty(raw.get("must_not") or raw.get("never_violate")),
    }


def normalize_profile(raw_profile: dict[str, Any], *, source_path: str) -> dict[str, Any]:
    pacing = raw_profile.get("pacing", {}) if isinstance(raw_profile.get("pacing"), dict) else {}
    cool_points = raw_profile.get("cool_points", {}) if isinstance(raw_profile.get("cool_points"), dict) else {}

    section_presence = raw_profile.get("__section_presence__", {})
    if not isinstance(section_presence, dict):
        section_presence = {}

    return {
        "contract_version": "1.0",
        "source_path": source_path,
        "name": raw_profile.get("name", ""),
        "display_name": raw_profile.get("display_name") or raw_profile.get("name", ""),
        "description": raw_profile.get("description", ""),
        "version": raw_profile.get("version", ""),
        "template": raw_profile.get("template", ""),
        "pacing": {
            "type": pacing.get("type", ""),
            "tension_ratio": pacing.get("tension_ratio", ""),
            "typical_chapter_length": pacing.get("typical_chapter_length"),
            "word_count": _normalize_word_count(pacing),
        },
        "cool_points": {
            "density": _normalize_density(cool_points),
            "max_interval": cool_points.get("max_interval"),
        },
        "strand_weights": _normalize_strand_weights(raw_profile.get("strand_weights")),
        "constraints": _normalize_constraints(raw_profile),
        "reader_expectations": _normalize_reader_expectations(raw_profile.get("reader_expectations")),
        "taboos": _normalize_taboos(raw_profile),
        "notes": {
            "has_dialogue_templates": bool(section_presence.get("dialogue_templates")),
            "has_scene_description": bool(section_presence.get("scene_description")),
            "has_sub_genres": bool(section_presence.get("sub_genres")) or isinstance(raw_profile.get("sub_genres"), dict),
            "has_progression_constraints": bool(section_presence.get("progression_constraints"))
            or isinstance(raw_profile.get("progression_constraints"), dict),
        },
    }


def summarize_for_state(normalized_profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "loaded": normalized_profile["source_path"],
        "bucket": "",
        "positioning_initialized": False,
        "tagpacks": [],
        "strong_tags": [],
        "narrative_modes": [],
        "tone_guardrails": [],
        "positioning_sidecar": ".mighty/content-positioning.json",
        "节奏": normalized_profile["pacing"],
        "爽点密度": normalized_profile["cool_points"]["density"] or 0,
        "strand权重": normalized_profile["strand_weights"],
        "特殊约束": normalized_profile["constraints"],
    }


def resolve_platform_positioning(raw_profile: dict[str, Any], *, platform: str) -> dict[str, Any]:
    positioning = raw_profile.get("platform_positioning", {})
    if not isinstance(positioning, dict):
        return {}
    candidate = positioning.get(platform, {})
    return candidate if isinstance(candidate, dict) else {}


def main(argv: list[str] | None = None) -> dict[str, Any]:
    import argparse

    parser = argparse.ArgumentParser(description="Normalize a shared profile into the project contract shape.")
    parser.add_argument("profile_path", help="Path to profile.yaml")
    parser.add_argument("--state-summary", action="store_true", help="Emit only the state.genre_profile projection")
    parser.add_argument("--describe-layers", action="store_true", help="Describe core/overlay/reference layer paths")
    parser.add_argument("--platform", default="", help="Optional platform overlay selector for --describe-layers")
    parser.add_argument("--bucket", default="", help="Optional bucket overlay selector for --describe-layers")
    args = parser.parse_args(argv)

    path = Path(args.profile_path)
    if args.describe_layers:
        payload = resolve_profile_layers(path.parent, platform=args.platform or None, bucket=args.bucket or None)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return payload
    normalized = normalize_profile(load_profile(path), source_path=str(path))
    payload = summarize_for_state(normalized) if args.state_summary else normalized
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    main()
