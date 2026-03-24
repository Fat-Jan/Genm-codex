# Setting Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a unified setting gate that aggressively materializes project-local setting assets, blocks writing when outline-dependent setting truth is incomplete, and routes MCP usage through high-risk review instead of direct canon writes.

**Architecture:** Keep the policy in one JSON file under `docs/`, implement the executable gate as a focused Python CLI under `scripts/`, and thread its contract through `novel-init`, `novel-outline`, `novel-write`, `novel-sync`, and the maintenance chain. Reuse the existing strong-quality-gate patterns where possible instead of inventing a parallel rule model.

**Tech Stack:** Python standard library (`argparse`, `json`, `pathlib`, `re`, `unittest`), Markdown skill contracts, project shell validation scripts

---

## File Structure

- `docs/setting-gate-policy.json`
  - single machine-readable source for setting coverage rules, MCP escalation triggers, and risk grades
- `scripts/setting_gate.py`
  - executable local-first enrichment and gating engine
- `tests/test_setting_gate.py`
  - policy, CLI helper, and integration tests for gate behavior
- `scripts/project-maintenance.py`
  - wire post-write setting gate + sync flow
- `scripts/post-task-maintenance.py`
  - keep write trigger aligned with the maintenance chain
- `scripts/sync-setting-assets.py`
  - align review queue shape and generated block handling with the gate
- `skills/novel-init/SKILL.md`
  - init-stage aggressive starter-card contract
- `skills/novel-outline/SKILL.md`
  - outline-stage hard gate contract
- `skills/novel-write/SKILL.md`
  - pre-write gate enforcement contract
- `skills/novel-sync/SKILL.md`
  - review queue / setting materialization contract alignment
- `skills/novel-scan/SKILL.md`
  - MCP-as-candidate, not MCP-as-canon contract
- `docs/start-here.md`
- `docs/default-workflows.md`
- `docs/skill-usage.md`
  - user-facing workflow updates

### Task 1: Lock Policy and Gate State Contract with Failing Tests

**Files:**
- Create: `tests/test_setting_gate.py`
- Test: `tests/test_setting_gate.py`

- [ ] **Step 1: Write the failing test for policy file presence and required sections**

```python
def test_setting_gate_policy_contains_required_sections(self):
    policy = json.loads(Path("docs/setting-gate-policy.json").read_text())
    self.assertIn("coverage_requirements", policy)
    self.assertIn("mcp_escalation", policy)
    self.assertIn("risk_grades", policy)
```

- [ ] **Step 2: Write the failing test for local-first gate blocking behavior**

```python
def test_run_gate_blocks_when_high_risk_gap_remains(self):
    result = setting_gate.run_gate(project_root=project_root, stage="outline")
    self.assertEqual(result["status"], "blocked")
    self.assertTrue(result["blocking_gaps"])
```

- [ ] **Step 3: Write the failing test for aggressive local card creation**

```python
def test_run_gate_materializes_local_cards_from_outline_and_state(self):
    result = setting_gate.run_gate(project_root=project_root, stage="outline")
    self.assertIn("设定集/角色/韩振.md", result["auto_created_files"])
```

- [ ] **Step 4: Write the failing test for MCP-derived high-risk review queuing**

```python
def test_mcp_candidate_requires_confirmation_and_blocks(self):
    result = setting_gate.grade_candidates([candidate], policy)
    self.assertTrue(result["review_items"][0]["requires_user_confirmation"])
    self.assertEqual(result["status"], "blocked")
```

- [ ] **Step 5: Run test to verify failure**

Run: `python3 -m unittest tests.test_setting_gate -v`
Expected: FAIL because `docs/setting-gate-policy.json` and `scripts/setting_gate.py` do not exist yet

### Task 2: Implement the Policy and Core Gate Script

**Files:**
- Create: `docs/setting-gate-policy.json`
- Create: `scripts/setting_gate.py`
- Modify: `tests/test_setting_gate.py`

- [ ] **Step 1: Add the policy file with required sections and conservative default thresholds**

- [ ] **Step 2: Implement policy loading, project scanning, local-first candidate extraction, and risk grading**

- [ ] **Step 3: Implement file materialization helpers for `设定集/角色|地点|势力|物品|世界观` and `.mighty/setting-gate.json`**

- [ ] **Step 4: Implement selective MCP candidate handling as review-only metadata, not canon writes**

