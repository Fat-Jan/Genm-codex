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
.mighty/launch-stack.json
.mighty/market-adjustments.json
.mighty/setting-gate.json
chapters/
大纲/总纲.md
大纲/卷纲/
大纲/章纲/
设定集/角色/主角.md
设定集/家族/
设定集/官制/
设定集/势力/
设定集/地点/
设定集/物品/
设定集/世界观/
设定集/力量体系.md
参考资料/
```

For ancient-family-power routes such as `宫斗宅斗 / 古代言情 / 历史家族权力`, also create:

```text
设定集/家族/宅门真值表.md
设定集/家族/小型家谱.md
设定集/官制/官职真值表.md
设定集/官制/权力层级图.md
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
   - treat `novel-genre` / `scripts/profile_contract.py` as the authoritative profile-contract entrance
   - do not invent a one-off profile parsing rule inside `novel-init`
   - if the project idea is still fuzzy, first seed `shared/templates/project/creative-brief.md`
   - follow `../../docs/00-当前有效/upstream-structure-contract.md` for the boundary between `creative-brief`, `总纲`, `launch-stack`, and `content-positioning`
3. Detect whether this is an ancient-family-power route.
   - Use genre, resolved profile slug, and any obvious project framing.
   - Typical matches include `palace-intrigue`, `ancient-romance`, `historical`, and projects whose core conflict depends on 宅门 / 宗族 / 嫡庶 / 继室 / 婚配法统.
4. Create the canonical project directories.
5. Initialize `.mighty/state.json` using the v5 state shape from the source project as the baseline.
6. Fill the initial state with:
   - `meta.title`
   - `meta.genre`
   - `meta.platform`
   - `meta.target_chapters`
   - `meta.target_words`
   - `progress.current_chapter = 0`
   - empty `chapter_meta`, `chapter_snapshots`, `summaries_index`
   - keep `chapter_meta` extensible for later per-chapter review fields such as:
     - `recommended_next_action`
     - `anti_flattening_flags`
     - `anti_flattening_summary`
7. Seed starter files from `../../shared/templates/` when possible.
   - If this is an ancient-family-power route, seed first:
     - `设定集/家族/宅门真值表.md` from `../../shared/templates/project/ancient-household-truth-sheet.md`
     - `设定集/家族/小型家谱.md` from `../../shared/templates/project/ancient-mini-genealogy.md`
     - `设定集/官制/官职真值表.md` from `../../shared/templates/project/ancient-office-truth-sheet.md`
     - `设定集/官制/权力层级图.md` from `../../shared/templates/project/ancient-power-ladder.md`
   - These files are upstream truth artifacts, not optional decoration.
8. Create lightweight sidecar files:
   - `.mighty/learned-patterns.json`
   - `.mighty/launch-stack.json`
   - `.mighty/market-adjustments.json`
   and keep `.mighty/state.json` only with small summary/pointer forms for those sections
   - initialize `.mighty/launch-stack.json` with a contract-compatible placeholder instead of an empty file:
```json
{
  "version": "1.0",
  "phase": "preselect",
  "premise_line": "",
  "primary_pivot": "",
  "secondary_pivot": "",
  "launch_grammar": {
    "primary": "",
    "candidates": [],
    "confidence": "low"
  },
  "retention_protocol": {
    "enabled_rules": [],
    "priority_rules": [],
    "violations": []
  },
  "compiler_output": {
    "outline_focus": [],
    "chapter_1_3_targets": [],
    "review_watchpoints": [],
    "precheck_risks": [],
    "package_guardrails": []
  },
  "confidence": "low",
  "drift_signal": "none",
  "reselect_note": ""
}
```
   - initialize launch-stack mirrors in `state.json`:
     - `active_launch_grammar`
     - `active_primary_pivot`
     - `launch_stack_phase`
     - `launch_stack_drift_signal`
9. Write:
   - `大纲/总纲.md` with a minimal outline scaffold
   - `设定集/角色/主角.md` with a starter protagonist scaffold
   - `设定集/力量体系.md` with a minimal system scaffold
   - If this is an ancient-family-power route, mark the initial total outline as provisional until:
     - protagonist mother source exists
     - core rival relation exists
     - birth-order map exists for any `二姑娘 / 三姑娘` style terms
     - core office titles and actual power chain are no longer empty when the story depends on官场/宫廷/地方权力
10. Record the chosen profile in `state.genre_profile`.
   - keep this as a lightweight projection, not a raw profile dump
   - preferred projection fields:
     - `loaded`
     - `节奏`
     - `爽点密度`
     - `strand权重`
     - `特殊约束`
   - when profile layer details are needed, derive them from `../../scripts/profile_contract.py` rather than ad-hoc field picking
11. After the starter files exist, run `setting gate(init)`:
   - preferred helper: `python3 scripts/setting_gate.py <project_root> --stage init`
   - aggressively materialize starter skeleton cards for repeated roles / locations / factions / items when they are already inferable from local project truth
   - write `.mighty/setting-gate.json` as the current gate snapshot
12. Report created files, chosen profile, whether the ancient-family-power route was detected, whether `setting gate(init)` ran, and any fallback decisions.

## Failure handling

- If no exact profile matches, choose the nearest slug and state the fallback explicitly.
- If templates are missing, create minimal plain Markdown placeholders instead of failing silently.
- Never create a root-level `state.json`; the canonical path is `.mighty/state.json`.
- If the directory already contains a conflicting project structure, stop and ask before overwriting.

## Notes

- Prefer creating a minimal valid state over filling every optional field.
- If no exact genre profile exists, choose the nearest profile slug and state the fallback explicitly.
- Do not silently create a root-level `state.json`; the canonical path is `.mighty/state.json`.
- For ancient-family-power routes, do not treat `大纲/总纲.md` as fully locked at init time unless the household truth sheet and mini genealogy already support the outward relation words.
- For ancient-family-power routes, do not freeze官名 into outward packaging until the office truth sheet and power ladder are minimally filled.
- `chapter_meta` is the preferred place for lightweight per-chapter structural review signals; do not create a parallel top-level anti-flattening store.
