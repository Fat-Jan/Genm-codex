---
name: novel-foreshadowing
description: Manage foreshadowing threads in a Codex-managed novel project by planting, listing, checking, and resolving foreshadowing items tracked in `.mighty/state.json`.
---

# Novel Foreshadowing

Use this skill when the user wants to plant, inspect, update, or resolve foreshadowing and suspense threads in a Codex-managed novel project.

## Inputs

- action:
  - plant
  - list
  - view
  - payoff
  - check
  - status
- optional `id`
- optional `name`
- optional expected range

## Preconditions

- `.mighty/state.json` exists
- project uses `plot_threads.foreshadowing` in state

## Primary data sources

Always read:

- `.mighty/state.json`

Read conditionally:

- `大纲/总纲.md`
- `大纲/章纲/*.md`
- target chapter file if the user wants context-specific planting or payoff

## Workflow

### plant

1. Create a new foreshadowing entry in `.mighty/state.json`.
2. Assign:
   - id
   - name
   - description
   - planted chapter
   - expected range
   - status
3. If the user does not provide an id, generate the next `fN`.

### list

1. Read `plot_threads.foreshadowing`.
2. Group by status when helpful.
3. Highlight warning or overdue items first.

### view

1. Show the selected foreshadowing item in full.
2. Include planted chapter, expected range, current status, and related entities.

### payoff

1. Mark the item as resolved.
2. Record the payoff chapter and summary if provided.

### check / status

1. Compare current chapter to expected ranges.
2. Surface `active`, `warning`, and `overdue` items.
3. Recommend the most urgent next payoff target.

## Outputs

- updated `.mighty/state.json`
- optional grouped foreshadowing report

## Notes

- Prefer state-based foreshadowing truth over scattered prose notes.
- If state and outline disagree, report the mismatch instead of silently choosing one.
- Keep foreshadowing IDs stable once created.
