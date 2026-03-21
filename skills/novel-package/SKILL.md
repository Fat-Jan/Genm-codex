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
- optional `content_bucket`
- optional `tagpack`
- optional `count`
- optional `target_character`
- optional `save`
- optional narrow judgment intent such as:
  - current text-carrying capacity
  - whether existing packaging should be updated

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
- `chapter_meta` for recent review / fix context
- `包装/*.md` when existing packaging already exists
- `../../shared/references/writing/character-naming-guide.md`
- `../../shared/references/platforms/<platform>-style.md`
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-content-data-layer.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-mvp-tagpacks.yaml`
- `../../docs/fanqie-rule-priority-matrix.md`
- `references/synopsis-platform-guide.md`
- `chapters/第001章.md` only when the user wants opening-hook refinement grounded in existing prose

## Workflow

1. Parse the requested packaging mode.
2. Read `.mighty/state.json` and determine:
   - title
   - genre
   - platform
   - optional `content_bucket`
   - current `genre_profile.bucket`
   - current progress
   - current `market_adjustments`
   - treat `genre_profile.bucket` as the active `content_bucket` when no explicit `content_bucket` input is provided
   - determine explicit `tagpack` if provided
3. Read `大纲/总纲.md` and extract:
   - premise
   - main conflict
   - protagonist position
   - strongest hook
4. Inspect recent project-local quality signals when they exist:
   - recent `chapter_meta`
   - recent `needs_fix`
   - recent `review_grade`
   - recent `recommended_next_action`
5. If state already contains project-local `market_adjustments`, treat those as the first packaging-side market hints.
6. If `.mighty/market-data.json` exists, use it conservatively as a secondary signal.
7. If existing packaging files already exist under `包装/`, read them before proposing replacements so the new output can explain whether the current packaging should be kept, tightened, or replaced.
8. If the platform is 番茄 and a content bucket is explicitly given, or a current `genre_profile.bucket` exists, or the request clearly asks for Fanqie-first packaging:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as bucket-layer constraints that sit upstream of packaging
9. If Fanqie packaging is active, also read:
   - `../../docs/fanqie-content-data-layer.md`
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - use them as packaging-side optimization rules for:
     - title patterns
     - title clarity
     - title cue selection
     - title risk filtering
     - synopsis click-through structure
     - opening-hook sharpness
   - do not let writing-technique rules override canon or the active bucket
10. If an explicit `tagpack` is given, or the request clearly asks for a tag-pack style such as `恶女`:
   - read `../../docs/fanqie-mvp-tagpacks.yaml`
   - prefer a tagpack whose `base_bucket` matches the active `content_bucket`
   - if a matching tagpack exists, treat it as an overlay on top of the bucket rather than a replacement for the bucket
11. Resolve packaging mode:

### narrow judgment shortcut

If the user is only asking for:

- current packaging fit
- current text-carrying capacity
- whether existing packaging should be updated

then do not expand into a full candidate set first.

Instead:

1. read:
   - `.mighty/state.json`
   - `大纲/总纲.md`
   - existing packaging under `包装/` when present
   - only the minimum recent chapter / review context needed
2. return a concise judgment first
3. only expand into full packaging proposals if the user also explicitly asks for them

### title

- produce 3-5 title candidates
- keep them platform-aware and genre-aware
- pick one recommended direction
- when Fanqie data-layer signals are available, vary candidates across:
  - click-first
  - steady longform
  - bucket-safe
  and explain which pattern each title is using

### synopsis

- produce 1-3 synopsis variants
- keep each variant concise and platform-fit
- emphasize conflict, hook, and reader pull

### naming

- if `target_character` is given, propose 3-7 names for that character
- otherwise focus on protagonist naming direction
- use the naming guide conservatively
- when Fanqie data-layer signals are active, prefer naming that matches:
  - current bucket readability
  - current tagpack tone
  - current title / synopsis positioning

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

12. Standardize the output into these sections when useful:
   - `项目定位`
   - `内容桶判断`
   - `标签包判断`
   - `正文承载状态`
   - `推荐主方案`
   - `备选方案`
   - `暂不推荐方向`
   - `包装约束`
   - `是否建议更新现有包装`
13. If `save` is not requested, return concise proposals only.
14. If `save` is requested:
   - ensure `包装/` exists
   - save to:
     - `包装/书名方案.md`
     - `包装/简介方案.md`
     - `包装/命名方案.md`
     - `包装/开篇包装.md`
     - or `包装/包装方案.md` for `full`
12. Do not rewrite `.mighty/state.json` in first-version packaging flows.

## Output conventions

Prefer:

- one recommended main direction
- 2-4 viable alternatives
- explicit reasons for what not to push
- compact packaging constraints tied to current canon and review state

For synopsis output, keep each version clearly labeled by angle, such as:

- 平台稳妥版
- 冲突强化版
- 爽点强化版

For full output, prefer this structure:

- `项目定位`
- `内容桶判断`
- `正文承载状态`
- `推荐主方案`
- `备选方案`
- `暂不推荐方向`
- `包装约束`
- `是否建议更新现有包装`

For narrow judgment-only output, prefer:

- `正文承载状态`
- `是否建议更新现有包装`

For naming output, explain:

- why the name fits the platform / genre
- what style it signals
- any risk of overused naming patterns

When the active bucket matches a first-batch MVP bucket such as `现实情感` or `宫斗宅斗`, make the packaging output more concrete by reflecting:

- the bucket’s `title_formula`
- the bucket’s `synopsis_formula`
- the bucket’s `opening_rule`
- the bucket’s `tag_pack`

When Fanqie content-data-layer signals are available, also reflect:

- `title_patterns`
- `title_cues`
- `synopsis_patterns`
- `click_through_risk`
- `overpromise_risk`

When an active tagpack such as `恶女 x 宫斗宅斗` is present, make the packaging output additionally reflect:

- the tagpack’s `positioning`
- the tagpack’s `reader_motive`
- the tagpack’s `title_cues`
- the tagpack’s `synopsis_cues`
- the tagpack’s `opening_rule`
- the tagpack’s `avoid`

## Save behavior

When saving:

- create `包装/` if missing
- overwrite only the mode-specific packaging file
- do not create extra hidden state files

## Notes

- Packaging should amplify what the project already is, not invent a different book.
- If Fanqie bucket constraints are present, treat them as upstream constraints rather than mere style hints.
- When both Fanqie bucket constraints and Fanqie writing-technique rules are active, apply them in this order:
  1. canon / state / outline
  2. active bucket
  3. Fanqie content-data-layer guidance
  4. writing-technique optimization
  5. tagpack overlay
- If a first-batch MVP bucket config exists, prefer it over generic bucket language.
- If a matching tagpack exists, use it as a second-layer overlay after bucket selection, not as a new standalone bucket.
- Prefer project-local `market_adjustments` over raw `market-data.json` when both exist, because the former is already filtered into project-usable hints.
- If recent chapter review says `needs_fix`, do not overpromise packaging that the current text cannot support.
- If existing packaging files already match the current text and market direction, say so explicitly instead of forcing a rewrite.
- Use market-scan output as a weak-to-medium signal unless confidence is clearly high.
- Keep first-version packaging practical; do not pretend to A/B test live platform response.
- If the user actually wants prose-level chapter improvement, route to `novel-polish`, `novel-fix`, or `novel-rewrite`.
