# Strong Quality Gates Design

Date: 2026-03-23

## Goal

Introduce a strong-gating quality model for Codex-managed novel projects so the default workflow can block clearly unsafe writing progress instead of only reporting issues after the fact.

The design must address two failure classes in one unified system:

- draft-quality failures
  - chapter shrinkage
  - typo / malformed prose clusters
  - outline-like compression
  - obvious character-voice drift
- source-of-truth failures
  - era-inappropriate clothing / objects / decor
  - kinship / marriage / office-title truth errors
  - missing setting support that the model would otherwise hallucinate
  - garbage entity extraction polluting `设定集/`

## Problem

The current workflow already has useful evaluators:

- `novel-write`
- `novel-close`
- `novel-review`
- `novel-precheck`
- `novel-sync`

But the system still has three gaps:

1. Writing can begin even when the required setting truth is missing.
2. A chapter can be written and converged even when hard quality risks should have blocked it earlier.
3. `state -> 设定集` sync can materialize low-confidence garbage entities into long-lived setting files.

This creates a predictable failure pattern:

- the model assumes the setting is sufficient
- fills missing truth by invention
- writes short or brittle chapters
- review reports some issues
- but the project still accumulates low-trust prose and low-trust setting assets

That is the wrong system behavior for long-form novel production.

## Design Summary

Add one unified strong-gate layer with a single rule source and three execution points:

1. pre-write source gate inside `novel-write`
2. post-write hard gate inside `novel-close` before a chapter can be considered converged
3. sync-pollution gate inside `novel-sync` / `scripts/sync-setting-assets.py`

The system should not create a separate parallel skill such as `novel-quality-gate`.

Instead, the gate becomes a first-class constraint inside the existing default workflow:

`outline -> write -> close/review -> sync`

## Scope

### In scope

- one shared gate policy for all three enforcement points
- hard-block behavior for missing source truth before writing
- hard-block behavior for objective chapter-quality failures after writing
- conservative detection and queueing of low-confidence sync entities
- minimal state persistence for post-write gate results
- compatibility with current `novel-review` / `novel-fix` / `novel-rewrite` routing

### Out of scope

- building a perfect typo detector
- replacing human editorial judgment
- automatic external research for every chapter by default
- broad NLP entity extraction redesign
- automatic cleanup of all existing polluted setting files in the first version
- creating a new workflow engine or new top-level quality database

## Single Source of Truth

Add one machine-readable policy file under `docs/`:

- `docs/strong-quality-gate-policy.json`

This file should hold only the hard-gate rules that must be reused by implementation points, for example:

- bucket-aware word-count hard minimums
- bucket-aware soft warning ranges
- shrinkage detection thresholds
- required truth-sheet mappings for ancient-family-power and office-hierarchy routes
- typo / repetition / malformed-entity conservative blocker thresholds
- sync candidate rejection patterns

Human explanation can live in a companion document if useful, but implementation logic must resolve from the JSON policy, not from duplicated prose in multiple skills.

## Architecture

### Unit 1: Pre-Write Source Gate

**Execution point:** `novel-write`

**Purpose:** Block chapter drafting when the chapter depends on truth that has not been materialized in `设定集/` or equivalent project-local rule files.

**Inputs**

- target chapter outline
- current `.mighty/state.json`
- relevant `设定集/` files
- gate policy

**Checks**

- does the target outline use ancient kinship / household status terms that require:
  - `设定集/家族/宅门真值表.md`
  - `设定集/家族/小型家谱.md`
- does the route use office hierarchy terms that require:
  - `设定集/官制/官职真值表.md`
  - `设定集/官制/权力层级图.md`
- does the chapter rely on explicit era-sensitive objects, clothing, decor, rites, or household rules that currently have no local source file
- does the route rely on a world rule that exists only as implied prose and not as a stable setting note

**Hard-block rule**

Block `novel-write` when a required truth source is missing for a term or mechanic that the outline clearly depends on.

**Response shape**

Return a blocking report with:

- `gate_status = blocked`
- failed checks
- missing files or truth sources
- minimal next action:
  - `novel-setting`
  - `novel-character`
  - `novel-scan` when external research is explicitly needed

**Non-goal**

Do not auto-generate missing truth blindly just to satisfy the gate.

### Unit 2: Post-Write Hard Gate

**Execution point:** `novel-close`

**Purpose:** Prevent a written chapter from being treated as converged when objective production-quality failures remain.

**Inputs**

- target chapter text
- `chapter_meta`
- current bucket / platform context
- recent chapter window when shrinkage comparison is needed
- gate policy

**Checks**

- chapter word count below active bucket `hard_min`
- chapter word count below `soft_min` and abnormally lower than the recent local baseline
- repeated shrinkage pattern across a recent multi-chapter window
- high-confidence typo / malformed prose clusters
- high-confidence repetitive filler clusters
- obvious OOC or voice drift when the contradiction is directly supportable from local cards / recent chapter context
- high-confidence era / canon violations that can be tied to project-local truth sources

**Hard-block rule**

The gate should block close success only for objective or high-confidence failures.

That means:

- block for hard word-count failure
- block for repeated shrinkage backed by recent-chapter stats
- block for directly supportable canon / truth-sheet violation
- block for high-confidence malformed-text clusters
- do not block on vague “maybe weak style” judgments

**Routing behavior**

When blocked:

- `novel-close` cannot report the chapter as closed for this pass
- the result must route to:
  - `novel-fix` for bounded repair
  - `novel-rewrite` for structural failure
- `novel-polish` may still be a follow-up route, but cannot override a hard-block failure

### Unit 3: Sync-Pollution Gate

