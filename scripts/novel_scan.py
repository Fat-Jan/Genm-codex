#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from acquire_source_text import acquire_article, now_iso  # noqa: E402
from prototype_fanqie_font_map import apply_mapping, build_approximate_mapping_for_text  # noqa: E402


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def contains_private_use_chars(text: str | None) -> bool:
    if not text:
        return False
    return any("\uE000" <= ch <= "\uF8FF" for ch in text)


def strip_private_use_chars(text: str | None) -> str:
    if not text:
        return ""
    return "".join(ch for ch in text if not ("\uE000" <= ch <= "\uF8FF"))


def retains_enough_text_after_strip(original: str, sanitized: str, *, min_ratio: float, min_length: int) -> bool:
    original_no_space = normalize_space(original)
    sanitized_no_space = normalize_space(sanitized)
    if len(sanitized_no_space) < min_length:
        return False
    if not contains_private_use_chars(original_no_space):
        return True
    original_len = len(original_no_space)
    if original_len == 0:
        return False
    return len(sanitized_no_space) / original_len >= min_ratio


def extract_font_url_note(notes: list[str] | None) -> str | None:
    for note in notes or []:
        if note.startswith("font_url:"):
            return note.removeprefix("font_url:").strip() or None
    return None


def download_font_to_temp(url: str) -> Path:
    request = Request(url, headers={"User-Agent": "Genm-codex/1.0 (+fanqie font decode)"})
    suffix = Path(urlparse(url).path).suffix or ".bin"
    with urlopen(request, timeout=30) as response:
        payload = response.read()
    handle = tempfile.NamedTemporaryFile(prefix="genm-fanqie-font-", suffix=suffix, delete=False)
    try:
        handle.write(payload)
        return Path(handle.name)
    finally:
        handle.close()


def decode_fanqie_obfuscated_body(
    *,
    body: str | None,
    notes: list[str] | None,
    reference_font_path: Path | None,
    reference_font_number: int | None = None,
    download_font_fn=download_font_to_temp,
    suggest_mapping_fn=build_approximate_mapping_for_text,
) -> str | None:
    if not body or not reference_font_path or not contains_private_use_chars(body):
        return body
    font_url = extract_font_url_note(notes)
    if not font_url:
        return body
    temp_path: Path | None = None
    try:
        temp_path = download_font_fn(font_url)
        mapping = suggest_mapping_fn(
            temp_path,
            reference_font_path,
            body,
            reference_font_number=reference_font_number,
        )
        if not mapping:
            return body
        return apply_mapping(body, mapping)
    except Exception:
        return body
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()


def summarize_body(text: str | None, limit: int = 180) -> str:
    if not text:
        return ""
    compact = normalize_space(text)
    return compact[:limit]


def focus_excerpt(url: str, text: str | None, limit: int = 240, *, allow_partial_sanitization: bool = False) -> str:
    if not text:
        return ""
    compact = normalize_space(text)
    hostname = urlparse(url).netloc.lower()
    if hostname.endswith("fanqienovel.com"):
        anchors = ["统计时间截止至", "榜单说明", "01 -", "01-"]
        start = None
        for anchor in anchors:
            idx = compact.find(anchor)
            if idx != -1:
                start = idx
                break
        if start is not None:
            trimmed = compact[start:]
            rank_idx = trimmed.find("01 -")
            if rank_idx == -1:
                rank_idx = trimmed.find("01-")
            if rank_idx != -1:
                trimmed = trimmed[rank_idx:]
            if contains_private_use_chars(trimmed):
                if not allow_partial_sanitization:
                    return ""
                cleaned = normalize_space(strip_private_use_chars(trimmed))
                if not cleaned:
                    return ""
                first_rank = parse_fanqie_ranking_entries(cleaned, allow_partial_sanitization=True)
                if first_rank:
                    first = first_rank[0]
                    return f"{first['rank']:02d} - {first['title']} {first['author']} {first['summary']}".strip()[:limit]
                return ""
            return trimmed[:limit]
    return compact[:limit]


