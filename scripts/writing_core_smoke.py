#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_BUCKETS = {
    "玄幻脑洞",
    "豪门总裁",
    "宫斗宅斗",
    "职场婚恋",
    "青春甜宠",
    "都市日常",
    "都市脑洞",
    "历史脑洞",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate writing-core smoke drafts and optional writeback.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--chapters", required=True)
    parser.add_argument("--mode", choices=("scaffold", "draft", "writeback"), default="draft")
    parser.add_argument("--output")
    parser.add_argument("--writeback", action="store_true")
    parser.add_argument("--save-packaging", action="store_true")
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_state(project_root: Path) -> dict:
    return load_json(project_root / ".mighty" / "state.json")


def load_sidecar(path: Path) -> dict:
    return load_json(path)


def infer_bucket(state: dict) -> str | None:
    genre_profile = state.get("genre_profile") or {}
    bucket = genre_profile.get("bucket")
    if bucket in SUPPORTED_BUCKETS:
        return bucket
    meta = state.get("meta") or {}
    genre = meta.get("genre")
    if genre in SUPPORTED_BUCKETS:
        return genre
    return None


def normalize_chapter_key(chapter: str | int) -> str:
    return f"{int(str(chapter)):03d}"


def parse_chapter_range(chapters: str) -> list[str]:
    text = chapters.strip()
    if "-" not in text:
        return [normalize_chapter_key(text)]
    start_text, end_text = [part.strip() for part in text.split("-", 1)]
    start = int(start_text)
    end = int(end_text)
    return [f"{value:03d}" for value in range(start, end + 1)]


def detect_target_chapter(state: dict, chapters: str) -> str:
    chapter_keys = parse_chapter_range(chapters)
    chapter_meta = state.get("chapter_meta") or {}
    for key in reversed(chapter_keys):
        if key in chapter_meta or str(int(key)) in chapter_meta:
            return key
    return chapter_keys[-1]


