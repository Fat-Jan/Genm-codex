---
name: novel-query
description: Query a Codex-managed novel project using natural language, lightweight structured requests, or common templates by reading `.mighty/state.json`, optionally `.mighty/index.json`, and related setting files, then returning concise facts, counts, lists, or tables.
---

# Novel Query

Use this skill when the user wants to inspect project state, list entities, count items, search indexed content, or ask natural-language questions about the current novel project.

## Inputs

- natural-language query
- template-like query request
- lightweight structured request such as:
  - `LIST ...`
  - `TABLE ...`
  - `COUNT ...`
  - `--template=<name>`

## Preconditions

- `.mighty/state.json` exists
- project has at least one initialized state or setting file

## Primary data sources

Always start with:

- `.mighty/state.json`

Use `.mighty/index.json` when it exists and the request benefits from indexed lookup:

- broad chapter search
- chapter summary lookup
- entity mention lookup
- index-backed project stats

Read conditionally when needed:

- `.mighty/active-context.json`
- `.mighty/workflow-health.json`
- `.mighty/quality-audit.json`
- `.mighty/knowledge-projection.json`
- `../../docs/10-进行中/batch-evidence-sidecar.json`
- `.mighty/import-report.json`
- `.mighty/state-archive.json`
- `.mighty/volume-summaries.json`
- `.mighty/learned-patterns.json`
- `.mighty/market-adjustments.json`
- `.mighty/setting-gate.json`
- `设定集/角色/*.md`
- `设定集/世界观/*.md`
- `设定集/力量体系.md`
- `大纲/总纲.md`
- `大纲/章纲/*.md`
- `chapters/*.md` only if neither state nor index has enough signal

## Supported query modes

### 1. Natural language

Examples:

- 主角现在什么境界
- 有哪些活跃伏笔
- 第001章之后主角状态怎么变了
- 项目现在进度怎么样
- setting gate 现在卡在哪
- 当前最小下一步动作是什么
- 第003章发生了什么
- 哪几章提到了后山东壁
- 现在有哪些活跃伏笔

### 2. Template-style requests

Use a fixed pattern when the user wants common summaries:

- active foreshadowing
- overdue foreshadowing
- character relations
- power progress
- location summary
- item inventory
- suspense check
- project stats
- index stats
- chapter summaries

### 3. Lightweight structured requests

Support a minimal subset of the old command’s structured syntax. Do not implement a full SQL parser.

Supported patterns:

- `LIST <field-or-subject>`
- `COUNT <subject>`
- `TABLE <field1, field2> FROM <subject>`
- optional simple filters expressed informally after the main subject

Examples:

- `LIST active foreshadowing`
- `COUNT chapters`
- `TABLE name, relationship FROM characters`
- `TABLE chapter, summary FROM chapters`

Map these requests onto state or index data rather than pretending to execute a real query language.

## Workflow

1. Parse the user query into:
   - target entity set
   - desired output type (`table`, `list`, `count`, or `summary`)
   - optional filters
2. Read `.mighty/state.json`.
3. If `.mighty/active-context.json` exists and the request asks about current writing context, near-term blockers, recent hooks, or next-step guidance, read it next.
4. If `.mighty/workflow-health.json` exists and the request asks about workflow-health, artifact truth, or next-step risk, read it next.
5. If `.mighty/quality-audit.json` exists and the request asks about quality artifact health, review drift, or workflow false positives, read it next.
6. If `../../docs/10-进行中/batch-evidence-sidecar.json` exists and the request asks about cross-platform evidence, profile readiness, exceptions, completion counts, or whether a profile is effectively wired vs 空挂, read it next.
7. If `.mighty/knowledge-projection.json` exists and the request asks about workflow contract, sidecar health, or compact project status, read it next.
8. If `.mighty/import-report.json` exists and the request asks about imported chapters, current import status, or next import handoff steps, read it next.
8. If `.mighty/index.json` exists and the request is chapter-heavy, mention-heavy, or stats-heavy, read it next.
9. If `.mighty/state-archive.json` exists and the request targets older chapters or full-history chapter metadata, read it next.
10. If `.mighty/volume-summaries.json` exists and the request targets old chapter ranges or compressed archive summaries, read it next.
11. If the request asks about learned style preferences, current market guidance, or project-side writing constraints, read:
   - `.mighty/learned-patterns.json`
   - `.mighty/market-adjustments.json`
12. If the request asks about write readiness, blockers, next actionable command, or `setting gate`, read:
   - `.mighty/setting-gate.json`
