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

Also read `../../docs/00-当前有效/upstream-structure-contract.md` and treat `shared/templates/project/creative-brief.md` as the earliest lightweight packaging-input source before a project has a stable full `总纲`.

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

Read `../../shared/references/shared/consumer-read-manifest.md` first.
Also read `../../docs/00-当前有效/quality-route-contract.md` for shared route language with `novel-review` / `novel-precheck`.

Shared bundles to apply here:

- `baseline-core`
- `launch-stack`
- `content-positioning`
- `market-adjustments`
- `fanqie-bucket`
- `fanqie-tagpack`

Always read:

- `.mighty/state.json`

Read for packaging generation:

- `大纲/总纲.md`
- `../../docs/opening-and-plot-framework/README.md`
- `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
- `../../docs/writing-core-framework/README.md`
- `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`

Read conditionally:

- `设定集/角色/主角.md`
- `设定集/角色/*.md` when naming a specific supporting character
- `设定集/家族/宅门真值表.md`
- `设定集/家族/小型家谱.md`
- `设定集/官制/官职真值表.md`
- `设定集/官制/权力层级图.md`
- `.mighty/market-data.json`
- `.mighty/market-adjustments.json`
- `.mighty/content-positioning.json`
- `chapter_meta` for recent review / fix context
- `包装/*.md` when existing packaging already exists
- `../../shared/references/writing/character-naming-guide.md`
- `../../shared/references/writing/ancient-household-kinship-guide.md`
- `../../shared/references/platforms/<platform>-style.md`
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-content-data-layer.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-mvp-tagpacks.yaml`
- `../../docs/fanqie-rule-priority-matrix.md`
- `../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
- `../../docs/opening-and-plot-framework/03-开篇故障与修正.md`
- `../../docs/opening-and-plot-framework/06-题材特化接口.md`
- `../../docs/writing-core-framework/06-精品审核与投稿前判断.md`
- `../../docs/writing-core-framework/08-开篇包装输入接口.md`
- `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md`
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
   - current `genre_profile.tagpacks`
   - current `genre_profile.strong_tags`
   - current `genre_profile.narrative_modes`
   - current `genre_profile.tone_guardrails`
   - current progress
   - current `market_adjustments` summary
   - treat `genre_profile.bucket` as the active `content_bucket` when no explicit `content_bucket` input is provided
   - determine explicit `tagpack` if provided
   - treat `state.genre_profile` as the primary runtime projection for profile-derived packaging constraints
   - if `.mighty/content-positioning.json` exists, prefer it as the project-facing composite-positioning sidecar
3. Read `大纲/总纲.md` and extract:
   - premise
   - main conflict
   - protagonist position
   - strongest hook
4. Read `../../docs/opening-and-plot-framework/README.md` and `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`.
   - also read `../../docs/writing-core-framework/README.md`
   - also read `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
   - when `.mighty/launch-stack.json` exists, consume `compiler_output.package_guardrails`
   - when additional raw profile detail is still needed, inspect it through `../../scripts/profile_contract.py`
   - when reading raw profile layers, use this order:
     - core profile
     - platform overlay when it exists
     - bucket overlay when it exists
     - reference files for long-form guidance
   - do not treat arbitrary embedded long-form sections in raw profile YAML as authoritative core config
5. If the request is `opening-hook`, `full`, or clearly depends on stronger first-screen packaging, also read:
   - `../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
   - `../../docs/opening-and-plot-framework/03-开篇故障与修正.md`
   - `../../docs/opening-and-plot-framework/06-题材特化接口.md`
   - `../../docs/writing-core-framework/06-精品审核与投稿前判断.md`
   - `../../docs/writing-core-framework/08-开篇包装输入接口.md`
   - `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
   - `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md` when the active Fanqie bucket matches a P0 overlay file
   - use them as packaging-side rules for:
     - keeping the opening promise legible
     - avoiding overpromising without a near-term payoff node
     - making the hook land on a concrete exchange rather than generic hype
     - converting opening method, genre-difference, premium-review, and overpromise cues into compact packaging constraints
6. If this is an ancient-family-power route and household truth files exist, read them before proposing outward relation words.
7. If the project clearly depends on court / palace / local-office / military rank logic and office truth files exist, read them before proposing outward官名.
8. Inspect recent project-local quality signals when they exist:
   - recent `chapter_meta`
   - recent `needs_fix`
   - recent `review_grade`
   - recent `recommended_next_action`
9. If `.mighty/market-adjustments.json` exists, treat that as the first packaging-side market hint source.
   When the active bucket equals `宫斗宅斗`，或 explicit `content_bucket=宫斗宅斗`，或 state/tagpack/genre 明显归属于宫廷/古代家族/宫斗宅斗这类路线时，额外从 adjustments 里查找以下 id：
   - `scan-surface-hook`
   - `scan-frontload-conflict`
   - `scan-kinship-truth-check`
   这些 id 仅在 palace 路线可读/可用，其他 bucket 不要外溢这些约束。
   每个命中后的 adjustment 必须转成具体包装指令并写入输出的 `包装约束` 段落，同时说明消费位置（书名、简介、开篇钩子等）：
   - `scan-surface-hook`：把钩点（婚配错位、赐婚/和离、高门婚配/权臣拉扯等）明确前置到首屏中的某个标题候选、简介段句或开篇包装提示，并交代哪个节奏节点落该钩子，防止钩子被压到中后段。
   - `scan-frontload-conflict`：包装承诺必须体现“先压后反击/换账”结构，说明压迫、陷害和即时反扑在前三章或首轮冲突单元一起闭合；若当前候选未满足，标出缺口和补救节点（比如第二章前置陷害）。
   - `scan-kinship-truth-check`：涉及嫡庶、齿序、赐婚、宫廷头衔等关系词前，要先读 `设定集/家族/宅门真值表.md`、`设定集/家族/小型家谱.md`（必要时再访 `设定集/官制/官职真值表.md`），包装主方案只输出已通过真值的关系词，未确认时声明为暂定方向并加注真实值缺口。
10. If state only has a summary/pointer form of `market_adjustments`, use it to locate the sidecar.
11. If `.mighty/market-data.json` exists, use it conservatively as a secondary signal.
12. If existing packaging files already exist under `包装/`, read them before proposing replacements so the new output can explain whether the current packaging should be kept, tightened, or replaced.
13. If the platform is 番茄 and a content bucket is explicitly given, or a current `genre_profile.bucket` exists, or the request clearly asks for Fanqie-first packaging:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as bucket-layer constraints that sit upstream of packaging
14. If Fanqie packaging is active, also read:
   - `../../docs/fanqie-content-data-layer.md`
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - when the active bucket is `宫斗宅斗` or another ancient-family-power route, also read `../../shared/references/writing/ancient-household-kinship-guide.md`
   - when the project涉及官场/宫廷/地方权力，也 read `../../shared/references/writing/ancient-office-hierarchy-guide.md`
   - use them as packaging-side optimization rules for:
     - title patterns
     - title clarity
     - title cue selection
     - title risk filtering
     - synopsis click-through structure
     - opening-hook sharpness
     - kinship / birth-order consistency before relation words are pushed into outward packaging
     - office-title / power-chain consistency before官名 is pushed into outward packaging
   - do not let writing-technique rules override canon or the active bucket
15. If an explicit `tagpack` is given, or the request clearly asks for a tag-pack style such as `恶女`:
   - read `../../docs/fanqie-mvp-tagpacks.yaml`
   - prefer a tagpack whose `base_bucket` matches the active `content_bucket`
   - if a matching tagpack exists, treat it as an overlay on top of the bucket rather than a replacement for the bucket
16. Resolve packaging mode:

When `.mighty/content-positioning.json` exists, also treat:

- `strong_tags` as candidate outward-facing packaging cues
- `tagpacks` as second-layer packaging overlays
- `narrative_modes` as packaging-safe structure hints
- `tone_guardrails` as package-risk filters

Do not turn every strong tag into a title token. Prefer:

- one primary bucket-facing cue
- one strong tag when it actually improves click-through clarity
- keep `tone_guardrails` mostly as internal packaging filters

Before finalizing title / synopsis / naming for submission-facing or replacement packaging:

1. derive a minimal canon sheet from `state`, `总纲`, and available role cards
2. if the project is ancient-family-power, verify:
   - whether `设定集/家族/宅门真值表.md` and `设定集/家族/小型家谱.md` exist
   - protagonist嫡庶来源
   - opponent relation word
   - whether `二姑娘 / 三姑娘` style terms have a valid birth-order map
3. if the project depends on官场/宫廷/地方权力, verify:
   - whether `设定集/官制/官职真值表.md` and `设定集/官制/权力层级图.md` exist
   - core官名属于什么类型
   - 该官名是否真能支撑包装里承诺的压制力
4. if the truth files are missing or unfilled, only provide provisional packaging directions and say that the main方案 is not yet safe to freeze
5. if outward packaging uses relation words or官名 but canon cannot support them, do not present that direction as the recommended main方案
6. for protagonist naming, report:
   - `search_scope`
   - `name_risk_level`
   - `collision_notes`

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

14. Standardize the output into these sections when useful:
   - `项目定位`
   - `内容桶判断`
   - `标签包判断`
   - `正文承载状态`
   - `推荐主方案`
   - `备选方案`
   - `暂不推荐方向`
   - `包装约束`
   - `是否建议更新现有包装`
15. If `save` is not requested, return concise proposals only.
16. If `save` is requested:
   - ensure `包装/` exists
   - save to:
     - `包装/书名方案.md`
     - `包装/简介方案.md`
     - `包装/命名方案.md`
     - `包装/开篇包装.md`
     - or `包装/包装方案.md` for `full`
17. Do not rewrite `.mighty/state.json` in first-version packaging flows.

## Output conventions

Prefer:

- one recommended main direction
- 2-4 viable alternatives
- Opening-and-plot rules should help package真实的开篇 promise，而不是放大正文无法兑现的空承诺。
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
- whether a minimal collision check was performed and what the risk level is

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
- Prefer `.mighty/market-adjustments.json` over raw `market-data.json` when both exist, because the former is already filtered into project-usable hints.
- If recent chapter review says `needs_fix`, do not overpromise packaging that the current text cannot support.
- If existing packaging files already match the current text and market direction, say so explicitly instead of forcing a rewrite.
- Use market-scan output as a weak-to-medium signal unless confidence is clearly high.
- Keep first-version packaging practical; do not pretend to A/B test live platform response.
- If the user actually wants prose-level chapter improvement, route to `novel-polish`, `novel-fix`, or `novel-rewrite`.
