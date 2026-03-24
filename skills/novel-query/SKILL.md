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

- `.mighty/state-archive.json`
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
3. If `.mighty/index.json` exists and the request is chapter-heavy, mention-heavy, or stats-heavy, read it next.
4. If `.mighty/state-archive.json` exists and the request targets older chapters or full-history chapter metadata, read it next.
5. If the request asks about learned style preferences, current market guidance, or project-side writing constraints, read:
   - `.mighty/learned-patterns.json`
   - `.mighty/market-adjustments.json`
6. If the request asks about write readiness, blockers, next actionable command, or `setting gate`, read:
   - `.mighty/setting-gate.json`
7. Resolve the request source:
   - state-first for current truth
   - state-archive for old chapter metadata / snapshot / summary history
   - sidecar-first for learned / market guidance
   - gate-first for current write-readiness blockers / `minimal_next_action`
   - index-first for chapter lookup / summary / mention search
8. If the answer is fully available from state, state-archive, sidecar, gate, or index, stop there.
9. Only read additional files if state, state-archive, sidecars, gate, and index all lack the needed detail.
10. Return the smallest useful result:
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
- `index-stats`
- `chapter-summaries`

Suggested behaviors:

- `active-foreshadowing`: list active foreshadowing items with status or expected range
- `character-relations`: summarize protagonist + active character relations from state and character files
- `project-stats`: summarize current chapter, total words, active foreshadowing count, review coverage
- `setting-gate`: summarize gate status, blocking gaps, queued confirmations, and `minimal_next_action`
- `index-stats`: if index exists, report indexed chapters, total chars/lines, and chapter numbers
- `chapter-summaries`: use `summaries_index` first, fall back to index chapter summaries
  - if state has been thinned, check `state-archive.summaries_index` before falling back to index

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

## Notes

- Do not invent missing state.
- Prefer current state over stale prose files if they disagree.
- When `state` has been thinned, prefer:
  1. current `state` for live truth
  2. `state-archive` for old chapter metadata
  3. sidecar files for learned / market guidance
  4. `index` for broad retrieval
- If the user asks for broad statistics, summarize first and only expand on request.
- Do not claim to support full Dataview/SQL syntax; keep the structured mode intentionally narrow.
- If `.mighty/setting-gate.json` exists, treat it as the source of truth for current write-readiness and next-action blockers.
