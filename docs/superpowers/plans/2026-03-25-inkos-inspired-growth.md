# InkOS-Inspired Growth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `Genm-codex` from a strong skill collection into a more stable novel-production system by formalizing chapter transactions, adding an active-context layer, splitting deterministic prose lint from editorial review, feeding review outcomes back into the next chapter, and adding safer reference-learning / existing-manuscript handoff paths.

**Architecture:** Reuse the repo's proven `docs/ + skills/ + scripts/ + lightweight sidecars` pattern instead of adopting InkOS's monolithic CLI, daemon, or parallel truth-file architecture. Treat existing plans for strong quality gates, setting gate, auto-close, writing-core, and launch-stack as partial foundations, then add one integration layer that makes chapter production transactional, state-light, and recoverable.

**Tech Stack:** Markdown design and workflow docs, `SKILL.md` contracts, Python 3 standard-library scripts under `scripts/`, JSON sidecars under `.mighty/`, `unittest` tests under `tests/`, repo validation via `bash scripts/validate-migration.sh`

---

### Task 1: Lock the integrated growth boundary before writing new runtime contracts

**Files:**
- Create: `tests/test_inkos_growth_plan.py`
- Read: `docs/superpowers/plans/2026-03-23-strong-quality-gates.md`
- Read: `docs/superpowers/plans/2026-03-23-novel-write-auto-close.md`
- Read: `docs/superpowers/plans/2026-03-24-writing-core-framework.md`
- Read: `docs/superpowers/plans/2026-03-24-fanqie-launch-stack.md`
- Read: `docs/superpowers/specs/2026-03-23-strong-quality-gates-design.md`
- Read: `docs/superpowers/specs/2026-03-24-setting-gate-design.md`
- Read: `docs/superpowers/specs/2026-03-23-novel-write-auto-close-design.md`

- [ ] **Step 1: Create `tests/test_inkos_growth_plan.py` as the umbrella contract test for the new integrated lane.**
- [ ] **Step 2: Add failing assertions that require the repo to expose five new/strengthened concepts across scripts, skills, and docs:**
  - chapter transaction steps
  - active context sidecar
  - deterministic post-write prose lint
  - short-lived review guardrails
  - existing-manuscript import bridge
- [ ] **Step 3: Add failing assertions that the new lane reuses existing sources of truth instead of creating a parallel workflow engine or a second state center.**
- [ ] **Step 4: Run `python -m unittest tests.test_inkos_growth_plan -v` and confirm it fails because the new contract files, references, and scripts do not exist yet.**

Verification:
- Run: `python -m unittest tests.test_inkos_growth_plan -v`
- Expect: FAIL with missing-file or missing-token assertions for the integrated growth contract

### Task 2: Formalize chapter transactions as the main production unit

