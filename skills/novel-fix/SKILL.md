---
name: novel-fix
description: Fix a reviewed chapter in a Codex-managed novel project by applying targeted changes from review findings while preserving continuity and avoiding unnecessary full rewrites.
---

# Novel Fix

Use this skill when a chapter already has review findings and the user wants focused fixes instead of a broad rewrite.

## Inputs

- `chapter`
- optional `issues`
- optional `content_bucket`
- optional preview intent

## Preconditions

- `.mighty/state.json` exists
- `chapters/第N章.md` exists
- `chapter_meta[N]` contains usable review findings or issue hints

## Required reads

- `.mighty/state.json`
- `chapters/第N章.md`
- `大纲/章纲/第N章.md`
- `../../shared/references/shared/core-constraints.md`

Read conditionally:

- `chapter_meta[N].critical_issues`
- `chapter_meta[N].warnings`
- `chapter_meta[N].suggested_fixes`
- relevant `设定集/角色/*.md`
- `设定集/力量体系.md`
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-rule-priority-matrix.md`
- `../../docs/fanqie-resistance-and-cost-rules.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`
- `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
- `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
- `../../docs/anti-flattening-framework/09-诊断信号与快速修复.md`
- `../../docs/anti-flattening-framework/10-工具包与工作流.md`
- `../../docs/anti-flattening-framework/12-案例对照与校准.md`

## First-version scope

This version is a targeted convergent fixer, not a universal editor.

Good fit:

- tighten explanatory passages
- patch continuity gaps
- strengthen weak hook or payoff beats
- align chapter text with existing character/state files
- finish all local issue clusters that belong to the same repair round

Not a good fit:

- major structural redesign
- full chapter rewrite from scratch
- outline-level changes

If the required change is too large or would replace most of the chapter, route to `novel-rewrite`.

Default intent for the current workflow:

- finish one chapter’s local repair work in one pass when possible
- avoid leaving easy same-scene fixes for another micro-pass
- if two repair attempts still do not close the chapter, escalate instead of nibbling

## Workflow

1. Read the chapter and current state.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
2. Read `../../shared/references/shared/core-constraints.md`.
3. Read the chapter’s review findings from `chapter_meta`.
   - when the issue cluster includes人物扁平、关系空心、阵营一声道、主角推进零代价等问题, also read:
     - `../../docs/anti-flattening-framework/README.md`
     - `../../docs/anti-flattening-framework/01-总纲.md`
     - `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
     - `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
     - `../../docs/anti-flattening-framework/09-诊断信号与快速修复.md`
     - `../../docs/anti-flattening-framework/10-工具包与工作流.md`
     - `../../docs/anti-flattening-framework/12-案例对照与校准.md`
4. Check prior repair-attempt history from `chapter_meta`.
   - use `fix_count + polish_count` when available
   - if repair attempts are already `>= 2` and the same critical issues still survive, stop and recommend `novel-rewrite`
5. Decide whether the requested fix is:
   - `fix` sized: proceed
   - `rewrite` sized: stop and recommend `novel-rewrite`
6. Build a fix plan from:
   - critical issues
   - warnings
   - suggested fixes
   - explicit `issues` filter if the user provided one
   - default to covering all local issue clusters from the latest review, not just one tiny symptom
   - if multiple easy fixes land in the same scene or paragraph, batch them into the same edit pass
7. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as fix-side constraints for:
     - opening urgency
     - payoff clarity
     - conflict density
     - chapter-end carryover
8. If Fanqie fix rules are active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - `../../docs/fanqie-resistance-and-cost-rules.md`
   - use them as third-layer fix-side optimization for:
     - first-page hook sharpness
     - explanation density
     - character vividness
     - suspense handoff
     - resistance / cost visibility
     - partial payoff repair
   - do not let technique rules override canon, chapter purpose, or active bucket
9. Apply the smallest set of changes that materially resolves the chosen issues.
   - when anti-flattening repair is active, prefer local repairs such as:
     - adding a hidden need
     - adding a non-protagonist action beat
     - restoring a relation debt or power asymmetry
     - making cost / residual risk visible
   - when you already touch a sentence or paragraph for a local repair, also absorb trivial wording / redundancy cleanup there instead of leaving a second micro-pass for `novel-polish`
   - do not smuggle a full structural rewrite into a fix pass
10. Preserve:
   - chapter purpose
   - key events
   - named entities
   - continuity with state and setting files
11. If preview mode is requested:
   - return a concise fix summary
   - include the proposed modified sections or chapter text
   - do not save
12. Otherwise:
   - create a backup under `.mighty/backup/`
   - save the fixed chapter
   - update fix metadata in `.mighty/state.json`
   - if a companion setting file must be synchronized for continuity, update it explicitly and mention it

## Outputs

- preview-only fix proposal, or
- updated `chapters/第N章.md`
- optional synced companion file
- optional backup artifact
- updated `.mighty/state.json`

## State update requirements

When saving, update at minimum:

- `meta.updated_at`
- `progress.last_write_chapter`
- `progress.last_write_time`
- `chapter_meta[N].updated_at`
- `chapter_meta[N].word_count`
- `chapter_meta[N].summary` when materially changed
- `chapter_meta[N].last_fix_time`
- `chapter_meta[N].fix_count`
- `chapter_meta[N].fixed_issues`

If the fix resolves previously recorded issues, also update when appropriate:

- `chapter_meta[N].needs_fix`
- `chapter_meta[N].critical_issues`
- `chapter_meta[N].warnings`

## Notes

- Prefer precise local edits over broad stylistic churn.
- This skill may be selected as the primary route inside `novel-close`.
- Prefer one convergent local repair pass over several tiny follow-up passes.
- If the review findings and chapter text disagree, trust the current chapter plus state, not stale assumptions.
- If the fix requires changing a related file like `设定集/角色/主角.md`, keep that change minimal and explain why.
- When Fanqie rules stack, apply them in this order:
  1. canon / state / chapter purpose
  2. active bucket
  3. anti-flattening repair rules
  4. writing-technique optimization
  5. tagpack overlay when explicitly active
- When a Fanqie content bucket is active, use it to sharpen delivery for that bucket, not to broaden the chapter or smuggle in a rewrite.
- If a first-batch MVP bucket config exists, use it to resolve issues in the most direct bucket-fitting way available.
- If anti-flattening repair would require replacing the chapter’s goal, scene order, or core conflict source, stop and route to `novel-rewrite`.
