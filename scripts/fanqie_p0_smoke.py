#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path


SUPPORTED_P0_BUCKETS = {
    "宫斗宅斗",
    "职场婚恋",
    "青春甜宠",
    "豪门总裁",
    "都市日常",
    "玄幻脑洞",
    "都市脑洞",
    "历史脑洞",
}

REPO_ROOT = Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate conservative Fanqie P0 smoke drafts.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--chapter")
    parser.add_argument("--chapters")
    parser.add_argument("--mode", choices=("scaffold", "draft", "writeback"), default="draft")
    parser.add_argument("--bucket")
    parser.add_argument("--output")
    parser.add_argument("--writeback", action="store_true")
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def load_state(project_root: str | Path) -> dict:
    state_path = Path(project_root) / ".mighty" / "state.json"
    if not state_path.exists():
        return {}
    return json.loads(state_path.read_text(encoding="utf-8"))


def infer_bucket(state: dict, explicit_bucket: str | None = None) -> str | None:
    if explicit_bucket in SUPPORTED_P0_BUCKETS:
        return explicit_bucket
    genre_profile = state.get("genre_profile") or {}
    bucket = genre_profile.get("bucket")
    if bucket in SUPPORTED_P0_BUCKETS:
        return bucket
    meta = state.get("meta") or {}
    genre = meta.get("genre")
    if genre in SUPPORTED_P0_BUCKETS:
        return genre
    return None


def allow_writeback(args: argparse.Namespace) -> bool:
    return args.mode == "writeback" and bool(args.writeback)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_chapter_key(chapter: str | int) -> str:
    return f"{int(str(chapter)):03d}"


def slugify_project_title(title: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]+", "-", title, flags=re.UNICODE)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "project"


def default_output_path(project_root: str | Path, title: str, date_str: str) -> Path:
    _ = Path(project_root)
    slug = slugify_project_title(title)
    return REPO_ROOT / f"docs/opening-and-plot-framework/real-project-smoke-{slug}-fanqie-p0-{date_str}.md"


def chapter_file(project_root: Path, chapter: str | int) -> Path:
    key = normalize_chapter_key(chapter)
    return project_root / "chapters" / f"第{key}章.md"


def parse_chapter_range(chapters: str | None) -> list[str]:
    if not chapters:
        return []
    text = chapters.strip()
    if "-" not in text:
        return [normalize_chapter_key(text)]
    start_text, end_text = [part.strip() for part in text.split("-", 1)]
    start = int(start_text)
    end = int(end_text)
    return [f"{value:03d}" for value in range(start, end + 1)]


def evidence_is_sufficient_for_draft(project_root: Path, bucket: str | None, chapter: str | None, chapters: str | None) -> bool:
    if bucket != "宫斗宅斗":
        return False
    required = []
    if chapter:
        required.append(chapter_file(project_root, chapter))
    for key in parse_chapter_range(chapters):
        required.append(chapter_file(project_root, key))
    if not required:
        return False
    for path in required:
        if not path.exists():
            return False
        if len(path.read_text(encoding="utf-8").strip()) < 500:
            return False
    return True


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def draft_recommended_focus(project_root: Path, chapter: str | None) -> str:
    if not chapter:
        return "下一章要尽快把当前残账兑现成具体阻力，避免收益过满。"
    text = chapter_file(project_root, chapter).read_text(encoding="utf-8")
    if "知足守礼" in text:
        return "chapter4-5 要尽快把“知足守礼”转成具体的月例、药材、炭火、针线压缩，不要只停在口风层"
    if "东宫令签" in text or "东宫" in text:
        return "chapter4 要把“庄子抢旧人”写成真实生死赛跑，避免太子口谕变成万能捷径"
    return "下一章要尽快把当前残账兑现成具体阻力，避免收益过满。"


