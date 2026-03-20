---
name: novel-retrieve
description: Retrieve writing-ready reference context from a Codex-managed novel project by quickly pulling character, setting, item, location, foreshadowing, or chapter-summary information for immediate drafting use.
---

# Novel Retrieve

Use this skill when the user needs a fast, writing-oriented reference view rather than a broad project query.

## Inputs

- query text
- optional `type`
  - `character`
  - `location`
  - `item`
  - `faction`
  - `power`
  - `foreshadowing`
  - `chapter`
  - `event`
- optional `write-assist`

## Positioning

This skill is not a replacement for:

- `novel-query`
- `novel-character`
- `novel-setting`
- `novel-index`

Instead, it acts as a fast retrieval layer on top of them:

- for immediate writing support
- for compact reference cards
- for “remind me what X is” style requests

## Preconditions

- `.mighty/state.json` exists
- at least one of these exists:
  - `设定集/`
  - `.mighty/index.json`
  - `chapters/`

## Required reads

Always start with:

- `.mighty/state.json`

Use when present:

- `.mighty/index.json`

Read conditionally:

- `设定集/角色/*.md`
- `设定集/势力/*.md`
- `设定集/地点/*.md`
- `设定集/物品/*.md`
- `设定集/力量体系.md`
- `大纲/总纲.md`
- `大纲/章纲/*.md`
- `chapters/*.md` only when state and index are still insufficient

## Retrieval strategy

Use this priority order:

1. exact filename or direct entity match
2. alias / role match from state or file text
3. index-backed lookup
4. semantic fallback from state + setting files

## Workflow

1. Parse the user request into:
   - target subject
   - preferred type
   - whether the user wants a compact reference card or broader writing assistance
2. Read `.mighty/state.json`.
3. If `.mighty/index.json` exists and helps narrow chapter/entity references, read it.
4. Resolve by type when the user already gave one.
5. Otherwise infer the best target bucket:
   - character
   - setting / location / item / faction
   - power system
   - foreshadowing
   - chapter / event
6. Return the smallest useful retrieval view.

## Type guidance

### character

Return:

- identity
- core personality
- motivation
- relationship relevance
- any current-state note from `.mighty/state.json`

### location / faction / item

Return:

- what it is
- why it matters
- story relevance
- any current status if available

### power

Return:

- relevant realm / rule / breakthrough condition
- any project-specific current progress

### foreshadowing

Return:

- planted chapter
- current status
- expected payoff range
- why it matters now

### chapter / event

Return:

- summary
- key events
- mentioned entities
- continuity relevance

## Write-assist mode

If the user clearly wants writing assistance, end with a compact “写作提示” section such as:

- this character’s voice
- this location’s atmosphere
- this item’s usable constraints
- this foreshadowing’s best reminder point

Do not automatically write new prose unless the user explicitly asks.

## Output conventions

Prefer one of these:

- compact reference card
- bullet summary
- concise table only when multiple fields help

## Notes

- Prefer current state over stale prose if they conflict.
- If the request is really a broad project query, recommend `novel-query`.
- If the request is actually a file update, recommend `novel-character` or `novel-setting`.
