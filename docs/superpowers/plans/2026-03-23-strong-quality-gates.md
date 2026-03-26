# Strong Quality Gates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为现有小说工作流落地强拦截质量门，在写前阻断资料不充分写作、在收口前阻断客观质量失败、并阻止脏实体继续沉淀进 `设定集/`。

**Architecture:** 以 `docs/strong-quality-gate-policy.json` 作为单一规则源，新建一个可复用的 Python gate helper 模块，供 `check-batch-quality-gate.py`、`sync-setting-assets.py` 和后续 workflow 验证逻辑共享。技能文档只声明拦截点和失败语义，不重复定义规则；测试以 `unittest` 为主，先锁规则解析与 blocker 语义，再补脚本接线和 smoke。

**Tech Stack:** Markdown skill specs, JSON policy file, Python 3 standard library scripts under `scripts/`, `unittest` tests under `tests/`

---

### Task 1: Define the strong-gate policy contract

**Files:**
- Create: `docs/strong-quality-gate-policy.json`
- Create: `tests/test_strong_quality_gate.py`
- Reference: `docs/fanqie-chapter-length-policy.json`
- Reference: `docs/superpowers/specs/2026-03-23-strong-quality-gates-design.md`

- [ ] Step 1: Write failing tests for policy loading, bucket threshold resolution, truth-source mapping, and sync rejection pattern access in `tests/test_strong_quality_gate.py`.
- [ ] Step 2: Run `python3 -m unittest tests.test_strong_quality_gate -v` and verify the new tests fail because the policy file or loader contract does not exist yet.
- [ ] Step 3: Create `docs/strong-quality-gate-policy.json` with only v1 hard-gate data:
  - bucket-aware `hard_min_chars`, `soft_min_chars`, and shrinkage thresholds
  - pre-write required source mappings for kinship truth, office truth, and world-rule support
  - conservative malformed-text blocker thresholds
  - sync candidate rejection patterns / stopwords / phrase-fragment rules
- [ ] Step 4: Re-run `python3 -m unittest tests.test_strong_quality_gate -v` and verify the policy-focused tests pass.

Verification:
- Run: `python3 -m json.tool docs/strong-quality-gate-policy.json >/dev/null`
- Expect: exits successfully with no JSON parse error
- Run: `python3 -m unittest tests.test_strong_quality_gate -v`
- Expect: policy-loading tests pass and name the new strong-gate policy contract explicitly

### Task 2: Build a reusable gate helper module

**Files:**
- Create: `scripts/strong_quality_gate.py`
- Modify: `tests/test_strong_quality_gate.py`

- [ ] Step 1: Extend `tests/test_strong_quality_gate.py` with failing tests for helper functions:
  - `load_policy`
  - `resolve_length_policy`
  - `detect_missing_truth_sources`
  - `evaluate_post_write_gate`
  - `classify_sync_candidate`
- [ ] Step 2: Run `python3 -m unittest tests.test_strong_quality_gate -v` and verify helper tests fail with missing-module or missing-symbol errors.
- [ ] Step 3: Implement `scripts/strong_quality_gate.py` as the shared gate library with small pure functions that accept text / state / policy inputs and return structured dict results instead of printing.
- [ ] Step 4: Keep the module narrow:
  - no direct CLI entry point in v1
  - no project-wide editor behavior
  - no automatic network research
- [ ] Step 5: Re-run `python3 -m unittest tests.test_strong_quality_gate -v` and verify all helper-level tests pass.

Verification:
- Run: `python3 -m unittest tests.test_strong_quality_gate -v`
- Expect: helper tests pass for policy resolution, missing-source detection, post-write hard-block evaluation, and sync candidate classification

### Task 3: Upgrade the batch quality gate into the shared hard-block path

**Files:**
- Modify: `scripts/check-batch-quality-gate.py`
- Modify: `tests/test_strong_quality_gate.py`
- Reference: `docs/fanqie-chapter-length-policy.json`

- [ ] Step 1: Add failing tests that prove `scripts/check-batch-quality-gate.py` now resolves thresholds through `scripts/strong_quality_gate.py` instead of duplicating its own length-rule semantics.
- [ ] Step 2: Add failing tests for:
  - hard-min short chapter failure
  - abnormal shrinkage failure against recent baseline
  - normal shorter-but-valid chapter pass
  - malformed repeated-token hard block
- [ ] Step 3: Run `python3 -m unittest tests.test_strong_quality_gate -v` and verify the script-integration tests fail before the refactor.
- [ ] Step 4: Refactor `scripts/check-batch-quality-gate.py` to import the shared helper module, preserve the current CLI shape, and add the new v1 hard-block signals without inventing a second policy format.
- [ ] Step 5: Re-run `python3 -m unittest tests.test_strong_quality_gate -v` and verify both old batch behavior and new hard-block semantics pass.

Verification:
- Run: `python3 scripts/check-batch-quality-gate.py smoke/e2e-gongdou-evil-antiflattening-20260322 --last-n 3`
- Expect: JSON output still includes `status`, `issues`, `warnings`, and resolved length policy fields
- Run: `python3 -m unittest tests.test_strong_quality_gate -v`
- Expect: batch-gate integration tests pass with shared helper usage

