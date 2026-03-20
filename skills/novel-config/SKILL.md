---
name: novel-config
description: Inspect and guide local project or Codex configuration for a novel workspace by checking `.env`, optional project config, and Codex config files, then suggesting the smallest useful setup action.
---

# Novel Config

Use this skill when the user wants to inspect, explain, or lightly adjust local configuration related to a Codex-managed novel project.

## Positioning

This is a guided configuration assistant, not a full environment manager.

It should:

- inspect current local configuration
- explain what is missing or conflicting
- suggest the next local action
- write a small local config file only when the user explicitly asks

It should not:

- claim to manage external provider accounts
- pretend to validate live API connectivity on its own
- rewrite unrelated user environment settings without an explicit request

## Inputs

- optional operation:
  - `check`
  - `providers`
  - `validate`
  - `quick-setup`
  - `switch-provider`
- optional provider name

## Candidate config sources

Inspect what exists, in this order:

1. project `.env`
2. project `.mighty/config.json`
3. `~/.codex/config.toml`

Do not assume legacy `~/.claude/settings.json` is the primary config in the Codex-native path.

## Required reads

Always read what exists:

- `.env`
- `.mighty/config.json`
- `~/.codex/config.toml`

Read conditionally:

- `README.md`
- `docs/skill-usage.md`

## Workflow

### check

1. Inspect the available config files.
2. Report:
   - whether project `.env` exists
   - whether project `.mighty/config.json` exists
   - which model/provider settings currently exist in `~/.codex/config.toml`
3. Explain any obvious gaps or mismatches.

### providers

1. Return the locally relevant provider landscape:
   - what is already configured
   - what provider names are referenced in existing guidance
2. Keep the result practical and brief.

### validate

1. Validate local config presence and shape only.
2. If the user really wants connectivity validation, recommend `novel-test`.

### quick-setup / switch-provider

1. Treat these as guided actions.
2. Show the smallest required local changes first.
3. Only write files if the user explicitly asked for the change to be applied.

## Output conventions

Prefer:

- current config status
- detected gaps
- recommended next command

## Notes

- If the user wants connection testing, route to `novel-test`.
- Prefer not to create `.env` unless the user explicitly asks to write one.
- If no project-local config exists, say so directly instead of pretending defaults are project-specific.
