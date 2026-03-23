---
name: novel-write
description: Write a chapter in a Codex-managed novel project by reading the current state, outline, setting files, and shared profile assets, then updating chapter content and project state.
---

# Novel Write

Use this skill when the user wants to write the next chapter from the current outline and project state.

## Inputs

- `chapter`
- optional `word_count`
- optional `style`
- optional `content_bucket`
- optional `tagpack`
- optional `skip_close`

## Preconditions

- `.mighty/state.json` exists
- `大纲/章纲/第N章.md` exists for the target chapter
- `设定集/角色/主角.md` exists
- Shared assets exist:
  - `../../shared/profiles/`
  - `../../shared/references/`
- If this is not chapter 1, either the previous chapter file or a valid prior summary exists

## Required reads

Always read:

- `.mighty/state.json`
- `大纲/章纲/第N章.md`
- `设定集/角色/主角.md`
- `../../shared/references/shared/core-constraints.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`

Read conditionally:

- `大纲/总纲.md` for main-arc alignment
- relevant `设定集/世界观/*.md`
- relevant supporting character files in `设定集/角色/`
- previous chapter file or summary
- `.mighty/workflow_state.json` when workflow safety must be checked before post-write auto-close
- `.mighty/learned-patterns.json`
- `.mighty/market-adjustments.json`
- current `learned_patterns` summary inside `.mighty/state.json`
- current `market_adjustments` summary inside `.mighty/state.json`
- `../../docs/fanqie-chapter-length-policy.json`
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-mvp-tagpacks.yaml`
- `../../docs/fanqie-rule-priority-matrix.md`
- `../../docs/fanqie-resistance-and-cost-rules.md`
- `../../docs/gongdou-zhaidou-fault-funnel-review-card.md`
- `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
- `../../docs/anti-flattening-framework/04-角色动力系统.md`
- `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
- `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
- `../../docs/anti-flattening-framework/07-场景级群像推进.md`
- `../../docs/anti-flattening-framework/08-流派故障库.md`
- `../../docs/anti-flattening-framework/10-工具包与工作流.md`

## Workflow

1. Read `.mighty/state.json`.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
   - determine explicit `tagpack` if provided
2. Read `../../shared/references/shared/core-constraints.md`.
3. Read the target chapter outline from `大纲/章纲/第N章.md`.
4. Read required setting files from `设定集/`.
5. Read `../../docs/anti-flattening-framework/README.md` and `../../docs/anti-flattening-framework/01-总纲.md`.
6. Load the shared profile matching the project genre from `../../shared/profiles/`.
7. Read any useful local guidance already present in the project:
   - prefer `.mighty/learned-patterns.json`
   - prefer `.mighty/market-adjustments.json`
   - if sidecar files are absent, fall back to `state.learned_patterns` / `state.market_adjustments`
