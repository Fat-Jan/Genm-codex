#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


def is_private_use_char(ch: str) -> bool:
    return len(ch) == 1 and "\uE000" <= ch <= "\uF8FF"


def extract_private_use_chars(text: str) -> list[str]:
    chars: list[str] = []
    seen: set[str] = set()
    for ch in text:
        if not is_private_use_char(ch) or ch in seen:
            continue
        seen.add(ch)
        chars.append(ch)
    return chars


def resolve_exact_matches(subset_signatures: dict[str, str], reference_signatures: dict[str, list[str]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for char, signature in subset_signatures.items():
        candidates = reference_signatures.get(signature, [])
        if len(candidates) == 1:
            mapping[char] = candidates[0]
    return mapping


def apply_mapping(text: str, mapping: dict[str, str]) -> str:
    return "".join(mapping.get(ch, ch) for ch in text)


def require_fonttools():
    try:
        from fontTools.pens.recordingPen import RecordingPen
        from fontTools.ttLib import TTFont
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "fontTools 未安装。请先安装后再运行该原型，例如："
            " python3 -m pip install fonttools brotli"
        ) from exc
    return TTFont, RecordingPen


def resolve_font_number(font_path: Path, font_number: int | None) -> int | None:
    if font_number is not None:
        return font_number
    if font_path.suffix.lower() == ".ttc":
        return 0
    return None


def open_font(font_path: Path, *, font_number: int | None = None):
    TTFont, _ = require_fonttools()
    resolved_number = resolve_font_number(font_path, font_number)
    kwargs = {}
    if resolved_number is not None:
        kwargs["fontNumber"] = resolved_number
    return TTFont(str(font_path), **kwargs)


def glyph_signature(glyphset, glyph_name: str, recording_pen_cls) -> str:
    pen = recording_pen_cls()
    glyphset[glyph_name].draw(pen)
    payload = repr(pen.value).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()


def normalized_segment_features(recording: list[tuple[str, tuple]], bounds: tuple[float, float, float, float], *, quantize: int = 24) -> Counter:
    minx, miny, maxx, maxy = bounds
    width = max(maxx - minx, 1)
    height = max(maxy - miny, 1)
    current = None
    features: list[tuple] = []

    def normalize_point(point: tuple[float, float]) -> tuple[int, int]:
        x, y = point
        return (
            round((x - minx) / width * quantize),
            round((y - miny) / height * quantize),
        )

    for op, args in recording:
        if op == "moveTo":
            current = args[0]
            continue
        if current is None:
            continue
        if op == "lineTo":
            left = normalize_point(current)
            right = normalize_point(args[0])
            features.append(("L", tuple(sorted((left, right)))))
            current = args[0]
            continue
        if op == "curveTo":
            p0 = normalize_point(current)
            p1 = normalize_point(args[0])
            p2 = normalize_point(args[1])
            p3 = normalize_point(args[2])
            forward = ("C", p0, p1, p2, p3)
            reverse = ("C", p3, p2, p1, p0)
            features.append(min(forward, reverse))
            current = args[2]
    return Counter(features)


def overlap_score(left: Counter | dict, right: Counter | dict) -> float:
    left = Counter(left)
    right = Counter(right)
    common = sum((left & right).values())
    total = sum((left | right).values())
    if total == 0:
        return 1.0
    return common / total


def rank_candidate_features(target: Counter, candidates: dict[str, Counter], *, limit: int = 10) -> list[tuple[str, float]]:
    ranked = sorted(
        ((char, overlap_score(target, features)) for char, features in candidates.items()),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked[:limit]


def resolve_approximate_matches(
    candidates: dict[str, list[tuple[str, float]]],
    *,
    min_score: float = 0.2,
    min_gap: float = 0.08,
) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for source_char, ranked in candidates.items():
        if not ranked:
            continue
        best_char, best_score = ranked[0]
        second_score = ranked[1][1] if len(ranked) > 1 else 0.0
        if best_score < min_score:
            continue
        if best_score - second_score < min_gap:
            continue
        mapping[source_char] = best_char
    return mapping


def build_subset_signatures(subset_font_path: Path) -> dict[str, str]:
    _, RecordingPen = require_fonttools()
    font = open_font(subset_font_path)
    glyphset = font.getGlyphSet()
    cmap: dict[int, str] = {}
    for table in font["cmap"].tables:
        cmap.update(table.cmap)

    result: dict[str, str] = {}
    for codepoint, glyph_name in cmap.items():
        ch = chr(codepoint)
        if not is_private_use_char(ch):
            continue
        result[ch] = glyph_signature(glyphset, glyph_name, RecordingPen)
    return result


def build_reference_signatures(
    reference_font_path: Path,
    *,
    chars: list[str] | None = None,
    reference_font_number: int | None = None,
) -> dict[str, list[str]]:
    _, RecordingPen = require_fonttools()
    font = open_font(reference_font_path, font_number=reference_font_number)
    glyphset = font.getGlyphSet()
    cmap: dict[int, str] = {}
    for table in font["cmap"].tables:
        cmap.update(table.cmap)

    if chars is None:
        codepoints = [cp for cp in cmap.keys() if 0x4E00 <= cp <= 0x9FFF]
    else:
        codepoints = [ord(ch) for ch in chars if ord(ch) in cmap]

    signatures: dict[str, list[str]] = {}
    for codepoint in codepoints:
        ch = chr(codepoint)
        glyph_name = cmap[codepoint]
        signature = glyph_signature(glyphset, glyph_name, RecordingPen)
        signatures.setdefault(signature, []).append(ch)
    return signatures


def build_subset_features(subset_font_path: Path, *, quantize: int = 24) -> dict[str, Counter]:
    _, RecordingPen = require_fonttools()
    from fontTools.pens.boundsPen import BoundsPen

    font = open_font(subset_font_path)
    glyphset = font.getGlyphSet()
    cmap: dict[int, str] = {}
    for table in font["cmap"].tables:
        cmap.update(table.cmap)

    features: dict[str, Counter] = {}
    for codepoint, glyph_name in cmap.items():
        ch = chr(codepoint)
        if not is_private_use_char(ch):
            continue
        recording_pen = RecordingPen()
        glyphset[glyph_name].draw(recording_pen)
        bounds_pen = BoundsPen(glyphset)
        glyphset[glyph_name].draw(bounds_pen)
        if bounds_pen.bounds is None:
            continue
        features[ch] = normalized_segment_features(recording_pen.value, bounds_pen.bounds, quantize=quantize)
    return features


def build_reference_features(
    reference_font_path: Path,
    *,
    chars: list[str] | None = None,
    quantize: int = 24,
    reference_font_number: int | None = None,
) -> dict[str, Counter]:
    _, RecordingPen = require_fonttools()
    from fontTools.pens.boundsPen import BoundsPen

    font = open_font(reference_font_path, font_number=reference_font_number)
    glyphset = font.getGlyphSet()
    cmap: dict[int, str] = {}
    for table in font["cmap"].tables:
        cmap.update(table.cmap)

    if chars is None:
        codepoints = [cp for cp in cmap.keys() if 0x4E00 <= cp <= 0x9FFF]
    else:
        codepoints = [ord(ch) for ch in chars if ord(ch) in cmap]

    features: dict[str, Counter] = {}
    for codepoint in codepoints:
        glyph_name = cmap[codepoint]
        recording_pen = RecordingPen()
        glyphset[glyph_name].draw(recording_pen)
        bounds_pen = BoundsPen(glyphset)
        glyphset[glyph_name].draw(bounds_pen)
        if bounds_pen.bounds is None:
            continue
        features[chr(codepoint)] = normalized_segment_features(recording_pen.value, bounds_pen.bounds, quantize=quantize)
    return features


def build_approximate_mapping_for_text(
    subset_font_path: Path,
    reference_font_path: Path,
    sample_text: str,
    *,
    reference_font_number: int | None = None,
) -> dict[str, str]:
    subset_features = build_subset_features(subset_font_path)
    reference_features = build_reference_features(reference_font_path, reference_font_number=reference_font_number)
    approximate_candidates = {
        char: rank_candidate_features(target, reference_features, limit=5)
        for char, target in subset_features.items()
        if char in extract_private_use_chars(sample_text)
    }
    return resolve_approximate_matches(approximate_candidates)


def run_probe(*, subset_font_path: Path, reference_font_path: Path, sample_text: str, reference_font_number: int | None = None) -> dict:
    subset_signatures = build_subset_signatures(subset_font_path)
    reference_signatures = build_reference_signatures(reference_font_path, reference_font_number=reference_font_number)
    exact_mapping = resolve_exact_matches(subset_signatures, reference_signatures)
    subset_features = build_subset_features(subset_font_path)
    reference_features = build_reference_features(reference_font_path, reference_font_number=reference_font_number)
    approximate_candidates = {
        char: rank_candidate_features(target, reference_features, limit=5)
        for char, target in subset_features.items()
        if char in extract_private_use_chars(sample_text)
    }
    approximate_mapping = resolve_approximate_matches(approximate_candidates)
    return {
        "sample_text": sample_text,
        "private_use_chars": extract_private_use_chars(sample_text),
        "resolved_mapping": {char: exact_mapping[char] for char in extract_private_use_chars(sample_text) if char in exact_mapping},
        "approximate_candidates": {
            char: [{"char": candidate, "score": round(score, 6)} for candidate, score in candidates]
            for char, candidates in approximate_candidates.items()
        },
        "suggested_mapping": {char: approximate_mapping[char] for char in extract_private_use_chars(sample_text) if char in approximate_mapping},
        "decoded_text": apply_mapping(sample_text, exact_mapping),
        "suggested_decoded_text": apply_mapping(sample_text, approximate_mapping),
        "mapped_char_count": len(exact_mapping),
        "subset_char_count": len(subset_signatures),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prototype font-based deobfuscation for Fanqie private-use glyphs.")
    parser.add_argument("subset_font", type=Path, help="Subset WOFF2 font downloaded from the target page.")
    parser.add_argument("reference_font", type=Path, help="Reference SourceHanSansSC-compatible font.")
    parser.add_argument("--reference-font-number", type=int, default=None, help="Optional font index when the reference font is a TTC collection.")
    parser.add_argument("--text", default="", help="Sample text containing private-use chars.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_probe(
        subset_font_path=args.subset_font,
        reference_font_path=args.reference_font,
        sample_text=args.text,
        reference_font_number=args.reference_font_number,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
