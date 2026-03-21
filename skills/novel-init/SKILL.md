---
name: novel-init
description: Initialize a new webnovel project for Codex by creating the required project structure, seed state file, and starter outline/setting files using the shared profiles and templates.
---

# Novel Init

Use this skill when the user wants to start a new novel project from scratch in a fresh directory.

## Inputs

- `title`
- `genre`
- optional `platform`
- optional `target_chapters`
- optional `target_words`

## Preconditions

- Current working directory is the target novel project root
- Shared assets exist:
  - `../../shared/profiles/`
  - `../../shared/templates/`
- The directory is either empty or the user explicitly wants to initialize in-place

## Required output structure

Create:

```text
.mighty/state.json
.mighty/learned-patterns.json
.mighty/market-adjustments.json
chapters/
大纲/总纲.md
大纲/卷纲/
大纲/章纲/
设定集/角色/主角.md
设定集/势力/
设定集/地点/
设定集/物品/
设定集/世界观/
设定集/力量体系.md
参考资料/
```

## State requirements

Initialize `.mighty/state.json` with, at minimum:

- `version`
- `meta`
- `progress`
- `entities`
- `plot_threads`
- `knowledge_base`
- `quality_metrics`
- `learned_patterns`
- `platform_config`
- `genre_profile`
- `chapter_meta`
- `chapter_snapshots`
- `summaries_index`
- `character_states`
- `constraints_loaded`

## Workflow

1. Validate required inputs.
2. Resolve the closest matching profile slug from `../../shared/profiles/`.
3. Create the canonical project directories.
4. Initialize `.mighty/state.json` using the v5 state shape from the source project as the baseline.
5. Fill the initial state with:
   - `meta.title`
   - `meta.genre`
   - `meta.platform`
   - `meta.target_chapters`
   - `meta.target_words`
   - `progress.current_chapter = 0`
   - empty `chapter_meta`, `chapter_snapshots`, `summaries_index`
6. Seed starter files from `../../shared/templates/` when possible.
7. Create lightweight sidecar files:
   - `.mighty/learned-patterns.json`
   - `.mighty/market-adjustments.json`
   and keep `.mighty/state.json` only with small summary/pointer forms for those sections
8. Write:
   - `大纲/总纲.md` with a minimal outline scaffold
   - `设定集/角色/主角.md` with a starter protagonist scaffold
   - `设定集/力量体系.md` with a minimal system scaffold
9. Record the chosen profile in `state.genre_profile`.
10. Report created files, chosen profile, and any fallback decisions.

## Failure handling

- If no exact profile matches, choose the nearest slug and state the fallback explicitly.
- If templates are missing, create minimal plain Markdown placeholders instead of failing silently.
- Never create a root-level `state.json`; the canonical path is `.mighty/state.json`.
- If the directory already contains a conflicting project structure, stop and ask before overwriting.

## Notes

- Prefer creating a minimal valid state over filling every optional field.
- If no exact genre profile exists, choose the nearest profile slug and state the fallback explicitly.
- Do not silently create a root-level `state.json`; the canonical path is `.mighty/state.json`.
