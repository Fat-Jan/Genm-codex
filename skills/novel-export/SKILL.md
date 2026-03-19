---
name: novel-export
description: Export a Codex-managed novel project to a requested format, starting with the simplest reliable path and applying platform-aware rules only when necessary.
---

# Novel Export

Use this skill when the user wants to export chapters from the project into a shareable or submission-ready format.

## Inputs

- `format`
- optional `start`
- optional `end`
- optional platform target

## Preconditions

- chapter files exist under `chapters/`
- export destination can be created under `exports/`
- shared references exist for platform-specific rules

## Workflow

1. Determine the export range.
2. Read the selected chapter files.
3. For `txt`, use the simplest reliable path first.
4. If a platform-specific export is requested, apply only the relevant formatting rules from shared references.
5. Write output under `exports/`.
6. Report:
   - exported file path
   - covered chapter range
   - format used
   - any warnings

## Outputs

- files under `exports/`

## Notes

- Treat single-range `txt` export as the minimum baseline path.
- Do not promise binary formats unless the environment and dependencies are available.
- If a requested format is unsupported in the current environment, fall back to `txt` and state the downgrade explicitly.
