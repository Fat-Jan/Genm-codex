# Fanqie P0 Smoke Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a conservative `scripts/fanqie_p0_smoke.py` tool that can scaffold a smoke document, generate bucket-summary drafts, and only write back lightweight bucket fields when explicitly requested.

**Architecture:** Build one small Python CLI under `scripts/` with three modes: `scaffold`, `draft`, and `writeback`. Reuse the existing `fanqie-p0-smoke-template.md`, `fanqie-p0-output-contract.md`, real-project smoke examples, and `.mighty/state.json` shape instead of inventing a second contract. Keep v1 local-only, single-bucket, and conflict-averse: if evidence is insufficient or bucket resolution is ambiguous, the tool must degrade to scaffold-only instead of pretending it can judge confidently.

**Tech Stack:** Python 3 standard library CLI script, repo-local Markdown templates under `docs/opening-and-plot-framework/`, `unittest` tests under `tests/`

---

### Task 1: Lock the CLI contract with failing tests

**Files:**
- Create: `tests/test_fanqie_p0_smoke.py`
- Reference: `docs/superpowers/specs/2026-03-23-fanqie-p0-smoke-tool-design.md`
- Reference: `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`

- [ ] **Step 1: Create `tests/test_fanqie_p0_smoke.py` with a `load_module()` helper for `scripts/fanqie_p0_smoke.py`.**
- [ ] **Step 2: Write failing tests for the CLI contract:**
  - default mode resolves to `draft`
  - explicit `--mode scaffold|draft|writeback` parses correctly
  - bucket inference prefers `genre_profile.bucket`, then `meta.genre`
  - unsupported or ambiguous bucket degrades to scaffold-only
  - `--writeback` is required before any state mutation is allowed
- [ ] **Step 3: Run `python -m unittest tests.test_fanqie_p0_smoke -v` and verify it fails because the script/module does not exist yet.**

Verification:
- Run: `python -m unittest tests.test_fanqie_p0_smoke -v`
- Expect: missing-module or missing-symbol failures that name `fanqie_p0_smoke.py`

### Task 2: Implement read-only project loading and path helpers

**Files:**
- Create: `scripts/fanqie_p0_smoke.py`
- Modify: `tests/test_fanqie_p0_smoke.py`

- [ ] **Step 1: Add failing tests for helper functions:**
  - `load_state(project_root)`
  - `infer_bucket(state, explicit_bucket=None)`
  - `normalize_chapter_key(chapter)`
  - `slugify_project_title(title)`
  - `default_output_path(project_root, title, date_str)`
- [ ] **Step 2: Run `python -m unittest tests.test_fanqie_p0_smoke -v` and verify helper-level tests fail before implementation.**
- [ ] **Step 3: Implement the minimal helpers in `scripts/fanqie_p0_smoke.py` using only the standard library.**
- [ ] **Step 4: Keep the helpers narrow:**
  - no network access
  - no market-scan pulling
  - no prose mutation
  - no implicit writeback
- [ ] **Step 5: Re-run `python -m unittest tests.test_fanqie_p0_smoke -v` and verify helper tests pass.**

Verification:
- Run: `python -m unittest tests.test_fanqie_p0_smoke -v`
- Expect: parsing, bucket inference, chapter normalization, and output-path tests pass

### Task 3: Implement `scaffold` mode using the smoke template shape

**Files:**
- Modify: `scripts/fanqie_p0_smoke.py`
- Modify: `tests/test_fanqie_p0_smoke.py`
- Reference: `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`

- [ ] **Step 1: Add failing tests that `scaffold` mode writes a markdown file with:**
  - project path and title
  - resolved bucket
  - chapter / chapter-range placeholders
  - `novel-review` sample block
  - `novel-precheck` sample block
  - final conclusion block
- [ ] **Step 2: Add a failing test that scaffold output for an unsupported bucket still writes a skeleton and includes an explicit degrade note.**
- [ ] **Step 3: Run `python -m unittest tests.test_fanqie_p0_smoke -v` and verify scaffold tests fail before implementation.**
- [ ] **Step 4: Implement markdown rendering for scaffold mode directly in `scripts/fanqie_p0_smoke.py`, reusing the existing template headings rather than parsing markdown templates dynamically in v1.**
- [ ] **Step 5: Re-run `python -m unittest tests.test_fanqie_p0_smoke -v` and verify scaffold output tests pass.**

Verification:
- Run: `python3 scripts/fanqie_p0_smoke.py --project-root "projects/庶女谋略" --chapter 003 --chapters 001-003 --mode scaffold`
- Expect: prints output path and writes a markdown smoke file with empty/draft sample blocks only

### Task 4: Implement conservative `draft` generation