def parse_fanqie_ranking_entries(text: str | None, *, allow_partial_sanitization: bool = False) -> list[dict]:
    if not text:
        return []
    compact = normalize_space(text)
    first_rank = re.search(r"01\s*-\s*", compact)
    if first_rank:
        compact = compact[first_rank.start():]
    matches = list(re.finditer(r"(\d{2})\s*-\s*", compact))
    if not matches:
        return []

    entries = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(compact)
        segment = compact[start:end].strip(" -")
        if not segment:
            continue

        stop_markers = [" 在读：", " 最近更新：", " 已完结 ", " 连载中 "]
        cutoff = len(segment)
        for marker in stop_markers:
            pos = segment.find(marker)
            if pos != -1:
                cutoff = min(cutoff, pos)
        head = segment[:cutoff].strip()
        tokens = head.split()
        if not tokens:
            continue

        raw_title = tokens[0]
        raw_author = tokens[1] if len(tokens) > 1 else ""
        raw_summary = " ".join(tokens[2:]).strip()
        if (contains_private_use_chars(raw_title) or contains_private_use_chars(raw_author) or contains_private_use_chars(raw_summary)) and not allow_partial_sanitization:
            continue
        title = strip_private_use_chars(raw_title).strip()
        author = strip_private_use_chars(raw_author).strip()
        summary = normalize_space(strip_private_use_chars(raw_summary))
        if re.fullmatch(r"\d+", title):
            continue
        if re.fullmatch(r"\d{2}:\d{2}", author):
            continue
        if not retains_enough_text_after_strip(raw_title, title, min_ratio=0.6, min_length=2):
            continue
        if not retains_enough_text_after_strip(raw_author, author, min_ratio=0.6, min_length=1):
            continue
        if len(title) < 2 or len(author) < 1:
            continue
        entries.append(
            {
                "rank": int(match.group(1)),
                "title": title,
                "author": author,
                "summary": summary,
            }
        )
    return entries


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def remove_file_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def default_source_plan(platform: str, genre: str, depth: str, source_urls: list[str] | None = None) -> dict:
    if source_urls:
        return {
            "requested_scope": {
                "mode": "external-urls",
                "platform": platform,
                "genre": genre,
                "depth": depth,
            },
            "collection_plan": [
                {
                    "priority": 1,
                    "trust_level": "mixed",
                    "category": "explicit-source-urls",
                    "targets": source_urls,
                    "status": "pending",
                }
            ],
            "targets": [{"name": url, "url": url, "trust_level": "mixed"} for url in source_urls],
            "notes": ["本次使用显式传入的 source URLs，不额外推断官方榜单入口。"],
        }

    if platform == "番茄" and genre == "玄幻" and depth == "quick":
        targets = [
            {"name": "番茄小说排行榜总页", "url": "https://fanqienovel.com/rank/1", "trust_level": "A"},
            {"name": "番茄传统玄幻阅读榜", "url": "https://fanqienovel.com/rank/1_2_258", "trust_level": "A"},
            {"name": "番茄传统玄幻新书榜", "url": "https://fanqienovel.com/rank/1_1_258", "trust_level": "A"},
            {"name": "番茄玄幻脑洞阅读榜", "url": "https://fanqienovel.com/rank/1_2_257", "trust_level": "A"},
            {"name": "番茄玄幻脑洞新书榜", "url": "https://fanqienovel.com/rank/1_1_257", "trust_level": "A"},
        ]
        return {
            "requested_scope": {
                "mode": "platform-default",
                "platform": platform,
                "genre": genre,
                "depth": depth,
            },
            "collection_plan": [
                {
                    "priority": 1,
                    "trust_level": "A",
                    "category": "官方平台榜单页",
                    "targets": [item["name"] for item in targets],
                    "status": "pending",
                }
            ],
            "targets": targets,
            "notes": [
                "当前仅内置番茄-玄幻-quick 的官方榜单入口。",
                "其余平台/题材组合默认退化为 skeleton 或显式 URLs 模式。",
            ],
        }

    if platform == "番茄" and genre == "宫斗宅斗" and depth == "quick":
        targets = [
            {"name": "番茄小说排行榜总页", "url": "https://fanqienovel.com/rank/0", "trust_level": "A"},
            {"name": "番茄宫斗宅斗阅读榜", "url": "https://fanqienovel.com/rank/0_2_246", "trust_level": "A"},
            {"name": "番茄宫斗宅斗新书榜", "url": "https://fanqienovel.com/rank/0_1_246", "trust_level": "A"},
            {"name": "番茄古风世情阅读榜", "url": "https://fanqienovel.com/rank/0_2_1139", "trust_level": "A"},
            {"name": "番茄古风世情新书榜", "url": "https://fanqienovel.com/rank/0_1_1139", "trust_level": "A"},
        ]
        return {
            "requested_scope": {
                "mode": "platform-default",
                "platform": platform,
                "genre": genre,
                "depth": depth,
            },
            "collection_plan": [
                {
                    "priority": 1,
                    "trust_level": "A",
                    "category": "官方平台榜单页",
                    "targets": [item["name"] for item in targets],
                    "status": "pending",
                }
            ],
            "targets": targets,
            "notes": [
                "当前已内置番茄-宫斗宅斗-quick 的官方榜单入口。",
                "宫斗宅斗信号会优先按嫡庶/家权、反击陷害、重生复仇与位阶压迫来提炼。",
            ],
        }

    return {
        "requested_scope": {
            "mode": "unsupported-default",
            "platform": platform,
            "genre": genre,
            "depth": depth,
        },
        "collection_plan": [],
        "targets": [],
        "notes": ["当前脚本未内置这组平台/题材的默认官方来源。"],
    }


