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


def _normalize_slug_token(value: str) -> str:
    return value.strip().lower().replace(" ", "-").replace("_", "-")


def _load_fanqie_bucket_name_map() -> dict[str, str]:
    repo_root = Path(__file__).resolve().parents[1]
    source = repo_root / "docs" / "fanqie-mvp-buckets.yaml"
    if not source.exists():
        return {}
    payload = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
    buckets = payload.get("buckets", {})
    if not isinstance(buckets, dict):
        return {}
    mapping: dict[str, str] = {}
    for bucket_key, details in buckets.items():
        if not isinstance(bucket_key, str) or not isinstance(details, dict):
            continue
        bucket_name = details.get("bucket_name")
        if isinstance(bucket_name, str) and bucket_name.strip():
            mapping[_normalize_slug_token(bucket_key)] = bucket_name.strip()
    return mapping


def _collect_declared_bucket_names(raw_profile: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for key in ("name", "display_name"):
        value = raw_profile.get(key)
        if isinstance(value, str) and value.strip():
            names.add(value.strip())
    positioning = raw_profile.get("platform_positioning", {})
    if isinstance(positioning, dict):
        for candidate in positioning.values():
            if not isinstance(candidate, dict):
                continue
            bucket_name = candidate.get("primary_bucket")
            if isinstance(bucket_name, str) and bucket_name.strip():
                names.add(bucket_name.strip())
    return names


def resolve_bucket_overlay_path(profile_dir: Path, bucket: str, *, raw_profile: dict[str, Any] | None = None) -> Path | None:
    if not bucket:
        return None

    raw_profile = raw_profile or {}
    declared_bucket_names = _collect_declared_bucket_names(raw_profile)
    normalized_input = _normalize_slug_token(bucket)
    fanqie_bucket_name_map = _load_fanqie_bucket_name_map()
    bucket_display_name = fanqie_bucket_name_map.get(normalized_input, "")

    candidate_names: list[str] = [normalized_input]
    comparison_values = {bucket.strip(), normalized_input}
    if bucket_display_name:
        comparison_values.add(bucket_display_name)
        comparison_values.add(_normalize_slug_token(bucket_display_name))

    normalized_declared = {
        bucket_name for bucket_name in declared_bucket_names if bucket_name
    } | {_normalize_slug_token(bucket_name) for bucket_name in declared_bucket_names if bucket_name}

    if comparison_values & normalized_declared:
        candidate_names.append(profile_dir.name)

    seen: set[str] = set()
    for candidate_name in candidate_names:
        normalized_name = _normalize_slug_token(candidate_name)
        if not normalized_name or normalized_name in seen:
            continue
        seen.add(normalized_name)
        candidate = profile_dir / f"bucket-{normalized_name}.yaml"
        if candidate.exists():
            return candidate
    return None


def resolve_profile_layers(profile_dir: Path, *, platform: str | None = None, bucket: str | None = None) -> dict[str, Any]:
    platform_slug = (platform or "").strip().lower().replace(" ", "-")
    raw_profile = load_profile(profile_dir / "profile.yaml")
    platform_overlay = resolve_platform_overlay_path(profile_dir, platform_slug) if platform_slug else None
    if platform_overlay is not None:
        raw_profile = merge_profile_layers(raw_profile, load_profile(platform_overlay))
    bucket_overlay = resolve_bucket_overlay_path(profile_dir, bucket or "", raw_profile=raw_profile) if bucket else None

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
    if bucket:
        bucket_overlay = resolve_bucket_overlay_path(profile_dir, bucket, raw_profile=payload)
        if bucket_overlay is not None:
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


def summarize_for_state(
    normalized_profile: dict[str, Any],
    *,
    raw_profile: dict[str, Any] | None = None,
    platform: str = "",
) -> dict[str, Any]:
    positioning = resolve_platform_positioning(raw_profile or {}, platform=platform) if platform else {}
    bucket = str(positioning.get("primary_bucket") or "")
    strong_tags = positioning.get("strong_tags", []) if isinstance(positioning.get("strong_tags", []), list) else []
    narrative_modes = positioning.get("narrative_modes", []) if isinstance(positioning.get("narrative_modes", []), list) else []
    tone_guardrails = positioning.get("tone_guardrails", []) if isinstance(positioning.get("tone_guardrails", []), list) else []
    return {
        "loaded": normalized_profile["source_path"],
        "bucket": bucket,
        "positioning_initialized": bool(positioning),
        "tagpacks": [],
        "strong_tags": strong_tags,
        "narrative_modes": narrative_modes,
        "tone_guardrails": tone_guardrails,
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
    raw_profile = load_profile_with_overlays(path, platform=args.platform or None, bucket=args.bucket or None)
    normalized = normalize_profile(raw_profile, source_path=str(path))
    payload = summarize_for_state(normalized, raw_profile=raw_profile, platform=args.platform or "") if args.state_summary else normalized
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    main()
