# `novel-close` Design

Date: 2026-03-23

## Goal

Add a new orchestration skill, `novel-close`, that performs one bounded chapter-convergence pass without blurring the existing skill boundaries.

The skill exists to make chapter cleanup easier to run as a default workflow step while keeping:

- `novel-review` read-only
- `novel-fix` responsible for local content repair
- `novel-polish` responsible for language-layer cleanup and anti-AI cleanup
- `novel-rewrite` responsible for structural rebuilds

## Problem

The current workflow already supports:

`novel-write -> novel-review -> novel-fix/polish/rewrite -> novel-review`

But it leaves two practical gaps:

1. The user must manually compose the convergence loop every time.
2. Anti-AI cleanup exists, but it only runs if the user explicitly chooses `novel-polish`.

Pushing anti-AI cleanup directly into `novel-review` would solve the second gap at the cost of breaking a more important invariant: review would stop being a pure evaluator and become a hidden editor.

## Design Summary

Introduce a new skill named `novel-close`.

`novel-close` is a bounded workflow orchestrator for one chapter. It does not replace any existing editing skill. It only coordinates them in a deterministic order:

1. run `novel-review`
2. select exactly one route
3. execute that route when needed
4. run a final `novel-review` if the chapter was modified

This makes anti-AI cleanup part of the standard convergence flow, but only through the existing `novel-polish` boundary.

## Scope

### In scope

- single-chapter convergence
- route selection based on the latest review result
- optional automatic anti-AI cleanup when the latest review points to `novel-polish`
- final re-review after any actual modification
- lightweight workflow trace written into existing chapter metadata

### Out of scope

- background execution
- multi-chapter batching
- hidden automatic edits after `novel-write`
- replacing `novel-review`, `novel-fix`, `novel-polish`, or `novel-rewrite`
- chaining multiple main repair routes in one close pass

## Skill Contract

### Name

`novel-close`

### Purpose

Complete one chapter convergence pass with explicit routing and preserved skill boundaries.

### Minimal inputs

- `chapter`

### Optional inputs

- `mode`
  - `auto`
  - `review-only`
  - `force-polish`
  - `force-fix`
- `threshold`
- `preview`

## Route Model

`novel-close` must always start from a fresh `novel-review`.

In `auto` mode, it reads the latest review output and selects one primary route:

- `none`
- `novel-fix`
- `novel-polish`
- `novel-rewrite`

Only one primary route may run in a single `novel-close` execution.

This rule is intentionally strict. It prevents the workflow from drifting back into:

- `fix -> polish -> tiny tweak -> another polish`
- mixed structural and cosmetic edits in one opaque pass
- unclear attribution of what actually improved the chapter

## Anti-AI Cleanup Behavior

Anti-AI cleanup is allowed inside `novel-close`, but only through the `novel-polish` branch.

`novel-close` may trigger `novel-polish` only when all of the following are true:

- the first review returns `recommended_next_action = novel-polish`
- the dominant issue cluster is language-layer
- the chapter has no structural blocker
- the chapter does not primarily need local plot/content repair
- current repair attempts are still below the escalation threshold

Typical triggers include:

- obvious AI-style wording
- explanation replacing scene display
- weak or generic dialogue
- pacing drag from explanatory prose
- voice flattening across characters

This keeps anti-AI cleanup real and automatic inside the convergence workflow, while preserving the rule that only `novel-polish` edits prose for that purpose.

## Interaction with Existing Skills

### `novel-review`

- stays read-only
- produces the first route decision
- produces the final validation pass after edits

### `novel-fix`

- remains the route for local content repair
- can absorb trivial wording cleanup in touched paragraphs, but is not the primary anti-AI mechanism

### `novel-polish`

- remains the only route that performs explicit anti-AI cleanup
- still preserves chapter purpose and avoids structural redesign

### `novel-rewrite`

- remains the route for structural failure
- `novel-close` must not downgrade rewrite-sized work into polish

