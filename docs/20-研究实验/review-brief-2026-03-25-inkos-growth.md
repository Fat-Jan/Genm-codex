# InkOS-Inspired Growth Review Brief

## Purpose

This brief is for a focused Claude review of the `inkos`-inspired growth lane that was implemented incrementally in this workspace.

The implementation goal was not to copy InkOS's monolithic CLI or daemon model.
The goal was to import the highest-value system ideas into the existing `Genm-codex` architecture:

- `docs/ + skills/ + scripts + sidecars`
- keep `state` as runtime truth
- avoid a second truth center
- preserve current workflow boundaries

## Implemented Scope

The work landed seven linked capabilities:

1. **Chapter transaction contract**
   - fixed single-chapter path:
     - `gate-check -> draft -> close -> maintenance -> snapshot`

2. **Active context sidecar**
   - `.mighty/active-context.json`
   - current-writing prompt assembly layer only

3. **Deterministic post-write lint**
   - `scripts/post_write_lint.py`
   - structured evidence only
   - no prose mutation

4. **Short-lived review guardrails**
   - `recent_guardrails` in `.mighty/learned-patterns.json`
   - sidecar-first, expiring next-chapter constraints

5. **Reference learning expansion**
   - chapter range
   - local file
   - retrievable URL text
   - still sidecar-first
   - no parallel `style_profile.json` system

6. **Existing manuscript import bridge**
   - `scripts/import_existing_chapters.py`
   - conservative import / reuse / conflict reporting
   - emits `.mighty/import-report.json`
   - explicitly does **not** pretend to reconstruct canon/state

7. **Longform context compression**
   - `scripts/build_volume_summaries.py`
   - `.mighty/volume-summaries.json`
   - compressed archive view only

## Primary Files To Review

### New scripts

- [scripts/build_active_context.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/build_active_context.py)
- [scripts/post_write_lint.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/post_write_lint.py)
- [scripts/import_existing_chapters.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/import_existing_chapters.py)
- [scripts/build_volume_summaries.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/build_volume_summaries.py)

### Workflow / maintenance integration

- [scripts/project-maintenance.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/project-maintenance.py)
- [scripts/post-task-maintenance.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/post-task-maintenance.py)
- [scripts/split-runtime-guidance.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/split-runtime-guidance.py)
- [scripts/thin-state.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/thin-state.py)

### Contract / schema / template updates

- [shared/references/shared/chapter-transaction-schema.md](/Users/arm/Desktop/vscode/Genm-codex/shared/references/shared/chapter-transaction-schema.md)
- [shared/references/shared/state-schema.md](/Users/arm/Desktop/vscode/Genm-codex/shared/references/shared/state-schema.md)
- [shared/templates/workflow-state-v2.json](/Users/arm/Desktop/vscode/Genm-codex/shared/templates/workflow-state-v2.json)
- [shared/templates/state-v5-template.json](/Users/arm/Desktop/vscode/Genm-codex/shared/templates/state-v5-template.json)
- [shared/templates/learned-patterns-template.json](/Users/arm/Desktop/vscode/Genm-codex/shared/templates/learned-patterns-template.json)
- [docs/strong-quality-gate-policy.json](/Users/arm/Desktop/vscode/Genm-codex/docs/strong-quality-gate-policy.json)
- [docs/writing-core-framework/07-memory-压缩信号约定.md](/Users/arm/Desktop/vscode/Genm-codex/docs/writing-core-framework/07-memory-压缩信号约定.md)
- [docs/00-当前有效/state-thinning-and-setting-sync.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/state-thinning-and-setting-sync.md)

### Skill contract changes

- [skills/novel-write/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-write/SKILL.md)
- [skills/novel-close/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-close/SKILL.md)
- [skills/novel-workflow/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-workflow/SKILL.md)
- [skills/novel-resume/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-resume/SKILL.md)
- [skills/novel-review/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-review/SKILL.md)
- [skills/novel-fix/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-fix/SKILL.md)
- [skills/novel-learn/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-learn/SKILL.md)
- [skills/novel-status/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-status/SKILL.md)
- [skills/novel-query/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-query/SKILL.md)
- [skills/novel-index/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-index/SKILL.md)
- [skills/novel-sync/SKILL.md](/Users/arm/Desktop/vscode/Genm-codex/skills/novel-sync/SKILL.md)

### User-facing docs

