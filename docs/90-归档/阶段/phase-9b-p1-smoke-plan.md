# Phase 9B / P1 Smoke Plan

## Target

Validate the first low-risk quality-loop integration round:

- `novel-write`
- `novel-review`
- `novel-polish`

## Intent

This round does not try to prove a full quality platform. It only validates that:

1. `novel-write` can read `learned_patterns` and `market_adjustments` as usable guidance
2. `novel-review` can return a clearer repair route recommendation
3. `novel-polish` can treat anti-AI and avoid-pattern guidance as first-class polish inputs

## Scenario

Use the existing sample project:

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

Current expectations before the smoke:

- `current_chapter = 3`
- `learned_patterns` already populated
- `market_adjustments` already populated
- `第004章` chapter outline exists

## Smoke 1: Write chapter 4 with integrated signals

Prompt shape:

- hard-bind the project root
- use `novel-write`
- target `chapter=4`
- request a concise post-run summary of:
  - which learned patterns were used
  - which market adjustments were used
  - what files changed

Pass conditions:

- `chapters/第004章.md` is created
- `.mighty/state.json` is updated
- output clearly references at least one `learned_patterns` signal and one `market_adjustments` signal

## Smoke 2: Review chapter 4 with routing

Prompt shape:

- hard-bind the project root
- use `novel-review`
- target `chapter=4`
- request:
  - score
  - key issues
  - recommended next action

Pass conditions:

- review runs on chapter 4
- answer includes a route recommendation:
  - `novel-fix`
  - or `novel-polish`
  - or `novel-rewrite`
- state review metadata updates

## Smoke 3: Polish preview with anti-AI / avoid-pattern focus

Prompt shape:

- hard-bind the project root
- use `novel-polish`
- target `chapter=4`
- preview-only
- ask what avoid-patterns and anti-AI concerns the polish pass is addressing

Pass conditions:

- no files are modified
- answer explicitly references project avoid-patterns or anti-AI style concerns
- output remains polish-sized, not rewrite-sized