def build_sources(
    plan: dict,
    acquire_fn,
    *,
    fanqie_reference_font_path: Path | None = None,
    fanqie_reference_font_number: int | None = None,
    fanqie_decode_mode: str = "off",
) -> tuple[list[dict], int]:
    sources = []
    success_count = 0
    for item in plan.get("targets", []):
        hostname = urlparse(item["url"]).netloc.lower()
        prefer_source = "direct_html" if hostname.endswith("fanqienovel.com") else None
        kwargs = {"min_body_chars": 300}
        if prefer_source:
            kwargs["prefer_source"] = prefer_source
        result = acquire_fn(item["url"], **kwargs)
        ok = result.get("status") in {"success", "partial"} and result.get("source_type") != "none"
        if ok:
            success_count += 1
        body = result.get("body")
        if hostname.endswith("fanqienovel.com") and fanqie_decode_mode == "approx":
            body = decode_fanqie_obfuscated_body(
                body=body,
                notes=result.get("notes"),
                reference_font_path=fanqie_reference_font_path,
                reference_font_number=fanqie_reference_font_number,
            )
        ranking_entries = parse_fanqie_ranking_entries(body) if hostname.endswith("fanqienovel.com") else []
        excerpt = focus_excerpt(item["url"], body)
        if ranking_entries:
            first = ranking_entries[0]
            excerpt = f"{first['rank']:02d} - {first['title']} {first['author']} {first['summary']}".strip()[:240]
        sources.append(
            {
                "name": item["name"],
                "url": item["url"],
                "trust_level": item["trust_level"],
                "status": result.get("status"),
                "source_type": result.get("source_type"),
                "failure_reason": result.get("failure_reason"),
                "title": result.get("title"),
                "final_url": result.get("final_url"),
                "notes": result.get("notes") or [],
                "excerpt": excerpt,
                "ranking_entries": ranking_entries,
            }
        )
    return sources, success_count


def source_text(source: dict) -> str:
    parts = [source.get("name") or "", source.get("title") or "", source.get("excerpt") or ""]
    for entry in source.get("ranking_entries") or []:
        parts.append(entry.get("title") or "")
        parts.append(entry.get("summary") or "")
    return normalize_space(" ".join(parts))


def is_fanqie_total_rank_source(source: dict) -> bool:
    raw_url = source.get("url") or ""
    parsed = urlparse(raw_url)
    normalized_path = parsed.path.rstrip("/")
    name = source.get("name") or ""
    return (parsed.netloc.lower().endswith("fanqienovel.com") and normalized_path == "/rank/1") or name == "番茄小说排行榜总页"


def evidence_sources_for_patterns(sources: list[dict]) -> list[dict]:
    filtered = []
    for source in sources:
        if source.get("status") not in {"success", "partial"}:
            continue
        if is_fanqie_total_rank_source(source):
            continue
        filtered.append(source)
    return filtered


TAG_RULES = {
    "长生": ["长生"],
    "系统/命格/词条": ["系统", "命格", "词条", "规则收益"],
    "苟道/无系统": ["苟", "无系统", "苟王"],
    "身份反差/退婚": ["退婚", "误认", "无敌", "老登"],
    "开局强钩子": ["开局", "护送", "灭世帝女"],
}


PALACE_TAG_RULES = {
    "嫡庶/家权": ["嫡女", "嫡庶", "家权", "掌家", "族谱"],
    "反击陷害": ["陷害", "反击", "反将一军", "打脸"],
    "重生复仇": ["重生", "复仇", "改命"],
    "位阶压迫": ["位分", "家法", "主母", "县主", "郡主", "贵女"],
    "高门婚配/权臣拉扯": ["和离", "错婚", "婚房", "赐婚", "权臣", "先婚后爱"],
}


PALACE_TAG_SIGNALS = {
    "嫡庶/家权": "宫斗宅斗前排样本持续强调嫡庶、掌家、族谱闭环与家权争夺。",
    "反击陷害": "陷害与反击的来回换手仍然是宫斗宅斗的即时追读点。",
    "重生复仇": "重生、改命、复仇在新书阶段仍然是高识别卖点。",
    "位阶压迫": "位分、家法、郡主/县主等位阶压迫仍然是首轮冲突的重要来源。",
    "高门婚配/权臣拉扯": "当前番茄古风女频前排样本里，高门婚配、权臣拉扯、和离/错婚等关系冲突很强势。",
}


PALACE_TAG_THRESHOLDS = {
    "嫡庶/家权": 2,
    "反击陷害": 2,
    "重生复仇": 1,
    "位阶压迫": 1,
    "高门婚配/权臣拉扯": 2,
}


