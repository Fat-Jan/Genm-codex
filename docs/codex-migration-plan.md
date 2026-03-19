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
