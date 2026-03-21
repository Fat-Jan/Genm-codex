---
name: novel-review
description: Review a chapter in a Codex-managed novel project for quality, continuity, pacing, and reader pull, then record the findings back into project state.
---

# Novel Review

Use this skill after a chapter draft exists and the user wants a structured quality assessment.

## Inputs

- `chapter`
- optional `detail`
- optional `threshold`
- optional `content_bucket`
- optional `tagpack`

## Preconditions

- `.mighty/state.json` exists
- `chapters/第N章.md` exists
- Shared references exist:
  - `../../shared/references/`
  - relevant shared profile under `../../shared/profiles/`

## Required reads

- `.mighty/state.json`
- `chapters/第N章.md`
- relevant profile under `../../shared/profiles/`

Read conditionally:

- previous chapter file or summary for continuity
- shared reference docs for reader-pull, pacing, and anti-AI constraints
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-mvp-tagpacks.yaml`
- `../../docs/fanqie-rule-priority-matrix.md`

## Workflow

1. Read `.mighty/state.json`.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
   - determine explicit `tagpack` if provided
2. Read `chapters/第N章.md`.
3. Read the genre/profile context.
4. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as upstream review constraints for:
     - opening speed
     - payoff timing
     - conflict density
     - chapter-end carryover
5. If Fanqie review is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - treat them as third-layer review checks for:
     - title / hook promise carryover
     - golden-three delivery
     - character vividness
     - suspense handoff and map-shift smoothness
   - do not let technique rules override canon or bucket law
6. If an explicit `tagpack` is given, or the request clearly asks for a tag-pack route such as `恶女`:
   - read `../../docs/fanqie-mvp-tagpacks.yaml`
   - prefer a tagpack whose `base_bucket` matches the active `content_bucket`
   - treat the chosen tagpack as a second-layer review lens after the bucket
7. Review for:
   - hook and reader pull
   - pacing
   - continuity
   - consistency
   - obvious AI-style issues
   - bucket-fit when applicable
   - bucket template fit when a first-batch MVP template exists:
     - primary reader motive
     - payoff cycle
     - ending-hook rule
   - tagpack fit when a matching tagpack exists:
     - protagonist_core
     - reader_motive
     - opening_rule
     - ending_hook_rule
8. Produce a structured report with:
   - total score
   - dimension scores
   - critical issues
   - warnings
   - suggested fixes
   - optional bucket-fit note
   - recommended next action:
     - `none`
     - `novel-fix`
     - `novel-polish`
     - `novel-rewrite`
9. Update review metadata for the chapter inside `.mighty/state.json`.
10. If the chapter falls below threshold, explicitly recommend `novel-rewrite`.

## Outputs

- review report in the response
- updated `.mighty/state.json`

## State update requirements

Update at minimum:

- `chapter_meta[chapter].review_score`
- `chapter_meta[chapter].review_grade`
- `chapter_meta[chapter].review_time`
- `chapter_meta[chapter].dimension_scores`
- `chapter_meta[chapter].needs_fix`

When the route is clear, also update:

- `chapter_meta[chapter].recommended_next_action`

## Notes

- Prefer deterministic, evidence-based findings over vague style criticism.
- If the user asks for auto-fix, route the main rewrite request through `novel-rewrite`.
- Do not claim a review passed unless the report actually shows the score and issues.
- Prefer `novel-fix` for narrow local issues, `novel-polish` for language-layer issues, and `novel-rewrite` for structural problems.
- When Fanqie rules stack, judge in this order:
  1. canon / state / chapter purpose
  2. active bucket fit
  3. writing-technique fit
  4. tagpack enhancement fit
- When Fanqie bucket constraints are active, use them to judge whether the chapter is delivering the expected click-through and carryover shape for that bucket, not to override canon or chapter purpose.
- If a first-batch MVP bucket config exists, prefer it over generic bucket commentary when judging fit.
- If a matching tagpack exists, use it as a second-layer lens on top of bucket fit, not as a new bucket.

## Route rules

Choose the primary route like this:

- `novel-fix`
  - local payoff weakness
  - one or two concrete issue clusters
  - no need to replace chapter purpose or ordering
- `novel-polish`
  - anti-AI cleanup
  - prose tightening
  - dialogue or description refinement
  - continuity remains structurally sound
- `novel-rewrite`
  - chapter purpose is wrong
  - event ordering or hook structure has to be rebuilt
  - multiple major issues point to a structural failure, not a local repair

If none of the above is needed, use `none`.