**Files:**
- Create: `shared/references/shared/chapter-transaction-schema.md`
- Create: `shared/templates/workflow-state-v2.json`
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-close/SKILL.md`
- Modify: `skills/novel-workflow/SKILL.md`
- Modify: `skills/novel-resume/SKILL.md`
- Modify: `scripts/post-task-maintenance.py`
- Modify: `scripts/project-maintenance.py`
- Modify: `docs/00-当前有效/default-workflows.md`
- Modify: `docs/00-当前有效/start-here.md`
- Modify: `docs/00-当前有效/skill-usage.md`
- Modify: `tests/test_inkos_growth_plan.py`
- Modify: `tests/test_setting_gate.py`

- [ ] **Step 1: Add failing tests that require one fixed transaction sequence for a single chapter: `gate-check -> draft -> close -> maintenance -> snapshot`.**
- [ ] **Step 2: Add failing tests that `skills/novel-workflow/SKILL.md` and `skills/novel-resume/SKILL.md` explicitly mention these step names and use them to locate the safest recovery point.**
- [ ] **Step 3: Create `shared/references/shared/chapter-transaction-schema.md` documenting the transaction phases, terminal states, and failure semantics.**
- [ ] **Step 4: Create `shared/templates/workflow-state-v2.json` with a conservative state shape that records the current transaction step, completed steps, failed steps, and the latest successful checkpoint.**
- [ ] **Step 5: Update `skills/novel-write/SKILL.md` so a successful single-chapter write is described as entering a transaction, not only producing prose.**
- [ ] **Step 6: Update `skills/novel-close/SKILL.md` so close remains the bounded convergence executor but clearly sits inside the larger transaction contract.**
- [ ] **Step 7: Update `scripts/post-task-maintenance.py` and `scripts/project-maintenance.py` so maintenance is documented and emitted as the transaction tail rather than a loosely related housekeeping script.**
- [ ] **Step 8: Update user-facing docs so the default workflow now treats the chapter transaction as the normal unit of progress.**
- [ ] **Step 9: Re-run `python -m unittest tests.test_inkos_growth_plan -v tests.test_setting_gate -v` and verify the transaction-contract assertions pass.**

Verification:
- Run: `python -m unittest tests.test_inkos_growth_plan -v`
- Expect: transaction schema, workflow template, and skill token assertions pass
- Run: `python -m unittest tests.test_setting_gate -v`
- Expect: existing gate/resume expectations still pass after workflow wording changes

### Task 3: Add an active-context sidecar and prompt-assembly contract

**Files:**
- Create: `scripts/build_active_context.py`
- Create: `tests/test_active_context.py`
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-review/SKILL.md`
- Modify: `skills/novel-status/SKILL.md`
- Modify: `skills/novel-query/SKILL.md`
- Modify: `scripts/project-maintenance.py`
- Modify: `scripts/thin-state.py`
- Modify: `docs/00-当前有效/state-thinning-and-setting-sync.md`
- Modify: `shared/references/shared/state-schema.md`
- Modify: `shared/templates/state-v5-template.json`
- Modify: `tests/test_inkos_growth_plan.py`

- [ ] **Step 1: Add failing tests for a new sidecar at `.mighty/active-context.json` that contains only current-writing inputs, not long-term canon.**
- [ ] **Step 2: Add failing tests for helper functions in `scripts/build_active_context.py`, for example:**
  - `load_state_and_sidecars`
  - `select_recent_summaries`
  - `select_active_hooks`
  - `select_relevant_entities`
  - `build_active_context`
- [ ] **Step 3: Implement `scripts/build_active_context.py` using only local project sources and existing sidecars.**
- [ ] **Step 4: Keep the sidecar intentionally narrow. It should prefer:**
  - recent chapter summaries
  - active foreshadowing
  - gate minimal next action when relevant
  - launch-stack mirrors when relevant
  - current short-lived guardrails
- [ ] **Step 5: Update `skills/novel-write/SKILL.md` and `skills/novel-review/SKILL.md` so they explicitly prefer `.mighty/active-context.json` before broad chapter/state reads when it exists.**
- [ ] **Step 6: Update `skills/novel-status/SKILL.md` and `skills/novel-query/SKILL.md` so they can explain whether the project has a fresh active context sidecar and what it summarizes.**
- [ ] **Step 7: Update `scripts/project-maintenance.py` so active-context rebuild happens after maintenance-safe state changes and before thinning/archiving.**
- [ ] **Step 8: Update `docs/00-当前有效/state-thinning-and-setting-sync.md`, `shared/references/shared/state-schema.md`, and `shared/templates/state-v5-template.json` so `active-context` is documented as a sidecar/pointer layer rather than a new truth source.**
- [ ] **Step 9: Re-run `python -m unittest tests.test_active_context -v tests.test_inkos_growth_plan -v` and verify the sidecar contract passes.**

Verification:
- Run: `python -m unittest tests.test_active_context -v`
- Expect: helper and sidecar-shape tests pass
- Run: `python3 scripts/build_active_context.py smoke/e2e-qinggan-evil`
- Expect: `.mighty/active-context.json` is created or updated with a concise current-writing payload

