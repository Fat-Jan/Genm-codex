# Genm → Genm-codex Migration Map

## Scope

Phase 1 only migrates the core creation loop and shared asset layer.

## Shared Assets

| Source | Target | Strategy | Status |
|--------|--------|----------|--------|
| `Genm/build/profiles/` | `Genm-codex/shared/profiles/` | full copy via sync script | pending sync |
| `Genm/build/references/` | `Genm-codex/shared/references/` | full copy via sync script | pending sync |
| `Genm/build/templates/` | `Genm-codex/shared/templates/` | full copy via sync script | pending sync |

## Core Skill Mapping

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-init.md` | `skills/novel-init/SKILL.md` | `shared/profiles`, `shared/templates` | done | initialize project structure |
| `build/commands/novel-outline.md` | `skills/novel-outline/SKILL.md` | `shared/profiles`, `shared/references` | done | total/chapter outline flows |
| `build/commands/novel-write.md` | `skills/novel-write/SKILL.md` | `shared/profiles`, `shared/references`, selected templates | done | write + quality + state update flow |
| `build/commands/novel-review.md` | `skills/novel-review/SKILL.md` | `shared/references` | done | chapter review and issue reporting |
| `build/commands/novel-rewrite.md` | `skills/novel-rewrite/SKILL.md` | `shared/references` | done | snapshot-aware rewrite flow |
| `build/commands/novel-export.md` | `skills/novel-export/SKILL.md` | `shared/references`, export rules | done | txt-first export workflow |

## Phase 2 Active Migration

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-query.md` | `skills/novel-query/SKILL.md` | project state + selected shared references | done | natural language and template-style project queries |
| `build/commands/novel-status.md` | `skills/novel-status/SKILL.md` | project state + chapter metadata + selected shared references | done | progress and quality dashboard |
| `build/commands/novel-character.md` | `skills/novel-character/SKILL.md` | character files + project state | done | character creation, update, and relation management |
| `build/commands/novel-setting.md` | `skills/novel-setting/SKILL.md` | setting files + project state | done | worldbuilding and setting management |
| `build/commands/novel-foreshadowing.md` | `skills/novel-foreshadowing/SKILL.md` | state foreshadowing threads + outline context | done | foreshadowing state management |
| `build/commands/novel-batch.md` | `skills/novel-batch/SKILL.md` | ordered chapter outlines + project state | done | sequential multi-chapter generation |

## Explicit Non-Migration in Phase 1

| Source Area | Decision | Reason |
|------------|----------|--------|
| Claude plugin manifest | do not migrate | Codex skills do not need Claude plugin packaging |
| historical test reports | do not migrate | not part of core skill behavior |
| legacy command drafts | do not migrate | already classified as reference-only in Genm |
| non-core commands | defer | keep phase 1 small and testable |
