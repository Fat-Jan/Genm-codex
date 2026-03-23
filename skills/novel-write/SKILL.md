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
- `../../docs/strong-quality-gate-policy.json`

## Workflow

1. Read `.mighty/state.json`.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
   - determine explicit `tagpack` if provided
2. Read the target chapter outline from `大纲/章纲/第N章.md`.
3. Read required setting files from `设定集/`.
4. Load the shared profile matching the project genre from `../../shared/profiles/`.
5. Read any useful local guidance already present in the project:
   - prefer `.mighty/learned-patterns.json`
   - prefer `.mighty/market-adjustments.json`
   - if sidecar files are absent, fall back to `state.learned_patterns` / `state.market_adjustments`
6. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as upstream prose constraints for:
     - opening speed
     - payoff timing
     - conflict density
     - chapter-end carryover
7. If Fanqie writing is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - `../../docs/fanqie-chapter-length-policy.json`
   - use them as third-layer prose optimization rules for:
     - first-page hook clarity
     - golden-three delivery
     - character vividness
     - suspense handoff and map-shift smoothness
     - chapter-length baseline
   - do not let writing-technique rules override canon, chapter purpose, or active bucket
8. If an explicit `tagpack` is given, or the request clearly asks for a tag-pack route such as `恶女`:
   - read `../../docs/fanqie-mvp-tagpacks.yaml`
   - prefer a tagpack whose `base_bucket` matches the active `content_bucket`
   - treat the chosen tagpack as a second-layer overlay on top of the bucket, not as a replacement for the bucket
9. Load high-value shared references from `../../shared/references/` only as needed.
10. Before drafting, run a strong pre-write source gate when the chapter clearly depends on kinship truth, office truth, world rules, era-sensitive objects, decor, rites, or household rules.
   - read `../../docs/strong-quality-gate-policy.json`
   - treat it as the single rule source for required truth files
   - if the required truth source is missing, stop before writing
   - report the blocking gap explicitly and route the user to the smallest upstream action such as:
     - `novel-setting`
     - `novel-character`
     - `novel-scan` only when external research is truly needed
   - do not hallucinate missing truth just to satisfy the chapter
11. If a previous chapter exists, read the prior chapter summary or chapter file for continuity.
12. Write `chapters/第N章.md` aligned to:
   - current state
   - target chapter outline
   - genre/platform expectations
   - learned style preferences when they are concrete
   - learned avoid-patterns when they are concrete
   - project-local market suggestions when they are relevant and low-risk
   - active Fanqie bucket constraints when they exist
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
   - and, when Fanqie chapter-length policy exists:
     - if `word_count` is not explicitly provided, treat the current bucket's preferred chapter range as the default target
13. Update `.mighty/state.json` with:
   - `progress.current_chapter`
   - `progress.total_words`
   - `progress.last_write_chapter`
   - `progress.last_write_time`
   - `chapter_meta`
   - `chapter_snapshots`
   - `summaries_index`
14. Do not write review scores here unless an actual review step was run.
15. After the base write succeeds, attempt a guarded automatic `novel-close` by default.
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
16. After a real writing round, the preferred maintenance hook remains:
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
- Strong write-time blocking rules must resolve from `../../docs/strong-quality-gate-policy.json`, not from duplicated prose thresholds in this skill.
- Do not invent structural state fields ad hoc; prefer extending the existing `.mighty/state.json` shape conservatively.
- Treat learned-pattern sidecar data as a preference signal, not a hard rule.
- Treat market-adjustment sidecar data as packaging or pacing guidance, not as a reason to break canon or outline purpose.
- `novel-write` does not inline `review -> route -> re-review`; guarded post-write convergence should hand off to `novel-close`.
- When Fanqie rules stack, apply them in this order:
  1. canon / state / chapter outline
  2. active bucket
  3. writing-technique optimization
  4. tagpack overlay
- When Fanqie bucket constraints are active, use them to tighten chapter rhythm and hook delivery, not to override canon, chapter purpose, or already established plot logic.
- If a first-batch MVP bucket config exists, prefer its reader-motive and payoff style over generic bucket language.
- If a matching tagpack exists, use it as a second-layer style/positioning overlay after bucket selection, not as a substitute for the bucket.
