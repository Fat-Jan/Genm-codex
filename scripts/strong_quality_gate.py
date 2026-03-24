from __future__ import annotations

import json
from pathlib import Path
import re


def load_policy() -> dict:
    policy_path = Path(__file__).resolve().parents[1] / "docs" / "strong-quality-gate-policy.json"
    return json.loads(policy_path.read_text(encoding="utf-8"))


def resolve_length_policy(state: dict, policy: dict) -> dict:
    bucket = state.get("genre_profile", {}).get("bucket")
    if bucket and bucket in policy.get("buckets", {}):
        active = dict(policy["buckets"][bucket])
        active["bucket_name"] = bucket
        active["track"] = active.get("track") or policy.get("buckets", {}).get(bucket, {}).get("track")
        return active

    target_chapters = int(state.get("meta", {}).get("target_chapters") or 0)
    track = "shortform" if target_chapters and target_chapters <= 8 else "longform"
    active = dict(policy["defaults"][track])
    active["track"] = track
    active["bucket_name"] = bucket or "__default__"
    return active


def _truth_source_trigger_terms(patterns: list[str]) -> set[str]:
    terms: set[str] = set()
    for pattern in patterns:
        stem = Path(pattern).stem.replace("*", "")
        if not stem:
            continue
        terms.add(stem)
        trimmed = stem
        for suffix in ("真值表", "层级图"):
            if trimmed.endswith(suffix):
                trimmed = trimmed[: -len(suffix)]
        if trimmed.startswith("小型"):
            trimmed = trimmed[2:]
        if len(trimmed) >= 2:
            terms.add(trimmed)
    return {term for term in terms if len(term) >= 2}


def _outline_mentions_category(outline_text: str, patterns: list[str]) -> bool:
    if not outline_text:
        return False
    return any(token in outline_text for token in _truth_source_trigger_terms(patterns))


def _route_requests_category(route_signal: dict, category_key: str) -> bool:
    truth_sources = route_signal.get("truth_sources")
    if isinstance(truth_sources, (list, tuple, set)):
        return category_key in truth_sources
    return False


def _matches_truth_source(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if "*" in pattern:
            prefix = pattern.split("*")[0]
            if path.startswith(prefix):
                return True
        elif path == pattern:
            return True
    return False


def detect_missing_truth_sources(outline_text: str, route_signal: dict, available_paths: list[str], policy: dict) -> dict:
    truth_sources = policy.get("pre_write_gate", {}).get("truth_sources", {})
    missing: list[dict] = []
    used: list[str] = []
    for key, patterns in truth_sources.items():
        triggered = _route_requests_category(route_signal, key) or _outline_mentions_category(outline_text, patterns)
        if not triggered:
            continue
        used.append(key)
        found = any(_matches_truth_source(path, patterns) for path in available_paths)
        if not found:
            missing.append({
                "key": key,
                "patterns": list(patterns),
            })
    return {"used": used, "missing": missing}


def _max_repeated_exact_token(text: str) -> tuple[str, int]:
    tokens = [token for token in text.split() if token]
    if not tokens:
        return "", 0
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    token, count = max(counts.items(), key=lambda item: item[1])
    return token, count


def _extract_fragments(text: str, min_len: int, include_clauses: bool) -> list[str]:
    if min_len <= 0:
        return []
    fragments: list[str] = []
    sentences = re.split(r"[。！？!?；;\\n]", text)
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) >= min_len:
            fragments.append(sentence)
        if include_clauses and sentence:
            clauses = re.split(r"[，,、]", sentence)
            for clause in clauses:
                clause = clause.strip()
                if len(clause) >= min_len:
                    fragments.append(clause)
    return fragments


def _repeated_fragments(fragments: list[str], min_occurrences: int) -> list[str]:
    if not fragments or min_occurrences <= 1:
        return []
    counts: dict[str, int] = {}
    for fragment in fragments:
        counts[fragment] = counts.get(fragment, 0) + 1
    return [fragment for fragment, count in counts.items() if count >= min_occurrences]


def _default_metrics(chapter_text: str, chapter_number: int | None) -> dict:
    metrics = {"chars": len(chapter_text)}
    if chapter_number is not None:
        metrics["chapter"] = chapter_number
    return metrics