### Task 4: Add sync-pollution rejection and queue-first behavior

**Files:**
- Modify: `scripts/sync-setting-assets.py`
- Modify: `tests/test_strong_quality_gate.py`
- Reference: `projects/庶女谋略/设定集/角色/张纸.md`
- Reference: `projects/庶女谋略/设定集/角色/白褙子.md`

- [ ] Step 1: Add failing tests for sync candidate rejection cases:
  - phrase fragment should go to review queue
  - garment/object/location phrases should not materialize as characters
  - explicit overrides can alias or ignore a candidate
  - repeated valid personal names still materialize
- [ ] Step 2: Run `python3 -m unittest tests.test_strong_quality_gate -v` and verify the sync-pollution tests fail before implementation.
- [ ] Step 3: Update `scripts/sync-setting-assets.py` to use the shared helper module before writing character files:
  - reject low-confidence candidates
  - preserve accepted stable entities
  - write rejected candidates into `.mighty/sync-review.json` with explicit reasons
- [ ] Step 4: Keep the v1 scope tight:
  - do not auto-delete existing polluted cards
  - do not redesign every extraction heuristic
  - do not bypass `sync-overrides`
- [ ] Step 5: Re-run `python3 -m unittest tests.test_strong_quality_gate -v` and verify queue-first behavior is enforced.

Verification:
- Run: `python3 scripts/sync-setting-assets.py projects/庶女谋略 --mode characters --recent-chapters 8`
- Expect: output lists a `review_queue` path and does not newly materialize obviously bad character names
- Run: `python3 -m unittest tests.test_strong_quality_gate -v`
- Expect: sync-pollution tests pass, including alias/ignore override cases

### Task 5: Wire strong-gate semantics into skill contracts

**Files:**
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-close/SKILL.md`
- Modify: `skills/novel-review/SKILL.md`
- Modify: `skills/novel-precheck/SKILL.md`
- Modify: `docs/00-当前有效/default-workflows.md`
- Modify: `docs/00-当前有效/skill-usage.md`

- [ ] Step 1: Update `skills/novel-write/SKILL.md` so the workflow explicitly loads the strong-gate policy and blocks drafting when required truth sources are missing.
- [ ] Step 2: Update `skills/novel-close/SKILL.md` so close success is impossible when post-write hard blockers remain; route to `novel-fix` or `novel-rewrite` instead.
- [ ] Step 3: Tighten `skills/novel-review/SKILL.md` and `skills/novel-precheck/SKILL.md` wording so they stay consistent with the new hard-block semantics without duplicating rule tables.
- [ ] Step 4: Update `docs/00-当前有效/default-workflows.md` and `docs/00-当前有效/skill-usage.md` to expose the new write-before-truth and close-before-pass expectations as project facts.
- [ ] Step 5: Re-read the modified docs together and remove any duplicated thresholds or contradictory wording.

Verification:
- Run: `rg -n "strong-quality-gate|quality_gate|blocked|truth source|sync-review" skills docs`
- Expect: skill/docs references point to one policy and clearly describe block-vs-warning semantics

### Task 6: Add focused smoke coverage and final verification

**Files:**
- Modify: `tests/test_strong_quality_gate.py`
- Create or Modify: `docs/90-归档/阶段/phase-*.md` only if new project facts require phase-history entry
- Optional smoke workspace: temporary test project under `tmp` / test fixtures only if needed

- [ ] Step 1: Add one end-to-end style unittest flow or fixture-backed smoke that covers:
  - missing truth-sheet blocks write-preflight
  - hard-min short chapter blocks close gate
  - polluted sync candidate goes to review queue
- [ ] Step 2: Run the full targeted test set:
  - `python3 -m unittest tests.test_strong_quality_gate -v`
  - `python3 -m unittest tests.test_novel_scan -v`
  - `python3 -m unittest tests.test_acquire_source_text -v`
- [ ] Step 3: Run lightweight repository verification:
  - `bash scripts/validate-migration.sh`
  - one direct invocation of `scripts/check-batch-quality-gate.py`
  - one direct invocation of `scripts/sync-setting-assets.py` against a safe sample project
- [ ] Step 4: If docs gained a new durable workflow fact, add the smallest necessary project-history note instead of scattering the same fact across multiple files.
- [ ] Step 5: Summarize residual risks that remain intentionally out of scope:
  - perfect proofreading
  - global canon reasoning
  - auto-cleaning existing polluted setting files

Verification:
- Run: `python3 -m unittest tests.test_strong_quality_gate -v`
- Expect: all strong-gate tests pass
- Run: `bash scripts/validate-migration.sh`
- Expect: migration validation still passes after skill/doc updates
- Run: `python3 scripts/check-batch-quality-gate.py smoke/e2e-gongdou-evil-antiflattening-20260322 --last-n 3`
- Expect: script runs successfully using the shared policy path
- Run: `python3 scripts/sync-setting-assets.py smoke/e2e-gongdou-evil-antiflattening-20260322 --mode characters --recent-chapters 8`
- Expect: script completes and emits a review queue path without crashing
