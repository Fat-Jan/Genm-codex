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

- `.mighty/active-context.json`
- `.mighty/state-archive.json`
- `.mighty/volume-summaries.json`
- `.mighty/learned-patterns.json`
- `.mighty/market-adjustments.json`
- `.mighty/setting-gate.json`
- `.mighty/index.json`
- `chapters/` to count written chapters
- `大纲/总纲.md`
- `大纲/章纲/*.md`

## Workflow

1. Read `.mighty/state.json`.
2. If `.mighty/state-archive.json` exists and the user asks for history/full mode, read it.
3. If `.mighty/volume-summaries.json` exists and the user asks for history/full mode, read it as the compressed archive view for old chapter ranges.
4. If `.mighty/active-context.json` exists and the user asks for full mode, risks, or next-step guidance, read it as the preferred current-writing sidecar.
5. If `.mighty/learned-patterns.json` or `.mighty/market-adjustments.json` exist and the user asks for full mode, risks, or next-step guidance, read them.
6. If `.mighty/setting-gate.json` exists and the user asks for full mode, risks, or next-step guidance, read it.
7. If `.mighty/index.json` exists and the user asks for stats/timeline/full mode, read it.
8. Summarize:
   - title
   - genre
   - platform
   - current chapter
   - total words
7. Inspect:
   - `chapter_meta`
   - `chapter_snapshots`
   - `quality_metrics`
   - `plot_threads.foreshadowing`
   - `plot_threads.suspense`
   - `main_quest`
   - `progress.milestones`
   - sidecar guidance summaries when present
   - current `recent_guardrails` and their expiry when present
   - active-context summary when present
   - gate status, blocking gaps, review items, and `minimal_next_action` when present
   - and when present, archived `chapter_meta` / `chapter_snapshots` coverage
9. Build the status sections that fit the request:
   - progress
   - quality
   - foreshadowing buckets / timeline
   - index stats when available
   - gate blockers when relevant
   - active risks
10. If `summary` mode:
   - return a concise dashboard
11. If `full` mode:
   - expand with quality trend, foreshadowing buckets, index-backed stats, active `recent_guardrails`, volume summaries coverage, and next risks
12. If the user asks for one focus area, prioritize that section and compress the rest.
13. End with the smallest useful next-step recommendation.
   - if `.mighty/setting-gate.json` is not `passed`, prefer the gate's `minimal_next_action` over generic writing advice

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
- setting gate

## Output conventions

- Prefer concise Markdown sections
- Use bullets for dashboards
- Use small tables only when comparing multiple status buckets
- Do not fabricate predictive timelines if the data is too sparse

## Notes

- Prefer state-derived truth over stale prose summaries.
- If chapter count from files and state disagree, report the mismatch explicitly.
- If `state` has been thinned, explain which chapters are still live in `state` and which are now only in `state-archive`.
- If `.mighty/volume-summaries.json` exists, explain when old detail is now served from volume summaries instead of live chapter rows.
- If there is insufficient data for a requested statistic, say so directly instead of inferring.
- Treat `index` as an accelerator and secondary source, not a replacement for `state`.
- Treat `.mighty/active-context.json` as the preferred current-writing sidecar when it exists.
- Treat sidecar files as the preferred place for learned / market guidance once they have been externalized.
- When `.mighty/learned-patterns.json` contains active `recent_guardrails`, surface them as short-lived next-chapter constraints instead of flattening them into generic style notes.
- If `.mighty/setting-gate.json` exists, treat it as the current write-readiness control point rather than inferring readiness from chapter count alone.
