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

## Remaining Next-Phase Items

- decide whether to add second-batch skills
- decide whether shared assets should later move from full-copy to selective-sync
- decide whether to expand validation beyond single-chapter txt export

## Notes

- `Genm` remains the source-of-truth repository.
- `Genm-codex` owns the Codex-native skills.
- Shared assets are copied, not hand-maintained in parallel.
