#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a narrow active-context sidecar for current writing/review.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--recent-limit", type=int, default=5)
    return parser.parse_args(argv)


def read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def unwrap_sidecar(payload: dict | None) -> dict:
    if not isinstance(payload, dict):
        return {}
    data = payload.get("data")
    if isinstance(data, dict):
        return data
    return payload


def load_state_and_sidecars(project_root: Path) -> dict:
    mighty = project_root / ".mighty"
    state = read_json(mighty / "state.json") or {}
    return {
        "state": state,
        "state_archive": read_json(mighty / "state-archive.json") or {},
        "learned": unwrap_sidecar(read_json(mighty / "learned-patterns.json")),
        "market": unwrap_sidecar(read_json(mighty / "market-adjustments.json")),
        "gate": read_json(mighty / "setting-gate.json") or {},
        "launch_stack": read_json(mighty / "launch-stack.json") or {},
    }


def _summary_value(value: object) -> str:
    if isinstance(value, dict):
        summary = value.get("summary")
        if isinstance(summary, str):
            return summary
    if isinstance(value, str):
        return value
    return ""


def select_recent_summaries(state: dict, state_archive: dict | None = None, limit: int = 5) -> list[dict]:
    merged: dict[str, object] = {}
    archive = (state_archive or {}).get("summaries_index", {})
    live = state.get("summaries_index", {})
    if isinstance(archive, dict):
        merged.update(archive)
    if isinstance(live, dict):
        merged.update(live)

    rows = [
        {"chapter": chapter, "summary": _summary_value(value)}
        for chapter, value in merged.items()
        if _summary_value(value)
    ]
    rows.sort(key=lambda row: int(row["chapter"]))
    return rows[-limit:]


def select_active_hooks(state: dict) -> list[dict]:
    hooks: list[dict] = []
    seen: set[str] = set()

    foreshadowing = state.get("plot_threads", {}).get("foreshadowing", {})
    for key in ("active", "pending", "warning", "overdue"):
        values = foreshadowing.get(key, [])
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, dict):
                continue
            identity = str(item.get("id") or item.get("name") or item.get("content") or "")
            if not identity or identity in seen:
                continue
            seen.add(identity)
            hooks.append(item)

    active_hooks = state.get("reading_power_state", {}).get("active_hooks", [])
    if isinstance(active_hooks, list):
        for item in active_hooks:
            if not isinstance(item, dict):
                continue
            identity = str(item.get("id") or item.get("name") or item.get("content") or "")
            if not identity or identity in seen:
                continue
            seen.add(identity)
            hooks.append(item)

    return hooks


def select_relevant_entities(state: dict) -> dict:
    def normalize_named_entries(values: object) -> list[str]:
        if not isinstance(values, list):
            return []
        out: list[str] = []
        for item in values:
            if isinstance(item, str) and item:
                out.append(item)
            elif isinstance(item, dict):
                name = item.get("name")
                if isinstance(name, str) and name:
                    out.append(name)
        return out

    entities = state.get("entities", {})
    characters = entities.get("characters", {})
    protagonist = characters.get("protagonist", {})
    active_characters = characters.get("active", [])
    if not isinstance(active_characters, list):
        active_characters = []

    locations = entities.get("locations", {})
    active_locations: list[str] = []
    current = locations.get("current")
    if isinstance(current, str) and current:
        active_locations.append(current)
    important = locations.get("important", [])
    if isinstance(important, list):
        active_locations.extend([x for x in important if isinstance(x, str) and x])

    factions = entities.get("factions", {}).get("active", [])
    active_factions = normalize_named_entries(factions)

    items = entities.get("items", {})
    tracked_items = []
    for key in ("tracked", "protagonist_inventory"):
        tracked_items.extend(normalize_named_entries(items.get(key, [])))

    # preserve order while deduplicating
    active_locations = list(dict.fromkeys(active_locations))
    active_factions = list(dict.fromkeys(active_factions))
    tracked_items = list(dict.fromkeys(tracked_items))

    return {
        "protagonist": protagonist if isinstance(protagonist, dict) else {},
        "active_characters": active_characters[:5],
        "active_locations": active_locations[:5],
        "active_factions": active_factions[:5],
        "tracked_items": tracked_items[:5],
    }


