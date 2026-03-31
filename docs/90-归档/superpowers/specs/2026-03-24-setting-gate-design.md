# Setting Gate Design

Date: 2026-03-24

## Goal

Introduce one unified setting-enrichment and pre-write gating layer so Codex-managed novel projects stop depending on implicit model memory for canon-critical facts.

The design must solve two problems together:

- `设定集/` is too sparse after project initialization and early writing
- writing can proceed before the project has enough explicit setting truth, which increases omission, drift, and hallucination risk

The target behavior is:

- create more project-local setting assets earlier
- block writing when story-dependent setting support is still incomplete
- use local project truth first
- escalate to MCP-backed research only for hard local gaps
- push stable post-write facts back into `设定集/`

## Problem

Current workflow pieces are individually useful:

- `novel-init`
- `novel-outline`
- `novel-write`
- `novel-sync`
- `scripts/project-maintenance.py`
- `novel-scan`

But they do not yet form one explicit setting-closure loop.

This creates a repeated failure pattern:

1. `novel-init` creates only a thin starter layer
2. `novel-outline` can finish while setting coverage is still shallow
3. `novel-write` reads `state` and a few local files, but the project may still lack durable cards for important people, places, factions, items, and rules
4. some truth is remembered only implicitly from recent context
5. later chapters drift, omit earlier facts, or invent missing glue
6. `novel-sync` can help only after writing has already moved forward

That is the wrong default for long-form work. The project should convert story dependencies into explicit assets before prose generation is allowed to continue.

## Design Summary

Add one unified setting gate with one policy source and one execution script:

- policy: `docs/setting-gate-policy.json`
- executor: `scripts/setting-gate.py`

This gate becomes the canonical coordinator for four workflow hooks:

1. `novel-init`
2. `novel-outline`
3. `novel-write`
4. `post-task-maintenance -> project-maintenance -> sync-setting-assets`

The desired loop is:

`init -> outline -> setting gate -> review/confirm -> write -> maintenance/sync -> setting assets`

The gate enforces five rules:

1. aggressive local-first card creation is allowed
2. writing cannot begin until the gate passes
3. `outline` completion triggers a hard coverage gate
4. MCP is only used for local hard gaps
5. MCP results never become canon without structured risk handling

## Scope

### In scope

- one shared setting gate policy
- aggressive setting skeleton creation during init
- outline-stage setting coverage audit as a hard gate
- automatic local-first card creation from project context
- selective MCP escalation for hard local gaps
- model-first self-review and risk grading
- user confirmation only for high-risk items
- post-write automatic maintenance and setting sync
- explicit machine-readable gate state

### Out of scope

- full autonomous worldbuilding without project anchors
- global MCP scans for every project by default
- direct MCP-to-canon writes
- replacing `state` as runtime truth
- full historical cleanup of every existing sparse project in v1
- broad NLP redesign beyond the current sync-oriented heuristics

## Core Model

The design depends on three fixed principles:

1. `.mighty/state.json` remains the runtime truth source
2. `设定集/` is the long-lived asset layer
3. prose generation must pass through `setting gate`

This prevents a parallel truth system:

- runtime and recency stay in `state`
- durable cards live under `设定集/`
- gating and review state live under `.mighty/`

## Single Sources of Truth

### Policy

Add one machine-readable policy file:

- `docs/setting-gate-policy.json`

It should define:

- coverage requirements by route type
- hard-block gap classes
- which asset types can be aggressively auto-created
- MCP escalation triggers
- risk grading thresholds
- which item classes require user confirmation

### Execution state

Add one gate state file:

- `.mighty/setting-gate.json`

Recommended minimum shape:

```json
{
  "version": "1.0",
  "status": "blocked",
  "checked_after": "outline",
  "blocking_gaps": [],
  "auto_created_files": [],
  "review_queue_count": 0,
  "mcp_used": false,
  "mcp_sources": []
}
```

### Review queue

Reuse and extend:

- `.mighty/sync-review.json`

Add fields so it can carry gate-produced review tasks, not only sync ambiguities:

- `source_stage`
- `confidence`
- `requires_user_confirmation`
- `candidate_files`
- `blocking`

## Architecture

### Unit 1: Init Bootstrap Layer

**Execution point:** `novel-init`

**Purpose:** Create more than a thin starter pair so a new project begins with usable setting scaffolds.

**Behavior**

