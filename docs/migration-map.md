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

## Phase 3A In Progress

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-polish.md` | `skills/novel-polish/SKILL.md` | chapter text + state + outline + selected setting files | done | first version focuses on minimal chapter polish closure, not interactive diff UI |
| `build/commands/novel-genre.md` | `skills/novel-genre/SKILL.md` | `shared/profiles` + project state | done | first version focuses on list/show/detect/apply, without Hive Bee orchestration |
| `build/commands/novel-analyze.md` | `skills/novel-analyze/SKILL.md` | chapter files + state + optional outlines + selected profiles | done | first version focuses on read-only chapter-range analysis, not heavy charting |
| `build/commands/novel-resume.md` | `skills/novel-resume/SKILL.md` | workflow state + project state + optional outline context | done | first version focuses on safe resume diagnosis and next-step recommendation, not full workflow replay |

## Phase 3B In Progress

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-index.md` | `skills/novel-index/SKILL.md` | chapter files + state + optional setting files | done | first version focuses on lightweight `.mighty/index.json`, not heavy entity extraction |
| `build/commands/novel-log.md` | `skills/novel-log/SKILL.md` | `.mighty/logs/trace.jsonl` | done | first version is a read-only tail/search/stats viewer with clear “log not initialized” behavior |

## Phase 4A In Progress

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-fix.md` | `skills/novel-fix/SKILL.md` | chapter review metadata + chapter text + state | done | first version focuses on targeted issue-based fixes, not broad automatic rewriting |
| `build/commands/novel-snapshot.md` | `skills/novel-snapshot/SKILL.md` | `chapter_snapshots` + `.mighty/snapshots/` | done | first version stays state-centric and reuses the existing snapshot layout |
| `build/commands/novel-precheck.md` | `skills/novel-precheck/SKILL.md` | chapter text + state + optional shared platform profile | done | first version is a read-only submission-readiness checker, not an upload automator |
| `build/commands/novel-workflow.md` | `skills/novel-workflow/SKILL.md` | `.mighty/workflow_state.json` + `.mighty/state.json` | done | first version is a lightweight state manager, not a full workflow orchestrator |

## Phase 4B In Progress

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-retrieve.md` | `skills/novel-retrieve/SKILL.md` | state + index + character/setting files | done | first version is a writing-oriented retrieval layer, not a second general query engine |
| `build/commands/novel-spinoff.md` | `skills/novel-spinoff/SKILL.md` | state + canon files + setting files | done | first version is a lightweight single-project spinoff writer, not a multi-book universe manager |

## Phase 5A In Progress

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-config.md` | `skills/novel-config/SKILL.md` | `.env` + `.mighty/config.json` + `~/.codex/config.toml` | done | first version is a guided local config inspector, not a full environment manager |
| `build/commands/novel-test.md` | `skills/novel-test/SKILL.md` | `.env` + `~/.codex/config.toml` | done | first version is a guided connection-test assistant, not a fake live probe |

## Phase 5B In Progress

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-learn.md` | `skills/novel-learn/SKILL.md` | local chapter range or local file + `learned_patterns` in state | done | first version is a local-content learner, not an automatic external fetcher |

## Phase 8A Experimental

| Source Command | Target Skill | Primary Shared Dependencies | Status | Notes |
|----------------|-------------|-----------------------------|--------|-------|
| `build/commands/novel-scan.md` | `skills/novel-scan/SKILL.md` | optional external sources + `.mighty/market-data.json` | done | first version is report-only and confidence-aware, with no default profile rewrites |

## Explicit Non-Migration in Phase 1

| Source Area | Decision | Reason |
|------------|----------|--------|
| Claude plugin manifest | do not migrate | Codex skills do not need Claude plugin packaging |
| historical test reports | do not migrate | not part of core skill behavior |
| legacy command drafts | do not migrate | already classified as reference-only in Genm |
| non-core commands | defer | keep phase 1 small and testable |
