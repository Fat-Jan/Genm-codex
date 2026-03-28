---
name: novel-review
description: Review a chapter in a Codex-managed novel project for quality, continuity, pacing, and reader pull, then record the findings back into project state.
---

# Novel Review

Use this skill after a chapter draft exists and the user wants a structured quality assessment.

Also read `../../docs/00-当前有效/upstream-structure-contract.md` so review does not confuse `总纲`, `launch-stack`, and `content-positioning` responsibilities.

Default intent for the current workflow:

- collect the chapter’s actionable problems in one review pass
- prefer a single repair round over repeated micro-fixes
- if the chapter still has critical issues after two repair attempts, route up to `novel-rewrite`

## Inputs

- `chapter`
- optional `detail`
- optional `threshold`
- optional `content_bucket`
- optional `tagpack`

## Preconditions

- `.mighty/state.json` exists
- `chapters/第N章.md` exists
- Shared references exist:
  - `../../shared/references/`
  - relevant shared profile under `../../shared/profiles/`

## Required reads

Read `../../shared/references/shared/consumer-read-manifest.md` first.
Also read `../../docs/00-当前有效/quality-route-contract.md` for shared route language with `novel-precheck` / `novel-package`.

Shared bundles to apply here:

- `baseline-core`
- `launch-stack`
- `active-context`
- `content-positioning`
- `fanqie-bucket`
- `fanqie-tagpack`