13. Resolve the request source:
   - active-context first for current writing slice / recent hooks / near-term watchpoints
   - do not treat active-context as a full protagonist-state truth source; if the answer needs live canon, fall back to `state`
   - workflow-health first for compact workflow truth / artifact health / repo-owned tail questions
   - quality-audit first for review artifact health / false-positive quality questions
   - evidence-sidecar first for cross-platform evidence status / exception / ontology-ready questions
   - knowledge-projection first for workflow contract / sidecar health / compact project summary questions
   - import-report first for imported chapter handoff state
   - state-first for current truth
   - state-archive for old chapter metadata / snapshot / summary history
   - volume summaries for compressed old chapter ranges when live rows are no longer available
   - sidecar-first for learned / market guidance
   - gate-first for current write-readiness blockers / `minimal_next_action`
   - index-first for chapter lookup / summary / mention search
14. If the answer is fully available from state, state-archive, sidecar, gate, or index, stop there.
15. Only read additional files if state, state-archive, sidecars, gate, and index all lack the needed detail.
16. Return the smallest useful result:
   - list for browsing
   - count for totals
   - short summary for direct questions
   - table only when multiple fields are explicitly helpful
   - for gate queries, prefer:
     - `status`
     - `blocking_gaps`
     - `review_items`
     - `minimal_next_action`

## Template guidance

Support these first:

- `active-foreshadowing`
- `overdue-foreshadowing`
- `character-relations`
- `power-progress`
- `location-summary`
- `item-inventory`
- `suspense-check`
- `project-stats`
- `workflow-health`
- `evidence-status`
- `index-stats`
- `chapter-summaries`

Suggested behaviors:

- `active-foreshadowing`: list active foreshadowing items with status or expected range
- `character-relations`: summarize protagonist + active character relations from state and character files
- `project-stats`: summarize current chapter, total words, active foreshadowing count, review coverage
- `workflow-health`: summarize `quality_audit_status`, `top_finding_codes`, `workflow_truth_status`, `workflow_truth_missing_artifacts`, and `repo_owned_tail_steps`
  - keep the terse answer shape aligned with `../../scripts/render_workflow_health_summary.py`
- `evidence-status`: summarize `complete_count`, `partial_count`, `exception_count`, and any requested profile’s `status / ontology_ready / exception`
- when the user asks for a more complete status dashboard or one-line operational summary, align with `../../scripts/render_project_status_dashboard.py`
- when the user asks about market scan / trend / current scan sidecars, align with `../../scripts/render_project_scan_summary.py`
- `setting-gate`: summarize gate status, blocking gaps, queued confirmations, and `minimal_next_action`
- `index-stats`: if index exists, report indexed chapters, total chars/lines, and chapter numbers
- `chapter-summaries`: use `summaries_index` first, fall back to index chapter summaries
  - if state has been thinned, check `state-archive.summaries_index` before falling back to index
- `volume-summaries`: use `.mighty/volume-summaries.json` to summarize archived chapter ranges when fine-grained rows have already been compressed
- `import-status`: summarize `.mighty/import-report.json`, imported chapter count, conflicts, and recommended next actions

## Index-aware query guidance

Use `.mighty/index.json` for:

- “哪些章节提到了 X”
- “列出已索引章节”
- “给我第1到3章摘要”
- “索引统计”

If the index is missing and the request clearly wants index-backed data, say so directly and recommend:

- `novel-index build`

## Output conventions

- Prefer concise Markdown
- Include field names when the result may be ambiguous
- If no result exists, say so directly and suggest the nearest alternative query
- When using index-backed data, mention that briefly so the user knows where the answer came from
- When using gate-backed data, mention that it came from `.mighty/setting-gate.json`
- When using active-context-backed data, mention that it came from `.mighty/active-context.json`
- When using workflow-health-backed data, mention that it came from `.mighty/workflow-health.json`
- When using quality-audit-backed data, mention that it came from `.mighty/quality-audit.json`
- When using knowledge-projection-backed data, mention that it came from `.mighty/knowledge-projection.json`
- When using evidence-sidecar-backed data, mention that it came from `docs/10-进行中/batch-evidence-sidecar.json`
- When using compressed archive data, mention that it came from `.mighty/volume-summaries.json`

## Notes

- Do not invent missing state.
- Prefer current state over stale prose files if they disagree.
- When `state` has been thinned, prefer:
  1. `.mighty/active-context.json` for current writing slice
  2. current `state` for live truth
  3. `state-archive` for old chapter metadata
  4. `.mighty/volume-summaries.json` for compressed old ranges
  5. `.mighty/workflow-health.json` for compact workflow truth / artifact health
  6. `.mighty/quality-audit.json` for review artifact health
  7. `../../docs/10-进行中/batch-evidence-sidecar.json` for cross-platform evidence status / exceptions / ontology-ready checks
  8. `.mighty/knowledge-projection.json` for workflow contract / sidecar health summaries
  9. sidecar files for learned / market guidance
  10. `index` for broad retrieval
- If the user asks for broad statistics, summarize first and only expand on request.
- Do not claim to support full Dataview/SQL syntax; keep the structured mode intentionally narrow.
- If `.mighty/setting-gate.json` exists, treat it as the source of truth for current write-readiness and next-action blockers.
