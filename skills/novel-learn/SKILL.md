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
- analyze retrievable URL text when the current environment can actually fetch it
- analyze pasted text if the user provides it
- update `learned_patterns` conservatively

It should not:

- pretend unsupported external fetches succeeded
- invent a remote analysis result from a bare URL
- create a parallel style center such as `style_profile.json` for this workflow
- overwrite learned preferences with overconfident claims from a tiny sample

## Inputs

- chapter range
- or local file path
- or retrievable URL text
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
  - retrievable URL text
  - pasted text

## Required reads

Always read:

- `.mighty/state.json`
- `../../docs/writing-core-framework/README.md`

Read conditionally:

- `chapters/第NNN章.md`
- local source file provided by the user
- retrievable URL text acquired through `../../scripts/acquire_source_text.py`
- `大纲/总纲.md`
- `设定集/角色/*.md`
- `.mighty/launch-stack.json`
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-rule-priority-matrix.md`
- `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
- `../../docs/writing-core-framework/07-memory-压缩信号约定.md`

## Workflow

1. Determine the learning source:
   - chapter range
   - local file
   - retrievable URL
   - pasted text
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
2. If the user gives a URL and the current environment can retrieve it, acquire the source text first.
   - prefer using `../../scripts/acquire_source_text.py`
   - treat `success` and `partial` results with a real body as usable learning input
   - record clearly whether the result came from direct retrieval or fallback retrieval
3. If the user gives only an external link and no retrievable content is available in the current environment:
   - say the source is not directly retrievable in the current path
   - ask for pasted text or a local file instead
4. Read the source material.
5. Read `../../docs/writing-core-framework/README.md`.
   - when the result will be saved, also use `../../docs/writing-core-framework/07-memory-压缩信号约定.md` as the single memory contract
6. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as an analysis lens for:
     - opening speed
     - payoff visibility
     - conflict density
     - carryover style
7. If `.mighty/launch-stack.json` exists, also read `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`.
   - compare local early-chapter evidence against:
     - `primary_pivot`
     - `launch_grammar.primary`
     - `retention_protocol`
     - current `drift_signal`
   - treat launch-stack as an early-phase hypothesis to verify, not as a truth source that can override actual text evidence
8. If Fanqie learning is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - use them as third-layer grouping hints for:
     - title / hook preference
     - golden-three rhythm
     - character vividness
     - suspense handoff
   - do not let technique rules overwrite local evidence from the actual text
9. Extract only defensible learning signals:
   - dialogue style
   - description density
   - pacing preference
   - preferred high-point patterns
   - avoid patterns
   - `opening_strategy`
   - `multi_line_guardrails`
   - `content_standard_alerts`
10. In `quick` mode:
   - return a concise learning summary
11. In `deep` mode:
   - provide stronger evidence and more explicit pattern grouping
12. If the user wants the result saved:
   - prefer updating `.mighty/learned-patterns.json`
   - keep `.mighty/state.json` only as a lightweight summary / pointer
   - keep the output contract sidecar-first; do not create a second permanent style center such as `style_profile.json`
   - refresh:
     - `learned_patterns.writing_style_preferences`
     - `learned_patterns.high_point_preferences`
     - `learned_patterns.avoid_patterns`
     - `learned_patterns.opening_strategy`
     - `learned_patterns.multi_line_guardrails`
     - `learned_patterns.content_standard_alerts`
     - `auto_learn_config.last_auto_learn`
     - `auto_learn_config.last_auto_learn_chapter` when chapter-based
   - preserve active `recent_guardrails` unless the user explicitly asks to replace them or newer review evidence has already superseded them
   - when `.mighty/launch-stack.json` exists, update only the lightweight drift mirror in `.mighty/state.json`:
     - keep `launch_stack_drift_signal = none` when evidence is aligned or too weak
     - use `watch` when opening strategy / payoff rhythm appears to drift but the pivot is still plausible
     - use `strong` when the actual early-chapter route clearly diverges from the saved pivot or launch grammar
   - do not rewrite the full `launch-stack.json` sidecar inside `novel-learn`; if drift is `watch` or `strong`, recommend rerunning `fanqie_launch_stack.py`
13. When returning the result, explain where the learned signals are most useful next:
   - `novel-write`
   - `novel-polish`
   - `novel-precheck`

## Output conventions

Prefer:

- source analyzed
- whether it came from chapter range, local file, retrievable URL, or pasted text
- strongest learned signals
- confidence caveat
- optional save summary

## Notes

- Be conservative when sample size is small.
- Prefer updating `.mighty/learned-patterns.json` over growing `state.json`.
- If URL learning succeeds, say which retrieval path produced the usable body instead of pretending the source was fetched directly from memory.
- If the source is too short or too noisy, say so directly instead of pretending a strong learning result exists.
- Learned signals are most useful when they stay small, actionable, and easy for downstream writing skills to consume.
- Do not let reference-learning overwrite still-active `recent_guardrails` with broad style claims.
- When Fanqie rules stack, group findings in this order:
  1. actual text evidence
  2. active bucket lens
  3. writing-technique lens
  4. tagpack flavor only if it was explicitly active in the source
- When a Fanqie content bucket is active, use it to interpret local patterns more precisely, not to overwrite local evidence with generic platform slogans.
- If a first-batch MVP bucket config exists, prefer its reader-motive and payoff-cycle lens when grouping patterns.
- When a launch-stack sidecar exists, treat `drift_signal` as a conservative feedback channel only; `novel-learn` may refresh the mirror risk level, but it should not silently replace the compiled sidecar itself.
