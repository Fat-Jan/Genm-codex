#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import strong_quality_gate


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic post-write lint checks on one chapter file.")
    parser.add_argument("chapter_file", help="Chapter markdown file")
    return parser.parse_args(argv)


def load_policy() -> dict:
    return strong_quality_gate.load_policy()


def _max_repeated_exact_token(text: str) -> tuple[str, int]:
    tokens = [token for token in text.split() if token]
    if not tokens:
        return "", 0
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    token, count = max(counts.items(), key=lambda item: item[1])
    return token, count


def analyze_text(text: str, policy: dict) -> dict:
    lint_policy = policy.get("post_write_lint", {})
    malformed_policy = policy.get("post_write_gate", {}).get("malformed_text", {})

    issues: list[dict] = []
    warnings: list[dict] = []
    matched_checks: list[str] = []

    ai_policy = lint_policy.get("ai_turn_markers", {})
    marker_words = ai_policy.get("words", [])
    marker_threshold = int(ai_policy.get("warn_total_occurrences", 0) or 0)
    marker_counts = {
        word: text.count(word)
        for word in marker_words
        if isinstance(word, str) and text.count(word) > 0
    }
    total_markers = sum(marker_counts.values())
    if marker_threshold and total_markers >= marker_threshold:
        warnings.append(
            {
                "code": "ai-turn-marker-density",
                "message": f"AI 转折标记词出现 {total_markers} 次",
                "detail": marker_counts,
            }
        )
        matched_checks.append("ai-turn-marker-density")

    explanation_patterns = lint_policy.get("explanation_first_patterns", [])
    explanation_hit = next((pattern for pattern in explanation_patterns if isinstance(pattern, str) and pattern in text), None)
    if explanation_hit:
        warnings.append(
            {
                "code": "explanation-first-template",
                "message": f"命中解释先行模板：{explanation_hit}",
            }
        )
        matched_checks.append("explanation-first-template")

    shock_patterns = lint_policy.get("collective_shock_patterns", [])
    shock_hit = None
    for pattern in shock_patterns:
        if not isinstance(pattern, str):
            continue
        match = re.search(pattern, text)
        if match:
            shock_hit = match.group(0)
            break
    if shock_hit:
        warnings.append(
            {
                "code": "collective-shock-template",
                "message": f"命中群体震惊模板：{shock_hit}",
            }
        )
        matched_checks.append("collective-shock-template")

    paragraph_policy = lint_policy.get("long_paragraphs", {})
    warn_over_chars = int(paragraph_policy.get("warn_over_chars", 0) or 0)
    warn_min_paragraphs = int(paragraph_policy.get("warn_min_paragraphs", 0) or 0)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    long_paragraph_count = sum(1 for p in paragraphs if len(p) >= warn_over_chars)
    if warn_over_chars and warn_min_paragraphs and long_paragraph_count >= warn_min_paragraphs:
        warnings.append(
            {
                "code": "long-paragraph-density",
                "message": f"超过 {warn_over_chars} 字的长段落有 {long_paragraph_count} 个",
                "detail": {
                    "long_paragraph_count": long_paragraph_count,
                    "warn_over_chars": warn_over_chars,
                },
            }
        )
        matched_checks.append("long-paragraph-density")

    token, token_count = _max_repeated_exact_token(text)
    exact_min = int(malformed_policy.get("repeated_exact_token_min_occurrences", 0) or 0)
    if exact_min and token and token_count >= exact_min:
        issues.append(
            {
                "code": "malformed-repeated-token",
                "message": f"存在重复 token: {token}",
                "detail": {
                    "token": token,
                    "occurrences": token_count,
                },
            }
        )
        matched_checks.append("malformed-repeated-token")

    return {
        "policy_source": policy.get("policy_name", "strong-quality-gate-policy"),
        "issues": issues,
        "warnings": warnings,
        "matched_checks": matched_checks,
        "metrics": {
            "chars": len(text),
            "paragraph_count": len(paragraphs),
            "long_paragraph_count": long_paragraph_count,
            "ai_turn_marker_count": total_markers,
        },
    }


def main(argv: list[str] | None = None) -> dict:
    args = parse_args(argv)
    chapter_path = Path(args.chapter_file)
    text = chapter_path.read_text(encoding="utf-8")
    payload = analyze_text(text, load_policy())
    payload["chapter_file"] = str(chapter_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


if __name__ == "__main__":
    main()
