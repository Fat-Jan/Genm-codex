---
name: novel-review
description: Review a chapter in a Codex-managed novel project for quality, continuity, pacing, and reader pull, then record the findings back into project state.
---

# Novel Review

Use this skill after a chapter draft exists and the user wants a structured quality assessment.

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

- `.mighty/state.json`
- `chapters/第N章.md`
- relevant profile under `../../shared/profiles/`
- `../../shared/references/shared/core-constraints.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`

Read conditionally:

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
- `../../docs/strong-quality-gate-policy.json`

## Workflow

1. Read `.mighty/state.json`.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
   - determine explicit `tagpack` if provided
2. Read `../../shared/references/shared/core-constraints.md`.
3. Read `chapters/第N章.md`.
4. Read the genre/profile context.
   - also read `../../docs/anti-flattening-framework/README.md` and `../../docs/anti-flattening-framework/01-总纲.md`
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
   - treat them as third-layer review checks for:
     - title / hook promise carryover
     - golden-three delivery
     - character vividness
     - suspense handoff and map-shift smoothness
     - whether the chapter is fast but too smooth
     - whether key gains have visible resistance and cost
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
   - pacing
   - continuity
   - consistency
   - obvious AI-style issues
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
- `chapter_meta[chapter].needs_fix`

When the route is clear, also update:

- `chapter_meta[chapter].recommended_next_action`
- `chapter_meta[chapter].anti_flattening_flags` when the chapter shows clear cast / relation / faction imbalance

## Notes

- Prefer deterministic, evidence-based findings over vague style criticism.
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
