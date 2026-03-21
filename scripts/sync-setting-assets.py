#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


COMMON_SURNAMES = (
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕张孔曹严华金魏陶姜戚谢邹喻柏水窦章"
    "云苏潘葛奚范彭郎鲁韦马苗凤花方俞任袁柳唐罗薛伍余米贝姚孟顾尹江钟温康田樊胡凌"
    "霍虞万支柯卢莫丁贾夏石付白邱邵程熊纪舒董梁杜阮蓝闵席季麻强贾路娄危童颜郭梅盛林"
    "刁徐丘骆高蔡樊胡霍柯裴陆荣翁荀惠曲封芮储靳汲胥焦巴宫宁简饶曾"
)

NAME_STOPWORDS = {
    "东宫", "婚书", "旧账", "账页", "顾家", "伯府", "祠堂", "药单", "银票", "副册", "外院",
    "书房", "旧档", "偏殿", "回帖", "实账", "东宫局", "婚书局", "旧案", "顾承州终", "顾家来人",
}

FACTION_SUFFIXES = ("府", "宫", "家", "司", "部", "阁", "宗", "门", "院")
LOCATION_HINTS = ("房", "堂", "仓", "庄", "院", "门", "廊", "阁", "祠")

SYNC_BEGIN = "<!-- NOVEL-SYNC:BEGIN -->"
SYNC_END = "<!-- NOVEL-SYNC:END -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync stable setting assets from state into 设定集/")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--mode", choices=["all", "characters", "locations", "factions"], default="all")
    parser.add_argument("--recent-chapters", type=int, default=8)
    parser.add_argument("--characters", default="")
    parser.add_argument("--locations", default="")
    parser.add_argument("--factions", default="")
    return parser.parse_args()


def load_state(project_root: Path) -> dict:
    state_path = project_root / ".mighty" / "state.json"
    return json.loads(state_path.read_text())


def recent_chapter_numbers(state: dict, recent_n: int) -> list[int]:
    nums = sorted(int(k) for k in state.get("chapter_meta", {}).keys())
    return nums[-recent_n:]


def chapter_texts(project_root: Path, chapter_numbers: list[int]) -> list[str]:
    texts = []
    for num in chapter_numbers:
        path = project_root / "chapters" / f"第{num:03d}章.md"
        if path.exists():
            texts.append(path.read_text())
    return texts


def infer_characters(state: dict, texts: list[str]) -> list[str]:
    candidates = []
    protagonist = state["entities"]["characters"]["protagonist"]["name"]
    joined = "\n".join(texts)
    role_names = re.findall(r"[\u4e00-\u9fff]{1,3}(?:氏|爷|娘子|妈妈|嬷嬷|族叔|太子)", joined)
    personal_names = re.findall(rf"[{COMMON_SURNAMES}][\u4e00-\u9fff]{{1,2}}", joined)
    for name in role_names + personal_names:
        if protagonist in name:
            continue
        if name in NAME_STOPWORDS:
            continue
        candidates.append(name)
    counts: dict[str, int] = {}
    for c in candidates:
        counts[c] = counts.get(c, 0) + 1
    result = [name for name, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])) if count >= 2]
    return result[:12]


def infer_locations(state: dict) -> list[str]:
    locs = []
    current = state["entities"]["locations"].get("current")
    if current:
        locs.append(current)
    for x in state["entities"]["locations"].get("important", []):
        if x not in locs:
            locs.append(x)
    return locs


def infer_factions(state: dict, texts: list[str], locations: list[str]) -> list[str]:
    factions = []
    joined = "\n".join(texts)
    tokens = re.findall(r"[\u4e00-\u9fff]{2,8}", joined)
    for token in tokens + locations:
        if token.endswith(FACTION_SUFFIXES) and token not in factions:
            factions.append(token)
    return factions[:10]


def parse_csv(arg: str) -> list[str]:
    return [x.strip() for x in arg.split(",") if x.strip()]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def replace_sync_block(existing: str, block: str) -> str:
    if SYNC_BEGIN in existing and SYNC_END in existing:
        start = existing.index(SYNC_BEGIN)
        end = existing.index(SYNC_END) + len(SYNC_END)
        return existing[:start] + block + existing[end:]
    if existing.endswith("\n"):
        return existing + "\n" + block + "\n"
    return existing + "\n\n" + block + "\n"


def write_file(path: Path, header: str, core_lines: list[str], sync_lines: list[str]) -> None:
    sync_block = "\n".join([SYNC_BEGIN, "## 当前同步信息", *sync_lines, SYNC_END])
    if path.exists():
        new_text = replace_sync_block(path.read_text(), sync_block)
    else:
        parts = [header, "", *core_lines, "", sync_block, ""]
        new_text = "\n".join(parts)
    path.write_text(new_text)