def detect_theme(sources: list[dict]) -> str:
    names = " ".join(source.get("name", "") for source in sources)
    if "宫斗宅斗" in names:
        return "palace"
    return "default"


def tag_rule_bundle(sources: list[dict]) -> tuple[dict, dict, dict]:
    if detect_theme(sources) == "palace":
        return PALACE_TAG_RULES, PALACE_TAG_SIGNALS, PALACE_TAG_THRESHOLDS
    return TAG_RULES, TAG_SIGNALS, TAG_THRESHOLDS


TAG_SIGNALS = {
    "长生": "在前排样本里反复出现长生/超长时间跨度信号，适合作为脑洞玄幻的高识别卖点。",
    "系统/命格/词条": "规则显性化与收益前置仍是新书场景里最容易完成首屏理解的钩子。",
    "苟道/无系统": "传统玄幻里仍能看到稳健、慢热、无系统这类稳态卖点。",
    "身份反差/退婚": "低位开局、退婚、误认、身份反差仍适合快速拉起冲突。",
    "开局强钩子": "“开局”型强钩子依然适合作为标题与简介的首轮抓取点。",
}


TAG_THRESHOLDS = {
    "长生": 2,
    "系统/命格/词条": 2,
    "苟道/无系统": 1,
    "身份反差/退婚": 2,
    "开局强钩子": 1,
}


def keyword_present(text: str, keyword: str) -> bool:
    if keyword == "系统":
        return "系统" in text and "无系统" not in text
    return keyword in text


def top_entries_for_source(source: dict, top_n: int = 3) -> list[str]:
    entries = sorted(source.get("ranking_entries") or [], key=lambda item: item.get("rank", 9999))
    if entries:
        return [
            normalize_space(" ".join([entry.get("title") or "", entry.get("summary") or ""]))
            for entry in entries[:top_n]
        ]
    return [source_text(source)]


def source_pattern_config(source: dict) -> dict:
    name = source.get("name") or ""
    if "新书榜" in name:
        return {"top_n": 5, "weight": 2}
    return {"top_n": 3, "weight": 1}


def collect_keyword_frequency(sources: list[dict], top_n: int | None = 3) -> dict[str, int]:
    counts: dict[str, int] = {}
    active_rules, _, _ = tag_rule_bundle(sources)
    for source in evidence_sources_for_patterns(sources):
        config = source_pattern_config(source)
        effective_top_n = top_n if top_n is not None else config["top_n"]
        weight = config["weight"] if top_n is None else 1
        for entry_text in top_entries_for_source(source, top_n=effective_top_n):
            for keywords in active_rules.values():
                for keyword in keywords:
                    if keyword_present(entry_text, keyword):
                        counts[keyword] = counts.get(keyword, 0) + weight
    return counts


def collect_keyword_evidence_titles(sources: list[dict], top_n: int | None = 3) -> dict[str, list[str]]:
    evidence: dict[str, list[str]] = {}
    active_rules, _, _ = tag_rule_bundle(sources)
    for source in evidence_sources_for_patterns(sources):
        matched_keywords: set[str] = set()
        config = source_pattern_config(source)
        effective_top_n = top_n if top_n is not None else config["top_n"]
        for entry_text in top_entries_for_source(source, top_n=effective_top_n):
            for keywords in active_rules.values():
                for keyword in keywords:
                    if keyword_present(entry_text, keyword):
                        matched_keywords.add(keyword)
        for keyword in matched_keywords:
            evidence.setdefault(keyword, []).append(source["name"])
    return evidence


def infer_hot_genres(sources: list[dict]) -> list[dict]:
    items = []
    if any(source["status"] in {"success", "partial"} and "传统玄幻" in source["name"] for source in sources):
        items.append(
            {
                "name": "传统玄幻",
                "signal": "当前官方来源里同时拿到了传统玄幻阅读榜/新书榜，说明传统玄幻仍是明确可见的稳定子类。",
                "confidence": "medium",
            }
        )
    if any(source["status"] in {"success", "partial"} and "玄幻脑洞" in source["name"] for source in sources):
        items.append(
            {
                "name": "玄幻脑洞",
                "signal": "当前官方来源里同时拿到了玄幻脑洞阅读榜/新书榜，说明高概念脑洞方向在快照里同样可见。",
                "confidence": "medium",
            }
        )
    return items


def infer_tag_matches(sources: list[dict]) -> dict[str, list[str]]:
    active_rules, _, active_thresholds = tag_rule_bundle(sources)
    frequencies = collect_keyword_frequency(sources, top_n=None)
    evidence = collect_keyword_evidence_titles(sources, top_n=None)
    matches: dict[str, list[str]] = {}
    for tag, keywords in active_rules.items():
        total = sum(frequencies.get(keyword, 0) for keyword in keywords)
        if total >= active_thresholds[tag]:
            titles: list[str] = []
            for keyword in keywords:
                for source_name in evidence.get(keyword, []):
                    if source_name not in titles:
                        titles.append(source_name)
            matches[tag] = titles
    return matches