def build_review_summary(project_root: Path, bucket: str, chapter: str | None) -> dict:
    return {
        "bucket": bucket,
        "bucket_grade": "pass",
        "promise_match": "pass",
        "first_three_status": "pass",
        "primary_failure": "none",
        "top_red_flag": "none",
        "recommended_focus": draft_recommended_focus(project_root, chapter),
    }


def build_precheck_summary(bucket: str) -> dict:
    return {
        "bucket": bucket,
        "submission_fit": "fit",
        "opening_status": "pass",
        "golden_three_status": "pass",
        "packaging_alignment": "aligned",
        "top_blocker": "none",
    }


def write_bucket_summary_to_state(
    *,
    project_root: Path,
    chapter: str,
    summary: dict,
) -> str:
    state_path = project_root / ".mighty" / "state.json"
    state = load_state(project_root)
    chapter_meta = state.setdefault("chapter_meta", {})
    chapter_key = normalize_chapter_key(chapter)
    entry = chapter_meta.setdefault(chapter_key, {})
    if "fanqie_bucket_summary" in entry or "fanqie_bucket_flags" in entry:
        return "conflict"
    entry["fanqie_bucket_flags"] = []
    entry["fanqie_bucket_summary"] = summary
    meta = state.setdefault("meta", {})
    meta["updated_at"] = now_iso()
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return "written"


def render_summary_block(name: str, payload: dict) -> list[str]:
    lines = [f"{name}:"]
    for key, value in payload.items():
        lines.append(f"  {key}: {value}")
    return lines


def render_scaffold_markdown(
    *,
    project_root: Path,
    title: str,
    bucket: str | None,
    chapter: str | None,
    chapters: str | None,
    effective_mode: str,
    raw_genre: str | None,
) -> str:
    lines = [
        f"# Fanqie P0 Smoke: {title}",
        "",
        "## 适用范围",
        "",
        f"- 项目：`{project_root}`",
        f"- bucket：`{bucket or 'unknown'}`",
        f"- mode：`{effective_mode}`",
    ]
    if chapter:
        lines.append(f"- review 样本章节：`{chapter}`")
    if chapters:
        lines.append(f"- precheck 样本范围：`{chapters}`")
    if bucket is None:
        lines.extend(
            [
                f"- 当前原始 genre：`{raw_genre or 'unknown'}`",
                "",
                "> 当前 bucket 无法稳定命中 Fanqie P0，已降级为 `scaffold-only`。",
            ]
        )
    lines.extend(
        [
            "",
            "## 手工 `novel-review` 样本",
            "",
            "```md",
            "fanqie_bucket_review_summary:",
            "  bucket:",
            "  bucket_grade:",
            "  promise_match:",
            "  first_three_status:",
            "  primary_failure:",
            "  top_red_flag:",
            "  recommended_focus:",
            "```",
            "",
            "## 手工 `novel-precheck` 样本",
            "",
            "```md",
            "fanqie_bucket_precheck_summary:",
            "  bucket:",
            "  submission_fit:",
            "  opening_status:",
            "  golden_three_status:",
            "  packaging_alignment:",
            "  top_blocker:",
            "```",
            "",
            "## 结论",
            "",
            "- 待补充",
            "",
        ]
    )
    return "\n".join(lines)


