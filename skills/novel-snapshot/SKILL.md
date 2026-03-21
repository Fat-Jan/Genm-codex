---
name: novel-snapshot
description: Generate, load, compare, and list chapter snapshots in a Codex-managed novel project by using `chapter_snapshots` in `.mighty/state.json` and existing files under `.mighty/snapshots/`.
---

# Novel Snapshot

Use this skill when the user wants to inspect chapter state history, create a fresh snapshot, compare two chapter states, or load a past chapter snapshot as continuation context.

## Inputs

- operation:
  - `generate`
  - `load`
  - `diff`
  - `list`
- optional chapter number
- optional second chapter number for `diff`
- optional recent count for `list`

## Preconditions

- `.mighty/state.json` exists
- project uses `chapter_snapshots` and/or `.mighty/snapshots/`

## Primary snapshot sources

Prefer this order:

1. `chapter_snapshots` inside `.mighty/state.json`
2. `chapter_snapshots` inside `.mighty/state-archive.json`
3. `.mighty/snapshots/` filesystem artifacts

Do not invent a separate third snapshot system.

## Required reads

Always read:

- `.mighty/state.json`

Read conditionally:

- `.mighty/state-archive.json`
- `.mighty/snapshots/`
- `chapters/第NNN章.md`
- `设定集/角色/主角.md`

## Workflow

### generate

1. Read `.mighty/state.json`.
2. Resolve the target chapter:
   - explicit chapter if provided
   - otherwise `progress.current_chapter`
3. Read the target chapter file if it exists.
4. Build a conservative snapshot payload from current state:
   - chapter
   - timestamp
   - word count
   - protagonist state
   - active characters
   - active foreshadowing
   - knowledge state
   - key events / summary when available
5. Save the snapshot into:
   - `chapter_snapshots[chapter]`
6. If `.mighty/snapshots/` is already used by the project, also create a filesystem snapshot entry under:
   - `.mighty/snapshots/chapter-XXX/<timestamp>/`
7. Return what was generated.

### load

1. Read `.mighty/state.json`.
2. Load the requested chapter snapshot from `chapter_snapshots`.
3. If the structured snapshot is missing, look for it in `.mighty/state-archive.json`.
4. If the structured snapshot is still missing, look for a matching filesystem snapshot.
4. Return a concise continuation context:
   - protagonist state
   - active characters
   - active foreshadowing
   - key events
   - summary

### diff

1. Read both target snapshots.
2. Compare:
   - protagonist power / location / inventory / status
   - active characters
   - active foreshadowing
   - knowledge state
   - summary / key events
3. Return a concise diff, emphasizing meaningful state changes rather than every field.

### list

1. Read available snapshots from `chapter_snapshots`.
2. Optionally supplement with `.mighty/snapshots/` directory inventory.
3. Return a concise list of:
   - chapter
   - created time
   - word count
   - short summary

## State update requirements

When generating a new snapshot, update at minimum:

- `meta.updated_at`
- `chapter_snapshots[chapter]`

Do not mutate unrelated sections.

## Output conventions

### generate

- target chapter
- snapshot timestamp
- whether state snapshot and/or filesystem snapshot were written

### load

- chapter
- protagonist snapshot
- active foreshadowing summary
- key events / summary

### diff

- changed protagonist state
- changed foreshadowing state
- newly introduced entities / events

### list

- recent snapshots table or concise bullet list

## Notes

- First version should be conservative and state-centric.
- If the requested chapter has no snapshot, say so directly and suggest `generate`.
- If a filesystem snapshot and state snapshot disagree, prefer the current `state` snapshot, then the archived `state` snapshot, unless the user explicitly wants raw filesystem artifacts.
