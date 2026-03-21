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
- **安全上限：一次性最多 3 章**

## Workflow

1. Validate `start` and `count`.
   - if `count > 3`, stop and require the batch to be split
   - do not silently continue a larger batch just because the user asked for it
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
   - `scripts/post-task-maintenance.py <project_root> --trigger batch --batch-count <count>`
   so the project does not keep accumulating all runtime facts only inside `state.json`
8. Treat the batch as valid only if the batch quality gate passes:
   - `scripts/check-batch-quality-gate.py`
   - if the quality gate fails, stop the long batch pattern and return to `review / fix / rewrite`

## Outputs

- multiple files under `chapters/`
- updated `.mighty/state.json`
- batch summary

## Notes

- Do not treat batch generation as parallel writing; continuity is more important than speed.
- **一次性最多 3 章。**
- More than 3 chapters in one run is treated as unsafe because it increases the risk of:
  - 提纲化短章
  - 后半段字数断崖
  - 概述代替演出
  - AI 摘要腔
- Treat post-batch maintenance as part of the stable workflow, not as optional cleanup.
