---
name: novel-sync
description: Sync stable characters, locations, factions, and items from current project state into `设定集/`, keeping `state` as the runtime truth while steadily materializing long-lived assets.
---

# Novel Sync

Use this skill when a Codex-managed novel project has written chapters and `.mighty/state.json` is carrying more and more long-lived information that should be materialized back into `设定集/`.

## Purpose

This skill is the first implementation of the `state -> 设定集` synchronization layer.

It should:

- keep `state` as runtime truth
- extract stable entities from recent chapter/state context
- create or refresh minimal files under:
  - `设定集/角色/`
  - `设定集/地点/`
  - `设定集/势力/`
  - `设定集/物品/`
- optionally thin old chapter metadata out of `state`
- optionally externalize heavy runtime guidance payloads out of `state`

It should not:

- treat `设定集/` as a stronger truth source than current chapter text + current state
- generate huge cast bibles for one-off entities
- rewrite the project’s canon or state

## Inputs

- optional `mode`
  - `all`
  - `characters`
  - `locations`
  - `factions`
  - `items`
  - `review-queue`
  - `thin-state`
- optional `recent_chapters`
- optional explicit lists:
  - `characters`
  - `locations`
  - `factions`
  - `items`

## Preconditions

- `.mighty/state.json` exists
- `设定集/` exists
- at least one written chapter or summary exists

## Primary data sources

Always read:

- `.mighty/state.json`

Read conditionally:

- recent `chapters/第NNN章.md`
- recent `chapter_meta`
- recent `summaries_index`
- existing files under `设定集/`
- [state-thinning-and-setting-sync.md](/Users/arm/Desktop/vscode/Genm-codex/docs/state-thinning-and-setting-sync.md)

## Sync principles

1. `state` is current runtime truth.
2. `设定集/` is the long-lived asset layer.
3. Only sync entities that are:
   - repeated
   - still active
   - likely to matter again
4. When current text + state disagree with an old card, prefer current text + state and refresh the card.

## Workflow

1. Read `.mighty/state.json`.
2. Determine the recent chapter window:
   - default to a small recent range such as 5-8 chapters
3. Read only the minimum recent chapter text / summaries needed.
4. Determine candidate sync targets:
   - protagonist current-state section in `主角.md`
   - stable active characters
   - important locations
   - important factions
   - important items
5. Create missing files conservatively.
6. If a file already exists:
   - keep human-authored content
   - only refresh a generated sync block
7. If `mode=thin-state`:
   - write `.mighty/state-archive.json`
   - move old `chapter_meta`
   - move old `chapter_snapshots`
   - move old `summaries_index`
   - keep only a recent chapter window inside `.mighty/state.json`
8. In a full maintenance round, prefer also writing:
   - `.mighty/learned-patterns.json`
   - `.mighty/market-adjustments.json`
   while keeping `state` only as a lightweight summary/pointer
9. Maintain a lightweight ambiguity queue:
   - `.mighty/sync-review.json`
   - use it for low-confidence candidates that should not be materialized blindly
   - use `.mighty/sync-overrides.json` to record resolved aliases or ignored candidates
10. Return a compact sync summary:
   - files created
   - files refreshed
   - whether state thinning happened
   - any ambiguous entities that still need human confirmation

## Notes

- This is a synchronization layer, not a replacement for `novel-character` or `novel-setting`.
- Use `novel-character` when the user wants to author or revise a specific role card in detail.
- Use `novel-setting` when the user wants to author or revise a specific location / faction / item file in detail.
- Use `novel-sync` when the user wants the project to stop depending purely on `state` for long-lived assets.
- `thin-state` must not alter protagonist runtime state, progress, active foreshadowing, or current quest fields.
- Treat `items` as evidence-chain / repeated-use assets; do not create cards for disposable props.
- For post-write maintenance, prefer running `scripts/project-maintenance.py` so sync, guidance split, and state thinning stay in one path.
- For queue review/closure, prefer `scripts/review-sync-queue.py`.