**Files:**
- Modify: `scripts/fanqie_p0_smoke.py`
- Modify: `tests/test_fanqie_p0_smoke.py`
- Reference: `docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
- Reference: `docs/opening-and-plot-framework/real-project-smoke-shunvmoulue-fanqie-p0-2026-03-23.md`
- Reference: `docs/opening-and-plot-framework/real-project-smoke-hunshu-taizi-fanqie-p0-2026-03-23.md`

- [ ] **Step 1: Add failing tests for `draft` mode that prove:**
  - when bucket is `宫斗宅斗` and chapter/chapters exist, the output includes non-empty `fanqie_bucket_review_summary` and `fanqie_bucket_precheck_summary`
  - the output is marked as `draft` / `需人工确认`
  - evidence references cite the exact chapter files used
  - when evidence is insufficient, the tool downgrades to scaffold-only and states why
- [ ] **Step 2: Keep v1 draft heuristics intentionally narrow:**
  - support `宫斗宅斗` strongly first
  - for other P0 buckets, fill bucket identity plus draft placeholders or downgrade when evidence is too weak
  - do not fabricate confident `pass/warn/fail` without minimally sufficient chapter evidence
- [ ] **Step 3: Implement summary drafting helpers that produce small dicts matching the output contract, not free-form prose blobs.**
- [ ] **Step 4: Re-run `python -m unittest tests.test_fanqie_p0_smoke -v` and verify draft-mode tests pass.**

Verification:
- Run: `python3 scripts/fanqie_p0_smoke.py --project-root "projects/庶女谋略" --chapter 003 --chapters 001-003`
- Expect: default `draft` output file contains `fanqie_bucket_review_summary` and `fanqie_bucket_precheck_summary`, each explicitly marked as draft-oriented
- Run: `python3 scripts/fanqie_p0_smoke.py --project-root "projects/庶妹换我婚书那夜，太子先开了口" --chapter 003 --chapters 001-003`
- Expect: second smoke file is generated successfully and reflects the same bucket with project-specific evidence references

### Task 5: Implement guarded `writeback`

**Files:**
- Modify: `scripts/fanqie_p0_smoke.py`
- Modify: `tests/test_fanqie_p0_smoke.py`
- Reference: `shared/references/shared/state-schema.md`

- [ ] **Step 1: Add failing tests for writeback behavior:**
  - `writeback` mode requires an explicit flag
  - only `fanqie_bucket_flags` and `fanqie_bucket_summary` are written
  - existing `review_score`, `review_grade`, and `recommended_next_action` remain untouched
  - when the target chapter already has `fanqie_bucket_summary`, the tool reports a conflict and does not overwrite by default
- [ ] **Step 2: Run `python -m unittest tests.test_fanqie_p0_smoke -v` and verify writeback tests fail before implementation.**
- [ ] **Step 3: Implement state mutation narrowly:**
  - create `chapter_meta[N]` only when the chapter key is absent
  - write only the two bucket fields
  - refresh `meta.updated_at`
  - preserve all unrelated keys exactly
- [ ] **Step 4: Re-run `python -m unittest tests.test_fanqie_p0_smoke -v` and verify writeback tests pass.**

Verification:
- Run: `python3 scripts/fanqie_p0_smoke.py --project-root "projects/庶妹换我婚书那夜，太子先开了口" --chapter 003 --chapters 001-003 --mode writeback --writeback`
- Expect: state writes only `fanqie_bucket_flags` and `fanqie_bucket_summary` under `chapter_meta["003"]`, or reports a conflict if already present

### Task 6: Wire minimal discoverability and final verification

**Files:**
- Modify: `docs/opening-and-plot-framework/README.md`
- Modify: `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`
- Modify: `progress.md`
- Optional Modify: `tests/test_opening_plot_framework.py` only if the new script or docs require a stable discovery assertion

- [ ] **Step 1: Add a small README note showing how to invoke `scripts/fanqie_p0_smoke.py` in `scaffold`, `draft`, and `writeback` modes.**
- [ ] **Step 2: Add a short note in `fanqie-p0-smoke-template.md` that the new script can generate this structure.**
- [ ] **Step 3: Re-run the full targeted verification set:**
  - `python -m unittest tests.test_fanqie_p0_smoke -v`
  - `python -m unittest tests.test_opening_plot_framework -v`
  - `bash scripts/validate-migration.sh`
- [ ] **Step 4: Log the implementation and residual risks in `progress.md`.**

Verification:
- Run: `python -m unittest tests.test_fanqie_p0_smoke -v`
- Expect: all smoke-tool tests pass
- Run: `python -m unittest tests.test_opening_plot_framework -v`
- Expect: framework regression tests still pass
- Run: `bash scripts/validate-migration.sh`
- Expect: migration validation still passes after script + docs updates
