---
name: novel-learn
description: Learn writing patterns from local chapter ranges or user-provided files/text in a Codex-managed novel project, then update `learned_patterns` conservatively without pretending unsupported external fetches succeeded.
---

# Novel Learn

Use this skill when the user wants to extract reusable writing patterns from the current project or from text they have already provided.

## Positioning

This version is a local-content learner first.

It should:

- analyze existing project chapters
- analyze a local file path if the user provides one
- analyze pasted text if the user provides it
- update `learned_patterns` conservatively

It should not:

- pretend unsupported external fetches succeeded
- invent a remote analysis result from a bare URL
- overwrite learned preferences with overconfident claims from a tiny sample

## Inputs

- chapter range
- or local file path
- or user-provided text content
- optional `depth`
  - `quick`
  - `deep`
- optional `content_bucket`
- optional explicit save intent

## Preconditions

- `.mighty/state.json` exists
- at least one usable source exists:
  - chapter files
  - local file
  - pasted text

## Required reads

Always read:

- `.mighty/state.json`

Read conditionally:

- `chapters/第NNN章.md`
- local source file provided by the user
- `大纲/总纲.md`
- `设定集/角色/*.md`
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-rule-priority-matrix.md`

## Workflow

1. Determine the learning source:
   - chapter range
   - local file
   - pasted text
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
2. If the user gives only an external link and no retrievable content is available in the current environment:
   - say the source is not directly retrievable in the current path
   - ask for pasted text or a local file instead
3. Read the source material.
4. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as an analysis lens for:
     - opening speed
     - payoff visibility
     - conflict density
     - carryover style
5. If Fanqie learning is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - use them as third-layer grouping hints for:
     - title / hook preference
     - golden-three rhythm
     - character vividness
     - suspense handoff
   - do not let technique rules overwrite local evidence from the actual text
6. Extract only defensible learning signals:
   - dialogue style
   - description density
   - pacing preference
   - preferred high-point patterns
   - avoid patterns
7. In `quick` mode:
   - return a concise learning summary
8. In `deep` mode:
   - provide stronger evidence and more explicit pattern grouping
9. If the user wants the result saved:
   - prefer updating `.mighty/learned-patterns.json`
   - keep `.mighty/state.json` only as a lightweight summary / pointer
   - refresh:
     - `learned_patterns.writing_style_preferences`
     - `learned_patterns.high_point_preferences`
     - `learned_patterns.avoid_patterns`
     - `auto_learn_config.last_auto_learn`
     - `auto_learn_config.last_auto_learn_chapter` when chapter-based
10. When returning the result, explain where the learned signals are most useful next:
   - `novel-write`
   - `novel-polish`
   - `novel-precheck`

## Output conventions

Prefer:

- source analyzed
- strongest learned signals
- confidence caveat
- optional save summary

## Notes

- Be conservative when sample size is small.
- Prefer updating `.mighty/learned-patterns.json` over growing `state.json`.
- If the source is too short or too noisy, say so directly instead of pretending a strong learning result exists.
- Learned signals are most useful when they stay small, actionable, and easy for downstream writing skills to consume.
- When Fanqie rules stack, group findings in this order:
  1. actual text evidence
  2. active bucket lens
  3. writing-technique lens
  4. tagpack flavor only if it was explicitly active in the source
- When a Fanqie content bucket is active, use it to interpret local patterns more precisely, not to overwrite local evidence with generic platform slogans.
- If a first-batch MVP bucket config exists, prefer its reader-motive and payoff-cycle lens when grouping patterns.
