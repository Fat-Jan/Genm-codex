---
name: novel-package
description: Create packaging-ready title, synopsis, naming, and opening-hook proposals for a Codex-managed novel project by reading project state, outline, genre/platform references, and optional market scan results, then optionally saving concise packaging docs under `包装/`.
---

# Novel Package

Use this skill when the user wants packaging-layer outputs for a Codex-managed novel project rather than mainline chapter prose.

## Positioning

This skill covers:

- title ideas
- synopsis variants
- character naming suggestions
- opening-hook packaging
- combined packaging proposals

It is not a replacement for:

- `novel-write`
- `novel-review`
- `novel-scan`
- `novel-genre`

It consumes signals from those systems and turns them into packaging outputs.

## Inputs

- optional `mode`
  - `title`
  - `synopsis`
  - `naming`
  - `opening-hook`
  - `full`
- optional `platform`
- optional `count`
- optional `target_character`
- optional `save`

## Preconditions

- `.mighty/state.json` exists
- `大纲/总纲.md` exists for `title`, `synopsis`, `opening-hook`, and `full`

## Required reads

Always read:

- `.mighty/state.json`

Read for packaging generation:

- `大纲/总纲.md`

Read conditionally:

- `设定集/角色/主角.md`
- `设定集/角色/*.md` when naming a specific supporting character
- `.mighty/market-data.json`
- `../../shared/references/writing/character-naming-guide.md`
- `../../shared/references/platforms/<platform>-style.md`
- `references/synopsis-platform-guide.md`
- `chapters/第001章.md` only when the user wants opening-hook refinement grounded in existing prose

## Workflow

1. Parse the requested packaging mode.
2. Read `.mighty/state.json` and determine:
   - title
   - genre
   - platform
   - current progress
   - current `market_adjustments`
3. Read `大纲/总纲.md` and extract:
   - premise
   - main conflict
   - protagonist position
   - strongest hook
4. If state already contains project-local `market_adjustments`, treat those as the first packaging-side market hints.
5. If `.mighty/market-data.json` exists, use it conservatively as a secondary signal.
6. Resolve packaging mode:

### title

- produce 3-5 title candidates
- keep them platform-aware and genre-aware
- pick one recommended direction

### synopsis

- produce 1-3 synopsis variants
- keep each variant concise and platform-fit
- emphasize conflict, hook, and reader pull

### naming

- if `target_character` is given, propose 3-7 names for that character
- otherwise focus on protagonist naming direction
- use the naming guide conservatively

### opening-hook

- produce 3-5 opening-hook or opening-packaging suggestions
- optimize for click-through and chapter-1 pull, not for fake hype

### full

- combine:
  - title candidates
  - one-line premise
  - synopsis variants
  - opening-hook suggestions
  - brief packaging notes

7. If `save` is not requested, return concise proposals only.
8. If `save` is requested:
   - ensure `包装/` exists
   - save to:
     - `包装/书名方案.md`
     - `包装/简介方案.md`
     - `包装/命名方案.md`
     - `包装/开篇包装.md`
     - or `包装/包装方案.md` for `full`
9. Do not rewrite `.mighty/state.json` in first-version packaging flows.

## Output conventions

Prefer:

- short candidate lists
- one recommended option
- compact rationale

For synopsis output, keep each version clearly labeled by angle, such as:

- 平台稳妥版
- 冲突强化版
- 爽点强化版

For naming output, explain:

- why the name fits the platform / genre
- what style it signals
- any risk of overused naming patterns

## Save behavior

When saving:

- create `包装/` if missing
- overwrite only the mode-specific packaging file
- do not create extra hidden state files

## Notes

- Packaging should amplify what the project already is, not invent a different book.
- Prefer project-local `market_adjustments` over raw `market-data.json` when both exist, because the former is already filtered into project-usable hints.
- Use market-scan output as a weak-to-medium signal unless confidence is clearly high.
- Keep first-version packaging practical; do not pretend to A/B test live platform response.
- If the user actually wants prose-level chapter improvement, route to `novel-polish`, `novel-fix`, or `novel-rewrite`.
