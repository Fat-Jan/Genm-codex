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
  - workflow
  - index

## Preconditions

- `.mighty/state.json` exists
- project has at least some chapter or outline data

## Primary data sources

Always read:

- `.mighty/state.json`

Read conditionally:

- `.mighty/active-context.json`
- `.mighty/quality-audit.json`
- `.mighty/knowledge-projection.json`
- `.mighty/workflow-health.json`
- `../../docs/10-进行中/batch-evidence-sidecar.json`
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
5. If `../../docs/10-进行中/batch-evidence-sidecar.json` exists and the user asks about cross-platform evidence status, profile readiness, ontology readiness, exception profiles, or batch evidence completion, read it as the preferred machine-readable evidence status sidecar.
6. If `.mighty/workflow-health.json` exists and the user asks for full mode, workflow-health, risks, or next-step guidance, read it as the preferred compact workflow health bundle.
7. If `.mighty/quality-audit.json` exists and the user asks for full mode, risks, or quality health, read it as the preferred audit summary for review/close artifact health.
8. If `.mighty/knowledge-projection.json` exists and the user asks for full mode, workflow health, or machine-readable project status, read it as the preferred compact projection.
9. If `.mighty/learned-patterns.json` or `.mighty/market-adjustments.json` exist and the user asks for full mode, risks, or next-step guidance, read them.
10. If `.mighty/setting-gate.json` exists and the user asks for full mode, risks, or next-step guidance, read it.
11. If `.mighty/index.json` exists and the user asks for stats/timeline/full mode, read it.
8. Summarize:
   - title
   - genre
   - platform
   - current chapter
   - total words
10. Inspect:
   - `chapter_meta`
   - `chapter_snapshots`
   - `quality_metrics`
   - `plot_threads.foreshadowing`
   - `plot_threads.suspense`
   - `main_quest`
   - `progress.milestones`
   - sidecar guidance summaries when present
   - quality-audit findings when present
   - knowledge-projection workflow / sidecar health summaries when present
   - workflow-health bundle summary when present
   - current `recent_guardrails` and their expiry when present
   - active-context summary when present
   - gate status, blocking gaps, review items, and `minimal_next_action` when present
   - and when present, archived `chapter_meta` / `chapter_snapshots` coverage
11. Build the status sections that fit the request:
   - progress
   - quality
   - foreshadowing buckets / timeline
   - index stats when available
   - gate blockers when relevant
   - active risks
12. If `summary` mode:
   - return a concise dashboard
13. If `full` mode:
   - expand with quality trend, foreshadowing buckets, index-backed stats, active `recent_guardrails`, volume summaries coverage, and next risks
14. If the user asks for one focus area, prioritize that section and compress the rest.
15. End with the smallest useful next-step recommendation.
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

### workflow

- when `.mighty/workflow-health.json` exists, prefer surfacing:
  - `quality_audit_status`
  - `top_finding_codes`
  - `workflow_truth_status`
  - `workflow_truth_missing_artifacts`
  - `repo_owned_tail_steps`
- when you need a compact human-facing block, mirror the section shape in `../../scripts/render_workflow_health_summary.py`
- when you need a full dashboard that also includes gate and current-writing slice, mirror `../../scripts/render_project_status_dashboard.py`
- when `.mighty/knowledge-projection.json` exists, prefer surfacing:
  - `workflow_contract.transaction_contract`
  - `workflow_contract.repo_owned_tail_steps`
  - `workflow_truth.status`
  - `workflow_truth.missing_artifacts`
- when `.mighty/quality-audit.json` exists, also surface:
  - `quality-audit.status`
  - top finding codes
- when `.mighty/market-data.json` or `.mighty/market-adjustments.json` exist and the user asks about市场/scan/trend, mirror `../../scripts/render_project_scan_summary.py`
- keep this section compact and operational, not architectural essay

### evidence

- when `../../docs/10-进行中/batch-evidence-sidecar.json` exists, prefer surfacing:
  - `summary.complete_count`
  - `summary.partial_count`
  - `summary.exception_count`
  - specific profile `status`
  - specific profile `ontology_ready`
  - specific profile `exception` / `exception_type`
- when the user asks whether a profile is “空挂”, explain whether:
  - the slug exists in `shared/profiles/*`
  - the evidence sidecar marks it `ontology_ready`
  - it is an explicit exception profile
- keep evidence answers compact and operational, not a long evidence-pack reprint

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
- workflow 健康
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
- Do not treat `active-context` as a second canon center for protagonist runtime state; it is only a narrow current-writing slice.
- Treat `.mighty/workflow-health.json` as the preferred compact workflow-health bundle when it exists.
- Treat `.mighty/quality-audit.json` as the preferred summary of review/close artifact health when it exists.
- Treat `.mighty/knowledge-projection.json` as the preferred compact machine-readable projection of workflow contract, sidecar health, and reviewed-chapter coverage when it exists.
- Treat `../../docs/10-进行中/batch-evidence-sidecar.json` as the preferred machine-readable source for cross-platform evidence status and exception profiles when it exists.
- Treat sidecar files as the preferred place for learned / market guidance once they have been externalized.
- When `.mighty/learned-patterns.json` contains active `recent_guardrails`, surface them as short-lived next-chapter constraints instead of flattening them into generic style notes.
- Keep `recent_guardrails` operational and short-lived; if they start looking like broad theory notes, treat that as a sidecar hygiene problem.
- If `.mighty/setting-gate.json` exists, treat it as the current write-readiness control point rather than inferring readiness from chapter count alone.
