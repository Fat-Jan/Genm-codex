---
name: novel-character
description: Create, inspect, update, and summarize character files in a Codex-managed novel project, including relationship context and lightweight role tracking.
---

# Novel Character

Use this skill when the user wants to manage character setup inside a Codex-managed novel project.

## Inputs

- action:
  - create
  - view
  - update
  - list
  - relation
  - graph
- optional character name

## Preconditions

- `设定集/角色/` exists
- `.mighty/state.json` exists for relationship and active character context

## Primary data sources

Always read as needed:

- `设定集/角色/*.md`
- `.mighty/state.json`

Read conditionally:

- `设定集/关系图.md`
- `大纲/总纲.md`
- `大纲/章纲/*.md`

## Workflow

### create

1. Create a new character file under `设定集/角色/`.
2. Include at minimum:
   - basic identity
   - personality
   - motivation
   - role in story
   - relationship to protagonist
3. If the user provides sparse input, keep the file minimal and mark missing sections explicitly.

### view

1. Read the requested character file.
2. Summarize role, current state, and relationship relevance.

### update

1. Read the existing character file.
2. Apply only the requested changes.
3. Preserve prior established facts unless the user explicitly overrides them.

### list

1. List all files under `设定集/角色/`.
2. Return a concise roster with role or relationship hints when available.

### relation

1. Read the involved character files.
2. Update relationship wording consistently in the files and, if used, `state.json`.

### graph

1. Read available character files.
2. Generate a lightweight Mermaid relationship graph only if the user asks for it.

## Outputs

- updated files under `设定集/角色/`
- optional relationship summary
- optional Mermaid graph

## Notes

- Do not invent large cast bibles unless the user asks.
- Prefer updating the character file first; only touch `.mighty/state.json` when the project already uses character-state tracking there.
