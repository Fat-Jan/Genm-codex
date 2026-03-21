---
name: novel-write
description: Write a chapter in a Codex-managed novel project by reading the current state, outline, setting files, and shared profile assets, then updating chapter content and project state.
---

# Novel Write

Use this skill when the user wants to write the next chapter from the current outline and project state.

## Inputs

- `chapter`
- optional `word_count`
- optional `style`
- optional `content_bucket`
- optional `tagpack`

## Preconditions

- `.mighty/state.json` exists
- `大纲/章纲/第N章.md` exists for the target chapter
- `设定集/角色/主角.md` exists
- Shared assets exist:
  - `../../shared/profiles/`
  - `../../shared/references/`
- If this is not chapter 1, either the previous chapter file or a valid prior summary exists

## Required reads

Always read:

- `.mighty/state.json`
- `大纲/章纲/第N章.md`
- `设定集/角色/主角.md`

Read conditionally:

- `大纲/总纲.md` for main-arc alignment
- relevant `设定集/世界观/*.md`
- relevant supporting character files in `设定集/角色/`
- previous chapter file or summary
- current `learned_patterns` inside `.mighty/state.json`
- current `market_adjustments` inside `.mighty/state.json`
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-mvp-tagpacks.yaml`

## Workflow

1. Read `.mighty/state.json`.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
   - determine explicit `tagpack` if provided
2. Read the target chapter outline from `大纲/章纲/第N章.md`.
3. Read required setting files from `设定集/`.
4. Load the shared profile matching the project genre from `../../shared/profiles/`.
5. Read any useful local guidance already present in state:
   - `learned_patterns`
   - `market_adjustments`
6. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as upstream prose constraints for:
     - opening speed
     - payoff timing
     - conflict density
     - chapter-end carryover
7. If an explicit `tagpack` is given, or the request clearly asks for a tag-pack route such as `恶女`:
   - read `../../docs/fanqie-mvp-tagpacks.yaml`
   - prefer a tagpack whose `base_bucket` matches the active `content_bucket`
   - treat the chosen tagpack as a second-layer overlay on top of the bucket, not as a replacement for the bucket
8. Load high-value shared references from `../../shared/references/` only as needed.
9. If a previous chapter exists, read the prior chapter summary or chapter file for continuity.
10. Write `chapters/第N章.md` aligned to:
   - current state
   - target chapter outline
   - genre/platform expectations
   - learned style preferences when they are concrete
   - learned avoid-patterns when they are concrete
   - project-local market suggestions when they are relevant and low-risk
   - active Fanqie bucket constraints when they exist
   - active first-batch MVP bucket template signals when they exist:
     - primary reader motive
     - tag pack
     - opening rule
     - payoff cycle
     - ending-hook rule
   - active tagpack overlay when it exists:
     - positioning
     - protagonist_core
     - reader_motive
     - opening_rule
     - payoff_rule
     - ending_hook_rule
11. Update `.mighty/state.json` with:
   - `progress.current_chapter`
   - `progress.total_words`
   - `progress.last_write_chapter`
   - `progress.last_write_time`
   - `chapter_meta`
   - `chapter_snapshots`
   - `summaries_index`
12. Do not write review scores here unless an actual review step was run.
13. Recommend running `novel-review` immediately after writing.

## Chapter state update requirements

At minimum, update:

- `chapter_meta[chapter]`
- `chapter_snapshots[chapter]`
- `summaries_index[chapter]`
- `entities.characters.protagonist` if the chapter changes protagonist state
- `plot_threads` if foreshadowing or suspense changes

## Outputs

- `chapters/第N章.md`
- updated `.mighty/state.json`
- optional note recommending `novel-review`

## Failure handling

- If `.mighty/state.json` is missing, stop and route back to `novel-init`.
- If the target chapter outline is missing, stop and route back to `novel-outline`.
- If continuity-critical state is ambiguous, prefer using the existing state file over guessing from prose.
- Do not invent new top-level state sections unless strictly required.

## Notes

- Keep writing aligned to the outline and current state.
- Do not invent structural state fields ad hoc; prefer extending the existing `.mighty/state.json` shape conservatively.
- Treat `learned_patterns` as a preference signal, not a hard rule.
- Treat `market_adjustments` as packaging or pacing guidance, not as a reason to break canon or outline purpose.
- When Fanqie bucket constraints are active, use them to tighten chapter rhythm and hook delivery, not to override canon, chapter purpose, or already established plot logic.
- If a first-batch MVP bucket config exists, prefer its reader-motive and payoff style over generic bucket language.
- If a matching tagpack exists, use it as a second-layer style/positioning overlay after bucket selection, not as a substitute for the bucket.
