---
name: novel-status
description: Show the current status of a Codex-managed novel project by reading `.mighty/state.json`, chapter files, and outline context, then summarizing progress, quality trend, active issues, and next-step guidance.
---

# Novel Status

Use this skill when the user wants a quick project overview, progress summary, quality trend, active foreshadowing status, or writing cadence snapshot.

## Inputs

- optional detail level: `summary` or `full`
- optional focus:
  - foreshadowing
  - timeline
  - stats
  - overdue items

## Preconditions

- `.mighty/state.json` exists
- project has at least some chapter or outline data

## Primary data sources

Always read:

- `.mighty/state.json`

Read conditionally:

- `chapters/` to count written chapters
- `大纲/总纲.md`
- `大纲/章纲/*.md`

## Workflow

1. Read `.mighty/state.json`.
2. Summarize:
   - title
   - genre
   - platform
   - current chapter
   - total words
3. Inspect:
   - `chapter_meta`
   - `chapter_snapshots`
   - `quality_metrics`
   - `plot_threads.foreshadowing`
   - `plot_threads.suspense`
4. If `summary` mode:
   - return a concise dashboard
5. If `full` mode:
   - expand with quality trend, foreshadowing buckets, and next risks
6. If the user asks for one focus area, prioritize that section and compress the rest.
7. End with the smallest useful next-step recommendation.

## Output conventions

- Prefer concise Markdown sections
- Use bullets for dashboards
- Use small tables only when comparing multiple status buckets

## Notes

- Prefer state-derived truth over stale prose summaries.
- If chapter count from files and state disagree, report the mismatch explicitly.
- If there is insufficient data for a requested statistic, say so directly instead of inferring.
