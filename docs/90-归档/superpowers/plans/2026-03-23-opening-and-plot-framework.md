# Opening And Plot Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a cross-genre opening-and-plot rules framework under `docs/` and wire it into `novel-outline`, `novel-write`, `novel-review`, `novel-precheck`, and `novel-package` without creating a parallel state center.

**Architecture:** Add a new repo-local framework directory that mirrors the proven anti-flattening pattern: one README plus focused rule modules. Skills consume the new docs conditionally, entry docs expose the new default workflow fact, and review/state docs gain only lightweight optional scoring keys for persistence.

**Tech Stack:** Markdown skill contracts, repo-local workflow docs, Python `unittest`, shell validation via `scripts/validate-migration.sh`

---

### Task 1: Add Red Test For Framework Presence And Wiring

**Files:**
- Create: `tests/test_opening_plot_framework.py`

- [ ] **Step 1: Write the failing test**

```python
def test_framework_files_exist(self):
    for relative_path in FRAMEWORK_FILES:
        self.assertTrue((REPO_ROOT / relative_path).exists())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_opening_plot_framework -v`
Expected: FAIL because the framework directory and doc paths do not exist yet.

- [ ] **Step 3: Keep test scope focused**

Add checks for:
- framework file inventory
- skill doc path references
- entry-doc exposure
- state schema optional score keys

### Task 2: Create The Framework Docs

**Files:**
- Create: `docs/opening-and-plot-framework/README.md`
- Create: `docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
- Create: `docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
- Create: `docs/opening-and-plot-framework/03-开篇故障与修正.md`
- Create: `docs/opening-and-plot-framework/04-剧情层次模型.md`
- Create: `docs/opening-and-plot-framework/05-推进链与残账设计.md`
- Create: `docs/opening-and-plot-framework/06-题材特化接口.md`

- [ ] **Step 1: Write README as the single-source entry**
- [ ] **Step 2: Write the three opening-oriented modules**
- [ ] **Step 3: Write the two plot-layering modules**
- [ ] **Step 4: Write the specialization-interface module**

### Task 3: Wire The Five Main Skills

**Files:**
- Modify: `skills/novel-outline/SKILL.md`
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-review/SKILL.md`
- Modify: `skills/novel-precheck/SKILL.md`
- Modify: `skills/novel-package/SKILL.md`

- [ ] **Step 1: Add explicit doc reads in each skill**
- [ ] **Step 2: Add workflow bullets describing how each skill consumes the framework**
- [ ] **Step 3: Keep rule priority explicit so the new framework does not override canon/bucket law**

### Task 4: Surface The New Fact And Document Lightweight Persistence

**Files:**
- Modify: `README.md`
- Modify: `docs/00-当前有效/start-here.md`
- Modify: `docs/00-当前有效/skill-usage.md`
- Modify: `docs/00-当前有效/default-workflows.md`
- Modify: `shared/references/shared/state-schema.md`
- Modify: `shared/templates/state-v5-template.json`

- [ ] **Step 1: Expose the new framework in repo entry docs**
- [ ] **Step 2: Document optional review score keys in the state schema**
- [ ] **Step 3: Keep the state template lightweight and non-invasive**

### Task 5: Verify And Record

**Files:**
- Modify: `task_plan.md`
- Modify: `findings.md`
- Modify: `progress.md`

- [ ] **Step 1: Run `python -m unittest tests.test_opening_plot_framework -v`**
- [ ] **Step 2: Run `bash scripts/validate-migration.sh`**
- [ ] **Step 3: Update plan/findings/progress with results and residual risk**
