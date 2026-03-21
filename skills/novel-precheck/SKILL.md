---
name: novel-precheck
description: Run a read-only pre-submission check for a Codex-managed novel project by reviewing target chapters for platform-fit, hook strength, quality signals, and obvious risk areas.
---

# Novel Precheck

Use this skill when the user wants a submission-readiness check before posting or submitting a chapter range to a platform.

## Inputs

- `platform`
- `chapters`
- optional `content_bucket`
- optional focus:
  - `golden-three`
  - `quality`
  - `ai-risk`
  - `platform-fit`
  - `bucket-fit`

## Preconditions

- `.mighty/state.json` exists
- target chapter files exist

## First-version scope

This version is a read-only checker. It should:

- inspect chapter range quality
- compare against lightweight platform expectations
- flag obvious risks
- recommend whether to submit now or revise first

It should not:

- automate publishing
- claim legal/compliance certainty
- pretend to replace a human editorial review

## Required reads

Always read:

- `.mighty/state.json`
- requested `chapters/第NNN章.md`

Read conditionally:

- `大纲/总纲.md`
- `大纲/章纲/第NNN章.md`
- `设定集/角色/主角.md`
- `learned_patterns` inside `.mighty/state.json`
- `market_adjustments` inside `.mighty/state.json`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../shared/profiles/<genre>/profile-<platform>.yaml`
- `../../shared/profiles/<genre>/profile-<platform>.yaml`

## Shared profile resolution

If the project already has `meta.genre` and `meta.platform`, and a matching shared profile exists, use it as a rubric reference.

Resolve shared profile roots in this order:

1. `shared/profiles/`
2. `../shared/profiles/`
3. `../../shared/profiles/`

## Workflow

1. Parse the requested platform and chapter range.
2. Read `.mighty/state.json`.
3. Read the target chapters.
4. If the range includes chapters 1-3, run a stronger “golden three” check:
   - hook arrival speed
   - protagonist presence
   - first conflict
   - payoff or hook continuity
5. Check platform fit using:
   - current project platform
   - matching shared profile if available
   - lightweight platform heuristics
   - project-local `market_adjustments` when they exist
   - Fanqie bucket constraints when `platform=番茄` and a bucket is provided, or when current `genre_profile.bucket` exists, or when the task is clearly bucket-aware
   - when no explicit `content_bucket` input is provided, treat `genre_profile.bucket` as the current active bucket
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
6. Check quality and editorial risk:
   - pacing softness
   - payoff density
   - weak suspense carryover
   - sparse review coverage
   - drift from already learned local style preferences when that drift is obvious
7. Check obvious AI-risk signals conservatively:
   - repetitive filler phrasing
   - explanation-heavy clusters
   - symmetry / generic phrasing if clearly present
8. Return a structured report:
   - overall readiness
   - must-fix items
   - should-fix items
   - strongest positives
   - submission recommendation
   - packaging readiness
   - optional bucket-fit note

When the active bucket matches a first-batch MVP bucket such as `现实情感` or `宫斗宅斗`, make the bucket-fit note concrete by checking:

- whether the text is following the bucket’s `opening_rule`
- whether the chapter or chapter range is delivering the expected `payoff_cycle`
- whether the outward positioning matches the bucket’s `title_formula` / `synopsis_formula`
- whether the current text is actually serving the bucket’s `primary_reader_motive`

## Platform guidance

### 番茄

- faster hook
- direct conflict early
- visible short-term payoff
- stronger immediate pull

### 七猫

- denser爽点
- stronger direct conflict
- protagonist decisiveness

### 起点

- faster protagonist orientation
- stronger setting / premise clarity
- avoid drift and excess filler

### 晋江

- stronger emotional precision
- cleaner prose and character tone

## Output conventions

Prefer this shape:

- 基本信息
- 综合评估
- 必须修复
- 建议修复
- 优势
- 内容桶适配
- 包装状态
- 投稿建议

Use `✅ / ⚠️ / ❌` style summaries when helpful.

## Notes

- This is not a legal or policy compliance guarantee.
- Be conservative: only flag issues you can support from the text.
- If there is too little data for a reliable decision, say so directly and recommend a narrower precheck or more review first.
- Treat `market_adjustments` as soft platform-fit hints, not as a reason to override the actual chapter text.
- Treat Fanqie content-bucket constraints as upstream targeting rules, not as proof that the project already fits that bucket.
- If a first-batch MVP bucket config exists, prefer its `precheck_focus` over generic bucket commentary.

## Submission status conventions

Prefer one of these final labels:

- `ready-now`
- `revise-then-submit`
- `do-not-submit`

Also report:

- `packaging-needs-update: yes|no`

Use `packaging-needs-update: yes` when:

- current text has materially shifted away from existing packaging emphasis
- recent review findings imply the packaging is overpromising
- market-adjustment packaging advice is clearly not reflected in current outward positioning
