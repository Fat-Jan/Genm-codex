# Fanqie Launch Stack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-version Fanqie launch-stack layer that turns the approved spec into repo-local docs, a conservative compiler CLI, lightweight sidecar/state contracts, and minimal skill wiring for `outline / write / review / precheck / package`.

**Architecture:** Keep the single source of truth in `docs/opening-and-plot-framework/fanqie-launch-stack/`, not in `state`. Add one small Python CLI under `scripts/` that infers a conservative `launch_stack` draft from project state, outline, and early chapters, then only writes `.mighty/launch-stack.json` and light state mirrors when explicitly requested. Reuse existing framework patterns: contract tests lock docs and skill references first, the CLI stays local-only and conflict-averse, and real-project evidence is generated from existing sample projects instead of inventing fake fixtures.

**Tech Stack:** Markdown framework docs, Python 3 standard library CLI under `scripts/`, `unittest` regression tests under `tests/`, repo-local `.mighty/` sidecars and `state.json` mirrors

---

### Task 1: Lock the launch-stack contract with failing tests

**Files:**
- Create: `tests/test_fanqie_launch_stack.py`
- Reference: `docs/90-归档/superpowers/specs/2026-03-24-fanqie-launch-stack-design.md`
- Reference: `tests/test_opening_plot_framework.py`
- Reference: `tests/test_writing_core_framework.py`

- [ ] **Step 1: Create `tests/test_fanqie_launch_stack.py` with the same repo-root helper pattern used by the existing framework contract tests.**
- [ ] **Step 2: Add failing assertions that require the launch-stack doc tree to exist under `docs/opening-and-plot-framework/fanqie-launch-stack/`.**
- [ ] **Step 3: Add failing assertions that require a new CLI script at `scripts/fanqie_launch_stack.py`.**
- [ ] **Step 4: Add failing assertions that require `skills/novel-outline/SKILL.md`, `skills/novel-write/SKILL.md`, `skills/novel-review/SKILL.md`, `skills/novel-precheck/SKILL.md`, and `skills/novel-package/SKILL.md` to mention the launch-stack docs or `.mighty/launch-stack.json`.**
- [ ] **Step 5: Add failing assertions that require `shared/references/shared/state-schema.md` and `shared/templates/state-v5-template.json` to mention the four light mirrors: `active_launch_grammar`, `active_primary_pivot`, `launch_stack_phase`, `launch_stack_drift_signal`.**
- [ ] **Step 6: Run `python -m unittest tests.test_fanqie_launch_stack -v` and confirm it fails because the files, tokens, and script do not exist yet.**

Verification:
- Run: `python -m unittest tests.test_fanqie_launch_stack -v`
- Expect: FAIL with missing-file or missing-token assertions that name the launch-stack paths directly

### Task 2: Create the launch-stack doc tree as the single source of truth

**Files:**
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/01-premise-layer.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/02-pivot-layer.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/03-launch-grammar-layer.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/04-retention-protocol-layer.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/05-compiler-contract.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/README.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/oppression-breakout.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/bonding-reversal.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/rule-trial.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/resource-climb.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/investigation-reveal.md`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/ensemble-return.md`
- Modify: `tests/test_fanqie_launch_stack.py`

- [ ] **Step 1: Implement the README and five layer docs so they clearly define `premise`, `pivot`, `launch grammar`, `retention protocol`, and `compiler output`, without drifting into a full-book theory dump.**
- [ ] **Step 2: Add the six launch-grammar cards with one consistent field shape: `best_for`, `not_for`, `reader_promise`, `chapter_1_3_minimums`, `scene_engine`, `review_watchpoints`, `precheck_failures`, and `package_guardrails`.**
- [ ] **Step 3: Keep `Genre Obligations` and full ledger automation out of v1; the docs should explicitly mark them as later extensions, not partial half-implementations.**
- [ ] **Step 4: Re-run `python -m unittest tests.test_fanqie_launch_stack -v` and verify the doc-tree existence assertions now pass while script/skill/state assertions still fail.**

Verification:
- Run: `python -m unittest tests.test_fanqie_launch_stack -v`
- Expect: doc existence tests pass; CLI, skill wiring, and state-contract tests still fail

### Task 3: Implement the conservative launch-stack compiler CLI in read-only draft mode

