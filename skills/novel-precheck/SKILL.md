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
- optional `tagpack`
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
- `.mighty/learned-patterns.json`
- `.mighty/market-adjustments.json`
- `learned_patterns` summary inside `.mighty/state.json`
- `market_adjustments` summary inside `.mighty/state.json`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-mvp-tagpacks.yaml`
- `../../docs/fanqie-rule-priority-matrix.md`
- `../../docs/fanqie-chapter-length-policy.json`
- `../../docs/strong-quality-gate-policy.json`
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
   - if an explicit `tagpack` is given, or the task clearly asks for a tag-pack route such as `恶女`, also read `../../docs/fanqie-mvp-tagpacks.yaml`
6. If Fanqie precheck is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - use them as third-layer precheck rules for:
     - title / synopsis promise consistency
     - opening-hook front-loading
     - golden-three delivery
     - character vividness
     - suspense handoff
   - do not let writing-technique rules override canon or active bucket
7. Check quality and editorial risk:
   - pacing softness
   - payoff density
   - weak suspense carryover
   - sparse review coverage
   - whether chapter length has fallen below the active Fanqie baseline
   - drift from already learned local style preferences when that drift is obvious
   - if strong quality gate is active, check:
     - whether the chapter range is already carrying unresolved hard blockers from the same policy
     - whether submission should be blocked until those hard blockers are cleared
8. Check obvious AI-risk signals conservatively:
   - repetitive filler phrasing
   - explanation-heavy clusters
   - symmetry / generic phrasing if clearly present
9. Return a structured report:
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

When a matching tagpack exists, also check:

- whether the protagonist presentation matches the tagpack’s `protagonist_core`
- whether the chapter is serving the tagpack’s `reader_motive`
- whether the opening and ending are close to the tagpack’s hook expectations

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
- When strong-gate policy is present, use it to justify hard submission blockers without re-copying the threshold table into this skill.
- If there is too little data for a reliable decision, say so directly and recommend a narrower precheck or more review first.
- When Fanqie rules stack, evaluate in this order:
  1. canon / state / actual chapter text
  2. active bucket fit
  3. writing-technique fit
  4. tagpack fit
- Treat `market_adjustments` as soft platform-fit hints, not as a reason to override the actual chapter text.
- Treat Fanqie content-bucket constraints as upstream targeting rules, not as proof that the project already fits that bucket.
- If a first-batch MVP bucket config exists, prefer its `precheck_focus` over generic bucket commentary.
- If a matching tagpack exists, use it as a second-layer precheck lens, not as a replacement for the bucket.

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
