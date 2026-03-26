---
name: novel-genre
description: List, inspect, detect, and apply genre profiles for a Codex-managed novel project by reading shared profile assets and syncing the selected profile back into project state.
---

# Novel Genre

Use this skill when the user wants to inspect available genres, detect the current genre, or apply a profile to a Codex-managed novel project.

## Inputs

- action:
  - `list`
  - `show`
  - `detect`
  - `apply`
- optional `genre`
- optional `platform`
- optional `content_bucket`

## Preconditions

- one of the shared profile roots exists:
  - `shared/profiles/`
  - `../../shared/profiles/`
- `.mighty/state.json` exists for `show`, `detect`, and `apply`

## Required reads

Always read as needed:

- the resolved profile root README
- the resolved profile root `*/profile.yaml`
- `.mighty/state.json`

Read conditionally:

- resolved profile root `<genre>/profile-<platform>.yaml`
- resolved profile root `<genre>/bucket-<content_bucket>.yaml`
- `大纲/总纲.md`
- `设定集/力量体系.md`
- `.mighty/content-positioning.json`
- `chapters/第001章.md` or nearby project files only when genre detection is truly unclear
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`

## Shared profile root resolution

Before listing or applying any profile, resolve the first existing profile root from:

1. `shared/profiles/`
2. `../../shared/profiles/`

Use that resolved root consistently for all reads during the task.

## Profile contract rules

- `novel-genre` is the primary project-facing entrance for profile selection and application.
- `state.genre_profile` is the runtime projection layer; it should stay lightweight.
- If raw profile detail is needed, interpret it through `../../scripts/profile_contract.py` rather than treating arbitrary raw YAML fields as the consumer contract.
- Use the following layer order:
  1. core profile: `<genre>/profile.yaml`
  2. platform overlay: `<genre>/profile-<platform>.yaml` when it exists
  3. bucket overlay: `<genre>/bucket-<bucket>.yaml` when it exists
  4. reference files: remaining `*.md` files under the profile directory
- Legacy embedded long-form sections inside raw profile YAML should be treated as reference-like material, not as authoritative core contract.

## Workflow

### list

1. Resolve the shared profile root.
2. Scan that profile root for directories or standalone profile files.
2. Return a concise list of available genre codes and visible names.

### show

1. Read `.mighty/state.json`.
2. Report:
   - current `meta.genre`
   - current `meta.platform`
   - current `genre_profile.bucket` when present
   - current `genre_profile.tagpacks / strong_tags / narrative_modes / tone_guardrails` when present
   - loaded profile path if present
   - resolved profile root if one exists
   - content-positioning sidecar path if present
   - a short summary of the active genre constraints

### detect

1. Prefer the current `meta.genre` if already set.
2. If the project genre is missing or obviously generic, infer from:
   - total outline
   - power-system or setting files
   - early chapter content when necessary
3. If the platform is 番茄 and the user asks for bucket detection, or the current task is clearly Fanqie-first:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - infer the best-fit content bucket conservatively from:
     - title / premise
     - current hook style
     - whether the project reads more like `传统玄幻`, `玄幻脑洞`, `东方仙侠`, etc.
4. Return:
   - detected genre
   - detected bucket when applicable
   - confidence
5. Do not silently rewrite state on detect-only requests.

### apply

1. Determine the target genre:
   - explicit user input wins
   - otherwise fall back to current `meta.genre`
2. Determine the target platform:
   - explicit user input wins
   - otherwise use `meta.platform`
3. Determine the target content bucket:
   - explicit `content_bucket` wins
   - otherwise keep the current `genre_profile.bucket` if one exists
4. Resolve the shared profile root.
3. Select the best profile path:
   - prefer `<resolved_root>/<genre>/profile-<platform>.yaml` when it exists
   - otherwise use `<resolved_root>/<genre>/profile.yaml`
   - if the genre is represented by a standalone directory without platform specializations, use its `profile.yaml`
5. If the platform is 番茄 and the target bucket is set:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - treat the bucket as an upstream targeting choice, not as a replacement for genre
6. If state already records a historical relative path such as `shared/profiles/...`, preserve that path style in `genre_profile.loaded` unless the user explicitly asks to rewrite stored paths.
7. Read the chosen profile and extract only the fields needed downstream.
   - prefer writing the normalized projection that `../../scripts/profile_contract.py` with `--state-summary` would emit
8. Update `.mighty/state.json` so the project reflects the chosen profile.
   - if the user explicitly provides composite positioning inputs, also update:
     - `genre_profile.tagpacks`
     - `genre_profile.strong_tags`
     - `genre_profile.narrative_modes`
     - `genre_profile.tone_guardrails`
     - `genre_profile.positioning_sidecar`
9. Return a concise application summary and next-step guidance.

## State update requirements

When applying a profile, update at minimum:

- `meta.genre`
- `meta.platform` when the user explicitly changed platform
- `meta.updated_at`
- `genre_profile.loaded`
- `genre_profile.节奏`
- `genre_profile.爽点密度`
- `genre_profile.strand权重`
- `genre_profile.特殊约束`

When a Fanqie content bucket is explicitly chosen, also update:

- `genre_profile.bucket`

When composite positioning is explicitly chosen, also update:

- `genre_profile.tagpacks`
- `genre_profile.strong_tags`
- `genre_profile.narrative_modes`
- `genre_profile.tone_guardrails`
- `genre_profile.positioning_sidecar`

When the selected profile clearly defines platform pacing/word-count guidance, also refresh `platform_config` to keep it aligned with the chosen profile.

## Output expectations

### list

- concise table or bullet list of available genres

### show / detect

- current or detected genre
- detected bucket when applicable
- confidence when detection is involved
- selected profile path
- short summary of pacing and constraints

### apply

- applied genre
- applied bucket when applicable
- resolved profile root
- selected profile path
- whether a platform-specific profile was used
- which state fields changed
- recommended next step, usually `novel-write`, `novel-polish`, or `novel-outline`

## Notes

- Keep first-version detection conservative; prefer explicit project state over overconfident inference.
- For Fanqie buckets, prefer a human-readable bucket name such as `传统玄幻` over inventing a new opaque id.
- Do not try to recreate the old Hive Bee orchestration.
- If the requested genre does not exist, list valid choices instead of guessing.
- Use the smallest useful subset of profile fields in state; do not dump the full profile into `.mighty/state.json`.