**Files:**
- Create: `scripts/fanqie_launch_stack.py`
- Modify: `tests/test_fanqie_launch_stack.py`
- Reference: `docs/90-归档/superpowers/specs/2026-03-24-fanqie-launch-stack-design.md`
- Reference: `docs/opening-and-plot-framework/fanqie-launch-stack/05-compiler-contract.md`

- [ ] **Step 1: Add failing helper tests for `load_state(project_root)`, `load_total_outline(project_root)`, `load_chapter_texts(project_root, chapters)`, `infer_pivot_candidates(...)`, `infer_launch_grammar_candidates(...)`, and `compile_launch_stack(...)`.**
- [ ] **Step 2: Add a failing CLI-contract test that default mode is `draft`, requires `--project-root`, and can accept `--chapter`, `--chapters`, and `--output`.**
- [ ] **Step 3: Implement the minimal CLI using only the standard library; keep it local-only and deterministic.**
- [ ] **Step 4: Keep inference intentionally conservative: when title, bucket, outline, or chapter evidence is too weak, downgrade confidence or leave only candidates instead of faking certainty.**
- [ ] **Step 5: Make `draft` mode emit a JSON object matching the compiler contract, either to stdout or to an explicit output path.**
- [ ] **Step 6: Re-run `python -m unittest tests.test_fanqie_launch_stack -v` and verify helper and draft-mode tests pass.**

Verification:
- Run: `python3 scripts/fanqie_launch_stack.py --project-root "projects/离婚冷静期那天，前夫把董事会席位押给了我" --chapter 003 --chapters 001-003`
- Expect: JSON output with `premise_line`, `primary_pivot`, `launch_grammar`, `retention_protocol`, `compiler_output`, and a non-empty `confidence`

### Task 4: Add guarded writeback for `.mighty/launch-stack.json` and light state mirrors

**Files:**
- Modify: `scripts/fanqie_launch_stack.py`
- Modify: `tests/test_fanqie_launch_stack.py`
- Reference: `shared/references/shared/state-schema.md`

- [ ] **Step 1: Add failing tests that writeback is blocked unless an explicit write flag is present.**
- [ ] **Step 2: Add failing tests that successful writeback creates or updates `.mighty/launch-stack.json` and mirrors only `active_launch_grammar`, `active_primary_pivot`, `launch_stack_phase`, and `launch_stack_drift_signal` into `state.json`.**
- [ ] **Step 3: Add a failing test that unrelated `chapter_meta`, `review_score`, and bucket summary fields remain untouched.**
- [ ] **Step 4: Add a failing test that existing `.mighty/launch-stack.json` is not overwritten silently without an explicit override flag.**
- [ ] **Step 5: Implement guarded writeback logic in `scripts/fanqie_launch_stack.py`.**
- [ ] **Step 6: Initialize empty placeholder files for `.mighty/hook-ledger.json` and `.mighty/payoff-ledger.json` only when writeback is explicitly requested and the files do not already exist.**
- [ ] **Step 7: Re-run `python -m unittest tests.test_fanqie_launch_stack -v` and verify writeback tests pass.**

Verification:
- Run: `python3 scripts/fanqie_launch_stack.py --project-root "<temp_project>" --chapter 003 --chapters 001-003 --mode writeback --writeback`
- Expect: `.mighty/launch-stack.json` is created, `state.json` gets only the four light mirror keys, and placeholder ledger files are created if absent

### Task 5: Wire the launch-stack into the five core writing skills

