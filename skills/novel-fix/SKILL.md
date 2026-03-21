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

## First-version scope

This version is a targeted fixer, not a universal editor.

Good fit:

- tighten explanatory passages
- patch continuity gaps
- strengthen weak hook or payoff beats
- align chapter text with existing character/state files

Not a good fit:

- major structural redesign
- full chapter rewrite from scratch
- outline-level changes

If the required change is too large or would replace most of the chapter, route to `novel-rewrite`.

## Workflow

1. Read the chapter and current state.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
2. Read the chapter’s review findings from `chapter_meta`.
3. Decide whether the requested fix is:
   - `fix` sized: proceed
   - `rewrite` sized: stop and recommend `novel-rewrite`
4. Build a fix plan from:
   - critical issues
   - warnings
   - suggested fixes
   - explicit `issues` filter if the user provided one
5. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as fix-side constraints for:
     - opening urgency
     - payoff clarity
     - conflict density
     - chapter-end carryover
6. Apply the smallest set of changes that materially resolves the chosen issues.
7. Preserve:
   - chapter purpose
   - key events
   - named entities
   - continuity with state and setting files
8. If preview mode is requested:
   - return a concise fix summary
   - include the proposed modified sections or chapter text
   - do not save
9. Otherwise:
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
- If the review findings and chapter text disagree, trust the current chapter plus state, not stale assumptions.
- If the fix requires changing a related file like `设定集/角色/主角.md`, keep that change minimal and explain why.
- When a Fanqie content bucket is active, use it to sharpen delivery for that bucket, not to broaden the chapter or smuggle in a rewrite.
- If a first-batch MVP bucket config exists, use it to resolve issues in the most direct bucket-fitting way available.
