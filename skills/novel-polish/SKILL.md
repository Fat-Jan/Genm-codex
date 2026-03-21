---
name: novel-polish
description: Polish an existing chapter in a Codex-managed novel project by improving prose, dialogue, description, or pacing while preserving plot, keeping a small delta, and updating polish metadata.
---

# Novel Polish

Use this skill when the user wants to refine an existing chapter without doing a full rewrite.

## Inputs

- `chapter`
- optional `aspect`
  - `prose`
  - `dialogue`
  - `description`
  - `pacing`
  - `all`
- optional `content_bucket`
- optional preview intent

## Preconditions

- `.mighty/state.json` exists
- `chapters/第N章.md` exists
- `大纲/章纲/第N章.md` exists

## Required reads

- `chapters/第N章.md`
- `.mighty/state.json`
- `大纲/章纲/第N章.md`

Read conditionally:

- `chapter_meta[N]` review findings
- `设定集/角色/*.md` when dialogue or OOC risk matters
- `设定集/力量体系.md` or other setting files when terminology consistency matters
- `.mighty/learned-patterns.json`
- `learned_patterns` summary inside `.mighty/state.json`
- `../../shared/references/writing/anti-ai-style.md` when prose, description, or all is requested
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-rule-priority-matrix.md`

## Workflow

1. Read the current chapter and current state.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
2. Determine whether the request is true polish or a structural rewrite request.
3. If the requested change would alter core plot, continuity, or chapter purpose, stop and recommend `novel-rewrite` instead.
4. Read the chapter outline and any directly relevant review findings.
5. If the project has usable learned-pattern sidecar data, use it as polish preferences:
   - preferred dialogue style
   - preferred description density
   - preferred high-point handling
   - avoid patterns
6. Choose the polish focus:
   - `prose`: remove repetition, tighten sentences, improve phrasing
   - `dialogue`: sharpen voice, reduce filler, preserve character tone
   - `description`: improve sensory detail and scene clarity
   - `pacing`: tighten slow sections, reduce explanatory drag, improve transitions
   - `all`: apply a balanced pass without broad structural changes
7. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as polish-side constraints for:
     - sentence-level opening urgency
     - payoff visibility
     - conflict density
     - chapter-end carryover sharpness
8. If Fanqie polish rules are active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - use them as third-layer polish-side optimization for:
     - hook sentence sharpness
     - title / synopsis promise carryover
     - character liveliness
     - suspense handoff and map-shift smoothness
   - do not let technique rules override canon, chapter purpose, or active bucket
9. For prose-like polish, explicitly watch for:
   - explanation replacing scene display
   - generic symmetrical phrasing
   - filler transitions
   - obvious anti-AI style warnings already known in the project
   - weak bucket-fit delivery when a Fanqie bucket is active
10. Preserve:
   - chapter purpose
   - core events
   - named entities
   - continuity with existing state
11. Keep the word-count delta modest by default, roughly within `±10%` unless the user explicitly wants a bigger change.
12. If the user asks for preview or comparison, return:
   - short change summary
   - optional before/after excerpts
   - proposed polished text without saving
13. Otherwise:
   - create a backup under `.mighty/backup/`
   - save the polished chapter back to `chapters/第N章.md`
   - update polish metadata in `.mighty/state.json`

## Outputs

- preview-only polish proposal, or
- updated `chapters/第N章.md`
- optional backup artifact under `.mighty/backup/`
- updated `.mighty/state.json`

## State update requirements

When saving, update at minimum:

- `meta.updated_at`
- `progress.last_write_chapter`
- `progress.last_write_time`
- `chapter_meta[N].updated_at`
- `chapter_meta[N].word_count`
- `chapter_meta[N].summary` when the chapter summary materially changed
- `chapter_meta[N].last_polish_time`
- `chapter_meta[N].polish_aspect`
- `chapter_meta[N].polish_count`

If the project already tracks snapshots, refresh `chapter_snapshots[N]` to match the saved polished version.

## Notes

- This skill is for refinement, not redesign.
- Prefer the smallest edit that improves readability and pull.
- If the chapter already has unresolved critical review issues, use them as polish priorities.
- If the user wants side-by-side diff behavior, keep it lightweight in text; do not recreate the old command’s interactive UI flow.
- If the project has explicit `avoid_patterns`, treat them as first-class polish targets.
- When Fanqie rules stack, apply them in this order:
  1. canon / state / chapter purpose
  2. active bucket
  3. writing-technique optimization
  4. tagpack overlay when explicitly active
- When a Fanqie content bucket is active, use it to sharpen delivery and readability for that bucket, not to override chapter purpose, canon, or already-accepted plot outcomes.
- If a first-batch MVP bucket config exists, prefer its reader-motive and ending-hook expectations over generic bucket language.
