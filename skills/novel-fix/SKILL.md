---
name: novel-fix
description: Fix a reviewed chapter in a Codex-managed novel project by applying targeted changes from review findings while preserving continuity and avoiding unnecessary full rewrites.
---

# Novel Fix

Use this skill when a chapter already has review findings and the user wants focused fixes instead of a broad rewrite.

## Inputs

- `chapter`
- optional `issues`
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
2. Read the chapter’s review findings from `chapter_meta`.
3. Decide whether the requested fix is:
   - `fix` sized: proceed
   - `rewrite` sized: stop and recommend `novel-rewrite`
4. Build a fix plan from:
   - critical issues
   - warnings
   - suggested fixes
   - explicit `issues` filter if the user provided one
5. Apply the smallest set of changes that materially resolves the chosen issues.
6. Preserve:
   - chapter purpose
   - key events
   - named entities
   - continuity with state and setting files
7. If preview mode is requested:
   - return a concise fix summary
   - include the proposed modified sections or chapter text
   - do not save
8. Otherwise:
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
