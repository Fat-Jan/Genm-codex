---
name: novel-analyze
description: Analyze a chapter range in a Codex-managed novel project for word count, pacing, cool-point density, continuity signals, and improvement opportunities, then return a concise report.
---

# Novel Analyze

Use this skill when the user wants a data-oriented analysis of one or more written chapters.

## Inputs

- `chapter_start`
- `chapter_end`
- optional `genre`
- optional focus:
  - `cool-points`
  - `pacing`
  - `consistency`
  - `stats`

## Preconditions

- `.mighty/state.json` exists
- the requested chapter files exist under `chapters/`

## Required reads

Always read:

- `.mighty/state.json`
- `chapters/第NNN章.md` for the requested range

Read conditionally:

- `大纲/章纲/第NNN章.md` for the same range
- `大纲/总纲.md`
- `设定集/角色/*.md`
- `设定集/力量体系.md`
- `../../shared/profiles/<genre>/profile.yaml`
- `../../shared/profiles/<genre>/profile-<platform>.yaml`

## Shared profile resolution

If the user provides `genre`, or if the project already has `meta.genre`, resolve shared profile roots in this order:

1. `shared/profiles/`
2. `../../shared/profiles/`

Only read the specific profile files needed for the active project genre/platform.

## Workflow

1. Parse the requested chapter range.
2. Read `.mighty/state.json` and confirm the range is valid.
3. Read the chapter files in that range.
4. Gather lightweight metrics:
   - total words / average words
   - chapter count
   - current review score coverage if present in `chapter_meta`
   - rough dialogue density
   - rough paragraph-length distribution
5. Analyze cool-point density using direct textual cues, not fake precision.
6. Analyze pacing by comparing:
   - chapter purpose from outlines
   - actual event movement in the written chapter
   - information-load vs forward motion
7. Analyze continuity signals:
   - protagonist state progression
   - active foreshadowing touched or ignored
   - major entities / locations appearing across the range
8. If a resolved genre profile is available, use it only as a rubric reference:
   - pacing expectations
   - cool-point density expectations
   - forbidden or weak patterns
9. Return a concise report with:
   - summary stats
   - strongest observations
   - risk points
   - 2-4 concrete improvement suggestions

## Output conventions

Prefer this structure:

- analysis scope
- core stats
- cool-point / pacing / consistency findings
- action recommendations

Use small tables only when they improve readability.
Do not fabricate exact measurements when the signal is only heuristic.

## Notes

- This skill is read-only in the default path; do not modify project files unless the user explicitly asks to save an analysis artifact.
- Prefer approximate but defensible analysis over fake quantitative certainty.
- If the requested range includes unwritten chapters, say so directly and analyze only the written subset.