- still create the current required starter files
- additionally create aggressive project-local skeletons derived from:
  - `title`
  - `genre`
  - resolved profile
  - initial total-outline scaffold
  - protagonist state

**Expected asset classes**

- protagonist card
- core supporting role skeletons
- key location skeletons
- key faction skeletons
- key item skeletons when premise-critical
- route-specific rule skeletons
- existing ancient-family-power truth sheets remain mandatory where relevant

**Important boundary**

These are starter cards, not confirmed canon expansions. They should be marked as generated scaffolds with clear source tags.

### Unit 2: Outline Coverage Hard Gate

**Execution point:** `novel-outline`

**Purpose:** Convert outline dependencies into explicit setting support before writing starts.

**Trigger**

Run automatically after a real total-outline completion and after material chapter-outline generation for the opening phase.

**Inputs**

- `大纲/总纲.md`
- relevant `大纲/章纲/*.md`
- `.mighty/state.json`
- existing `设定集/`
- gate policy

**Checks**

- which core roles now act as real plot drivers but still lack cards
- which locations, factions, and items appear as repeated story anchors but still lack cards
- which rules are required by the premise or early-chapter mechanics but exist only as implied prose
- whether ancient kinship / office truth requirements are satisfied
- whether real-world route dependencies require stable local references

**Hard-block rule**

If high-risk coverage gaps remain after automatic local-first enrichment, the project cannot proceed to `novel-write`.

### Unit 3: Local-First Enrichment Engine

**Execution point:** `scripts/setting-gate.py`

**Purpose:** Auto-create as many project-local assets as possible before any MCP escalation.

**Local sources in priority order**

1. `.mighty/state.json`
2. `大纲/总纲.md`
3. `大纲/章纲/*.md`
4. existing `设定集/`
5. recent `chapters/*.md` when available

**Behavior**

- aggressively create missing setting cards from local project truth
- prefer thin, useful cards over perfect encyclopedic cards
- preserve existing human-authored sections
- write generated sections in replaceable blocks

**Asset output targets**

- `设定集/角色/`
- `设定集/地点/`
- `设定集/势力/`
- `设定集/物品/`
- `设定集/世界观/`
- `设定集/力量体系.md`
- existing truth-sheet directories where applicable

### Unit 4: MCP Escalation for Hard Local Gaps

**Execution point:** `scripts/setting-gate.py`, with `novel-scan`/fetch-backed support

**Purpose:** Fill only the setting gaps that cannot be resolved from local project truth.

**Default mode**

`local-first`

**MCP trigger policy**

Escalate only when all three are true:

1. the gap is still blocking after local-first enrichment
2. the gap type is marked MCP-eligible in policy
3. the missing truth is not safely derivable from local project canon

**Typical MCP-eligible gaps**

- legal / labor / financial / medical / school-system reality constraints
- ancient office / rite / marriage / household truth when local references are insufficient
- specialized procedural or institutional rule support

**Non-goal**

Do not perform a broad MCP pre-scan for every project. This is selective escalation only.

### Unit 5: Risk Grading and Review Closure

**Execution point:** `scripts/setting-gate.py`

**Purpose:** Avoid either extreme:

- blindly writing every generated card straight into canon
- forcing the user to manually confirm every low-risk asset

**Grading model**

- low risk
  - directly materialize
- medium risk
  - materialize only as reviewed/generated candidate and queue for review
- high risk
  - queue for review
  - mark `requires_user_confirmation=true`
  - keep gate blocked

**High-risk classes by default**

- MCP-derived new facts
- rules that change causality or resource logic
- legal / medical / financial / institutional truths
- office / rite / kinship truths with downstream canon impact
- character cards that materially change identity, motive, or relation structure

### Unit 6: Write Gate Enforcement

**Execution point:** `novel-write`

**Purpose:** Make the setting gate an actual workflow control point instead of a suggestion.

**Behavior**

- before drafting, check `.mighty/setting-gate.json`
- if status is not `passed`, stop before writing
- return:
  - blocking gaps
  - queued confirmations
  - minimal next action

`novel-write` should not bypass this gate just because recent chapter context exists.

### Unit 7: Post-Write Setting Closure

**Execution point:** `scripts/post-task-maintenance.py -> scripts/project-maintenance.py -> scripts/sync-setting-assets.py`

**Purpose:** Push stable new facts from recent writing back into durable setting assets.

**Behavior**