def infer_hot_tags(sources: list[dict]) -> list[dict]:
    _, active_signals, _ = tag_rule_bundle(sources)
    matches = infer_tag_matches(sources)
    hot_tags = []
    for tag, source_names in matches.items():
        hot_tags.append(
            {
                "tag": tag,
                "signal": active_signals[tag],
                "evidence_titles": source_names,
            }
        )
    return hot_tags


def infer_opening_patterns(sources: list[dict]) -> list[dict]:
    matches = infer_tag_matches(sources)
    theme = detect_theme(sources)
    patterns = []
    if theme == "palace":
        if any(tag in matches for tag in {"位阶压迫", "嫡庶/家权"}):
            patterns.append(
                {
                    "pattern": "开篇先立压迫位阶",
                    "detail": "宫斗宅斗开篇应先把尊卑、位阶、嫡庶或家权压迫感立起来，再推进反击。",
                    "confidence": "medium",
                }
            )
        if any(tag in matches for tag in {"反击陷害", "重生复仇"}):
            patterns.append(
                {
                    "pattern": "先压后反击",
                    "detail": "先让主角吃到真实压迫，再尽快兑现一次反击或换账，不宜只铺氛围。",
                    "confidence": "medium",
                }
            )
        if "高门婚配/权臣拉扯" in matches:
            patterns.append(
                {
                    "pattern": "婚配冲突先落地",
                    "detail": "当前古风女频前排更偏好先把婚约、错婚、和离、权臣婚配等关系冲突直接摆上台面。",
                    "confidence": "medium",
                }
            )
        return patterns
    if any(tag in matches for tag in {"开局强钩子", "身份反差/退婚"}):
        patterns.append(
            {
                "pattern": "一句话高概念开局",
                "detail": "标题或首段直接亮出开局机制、身份反差或强冲突，降低读者理解门槛。",
                "confidence": "medium",
            }
        )
    if "系统/命格/词条" in matches:
        patterns.append(
            {
                "pattern": "规则收益前置",
                "detail": "尽量在开篇前半段就说明系统/命格/词条规则，并尽早兑现第一批收益。",
                "confidence": "medium",
            }
        )
    if any(tag in matches for tag in {"苟道/无系统", "身份反差/退婚"}):
        patterns.append(
            {
                "pattern": "旧母题加快反馈",
                "detail": "退婚、宗门压迫、低位身份等老母题仍可用，但要配合更快的反馈节奏。",
                "confidence": "medium",
            }
        )
    return patterns


def infer_cool_point_patterns(sources: list[dict]) -> list[dict]:
    matches = infer_tag_matches(sources)
    theme = detect_theme(sources)
    patterns = []
    if theme == "palace":
        if "反击陷害" in matches:
            patterns.append(
                {
                    "pattern": "反击陷害当场兑现",
                    "detail": "宫斗宅斗前排样本偏好让陷害与反击在同一交易单元里形成即时回报。",
                }
            )
        if "嫡庶/家权" in matches:
            patterns.append(
                {
                    "pattern": "家权账本持续改动",
                    "detail": "嫡庶、掌家、族谱与家权换手会持续提供追读张力。",
                }
            )
        if "位阶压迫" in matches:
            patterns.append(
                {
                    "pattern": "位阶差制造压迫",
                    "detail": "位分、家法、封号和门第差距是宫斗宅斗最稳定的压迫源。",
                }
            )
        if "高门婚配/权臣拉扯" in matches:
            patterns.append(
                {
                    "pattern": "高门婚配制造拉扯",
                    "detail": "高门婚配、错婚、和离与权臣/郡主关系会持续提供关系张力和阶层冲突。",
                }
            )
        return patterns
    if "长生" in matches:
        patterns.append(
            {
                "pattern": "超长时间跨度",
                "detail": "长生视角容易制造时代更替、故人更迭和主角仍在场的爽点。",
            }
        )
    if "系统/命格/词条" in matches:
        patterns.append(
            {
                "pattern": "规则显性化",
                "detail": "系统、命格、词条等机制把成长收益写明，读者更容易预判后续回报。",
            }
        )
    if "身份反差/退婚" in matches:
        patterns.append(
            {
                "pattern": "低位身份反杀",
                "detail": "退婚、误认、低位开局更容易快速拉起逆袭张力。",
            }
        )
    if "苟道/无系统" in matches:
        patterns.append(
            {
                "pattern": "传统稳态卖点仍有效",
                "detail": "无系统、慢热、苟道、布局流并没有失效，仍能作为传统玄幻的稳态卖点。",
            }
        )
    return patterns


