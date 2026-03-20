---
name: novel-log
description: Inspect a Codex-managed novel project's lightweight trace log by tailing, searching, or summarizing `.mighty/logs/trace.jsonl`, and clearly report when logging has not been initialized.
---

# Novel Log

Use this skill when the user wants to inspect recent trace events, search log entries, or summarize log activity for a Codex-managed novel project.

## Inputs

- operation:
  - `tail`
  - `search`
  - `stats`
  - `init-check`
- optional line count for `tail`
- optional keyword for `search`

## Preconditions

- `.mighty/` exists

## Log location

- primary log file: `.mighty/logs/trace.jsonl`
- optional archive file: `.mighty/logs/trace.jsonl.archive`

## First-version scope

This version is intentionally light:

- inspect existing logs
- report absence cleanly
- summarize log activity

Do not build a full logging subsystem here.

## Required reads

Always read only what exists:

- `.mighty/logs/trace.jsonl`
- `.mighty/logs/trace.jsonl.archive`

## Expected log shape

Treat each line as a JSON object with fields like:

- `ts`
- `event`
- `session_id`
- `skill`
- `bee`
- `result`
- `error`

If lines are malformed, skip bad lines and report that partial parsing was required.

## Workflow

### init-check

1. Check whether `.mighty/logs/trace.jsonl` exists.
2. Report:
   - exists or missing
   - whether archive exists
   - recommended next step

### tail

1. Check whether `.mighty/logs/trace.jsonl` exists.
2. If missing, say logging is not initialized and stop.
3. Read the last `N` lines, defaulting to a small number such as `20`.
4. Parse each line as JSON when possible.
5. Return a concise table or bullet list with:
   - time
   - event
   - key detail

### search

1. Check whether `.mighty/logs/trace.jsonl` exists.
2. If missing, say logging is not initialized and stop.
3. Search for the keyword in:
   - raw lines
   - parsed `event`
   - parsed `skill`
   - parsed `bee`
   - parsed `error`
4. Return matching entries with the smallest useful context.

### stats

1. Check whether `.mighty/logs/trace.jsonl` exists.
2. If missing, say logging is not initialized and stop.
3. Parse the file conservatively.
4. Summarize:
   - total record count
   - event counts
   - skill counts when present
   - error count when present
   - earliest and latest timestamps if readable

## Output conventions

### tail

- recent entry list
- avoid dumping full raw JSON unless the user asks

### search

- keyword searched
- match count
- matching entry summary

### stats

- concise dashboard
- event buckets
- notable errors if any

## Notes

- This version is read-only.
- If the log file does not exist, do not create it automatically; just say logging has not been initialized.
- If the log exists but is empty, report that directly instead of pretending there is activity.