### Task 4: Split deterministic post-write lint from review judgment

**Files:**
- Create: `scripts/post_write_lint.py`
- Create: `tests/test_post_write_lint.py`
- Modify: `docs/strong-quality-gate-policy.json`
- Modify: `skills/novel-close/SKILL.md`
- Modify: `skills/novel-fix/SKILL.md`
- Modify: `skills/novel-review/SKILL.md`
- Modify: `docs/00-当前有效/default-workflows.md`
- Modify: `tests/test_strong_quality_gate.py`
- Modify: `tests/test_inkos_growth_plan.py`

- [ ] **Step 1: Add failing tests for deterministic prose checks that should not depend on LLM review, including:**
  - repeated AI-turn markers
  - obvious explanation-first template lines
  - long-paragraph density
  - collective-shock template lines
  - malformed repeated exact tokens
- [ ] **Step 2: Add failing tests that `docs/strong-quality-gate-policy.json` exposes only the machine-readable thresholds/patterns needed by the lint script.**
- [ ] **Step 3: Implement `scripts/post_write_lint.py` as a narrow, structured checker that returns findings by severity and category.**
- [ ] **Step 4: Keep the script read-only. It must not mutate prose.**
- [ ] **Step 5: Update `skills/novel-close/SKILL.md` so deterministic lint executes before close success is declared, but only policy-backed blockers can stop closure.**
- [ ] **Step 6: Update `skills/novel-fix/SKILL.md` so bounded local repair can explicitly consume deterministic lint findings.**
- [ ] **Step 7: Tighten `skills/novel-review/SKILL.md` wording so review remains the read-only evaluator and does not absorb deterministic lint into vague editorial commentary.**
- [ ] **Step 8: Re-run `python -m unittest tests.test_post_write_lint -v tests.test_strong_quality_gate -v` and verify lint and policy integration both pass.**

Verification:
- Run: `python -m unittest tests.test_post_write_lint -v`
- Expect: deterministic lint tests pass
- Run: `python3 scripts/post_write_lint.py smoke/e2e-qinggan-evil/chapters/第001章.md`
- Expect: JSON output with `issues`, `warnings`, and policy-backed categories only

### Task 5: Feed review outcomes back into the next chapter as short-lived guardrails

