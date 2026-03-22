# novel-close Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增 `novel-close` 组合 skill，把“单章收口轮”固化为 `review -> 单一路由 -> re-review` 的清晰流程，并把压 AI 味稳定放进 `polish` 分支。

**Architecture:** 以新建 `skills/novel-close/SKILL.md` 为中心，围绕现有 `novel-review` / `novel-fix` / `novel-polish` / `novel-rewrite` 的边界做编排，不把执行逻辑塞回 `novel-review` 或 `novel-workflow`。轻量状态痕迹继续挂在 `chapter_meta[N]`，文档与安装脚本同步更新，确保新 skill 可发现、可安装、可验证。

**Tech Stack:** Markdown skill specs, repo shell scripts, JSON state template, shared schema docs, repo-local verification commands

---

### Task 1: Register `novel-close` in repo structure

**Files:**
- Create: `skills/novel-close/SKILL.md`
- Create: `skills/novel-close/agents/openai.yaml`
- Modify: `scripts/install-skills.sh`
- Modify: `scripts/validate-migration.sh`

- [ ] **Step 1: Add a failing structural expectation to the migration validator**

```bash
for skill in \
  novel-init \
  novel-analyze \
  novel-close \
  novel-outline
```

Run:

```bash
bash scripts/validate-migration.sh
```

Expected: FAIL with `Missing file: .../skills/novel-close/SKILL.md`

- [ ] **Step 2: Create the minimal `novel-close` skill skeleton**

```md
---
name: novel-close
description: Close one chapter through a bounded review -> route -> re-review pass.
---
```

- [ ] **Step 3: Add installation aliases for `novel-close`**

```bash
install_skill_aliases "novel-close"
```

- [ ] **Step 4: Add the default agent prompt file**

```yaml
model: gpt-5
default_prompt: "Use $novel-close to converge one reviewed chapter through one bounded repair route."
```

- [ ] **Step 5: Re-run structure checks**

Run:

```bash
bash scripts/validate-migration.sh
bash scripts/install-skills.sh
```

Expected:

- `Migration validation passed`
- `Installed Genm-codex skills into .../.codex/skills`

- [ ] **Step 6: Commit**

```bash
git add skills/novel-close/SKILL.md skills/novel-close/agents/openai.yaml scripts/install-skills.sh scripts/validate-migration.sh
git commit -m "feat: register novel-close skill"
```

### Task 2: Implement the `novel-close` orchestration contract

**Files:**
- Modify: `skills/novel-close/SKILL.md`
- Reference: `docs/superpowers/specs/2026-03-23-novel-close-design.md`
- Reference: `skills/novel-review/SKILL.md`
- Reference: `skills/novel-fix/SKILL.md`
- Reference: `skills/novel-polish/SKILL.md`
- Reference: `skills/novel-rewrite/SKILL.md`

- [ ] **Step 1: Write the failing contract assertions as grep checks**

Run:

```bash
rg -n "mode=auto|review-only|force-polish|force-fix|Single-route-per-pass|Re-review after edit" skills/novel-close/SKILL.md
```

Expected: FAIL or incomplete matches before the body is written

- [ ] **Step 2: Fill in inputs, preconditions, required reads, and outputs**

```md
## Inputs
- `chapter`
- optional `mode`
- optional `threshold`
- optional `preview`
```

- [ ] **Step 3: Encode the route rules exactly once**

```md
- run `novel-review` first
- choose one route only: `none` / `novel-fix` / `novel-polish` / `novel-rewrite`
- do not run `fix + polish` in the same pass
```

- [ ] **Step 4: Encode anti-AI polish gating**

```md
Only trigger `novel-polish` when:
- `recommended_next_action = novel-polish`
- dominant issue cluster is language-layer
- no structural blocker
- repair attempts remain below rewrite escalation
```

- [ ] **Step 5: Encode re-review and stop conditions**

```md
If chapter text changed, run a final `novel-review`.
If route is ambiguous, prefer safety and route up.
```

- [ ] **Step 6: Re-run the contract assertions**

Run:

```bash
rg -n "mode=auto|review-only|force-polish|force-fix|Single-route-per-pass|Re-review after edit|recommended_next_action = novel-polish" skills/novel-close/SKILL.md
sed -n '1,260p' skills/novel-close/SKILL.md
```

Expected: all required clauses are present and readable in one pass

- [ ] **Step 7: Commit**

```bash
git add skills/novel-close/SKILL.md
git commit -m "feat: define novel-close orchestration contract"
```

### Task 3: Add lightweight close-trace state fields

**Files:**
- Modify: `shared/references/shared/state-schema.md`
- Modify: `shared/templates/state-v5-template.json`
- Reference: `docs/superpowers/specs/2026-03-23-novel-close-design.md`

- [ ] **Step 1: Write the failing schema search**

Run:

```bash
rg -n "last_close_time|last_close_route|last_close_review_score_before|last_close_review_score_after" shared/references/shared/state-schema.md shared/templates/state-v5-template.json
```

Expected: no matches yet

- [ ] **Step 2: Extend the schema doc with the four optional chapter-meta fields**

