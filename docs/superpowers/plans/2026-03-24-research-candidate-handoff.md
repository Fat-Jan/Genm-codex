# Research Candidate Handoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one minimal research-candidate handoff path so external scan results can be passed into `setting gate` as reviewable candidates without becoming canon.

**Architecture:** Keep the current local-first workflow intact. `novel_scan.py` will optionally emit `.mighty/research-candidates.json`, and `setting_gate.py` will optionally ingest that file through a new CLI/loader path and route candidates into the existing `grade_candidates -> sync-review -> setting-gate.json` closure.

**Tech Stack:** Python 3, `unittest`, JSON sidecar files, existing project scripts under `scripts/`

---

### Task 1: Lock Setting Gate Candidate-File Behavior

**Files:**
- Modify: `tests/test_setting_gate.py`
- Modify: `scripts/setting_gate.py`
- Test: `tests/test_setting_gate.py`

- [ ] **Step 1: Write the failing tests**

Add tests for:
- loading candidates from a JSON file through a helper
- CLI `--candidates-file` writing review items into `.mighty/setting-gate.json`

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_setting_gate -v`
Expected: FAIL because candidate-file support does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Add:
- `--candidates-file` CLI argument
- helper to read `{"candidates": [...]}` payloads
- pass loaded candidates into existing `run_gate(..., mcp_candidates=...)`

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_setting_gate -v`
Expected: PASS

### Task 2: Lock Novel Scan Candidate Emission

**Files:**
- Modify: `tests/test_novel_scan.py`
- Modify: `scripts/novel_scan.py`
- Test: `tests/test_novel_scan.py`

- [ ] **Step 1: Write the failing tests**

Add tests for:
- optional candidate sidecar emission
- no emission on low-confidence or non-truth findings

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_novel_scan -v`
Expected: FAIL because scan does not emit research candidate files yet.

- [ ] **Step 3: Write minimal implementation**

Add:
- optional `emit_research_candidates` / `research_candidates_file` support
- candidate builder that only emits conservative truth-gap candidates
- sidecar write/remove behavior under `.mighty/research-candidates.json`

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_novel_scan -v`
Expected: PASS

### Task 3: Document the New Optional Handoff

**Files:**
- Modify: `docs/skill-usage.md`
- Modify: `docs/default-workflows.md`
- Modify: `skills/novel-scan/SKILL.md`

- [ ] **Step 1: Update docs**

Document:
- candidate sidecar file path
- optional handoff command shape
- explicit boundary: candidate only, not canon

- [ ] **Step 2: Verify references**

Run: `rg -n "research-candidates|candidates-file|setting gate" docs skills`
Expected: relevant docs and skill contract mention the new optional path.

### Task 4: Full Verification

**Files:**
- Test: `tests/test_setting_gate.py`
- Test: `tests/test_novel_scan.py`
- Test: `tests/test_acquire_source_text.py`

- [ ] **Step 1: Run focused regression**

Run: `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`
Expected: PASS

- [ ] **Step 2: Record any residual limits**

Confirm final messaging keeps these boundaries:
- no direct canon writes
- no default workflow change
- no shared asset writes
