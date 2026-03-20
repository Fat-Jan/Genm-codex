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
- `Phase 4B / P1` implementation status: started
- `novel-spinoff`: created
- `Phase 4B / P0` smoke status:
  - `novel-retrieve`: pass
- `Phase 4B / P0` smoke status:
  - `novel-retrieve`: pass

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
