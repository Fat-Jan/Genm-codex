from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


DEFAULT_RETENTION_RULES = [
    "first-page-hook",
    "chapter-end-hook",
    "hook-handover",
    "first-hard-payoff",
    "half-win-with-residual",
    "no-foolish-humiliation",
    "early-stability",
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile a conservative Fanqie launch stack.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--chapter")
    parser.add_argument("--chapters")
    parser.add_argument("--mode", choices=("draft", "writeback"), default="draft")
    parser.add_argument("--output")
    parser.add_argument("--writeback", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args(argv)


def allow_writeback(args: argparse.Namespace) -> bool:
    return args.mode == "writeback" and bool(args.writeback)


def load_state(project_root: Path) -> dict:
    return json.loads((project_root / ".mighty" / "state.json").read_text(encoding="utf-8"))


def load_total_outline(project_root: Path) -> str:
    path = project_root / "大纲" / "总纲.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def normalize_chapter_key(chapter: str | int) -> str:
    return f"{int(str(chapter)):03d}"


def expand_chapter_range(chapters: str | None) -> list[str]:
    if not chapters:
        return []
    if "-" not in chapters:
        return [normalize_chapter_key(chapters)]
    start, end = chapters.split("-", 1)
    start_num = int(start)
    end_num = int(end)
    return [f"{num:03d}" for num in range(start_num, end_num + 1)]


def load_chapter_texts(project_root: Path, chapters: str | None) -> dict[str, str]:
    chapter_map: dict[str, str] = {}
    for key in expand_chapter_range(chapters):
        path = project_root / "chapters" / f"第{key}章.md"
        if path.exists():
            chapter_map[key] = path.read_text(encoding="utf-8")
    return chapter_map


def _join_text_sources(state: dict, outline_text: str, chapter_texts: dict[str, str]) -> str:
    parts = [
        state.get("meta", {}).get("title", ""),
        state.get("meta", {}).get("genre", ""),
        state.get("genre_profile", {}).get("bucket", ""),
        outline_text,
        *chapter_texts.values(),
    ]
    return "\n".join(part for part in parts if part)


def _score_keywords(text: str, keywords: Iterable[str]) -> int:
    return sum(text.count(keyword) for keyword in keywords)


def infer_pivot_candidates(state: dict, outline_text: str, chapter_texts: dict[str, str]) -> list[dict]:
    text = _join_text_sources(state, outline_text, chapter_texts)
    scores = {
        "character-conflict": _score_keywords(text, ["离婚", "前夫", "合伙人", "绑定", "站位", "关系", "同居"]),
        "rule-world": _score_keywords(text, ["规则", "怪谈", "禁忌", "法则"]),
        "gift-system": _score_keywords(text, ["系统", "金手指", "外挂", "面板"]),
        "mystery-gap": _score_keywords(text, ["真相", "旧案", "线索", "内幕", "供词", "秘密"]),
        "transgressive-action": _score_keywords(text, ["抢婚", "背刺", "越线", "押给了我", "改口"]),
        "inciting-event": _score_keywords(text, ["那天", "试运营", "并购", "裁我", "赐婚", "夺"]),
    }
    if not any(scores.values()):
        scores["inciting-event"] = 1
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return [{"id": pivot_id, "score": float(score)} for pivot_id, score in ordered if score > 0][:3]


def infer_launch_grammar_candidates(
    state: dict, pivot_candidates: list[dict], outline_text: str, chapter_texts: dict[str, str]
) -> list[dict]:
    text = _join_text_sources(state, outline_text, chapter_texts)
    bucket = state.get("genre_profile", {}).get("bucket", "") or state.get("meta", {}).get("genre", "")
    top_pivot = pivot_candidates[0]["id"] if pivot_candidates else "inciting-event"
    scores = {
        "oppression-breakout": _score_keywords(text, ["压制", "反击", "翻盘", "不公", "打脸"]),
        "bonding-reversal": _score_keywords(text, ["离婚", "前夫", "绑定", "合伙人", "同居", "关系"]),
        "rule-trial": _score_keywords(text, ["规则", "系统", "试错", "异常", "法则"]),
        "resource-climb": _score_keywords(text, ["资源", "灵石", "试炼", "升级", "拍卖", "宗门"]),
        "investigation-reveal": _score_keywords(text, ["旧案", "线索", "真相", "供词", "追查"]),
        "ensemble-return": _score_keywords(text, ["邻居", "楼道", "群像", "整栋楼", "社区"]),
    }

    if top_pivot == "character-conflict":
        scores["bonding-reversal"] += 3
    if top_pivot == "mystery-gap":
        scores["investigation-reveal"] += 3
    if top_pivot == "gift-system":
        scores["rule-trial"] += 2
    if "职场婚恋" in bucket or "豪门总裁" in bucket:
        scores["bonding-reversal"] += 2
    if "玄幻脑洞" in bucket or "历史脑洞" in bucket:
        scores["resource-climb"] += 2

    if not any(scores.values()):
        scores["oppression-breakout"] = 1

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return [{"id": grammar_id, "score": float(score)} for grammar_id, score in ordered if score > 0][:3]


def build_premise_line(state: dict, outline_text: str) -> str:
    title = state.get("meta", {}).get("title", "").strip()
    if title:
        return title
    first_line = next((line.strip() for line in outline_text.splitlines() if line.strip()), "")
    return first_line or "待补一句话故事"


def confidence_label(primary_score: float) -> str:
    if primary_score >= 5:
        return "high"
    if primary_score >= 2:
        return "medium"
    return "low"


def _review_watchpoints(primary_grammar: str) -> list[str]:
    mapping = {
        "bonding-reversal": ["关系推进是否只有口头拉扯", "第一次站位变化是否留下现实后果"],
        "resource-climb": ["收益是否白拿", "升级是否缺阶段代价"],
        "investigation-reveal": ["前三章是否至少翻一次信息页", "追查是否只靠巧合"],
        "rule-trial": ["规则是否只讲不演", "试错是否真正付出成本"],
        "ensemble-return": ["群像是否只有热闹没有主入口", "回流残账是否成立"],
    }
    return mapping.get(primary_grammar, ["第一页是否尽快入事", "前三章是否存在一次硬兑现"])


def compile_launch_stack(
    state: dict, outline_text: str, chapter_texts: dict[str, str], chapter: str | None = None, chapters: str | None = None
) -> dict:
    pivot_candidates = infer_pivot_candidates(state, outline_text, chapter_texts)
    grammar_candidates = infer_launch_grammar_candidates(state, pivot_candidates, outline_text, chapter_texts)
    primary_pivot = pivot_candidates[0]["id"] if pivot_candidates else "inciting-event"
    secondary_pivot = pivot_candidates[1]["id"] if len(pivot_candidates) > 1 else ""
    primary_grammar = grammar_candidates[0]["id"] if grammar_candidates else "oppression-breakout"
    grammar_confidence = confidence_label(grammar_candidates[0]["score"] if grammar_candidates else 0)

    return {
        "version": "1.0",
        "phase": "draft",
        "premise_line": build_premise_line(state, outline_text),
        "primary_pivot": primary_pivot,
        "secondary_pivot": secondary_pivot,
        "launch_grammar": {
            "primary": primary_grammar,
            "candidates": grammar_candidates,
            "confidence": grammar_confidence,
        },
        "retention_protocol": {
            "enabled_rules": list(DEFAULT_RETENTION_RULES),
            "priority_rules": ["first-page-hook", "chapter-end-hook", "first-hard-payoff"],
            "violations": [],
        },
        "compiler_output": {
            "outline_focus": [
                f"锁定 `{primary_pivot}` 支点",
                f"前 1-3 章按 `{primary_grammar}` 推进",
            ],
            "chapter_1_3_targets": [
                "第001章给首屏钩子",
                "第002章给交换、误判或加压",
                "第003章给第一次硬兑现或半胜带残账",
            ],
            "review_watchpoints": _review_watchpoints(primary_grammar),
            "precheck_risks": [
                "前三章只有 promise 没有换账",
                "章末钩子没有接力",
            ],
            "package_guardrails": [
                "不要把未兑现的大卖点包装成已兑现事实",
            ],
        },
        "hook_ledger_summary": {"count": 0},
        "payoff_ledger_summary": {"count": 0},
        "confidence": grammar_confidence,
        "drift_signal": "none",
        "reselect_note": "",
        "target_chapter": normalize_chapter_key(chapter) if chapter else "",
        "chapter_range": chapters or "",
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_launch_stack_sidecars(project_root: Path, result: dict, force: bool = False) -> None:
    mighty = project_root / ".mighty"
    mighty.mkdir(parents=True, exist_ok=True)
    sidecar_path = mighty / "launch-stack.json"
    if sidecar_path.exists() and not force:
        raise RuntimeError("launch-stack.json already exists")

    _write_json(sidecar_path, result)

    for name in ("hook-ledger.json", "payoff-ledger.json"):
        ledger_path = mighty / name
        if not ledger_path.exists():
            _write_json(ledger_path, {"version": "1.0", "items": []})


def mirror_launch_stack_to_state(project_root: Path, result: dict) -> None:
    state = load_state(project_root)
    state["active_launch_grammar"] = result["launch_grammar"]["primary"]
    state["active_primary_pivot"] = result["primary_pivot"]
    state["launch_stack_phase"] = result["phase"]
    state["launch_stack_drift_signal"] = result["drift_signal"]
    _write_json(project_root / ".mighty" / "state.json", state)


def run_launch_stack(
    project_root: Path,
    chapter: str | None = None,
    chapters: str | None = None,
    output_path: Path | None = None,
    mode: str = "draft",
    writeback: bool = False,
    force: bool = False,
) -> dict:
    state = load_state(project_root)
    outline_text = load_total_outline(project_root)
    chapter_texts = load_chapter_texts(project_root, chapters)
    result = compile_launch_stack(state, outline_text, chapter_texts, chapter=chapter, chapters=chapters)
    result["effective_mode"] = mode
    if output_path is not None:
        _write_json(output_path, result)
    if mode == "writeback":
        if not writeback:
            raise RuntimeError("writeback requires explicit flag")
        write_launch_stack_sidecars(project_root, result, force=force)
        mirror_launch_stack_to_state(project_root, result)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = run_launch_stack(
        project_root=Path(args.project_root),
        chapter=args.chapter,
        chapters=args.chapters,
        output_path=Path(args.output) if args.output else None,
        mode=args.mode,
        writeback=args.writeback,
        force=args.force,
    )
    if not args.output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