```md
| last_close_time | string | 最近一次 `novel-close` 执行时间 |
| last_close_route | string | 最近一次 `novel-close` 主路由 |
```

- [ ] **Step 3: Add nullable/default placeholders to the state template**

```json
"last_close_time": null,
"last_close_route": "",
"last_close_review_score_before": 0,
"last_close_review_score_after": 0
```

- [ ] **Step 4: Validate the JSON template**

Run:

```bash
jq empty shared/templates/state-v5-template.json
rg -n "last_close_time|last_close_route|last_close_review_score_before|last_close_review_score_after" shared/references/shared/state-schema.md shared/templates/state-v5-template.json
```

Expected:

- `jq` exits successfully
- all four fields appear in both schema/template where appropriate

- [ ] **Step 5: Commit**

```bash
git add shared/references/shared/state-schema.md shared/templates/state-v5-template.json
git commit -m "feat: add novel-close state trace fields"
```

### Task 4: Surface `novel-close` in user-facing docs

**Files:**
- Modify: `README.md`
- Modify: `docs/default-workflows.md`
- Modify: `docs/skill-usage.md`
- Modify: `docs/start-here.md`

- [ ] **Step 1: Update the installed-skill / workflow entry points**

```md
- `genm-novel-close`
- `novel-close`
```

- [ ] **Step 2: Replace the manual single-chapter convergence sequence in the default workflow**

```md
1. `novel-write`
2. `novel-close`

其中 `novel-close` 内部执行：
`novel-review -> route -> novel-review`
```

- [ ] **Step 3: Update skill usage examples and “从哪里开始” guidance**

```md
请使用 novel-close skill，对第001章做一次 auto 模式单章收口。
```

- [ ] **Step 4: Make sure the docs still explain route semantics**

```md
局部问题 -> `novel-fix`
语言层问题 -> `novel-polish`
结构层问题 -> `novel-rewrite`
```

- [ ] **Step 5: Verify discoverability**

Run:

```bash
rg -n "novel-close" README.md docs/default-workflows.md docs/skill-usage.md docs/start-here.md
```

Expected: each entry point contains at least one accurate `novel-close` mention

- [ ] **Step 6: Commit**

```bash
git add README.md docs/default-workflows.md docs/skill-usage.md docs/start-here.md
git commit -m "docs: surface novel-close in user workflows"
```

### Task 5: Align adjacent skill guidance with the new close loop

**Files:**
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-review/SKILL.md`
- Modify: `skills/novel-polish/SKILL.md`
- Modify: `skills/novel-fix/SKILL.md`

- [ ] **Step 1: Update `novel-write` next-step guidance**

```md
Recommend running `novel-close` immediately after writing.
```

- [ ] **Step 2: Update `novel-review` notes so auto-edit requests route to `novel-close` for bounded closure**

```md
If the user wants one bounded convergence pass rather than review-only output, recommend `novel-close`.
```

- [ ] **Step 3: Update `novel-polish` and `novel-fix` notes to acknowledge orchestration by `novel-close`**

```md
This skill may be selected as the primary route inside `novel-close`.
```

- [ ] **Step 4: Re-read the four files for contradictions**

Run:

```bash
rg -n "novel-close|Recommend running `novel-close`|bounded convergence pass" skills/novel-write/SKILL.md skills/novel-review/SKILL.md skills/novel-polish/SKILL.md skills/novel-fix/SKILL.md
sed -n '170,220p' skills/novel-write/SKILL.md
```

Expected: no file still implies that plain `novel-review` is the only default post-write step

- [ ] **Step 5: Commit**

```bash
git add skills/novel-write/SKILL.md skills/novel-review/SKILL.md skills/novel-polish/SKILL.md skills/novel-fix/SKILL.md
git commit -m "docs: align skill guidance around novel-close"
```

### Task 6: Run verification and record smoke evidence

**Files:**
- Modify: `progress.md`
- Optional create: `docs/smoke-novel-close-2026-03-23.md`

- [ ] **Step 1: Run repository-level validation**

Run:

```bash
bash scripts/validate-migration.sh
```

Expected: `Migration validation passed`

- [ ] **Step 2: Verify installed alias generation**

Run:

```bash
bash scripts/install-skills.sh
ls -l "${HOME}/.codex/skills" | rg "novel-close|genm-novel-close"
```

Expected: both symlinks exist and point to `skills/novel-close`

- [ ] **Step 3: Run a manual contract smoke against the sample project**

Run:

```bash
sed -n '1,260p' skills/novel-close/SKILL.md
sed -n '1,200p' e2e-novel/.mighty/state.json
```

Expected:

- `novel-close` clearly describes `review -> single route -> re-review`
- state trace fields can be written without requiring a new top-level state block

- [ ] **Step 4: Record evidence**

```md
- `novel-close` added to install + validation scripts
- docs entry points updated
- state schema/template updated
- migration validation passed
```

- [ ] **Step 5: Final commit**

```bash
git add progress.md docs/smoke-novel-close-2026-03-23.md
git commit -m "test: record novel-close verification evidence"
```

If no dedicated smoke doc is created, replace the final command with:

```bash
git add progress.md
git commit -m "test: record novel-close verification evidence"
```
