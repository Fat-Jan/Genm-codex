---
name: novel-resume
description: Resume a Codex-managed novel project from an interrupted workflow or from the current project state by identifying the safest continuation point and recommending the next action.
---

# Novel Resume

Use this skill when the user wants to continue after an interruption, recover an in-progress workflow, or quickly figure out the safest next writing step.

## Inputs

- optional `chapter`
- optional `from-workflow`
- optional explicit intent to continue immediately

## Preconditions

At least one of these should exist:

- `.mighty/workflow_state.json`
- `.mighty/state.json`

## Required reads

Always read what exists:

- `.mighty/workflow_state.json`
- `.mighty/state.json`
- `.mighty/setting-gate.json`

Read conditionally:

- `.mighty/import-report.json`
- `.mighty/learned-patterns.json`
- `.mighty/market-adjustments.json`
- `chapters/第NNN章.md`
- `大纲/章纲/第NNN章.md`
- `大纲/总纲.md`
- `设定集/角色/主角.md`

## Workflow

### 1. Choose the resume source

Use this priority order:

1. explicit `from-workflow`
2. active `.mighty/workflow_state.json`
3. explicit `chapter`
4. fallback to `.mighty/state.json`

### 2. Workflow-state recovery mode

If `.mighty/workflow_state.json` exists and contains an active task:

1. Read:
   - `command`
   - `args`
   - `status`
   - `current_step`
   - `completed_steps`
   - `failed_steps`
   - `pending_steps`
   - `last_heartbeat`
2. Identify the safest resume point:
   - `running` -> resume from `current_step`
   - `failed` -> retry the latest failed step if clear, otherwise use `current_step`
   - `timeout` -> restart from `current_step`
   - `cancelled` -> suggest resuming from the first pending step or the current step
   - when the task follows the fixed chapter transaction (`gate-check -> draft -> close -> maintenance -> snapshot`), prefer the safest recovery point instead of jumping ahead:
     - `gate-check` -> resolve blockers first
     - `draft` -> confirm chapter/state write boundary
     - `close` -> return to `novel-close`
     - `maintenance` -> finish maintenance before prose continuation
     - `snapshot` -> refresh or generate the final snapshot evidence
3. Return:
   - active task summary
   - interruption point
   - recommended next action
   - safest recovery point
   - prerequisite checks needed before continuing
   - if `.mighty/setting-gate.json` exists and is not `passed`, surface:
     - `blocking_gaps`
     - `review_items`
     - `minimal_next_action`
     before recommending any prose-generation continuation

### 3. State-based fallback mode

If there is no usable workflow state:

1. Read `.mighty/state.json`.
2. Determine:
   - current chapter
   - total words
   - protagonist current state
   - active foreshadowing
   - current learned / market guidance when available in sidecars
   - whether `.mighty/import-report.json` exists and indicates that existing chapters were imported but not fully reconstructed
   - whether the next chapter outline exists
   - whether `.mighty/setting-gate.json` blocks writing
3. If the user provided `chapter`, use it as the continuation target.
4. Otherwise, recommend the next chapter after `progress.current_chapter`.
5. Return a concise continuation brief:
   - current progress
   - immediate unresolved hooks
   - whether an import-report exists and still needs:
     - `novel-index build`
     - `setting gate`
   - gate status when present
   - `minimal_next_action` when the gate is `blocked` or `review_required`
   - next recommended command

## Output conventions

Prefer one of these formats:

### Workflow recovery

- target command
- workflow status
- interruption point
- completed / pending / failed steps
- safest resume action

### State fallback

- current chapter
- total words
- protagonist state summary
- active foreshadowing summary
- gate status / minimal next action when relevant
- next recommended chapter or task

## First-version safety rules

- Default path is read-only diagnosis plus recommendation.
- Do not pretend to replay partial hidden internal steps that do not exist in the Codex version.
- Only recommend a concrete follow-up skill when the target is unambiguous:
  - `novel-write`
  - `novel-review`
  - `novel-polish`
  - `novel-rewrite`
  - `novel-outline`
- If both workflow state and project state are ambiguous, say so directly and ask for the smallest missing input.

## Notes

- The Codex version does not assume the full legacy workflow engine exists.
- Treat `workflow_state.json` as advisory state, not as proof that every underlying step artifact exists.
- When a task clearly follows the fixed chapter transaction, use that order to compute the safest recovery point instead of guessing from timestamps alone.
- If the requested chapter outline is missing, recommend `novel-outline` instead of guessing the continuation path.
- When sidecar guidance exists, prefer reading it over the summary pointer in `state`.
- If `.mighty/import-report.json` exists, treat it as a real handoff artifact for imported chapters; do not pretend import alone reconstructed full canon/state.
- If `.mighty/setting-gate.json` is present and not `passed`, do not recommend `novel-write` as the next step ahead of the gate's `minimal_next_action`.
