---
name: novel-close
description: Close one chapter through a bounded review -> route -> re-review pass.
---

# Novel Close

Use this skill when the user wants one explicit chapter-convergence pass instead of manually stitching together `novel-review`, `novel-fix`, `novel-polish`, or `novel-rewrite`.

This skill may also be invoked as the guarded post-write close step after `novel-write`.

Inside the default chapter transaction, this skill is the `close` phase:

1. `gate-check`
2. `draft`
3. `close`
4. `maintenance`
5. `snapshot`

Default intent for the current workflow:

- always start from a fresh review
- execute at most one main repair route in a single pass
- re-review after any real text change
- keep anti-AI cleanup inside the `novel-polish` boundary instead of letting `novel-review` edit text
- remain the executor for chapter convergence; upstream write flows decide whether to hand off here

## Inputs

- `chapter`
- optional `mode`
  - `auto`
  - `review-only`
  - `force-polish`
  - `force-fix`
- optional `threshold`
- optional `preview`

## Preconditions

- `.mighty/state.json` exists
- `chapters/第N章.md` exists
- the standard route skills exist:
  - `novel-review`
  - `novel-fix`
  - `novel-polish`
  - `novel-rewrite`

## Required reads

- `.mighty/state.json`
- `chapters/第N章.md`
- `../../docs/default-workflows.md`

Read conditionally:

- `chapter_meta[N]` for:
  - `review_score`
  - `review_grade`
  - `recommended_next_action`
  - `fix_count`
  - `polish_count`
  - `critical_issues`
  - `warnings`
  - `issue_clusters`
- `大纲/章纲/第N章.md` when route ambiguity needs chapter-purpose confirmation
- `../../docs/strong-quality-gate-policy.json` when post-write hard blocking must be evaluated
- `scripts/post_write_lint.py` when deterministic post-write lint findings must be checked before close success

## Workflow

### `mode=auto`

1. Read the current chapter state.
2. Run a fresh `novel-review`.
3. Inspect:
   - `recommended_next_action`
   - `issue_clusters`
   - `critical_issues`
   - repair-attempt history from `fix_count + polish_count`
4. Choose exactly one main route:
   - `none`
   - `novel-fix`
   - `novel-polish`
   - `novel-rewrite`
5. If the route is `none`:
   - stop
   - report that the chapter does not need a repair pass
6. If the route is `novel-fix`:
   - run one bounded local repair pass
   - do not append a same-pass polish
7. If the route is `novel-polish`:
   - run one bounded polish pass
   - use that pass for anti-AI cleanup only when the polish gate below is satisfied
8. If the route is `novel-rewrite`:
   - stop and explicitly surface rewrite as the correct next move
   - do not downgrade rewrite-sized work into `novel-fix` or `novel-polish`
9. Before reporting close success, run the strong post-write hard gate when the project uses `../../docs/strong-quality-gate-policy.json`.
   - first run deterministic post-write lint through `scripts/post_write_lint.py`
   - treat deterministic lint as structured evidence, not as hidden editing
   - treat the policy file as the single rule source for hard blockers
   - if the gate reports a blocker, `novel-close` must not report the chapter as closed for this pass
   - route the chapter back to:
     - `novel-fix` for bounded local repair
     - `novel-rewrite` for structural failure
   - do not let a cosmetic polish path override a hard blocker
   - warnings from deterministic lint may inform `novel-fix` or later polish, but only policy-backed blockers stop close success
10. If chapter text changed, run a second `novel-review`.
11. Persist lightweight close metadata inside `chapter_meta[N]` when the project tracks those fields.

### `mode=review-only`

1. Run the opening `novel-review`.
2. Return the route recommendation and issue clusters.
3. Do not modify chapter text.
4. Do not run re-review.

### `mode=force-polish`

1. Still run the opening `novel-review`.
2. Proceed only when:
   - no structural blocker is present
   - the chapter does not primarily need `novel-fix`
   - repair attempts are still below rewrite escalation
3. If those conditions fail, stop and report that force-polish is unsafe.
4. If the chapter changed, run a final `novel-review`.

### `mode=force-fix`

1. Still run the opening `novel-review`.
2. Proceed only when the chapter remains `fix` sized.
3. If the chapter is rewrite sized, stop and route up.
4. If the chapter changed, run a final `novel-review`.

## Polish Gate

Anti-AI cleanup is allowed in `novel-close`, but only through the `novel-polish` branch.

Trigger `novel-polish` only when all of these are true:

- the fresh review returns `recommended_next_action = novel-polish`
- the dominant issue cluster is language-layer
- there is no structural blocker
- the chapter does not primarily need local plot / continuity / hook repair
- repair attempts remain below the rewrite escalation threshold

Typical qualifying language-layer issues:

- obvious AI-style wording
- explanation replacing scene display
- weak or generic dialogue
- pacing drag from explanatory prose
- flattened voice across characters

## Guardrails

### Review-first

- `novel-close` never skips the first `novel-review`

### Single-route-per-pass

- each run executes at most one main repair route
- do not run `fix + polish` in the same pass
- do not mix structural rebuild and cosmetic cleanup in one opaque action

### Re-review after edit

- any actual text change must be followed by a final `novel-review`

### Strong Hard Gate

- `novel-close` cannot declare convergence success when the strong post-write gate still reports objective blockers
- block only on policy-backed hard failures, not on vague style discomfort

## Output conventions

Return:

- first review summary
- chosen route
- whether an edit actually ran
- final review result when re-review happened
- concise statement of whether the chapter is now closed for this pass

## State update requirements

When the project tracks close metadata, update conservatively:

- `chapter_meta[N].last_close_time`
- `chapter_meta[N].last_close_route`
- `chapter_meta[N].last_close_review_score_before`
- `chapter_meta[N].last_close_review_score_after`

Do not create a new top-level workflow or quality state center for this feature.

## Notes

- This skill is an orchestrator, not a new editor.
- `novel-close` remains the executor; `novel-write` may decide whether to attempt the post-write handoff.
- `novel-close` participates in the larger chapter transaction contract, but it does not own `maintenance` or `snapshot`.
- Do not preload child skill contracts here. Once `novel-review` / `novel-fix` / `novel-polish` / `novel-rewrite` is selected, let that skill load its own required reads and boundaries.
- `novel-review` stays read-only.
- `novel-polish` remains the only explicit anti-AI cleanup route.
- If routing is ambiguous, prefer safety:
  - structural ambiguity -> surface `novel-rewrite`
  - mixed local-content and language issues -> prefer `novel-fix`
  - pure language cleanup -> prefer `novel-polish`
- If the user wants a single bounded convergence pass rather than a review-only report, this skill is the preferred entry point.
- Strong post-write blockers must resolve from `../../docs/strong-quality-gate-policy.json`, not from duplicated threshold text in this skill.