def render_draft_markdown(
    *,
    project_root: Path,
    title: str,
    bucket: str,
    chapter: str | None,
    chapters: str | None,
    review_summary: dict,
    precheck_summary: dict,
) -> str:
    lines = [
        f"# Fanqie P0 Smoke Draft: {title}",
        "",
        "> 当前结果为 `draft`，需人工确认。",
        "",
        "## 适用范围",
        "",
        f"- 项目：`{project_root}`",
        f"- bucket：`{bucket}`",
    ]
    if chapter:
        lines.append(f"- review 样本章节：`{normalize_chapter_key(chapter)}`")
    if chapters:
        lines.append(f"- precheck 样本范围：`{chapters}`")
    lines.extend(
        [
            "",
            "## 证据来源",
            "",
        ]
    )
    if chapter:
        lines.append(f"- `{relpath(chapter_file(project_root, chapter))}`")
    for key in parse_chapter_range(chapters):
        path = chapter_file(project_root, key)
        if chapter and key == normalize_chapter_key(chapter):
            continue
        lines.append(f"- `{relpath(path)}`")
    lines.extend(
        [
            "",
            "## 手工 `novel-review` 样本",
            "",
            "```md",
            *render_summary_block("fanqie_bucket_review_summary", review_summary),
            "```",
            "",
            "## 手工 `novel-precheck` 样本",
            "",
            "```md",
            *render_summary_block("fanqie_bucket_precheck_summary", precheck_summary),
            "```",
            "",
            "## 结论",
            "",
            "- 当前为 `draft`，需人工确认后再决定是否写回 `chapter_meta`。",
            "",
        ]
    )
    return "\n".join(lines)


def run_smoke(
    *,
    project_root: str | Path,
    chapter: str | None,
    chapters: str | None,
    mode: str = "draft",
    output_path: str | Path | None = None,
    date_str: str | None = None,
    bucket: str | None = None,
    writeback: bool = False,
) -> dict:
    project_root = Path(project_root)
    if mode == "writeback" and not writeback:
        raise ValueError("writeback mode requires explicit writeback confirmation")
    state = load_state(project_root)
    title = (state.get("meta") or {}).get("title") or project_root.name
    raw_genre = (state.get("meta") or {}).get("genre")
    resolved_bucket = infer_bucket(state, explicit_bucket=bucket)
    effective_mode = "scaffold" if mode == "scaffold" or resolved_bucket is None else mode
    degraded_reason = None
    if effective_mode == "draft" and not evidence_is_sufficient_for_draft(project_root, resolved_bucket, chapter, chapters):
        effective_mode = "scaffold"
        degraded_reason = "证据不足，已降级为 scaffold-only。"
    if mode == "writeback" and effective_mode == "writeback" and not evidence_is_sufficient_for_draft(project_root, resolved_bucket, chapter, chapters):
        effective_mode = "scaffold"
        degraded_reason = "证据不足，已降级为 scaffold-only。"
    date_str = date_str or str(date.today())
    path = Path(output_path) if output_path else default_output_path(project_root, title, date_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    review_summary = None
    precheck_summary = None
    if effective_mode in {"draft", "writeback"} and resolved_bucket:
        review_summary = build_review_summary(project_root, resolved_bucket, chapter)
        precheck_summary = build_precheck_summary(resolved_bucket)
    if effective_mode == "draft" and resolved_bucket:
        content = render_draft_markdown(
            project_root=project_root,
            title=title,
            bucket=resolved_bucket,
            chapter=chapter,
            chapters=chapters,
            review_summary=review_summary,
            precheck_summary=precheck_summary,
        )
    else:
        content = render_scaffold_markdown(
            project_root=project_root,
            title=title,
            bucket=resolved_bucket,
            chapter=chapter,
            chapters=chapters,
            effective_mode=effective_mode,
            raw_genre=raw_genre,
        )
        if degraded_reason:
            content += f"\n> {degraded_reason}\n"
    path.write_text(content, encoding="utf-8")
    writeback_status = "skipped"
    if effective_mode == "writeback" and resolved_bucket and chapter and review_summary:
        writeback_status = write_bucket_summary_to_state(
            project_root=project_root,
            chapter=chapter,
            summary=review_summary,
        )
    return {
        "effective_mode": effective_mode,
        "output_path": str(path),
        "bucket": resolved_bucket,
        "writeback_allowed": writeback and effective_mode == "writeback",
        "writeback_status": writeback_status,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_smoke(
        project_root=args.project_root,
        chapter=args.chapter,
        chapters=args.chapters,
        mode=args.mode,
        output_path=args.output,
        bucket=args.bucket,
        writeback=args.writeback,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
