---
name: novel-batch
description: Write a small batch of chapters in sequence for a Codex-managed novel project, reusing shared context while updating state after each chapter.
---

# Novel Batch

Use this skill when the user wants to generate multiple chapters in one ordered run.

## Inputs

- `start`
- `count`
- optional `word_count`

## Preconditions

- `.mighty/state.json` exists
- relevant chapter outlines already exist under `大纲/章纲/`
- `count` should stay small enough to preserve continuity confidence

## Workflow

1. Validate `start` and `count`.
2. Read `.mighty/state.json`.
3. Read the required range of chapter outlines.
4. Reuse the same shared profile and setting context for the batch.
5. Generate chapters **sequentially**, not independently:
   - write chapter N
   - update `.mighty/state.json`
   - use the updated state for chapter N+1
6. After the batch, return a compact summary:
   - chapters generated
   - total words
   - notable new entities
   - notable new foreshadowing
7. After the batch, the preferred automatic hook is:
   - `scripts/post-task-maintenance.py <project_root> --trigger batch`
   so the project does not keep accumulating all runtime facts only inside `state.json`

## Outputs

- multiple files under `chapters/`
- updated `.mighty/state.json`
- batch summary

## Notes

- Do not treat batch generation as parallel writing; continuity is more important than speed.
- Prefer small batches (for example <= 5 chapters) unless the user explicitly asks for more.
- Treat post-batch maintenance as part of the stable workflow, not as optional cleanup.