def chapter_meta_entry(state: dict, chapter_key: str) -> tuple[dict, str]:
    chapter_meta = state.setdefault("chapter_meta", {})
    legacy_key = str(int(chapter_key))
    if chapter_key in chapter_meta:
        return chapter_meta[chapter_key], chapter_key
    if legacy_key in chapter_meta:
        return chapter_meta[legacy_key], legacy_key
    chapter_meta[chapter_key] = {}
    return chapter_meta[chapter_key], chapter_key


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def extract_outline_pitch(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    in_fence = False
    for index, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line == "## 一句话卖点":
            for candidate in lines[index + 1 :]:
                if candidate.startswith("```"):
                    break
                if (
                    candidate
                    and not candidate.startswith("#")
                    and not candidate.startswith("-")
                    and not candidate.startswith(">")
                    and not candidate.startswith("```")
                ):
                    return candidate
    in_fence = False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if (
            line
            and not line.startswith("#")
            and not line.startswith("-")
            and not line.startswith(">")
            and not line.startswith("```")
        ):
            return line
    return ""


def collect_text(project_root: Path, chapters: str) -> str:
    parts = []
    parts.append(read_text(project_root / "大纲" / "总纲.md"))
    for key in parse_chapter_range(chapters):
        parts.append(read_text(project_root / "chapters" / f"第{key}章.md"))
    return "\n".join(part for part in parts if part)


def evidence_sources(project_root: Path, chapters: str) -> list[str]:
    paths = [
        project_root / ".mighty" / "state.json",
        project_root / ".mighty" / "learned-patterns.json",
        project_root / ".mighty" / "market-adjustments.json",
        project_root / "大纲" / "总纲.md",
    ]
    for key in parse_chapter_range(chapters):
        paths.append(project_root / "chapters" / f"第{key}章.md")
    return [str(path.relative_to(REPO_ROOT)) if path.exists() and REPO_ROOT in path.parents else str(path) for path in paths if path.exists()]


def sample_date(date_str: str | None) -> str:
    return date_str or str(date.today())


def slugify_title(title: str) -> str:
    return title.replace("，", "-").replace("。", "").replace(" ", "-")


def default_output_path(project_root: Path, title: str, date_str: str) -> Path:
    return REPO_ROOT / "docs" / "writing-core-framework" / f"real-project-smoke-{slugify_title(title)}-{date_str}.md"


def packaging_template(title: str, bucket: str, text: str) -> dict:
    outline_pitch = extract_outline_pitch(text)
    if bucket == "玄幻脑洞":
        return {
            "current_title": "keep",
            "opening_method_cue": "首屏先砸生存困局，第1章点亮废丹重定价机制，第2章先救急，第3章完成卖出天价的小闭环。",
            "genre_difference_cue": "玄幻脑洞要让机制先改现实账本，再慢慢抬大世界，不要先讲设定。",
            "premium_review_cue": "第4-5章要把更大利益和更大反噬一起抬上来。",
            "overpromise_warning": "不要提前包装成丹院黑幕已经揭开或主角已横压宗门。",
            "payoff_timing_reminder": "第一轮兑现已在第3章完成；下一轮应在第4-5章给更大交易和追责。",
            "title": title,
            "one_liner": "月考垫底、今夜将逐下山的沈砚秋，发现废丹不是没用，而是卖错了人。",
            "synopsis": "青岚宗外门垫底那天，沈砚秋离被赶下山只差三十贡献点。谁都当废丹是垃圾，只有他在废丹窖里看见了一杆能重新定价的碎纹丹秤。别人倒掉的废丹，在他手里不再是废，而是能换灵石、换人脉、也换命的生意。",
        }
    if bucket == "豪门总裁":
        return {
            "current_title": "keep",
            "opening_method_cue": "离婚当天先翻项目账，第2章让董事会和并购盘进场，第3章把合伙人位置落成小兑现。",
            "genre_difference_cue": "豪门总裁要让关系和资源同场推进，不能只剩情绪拉扯。",
            "premium_review_cue": "第4章起要把合伙人位置兑现成真实权限、资源和舆论代价。",
            "overpromise_warning": "不要提前包装成她已赢下董事会或彻底反杀家族盘。",
            "payoff_timing_reminder": "第一轮位置兑现已在第3章完成；下一轮应在第4-5章落到控制权和代价。",
            "title": title,
            "one_liner": "离婚冷静期最后一天，沈南枝不抢前夫，只抢位置。",
            "synopsis": "离婚冷静期最后一天，沈南枝翻到离婚协议第十一页，才发现自己不只是要离婚，还要被顺手踢出曜衡医疗试运营。她不认。协议可以签，项目账不能让。周叙白把董事会席位先押到她手里，不是给她安慰，而是把一张会引爆舆论和家族盘的位置先给她站稳。",
        }
    if bucket == "宫斗宅斗":
        return {
            "current_title": "keep",
            "opening_method_cue": "第一章先把继母压制和婚书被换砸下来，第二章把旧账和规矩一起抬上桌，第三章让东宫开口锁住第一轮反击。",
            "genre_difference_cue": "宫斗宅斗要让压制关系、礼法规矩和东宫抬局同场推进，不能只剩后宅吵架。",
            "premium_review_cue": "后续章节要把婚书局兑现成更实的旧账、人证和权力网，别让太子口谕变成万能捷径。",
            "overpromise_warning": "不要提前包装成女主已经彻底赢下伯府，也不要把更大的宫中旧案写成已揭开。",
            "payoff_timing_reminder": "第一轮兑现应落在东宫点名和崔妈妈线启动；下一轮尽快落到旧账实证和更高层反扑。",
            "title": title,
            "one_liner": "继母动她婚书那夜，庶二姑娘谢云昭把亡母旧账掀上正厅，逼得东宫先开了口。",
            "synopsis": outline_pitch or "继母动她婚书那夜，庶二姑娘谢云昭把亡母旧账掀上正厅，逼得东宫先开了口。她争的不是一门婚事，而是谁也不能把规矩、婚书和旧账一起踩成废纸。",
        }
    if bucket == "都市日常":
        return {
            "current_title": "keep",
            "opening_method_cue": "先把搬回老小区后的现实困局拍到桌上，再用换饭和跑腿把第一层关系网接起来。",
            "genre_difference_cue": "都市日常要先让生活账本和人情网同时推进，不能先写温暖气氛。",
            "premium_review_cue": "后续章节要把临时工、老楼微更新和父亲康复账接成更实的生活改善链。",
            "overpromise_warning": "不要提前包装成整栋楼已经成了她的稳定后盾，也不要把社区线写成已经彻底打开。",
            "payoff_timing_reminder": "第一轮兑现应落在供气恢复、回请邻居和第一份临时收入上；下一轮尽快落到更稳的工作链路和更重的人情代价。",
            "title": title,
            "one_liner": "被裁员后搬回老小区的苏禾，先靠换饭活下来，再靠把一件件小事办成，把自己重新接回整栋楼的人情网。",
            "synopsis": outline_pitch or "被裁员的苏禾搬回老小区，在停气、父亲康复和存款见底的夹击里，靠换饭和跑腿把自己重新接回整栋楼的人情网。",
        }
    if bucket == "历史脑洞":
        return {
            "current_title": "keep",
            "opening_method_cue": "第一章先把县衙清积案问责压到主角头上，再用卷宗回响撬开第一桩旧案的现实口子。",
            "genre_difference_cue": "历史脑洞要让制度压力和翻案脑洞同场推进，不能写成纯神探破案或背景板官场文。",
            "premium_review_cue": "后续章节要把翻旧案兑现成更实的堂前资格、卷宗流转链和上位者敌意。",
            "overpromise_warning": "不要提前包装成主角已经查清压案黑手，也不要把升堂写成已彻底坐实的结果。",
            "payoff_timing_reminder": "第一轮兑现应落在旧案翻口、保位和堂前边缘资格；下一轮尽快落到压案链的具体人和制度反扑。",
            "title": title,
            "one_liner": "清河县县衙清积案问责压顶时，最底层刑房杂吏沈砚靠“卷宗回响”翻旧案保命、拿权，也一步步撞上真正的压案链。",
            "synopsis": outline_pitch or "清河县县衙清积案问责压顶时，最底层刑房杂吏沈砚靠“卷宗回响”翻旧案保命、拿权，也一步步撞上真正的压案链。",
        }
    if bucket == "职场婚恋":
        return {
            "current_title": "keep",
            "opening_method_cue": "第一章先把升职接锅和合租揭面双困局砸下来，第二章误判升级，第三章拿下试运行窗口。",
            "genre_difference_cue": "职场婚恋要让工作链路和同屋边界同场推进，不能只写旧情和空糖。",
            "premium_review_cue": "后续章节要把试运行窗口兑现成更实的数据、续约和抢功代价，不要让关系推进脱离业务。",
            "overpromise_warning": "不要提前包装成男女主已经结盟或项目已经稳了，也不要把前上司写成会直接开后门的安全男主。",
            "payoff_timing_reminder": "第一轮兑现应落在72小时试运行窗口；下一轮尽快落到续约结果、公司内抢功和同住越界成本。",
            "title": title,
            "one_liner": "姜栀升职当天接下一个随时会砸掉她职位的大客户，回到新租房却发现新室友正是刚跳去甲方的前上司裴述。",
            "synopsis": outline_pitch or "姜栀升职当天接下一个随时会砸掉她职位的大客户，回到新租房却发现新室友正是刚跳去甲方的前上司裴述。一个掌握续约生死，一个连退房都退不起，他们只能在工作链路冲突和同屋檐下的生活摩擦里，一边算项目账，一边算关系账。",
        }
    if bucket == "青春甜宠":
        return {
            "current_title": "keep",
            "opening_method_cue": "第一章先把转学和身份错认砸下来，第二章把学习互助和校园误判推进，第三章给第一次关系小兑现。",
            "genre_difference_cue": "青春甜宠要让身份错认、学习互助和校园节奏同场推进，不能只剩朦胧氛围。",
            "premium_review_cue": "后续章节要把身份错认兑现成更具体的校园关系变化和代价，而不是只反复心动。",
            "overpromise_warning": "不要提前包装成两人已经明确双向奔赴，也不要把校园误判写成已经彻底解除。",
            "payoff_timing_reminder": "第一轮兑现应落在身份错认后的关系绑定和学习互助；下一轮尽快落到校园舆论与边界成本。",
            "title": title,
            "one_liner": "转学第一天，林见夏把校草认成了新来的代课老师，一次身份错认直接把她推进了全校最惹眼的学习互助关系里。",
            "synopsis": "转学第一天，林见夏把校草认成了新来的代课老师，一次身份错认直接把她推进了全校最惹眼的学习互助关系里。她原本只想低调适应新学校，却在误判、流言和被迫同框中，一边补课，一边把关系账越算越近。",
        }
    if bucket == "都市脑洞":
        return {
            "current_title": "keep",
            "opening_method_cue": "第一章先把赔光积蓄和违约金压到头上，再让系统赔付直接到账，第二章继续把到账变成可见反咬资本。",
            "genre_difference_cue": "都市脑洞要先让系统或异常能力改现实账本，不能只讲设定概念。",
            "premium_review_cue": "后续章节要把赔付、反咬和更大代价接起来，不要让系统只剩发钱爽点。",
            "overpromise_warning": "不要提前包装成主角已经彻底翻盘，也不要把系统写成无成本印钞机。",
            "payoff_timing_reminder": "第一轮兑现应落在系统赔付到账和违约局反咬；下一轮尽快落到更大现实代价和更强对手。",
            "title": title,
            "one_liner": "赔光积蓄、还背着巨额违约金的那天，系统先把一笔真金白银打到了顾停洲账上。",
            "synopsis": "赔光积蓄、还背着巨额违约金的那天，顾停洲手机里突然激活了一个只赔“真实亏损”的系统。别人扣在他头上的每一笔账，都可能先变成一笔到账的赔付，再变成他反咬回去的筹码。",
        }
    return {
        "current_title": "keep",
        "opening_method_cue": "先把当前主冲突与位置差拍到桌上，再给第一轮可见兑现。",
        "genre_difference_cue": f"{bucket} 的开篇要让题材 promise 和现实账本一起推进。",
        "premium_review_cue": "后续章节要把当前位置兑现成更实的资源与代价。",
        "overpromise_warning": "不要把后续大盘当成前三章已兑现卖点。",
        "payoff_timing_reminder": "第一轮小兑现后，下一轮应尽快落到更实的资源和风险。",
        "title": title,
        "one_liner": outline_pitch or title,
        "synopsis": outline_pitch or text[:180].replace("\n", ""),
    }


def precheck_template(bucket: str, packaging_exists: bool) -> dict:
    return {
        "投稿建议": "ready-now",
        "packaging-needs-update": "no" if packaging_exists else "yes",
        "content_standard_summary": {
            "primary_failure_mode": "none",
            "execution_risk": "low",
        },
    }


def build_writeback_preview(chapter_key: str, bucket: str, *, packaging_status: str, writeback_status: str) -> dict:
    return {
        "chapter": chapter_key,
        "fields": ["content_standard_flags", "packaging_alignment_note"],
        "bucket": bucket,
        "packaging_status": packaging_status,
        "writeback_status": writeback_status,
    }


def update_learned_patterns(path: Path, bucket: str, title: str, text: str) -> str:
    data = load_sidecar(path)
    container = data.get("data") if isinstance(data.get("data"), dict) else data
    if not isinstance(container, dict):
        container = {}
    if bucket == "玄幻脑洞":
        container["opening_strategy"] = "首屏先砸生存困局，第1章点亮废丹重定价机制，第2章先救急，第3章当众卖出天价完成小闭环。"
        container["multi_line_guardrails"] = [
            "主线先稳住保名与废丹生意翻身，次线只轻触内门压价链和碎纹丹秤来历。",
            "每章至少同时推进现实账本变化和被盯上风险。",
        ]
        container["content_standard_alerts"] = [
            "避免说明文式玄幻",
            "避免机制只是挂名",
        ]
    elif bucket == "豪门总裁":
        container["opening_strategy"] = "第一章先把离婚协议和项目账删改拍到桌上，第二章让董事会与并购盘进场，第三章再把合伙人位置落成可见小兑现。"
        container["multi_line_guardrails"] = [
            "主线先稳住离婚局里的项目位置，次线再轻触董事会并购盘和豪门家族压力。",
            "每章都要同时推进资源位变化和舆论/家族代价。",
        ]
        container["content_standard_alerts"] = [
            "避免只剩身份标签和金句",
            "避免霸总一句话解决所有问题",
        ]
    elif bucket == "宫斗宅斗":
        container["opening_strategy"] = "第一章先落继母压制与婚书被换，第二章把旧账和规矩抬上桌，第三章让东宫开口锁住第一轮反击。"
        container["multi_line_guardrails"] = [
            "主线先稳住婚书局和女主位置，次线只轻触伯府旧账、顾家旧线和更高宫中权力网。",
            "每章都要同时推进压制关系变化和证据链变化，不要只靠口舌压人。"
        ]
        container["content_standard_alerts"] = [
            "避免后宅吵架替代权力换账",
            "避免太子口谕变成万能捷径",
            "不要提前把宫中旧案写透。"
        ]
    else:
        container.setdefault("opening_strategy", f"{title} 当前开篇先把主冲突拍到桌上。")
        container.setdefault("multi_line_guardrails", ["主线先推进真实位置变化，次线只轻触更大盘。"])
        container.setdefault("content_standard_alerts", ["避免解释先于事件。"])
    if "data" in data and isinstance(data["data"], dict):
        data["data"] = container
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        path.write_text(json.dumps(container, ensure_ascii=False, indent=2), encoding="utf-8")
    return "written"


def update_state(path: Path, bucket: str, chapter_key: str, packaging_note: str) -> str:
    state = load_json(path)
    chapter_entry, actual_key = chapter_meta_entry(state, chapter_key)
    chapter_entry["content_standard_flags"] = chapter_entry.get("content_standard_flags", [])
    chapter_entry["packaging_alignment_note"] = packaging_note
    learned_patterns = state.setdefault("learned_patterns", {})
    learned_patterns["externalized"] = True
    learned_patterns["sidecar_file"] = ".mighty/learned-patterns.json"
    learned_patterns["last_updated"] = now_iso()
    learned_patterns["available_sections"] = [
        "avoid_patterns",
        "content_standard_alerts",
        "high_point_preferences",
        "multi_line_guardrails",
        "opening_strategy",
        "user_feedback",
        "writing_style_preferences",
    ]
    meta = state.setdefault("meta", {})
    meta["updated_at"] = now_iso()
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return "written"


def save_packaging_file(project_root: Path, packaging: dict) -> str:
    packaging_dir = project_root / "包装"
    packaging_dir.mkdir(parents=True, exist_ok=True)
    output = packaging_dir / "包装方案.md"
    status = "written"
    if output.exists():
        existing = output.read_text(encoding="utf-8").strip()
        if existing:
            output = packaging_dir / "包装方案-writing-core.md"
            status = "written-sidecar"
    lines = [
        f"# 《{packaging['title']}》包装方案",
        "",
        "## 推荐主方案",
        "",
        "### 推荐书名",
        "",
        packaging["title"],
        "",
        "### 一句话卖点",
        "",
        packaging["one_liner"],
        "",
        "### 推荐简介",
        "",
        packaging["synopsis"],
        "",
        "## 包装约束",
        "",
        f"- opening_method_cue: {packaging['opening_method_cue']}",
        f"- genre_difference_cue: {packaging['genre_difference_cue']}",
        f"- premium_review_cue: {packaging['premium_review_cue']}",
        f"- overpromise_warning: {packaging['overpromise_warning']}",
        f"- payoff_timing_reminder: {packaging['payoff_timing_reminder']}",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")
    return status


def render_summary_block(name: str, payload: dict) -> list[str]:
    lines = [f"{name}:"]
    for key, value in payload.items():
        if isinstance(value, dict):
            lines.append(f"  {key}:")
            for sub_key, sub_value in value.items():
                lines.append(f"    {sub_key}: {sub_value}")
        else:
            lines.append(f"  {key}: {value}")
    return lines


def render_markdown(
    *,
    title: str,
    project_root: Path,
    bucket: str,
    chapters: str,
    evidence: list[str],
    packaging: dict,
    precheck: dict,
    writeback_preview: dict,
    mode: str,
) -> str:
    lines = [
        f"# Writing Core Smoke Draft: {title}",
        "",
        f"> 当前结果为 `{mode}`，需人工确认。",
        "",
        "## 适用范围",
        "",
        f"- 项目：`{project_root}`",
        f"- bucket：`{bucket}`",
        f"- 章节范围：`{chapters}`",
        "",
        "## 证据来源",
        "",
        *[f"- `{item}`" for item in evidence],
        "",
        "## 包装判断样本",
        "",
        "```md",
        *render_summary_block("packaging_judgment", packaging),
        "```",
        "",
        "## 预检判断样本",
        "",
        "```md",
        *render_summary_block("precheck_summary", precheck),
        "```",
        "",
        "## writeback 预览",
        "",
        "```md",
        *render_summary_block("writeback_preview", writeback_preview),
        "```",
        "",
    ]
    if str(writeback_preview.get("packaging_status", "")).startswith("written"):
        lines.extend(
            [
                "## 收口更新",
                "",
                "- 已生成：",
                "  - `包装/包装方案.md` 或 sidecar 包装文件",
                "- `packaging-needs-update` 已被消化成实际包装产物。",
                "",
            ]
        )
    return "\n".join(lines)


def run_smoke(
    *,
    project_root: str | Path,
    chapters: str,
    mode: str = "draft",
    output_path: str | Path | None = None,
    date_str: str | None = None,
    writeback: bool = False,
    save_packaging: bool = False,
) -> dict:
    if mode == "writeback" and not writeback:
        raise ValueError("writeback mode requires explicit writeback confirmation")
    project_root = Path(project_root)
    state_path = project_root / ".mighty" / "state.json"
    learned_path = project_root / ".mighty" / "learned-patterns.json"
    state = load_state(project_root)
    title = (state.get("meta") or {}).get("title") or project_root.name
    bucket = infer_bucket(state) or "unknown"
    text = collect_text(project_root, chapters)
    chapter_key = detect_target_chapter(state, chapters)
    packaging = packaging_template(title, bucket, text)
    packaging_exists = (project_root / "包装" / "包装方案.md").exists()
    precheck = precheck_template(bucket, packaging_exists)
    precheck["content_standard_summary"]["packaging_alignment_note"] = packaging["overpromise_warning"]
    evidence = evidence_sources(project_root, chapters)
    writeback_preview = build_writeback_preview(
        chapter_key,
        bucket,
        packaging_status="existing" if packaging_exists else "pending",
        writeback_status="pending",
    )
    path = Path(output_path) if output_path else default_output_path(project_root, title, sample_date(date_str))
    path.parent.mkdir(parents=True, exist_ok=True)
    packaging_status = "skipped"
    writeback_status = "skipped"
    effective_mode = mode
    if mode == "writeback":
        if learned_path.exists():
            update_learned_patterns(learned_path, bucket, title, text)
        writeback_status = update_state(state_path, bucket, chapter_key, packaging["overpromise_warning"])
        if save_packaging:
            packaging_status = save_packaging_file(project_root, packaging)
            precheck["packaging-needs-update"] = "no"
        else:
            packaging_status = "pending"
        writeback_preview = build_writeback_preview(
            chapter_key,
            bucket,
            packaging_status=packaging_status,
            writeback_status=writeback_status,
        )
    content = render_markdown(
        title=title,
        project_root=project_root,
        bucket=bucket,
        chapters=chapters,
        evidence=evidence,
        packaging=packaging,
        precheck=precheck,
        writeback_preview=writeback_preview,
        mode=effective_mode,
    )
    path.write_text(content, encoding="utf-8")
    return {
        "effective_mode": effective_mode,
        "output_path": str(path),
        "bucket": bucket,
        "writeback_status": writeback_status,
        "packaging_status": packaging_status,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_smoke(
        project_root=args.project_root,
        chapters=args.chapters,
        mode=args.mode,
        output_path=args.output,
        date_str=None,
        writeback=args.writeback,
        save_packaging=args.save_packaging,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