- [docs/00-当前有效/default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/default-workflows.md)
- [docs/00-当前有效/start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/start-here.md)
- [docs/00-当前有效/skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/skill-usage.md)
- [docs/90-归档/阶段/phase-5b-p0-learn-smoke-plan.md](/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/phase-5b-p0-learn-smoke-plan.md)
- [docs/90-归档/阶段/phase-5b-p0-learn-smoke-results.md](/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/phase-5b-p0-learn-smoke-results.md)

### Tests

- [tests/test_inkos_growth_plan.py](/Users/arm/Desktop/vscode/Genm-codex/tests/test_inkos_growth_plan.py)
- [tests/test_active_context.py](/Users/arm/Desktop/vscode/Genm-codex/tests/test_active_context.py)
- [tests/test_post_write_lint.py](/Users/arm/Desktop/vscode/Genm-codex/tests/test_post_write_lint.py)
- [tests/test_import_existing_chapters.py](/Users/arm/Desktop/vscode/Genm-codex/tests/test_import_existing_chapters.py)
- [tests/test_volume_summaries.py](/Users/arm/Desktop/vscode/Genm-codex/tests/test_volume_summaries.py)
- [tests/test_acquire_source_text.py](/Users/arm/Desktop/vscode/Genm-codex/tests/test_acquire_source_text.py)
- [tests/test_strong_quality_gate.py](/Users/arm/Desktop/vscode/Genm-codex/tests/test_strong_quality_gate.py)
- [tests/test_writing_core_smoke.py](/Users/arm/Desktop/vscode/Genm-codex/tests/test_writing_core_smoke.py)

### Plan used for execution

- [docs/superpowers/plans/2026-03-25-inkos-inspired-growth.md](/Users/arm/Desktop/vscode/Genm-codex/docs/superpowers/plans/2026-03-25-inkos-inspired-growth.md)

## What To Review For

Please prioritize:

1. **Boundary preservation**
   - no second truth center
   - no accidental migration toward a monolithic InkOS-style runtime
   - sidecars remain sidecars

2. **Contract coherence**
   - skills, scripts, templates, docs, and tests agree on:
     - chapter transaction
     - active-context
     - post-write lint
     - recent guardrails
     - import-report
     - volume-summaries

3. **False certainty / overclaim risk**
   - imported chapters do not pretend to reconstruct canon/state
   - URL learning only succeeds when content is actually retrievable
   - volume summaries do not get mistaken for detailed fact truth

4. **Maintenance ordering**
   - active-context build happens in the right place
   - thin-state refreshes volume summaries after archive changes

5. **State bloat risk**
   - short-lived or compressed data stays sidecar-first
   - `state.json` only keeps pointers/light summaries where intended

## Verification Already Run

Fresh verification was run in this workspace:

```bash
python -m unittest tests.test_setting_gate tests.test_strong_quality_gate tests.test_active_context tests.test_post_write_lint tests.test_writing_core_smoke tests.test_acquire_source_text tests.test_import_existing_chapters tests.test_volume_summaries tests.test_inkos_growth_plan -v

bash scripts/validate-migration.sh
```

Observed result:

- `113` tests passed
- migration validation passed

Spot checks also run:

```bash
python3 scripts/post_write_lint.py smoke/e2e-qinggan-evil/chapters/第001章.md
python3 scripts/import_existing_chapters.py smoke/e2e-qinggan-evil --from smoke/e2e-qinggan-evil/chapters
python3 scripts/build_volume_summaries.py smoke/e2e-qinggan-evil
```

## Intentional Non-Goals

These are intentional and should not be flagged as missing unless you think the boundary is wrong:

- no daemon / scheduler / notification subsystem
- no SQLite temporal memory DB
- no automatic canon reconstruction from imported manuscripts
- no new permanent style center such as `style_profile.json`
- no prose mutation inside maintenance scripts
- no replacement of `state` as runtime truth

## Unrelated Dirty Files To Ignore

There are pre-existing or unrelated dirty paths in the worktree that are not part of this implementation and should not be mixed into review conclusions:

- [findings.md](/Users/arm/Desktop/vscode/Genm-codex/findings.md)
- [progress.md](/Users/arm/Desktop/vscode/Genm-codex/progress.md)
- [task_plan.md](/Users/arm/Desktop/vscode/Genm-codex/task_plan.md)
- [task_plan_archive.md](/Users/arm/Desktop/vscode/Genm-codex/task_plan_archive.md)
- `.omx/`
- two existing dirty `projects/.../.mighty/state.json` files already present in the workspace

Review should focus on the files listed above under implemented scope, not on unrelated workspace noise.
