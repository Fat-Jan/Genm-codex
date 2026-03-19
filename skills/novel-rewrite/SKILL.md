---
name: novel-rewrite
description: Rewrite an existing chapter in a Codex-managed novel project while preserving continuity, creating snapshots, and updating review-aware state.
---

# Novel Rewrite

Use this skill when an existing chapter needs targeted revision for pacing, quality, style, or continuity.

## Inputs

- `chapter`
- `reason`
- optional `base`
- optional preview mode

## Preconditions

- `.mighty/state.json` exists
- `chapters/第N章.md` exists
- snapshot directory can be created under `.mighty/snapshots/`
- chapter outline and continuity context remain available

## Required reads

- `chapters/第N章.md`
- `.mighty/state.json`
- `大纲/章纲/第N章.md`

Read conditionally:

- previous review findings from `chapter_meta`
- current summary and snapshot data
- relevant setting files

## Workflow

1. Read the current chapter file.
2. Read `.mighty/state.json`.
3. Create a pre-rewrite snapshot under `.mighty/snapshots/`.
4. Read relevant outline and setting context.
5. If the chapter has prior review findings, use them as rewrite inputs.
6. Rewrite the chapter directly, focusing on the provided reason.
7. If preview mode is requested, return preview content without saving.
8. Otherwise save the new chapter content back to `chapters/第N章.md`.
9. Create a post-rewrite snapshot.
10. Update `.mighty/state.json` rewrite metadata and chapter snapshot info.

## Outputs

- updated `chapters/第N章.md` or preview content
- new snapshot artifacts under `.mighty/snapshots/`
- updated `.mighty/state.json`

## State update requirements

Update at minimum:

- `chapter_meta[chapter].last_rewrite_time`
- `chapter_meta[chapter].rewrite_reason`
- `chapter_meta[chapter].rewrite_count`
- `chapter_snapshots[chapter]`

## Notes

- Do not reference or rely on any nonexistent `rewrite-engine`.
- Keep the rewrite targeted; preserve core plot and setting unless the user explicitly asks for structural change.
- If the rewrite request is effectively a full story redesign, stop and ask for a new outline instead of forcing a local chapter rewrite.