def infer_recommended_buckets(sources: list[dict]) -> list[dict]:
    buckets = []
    has_traditional = any(source["status"] in {"success", "partial"} and "传统玄幻" in source["name"] for source in sources)
    has_brainhole = any(source["status"] in {"success", "partial"} and "玄幻脑洞" in source["name"] for source in sources)
    if has_traditional:
        buckets.append(
            {
                "bucket_name": "传统玄幻",
                "config_key": "xuanhuan_traditional",
                "priority_rank": 3,
                "track": "longform",
                "confidence": "medium",
                "reason": "当前快照里传统玄幻阅读榜和新书榜都可见，适合作为保守主桶。",
            }
        )
    if has_brainhole:
        buckets.append(
            {
                "bucket_name": "玄幻脑洞",
                "config_key": "",
                "priority_rank": 0,
                "track": "longform",
                "confidence": "medium",
                "reason": "当前快照里玄幻脑洞阅读榜和新书榜都可见，适合作为高概念备选桶。",
            }
        )
    return buckets


def build_findings(sources: list[dict], *, real_report: bool) -> dict:
    platform_notes = []
    for source in sources:
        note = f"{source['name']}：{source['status']}"
        if source.get("source_type"):
            note += f"，来源 {source['source_type']}"
        if source.get("title"):
            note += f"，标题《{source['title']}》"
        if source.get("excerpt"):
            note += f"，摘要：{source['excerpt']}"
        platform_notes.append({"note": note, "confidence": "medium" if source["trust_level"] == "A" else "low"})

    return {
        "finding_mode": "current_snapshot_only" if real_report else "skeleton_only",
        "hot_genres": infer_hot_genres(sources) if real_report else [],
        "recommended_content_buckets": infer_recommended_buckets(sources) if real_report else [],
        "hot_tags": infer_hot_tags(sources) if real_report else [],
        "opening_patterns": infer_opening_patterns(sources) if real_report else [],
        "cool_point_patterns": infer_cool_point_patterns(sources) if real_report else [],
        "platform_notes": platform_notes,
    }


def build_confidence(success_count: int, sources: list[dict]) -> dict:
    official_success = sum(1 for source in sources if source["trust_level"] == "A" and source["status"] in {"success", "partial"})
    if official_success > 0:
        return {
            "overall": "medium",
            "reason": "当前运行中拿到了至少一个 A 级官方来源，但仍只是单次快照，没有时间序列或后台行为数据。",
        }
    return {
        "overall": "low",
        "reason": "当前运行未拿到可信外部正文证据，结果退化为 skeleton。",
    }


def build_gaps(success_count: int, plan: dict) -> list[str]:
    gaps = []
    if success_count == 0:
        gaps.append("当前运行未拿到可消费的外部来源正文，只能输出 skeleton。")
    if not plan.get("targets"):
        gaps.append("当前平台/题材组合没有内置默认来源；如需真实扫描，请显式传入 source URLs。")
    gaps.append("当前版本不做跨周、跨月时间序列采集。")
    gaps.append("当前版本不读取平台后台指标、评论聚类或转化数据。")
    return gaps


def build_apply_recommendations(real_report: bool, platform: str, genre: str) -> list[dict]:
    if not real_report:
        return []
    return [
        {
            "type": "manual_review",
            "suggestion": f"先人工复核本轮 {platform}-{genre} 抓到的来源摘要，再决定是否把信号继续喂给 package / write。",
            "confidence": "low",
            "note": "当前脚本负责收集与落盘，不负责高强度趋势推理。",
        }
    ]


