---
name: novel-setting
description: Create, inspect, update, and summarize worldbuilding assets in a Codex-managed novel project, including power systems, factions, locations, items, and core world rules.
---

# Novel Setting

Use this skill when the user wants to manage worldbuilding assets in a Codex-managed novel project.

## Inputs

- type:
  - power
  - faction
  - location
  - item
  - rule
- action:
  - create
  - view
  - update
  - list
- optional name

## Preconditions

- `设定集/` exists
- `.mighty/state.json` exists if the project tracks setting versions or downstream consistency

## Primary data sources

Always read as needed:

- `设定集/力量体系.md`
- `设定集/势力/*.md`
- `设定集/地点/*.md`
- `设定集/物品/*.md`
- `.mighty/state.json`

Read conditionally:

- `大纲/总纲.md`
- `大纲/章纲/*.md`

## Workflow

### create

1. Determine the target setting file path from `type` and optional `name`.
2. Create the file with a minimal valid scaffold.
3. Include only the fields needed to make the setting usable downstream.

### view

1. Read the target setting file.
2. Summarize the core rules, entities, or constraints.

### update

1. Read the existing setting file.
2. Apply the requested changes without expanding unrelated sections.
3. If the setting materially changes downstream writing assumptions, note the impact.

### list

1. List relevant files under the matching setting directory.
2. Return a concise inventory.

## Type-specific expectations

### power

- canonical path: `设定集/力量体系.md`
- include tiers, breakthrough logic, constraints, and any special systems

### faction

- canonical path: `设定集/势力/<名称>.md`
- include type, influence, key figures, and relation to protagonist

### location

- canonical path: `设定集/地点/<名称>.md`
- include purpose, atmosphere, and story relevance

### item

- canonical path: `设定集/物品/<名称>.md`
- include type, owner, function, and limits

### rule

- either update the relevant setting file or create a dedicated world-rule note under `设定集/世界观/`

## Outputs

- updated files under `设定集/`
- optional note about downstream consistency impact

## Notes

- Prefer the smallest setting edit that preserves internal consistency.
- If a requested change would invalidate existing chapter content, say so explicitly.
- Only touch `.mighty/state.json` when the project already uses `setting_versions` or related tracking there.