### `novel-workflow`

Do not extend `novel-workflow` into the executor for this feature.

Current `novel-workflow` is a lightweight state manager, not a true orchestrator. Expanding it into execution control would blur its current contract and make the system harder to reason about.

## State Design

Do not create a new quality-center file.

Keep using `chapter_meta[N]` as the persistence layer, with only lightweight convergence trace fields added if needed:

- `last_close_time`
- `last_close_route`
- `last_close_review_score_before`
- `last_close_review_score_after`

These fields are intentionally narrow. They record what happened during the convergence pass without turning state into a workflow engine or a second scoring system.

## Workflow

### `mode=auto`

1. Read current chapter state.
2. Run `novel-review`.
3. Inspect:
   - `recommended_next_action`
   - issue clusters
   - repair-attempt history
4. Choose one route.
5. If route is `none`, stop and report no edit needed.
6. If route is `novel-fix`, run one local repair pass.
7. If route is `novel-polish`, run one polish pass.
8. If route is `novel-rewrite`, stop and recommend explicit rewrite handling, or invoke rewrite only if the skill contract for this mode allows it.
9. If the chapter changed, run a second `novel-review`.
10. Persist lightweight close metadata.

### `mode=review-only`

- run only the opening `novel-review`
- do not modify chapter text
- do not run re-review

### `mode=force-polish`

- still requires an opening `novel-review`
- only proceeds if no structural blocker is present
- otherwise stop and report that force-polish is unsafe

### `mode=force-fix`

- still requires an opening `novel-review`
- only proceeds if the chapter remains fix-sized
- otherwise stop and route up

## Guardrails

Three guardrails define the feature:

1. Review-first
   - `novel-close` never skips the first review.
2. Single-route-per-pass
   - each run executes at most one main repair route.
3. Re-review after edit
   - any actual text change must be followed by a final review.

Together these rules preserve explainability and make every close pass auditable.

## Error Handling

`novel-close` should stop early and report directly when:

- chapter files are missing
- `.mighty/state.json` is missing or malformed
- latest review output is incomplete
- forced mode conflicts with the detected route
- repair attempts already meet the rewrite escalation threshold

If routing is ambiguous, prefer safety:

- structural ambiguity -> stop and recommend `novel-rewrite`
- mixed local-content and language issues -> prefer `novel-fix`
- pure language cleanup -> prefer `novel-polish`

## Default Workflow Placement

Update the recommended正文生产 workflow from:

`novel-write -> novel-review -> route -> novel-review`

to:

`novel-write -> novel-close`

The documentation must still explain that `novel-close` is only a wrapper around:

`review -> route -> re-review`

This keeps the user-facing workflow simpler without hiding the underlying quality model.

## Testing Strategy

### Contract checks

- `novel-review` remains read-only
- `novel-close` never executes more than one main route
- anti-AI cleanup happens only via the polish branch

### Happy paths

- review returns `none`
- review returns `novel-polish` for AI-style cleanup
- review returns `novel-fix` for local repair

### Guardrail paths

- review returns `novel-rewrite`
- forced polish encounters structural blockers
- repair attempts already exceed allowed convergence retries

### Evidence to collect

- before/after review score
- selected route
- whether re-review happened
- whether the chapter actually converged

## Recommended Implementation Order

1. Add `skills/novel-close/SKILL.md`
2. Wire its workflow rules against existing route semantics
3. Extend lightweight chapter state with close-trace fields if needed
4. Update `docs/default-workflows.md`
5. Update `docs/skill-usage.md`
6. Smoke-test at least:
   - polish route
   - fix route
   - rewrite stop path

## Decision

The best solution is not “make review auto-edit”.

The best solution is:

- keep `novel-review` pure
- introduce `novel-close` as a visible convergence workflow
- let anti-AI cleanup run automatically only when routed through `novel-polish`
- require re-review after every actual edit

That gives the project a real anti-AI convergence flow without breaking the current skill architecture.