def build_apply_recommendations_from_findings(payload: dict) -> list[dict]:
    platform = payload["targets"]["platforms"][0] if payload["targets"]["platforms"] else ""
    genre = payload["targets"]["genre"]
    recommendations = build_apply_recommendations(payload["report_kind"] == "real_report", platform, genre)
    tags = {item["tag"] for item in payload["findings"].get("hot_tags", [])}
    patterns = {item["pattern"] for item in payload["findings"].get("opening_patterns", [])}

    if "开局强钩子" in tags or "一句话高概念开局" in patterns or "身份反差/退婚" in tags:
        recommendations.append(
            {
                "type": "hook_design",
                "suggestion": "把书名、简介或开篇首段里的高概念钩子再前移半步，优先暴露身份反差、开局机制或强冲突。",
                "confidence": "medium",
                "note": "基于当前榜单前排样本，开篇阶段的强钩子仍然是新书抓取重点。",
            }
        )

    if "系统/命格/词条" in tags or "规则收益前置" in patterns:
        recommendations.append(
            {
                "type": "payoff_design",
                "suggestion": "在前几章更早兑现规则收益，让系统/命格/词条带来的第一批回报尽快可见。",
                "confidence": "medium",
                "note": "基于当前样本，规则显性化和收益前置仍是稳定有效的爽点组织方式。",
            }
        )

    if "高门婚配/权臣拉扯" in tags or "婚配冲突先落地" in patterns:
        recommendations.append(
            {
                "type": "hook_design",
                "suggestion": "把婚配错位、赐婚拉扯或高门关系冲突尽量前置到开篇交易单元里，避免宫斗宅斗的主钩子出场过晚。",
                "confidence": "medium",
                "note": "基于当前宫斗宅斗样本，关系位阶与婚配冲突本身就能承担首屏钩子。",
            }
        )

    if "反击陷害" in tags or "先压后反击" in patterns:
        recommendations.append(
            {
                "type": "conflict_design",
                "suggestion": "让压迫、陷害与第一轮反击尽量落在同一段剧情单元里，避免只铺压不兑现。",
                "confidence": "medium",
                "note": "基于当前宫斗宅斗样本，先压后反击的即时兑现仍是追读核心。",
            }
        )

    if "高门婚配/权臣拉扯" in tags or "嫡庶/家权" in tags:
        recommendations.append(
            {
                "type": "truth_consistency",
                "suggestion": "包装、书名、简介和章纲里的关系词，必须先回到嫡庶/齿序/高门婚配真值，别让高点击关系词先跑在真值前面。",
                "confidence": "medium",
                "note": "宫斗宅斗和古风高门线里，关系词一旦脱离法统与齿序真值，很容易直接把整条线写崩。",
            }
        )

    return [
        recommendation
        for recommendation in recommendations
    ]


def build_adjustments(payload: dict) -> dict:
    source_scan = {
        "scan_time": payload["scan_time"],
        "mode": payload["mode"],
        "platform": payload["targets"]["platforms"][0] if payload["targets"]["platforms"] else "",
        "genre": payload["targets"]["genre"],
        "depth": payload["targets"]["depth"],
        "report_kind": payload["report_kind"],
        "confidence": payload["confidence"],
        "sources": [source["url"] for source in payload["sources"] if source["status"] in {"success", "partial"}],
    }
    adjustments = []
    if payload["report_kind"] == "real_report":
        adjustments.append(
            {
                "id": "scan-manual-review-first",
                "priority": "medium",
                "scope": "project",
                "applies_to": ["包装", "开篇钩子", "后续写作方向"],
                "suggestion": "先基于本轮市场来源做人工复核，再把稳定信号同步到包装或写作链。",
                "reason": "当前脚本已经拿到真实来源，但仍属于单次快照，不宜直接上升为强约束。",
            }
        )
        tags = {item["tag"] for item in payload["findings"].get("hot_tags", [])}
        patterns = {item["pattern"] for item in payload["findings"].get("opening_patterns", [])}
        if "开局强钩子" in tags or "一句话高概念开局" in patterns or "身份反差/退婚" in tags:
            adjustments.append(
                {
                    "id": "scan-surface-hook",
                    "priority": "high",
                    "scope": "project",
                    "applies_to": ["包装", "简介", "开篇前三章"],
                    "suggestion": "优先把开局机制、身份反差或强冲突写到首屏最前面，不要把高概念钩子埋到中后段。",
                    "reason": "当前榜单前排样本显示，新书抓取仍然明显偏向一句话高概念和低位强冲突。",
                }
            )
        if "系统/命格/词条" in tags or "规则收益前置" in patterns:
            adjustments.append(
                {
                    "id": "scan-frontload-payoff",
                    "priority": "high",
                    "scope": "project",
                    "applies_to": ["前3-5章", "开篇试炼/任务段"],
                    "suggestion": "让规则收益和第一批回报更早落地，避免系统/命格/词条只停留在设定介绍层。",
                    "reason": "当前样本里规则显性化与收益前置仍然是高频组织方式。",
                }
            )
        if "高门婚配/权臣拉扯" in tags or "婚配冲突先落地" in patterns:
            adjustments.append(
                {
                    "id": "scan-surface-hook",
                    "priority": "high",
                    "scope": "project",
                    "applies_to": ["包装", "简介", "开篇前三章"],
                    "suggestion": "优先把婚配错位、赐婚拉扯或高门关系冲突写到首屏最前面，不要把主钩子拖到后段。",
                    "reason": "当前宫斗宅斗样本显示，婚配与位阶关系本身就能承担第一钩子。",
                }
            )
        if "反击陷害" in tags or "先压后反击" in patterns:
            adjustments.append(
                {
                    "id": "scan-frontload-conflict",
                    "priority": "high",
                    "scope": "project",
                    "applies_to": ["开篇前3章", "首轮冲突单元"],
                    "suggestion": "让陷害与反击尽量在同一轮剧情里闭合，避免长期只受压不回击。",
                    "reason": "当前宫斗宅斗样本里，先压后反击的即时兑现是高频追读点。",
                }
            )
        if "高门婚配/权臣拉扯" in tags or "嫡庶/家权" in tags:
            adjustments.append(
                {
                    "id": "scan-kinship-truth-check",
                    "priority": "high",
                    "scope": "project",
                    "applies_to": ["书名关系词", "简介", "章纲", "设定集/家族"],
                    "suggestion": "涉及嫡女、庶妹、县主、郡主、和离、赐婚等关系词时，先补齐嫡庶、齿序、婚配与家权真值，再让包装和正文消费。",
                    "reason": "当前市场偏好确实吃高门婚配和关系冲突，但这类词如果脱离真值，会比普通题材更快出戏。",
                }
            )
    return {
        "last_applied": payload["scan_time"],
        "source_scan": source_scan,
        "adjustments": adjustments,
    }


