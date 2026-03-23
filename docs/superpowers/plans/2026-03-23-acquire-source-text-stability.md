# Acquire Source Text Stability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a stable report-only article acquisition helper that tries `fetch MCP`, falls back to direct HTML extraction, and always returns a structured result instead of blocking research flows.

**Architecture:** Add a standalone Python helper under `scripts/` with a deterministic stage pipeline and a small persisted domain-policy cache. Keep external providers pluggable through command hooks so the repo does not hard-code one MCP/server implementation. Lock the behavior with unit tests before implementation and expose a CLI for downstream scripts or manual use.

**Tech Stack:** Python standard library (`argparse`, `dataclasses`, `html.parser`, `json`, `subprocess`, `urllib`, `unittest`)

---

### Task 1: Lock result shape and pipeline behavior with tests

**Files:**
- Create: `tests/test_acquire_source_text.py`
- Test: `tests/test_acquire_source_text.py`

- [ ] **Step 1: Write failing tests for the success path and fallbacks**
- [ ] **Step 2: Run `python3 -m unittest tests/test_acquire_source_text.py -v` and verify failure**
- [ ] **Step 3: Cover domain policy updates and skip behavior**

### Task 2: Implement the acquisition helper

**Files:**
- Create: `scripts/acquire_source_text.py`
- Modify: `tests/test_acquire_source_text.py`

- [ ] **Step 1: Implement the structured result dataclasses and stage attempt records**
- [ ] **Step 2: Implement pluggable `fetch MCP` and search command providers**
- [ ] **Step 3: Implement direct HTML fetch and built-in text extraction fallback**
- [ ] **Step 4: Implement persisted domain policy loading/saving**
- [ ] **Step 5: Re-run `python3 -m unittest tests/test_acquire_source_text.py -v` and verify pass**

### Task 3: Expose the helper and document the new fact

**Files:**
- Modify: `docs/phase-7a-scan-contract.md`
- Modify: `docs/skill-usage.md`

- [ ] **Step 1: Add a short usage note for the helper and its purpose**
- [ ] **Step 2: Re-run targeted verification for docs and CLI help**
- [ ] **Step 3: Capture any residual limits without overstating external fetch guarantees**
