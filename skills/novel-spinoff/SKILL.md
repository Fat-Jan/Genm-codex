---
name: novel-spinoff
description: Create a lightweight spinoff chapter inside a Codex-managed novel project by reusing the current canon, state, and setting files without requiring a multi-book universe system.
---

# Novel Spinoff

Use this skill when the user wants to write a side story, character episode, alternate branch, or special extra inside the current project.

## Inputs

- `type`
  - `角色篇`
  - `外传`
  - `IF线`
  - `节日特典`
  - `前传`
  - `后传`
- optional `chapter`
- optional `word_count`
- optional `focus_character`
- optional `time_point`

## First-version scope

This version is intentionally single-project and lightweight.

It should:

- reuse the current project as canon source
- produce a clearly marked spinoff chapter file
- preserve consistency with the main project unless the type explicitly allows divergence

It should not:

- require `.mighty/books/`
- require a universe-wide canon system
- implement a full multi-book lineage manager

## Preconditions

- `.mighty/state.json` exists
- `大纲/总纲.md` exists
- `设定集/角色/主角.md` exists

## Required reads

Always read:

- `.mighty/state.json`
- `大纲/总纲.md`
- `设定集/角色/主角.md`

Read conditionally:

- `设定集/角色/*.md` for `focus_character`
- `设定集/力量体系.md`
- relevant `chapters/*.md`
- `大纲/章纲/*.md` when the requested time point is close to the mainline

## Spinoff type guidance

### 角色篇

- focus on one character’s perspective or hidden side
- must preserve character core traits

### 外传

- expand a side thread or world corner
- should not conflict with the mainline

### IF线

- must clearly mark the divergence point
- should be labeled as non-mainline

### 节日特典

- can be lighter in tone
- still should not break core characterization

### 前传 / 后传

- use cautiously in version one
- only proceed if the user gives enough timeline context

## Workflow

1. Parse the requested spinoff type and scope.
2. Read current project canon sources.
3. Determine the safest single-project placement:
   - if a `chapter` name is provided, use it
   - otherwise create a clearly labeled spinoff filename under `chapters/`
4. Build a short canon summary for the spinoff:
   - what must remain true
   - what may diverge
   - where the story sits relative to the mainline
5. Write the spinoff chapter.
6. Mark the output clearly as spinoff content.
7. Update `.mighty/state.json` conservatively:
   - add chapter metadata
   - do not let a spinoff silently replace mainline progress unless the user explicitly wants that

## File placement

Prefer one of:

- `chapters/番外-<名称>.md`
- `chapters/外传-<名称>.md`
- `chapters/IF线-<名称>.md`
- `chapters/特典-<名称>.md`

Keep naming explicit so the file is not mistaken for the next mainline chapter.

## State update requirements

When saving a spinoff, update conservatively:

- `meta.updated_at`
- `chapter_meta[spinoff_id]`
- optional summary entry

Do not advance `progress.current_chapter` unless the user explicitly wants the spinoff to count as mainline progression.

## Output conventions

Return:

- spinoff type
- canon constraints used
- output file path
- whether the result is canonical, side-canonical, or explicitly non-canonical

## Notes

- If the user asks for a heavy multi-book parent-canon workflow, say that the current Codex version only supports the lightweight single-project path.
- If the request would obviously spoil or contradict unresolved mainline facts, say so and recommend a safer framing.
