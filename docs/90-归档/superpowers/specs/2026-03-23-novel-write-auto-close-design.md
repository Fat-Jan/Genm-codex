# `novel-write` Auto-Close Design

Date: 2026-03-23

## Goal

Make single-chapter `novel-write` runs attempt a guarded automatic `novel-close` by default, so chapter convergence is not left to user memory.

The design must preserve the existing architectural boundaries:

- `novel-write` writes the chapter
- `novel-close` orchestrates `review -> route -> re-review`
- `novel-review` remains read-only
- `novel-fix` / `novel-polish` / `novel-rewrite` keep their current roles
- `novel-batch` does not inherit this default behavior

## Problem

The project now has a dedicated `novel-close` skill, but the default workflow still depends on the user remembering to run it after writing.

That creates a predictable failure mode:

1. the chapter is written
2. the user moves on
3. convergence is skipped
4. `state` falls behind the real repair route

For this user, “default on” is preferable to “optional but easy to forget.”

At the same time, directly stuffing hidden review/fix/polish behavior into `novel-write` would blur boundaries if done carelessly.

## Design Summary

Keep `novel-close` as the executor.

Add a new default behavior to `novel-write`:

- after a successful single-chapter write
- after base chapter/state updates are saved
- `novel-write` automatically attempts one guarded `novel-close`

This is not an unconditional auto-edit system.

It is a guarded post-write handoff with three rules:

1. default on
2. single-chapter only
3. explicit skip remains available

## Why This Layer

The auto-close trigger should live in `novel-write`, not in `post-task-maintenance.py`.

Reason:

- this is part of the content-production mainline, not the maintenance lane
- maintenance currently handles sync / sidecar / thinning / housekeeping concerns
- allowing maintenance to mutate prose would make the system harder to reason about

So the intended layering is:

- `novel-write` decides whether to trigger post-write close
- `novel-close` performs the close
- maintenance remains maintenance

## Scope

### In scope

- auto-attempt `novel-close` after single-chapter `novel-write`
- guard conditions that decide whether auto-close may run
- explicit skip control for users
- clear output telling the user whether auto-close ran or was skipped
- reusing existing `chapter_meta` close-trace fields when close actually runs

### Out of scope

- changing `novel-batch` to auto-close each chapter
- moving auto-close into maintenance scripts
- hidden background task execution
- new top-level workflow automation state
- changing `novel-review` into an editor

## Default Behavior

After `novel-write` finishes a single chapter and saves its base outputs, it should:

1. evaluate auto-close guard conditions
2. if guards pass, invoke `novel-close`
3. if guards fail, skip auto-close explicitly and report why

Default setting: ON

This default should be the normal behavior unless the user explicitly opts out for that run.

## Explicit Escape Hatch

Support an explicit opt-out such as:

- `skip_close=true`

When present:

- `novel-write` completes normally
- automatic `novel-close` is not attempted
- response must say auto-close was skipped intentionally

## Guard Conditions

Auto-close should run only when all of the following are true:

1. this is a single-chapter `novel-write`, not `novel-batch`
2. `.mighty/state.json` exists
3. target outline file exists
4. the target chapter file was successfully written
5. current workflow state is not clearly failed or malformed
6. the user did not explicitly request a write-only pass

If any guard fails:

- do not fake execution
- do not silently suppress the behavior
- report the exact skip reason

## Skip Reasons

The user-visible response should clearly indicate one of these paths:

- auto-close ran
- auto-close skipped because this is batch mode
- auto-close skipped because `skip_close=true`
- auto-close skipped because required project files are missing
- auto-close skipped because workflow state is unsafe

This keeps the “default on” behavior understandable instead of magical.

## Interaction with `novel-close`

`novel-write` should not inline `review -> route -> re-review`.

It should call or hand off to `novel-close` as a separate bounded phase.

That preserves:

- explainability
- modularity
- future reuse of `novel-close` outside `novel-write`

## Interaction with `novel-batch`

`novel-batch` should not inherit the single-chapter default.

Reason:

- batch mode has a different cost and rhythm profile
- per-chapter auto-close inside batch would slow throughput and complicate failure handling
- current workflow already expects batch-level quality gating separately

So the rule is simple:

- `novel-write`: default guarded auto-close ON
- `novel-batch`: default guarded auto-close OFF

## State Design

Do not add a new top-level automation center.

Do not add extra `auto_close_attempted` / `auto_close_result` fields.

Use existing mechanisms:

- `novel-close` already writes close-trace fields when it actually runs
- `novel-write` response should tell the user whether auto-close ran or was skipped

This keeps state small and avoids duplicating execution trace data in multiple places.

## Output Design

`novel-write` output should now report one of these outcomes:

### Auto-close ran

- chapter written
- auto-close attempted
- close route used
- final status after close when available

### Auto-close skipped

- chapter written
- auto-close not attempted
- explicit reason

Example shape:

```md
写作完成：第016章
自动收口：已执行 / 已跳过
原因或路由：`novel-fix` / `novel-polish` / `none` / `skip_close=true` / `batch mode`
```

## Files Expected to Change

Primary implementation target:

- `skills/novel-write/SKILL.md`

Supporting contract updates:

- `skills/novel-close/SKILL.md`

User-facing workflow docs:

- `docs/00-当前有效/default-workflows.md`
- `docs/00-当前有效/skill-usage.md`
- `docs/00-当前有效/start-here.md`

Possibly also:

- `README.md`

Only if needed for discoverability.

## Error Handling

If auto-close invocation fails after the chapter has already been written:

- the write itself should still count as successful
- `novel-write` must explicitly report that post-write auto-close failed
- do not pretend the chapter is converged

This is important because write success and close success are separate stages.

## Testing Strategy

### Happy path

- single-chapter write completes
- guarded auto-close runs
- user is told it ran

### Explicit skip

- single-chapter write with `skip_close=true`
- chapter writes successfully
- auto-close is skipped with explicit reason

### Batch safety

- batch path does not auto-close

### Guard failure

- missing outline or unsafe workflow state
- chapter still writes only when the write preconditions allow it
- auto-close is reported as skipped or failed clearly

### Boundary checks

- `novel-review` remains read-only
- `novel-write` does not absorb `novel-close` logic internally
- `post-task-maintenance.py` remains outside prose mutation

## Decision

The best design is:

- default on
- guarded
- single-chapter only
- explicit skip available
- implemented as a `novel-write -> novel-close` handoff

This satisfies the user’s preference for not forgetting convergence, while keeping the current quality architecture coherent.
