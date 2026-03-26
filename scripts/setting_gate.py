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

import strong_quality_gate
import fanqie_launch_stack
import sidecar_freshness
from trace_log import append_trace


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
    parser.add_argument("--candidates-file", default="", help="Optional research candidates JSON file")
    parser.add_argument("--report-only", action="store_true")
    return parser.parse_args()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_candidates_file(path: Path | str | None) -> list[dict]:
    if not path:
        return []
    payload = _read_json(Path(path))
    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list):
        raise ValueError("candidates file must contain a top-level 'candidates' array")
    return [item for item in candidates if isinstance(item, dict)]


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


def detect_gate_requirements(project_root: Path, stage: str) -> dict:
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
    chapter_outline_dir = project_root / "大纲" / "章纲"
    chapter_outline_count = len(list(chapter_outline_dir.glob("*.md"))) if chapter_outline_dir.exists() else 0
    return {
        "project_root": project_root,
        "stage": stage,
        "state": state,
        "policy": policy,
        "outline_text": outline_text,
        "truth_result": truth_result,
        "chapter_outline_count": chapter_outline_count,
    }


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


def _build_minimal_next_action(project_root: Path, stage: str, blocking_gaps: list[dict], review_items: list[dict]) -> dict:
    rerun_cmd = f"python3 scripts/setting_gate.py {project_root} --stage {stage}"
    if any(item.get("source") == "mcp" and item.get("blocking") for item in review_items):
        return {
            "action": "review-sync-queue",
            "reason": "high-risk research candidate requires confirmation before canon use",
            "suggested_commands": [
                f"python3 scripts/review-sync-queue.py {project_root} --list",
                rerun_cmd,
            ],
        }

    blocking_keys = {gap.get("key", "") for gap in blocking_gaps}
    if blocking_keys & {"kinship_truth", "office_truth", "world_rule_support"}:
        return {
            "action": "novel-setting",
            "reason": "project-local truth source is missing for the current outline route",
            "suggested_commands": [
                rerun_cmd,
            ],
        }

    if blocking_gaps:
        return {
            "action": "novel-setting",
            "reason": "gate is blocked and needs project-local setting completion",
            "suggested_commands": [
                rerun_cmd,
            ],
        }

    if review_items:
        return {
            "action": "review-sync-queue",
            "reason": "gate has queued review items that should be triaged before writing",
            "suggested_commands": [
                f"python3 scripts/review-sync-queue.py {project_root} --list",
            ],
        }

    return {
        "action": "none",
        "reason": "gate passed",
        "suggested_commands": [],
    }


def _is_fanqie_project(state: dict) -> bool:
    platform = str(state.get("meta", {}).get("platform", "")).strip().lower()
    return platform == "番茄"


def maybe_auto_compile_launch_stack(project_root: Path, state: dict, *, stage: str, report_only: bool) -> dict:
    if stage != "outline":
        return {"status": "not_applicable", "reason": "stage_not_outline"}
    if not _is_fanqie_project(state):
        return {"status": "not_applicable", "reason": "not_fanqie"}

    sidecar_path = project_root / ".mighty" / "launch-stack.json"
    if sidecar_path.exists() and not fanqie_launch_stack._is_preselect_placeholder(sidecar_path):
        return {"status": "already_ready", "reason": "locked_sidecar_present", "sidecar_file": str(sidecar_path)}
    if report_only:
        return {"status": "report_only_skipped", "reason": "report_only", "sidecar_file": str(sidecar_path)}

    outline_text = fanqie_launch_stack.load_total_outline(project_root)
    chapter_texts = fanqie_launch_stack.load_chapter_texts(project_root, "001-003")
    chapter_keys = sorted(chapter_texts.keys())
    result = fanqie_launch_stack.compile_launch_stack(
        state,
        outline_text,
        chapter_texts,
        chapter=chapter_keys[-1] if chapter_keys else None,
        chapters=f"{chapter_keys[0]}-{chapter_keys[-1]}" if chapter_keys else None,
    )
    if len(chapter_keys) < 3:
        result["phase"] = "draft"
        result["drift_signal"] = "watch"
        result["reselect_note"] = "auto-compiled from outline-only or partial early chapters"
    fanqie_launch_stack.write_launch_stack_sidecars(project_root, result, force=True)
    fanqie_launch_stack.mirror_launch_stack_to_state(project_root, result)
    append_trace(
        project_root,
        event="launch_stack.auto_compiled",
        skill="setting-gate",
        result="success",
        details={
            "stage": stage,
            "sidecar_file": str(sidecar_path),
            "compiled_phase": result["phase"],
            "chapter_count": len(chapter_keys),
        },
    )
    return {
        "status": "compiled",
        "reason": "fanqie_outline_gate_autocompile",
        "sidecar_file": str(sidecar_path),
        "launch_grammar": result["launch_grammar"]["primary"],
        "primary_pivot": result["primary_pivot"],
    }


