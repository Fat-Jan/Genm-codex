---
name: novel-outline
description: Generate or refine the total outline and chapter outline files for a Codex-managed novel project using the shared profiles, references, and current project state.
---

# Novel Outline

Use this skill after project initialization, or when the user wants to generate or revise the story outline.

## Inputs

- `mode`: `total` or `chapter`
- optional `start`
- optional `count`
- optional multi-option request

## Preconditions

- `.mighty/state.json` exists
- `大纲/` exists
- Shared assets exist:
  - `../../shared/profiles/`
  - `../../shared/references/`

## Workflow

1. Read `.mighty/state.json` for `meta.title`, `meta.genre`, and `meta.platform`.
2. Load the relevant shared profile for rhythm and reader expectations.
3. For `mode=total`:
   - create or update `大纲/总纲.md`
   - include hook, premise, main conflict, arc direction, and ending direction
4. For `mode=chapter`:
   - create `大纲/章纲/第N章.md`
   - include chapter goal, conflict, reveal, hook, and continuity notes
5. Keep chapter outlines specific enough for writing, but short enough to maintain.
6. If the user asks for multiple options, present 2-3 outline variants before locking one in.
7. Report which outline files were created or updated.

## Output files

- `大纲/总纲.md`
- `大纲/章纲/第N章.md`

## Notes

- Treat `大纲/总纲.md` as the law for later writing steps.
- If the user asks for broad ideation, provide multiple outline options before locking one in.
- Do not generate chapter writing content here; this skill ends at outline artifacts.
