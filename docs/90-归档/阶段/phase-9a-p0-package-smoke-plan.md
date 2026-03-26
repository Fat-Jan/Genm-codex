# Phase 9A / P0 Smoke Plan

## Target

Validate the first-version `novel-package` skill.

## Scenario

Use the existing sample project:

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## Smoke 1: Full packaging proposal

Prompt shape:

- hard-bind the project root
- ask for `mode=full`
- require:
  - title candidates
  - synopsis variants
  - opening-hook suggestions
  - one recommended direction
- do not modify files

Pass conditions:

- returns packaging outputs instead of chapter prose
- remains aligned with current canon
- uses state / outline and optional market data conservatively

## Smoke 2: Naming proposal

Prompt shape:

- hard-bind the project root
- ask for `mode=naming`
- target an existing or planned character
- do not modify files

Pass conditions:

- provides multiple names
- explains style fit
- does not fabricate unrelated character state

## Smoke 3: Save path

Prompt shape:

- hard-bind the project root
- ask for `mode=synopsis`
- enable `save`

Pass conditions:

- creates `包装/简介方案.md`
- does not modify `.mighty/state.json`
- output remains packaging-oriented
