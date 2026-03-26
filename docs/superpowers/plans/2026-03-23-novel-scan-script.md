# Novel Scan Script Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a minimal executable `novel-scan` script that produces `.mighty/market-data.json` in `report-only` mode, optionally writes project-local market adjustments in `project-annotate` mode, and reuses the stable acquisition helper for external collection.

**Architecture:** Keep the implementation in a standalone Python CLI under `scripts/`. Build a small source-plan layer for supported platform/genre combinations, pipe URLs through `acquire_source_text`, and emit conservative market-data skeletons when evidence is weak. For project annotation, write sidecar guidance and keep `state.json` updates lightweight.

**Tech Stack:** Python standard library (`argparse`, `json`, `pathlib`, `unittest`)

---

### Task 1: Lock output files and fallback behavior with tests

**Files:**
- Create: `tests/test_novel_scan.py`
- Test: `tests/test_novel_scan.py`

- [ ] **Step 1: Write failing tests for `report-only` skeleton output**
- [ ] **Step 2: Write failing tests for `project-annotate` sidecar + state summary**
- [ ] **Step 3: Run `python3 -m unittest tests/test_novel_scan.py -v` and verify failure**

### Task 2: Implement the script

**Files:**
- Create: `scripts/novel_scan.py`
- Modify: `tests/test_novel_scan.py`

- [ ] **Step 1: Implement source-plan building and supported quick routes**
- [ ] **Step 2: Implement market-data generation using `acquire_source_text`**
- [ ] **Step 3: Implement project-local annotation writes**
- [ ] **Step 4: Re-run `python3 -m unittest tests/test_novel_scan.py -v` and verify pass**

### Task 3: Document the executable entry

**Files:**
- Modify: `skills/novel-scan/SKILL.md`
- Modify: `docs/00-当前有效/skill-usage.md`

- [ ] **Step 1: Document the script as the executable report-only helper**
- [ ] **Step 2: Run targeted verification on CLI help and tests**