def can_apply_adjustments(payload: dict) -> bool:
    return payload["mode"] == "project-annotate" and payload["report_kind"] == "real_report" and payload["confidence"]["overall"] in {"medium", "high"}


def run_scan(
    *,
    project_root: Path,
    platform: str,
    genre: str,
    depth: str,
    mode: str,
    source_urls: list[str] | None = None,
    acquire_fn=None,
    timestamp: str | None = None,
    fanqie_reference_font_path: Path | None = None,
    fanqie_reference_font_number: int | None = None,
    fanqie_decode_mode: str = "off",
) -> dict:
    timestamp = timestamp or now_iso()
    mighty_dir = project_root / ".mighty"
    mighty_dir.mkdir(parents=True, exist_ok=True)
    state_path = mighty_dir / "state.json"
    state = load_json(state_path)
    plan = default_source_plan(platform, genre, depth, source_urls)

    if acquire_fn is None:
        def acquire_fn(url: str, **kwargs):
            return acquire_article(url, **kwargs).to_dict()

    sources, success_count = build_sources(
        plan,
        acquire_fn,
        fanqie_reference_font_path=fanqie_reference_font_path,
        fanqie_reference_font_number=fanqie_reference_font_number,
        fanqie_decode_mode=fanqie_decode_mode,
    )
    real_report = success_count > 0
    if plan.get("collection_plan"):
        plan["collection_plan"][0]["status"] = "completed" if real_report else "attempted"

    payload = {
        "version": "1.0",
        "scan_time": timestamp,
        "mode": mode,
        "report_kind": "real_report" if real_report else "skeleton",
        "targets": {
            "platforms": [platform] if platform else [],
            "genre": genre,
            "depth": depth,
        },
        "source_plan": plan,
        "sources": sources,
        "findings": build_findings(sources, real_report=real_report),
        "confidence": build_confidence(success_count, sources),
        "gaps": build_gaps(success_count, plan),
        "apply_recommendations": [],
    }
    payload["apply_recommendations"] = build_apply_recommendations_from_findings(payload)
    write_json(mighty_dir / "market-data.json", payload)

    adjustments_path = mighty_dir / "market-adjustments.json"
    if can_apply_adjustments(payload):
        adjustments = build_adjustments(payload)
        write_json(adjustments_path, adjustments)
        state["market_adjustments"] = {
            "last_applied": adjustments["last_applied"],
            "source_scan": adjustments["source_scan"],
            "adjustments": adjustments["adjustments"],
            "sidecar_file": str(adjustments_path),
        }
        write_json(state_path, state)
    else:
        remove_file_if_exists(adjustments_path)
        if "market_adjustments" in state:
            del state["market_adjustments"]
            write_json(state_path, state)

    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a report-only or project-annotate novel market scan.")
    parser.add_argument("project_root")
    parser.add_argument("--platform", default="")
    parser.add_argument("--genre", default="")
    parser.add_argument("--depth", default="quick")
    parser.add_argument("--mode", choices=["report-only", "project-annotate"], default="report-only")
    parser.add_argument("--source-url", action="append", dest="source_urls")
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--fanqie-reference-font", default=os.getenv("GENM_FANQIE_REFERENCE_FONT", ""))
    parser.add_argument("--fanqie-reference-font-number", type=int, default=int(os.getenv("GENM_FANQIE_REFERENCE_FONT_NUMBER", "0")) if os.getenv("GENM_FANQIE_REFERENCE_FONT_NUMBER") else None)
    parser.add_argument("--fanqie-decode-mode", choices=["off", "approx"], default=os.getenv("GENM_FANQIE_DECODE_MODE", "off"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_scan(
        project_root=Path(args.project_root),
        platform=args.platform,
        genre=args.genre,
        depth=args.depth,
        mode=args.mode,
        source_urls=args.source_urls,
        timestamp=args.timestamp or None,
        fanqie_reference_font_path=Path(args.fanqie_reference_font) if args.fanqie_reference_font else None,
        fanqie_reference_font_number=args.fanqie_reference_font_number,
        fanqie_decode_mode=args.fanqie_decode_mode,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
