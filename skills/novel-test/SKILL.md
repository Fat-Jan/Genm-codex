---
name: novel-test
description: Inspect local provider configuration and guide a safe connection test flow for a Codex-managed novel workspace without pretending that live API validation already happened.
---

# Novel Test

Use this skill when the user wants to check whether provider configuration looks testable and what the next connectivity test step should be.

## Positioning

This is a guided connection-test assistant, not an automatic external API probe by default.

It should:

- inspect local provider configuration
- explain what can be tested
- prepare a safe next-step test plan
- interpret likely failure modes

It should not:

- claim a live API test succeeded unless one was actually run
- fake connectivity results

## Inputs

- optional provider name
- optional `all`
- optional `verbose`

## Required reads

Always read what exists:

- `.env`
- `~/.codex/config.toml`

Read conditionally:

- `.mighty/config.json`

## Workflow

1. Inspect local config presence.
2. Identify candidate provider settings and model info.
3. Determine whether the workspace has enough information for a real test:
   - provider name
   - base URL
   - auth pattern or token presence
4. Report one of:
   - ready for manual connectivity test
   - partially configured
   - missing required config
5. If the user wants a real test and the environment already exposes an obvious safe route, explain the exact next test command.
6. If not enough information exists, say what is missing.

## Output conventions

Prefer:

- detected provider(s)
- local readiness
- next recommended test action
- likely failure explanations

## Notes

- Prefer honesty over false success.
- If the user wants configuration help first, route to `novel-config`.
- If multiple providers are present, recommend the one with the clearest existing local config instead of making the user parse everything.