8. When the chapter route is multi-character, multi-faction, relationship-heavy, politics-heavy, transmigration, system-driven, or the user explicitly asks for人物活人感/反脸谱化:
   - read:
     - `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
     - `../../docs/anti-flattening-framework/04-角色动力系统.md`
     - `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
     - `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
     - `../../docs/anti-flattening-framework/07-场景级群像推进.md`
     - `../../docs/anti-flattening-framework/08-流派故障库.md`
     - `../../docs/anti-flattening-framework/10-工具包与工作流.md`
   - use them as prose-side structural constraints for:
     - keeping supporting cast from collapsing into pure function roles
     - preserving non-protagonist goals in scenes
     - showing relation debt / power asymmetry where relevant
     - keeping gains earned through visible resistance and cost
     - leaving scene residue for the next chapter
9. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as upstream prose constraints for:
     - opening speed
     - payoff timing
     - conflict density
     - chapter-end carryover
10. If Fanqie writing is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - `../../docs/fanqie-chapter-length-policy.json`
   - `../../docs/fanqie-resistance-and-cost-rules.md`
   - when the active bucket is `宫斗宅斗`, also read `../../docs/gongdou-zhaidou-fault-funnel-review-card.md`
   - use them as third-layer prose optimization rules for:
     - first-page hook clarity
     - golden-three delivery
     - character vividness
     - suspense handoff and map-shift smoothness
     - chapter-length baseline
     - visible resistance
     - visible cost
     - partial payoff instead of frictionless resolution
     - when the active bucket is `宫斗宅斗`, run a lightweight funnel preflight before drafting:
       - lock one effective transaction unit with a concrete contested object
       - ensure the chapter will change at least one of power / information / relationship / resource ledgers
       - ensure one non-protagonist role carries an independent agenda in the core scene
       - block summary-only progression, threat-only carryover, and authority-only shortcut wins
   - do not let writing-technique rules override canon, chapter purpose, or active bucket
11. If an explicit `tagpack` is given, or the request clearly asks for a tag-pack route such as `恶女`:
   - read `../../docs/fanqie-mvp-tagpacks.yaml`
   - prefer a tagpack whose `base_bucket` matches the active `content_bucket`
   - treat the chosen tagpack as a second-layer overlay on top of the bucket, not as a replacement for the bucket
12. Load high-value shared references from `../../shared/references/` only as needed.
13. If a previous chapter exists, read the prior chapter summary or chapter file for continuity.
14. Write `chapters/第N章.md` aligned to:
   - current state
   - target chapter outline
   - genre/platform expectations
   - learned style preferences when they are concrete
   - learned avoid-patterns when they are concrete
   - project-local market suggestions when they are relevant and low-risk
   - active Fanqie bucket constraints when they exist
   - active resistance/cost constraints when they exist:
     - key gain must meet visible resistance
     - visible cost must remain on page
     - major alliance or evidence should not arrive frictionlessly
     - chapter-end win should usually leave residual risk
   - active first-batch MVP bucket template signals when they exist:
     - primary reader motive
     - tag pack
     - opening rule
     - payoff cycle
     - ending-hook rule
   - active tagpack overlay when it exists:
     - positioning
     - protagonist_core
     - reader_motive
     - opening_rule
     - payoff_rule
     - ending_hook_rule
   - active anti-flattening rules when they exist:
     - supporting characters should not only appear as buttons or mouthpieces
     - at least one meaningful non-protagonist intention should stay visible in a key scene when the route needs群像
     - important gains should leave relation, risk, or cost residue
     - relation or faction support should not read as frictionless auto-alignment
   - when the active bucket is `宫斗宅斗` and the funnel card is active:
     - do not let the chapter pass as summary-only progression
     - make the contested object, blocker, and changed ledger legible on page
     - avoid resolving the chapter mainly through one authority shortcut
     - keep at least one key non-protagonist role from collapsing into pure delivery or reaction
   - and, when Fanqie chapter-length policy exists:
     - if `word_count` is not explicitly provided, treat the current bucket's preferred chapter range as the default target
15. Update `.mighty/state.json` with:
   - `progress.current_chapter`
   - `progress.total_words`
   - `progress.last_write_chapter`
   - `progress.last_write_time`
   - `chapter_meta`
   - `chapter_snapshots`
   - `summaries_index`
16. Do not write review scores here unless an actual review step was run.
17. After the base write succeeds, attempt a guarded automatic `novel-close` by default.
   - run this only for a normal single-chapter `novel-write`
   - do not inherit this behavior into `novel-batch`
   - if `skip_close=true`, do not attempt auto-close and report that it was intentionally skipped
   - otherwise attempt `novel-close` only when all guards pass:
     - `.mighty/state.json` exists
     - `大纲/章纲/第N章.md` exists
     - the chapter file was written successfully
     - current workflow state is not clearly failed or malformed when workflow state exists
     - the user did not explicitly request a write-only pass
   - if guards fail, do not fake execution; report the exact skip reason
   - if auto-close fails after the chapter was written, keep the write as successful and report the post-write close failure clearly
18. After a real writing round, the preferred maintenance hook remains:
   - `scripts/post-task-maintenance.py <project_root> --trigger write`
   which should call the maintenance chain for stable entities, runtime guidance, and state thinning.
   - maintenance is not the place where prose mutation or `novel-close` execution should live

## Chapter state update requirements

At minimum, update:

- `chapter_meta[chapter]`
- `chapter_snapshots[chapter]`
- `summaries_index[chapter]`
- `entities.characters.protagonist` if the chapter changes protagonist state
- `plot_threads` if foreshadowing or suspense changes

## Outputs

- `chapters/第N章.md`
- updated `.mighty/state.json`
- optional write summary including:
  - whether auto-close was attempted
  - whether it ran or was skipped
  - route used or skip reason when available

## Failure handling

- If `.mighty/state.json` is missing, stop and route back to `novel-init`.
- If the target chapter outline is missing, stop and route back to `novel-outline`.
- If continuity-critical state is ambiguous, prefer using the existing state file over guessing from prose.
- Do not invent new top-level state sections unless strictly required.

## Notes

- Keep writing aligned to the outline and current state.
- Do not invent structural state fields ad hoc; prefer extending the existing `.mighty/state.json` shape conservatively.
- Treat learned-pattern sidecar data as a preference signal, not a hard rule.
- Treat market-adjustment sidecar data as packaging or pacing guidance, not as a reason to break canon or outline purpose.
- `novel-write` does not inline `review -> route -> re-review`; guarded post-write convergence should hand off to `novel-close`.
- When Fanqie rules stack, apply them in this order:
  1. canon / state / chapter outline
  2. active bucket
  3. anti-flattening structure rules
  4. writing-technique optimization
  5. tagpack overlay
- When Fanqie bucket constraints are active, use them to tighten chapter rhythm and hook delivery, not to override canon, chapter purpose, or already established plot logic.
- When Fanqie resistance rules are active, prefer fast scenes with earned gains over frictionless automatic progression.
- If a first-batch MVP bucket config exists, prefer its reader-motive and payoff style over generic bucket language.
- If a matching tagpack exists, use it as a second-layer style/positioning overlay after bucket selection, not as a substitute for the bucket.
- Anti-flattening rules should make people and factions act like real participants in the chapter, but they do not authorize changing the outline goal or smuggling a rewrite into ordinary writing.
- When the active bucket is `宫斗宅斗`, the funnel card should be used as a light preflight, not as a full review pass; it is there to stop thin transaction skeletons from becoming finished chapters.
