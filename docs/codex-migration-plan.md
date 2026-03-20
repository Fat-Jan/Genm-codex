# Genm-codex Migration Status

## Phase 1 Goal

Build a Codex-native workspace that can host:

- `novel-init`
- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-rewrite`
- `novel-export`

while reusing copied shared assets from the source `Genm` repository.

## Components

- `scripts/sync-shared-from-genm.sh`
- `scripts/validate-migration.sh`
- `docs/migration-map.md`
- `skills/novel-init/SKILL.md`
- `skills/novel-outline/SKILL.md`
- `skills/novel-write/SKILL.md`
- `skills/novel-review/SKILL.md`
- `skills/novel-rewrite/SKILL.md`
- `skills/novel-export/SKILL.md`

## Current Status

- workspace skeleton: created
- shared assets: synced
- validator script: created
- migration map: created
- phase-1 core skills: created
- phase-1 core skills: linked into `~/.codex/skills/` with `genm-novel-*` names
- phase-1 core skills: discovery and triggering verified in a fresh Codex session
- phase-1 minimum E2E closure: passed (`init → outline → write → review → rewrite → export`)
- phase-1 delivery docs: created (`README.md`, `docs/skill-usage.md`, `docs/phase-1-summary.md`, `docs/phase-2-priorities.md`)
- install script: created and verified (`scripts/install-skills.sh`)
- migration validator: still passing after wrap-up changes
- phase-2 docs: created (`docs/phase-2-smoke-plan.md`, `docs/phase-2-smoke-results.md`, `docs/phase-2-summary.md`)

## Remaining Next-Phase Items

- decide whether shared assets should later move from full-copy to selective-sync
- decide whether to expand validation beyond single-chapter txt export

## Phase 3 Direction

- third-phase scope selected: `A + B`
- execution shape: split into `Phase 3A` and `Phase 3B`
- scope doc: `docs/phase-3-scope.md`
- `Phase 3A`: `novel-polish`, `novel-genre`, `novel-analyze`, `novel-resume`
- `Phase 3B`: `novel-index`, extended `novel-query`, advanced `novel-status`, `novel-log`
- recommended implementation start: `Phase 3A / P0`
- `Phase 3A / P0` implementation status: started
- `novel-polish`: created
- `novel-genre`: created
- `Phase 3A / P1` implementation status: started
- `novel-analyze`: created
- `Phase 3A / P2` implementation status: started
- `novel-resume`: created
- `Phase 3A / P2` smoke status:
  - `novel-resume`: pass (state fallback path)
- `Phase 3B / P0` implementation status: started
- `novel-index`: created
- `Phase 3B / P0` smoke status:
  - `novel-index`: pass
- `Phase 3B / P1` implementation status: started
- `novel-query`: extended to support index-aware, template-style, and lightweight structured queries
- `Phase 3B / P1` smoke status:
  - `novel-query`: pass
  - `novel-status`: pass
- `Phase 3B / P2` implementation status: started
- `novel-log`: created
- `Phase 3B / P2` smoke status:
  - `novel-log`: pass
- `Phase 3A / P1` smoke status:
  - `novel-analyze`: pass
- `Phase 3A / P0` smoke status:
  - `novel-polish`: pass
  - `novel-genre`: pass

### Phase 3 current conclusion

- `Phase 3A`: validated
- `Phase 3B`: validated
- repository now has enough migration coverage to justify a `v0.4.0` release line

## Phase 4 Direction

- fourth-phase scope selected
- scope doc: `docs/phase-4-scope.md`
- `Phase 4A`: `novel-fix`, `novel-snapshot`, `novel-precheck`, `novel-workflow`
- `Phase 4B`: `novel-retrieve`, `novel-spinoff`
- deferred for later: `novel-learn`, `novel-scan`
- low-priority / likely non-skillized: `novel-config`, `novel-test`, `novel-tutorial`, `novel-help`
- `Phase 4A / P0` implementation status: started
- `novel-fix`: created
- `novel-snapshot`: created
- `Phase 4A / P0` smoke status:
  - `novel-fix`: pass
  - `novel-snapshot`: pass
- `Phase 4A / P1` implementation status: started
- `novel-precheck`: created
- `Phase 4A / P2` implementation status: started
- `novel-workflow`: created
- `Phase 4A / P1` smoke status:
  - `novel-precheck`: pass
- `Phase 4A / P2` smoke status:
  - `novel-workflow`: pass

### Phase 4A current conclusion

- `Phase 4A`: validated
- `Phase 4B / P0` implementation status: started
- `novel-retrieve`: created
- `Phase 4B / P0` smoke status:
  - `novel-retrieve`: pass
- `Phase 4B / P1` implementation status: started
- `novel-spinoff`: created
- `Phase 4B / P1` smoke status:
  - `novel-spinoff`: pass

### Phase 4 current conclusion

- `Phase 4A`: validated
- `Phase 4B`: validated
- repository now has enough migration coverage to justify a `v0.6.0` release line

## Phase 5 Direction

- fifth-phase scope selected
- scope doc: `docs/phase-5-scope.md`
- `Phase 5A`: `novel-config`, `novel-test`
- `Phase 5B`: `novel-learn`
- deferred for later: `novel-scan`
- docs-first / likely non-skillized: `novel-help`, `novel-tutorial`
- `Phase 5A / P0` implementation status: started
- `novel-config`: created
- `novel-test`: created
- `Phase 5A / P0` smoke status:
  - `novel-config`: pass
  - `novel-test`: pass
- `Phase 5B / P0` implementation status: started
- `novel-learn`: created
- `Phase 5B / P0` smoke status:
  - `novel-learn`: pass

### Phase 5 current conclusion

- `Phase 5A`: validated
- `Phase 5B`: validated
- repository now has enough migration coverage to justify a `v0.8.0` release line

## Phase 6 Direction

- sixth-phase scope selected
- scope doc: `docs/phase-6-scope.md`
- `Phase 6A`: docs-first help/tutorial consolidation
- `Phase 6B`: keep `novel-scan` deferred until external trend-scanning contracts are stable
- `novel-help` / `novel-tutorial`: docs-first, likely non-skillized
- `novel-scan`: external-dependency candidate, still deferred
- `Phase 6A` implementation status: completed (docs-first)
- `Phase 6B`: deferred

### Phase 6 current conclusion

- `Phase 6A`: validated
- repository now has enough coverage to justify a `v0.9.0` docs-first consolidation release

## Phase 7 Direction

- seventh-phase scope selected
- scope doc: `docs/phase-7-scope.md`
- `Phase 7A`: external trend-scanning contract design for `novel-scan`
- `Phase 7B`: selective-sync governance design for `shared` assets
- no direct implementation promised yet
- `Phase 7A` contract doc: `docs/phase-7a-scan-contract.md`
- `Phase 7B` governance doc: `docs/phase-7b-selective-sync-governance.md`
- `sync-shared-from-genm.sh` now supports `--report`
- `sync-shared-from-genm.sh` now supports `--domain`
- shared dependency map doc: `docs/shared-asset-dependency-map.md`

## Phase 8 Direction

- eighth-phase scope selected
- scope doc: `docs/phase-8-scope.md`
- `Phase 8A`: experimental `novel-scan` report-only implementation
- `Phase 8B`: shared sync observability hardening
- no default production rollout promised yet
- `Phase 8A / P0` implementation status: started
- `novel-scan`: created
- `Phase 8A / P0` smoke status:
  - `novel-scan`: pass
- `Phase 8A / P1` smoke status:
  - `novel-scan`: pass (project-annotate path)
- `Phase 8B` implementation status: started
- `sync-shared-from-genm.sh`: supports `--report-json`

### Phase 8 current conclusion

- `Phase 8A`: validated
- `Phase 8B`: partially validated
- repository now has enough coverage to justify a `v0.12.0` experimental release line

## Phase 9 Direction

- ninth-phase scope selected
- scope doc: `docs/phase-9-scope.md`
- value-gap analysis: `docs/phase-9-writing-value-gap-analysis.md`
- `Phase 9A`: packaging generation layer
- `Phase 9B`: quality loop integration
- execution strategy: run `Phase 9A` and `Phase 9B` in parallel, then unify shared touchpoints
- `Phase 9A / P0` implementation status: started
- `novel-package`: created
- `Phase 9A / P0` smoke status:
  - `novel-package`: pass
- `Phase 9A / P0` smoke results: `docs/phase-9a-p0-package-smoke-results.md`
- `Phase 9B / P0` design status: started
- quality-loop design doc: `docs/phase-9b-quality-loop-design.md`
- `Phase 9B / P1` integration status: started
- low-risk integration applied to:
  - `novel-write`
  - `novel-polish`
  - `novel-review`
- current integration direction:
  - `write` reads `learned_patterns` and `market_adjustments` conservatively
  - `polish` treats `avoid_patterns` and anti-AI guidance as first-class inputs
  - `review` returns a clearer next-action recommendation (`fix` / `polish` / `rewrite`)
- `Phase 9B / P1` smoke results: `docs/phase-9b-p1-smoke-results.md`
- `Phase 9B / P1` smoke status:
  - `novel-write`: pass
  - `novel-review`: pass
  - `novel-polish`: pass
- `Phase 9A / P1` integration status: started
- current direction:
  - `novel-package` prefers project-local `market_adjustments` over raw market snapshots when both exist
- `Phase 9B / P2` integration status: started
- current direction:
  - `novel-precheck` can treat `market_adjustments` and learned patterns as soft final-gate signals
  - `novel-learn` now points learned output back toward `write / polish / precheck`
- `Phase 9B / P2` smoke results: `docs/phase-9b-p2-smoke-results.md`
- `Phase 9B / P2` smoke status:
  - `novel-precheck`: pass
  - `novel-learn`: pass

### Phase 9 current conclusion

- `Phase 9A`: validated
- `Phase 9B`: validated
- repository now has enough coverage to justify a `v0.13.0` release line

## Phase 10 Direction

- tenth-phase scope selected
- scope doc: `docs/phase-10-scope.md`
- `Phase 10A`: packaging and market-signal convergence
- `Phase 10B`: stable quality routing
- recommended implementation start:
  - normalize `novel-package` output structure
  - tighten `review / precheck` route consistency
- `Phase 10A / P0` smoke results: `docs/phase-10a-p0-smoke-results.md`
- `Phase 10B / P0` smoke results: `docs/phase-10b-p0-smoke-results.md`
- `Phase 10A / P0` smoke status:
  - `novel-package`: pass
- `Phase 10B / P0` smoke status:
  - `novel-precheck`: pass
- `Phase 10A / P1` smoke results: `docs/phase-10a-p1-smoke-results.md`
- `Phase 10B / P1` smoke results: `docs/phase-10b-p1-smoke-results.md`
- `Phase 10A / P1` smoke status:
  - `novel-package`: pass
- `Phase 10B / P1` smoke status:
  - `novel-review`: pass
- `Phase 10A / P1` implementation status: started
- current direction:
  - `novel-package` should report current text-carrying capacity and whether existing packaging needs update
  - a narrow-judgment shortcut was added so this check does not need to expand into a full packaging proposal first
- `Phase 10B / P1` implementation status: started
- current direction:
  - verify `novel-review` can persist `recommended_next_action` into chapter state

### Phase 10 current conclusion

- `Phase 10A`: validated
- `Phase 10B`: validated
- repository now has enough coverage to justify a `v0.14.0` convergence release line

## Phase 11 Direction

- eleventh-phase scope selected
- scope doc: `docs/phase-11-scope.md`
- `Phase 11A`: `v1.0.0` boundary definition
- `Phase 11B`: default workflow convergence
- recommended implementation start:
  - define the `v1.0.0` boundary
  - define the default workflow

## Phase 12 Direction

- twelfth-phase scope selected
- scope doc: `docs/phase-12-scope.md`
- `Phase 12A`: `v1.0.0` readiness checklist
- `Phase 12B`: readiness assessment
- recommended implementation start:
  - write `docs/v1-readiness-checklist.md`
  - write `docs/v1-readiness-assessment.md`

### Phase 12 current conclusion

- `Phase 12A`: validated
- `Phase 12B`: validated
- repository now has enough readiness evidence to justify a `v0.16.0` readiness release line

## Phase 13 Direction

- thirteenth-phase scope selected
- scope doc: `docs/phase-13-scope.md`
- `Phase 13A`: `v1.0.0-rc1` plan
- `Phase 13B`: RC exit criteria
- recommended implementation start:
  - write `docs/v1-rc-plan.md`
  - write `docs/v1-rc-exit-criteria.md`

## Phase 14 Direction

- fourteenth-phase scope selected
- scope doc: `docs/phase-14-scope.md`
- `Phase 14A`: RC execution log
- `Phase 14B`: writing model and reasoning strategy
- recommended implementation start:
  - write `docs/v1-rc-execution-log.md`
  - write `docs/writing-model-strategy.md`

## Phase 2 Smoke Status

- `novel-query`: pass (after strict directory-bound re-test)
- `novel-status`: pass
- `novel-character`: pass
- `novel-setting`: pass
- `novel-foreshadowing`: pass
- `novel-batch` (real ordered writing): pass

### Current conclusion

Second-phase migrated skills now have a usable smoke baseline. The next decision is no longer “are these skills basically wired up?”, but whether to:

1. deepen validation
2. migrate more advanced capabilities

At this point, the repository has enough coverage to justify a second release line.

## Notes

- `Genm` remains the source-of-truth repository.
- `Genm-codex` owns the Codex-native skills.
- Shared assets are copied, not hand-maintained in parallel.
