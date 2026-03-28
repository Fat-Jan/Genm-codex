#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Externalize learned patterns and market adjustments from state.json")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--timestamp", default="")
    return parser.parse_args()


def _trim_string_list(value: object, limit: int = 5) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item][:limit]


def normalize_recent_guardrails(learned: dict) -> dict:
    payload = learned.get("recent_guardrails", {})
    if not isinstance(payload, dict):
        return learned

    normalized = dict(learned)
    normalized["recent_guardrails"] = {
        "must_avoid": _trim_string_list(payload.get("must_avoid")),
        "must_preserve": _trim_string_list(payload.get("must_preserve")),
        "next_chapter_watchpoints": _trim_string_list(payload.get("next_chapter_watchpoints")),
        "expires_after_chapter": payload.get("expires_after_chapter"),
    }
    return normalized


def main() -> None:
    args = parse_args()
    root = Path(args.project_root)
    mighty = root / ".mighty"
    state_path = mighty / "state.json"
    state = json.loads(state_path.read_text())
    ts = args.timestamp or now_iso()

    learned_path = mighty / "learned-patterns.json"
    market_path = mighty / "market-adjustments.json"

    learned = state.get("learned_patterns", {})
    if isinstance(learned, dict) and learned.get("externalized") and learned_path.exists():
        learned = json.loads(learned_path.read_text()).get("data", {})
    if isinstance(learned, dict):
        learned = normalize_recent_guardrails(learned)

    market = state.get("market_adjustments", {})
    if isinstance(market, dict) and market.get("externalized") and market_path.exists():
        market = json.loads(market_path.read_text()).get("data", {})

    learned_path.write_text(json.dumps({
        "version": "1.0",
        "last_updated": ts,
        "data": learned,
    }, ensure_ascii=False, indent=2))
    market_path.write_text(json.dumps({
        "version": "1.0",
        "last_updated": ts,
        "data": market,
    }, ensure_ascii=False, indent=2))

    state["learned_patterns"] = {
        "externalized": True,
        "sidecar_file": ".mighty/learned-patterns.json",
        "last_updated": ts,
        "available_sections": sorted(list(learned.keys())) if isinstance(learned, dict) else [],
        "has_recent_guardrails": isinstance(learned, dict) and isinstance(learned.get("recent_guardrails"), dict),
        "recent_guardrails_expires_after_chapter": (
            learned.get("recent_guardrails", {}).get("expires_after_chapter")
            if isinstance(learned, dict) and isinstance(learned.get("recent_guardrails"), dict)
            else None
        ),
    }
    state["market_adjustments"] = {
        "externalized": True,
        "sidecar_file": ".mighty/market-adjustments.json",
        "last_updated": ts,
        "last_applied": market.get("last_applied") if isinstance(market, dict) else None,
        "source_scan": market.get("source_scan") if isinstance(market, dict) else None,
        "adjustment_count": len(market.get("adjustments", [])) if isinstance(market, dict) else 0,
    }

    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    print(json.dumps({
        "project": str(root),
        "learned_patterns_file": str(learned_path),
        "market_adjustments_file": str(market_path),
        "state_updated": str(state_path),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
