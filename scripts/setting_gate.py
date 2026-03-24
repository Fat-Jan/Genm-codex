#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import strong_quality_gate


GATE_BEGIN = "<!-- SETTING-GATE:BEGIN -->"
GATE_END = "<!-- SETTING-GATE:END -->"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_policy() -> dict:
    policy_path = Path(__file__).resolve().parents[1] / "docs" / "setting-gate-policy.json"
    return json.loads(policy_path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local-first setting enrichment and gate evaluation.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--stage", choices=["init", "outline", "write", "write-post"], default="outline")
    parser.add_argument("--report-only", action="store_true")
    return parser.parse_args()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_state(project_root: Path) -> dict:
    return _read_json(project_root / ".mighty" / "state.json")


def read_outline_text(project_root: Path) -> str:
    parts: list[str] = []
    total_outline = project_root / "大纲" / "总纲.md"
    if total_outline.exists():
        parts.append(total_outline.read_text(encoding="utf-8"))
    chapter_dir = project_root / "大纲" / "章纲"
    if chapter_dir.exists():
        for path in sorted(chapter_dir.glob("*.md"))[:5]:
            parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def available_setting_paths(project_root: Path) -> list[str]:
    setting_root = project_root / "设定集"
    if not setting_root.exists():
        return []
    return sorted(str(path.relative_to(project_root)).replace("\\", "/") for path in setting_root.rglob("*.md"))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _replace_generated_block(existing: str, block: str) -> str:
    if GATE_BEGIN in existing and GATE_END in existing:
        start = existing.index(GATE_BEGIN)
        end = existing.index(GATE_END) + len(GATE_END)
        return existing[:start] + block + existing[end:]
    if existing.endswith("\n"):
        return existing + "\n" + block + "\n"
    return existing + "\n\n" + block + "\n"


def _write_generated_card(path: Path, title: str, body_lines: list[str]) -> None:
    block = "\n".join([GATE_BEGIN, *body_lines, GATE_END])
    if path.exists():
        new_text = _replace_generated_block(path.read_text(encoding="utf-8"), block)
    else:
        new_text = "\n".join([f"# {title}", "", block, ""])
    path.write_text(new_text, encoding="utf-8")


def _stage_tag(policy: dict, stage: str) -> str:
    return policy.get("coverage_requirements", {}).get("stage_tags", {}).get(stage, f"{stage}-generated")


def _extract_active_characters(state: dict) -> list[dict[str, Any]]:
    active = state.get("entities", {}).get("characters", {}).get("active", [])
    result = []
    seen: set[str] = set()
    for item in active:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name or name in seen:
            continue
        seen.add(name)
        result.append({
            "name": name,
            "role": str(item.get("role") or "重要角色"),
            "relationship": str(item.get("relationship") or "待补充"),
        })
    return result


def _extract_locations(state: dict) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    protagonist_current = (
        state.get("entities", {})
        .get("characters", {})
        .get("protagonist", {})
        .get("location", {})
        .get("current")
    )
    for item in [
        protagonist_current,
        state.get("entities", {}).get("locations", {}).get("current"),
        *state.get("entities", {}).get("locations", {}).get("important", []),
    ]:
        name = str(item or "").strip()
        if not name or name in seen:
            continue
        seen.add(name)
        out.append(name)
    return out


def _extract_factions(state: dict) -> list[str]:
    factions = state.get("entities", {}).get("factions", {}).get("active", [])
    out: list[str] = []
    seen: set[str] = set()
    for item in factions:
        name = str(item if not isinstance(item, dict) else item.get("name", "")).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        out.append(name)
    return out


def _extract_items(state: dict) -> list[str]:
    protagonist = state.get("entities", {}).get("characters", {}).get("protagonist", {})
    items = [
        *protagonist.get("inventory", []),
        *state.get("entities", {}).get("items", {}).get("tracked", []),
        *state.get("entities", {}).get("items", {}).get("protagonist_inventory", []),
    ]
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        name = str(item).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        out.append(name)
    return out


def materialize_local_cards(project_root: Path, state: dict, policy: dict, stage: str, report_only: bool) -> list[str]:
    created: list[str] = []
    stage_tag = _stage_tag(policy, stage)

    char_dir = project_root / "设定集" / "角色"
    loc_dir = project_root / "设定集" / "地点"
    fac_dir = project_root / "设定集" / "势力"
    item_dir = project_root / "设定集" / "物品"
    for directory in (char_dir, loc_dir, fac_dir, item_dir):
        ensure_dir(directory)

    protagonist_name = str(
        state.get("entities", {}).get("characters", {}).get("protagonist", {}).get("name", "")
    ).strip()

    for character in _extract_active_characters(state)[: policy.get("candidate_rules", {}).get("characters", {}).get("max_auto_create", 12)]:
        if character["name"] == protagonist_name:
            continue
        rel_path = Path("设定集") / "角色" / f"{character['name']}.md"
        if rel_path.as_posix() in available_setting_paths(project_root):
            continue
        created.append(rel_path.as_posix())
        if report_only:
            continue
        _write_generated_card(
            project_root / rel_path,
            character["name"],
            [
                f"- source_tag: {stage_tag}",
                f"- generated_at: {now_iso()}",
                f"- 角色定位：{character['role']}",
                f"- 与主角关系：{character['relationship']}",
            ],
        )

    for location in _extract_locations(state)[: policy.get("candidate_rules", {}).get("locations", {}).get("max_auto_create", 8)]:
        rel_path = Path("设定集") / "地点" / f"{location}.md"
        if rel_path.as_posix() in available_setting_paths(project_root):
            continue
        created.append(rel_path.as_posix())
        if report_only:
            continue
        _write_generated_card(
            project_root / rel_path,
            location,
            [
                f"- source_tag: {stage_tag}",
                f"- generated_at: {now_iso()}",
                "- 类型：重要地点",
                "- 当前状态：由 setting gate 根据运行态与大纲骨架自动补卡。",
            ],
        )

    for faction in _extract_factions(state)[: policy.get("candidate_rules", {}).get("factions", {}).get("max_auto_create", 8)]:
        rel_path = Path("设定集") / "势力" / f"{faction}.md"
        if rel_path.as_posix() in available_setting_paths(project_root):
            continue
        created.append(rel_path.as_posix())
        if report_only:
            continue
        _write_generated_card(
            project_root / rel_path,
            faction,
            [
                f"- source_tag: {stage_tag}",
                f"- generated_at: {now_iso()}",
                "- 类型：关键组织/单位",
                "- 当前状态：由 setting gate 自动生成的势力骨架。",
            ],
        )

    for item in _extract_items(state)[: policy.get("candidate_rules", {}).get("items", {}).get("max_auto_create", 8)]:
        rel_path = Path("设定集") / "物品" / f"{item}.md"
        if rel_path.as_posix() in available_setting_paths(project_root):
            continue
        created.append(rel_path.as_posix())
        if report_only:
            continue
        _write_generated_card(
            project_root / rel_path,
            item,
            [
                f"- source_tag: {stage_tag}",
                f"- generated_at: {now_iso()}",
                "- 类型：关键物品",
                "- 当前状态：由 setting gate 自动生成的物品骨架。",
            ],
        )

    return created


def grade_candidates(candidates: list[dict], policy: dict) -> dict:
    review_items: list[dict] = []
    status = "passed"
    for candidate in candidates:
        source = str(candidate.get("source") or "local")
        kind = str(candidate.get("kind") or "unknown")
        risk = "low"
        requires_user_confirmation = False
        blocking = False
        if source == "mcp":
            risk = "high"
            requires_user_confirmation = True
            blocking = True
        elif kind == "rule":
            risk = "medium"

        if risk != "low":
            review_items.append({
                "name": candidate.get("name", ""),
                "kind": kind,
                "source": source,
                "confidence": candidate.get("confidence", "medium"),
                "risk": risk,
                "requires_user_confirmation": requires_user_confirmation,
                "blocking": blocking,
            })
        if blocking:
            status = "blocked"
        elif review_items and status != "blocked":
            status = "review_required"
    return {"status": status, "review_items": review_items}


def _write_sync_review(project_root: Path, stage: str, review_items: list[dict], report_only: bool) -> None:
    if report_only:
        return
    path = project_root / ".mighty" / "sync-review.json"
    existing_reviewed = []
    if path.exists():
        try:
            existing_reviewed = _read_json(path).get("reviewed_entities", [])
        except Exception:
            existing_reviewed = []
    payload = {
        "version": "1.0",
        "generated_at": now_iso(),
        "ambiguous_entities": [
            {
                "name": item.get("name", ""),
                "kind": item.get("kind", ""),
                "reason": item.get("risk", ""),
                "source_stage": stage,
                "confidence": item.get("confidence", "medium"),
                "requires_user_confirmation": item.get("requires_user_confirmation", False),
                "blocking": item.get("blocking", False),
                "candidate_files": item.get("candidate_files", []),
            }
            for item in review_items
        ],
        "reviewed_entities": existing_reviewed,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_gate_state(project_root: Path, result: dict, report_only: bool) -> None:
    if report_only:
        return
    ensure_dir(project_root / ".mighty")
    path = project_root / ".mighty" / "setting-gate.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


def run_gate(
    *,
    project_root: Path,
    stage: str = "outline",
    report_only: bool = False,
    mcp_candidates: list[dict] | None = None,
) -> dict:
    project_root = Path(project_root)
    state = load_state(project_root)
    policy = load_policy()
    outline_text = read_outline_text(project_root)
    available_paths = available_setting_paths(project_root)
    strong_policy = strong_quality_gate.load_policy()
    truth_result = strong_quality_gate.detect_missing_truth_sources(
        outline_text=outline_text,
        route_signal={},
        available_paths=available_paths,
        policy=strong_policy,
    )

    auto_created_files = materialize_local_cards(project_root, state, policy, stage, report_only)
    graded = grade_candidates(mcp_candidates or [], policy)

    blocking_gaps = truth_result["missing"]
    if graded["status"] == "blocked":
        blocking_gaps = blocking_gaps + [
            {
                "key": item["kind"],
                "source": item["source"],
                "name": item["name"],
            }
            for item in graded["review_items"]
            if item.get("blocking")
        ]

    status = "passed"
    if blocking_gaps:
        status = "blocked"
    elif graded["status"] == "review_required":
        status = "review_required"

    result = {
        "version": "1.0",
        "status": status,
        "checked_after": stage,
        "blocking_gaps": blocking_gaps,
        "auto_created_files": auto_created_files,
        "review_queue_count": len(graded["review_items"]),
        "mcp_used": bool(mcp_candidates),
        "mcp_sources": sorted({item.get("source", "") for item in (mcp_candidates or []) if item.get("source")}),
        "review_items": graded["review_items"],
        "truth_sources_checked": truth_result["used"],
    }
    _write_gate_state(project_root, result, report_only)
    _write_sync_review(project_root, stage, graded["review_items"], report_only)
    return result


def main() -> None:
    args = parse_args()
    result = run_gate(project_root=Path(args.project_root), stage=args.stage, report_only=args.report_only)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