def role_hint(name: str) -> str:
    if name.endswith("氏"):
        return "后宅长辈/压制者"
    if name.endswith("娘子"):
        return "管事角色"
    if name.endswith("妈妈") or name.endswith("嬷嬷"):
        return "旧仆/证人"
    if name.endswith("爷"):
        return "家族长辈"
    if name == "太子":
        return "更高权力角色"
    return "重要角色"


def write_character_files(project_root: Path, state: dict, names: list[str], chapter_nums: list[int]) -> list[str]:
    out = []
    char_dir = project_root / "设定集" / "角色"
    ensure_dir(char_dir)
    protagonist = state["entities"]["characters"]["protagonist"]
    protagonist_path = char_dir / "主角.md"
    protagonist_sync = [
        f"- 最近同步章节：第{chapter_nums[0]:03d}章~第{chapter_nums[-1]:03d}章",
        f"- 当前章节：第{state['progress']['current_chapter']}章",
        f"- 当前地点：{protagonist['location']['current']}",
        f"- 当前状态：{' / '.join(protagonist.get('status', []))}",
        f"- 当前目标：{' / '.join(protagonist.get('current_goals', []))}",
    ]
    if protagonist_path.exists():
        protagonist_path.write_text(replace_sync_block(protagonist_path.read_text(), "\n".join([SYNC_BEGIN, "## 当前同步信息", *protagonist_sync, SYNC_END])) + ("\n" if not protagonist_path.read_text().endswith("\n") else ""))
        out.append(str(protagonist_path))
    for name in names:
        if name == protagonist["name"]:
            continue
        path = char_dir / f"{name}.md"
        core = [
            "## 基本信息",
            f"- 姓名：{name}",
            f"- 角色定位：{role_hint(name)}",
            "",
            "## 故事作用",
            "- 当前由同步层标记为稳定出现的重要角色，后续可再人工补充。",
        ]
        sync = [
            f"- 最近同步章节：第{chapter_nums[0]:03d}章~第{chapter_nums[-1]:03d}章",
            f"- 当前与主角关系：需后续人工确认，当前按“重要角色”跟踪",
            f"- 当前备注：该角色已在近段正文/摘要中稳定出现，已从运行态沉淀到角色卡。",
        ]
        write_file(path, f"# {name}", core, sync)
        out.append(str(path))
    return out


def write_location_files(project_root: Path, names: list[str], chapter_nums: list[int]) -> list[str]:
    out = []
    loc_dir = project_root / "设定集" / "地点"
    ensure_dir(loc_dir)
    for name in names:
        path = loc_dir / f"{name}.md"
        core = [
            "## 基本信息",
            f"- 名称：{name}",
            "- 类型：重要地点",
            "",
            "## 故事作用",
            "- 该地点已被同步层判定为后续仍会使用或具规则作用的地点。",
        ]
        sync = [
            f"- 最近同步章节：第{chapter_nums[0]:03d}章~第{chapter_nums[-1]:03d}章",
            "- 当前备注：由 state 中的重要地点与当前地点同步生成。",
        ]
        write_file(path, f"# {name}", core, sync)
        out.append(str(path))
    return out


def write_faction_files(project_root: Path, names: list[str], chapter_nums: list[int]) -> list[str]:
    out = []
    fac_dir = project_root / "设定集" / "势力"
    ensure_dir(fac_dir)
    for name in names:
        path = fac_dir / f"{name}.md"
        core = [
            "## 基本信息",
            f"- 名称：{name}",
            "- 类型：重要势力",
            "",
            "## 故事作用",
            "- 该势力已被同步层判定为后续仍会参与主线推进的组织/家门/权力单位。",
        ]
        sync = [
            f"- 最近同步章节：第{chapter_nums[0]:03d}章~第{chapter_nums[-1]:03d}章",
            "- 当前备注：由正文与地点/摘要中的稳定势力名同步生成。",
        ]
        write_file(path, f"# {name}", core, sync)
        out.append(str(path))
    return out


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root)
    state = load_state(project_root)
    chapters = recent_chapter_numbers(state, args.recent_chapters)
    texts = chapter_texts(project_root, chapters)

    characters = parse_csv(args.characters) or infer_characters(state, texts)
    locations = parse_csv(args.locations) or infer_locations(state)
    factions = parse_csv(args.factions) or infer_factions(state, texts, locations)

    synced = {"characters": [], "locations": [], "factions": []}
    if args.mode in ("all", "characters"):
        synced["characters"] = write_character_files(project_root, state, characters, chapters)
    if args.mode in ("all", "locations"):
        synced["locations"] = write_location_files(project_root, locations, chapters)
    if args.mode in ("all", "factions"):
        synced["factions"] = write_faction_files(project_root, factions, chapters)

    print(json.dumps({
        "project": str(project_root),
        "chapters_window": chapters,
        "characters": [Path(x).name for x in synced["characters"]],
        "locations": [Path(x).name for x in synced["locations"]],
        "factions": [Path(x).name for x in synced["factions"]],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