**Files:**
- Modify: `skills/novel-review/SKILL.md`
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-learn/SKILL.md`
- Modify: `skills/novel-status/SKILL.md`
- Modify: `docs/writing-core-framework/07-memory-压缩信号约定.md`
- Modify: `scripts/split-runtime-guidance.py`
- Modify: `tests/test_writing_core_smoke.py`
- Modify: `tests/test_inkos_growth_plan.py`

- [ ] **Step 1: Add failing tests for a new short-lived section in `.mighty/learned-patterns.json`, for example `recent_guardrails`.**
- [ ] **Step 2: Define the minimum contract in `docs/writing-core-framework/07-memory-压缩信号约定.md`, keeping the fields small and explicitly expiring.**
- [ ] **Step 3: Update `skills/novel-review/SKILL.md` so it can emit:**
  - `must_avoid`
  - `must_preserve`
  - `next_chapter_watchpoints`
  - `expires_after_chapter`
- [ ] **Step 4: Update `skills/novel-write/SKILL.md` so it prefers active short-lived guardrails over stale long-term style generalizations when both exist.**
- [ ] **Step 5: Update `skills/novel-learn/SKILL.md` so reference learning does not overwrite short-lived guardrails with broad style claims.**
- [ ] **Step 6: Update `scripts/split-runtime-guidance.py` so guardrails can stay sidecar-first and `state.json` remains a summary/pointer layer.**
- [ ] **Step 7: Update `skills/novel-status/SKILL.md` so full mode can surface current guardrails and their expiry clearly.**
- [ ] **Step 8: Re-run `python -m unittest tests.test_writing_core_smoke -v tests.test_inkos_growth_plan -v` and verify the guardrail contract passes.**

Verification:
- Run: `python -m unittest tests.test_writing_core_smoke -v`
- Expect: learned-pattern and sidecar tests still pass with the new guardrail layer

### Task 6: Expand reference learning without creating a parallel style subsystem

**Files:**
- Modify: `skills/novel-learn/SKILL.md`
- Modify: `scripts/acquire_source_text.py`
- Modify: `tests/test_acquire_source_text.py`
- Modify: `tests/test_writing_core_smoke.py`
- Modify: `docs/90-归档/阶段/phase-5b-p0-learn-smoke-plan.md`
- Modify: `docs/90-归档/阶段/phase-5b-p0-learn-smoke-results.md`
- Modify: `tests/test_inkos_growth_plan.py`

- [ ] **Step 1: Add failing tests that `novel-learn` explicitly supports three source classes: current-project chapters, local files, and retrievable URLs.**
- [ ] **Step 2: Keep the output contract sidecar-first. Do not add a second permanent style center such as `style_profile.json` unless a later plan explicitly requires it.**
- [ ] **Step 3: Extend `scripts/acquire_source_text.py` tests for the reference-learning path, including successful fetch, fallback behavior, and explicit failure reporting.**
- [ ] **Step 4: Update `skills/novel-learn/SKILL.md` so URL-based learning is allowed only when the source text is actually retrieved in the current environment.**
- [ ] **Step 5: Update smoke docs so the repo records concrete evidence for local-file learning and URL-based learning without pretending unsupported fetches worked.**
- [ ] **Step 6: Re-run `python -m unittest tests.test_acquire_source_text -v tests.test_writing_core_smoke -v` and verify reference-learning coverage passes.**

Verification:
- Run: `python -m unittest tests.test_acquire_source_text -v`
- Expect: retrieval-path tests pass
- Run: `python -m unittest tests.test_writing_core_smoke -v`
- Expect: learned-pattern smoke coverage still passes after source-expansion changes

### Task 7: Add an existing-manuscript import bridge that joins the current workflow safely

**Files:**
- Create: `scripts/import_existing_chapters.py`
- Create: `tests/test_import_existing_chapters.py`
- Modify: `skills/novel-resume/SKILL.md`
- Modify: `skills/novel-index/SKILL.md`
- Modify: `skills/novel-sync/SKILL.md`
- Modify: `skills/novel-query/SKILL.md`
- Modify: `docs/00-当前有效/default-workflows.md`
- Modify: `docs/00-当前有效/start-here.md`
- Modify: `docs/00-当前有效/skill-usage.md`
- Modify: `tests/test_inkos_growth_plan.py`

- [ ] **Step 1: Add failing tests for a conservative import bridge that accepts either a single text file or a chapter directory and produces an import report.**
- [ ] **Step 2: Keep v1 deliberately narrow:**
  - copy/import chapters
  - generate `.mighty/import-report.json`
  - trigger `novel-index` and gate-facing follow-up paths
  - never pretend that all canon/state truth was automatically reconstructed
- [ ] **Step 3: Implement `scripts/import_existing_chapters.py` using standard library file IO and the current chapter naming conventions.**
- [ ] **Step 4: Route ambiguities into existing review surfaces rather than a new state center:**
  - `setting gate`
  - `sync-review`
  - `novel-resume`
- [ ] **Step 5: Update `skills/novel-resume/SKILL.md`, `skills/novel-index/SKILL.md`, `skills/novel-sync/SKILL.md`, and `skills/novel-query/SKILL.md` so imported projects have a safe first recovery path.**
- [ ] **Step 6: Update entry docs so “continue an existing manuscript” becomes an explicit supported path rather than an implied workaround.**
- [ ] **Step 7: Re-run `python -m unittest tests.test_import_existing_chapters -v tests.test_inkos_growth_plan -v` and verify the import-bridge contract passes.**

Verification:
- Run: `python -m unittest tests.test_import_existing_chapters -v`
- Expect: import-report and handoff tests pass
- Run: `python3 scripts/import_existing_chapters.py smoke/e2e-qinggan-evil --from smoke/e2e-qinggan-evil/chapters`
- Expect: report JSON is produced and the command does not claim unsupported canon reconstruction

### Task 8: Add longform context compression without replacing current truth sources

**Files:**
- Create: `scripts/build_volume_summaries.py`
- Create: `tests/test_volume_summaries.py`
- Modify: `scripts/thin-state.py`
- Modify: `skills/novel-status/SKILL.md`
- Modify: `skills/novel-query/SKILL.md`
- Modify: `docs/00-当前有效/state-thinning-and-setting-sync.md`
- Modify: `tests/test_inkos_growth_plan.py`

- [ ] **Step 1: Add failing tests for a new longform summary artifact such as `.mighty/volume-summaries.json` or a similarly narrow sidecar.**
- [ ] **Step 2: Keep the contract simple: completed chapter ranges compress into volume-level summaries while recent chapter-level summaries remain live.**
- [ ] **Step 3: Implement `scripts/build_volume_summaries.py` so it reads existing chapter summaries / state-archive data and writes compressed summaries without touching prose or canon files.**
- [ ] **Step 4: Update `scripts/thin-state.py` so long projects can rebuild or refresh compressed volume context during maintenance.**
- [ ] **Step 5: Update `skills/novel-status/SKILL.md` and `skills/novel-query/SKILL.md` so they can explain when old detail is now served from volume summaries instead of live chapter rows.**
- [ ] **Step 6: Re-run `python -m unittest tests.test_volume_summaries -v tests.test_inkos_growth_plan -v` and verify the longform-compression contract passes.**

Verification:
- Run: `python -m unittest tests.test_volume_summaries -v`
- Expect: volume-summary generation and archive-integrity tests pass

### Task 9: Run integrated verification and record residual risks

**Files:**
- Modify: `progress.md` only if a local planning workflow is active
- Modify: `docs/90-归档/阶段/phase-*.md` only if the repo needs a durable project-history note for landed growth facts

- [ ] **Step 1: Run the full targeted verification set once the lane is implemented:**
  - `python -m unittest tests.test_inkos_growth_plan -v`
  - `python -m unittest tests.test_setting_gate -v`
  - `python -m unittest tests.test_strong_quality_gate -v`
  - `python -m unittest tests.test_active_context -v`
  - `python -m unittest tests.test_post_write_lint -v`
  - `python -m unittest tests.test_writing_core_smoke -v`
  - `python -m unittest tests.test_acquire_source_text -v`
  - `python -m unittest tests.test_import_existing_chapters -v`
  - `python -m unittest tests.test_volume_summaries -v`
- [ ] **Step 2: Run `bash scripts/validate-migration.sh` and confirm no repo-integrity regressions.**
- [ ] **Step 3: Run one direct CLI/script sanity pass for each new executable:**
  - `python3 scripts/build_active_context.py <sample_project>`
  - `python3 scripts/post_write_lint.py <sample_chapter>`
  - `python3 scripts/import_existing_chapters.py <sample_project> --from <sample_source>`
  - `python3 scripts/build_volume_summaries.py <sample_project>`
- [ ] **Step 4: Record residual risks explicitly instead of papering over them, especially:**
  - deterministic lint false positives
  - imported-manuscript canon ambiguity
  - active-context freshness drift
  - longform compression losing niche retrieval details
- [ ] **Step 5: If the lane lands as a durable repo fact, add the smallest necessary release/history note rather than scattering duplicate explanations across many docs.**

Verification:
- Run: `bash scripts/validate-migration.sh`
- Expect: migration validation still passes after adding scripts, tests, skill contract updates, and sidecar docs
- Run: `python -m unittest tests.test_inkos_growth_plan -v`
- Expect: integrated growth contract passes end-to-end