- [ ] **Step 5: Re-run `python3 -m unittest tests.test_setting_gate -v` and verify pass**

### Task 3: Align Maintenance and Review Queue Plumbing

**Files:**
- Modify: `scripts/sync-setting-assets.py`
- Modify: `scripts/project-maintenance.py`
- Modify: `scripts/post-task-maintenance.py`
- Modify: `tests/test_setting_gate.py`
- Test: `tests/test_setting_gate.py`

- [ ] **Step 1: Write the failing integration test for write-post maintenance invoking gate + sync flow**

```python
def test_project_maintenance_runs_setting_gate_before_sync(self):
    payload = json.loads(run_project_maintenance(project_root))
    self.assertIn("setting-gate.py", payload["steps"])
```

- [ ] **Step 2: Write the failing integration test for extended `sync-review.json` fields**

```python
def test_sync_review_contains_stage_confidence_and_confirmation_flags(self):
    review_doc = json.loads((project_root / ".mighty" / "sync-review.json").read_text())
    self.assertIn("source_stage", review_doc["ambiguous_entities"][0])
```

- [ ] **Step 3: Run `python3 -m unittest tests.test_setting_gate -v` and verify failure on new assertions**

- [ ] **Step 4: Update maintenance scripts and queue writing shape to satisfy the tests**

- [ ] **Step 5: Re-run `python3 -m unittest tests.test_setting_gate -v` and verify pass**

### Task 4: Wire Skill Contracts to the New Gate

**Files:**
- Modify: `skills/novel-init/SKILL.md`
- Modify: `skills/novel-outline/SKILL.md`
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-sync/SKILL.md`
- Modify: `skills/novel-scan/SKILL.md`
- Modify: `docs/start-here.md`
- Modify: `docs/default-workflows.md`
- Modify: `docs/skill-usage.md`
- Test: `tests/test_setting_gate.py`

- [ ] **Step 1: Write the failing contract test for required setting-gate references in the relevant skill files**

```python
def test_skill_contracts_reference_setting_gate_flow(self):
    self.assertIn("setting gate", Path("skills/novel-outline/SKILL.md").read_text())
    self.assertIn(".mighty/setting-gate.json", Path("skills/novel-write/SKILL.md").read_text())
```

- [ ] **Step 2: Write the failing contract test for user-facing workflow docs**

```python
def test_workflow_docs_describe_outline_hard_gate_and_write_post_sync(self):
    text = Path("docs/default-workflows.md").read_text()
    self.assertIn("setting gate", text)
```

- [ ] **Step 3: Run `python3 -m unittest tests.test_setting_gate -v` and verify failure on missing contract text**

- [ ] **Step 4: Update skill and workflow docs to describe the new gate and MCP boundaries**

- [ ] **Step 5: Re-run `python3 -m unittest tests.test_setting_gate -v` and verify pass**

### Task 5: Run Regression and Smoke Verification

**Files:**
- Modify: `task_plan.md`
- Modify: `findings.md`
- Modify: `progress.md`

- [ ] **Step 1: Run focused regression tests**

Run: `python3 -m unittest tests.test_setting_gate tests.test_strong_quality_gate -v`
Expected: PASS

- [ ] **Step 2: Run migration validation**

Run: `bash scripts/validate-migration.sh`
Expected: `Migration validation passed`

- [ ] **Step 3: Run a read-only smoke on the two sparse projects using the gate CLI**

Run: `python3 scripts/setting_gate.py projects/公司裁我那天，系统先赔了我一百万 --stage outline --report-only`
Expected: reports auto-created candidates and any blocking gaps without mutating canon unexpectedly

Run: `python3 scripts/setting_gate.py projects/转学第一天，我把校草认成了新来的代课老师 --stage outline --report-only`
Expected: same behavior for the second project

- [ ] **Step 4: Record verification and findings in planning files**

- [ ] **Step 5: Commit the implementation**

```bash
git add docs/setting-gate-policy.json scripts/setting_gate.py scripts/sync-setting-assets.py scripts/project-maintenance.py scripts/post-task-maintenance.py skills/novel-init/SKILL.md skills/novel-outline/SKILL.md skills/novel-write/SKILL.md skills/novel-sync/SKILL.md skills/novel-scan/SKILL.md docs/start-here.md docs/default-workflows.md docs/skill-usage.md tests/test_setting_gate.py task_plan.md findings.md progress.md
git commit -m "feat: add setting gate workflow"
```
