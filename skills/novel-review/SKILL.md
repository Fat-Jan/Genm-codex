---
name: novel-review
description: Review a chapter in a Codex-managed novel project for quality, continuity, pacing, and reader pull, then record the findings back into project state.
---

# Novel Review

Use this skill after a chapter draft exists and the user wants a structured quality assessment.

## Inputs

- `chapter`
- optional `detail`
- optional `threshold`

## Preconditions

- `.mighty/state.json` exists
- `chapters/第N章.md` exists
- Shared references exist:
  - `../../shared/references/`
  - relevant shared profile under `../../shared/profiles/`

## Required reads

- `.mighty/state.json`
- `chapters/第N章.md`
- relevant profile under `../../shared/profiles/`

Read conditionally:

- previous chapter file or summary for continuity
- shared reference docs for reader-pull, pacing, and anti-AI constraints

## Workflow

1. Read `.mighty/state.json`.
2. Read `chapters/第N章.md`.
3. Read the genre/profile context.
4. Review for:
   - hook and reader pull
   - pacing
   - continuity
   - consistency
   - obvious AI-style issues
5. Produce a structured report with:
   - total score
   - dimension scores
   - critical issues
   - warnings
   - suggested fixes
6. Update review metadata for the chapter inside `.mighty/state.json`.
7. If the chapter falls below threshold, explicitly recommend `novel-rewrite`.

## Outputs

- review report in the response
- updated `.mighty/state.json`

## State update requirements

Update at minimum:

- `chapter_meta[chapter].review_score`
- `chapter_meta[chapter].review_grade`
- `chapter_meta[chapter].review_time`
- `chapter_meta[chapter].dimension_scores`
- `chapter_meta[chapter].needs_fix`

## Notes

- Prefer deterministic, evidence-based findings over vague style criticism.
- If the user asks for auto-fix, route the main rewrite request through `novel-rewrite`.
- Do not claim a review passed unless the report actually shows the score and issues.
