---
name: novel-query
description: Query a Codex-managed novel project using natural language or simple structured filters by reading `.mighty/state.json` and related setting files, then returning concise project facts, lists, counts, or summaries.
---

# Novel Query

Use this skill when the user wants to inspect project state, list entities, count items, or ask natural-language questions about the current novel project.

## Inputs

- natural-language query
- or template-like query request

## Preconditions

- `.mighty/state.json` exists
- project has at least one initialized state or setting file

## Primary data sources

Always start with:

- `.mighty/state.json`

Read conditionally when needed:

- `设定集/角色/*.md`
- `设定集/世界观/*.md`
- `设定集/力量体系.md`
- `大纲/总纲.md`
- `大纲/章纲/*.md`

## Supported query modes

### 1. Natural language

Examples:

- 主角现在什么境界
- 有哪些活跃伏笔
- 第001章之后主角状态怎么变了
- 项目现在进度怎么样

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

## Workflow

1. Parse the user query into:
   - target entity set
   - desired output type (`table`, `list`, `count`, or `summary`)
   - optional filters
2. Read `.mighty/state.json`.
3. If the answer is fully available from state, stop there.
4. Only read additional files if state lacks the needed detail.
5. Return the smallest useful result:
   - list for browsing
   - count for totals
   - short summary for direct questions
   - table only when multiple fields are explicitly helpful

## Output conventions

- Prefer concise Markdown
- Include field names when the result may be ambiguous
- If no result exists, say so directly and suggest the nearest alternative query

## Notes

- Do not invent missing state.
- Prefer current state over stale prose files if they disagree.
- If the user asks for broad statistics, summarize first and only expand on request.
