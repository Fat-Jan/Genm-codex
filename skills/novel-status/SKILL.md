---
name: novel-status
description: Show the current status of a Codex-managed novel project by reading `.mighty/state.json`, optionally `.mighty/index.json`, chapter files, and outline context, then summarizing progress, quality trend, foreshadowing state, stats, and next-step guidance.
---

# Novel Status

Use this skill when the user wants a quick project overview, progress summary, quality trend, foreshadowing timeline view, index-backed stats, or next-step guidance.

## Inputs

- optional detail level: `summary` or `full`
- optional focus:
  - foreshadowing
  - timeline
  - stats
  - overdue items
  - quality
  - index

## Preconditions

- `.mighty/state.json` exists
- project has at least some chapter or outline data

## Primary data sources

Always read:

- `.mighty/state.json`

Read conditionally:

- `.mighty/state-archive.json`
- `.mighty/learned-patterns.json`
- `.mighty/market-adjustments.json`
- `.mighty/index.json`
- `chapters/` to count written chapters
- `大纲/总纲.md`
- `大纲/章纲/*.md`

## Workflow

1. Read `.mighty/state.json`.
2. If `.mighty/state-archive.json` exists and the user asks for history/full mode, read it.
3. If `.mighty/learned-patterns.json` or `.mighty/market-adjustments.json` exist and the user asks for full mode, risks, or next-step guidance, read them.
4. If `.mighty/index.json` exists and the user asks for stats/timeline/full mode, read it.
4. Summarize:
   - title
   - genre
   - platform
   - current chapter
   - total words
5. Inspect:
   - `chapter_meta`
   - `chapter_snapshots`
   - `quality_metrics`
   - `plot_threads.foreshadowing`
   - `plot_threads.suspense`
   - `main_quest`
   - `progress.milestones`
   - sidecar guidance summaries when present
   - and when present, archived `chapter_meta` / `chapter_snapshots` coverage
6. Build the status sections that fit the request:
   - progress
   - quality
   - foreshadowing buckets / timeline
   - index stats when available
   - active risks
6. If `summary` mode:
   - return a concise dashboard
7. If `full` mode:
   - expand with quality trend, foreshadowing buckets, index-backed stats, and next risks
8. If the user asks for one focus area, prioritize that section and compress the rest.
9. End with the smallest useful next-step recommendation.

## Focus guidance

### foreshadowing / timeline

- summarize:
  - active
  - pending
  - warning
  - overdue
  - resolved
- when possible, point out the nearest recovery / payoff pressure

### stats

- use `state` for project-truth metrics
- use `index` for indexed chapter count, chars, lines, and chapter coverage
- explicitly report mismatches instead of hiding them

### quality

- summarize:
  - recent scores
  - average score
  - trend
  - dimension scores
- if review coverage is sparse, say so directly

### overdue items

- focus on:
  - overdue foreshadowing
  - warning bucket
  - mismatches between current chapter and unresolved hooks

## Enhanced output expectations

For `full` or stats-heavy requests, prefer sections such as:

- 基本信息
- 进度概览
- 质量状态
- 伏笔状态 / 时间线
- 索引统计
- 风险与建议

## Output conventions

- Prefer concise Markdown sections
- Use bullets for dashboards
- Use small tables only when comparing multiple status buckets
- Do not fabricate predictive timelines if the data is too sparse

## Notes

- Prefer state-derived truth over stale prose summaries.
- If chapter count from files and state disagree, report the mismatch explicitly.
- If `state` has been thinned, explain which chapters are still live in `state` and which are now only in `state-archive`.
- If there is insufficient data for a requested statistic, say so directly instead of inferring.
- Treat `index` as an accelerator and secondary source, not a replacement for `state`.
- Treat sidecar files as the preferred place for learned / market guidance once they have been externalized.