def summarize_recent_guardrails(learned: dict | None) -> dict:
    payload = (learned or {}).get("recent_guardrails", {})
    if not isinstance(payload, dict):
        payload = {}

    must_avoid = payload.get("must_avoid", [])
    must_preserve = payload.get("must_preserve", [])
    watchpoints = payload.get("next_chapter_watchpoints", [])

    def count_list(value: object) -> int:
        return len(value) if isinstance(value, list) else 0

    return {
        "has_recent_guardrails": bool(payload),
        "must_avoid_count": count_list(must_avoid),
        "must_preserve_count": count_list(must_preserve),
        "watchpoint_count": count_list(watchpoints),
        "expires_after_chapter": payload.get("expires_after_chapter"),
        "source_sidecar": ".mighty/learned-patterns.json" if payload else None,
    }


def build_active_context(
    *,
    state: dict,
    state_archive: dict | None,
    learned: dict | None,
    market: dict | None,
    gate: dict | None,
    launch_stack: dict | None,
    generated_at: str,
    recent_limit: int = 5,
) -> dict:
    recent_summaries = select_recent_summaries(state, state_archive, limit=recent_limit)
    total_summary_count = 0
    for source in ((state_archive or {}).get("summaries_index", {}), state.get("summaries_index", {})):
        if isinstance(source, dict):
            total_summary_count += len(source)

    learned = learned or {}
    gate = gate or {}
    launch_stack = launch_stack or {}
    guardrail_summary = summarize_recent_guardrails(learned)

    return {
        "version": "1.0",
        "generated_at": generated_at,
        "title": state.get("meta", {}).get("title", ""),
        "current_chapter": state.get("progress", {}).get("current_chapter", 0),
        "summary_window": {
            "count": total_summary_count,
            "recent_count": len(recent_summaries),
            "latest_chapter": recent_summaries[-1]["chapter"] if recent_summaries else None,
        },
        "recent_summaries": recent_summaries,
        "active_hooks": select_active_hooks(state),
        "relevant_entities": select_relevant_entities(state),
        "write_readiness": {
            "gate_status": gate.get("status", "unknown"),
            "blocking_gaps": gate.get("blocking_gaps", [])[:3] if isinstance(gate.get("blocking_gaps", []), list) else [],
            "minimal_next_action": gate.get("minimal_next_action"),
        },
        "launch_stack": {
            "active_launch_grammar": state.get("active_launch_grammar", ""),
            "active_primary_pivot": state.get("active_primary_pivot", ""),
            "launch_stack_phase": state.get("launch_stack_phase", ""),
            "launch_stack_drift_signal": state.get("launch_stack_drift_signal", "none"),
            "has_sidecar": bool(launch_stack),
        },
        "guardrail_summary": guardrail_summary,
        "market_signal_ids": [
            item.get("id")
            for item in (market.get("adjustments", []) if isinstance(market.get("adjustments", []), list) else [])
            if isinstance(item, dict) and item.get("id")
        ][:5],
    }


def main(argv: list[str] | None = None) -> dict:
    args = parse_args(argv)
    root = Path(args.project_root)
    mighty = root / ".mighty"
    mighty.mkdir(parents=True, exist_ok=True)
    loaded = load_state_and_sidecars(root)
    ts = args.timestamp or now_iso()
    payload = build_active_context(
        state=loaded["state"],
        state_archive=loaded["state_archive"],
        learned=loaded["learned"],
        market=loaded["market"],
        gate=loaded["gate"],
        launch_stack=loaded["launch_stack"],
        generated_at=ts,
        recent_limit=args.recent_limit,
    )
    sidecar_path = mighty / "active-context.json"
    sidecar_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    state = loaded["state"]
    if isinstance(state, dict):
        state["active_context"] = {
            "sidecar_file": ".mighty/active-context.json",
            "last_built": ts,
            "summary_window": payload["summary_window"],
            "hook_count": len(payload["active_hooks"]),
            "guardrail_count": (
                payload["guardrail_summary"]["must_avoid_count"]
                + payload["guardrail_summary"]["must_preserve_count"]
                + payload["guardrail_summary"]["watchpoint_count"]
            ),
        }
        (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    result = {
        "project": str(root),
        "active_context_file": str(sidecar_path),
        "summary_window": payload["summary_window"],
        "hook_count": len(payload["active_hooks"]),
        "guardrail_count": (
            payload["guardrail_summary"]["must_avoid_count"]
            + payload["guardrail_summary"]["must_preserve_count"]
            + payload["guardrail_summary"]["watchpoint_count"]
        ),
        "state_updated": str(mighty / "state.json"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    main()