def evaluate_post_write_gate(
    *,
    state: dict,
    chapter_text: str,
    baseline_avg_chars: float | None,
    policy: dict,
    chapter_number: int | None = None,
) -> dict:
    length_policy = resolve_length_policy(state, policy)
    hard_min = int(length_policy["hard_min_chars"])
    soft_min = int(length_policy["soft_min_chars"])

    shrinkage_policy = policy.get("post_write_gate", {}).get("shrinkage", {})
    malformed_policy = policy.get("post_write_gate", {}).get("malformed_text", {})

    issues: list[dict] = []
    warnings: list[dict] = []
    matched_checks: list[str] = []
    metrics = _default_metrics(chapter_text, chapter_number)

    if metrics["chars"] < hard_min:
        issue = {
            "code": "chapter-too-short",
            "message": f"章节长度 {metrics['chars']} 低于硬下限 {hard_min}",
        }
        if chapter_number is not None:
            issue["chapter"] = chapter_number
        issues.append(issue)
        matched_checks.append("hard-min-chars")
    elif metrics["chars"] < soft_min:
        warn = {
            "code": "chapter-below-soft-floor",
            "message": f"章节长度 {metrics['chars']} 低于软下限 {soft_min}",
        }
        if chapter_number is not None:
            warn["chapter"] = chapter_number
        warnings.append(warn)
        matched_checks.append("soft-min-chars")

    baseline_ratio = float(shrinkage_policy.get("baseline_drop_ratio", 0.0) or 0.0)
    if baseline_avg_chars and baseline_ratio:
        if metrics["chars"] < baseline_avg_chars * baseline_ratio:
            issue = {
                "code": "sharp-length-drop",
                "message": f"章节长度相对基线跌破 {baseline_ratio:.2f}",
                "detail": {
                    "baseline_avg_chars": baseline_avg_chars,
                    "ratio": baseline_ratio,
                },
            }
            if chapter_number is not None:
                issue["chapter"] = chapter_number
            issues.append(issue)
            matched_checks.append("shrinkage-baseline-drop")

    compressed_ratio = float(shrinkage_policy.get("compressed_ratio_of_hard_min", 0.0) or 0.0)
    compressed_floor = int(shrinkage_policy.get("compressed_floor_chars", 0) or 0)
    if compressed_ratio:
        compressed_threshold = max(compressed_floor, int(hard_min * compressed_ratio))
        if metrics["chars"] < compressed_threshold:
            issue = {
                "code": "compressed-below-threshold",
                "message": f"章节长度低于压缩阈值 {compressed_threshold}",
            }
            if chapter_number is not None:
                issue["chapter"] = chapter_number
            issues.append(issue)
            matched_checks.append("compressed-hard-min")

    token, token_count = _max_repeated_exact_token(chapter_text)
    exact_min = int(malformed_policy.get("repeated_exact_token_min_occurrences", 0) or 0)
    if exact_min and token_count >= exact_min and token:
        issues.append({
            "code": "malformed-repeated-token",
            "message": f"存在重复 token: {token}",
            "detail": {"token": token, "occurrences": token_count},
        })
        matched_checks.append("malformed-repeated-exact-token")

    fragment_min = int(malformed_policy.get("repeated_fragment_min_occurrences", 0) or 0)
    sentence_min = int(malformed_policy.get("duplicated_sentence_fragment_min_occurrences", 0) or 0)
    min_fragment_chars = 10
    sentence_fragments = _extract_fragments(chapter_text, min_fragment_chars, include_clauses=False)
    repeated_sentences = _repeated_fragments(sentence_fragments, sentence_min) if sentence_min else []
    clause_fragments = _extract_fragments(chapter_text, min_fragment_chars, include_clauses=True)
    repeated_clauses = _repeated_fragments(clause_fragments, fragment_min) if fragment_min else []
    repeated_fragments = list({*repeated_sentences, *repeated_clauses})
    if repeated_fragments:
        issues.append({
            "code": "malformed-repeated-fragment",
            "message": "存在重复句段",
            "detail": {"fragments": repeated_fragments[:5]},
        })
        matched_checks.append("malformed-repeated-fragment")

    status = "block" if issues else "pass"
    return {
        "status": status,
        "issues": issues,
        "warnings": warnings,
        "length_policy": length_policy,
        "baseline_avg_chars": baseline_avg_chars,
        "metrics": metrics,
        "matched_checks": matched_checks,
    }


def classify_sync_candidate(
    *,
    name: str,
    occurrences: int,
    policy: dict,
    phrase_fragment_hits: int = 0,
    repetitive_noise_hits: int = 0,
) -> dict:
    characters = policy.get("sync_gate", {}).get("characters", {})
    reasons: list[str] = []
    accepted = True

    if re.fullmatch(r"(?:高|初)(?:一|二|三|\d{1,2})", name):
        accepted = False
        reasons.append("school-grade-token")

    min_mentions = int(characters.get("min_confidence_mentions", 0) or 0)
    if occurrences < min_mentions:
        accepted = False
        reasons.append("insufficient-mentions")

    max_chars = int(characters.get("max_person_name_chars", 0) or 0)
    if max_chars and len(name) > max_chars:
        accepted = False
        reasons.append("too-long")

    reject_contains = characters.get("reject_if_contains", [])
    if any(token in name for token in reject_contains):
        accepted = False
        reasons.append("contains-rejected-token")

    if name in set(characters.get("reject_exact_names", [])):
        accepted = False
        reasons.append("rejected-exact-name")

    if any(name.endswith(suffix) for suffix in characters.get("reject_suffixes", [])):
        accepted = False
        reasons.append("rejected-suffix")

    garment_hints = characters.get("garment_or_object_hints", [])
    if any(hint in name for hint in garment_hints):
        accepted = False
        reasons.append("garment-or-object-hint")

    fragment_threshold = int(characters.get("phrase_fragment_reject_min_occurrences", 0) or 0)
    if fragment_threshold and phrase_fragment_hits >= fragment_threshold:
        accepted = False
        reasons.append("phrase-fragment")

    noise_threshold = int(characters.get("repetitive_noise_reject_min_occurrences", 0) or 0)
    if noise_threshold and repetitive_noise_hits >= noise_threshold:
        accepted = False
        reasons.append("repetitive-noise")

    return {
        "name": name,
        "accepted": accepted,
        "reasons": reasons,
        "occurrences": occurrences,
        "phrase_fragment_hits": phrase_fragment_hits,
        "repetitive_noise_hits": repetitive_noise_hits,
    }