**Execution point:** `novel-sync` and `scripts/sync-setting-assets.py`

**Purpose:** Stop low-confidence extraction from turning runtime noise into long-lived setting canon.

**Inputs**

- recent chapter texts
- `state`
- sync overrides
- gate policy

**Checks**

- candidate looks like a phrase fragment instead of a stable entity
- candidate is an object / garment / location phrase being misclassified as a character
- candidate is too low-confidence to materialize safely
- candidate is repetitive noise that should go to review queue instead

**Hard-block rule**

Low-confidence or rejected candidates must not be written into `设定集/`.

They should go to `.mighty/sync-review.json` with:

- name
- kind
- reason
- chapter window

**Examples this gate must catch**

- `张纸`
- `白褙子`
- `花厅里`
- `危险`

## Data Flow

### Write flow

1. `novel-write` loads policy.
2. `novel-write` runs pre-write source gate.
3. If blocked:
   - stop before drafting
   - report missing truth sources
4. If passed:
   - continue normal writing

### Close flow

1. chapter draft exists
2. `novel-close` loads policy
3. `novel-close` runs post-write hard gate before final close success
4. if blocked:
   - route to `novel-fix` or `novel-rewrite`
   - never report convergence success
5. if passed:
   - continue existing review-first bounded close logic

### Sync flow

1. sync gathers candidate entities
2. sync applies candidate rejection rules
3. high-confidence stable entities materialize to `设定集/`
4. low-confidence candidates move to `sync-review`

## State Design

Do not create a new top-level quality center.

Persist only minimal post-write gate results under `chapter_meta[N]` when a chapter file exists:

- `quality_gate_status`
- `quality_gate_time`
- `quality_gate_failed_checks`

Optional:

- `quality_gate_word_count_baseline`
- `quality_gate_blocking_route`

Pre-write gate failures do not need a new persistent store in v1. Reporting in the response is enough unless implementation later proves a stable need.

## Rule Design Notes

### Word-count gate

Use the active bucket policy already present in project docs as the base.

The strong gate should not invent a new word-count system. It should reuse the current bucket-aware chapter-length policy and only add stronger enforcement semantics.

### Shrinkage gate

The gate should not block merely because one chapter is shorter than the last one.

Block only when both are true:

- the chapter is already below the configured lower band
- and the drop is materially abnormal against a recent local baseline

This avoids punishing legitimate compression chapters while still catching “three-chapter workflow degradation”.

### Typo / malformed-text gate

Use conservative heuristics only.

Blockers should focus on:

- repeated exact malformed tokens
- repeated broken phrases
- obvious duplicated sentence fragments
- recurrent punctuation corruption

Do not pretend to do perfect proofreading.

### Voice / canon gate

Block only when the contradiction is directly supported by:

- `设定集/角色/*.md`
- truth sheets
- recent chapter summaries or text

Low-confidence style concerns remain review findings, not hard blocks.

## Error Handling

The system must fail closed, but clearly.

### If policy file is missing

- `novel-write` and `novel-close` should stop and say the strong-gate policy is unavailable
- do not silently bypass hard gates

### If required setting files are missing

- pre-write source gate blocks and reports exact missing files

### If chapter metadata is incomplete

- post-write gate should fall back to chapter text and recent written files
- missing metadata alone should not disable the gate

### If sync overrides are malformed

- sync should still refuse unsafe candidates
- low-confidence entities should default to review queue, not direct materialization

## Testing Strategy

Implementation should be verified with focused tests and one end-to-end sample flow.

### Policy tests

- policy file parses
- bucket thresholds resolve correctly
- required truth-source mappings resolve correctly

### Pre-write gate tests

- chapter depending on kinship truth blocks when truth sheets are absent
- chapter depending on office titles blocks when office truth files are absent
- chapter with complete sources passes

### Post-write gate tests

- hard-min short chapter blocks
- abnormal shrinkage against recent baseline blocks
- normal shorter-but-valid chapter passes
- obvious malformed-token cluster blocks
- vague style-only issue does not hard-block

### Sync gate tests

- phrase-fragment character candidates are rejected to review queue
- real repeated character names still materialize
- overrides can force-ignore or alias a candidate

### End-to-end smoke

Use a project sample with:

- one missing truth-sheet case
- one short-chapter failure case
- one polluted-sync candidate case

The smoke should prove:

- write is blocked before hallucinated drafting
- close is blocked before false convergence
- sync no longer writes garbage entity cards

## Risks

### Risk 1: False positives block valid writing

Mitigation:

- only hard-block on objective or high-confidence checks
- keep subjective findings in review, not in gate blockers

### Risk 2: Rule duplication across skills

Mitigation:

- one JSON policy
- skill docs only describe where the policy is enforced

### Risk 3: Over-engineered checker scope

Mitigation:

- v1 blocks only the failures already proven costly in real projects
- no universal language-analysis ambition

## Recommended Implementation Order

1. add `docs/strong-quality-gate-policy.json`
2. implement sync-pollution gate in `scripts/sync-setting-assets.py`
3. wire pre-write source gate into `skills/novel-write/SKILL.md`
4. wire post-write hard gate into `skills/novel-close/SKILL.md`
5. tighten downstream wording in `novel-review` / `novel-precheck` only as needed for consistency
6. add focused tests and smoke evidence

## Success Criteria

This design is successful when:

- a chapter that lacks required truth sources cannot enter drafting
- a chapter that clearly fails hard quality constraints cannot be reported as closed
- sync no longer materializes obvious garbage entities into `设定集/`
- the system still uses existing workflow units instead of growing a new parallel skill stack