- run by default after a real writing round
- sync stable entities from recent chapters and runtime state
- preserve human-authored content
- update only generated blocks when cards already exist
- queue ambiguous entities instead of dropping them silently

This is the back half of the loop. It ensures the project gets more explicit after writing, not less.

## End-to-End Flow

### Init path

1. `novel-init` builds canonical project structure
2. starter assets are created aggressively, not minimally
3. `setting gate(init)` writes initial gate state
4. unresolved high-risk gaps are queued early

### Outline path

1. `novel-outline` creates or updates total/chapter outline
2. `setting gate(outline)` runs automatically
3. local-first enrichment creates missing cards
4. MCP is invoked only for hard local gaps
5. risk grading runs
6. if high-risk blocking gaps remain, gate stays blocked and writing cannot begin

### Write path

1. `novel-write` checks gate status
2. if gate passed, drafting proceeds
3. after write success, maintenance hook runs automatically
4. stable entities are synced back into `设定集/`
5. review queue is refreshed

## Hard-Block Conditions

Gate should block writing for at least these classes:

- outline depends on a rule set that has no stable local support card
- repeated core role lacks a role card
- repeated critical place / faction / item lacks a card
- ancient kinship or office truth is missing
- MCP introduced a high-risk fact that has not been confirmed
- a newly generated high-risk card conflicts with existing canon

## Auto-Creation Policy

The v1 system should be aggressive, but not reckless.

### Allowed aggressive creation

- thin skeleton cards for repeated story anchors
- lightweight world-rule notes when the premise depends on them
- project-local placeholders with explicit generated markers
- route-specific truth scaffolds

### Forbidden automatic behavior

- converting every named mention into a durable card
- direct MCP-to-canon writes
- overwriting confirmed human-authored facts
- unblocking writing without clearing high-risk review items

## Source Tagging

Every generated card or generated section should carry a source tag such as:

- `init-bootstrap`
- `outline-gate-local`
- `write-sync-local`
- `gate-mcp-candidate`

This is necessary for:

- future refreshes
- trust debugging
- reviewing whether a fact came from local canon or MCP-backed research

## File Changes

### New files

- `docs/setting-gate-policy.json`
- `scripts/setting-gate.py`
- optional `.mighty/setting-gate.json` generated at runtime

### Modified files

- `skills/novel-init/SKILL.md`
- `skills/novel-outline/SKILL.md`
- `skills/novel-write/SKILL.md`
- `skills/novel-sync/SKILL.md`
- `skills/novel-scan/SKILL.md`
- `scripts/sync-setting-assets.py`
- `scripts/project-maintenance.py`
- `scripts/post-task-maintenance.py`
- `docs/00-当前有效/start-here.md`
- `docs/00-当前有效/default-workflows.md`
- `docs/00-当前有效/skill-usage.md`

## Rollout Order

1. add `docs/setting-gate-policy.json`
2. implement `scripts/setting-gate.py`
3. wire the hard gate into `novel-outline`
4. extend `novel-init` with aggressive starter-card creation
5. enforce gate checking in `novel-write`
6. extend post-write maintenance and sync contracts
7. align `novel-scan` with MCP-as-candidate, not MCP-as-canon
8. update workflow documentation

## Verification Strategy

Use the two currently sparse early-stage projects as primary smoke targets:

- `projects/公司裁我那天，系统先赔了我一百万`
- `projects/转学第一天，我把校草认成了新来的代课老师`

The first validation goals are:

1. after outline, the gate detects coverage gaps instead of allowing blind writing
2. automatic local-first enrichment creates visibly richer `设定集/`
3. MCP is only requested for true local hard gaps
4. high-risk gaps block writing until review is complete
5. post-write maintenance grows setting assets rather than leaving them static

## Risks

- aggressive creation can still overproduce noisy cards if the heuristics are too loose
- hard-gate behavior can feel heavy if review queue design is poor
- MCP-derived candidate handling can become confusing if source tags are inconsistent
- existing projects may surface many historical gaps on first adoption

These risks are acceptable because the current failure mode is worse: silent drift and hallucinated glue.

## Open Decisions Already Locked

The design intentionally locks these choices:

- aggressive enrichment instead of conservative enrichment
- local-first before MCP
- MCP only for hard local gaps
- outline-stage setting coverage as a hard gate
- model-first self-review with user confirmation only for high-risk items

These should not be reopened during implementation unless the first smoke run shows a concrete failure mode.
