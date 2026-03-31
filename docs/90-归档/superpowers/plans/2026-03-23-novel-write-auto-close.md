# novel-write Auto-Close Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 `novel-write` 在单章写作后默认尝试守卫式自动 `novel-close`，并支持显式 `skip_close=true` 跳过。

**Architecture:** 不把 `review -> route -> re-review` 塞进 `novel-write` 本体，而是由 `novel-write` 在写完并落基础 state 后，按守卫条件显式 handoff 给 `novel-close`。`novel-batch` 不继承该默认行为，维护链也不参与正文改动。

**Tech Stack:** Markdown skill contracts, repo-local workflow docs, existing `chapter_meta` close-trace fields, shell-based validation

---

### Task 1: Extend `novel-write` contract for guarded auto-close

**Files:**
- Modify: `skills/novel-write/SKILL.md`
- Reference: `docs/90-归档/superpowers/specs/2026-03-23-novel-write-auto-close-design.md`
- Reference: `skills/novel-close/SKILL.md`

- [ ] **Step 1: Add the new input expectation**

```md
- optional `skip_close`
```

- [ ] **Step 2: Add the post-write auto-close workflow step**

```md
after base state updates:
- if single-chapter write and guards pass and `skip_close` is not true:
  - attempt `novel-close`
- otherwise:
  - report explicit skip reason
```

- [ ] **Step 3: Encode the guard conditions**

```md
- not batch mode
- state exists
- outline exists
- target chapter file written successfully
- workflow state not clearly failed
- user did not request write-only
```

- [ ] **Step 4: Encode failure behavior**

```md
If auto-close fails after the chapter is written:
- keep write success
- report post-write auto-close failure clearly
```

- [ ] **Step 5: Update output conventions**

```md
- chapter written
- auto-close attempted or skipped
- route used or skip reason
```

- [ ] **Step 6: Verify contract text**

Run:

```bash
rg -n "skip_close|auto-close|novel-close|write-only|single-chapter" skills/novel-write/SKILL.md
sed -n '1,260p' skills/novel-write/SKILL.md
```

Expected: the guarded auto-close behavior is explicit and does not inline `novel-close` internals

- [ ] **Step 7: Commit**

```bash
git add skills/novel-write/SKILL.md
git commit -m "feat: add guarded auto-close to novel-write contract"
```

### Task 2: Clarify `novel-close` as a post-write handoff target

**Files:**
- Modify: `skills/novel-close/SKILL.md`

- [ ] **Step 1: Add explicit note that `novel-close` may be called by `novel-write`**

```md
This skill may be invoked as the guarded post-write close step after `novel-write`.
```

- [ ] **Step 2: Clarify skip/guard interaction expectations**

```md
`novel-close` remains the executor.
`novel-write` decides whether to attempt the handoff.
```

- [ ] **Step 3: Verify wording**

Run:

```bash
rg -n "post-write|novel-write|executor|handoff" skills/novel-close/SKILL.md
```

Expected: the relationship between `novel-write` and `novel-close` is explicit and boundary-safe

- [ ] **Step 4: Commit**

```bash
git add skills/novel-close/SKILL.md
git commit -m "docs: clarify novel-close as post-write handoff"
```

### Task 3: Update default workflow docs

**Files:**
- Modify: `docs/00-当前有效/default-workflows.md`
- Modify: `docs/00-当前有效/start-here.md`
- Modify: `docs/00-当前有效/skill-usage.md`
- Optional modify: `README.md`

- [ ] **Step 1: Update the main正文 workflow**

```md
`novel-write` now defaults to a guarded automatic `novel-close` for single-chapter runs.
```

- [ ] **Step 2: Document the batch exception**

```md
`novel-batch` does not auto-close each chapter.
```

- [ ] **Step 3: Document explicit skip**

```md
Use `skip_close=true` when the user wants write-only behavior.
```

- [ ] **Step 4: Verify discoverability**

Run:

```bash
rg -n "skip_close|auto-close|自动收口|novel-close" docs/00-当前有效/default-workflows.md docs/00-当前有效/start-here.md docs/00-当前有效/skill-usage.md README.md
```

Expected: user-facing docs consistently describe the new default-on guarded behavior

- [ ] **Step 5: Commit**

```bash
git add docs/00-当前有效/default-workflows.md docs/00-当前有效/start-here.md docs/00-当前有效/skill-usage.md README.md
git commit -m "docs: describe novel-write auto-close workflow"
```

### Task 4: Verify boundaries and non-goals

**Files:**
- Read-only check: `skills/novel-batch/SKILL.md`
- Read-only check: `scripts/post-task-maintenance.py`
- Modify if absolutely necessary: none expected

- [ ] **Step 1: Confirm `novel-batch` is untouched**

Run:

```bash
rg -n "novel-close|auto-close|skip_close" skills/novel-batch/SKILL.md
```

Expected: no matches

- [ ] **Step 2: Confirm maintenance script is untouched**

Run:

```bash
rg -n "novel-close|auto-close" scripts/post-task-maintenance.py
```

Expected: no matches

- [ ] **Step 3: Record boundary result in the plan execution notes or progress log**

```md
- auto-close stays in the write -> close path
- batch remains batch
- maintenance remains maintenance
```

- [ ] **Step 4: Commit only if boundary docs/logs were updated**

```bash
git add progress.md
git commit -m "test: record auto-close boundary checks"
```

Skip this commit if no tracked file changed.

### Task 5: Run final validation

**Files:**
- Modify: `progress.md`

- [ ] **Step 1: Run migration validation**

Run:

```bash
bash scripts/validate-migration.sh
```

Expected: `Migration validation passed`

- [ ] **Step 2: Re-read the two skill contracts together**

Run:

```bash
sed -n '1,260p' skills/novel-write/SKILL.md
sed -n '1,260p' skills/novel-close/SKILL.md
```

Expected:

- `novel-write` triggers guarded auto-close
- `novel-close` remains the executor
- neither file implies hidden background work

- [ ] **Step 3: Record verification evidence**

```md
- guarded auto-close documented
- explicit skip documented
- batch exclusion preserved
- maintenance boundary preserved
- migration validation passed
```

- [ ] **Step 4: Commit**

```bash
git add progress.md
git commit -m "test: record novel-write auto-close verification evidence"
```