**Files:**
- Modify: `skills/novel-outline/SKILL.md`
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-review/SKILL.md`
- Modify: `skills/novel-precheck/SKILL.md`
- Modify: `skills/novel-package/SKILL.md`
- Modify: `tests/test_fanqie_launch_stack.py`

- [ ] **Step 1: Add failing token tests that `novel-outline` reads the launch-stack README and compiler contract, plus `.mighty/launch-stack.json` when it exists.**
- [ ] **Step 2: Add failing token tests that `novel-write` consumes `retention_protocol` and `chapter_1_3_targets` rather than re-explaining the docs inline.**
- [ ] **Step 3: Add failing token tests that `novel-review` and `novel-precheck` mention `launch_alignment`, `drift_signal`, or equivalent launch-stack watchpoints.**
- [ ] **Step 4: Add failing token tests that `novel-package` reads `package_guardrails` from the launch-stack compiler output.**
- [ ] **Step 5: Update the five skill contracts to reference the new docs and sidecar conservatively, without inventing a hidden orchestrator.**
- [ ] **Step 6: Re-run `python -m unittest tests.test_fanqie_launch_stack -v` and verify the skill-wiring assertions pass.**

Verification:
- Run: `python -m unittest tests.test_fanqie_launch_stack -v`
- Expect: skill-reference assertions for all five target skills pass

### Task 6: Extend the state and initialization contract without creating a second rules center

**Files:**
- Modify: `shared/references/shared/state-schema.md`
- Modify: `shared/templates/state-v5-template.json`
- Modify: `skills/novel-init/SKILL.md`
- Modify: `docs/00-当前有效/state-thinning-and-setting-sync.md`
- Modify: `tests/test_fanqie_launch_stack.py`

- [ ] **Step 1: Add failing token tests that `state-schema.md` documents the four light launch-stack mirror fields and points detailed storage to `.mighty/launch-stack.json`.**
- [ ] **Step 2: Add failing tests that `state-v5-template.json` contains the four launch-stack mirror keys in the correct place.**
- [ ] **Step 3: Add failing token tests that `novel-init` and `docs/00-当前有效/state-thinning-and-setting-sync.md` mention the launch-stack sidecar as a sidecar/pointer-style contract, not a large state payload.**
- [ ] **Step 4: Update the schema, template, and docs to match the spec.**
- [ ] **Step 5: Re-run `python -m unittest tests.test_fanqie_launch_stack -v` and confirm the state-contract assertions pass.**

Verification:
- Run: `python -m unittest tests.test_fanqie_launch_stack -v`
- Expect: schema/template/init-doc assertions pass without regressions

### Task 7: Expose the new layer in framework and entry docs

**Files:**
- Modify: `docs/opening-and-plot-framework/README.md`
- Modify: `README.md`
- Modify: `docs/00-当前有效/start-here.md`
- Modify: `docs/00-当前有效/skill-usage.md`
- Modify: `docs/00-当前有效/default-workflows.md`
- Modify: `tests/test_fanqie_launch_stack.py`

- [ ] **Step 1: Add failing token tests that the framework README and project entry docs mention `fanqie-launch-stack`.**
- [ ] **Step 2: Update `docs/opening-and-plot-framework/README.md` to point readers to the new launch-stack docs and explain that this layer precedes bucket-specific overlays.**
- [ ] **Step 3: Update `README.md`, `docs/00-当前有效/start-here.md`, `docs/00-当前有效/skill-usage.md`, and `docs/00-当前有效/default-workflows.md` so the new layer is discoverable from normal project entry points.**
- [ ] **Step 4: Re-run `python -m unittest tests.test_fanqie_launch_stack -v` and confirm the entry-doc assertions pass.**

Verification:
- Run: `python -m unittest tests.test_fanqie_launch_stack -v`
- Expect: framework and entry-doc assertions pass

### Task 8: Generate real-project evidence and run final verification

**Files:**
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.json`
- Create: `docs/opening-and-plot-framework/fanqie-launch-stack-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.json`
- Modify: `tests/test_fanqie_launch_stack.py`
- Modify: `progress.md`

- [ ] **Step 1: Add failing tests that require two real-project smoke artifacts, one relation-forward and one resource-forward.**
- [ ] **Step 2: Run the new CLI in read-only `draft` mode on the two sample projects and save the JSON outputs under `docs/opening-and-plot-framework/`.**
- [ ] **Step 3: Add assertions that the smoke artifacts contain non-empty `primary_pivot`, `launch_grammar`, and `compiler_output`.**
- [ ] **Step 4: Run the full verification set:**
  - `python -m unittest tests.test_fanqie_launch_stack -v`
  - `python -m unittest tests.test_opening_plot_framework -v`
  - `python -m unittest tests.test_writing_core_framework -v`
  - `bash scripts/validate-migration.sh`
- [ ] **Step 5: Record implementation outcomes, sample evidence, and residual risks in `progress.md`.**

Verification:
- Run: `python -m unittest tests.test_fanqie_launch_stack -v`
- Expect: all launch-stack contract tests pass
- Run: `python -m unittest tests.test_opening_plot_framework -v`
- Expect: existing opening-and-plot framework regressions still pass
- Run: `python -m unittest tests.test_writing_core_framework -v`
- Expect: writing-core framework regressions still pass
- Run: `bash scripts/validate-migration.sh`
- Expect: migration validation still passes after docs, script, skill, and state-contract updates
