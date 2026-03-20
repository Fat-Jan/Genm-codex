---
name: novel-index
description: Build, update, query, and summarize a lightweight index for a Codex-managed novel project by scanning chapter files and state, then storing the result in `.mighty/index.json`.
---

# Novel Index

Use this skill when the user wants faster project lookup, lightweight entity tracking, or a generated index over written chapters.

## Inputs

- operation:
  - `build`
  - `update`
  - `query`
  - `stats`
- optional chapter number for `update`
- optional keyword and type filter for `query`

## Preconditions

- `.mighty/state.json` exists
- `chapters/` exists

## Index location

- `.mighty/index.json`

## Required reads

Always read:

- `.mighty/state.json`
- `chapters/*.md`

Read conditionally:

- `大纲/章纲/*.md`
- `设定集/角色/*.md`
- `设定集/地点/*.md`
- `设定集/物品/*.md`

## First-version scope

The first version should stay lightweight and deterministic:

- build a chapter index
- reuse `chapter_meta` and `summaries_index` when available
- extract obvious entities from state and chapter text
- support simple keyword query over indexed summaries/entities
- provide useful stats

Do not try to build a perfect NLP entity extractor in version one.

## Recommended index shape

Keep `.mighty/index.json` compact and readable. Include at minimum:

```json
{
  "version": "1.0",
  "built_at": "<timestamp>",
  "chapters": {
    "1": {
      "file": "chapters/第001章.md",
      "word_count": 3152,
      "summary": "章节摘要",
      "entities": {
        "characters": ["沈照", "周通"],
        "locations": ["后山废井"],
        "items": ["残缺古镜"]
      },
      "key_events": ["古镜苏醒"]
    }
  },
  "entities": {
    "characters": {},
    "locations": {},
    "items": {}
  },
  "foreshadowing_index": {},
  "stats": {
    "total_chapters": 3,
    "total_words": 9152
  }
}
```

## Workflow

### build

1. Read `.mighty/state.json`.
2. Scan written chapter files under `chapters/`.
3. For each chapter:
   - read file path and text
   - use `chapter_meta` and `summaries_index` when present
   - gather obvious entity mentions from:
     - protagonist / active characters in state
     - important locations / tracked items in state
     - direct text mentions when easy to identify
4. Build:
   - `chapters`
   - lightweight `entities`
   - `foreshadowing_index` from current state
   - `stats`
5. Save to `.mighty/index.json`.

### update

1. If a chapter is provided, refresh only that chapter entry.
2. Otherwise refresh the latest written chapter from state.
3. Update aggregate entity mentions and stats conservatively.
4. Save back to `.mighty/index.json`.

### query

1. Read `.mighty/index.json`.
2. Search by keyword.
3. Optional type filters:
   - `character`
   - `location`
   - `item`
   - `chapter`
   - `foreshadowing`
4. Return the smallest useful result:
   - matching entity summary
   - matching chapters
   - related summaries

### stats

1. Read `.mighty/index.json`.
2. Report:
   - indexed chapter count
   - total indexed words
   - entity counts
   - most-mentioned entities when available
   - foreshadowing status counts when available

## Output conventions

### build / update

- index path
- indexed chapter count
- whether build was full or incremental
- top-level stats summary

### query

- matched type
- matched entries
- relevant chapter references when available

### stats

- concise dashboard
- avoid large tables unless they help

## Notes

- Prefer state-derived truth over unreliable free-text extraction.
- If no index exists for `query` or `stats`, recommend `build` first.
- Do not overwrite `.mighty/state.json` here.
- Keep this index lightweight enough that `query` and `status` can use it later, but do not force them to depend on it yet.
