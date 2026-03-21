---
name: novel-outline
description: Generate or refine the total outline and chapter outline files for a Codex-managed novel project using the shared profiles, references, and current project state.
---

# Novel Outline

Use this skill after project initialization, or when the user wants to generate or revise the story outline.

## Inputs

- `mode`: `total` or `chapter`
- optional `start`
- optional `count`
- optional `content_bucket`
- optional multi-option request

## Preconditions

- `.mighty/state.json` exists
- `大纲/` exists
- Shared assets exist:
  - `../../shared/profiles/`
  - `../../shared/references/`

## Workflow

1. Read `.mighty/state.json` for `meta.title`, `meta.genre`, `meta.platform`, and current `genre_profile.bucket` when present.
   - if no explicit `content_bucket` input is provided, treat `genre_profile.bucket` as the active Fanqie content bucket
2. Load the relevant shared profile for rhythm and reader expectations.
3. If the platform is 番茄 and a `content_bucket` is explicitly given, or a current `genre_profile.bucket` exists, or the user clearly asks for Fanqie-first outline refinement:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - treat those bucket rules as upstream outline constraints, not as mere packaging hints
4. For `mode=total`:
   - create or update `大纲/总纲.md`
   - include hook, premise, main conflict, arc direction, and ending direction
   - when bucket constraints are active, also align:
     - opening speed
     - payoff cycle
     - bucket-style conflict density
     - title / synopsis promise consistency
5. For `mode=chapter`:
   - create `大纲/章纲/第N章.md`
   - include chapter goal, conflict, reveal, hook, and continuity notes
   - when bucket constraints are active, also align:
     - current bucket’s opening rule
     - current bucket’s payoff timing
     - current bucket’s pacing density
     - current bucket’s ending or carryover expectation
6. Keep chapter outlines specific enough for writing, but short enough to maintain.
7. If the user asks for multiple options, present 2-3 outline variants before locking one in.
8. Report which outline files were created or updated, and mention the bucket when one was used.

## Output files

- `大纲/总纲.md`
- `大纲/章纲/第N章.md`

## Notes

- Treat `大纲/总纲.md` as the law for later writing steps.
- If the user asks for broad ideation, provide multiple outline options before locking one in.
- Do not generate chapter writing content here; this skill ends at outline artifacts.
- If Fanqie bucket rules are active, they should guide outline shape before packaging and before prose generation.