- `.mighty/state.json`
- `chapters/第N章.md`
- relevant profile under `../../shared/profiles/`
- `../../shared/references/shared/core-constraints.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`
- `../../docs/opening-and-plot-framework/README.md`
- `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
- `../../docs/writing-core-framework/README.md`
- `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`

Read conditionally:

- `.mighty/active-context.json`
- `.mighty/content-positioning.json`
- previous chapter file or summary for continuity
- shared reference docs for reader-pull, pacing, and anti-AI constraints
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-mvp-tagpacks.yaml`
- `../../docs/fanqie-rule-priority-matrix.md`
- `../../docs/fanqie-resistance-and-cost-rules.md`
- `../../docs/gongdou-zhaidou-fault-funnel-review-card.md`
- `../../docs/anti-flattening-framework/02-叙事权与主角特权.md`
- `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
- `../../docs/anti-flattening-framework/04-角色动力系统.md`
- `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
- `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
- `../../docs/anti-flattening-framework/07-场景级群像推进.md`
- `../../docs/anti-flattening-framework/08-流派故障库.md`
- `../../docs/anti-flattening-framework/09-诊断信号与快速修复.md`
- `../../docs/anti-flattening-framework/11-检查清单与评分规约.md`
- `../../docs/anti-flattening-framework/12-案例对照与校准.md`
- `../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
- `../../docs/opening-and-plot-framework/03-开篇故障与修正.md`
- `../../docs/opening-and-plot-framework/04-剧情层次模型.md`
- `../../docs/opening-and-plot-framework/05-推进链与残账设计.md`
- `../../docs/opening-and-plot-framework/06-题材特化接口.md`
- `../../docs/writing-core-framework/01-写作基本功总纲.md`
- `../../docs/writing-core-framework/02-叙述-镜头-信息投放.md`
- `../../docs/writing-core-framework/03-对白-动作-情绪-段落节奏.md`
- `../../docs/writing-core-framework/05-内容标准与常见失格.md`
- `../../docs/writing-core-framework/06-精品审核与投稿前判断.md`
- `../../docs/writing-core-framework/07-memory-压缩信号约定.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
- `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-checkcards/<bucket>.md`
- `../../docs/strong-quality-gate-policy.json`

## Workflow

1. Read `.mighty/state.json`.
   - if `.mighty/active-context.json` exists, read it first as the preferred current-review sidecar before broad file expansion
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
   - determine explicit `tagpack` if provided
   - treat `state.genre_profile` as the primary runtime projection for profile-derived review context
   - if `.mighty/content-positioning.json` exists, treat it as the preferred project-facing composite-positioning sidecar
2. Read `../../shared/references/shared/core-constraints.md`.
3. Read `chapters/第N章.md`.
4. Read the genre/profile context.
   - first prefer the lightweight projection already present in `state.genre_profile`
   - only if additional detail is still needed, inspect raw profile data through `../../scripts/profile_contract.py`
   - when reading raw profile layers, use this order:
     - core profile
     - platform overlay when it exists
     - bucket overlay when it exists
     - reference files for long-form guidance
   - do not treat arbitrary embedded long-form sections in raw profile YAML as authoritative core config
   - also read `../../docs/anti-flattening-framework/README.md` and `../../docs/anti-flattening-framework/01-总纲.md`
   - also read `../../docs/opening-and-plot-framework/README.md` and `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
   - also read `../../docs/writing-core-framework/README.md`
   - also read `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
   - when `.mighty/launch-stack.json` exists, use it as an extra launch-side rubric and report `launch_alignment` / `drift_signal` when early-phase delivery明显偏离
   - when the chapter or request clearly depends on人物立体度、群像关系、阵营冲突、多视角、穿书/穿越/系统/权谋等题材风险, or when no explicit exemption is given for a lightweight pass, also read:
     - `../../docs/anti-flattening-framework/02-叙事权与主角特权.md`
     - `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
     - `../../docs/anti-flattening-framework/04-角色动力系统.md`
     - `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
     - `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
     - `../../docs/anti-flattening-framework/07-场景级群像推进.md`
     - `../../docs/anti-flattening-framework/08-流派故障库.md`
     - `../../docs/anti-flattening-framework/09-诊断信号与快速修复.md`
     - `../../docs/anti-flattening-framework/11-检查清单与评分规约.md`
     - `../../docs/anti-flattening-framework/12-案例对照与校准.md`
     - `../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
     - `../../docs/opening-and-plot-framework/03-开篇故障与修正.md`
     - `../../docs/opening-and-plot-framework/04-剧情层次模型.md`
     - `../../docs/opening-and-plot-framework/05-推进链与残账设计.md`
     - `../../docs/opening-and-plot-framework/06-题材特化接口.md`
     - `../../docs/writing-core-framework/01-写作基本功总纲.md`
     - `../../docs/writing-core-framework/02-叙述-镜头-信息投放.md`
     - `../../docs/writing-core-framework/03-对白-动作-情绪-段落节奏.md`
     - `../../docs/writing-core-framework/05-内容标准与常见失格.md`
     - `../../docs/writing-core-framework/06-精品审核与投稿前判断.md`
     - `../../docs/writing-core-framework/07-memory-压缩信号约定.md`
     - `../../docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
     - `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
     - `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md` when the active Fanqie bucket matches a P0 overlay file
     - `../../docs/opening-and-plot-framework/fanqie-p0-checkcards/<bucket>.md` when the active Fanqie bucket matches a P0 checkcard file
5. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as upstream review constraints for:
     - opening speed
     - payoff timing
     - conflict density
     - chapter-end carryover
6. If Fanqie review is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - `../../docs/fanqie-resistance-and-cost-rules.md`
   - when the active bucket is `宫斗宅斗`, also read `../../docs/gongdou-zhaidou-fault-funnel-review-card.md`
   - when the active bucket matches a Fanqie P0 bucket, also read `../../docs/opening-and-plot-framework/fanqie-p0-checkcards/<bucket>.md`
   - treat them as third-layer review checks for:
     - title / hook promise carryover
     - golden-three delivery
     - character vividness
     - suspense handoff and map-shift smoothness
     - whether the chapter is fast but too smooth
     - whether key gains have visible resistance and cost
     - bucket-specific structural red flags before generic commentary
     - when the active bucket is `宫斗宅斗`, run the funnel card as a strict first-pass gate:
       - effective transaction unit exists
       - the transaction changes at least one ledger
       - the chapter is not relying on authority-only shortcut resolution
       - the most function-like role is named when participants collapse into tools
   - do not let technique rules override canon or bucket law
7. If an explicit `tagpack` is given, or the request clearly asks for a tag-pack route such as `恶女`:
   - read `../../docs/fanqie-mvp-tagpacks.yaml`
   - prefer a tagpack whose `base_bucket` matches the active `content_bucket`
   - treat the chosen tagpack as a second-layer review lens after the bucket
8. Review for:
   - hook and reader pull
   - opening hook clarity and opening promise carryover when the chapter is in 1-3 or still serving the opening contract
   - whether the chapter is background-first, pressure-only, or missing a near-term exchange
   - pacing
   - continuity
   - consistency
   - obvious AI-style issues
   - plot layering clarity:
     - main line readability
     - touched subline readability
     - whether relationship / rule changes are actually legible as lines
   - progression effectiveness:
     - event movement
     - information-gap movement
     - cost movement
     - residual-risk movement
   - execution craft:
     - whether explanation is crowding out scene
     - whether dialogue is floating without action anchors
     - whether emotion is mostly label-based instead of consequence-based
     - whether paragraph rhythm has collapsed into summary
   - content-standard fit:
     - background-first opening
     - summary-replacing-drama
     - frictionless gain
     - overpromise relative to near-term payoff
   - protagonist privilege balance
   - character agency / role independence
   - relationship tension structure
   - faction divergence when factions or alliances are present
   - conflict / cost / consequence chain visibility
   - scene mobility: whether only the protagonist is allowed to act
   - genre fault control when the route is high-risk for flattening
   - bucket-fit when applicable
   - bucket template fit when a first-batch MVP template exists:
     - primary reader motive
     - payoff cycle
     - ending-hook rule
   - tagpack fit when a matching tagpack exists:
     - protagonist_core
     - reader_motive
     - opening_rule
     - ending_hook_rule
   - content-positioning fit when it exists:
     - 标签成立但主桶跑偏
     - 群像存在但主入口消失
     - 副本切换过快导致 promise 漂移
     - 轻松风味把代价链冲没了
   - resistance/cost fit:
     - evidence too automatic
     - alliance too easy
     - payoff too complete
     - residual risk too weak
   - when the active bucket is `宫斗宅斗`, funnel fit:
     - effective transaction unit
     - transaction realism
     - living participants instead of function roles
   - when the project uses the strong quality gate:
     - surface policy-backed hard blockers before softer style notes
     - do not contradict a known write-preflight / close-gate blocker with a casual “looks fine”
   - do not absorb deterministic post-write lint into vague editorial judgment; keep those findings separable so `novel-close` and `novel-fix` can consume them as explicit evidence
9. Before routing, collapse findings into at most `3` actionable issue clusters.
   - each cluster should map to one repair action family, not a one-line tweak
   - if multiple small issues live in the same paragraph / beat / scene, group them together
   - distinguish:
     - structural blockers
     - local repair items
     - language-layer cleanup items
10. Check repair-attempt history in `chapter_meta`.
   - treat `fix_count + polish_count` as the current repair-attempt total when present
   - if repair attempts are already `>= 2` and critical issues still remain, prefer `novel-rewrite`
11. Produce a structured report with:
   - total score
   - dimension scores
   - critical issues
   - warnings
   - suggested fixes
   - `issue_clusters`
   - optional `recent_guardrails` for the next chapter:
     - `must_avoid`
     - `must_preserve`
     - `next_chapter_watchpoints`
     - `expires_after_chapter`
   - optional `repair_pass_plan` with:
     - primary_route
     - cluster_order
     - clusters_to_finish_now
     - trivial_polish_can_be_absorbed_in_fix
   - optional `anti_flattening_summary` with:
     - protagonist_privilege_risk
     - cast_flattening_signals
     - faction_or_relation_failure
     - minimum viable repair direction
   - when the active bucket matches a Fanqie P0 bucket, optionally include `fanqie_bucket_review_summary` with:
     - bucket
     - bucket_grade
     - promise_match
     - first_three_status
     - primary_failure
     - top_red_flag
     - recommended_focus
   - when the active bucket is `宫斗宅斗`, also include `gongdou_funnel_summary` with:
     - funnel_grade
     - failed_layer
     - root_cause
     - changed_ledger
     - most_function_like_role
   - optional bucket-fit note
   - recommended next action:
     - `none`
     - `novel-fix`
     - `novel-polish`
     - `novel-rewrite`
12. Update review metadata for the chapter inside `.mighty/state.json`.
13. If the chapter falls below threshold, explicitly recommend `novel-rewrite`.

## Outputs

- review report in the response
- updated `.mighty/state.json`

## State update requirements

Update at minimum:

- `chapter_meta[chapter].review_score`
- `chapter_meta[chapter].review_grade`
- `chapter_meta[chapter].review_time`
- `chapter_meta[chapter].dimension_scores`
- `chapter_meta[chapter].issue_clusters`
- `chapter_meta[chapter].needs_fix`

When the route is clear, also update:

- `chapter_meta[chapter].recommended_next_action`
- `chapter_meta[chapter].anti_flattening_flags` when the chapter shows clear cast / relation / faction imbalance
- `chapter_meta[chapter].fanqie_bucket_flags` when the bucket-specific red flags are clear and stable
- `chapter_meta[chapter].fanqie_bucket_summary` when a short bucket-level summary would help downstream routing
- when useful, `chapter_meta[chapter].dimension_scores` may also include:
  - `开篇抓力`
  - `层次清晰度`
  - `推进有效性`
- when the chapter exposes a clear next-chapter correction signal, prefer writing a short-lived `recent_guardrails` block into `.mighty/learned-patterns.json` instead of bloating `state.json`

## Notes

- Prefer deterministic, evidence-based findings over vague style criticism.
- If you emit `recent_guardrails`, keep them short-lived and execution-facing; do not turn them into broad theory notes.
- Do not let a chapter settle into the state “high review score + empty `issue_clusters` + continue writing” when structural or language risks are still being described in prose; downstream consumers must be able to read the artifact, not infer hidden judgment.
- If the user asks for auto-fix, route the main rewrite request through `novel-rewrite`.
- If the user wants one bounded convergence pass rather than a review-only report, recommend `novel-close`.
- Do not claim a review passed unless the report actually shows the score and issues.
- Prefer `novel-fix` for narrow local issues, `novel-polish` for language-layer issues, and `novel-rewrite` for structural problems.
- Default review output should help a single repair round finish the chapter, not create a long tail of tiny follow-up edits.
- Do not emit many single-line fix tips when they can be merged into one issue cluster and solved together.
- When Fanqie rules stack, judge in this order:
  1. canon / state / chapter purpose
  2. active bucket fit
  3. anti-flattening structure fit
  4. writing-technique fit
  5. tagpack enhancement fit
- When Fanqie bucket constraints are active, use them to judge whether the chapter is delivering the expected click-through and carryover shape for that bucket, not to override canon or chapter purpose.
- Opening-and-plot rules should help judge开篇承诺、层次清晰度与推进账本, but should not override canon, bucket law, or the actual chapter purpose.
- If a first-batch MVP bucket config exists, prefer it over generic bucket commentary when judging fit.
- If a matching tagpack exists, use it as a second-layer lens on top of bucket fit, not as a new bucket.
- If anti-flattening findings point to protagonist privilege overload, hollow support cast, fake faction conflict, or zero-cost manipulation, surface them before cosmetic style notes.
- When the active bucket is `宫斗宅斗`, apply the funnel card before broad style commentary; if layer one fails, treat that as a structural failure rather than a mere pacing note.
- When strong-gate policy is present, treat it as the source of hard-block semantics; `novel-review` may explain and route around blockers, but should not redefine the blocker thresholds here.

## Route rules

Choose the primary route like this:

- `novel-fix`
  - local payoff weakness
  - one or two concrete issue clusters
  - no need to replace chapter purpose or ordering
  - for `宫斗宅斗`, a real transaction exists but is too thin, too smooth, or has one function-like role that can be repaired locally
  - prefer this route over `novel-polish` when both local content issues and trivial prose issues coexist; minor wording cleanup should be absorbed into the same repair round
- `novel-polish`
  - anti-AI cleanup
  - prose tightening
  - dialogue or description refinement
  - continuity remains structurally sound
  - language-layer cleanup is the primary remaining issue after local content is already sound
- `novel-rewrite`
  - chapter purpose is wrong
  - event ordering or hook structure has to be rebuilt
  - multiple major issues point to a structural failure, not a local repair
  - for `宫斗宅斗`, no effective transaction unit exists, or layer one of the funnel clearly fails
  - repair attempts are already `>= 2` and the chapter still has unresolved critical issues or still falls below threshold

If none of the above is needed, use `none`.