def enrich_gate_result(
    detection: dict,
    *,
    report_only: bool,
    mcp_candidates: list[dict] | None = None,
) -> dict:
    project_root = detection["project_root"]
    stage = detection["stage"]
    state = detection["state"]
    policy = detection["policy"]
    outline_text = detection["outline_text"]
    truth_result = detection["truth_result"]
    chapter_outline_count = detection["chapter_outline_count"]

    launch_stack_action = maybe_auto_compile_launch_stack(
        project_root,
        state,
        stage=stage,
        report_only=report_only,
    )
    auto_created_files = materialize_local_cards(project_root, state, policy, stage, report_only)
    graded = grade_candidates(mcp_candidates or [], policy)

    blocking_gaps = list(truth_result.get("missing", []))
    if graded["status"] == "blocked":
        blocking_gaps.extend(
            [
                {
                    "key": item["kind"],
                    "source": item["source"],
                    "name": item["name"],
                }
                for item in graded["review_items"]
                if item.get("blocking")
            ]
        )

    if blocking_gaps:
        status = "blocked"
    elif graded["status"] == "review_required":
        status = "review_required"
    else:
        status = "passed"

    mcp_candidates_list = mcp_candidates or []
    result = {
        "version": "1.0",
        "status": status,
        "checked_after": stage,
        "launch_stack_action": launch_stack_action,
        "blocking_gaps": blocking_gaps,
        "auto_created_files": auto_created_files,
        "review_queue_count": len(graded["review_items"]),
        "mcp_used": bool(mcp_candidates_list),
        "mcp_sources": sorted(
            {
                item.get("source", "")
                for item in mcp_candidates_list
                if item.get("source")
            }
        ),
        "review_items": graded["review_items"],
        "truth_sources_checked": truth_result["used"],
        "minimal_next_action": _build_minimal_next_action(
            project_root,
            stage,
            blocking_gaps,
            graded["review_items"],
        ),
        "freshness": sidecar_freshness.build_freshness(
            repo_root=SCRIPT_DIR.parent,
            artifact_key="setting-gate",
            timestamp=now_iso(),
            project_root=project_root,
            inputs={
                "state.json": {
                    "path": ".mighty/state.json",
                    "updated_at": state.get("meta", {}).get("updated_at"),
                    "current_chapter": state.get("progress", {}).get("current_chapter"),
                },
                "outline": {
                    "path": "大纲/总纲.md + 大纲/章纲/*.md",
                    "has_text": bool(outline_text.strip()),
                    "chapter_outline_count": chapter_outline_count,
                },
                "research-candidates.json": {
                    "path": ".mighty/research-candidates.json",
                    "count": len(mcp_candidates_list),
                },
            },
        ),
    }
    return result


def persist_gate_result(project_root: Path, stage: str, result: dict, report_only: bool) -> None:
    _write_gate_state(project_root, result, report_only)
    _write_sync_review(project_root, stage, result.get("review_items", []), report_only)


def trace_gate_result(project_root: Path, stage: str, result: dict, report_only: bool) -> None:
    if report_only:
        return
    append_trace(
        project_root,
        event=f"setting_gate.{result['status']}",
        skill="setting-gate",
        result=result["status"],
        details={
            "stage": stage,
            "blocking_gap_count": len(result["blocking_gaps"]),
            "review_queue_count": result["review_queue_count"],
            "launch_stack_action": result["launch_stack_action"].get("status"),
        },
    )


def run_gate(
    *,
    project_root: Path,
    stage: str = "outline",
    report_only: bool = False,
    mcp_candidates: list[dict] | None = None,
) -> dict:
    detection = detect_gate_requirements(project_root, stage)
    result = enrich_gate_result(
        detection,
        report_only=report_only,
        mcp_candidates=mcp_candidates,
    )
    persist_gate_result(detection["project_root"], stage, result, report_only)
    trace_gate_result(detection["project_root"], stage, result, report_only)
    return result


def main() -> None:
    args = parse_args()
    result = run_gate(
        project_root=Path(args.project_root),
        stage=args.stage,
        report_only=args.report_only,
        mcp_candidates=load_candidates_file(args.candidates_file),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
