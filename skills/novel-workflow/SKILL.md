---
name: novel-workflow
description: Inspect and manage a lightweight `.mighty/workflow_state.json` for a Codex-managed novel project, including status, step completion, failure marking, and reset operations.
---

# Novel Workflow

Use this skill when the user wants to view or update lightweight workflow state for a Codex-managed novel project.

## Inputs

- operation:
  - `status`
  - `complete`
  - `fail`
  - `reset`
- optional step name
- optional failure reason

## Preconditions

- `.mighty/` exists

## Workflow state location

- `.mighty/workflow_state.json`
- `shared/templates/workflow-state-v2.json` is the preferred template for the chapter transaction contract

## First-version scope

This version is a state manager, not a full orchestrator.

It should:

- show current workflow state
- mark a step complete
- mark a step failed
- reset current task state

It should not:

- spawn or run hidden background tasks
- pretend to replay the entire workflow automatically
- claim external process control it does not have

## Expected state shape

Use a conservative version of the legacy structure, upgraded for the fixed chapter transaction:

```json
{
  "version": "2.0",
  "transaction_contract": "chapter-transaction-v1",
  "current_task": {
    "command": "novel-write",
    "args": {},
    "status": "running",
    "current_step": "gate-check",
    "completed_steps": [],
    "failed_steps": [],
    "pending_steps": ["gate-check", "draft", "close", "maintenance", "snapshot"],
    "last_successful_checkpoint": null,
    "started_at": "...",
    "last_heartbeat": "...",
    "error_message": null
  },
  "history": []
}
```

Recommended fixed step order for a single-chapter chapter transaction:

1. `gate-check`
2. `draft`
3. `close`
4. `maintenance`
5. `snapshot`

## Required reads

Always read what exists:

- `.mighty/workflow_state.json`
- `.mighty/state.json`

## Workflow

### status

1. If `.mighty/workflow_state.json` is missing:
   - report idle / no active workflow
   - suggest using `novel-write`, `novel-batch`, or `novel-resume`
2. If it exists:
   - summarize current task
   - summarize current step
   - summarize completed / pending / failed steps
   - if the current task follows the chapter transaction, explain which of the five fixed steps it is currently in
   - mention `last_heartbeat`

### complete

1. Read workflow state.
2. Validate that the requested step is present in the active task.
3. Move the step from `pending_steps` to `completed_steps` when needed.
4. Advance `current_step` to the next pending step when possible, preserving the fixed transaction order when it exists.
5. Refresh `last_heartbeat`.
6. If no pending steps remain, mark task `completed`.
7. If the completed task was `novel-write` or `novel-batch`, recommend post-write maintenance:
   - `scripts/post-task-maintenance.py <project_root> --trigger workflow`
   - or `novel-sync`

### fail

1. Read workflow state.
2. Validate step name.
3. Add the step to `failed_steps` if needed.
4. Mark task status as `failed`.
5. Set `error_message`.
6. Refresh `last_heartbeat`.

### reset

1. Read workflow state if it exists.
2. Archive the current task into `history` when possible.
3. Clear `current_task`.
4. Preserve bounded history.

## Output conventions

### status

- task status
- current step
- completed / pending / failed
- resume recommendation when relevant

### complete / fail / reset

- action taken
- new workflow status
- next recommended command

## Notes

- If the workflow file is malformed, say so directly and recommend reset or manual repair.
- Treat this as coordination state only.
- Prefer the fixed chapter transaction order when the task is a normal single-chapter prose run.
- If the user actually wants to continue writing, route to `novel-resume` or `novel-write` rather than pretending workflow state alone performs the work.
- For long-running projects, do not treat workflow completion as fully stable until maintenance has had a chance to sync settings and thin `state`.
