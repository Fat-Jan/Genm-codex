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
  - `anti-flattening`

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
- `../../shared/references/shared/core-constraints.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`
- `../../docs/opening-and-plot-framework/README.md`
- `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
- `../../docs/writing-core-framework/README.md`
- `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`

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
- `../../docs/fanqie-resistance-and-cost-rules.md`
- `../../docs/anti-flattening-framework/02-叙事权与主角特权.md`
- `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
- `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
- `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
- `../../docs/anti-flattening-framework/08-流派故障库.md`
- `../../docs/anti-flattening-framework/11-检查清单与评分规约.md`
- `../../docs/anti-flattening-framework/12-案例对照与校准.md`
- `../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
- `../../docs/opening-and-plot-framework/03-开篇故障与修正.md`
- `../../docs/opening-and-plot-framework/04-剧情层次模型.md`
- `../../docs/opening-and-plot-framework/05-推进链与残账设计.md`
- `../../docs/opening-and-plot-framework/06-题材特化接口.md`
- `../../docs/writing-core-framework/05-内容标准与常见失格.md`
- `../../docs/writing-core-framework/06-精品审核与投稿前判断.md`
- `../../docs/writing-core-framework/08-开篇包装输入接口.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
- `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-checkcards/<bucket>.md`
- `../../shared/references/writing/ancient-household-kinship-guide.md`
- `../../shared/references/writing/ancient-office-hierarchy-guide.md`
- `../../shared/profiles/<genre>/profile-<platform>.yaml`

## Shared profile resolution

If the project already has `meta.genre` and `meta.platform`, and a matching shared profile exists, use it as a rubric reference.

Resolve shared profile roots in this order:

1. `shared/profiles/`
2. `../../shared/profiles/`

## Workflow

1. Parse the requested platform and chapter range.
2. Read `.mighty/state.json`.
3. Read `../../shared/references/shared/core-constraints.md`.
4. Read the target chapters.
5. Read `../../docs/anti-flattening-framework/README.md` and `../../docs/anti-flattening-framework/01-总纲.md`.
   - also read `../../docs/opening-and-plot-framework/README.md` and `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
   - also read `../../docs/writing-core-framework/README.md`
   - also read `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
   - when `.mighty/launch-stack.json` exists, consume launch-side `precheck_risks` and surface any `drift_signal`
6. When the route is multi-character, multi-faction, politics-heavy, relationship-heavy, transmigration/system-heavy, or the user explicitly asks for反脸谱化预检:
   - read:
     - `../../docs/anti-flattening-framework/02-叙事权与主角特权.md`
     - `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
     - `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
     - `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
     - `../../docs/anti-flattening-framework/08-流派故障库.md`
     - `../../docs/anti-flattening-framework/11-检查清单与评分规约.md`
     - `../../docs/anti-flattening-framework/12-案例对照与校准.md`
6a. When the range includes chapters 1-3, or the user explicitly asks for开篇/剧情层次预检:
   - read:
     - `../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
     - `../../docs/opening-and-plot-framework/03-开篇故障与修正.md`
     - `../../docs/opening-and-plot-framework/04-剧情层次模型.md`
     - `../../docs/opening-and-plot-framework/05-推进链与残账设计.md`
     - `../../docs/opening-and-plot-framework/06-题材特化接口.md`
     - `../../docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
     - `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
     - `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md` when the active Fanqie bucket matches a P0 overlay file
     - `../../docs/opening-and-plot-framework/fanqie-p0-checkcards/<bucket>.md` when the active Fanqie bucket matches a P0 checkcard file
6b. When the precheck needs stronger execution or submission judgment:
   - read:
     - `../../docs/writing-core-framework/05-内容标准与常见失格.md`
     - `../../docs/writing-core-framework/06-精品审核与投稿前判断.md`
     - `../../docs/writing-core-framework/08-开篇包装输入接口.md`
   - use them to judge:
     - whether current prose is scene-based enough for submission
     - whether packaging is overpromising current delivery
     - whether current opening promise and near-term payoff timing are aligned
5. If the range includes chapters 1-3, run a stronger “golden three” check:
   - hook arrival speed
   - protagonist presence
   - first conflict
   - payoff or hook continuity
7. Check platform fit using:
   - current project platform
   - matching shared profile if available
   - lightweight platform heuristics
   - project-local `market_adjustments` when they exist
   - Fanqie bucket constraints when `platform=番茄` and a bucket is provided, or when current `genre_profile.bucket` exists, or when the task is clearly bucket-aware
   - when no explicit `content_bucket` input is provided, treat `genre_profile.bucket` as the current active bucket
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - if an explicit `tagpack` is given, or the task clearly asks for a tag-pack route such as `恶女`, also read `../../docs/fanqie-mvp-tagpacks.yaml`
   - when the active bucket is `宫斗宅斗`, explicitly inspect palace-specific adjustment ids when present:
     - `scan-surface-hook`
     - `scan-frontload-conflict`
     - `scan-kinship-truth-check`
8. If Fanqie precheck is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - `../../docs/fanqie-resistance-and-cost-rules.md`
   - use them as third-layer precheck rules for:
     - title / synopsis promise consistency
     - opening-hook front-loading
     - golden-three delivery
     - character vividness
     - suspense handoff
     - resistance / cost / residual-risk visibility
     - bucket-specific submission red flags before generic softness notes
     - packaging promise vs actual opening delivery
     - when the active bucket is `宫斗宅斗`, also treat palace-specific adjustments as concrete precheck lenses:
       - `scan-surface-hook`
         - has the chapter range actually front-loaded婚配错位 / 赐婚 / 和离 / 高门关系冲突
       - `scan-frontload-conflict`
         - do chapters 1-3 complete at least one压迫->反击 / 压迫->换账 loop
       - `scan-kinship-truth-check`
         - are relation words still consistent with household truth files across title / synopsis / outline /正文
   - do not let writing-technique rules override canon or active bucket
9. Check quality and editorial risk:
   - whether the opening promise is visible enough in chapters 1-3
   - whether chapters 1-3 contain a real first exchange or first payoff instead of pressure-only motion
   - whether the range can clearly name its primary line and touched secondary line
   - whether major movement changes only events, or also changes information / relation / cost / residue ledgers
   - pacing softness
   - payoff density
   - weak suspense carryover
   - sparse review coverage
   - protagonist privilege overload or all-problems-solved-by-main-character risk
   - whether key supporting roles still behave like independent people
   - whether relations or factions have collapsed into a single voice
   - whether major gains are too smooth, too cheap, or too unopposed
   - whether chapter length has fallen below the active Fanqie baseline
   - drift from already learned local style preferences when that drift is obvious
   - if the bucket is ancient-family-power, check relation-schema risk:
     - 嫡庶是否能回到明确法统
     - `二姑娘 / 三姑娘` 等齿序称谓是否闭合
     - outward packaging relation words是否和正文真值一致
   - if the text depends on ancient office hierarchy, check office-schema risk:
     - 官名、品秩、实权是否分清
     - 是否存在跨代混用
     - 地方 / 东宫 / 内廷 / 外朝权力链是否错位
   - if Fanqie resistance rules are active, check:
     - 推进是否过顺
     - 证据是否过于自动上门
     - 同盟是否达成过快
     - 胜利是否没有代价或残留风险
   - if strong quality gate is active, check:
     - whether the chapter range is already carrying unresolved hard blockers from the same policy
     - whether submission should be blocked until those hard blockers are cleared
10. Check obvious AI-risk signals conservatively:
   - repetitive filler phrasing
   - explanation-heavy clusters
   - symmetry / generic phrasing if clearly present
11. Check outward-facing originality risk conservatively:
   - title / synopsis / protagonist name是否存在明显高相似度风险
   - if the project is submission-facing and naming/title checks were not run, say so directly
12. Return a structured report:
   - overall readiness
   - must-fix items
   - should-fix items
   - strongest positives
   - optional anti-flattening note
   - when the active bucket matches a Fanqie P0 bucket, optionally include `fanqie_bucket_precheck_summary` with:
     - bucket
     - submission_fit
     - opening_status
     - golden_three_status
     - packaging_alignment
     - top_blocker
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

## 宫斗宅斗路线的宫廷市场调整检查

### 触发条件
- 先检查显式输入的 `content_bucket`，再依赖 `.mighty/state.json` 中的 `genre_profile.bucket`（或 `meta.genre`）来判定是否属于宫斗宅斗。只有当 bucket 直接等于 `宫斗宅斗`、或者 genre 字段含有“宫斗”、“宅斗”等关键词并且章节明显在处理古代家族/嫡庶/婚配/权谋冲突时，才把当前检查流程视为 palace route，否则直接跳过下面的 palace-specific check。
- 当触发条件成立后，优先读取 `.mighty/market-adjustments.json`，缺失时回退到 `state.market_adjustments` 的 summary/pointer，并只看 `id` 是 `scan-surface-hook`、`scan-frontload-conflict`、`scan-kinship-truth-check` 的记录。其他 bucket 仍然可以读取通用市场调整，但这三条不能跨桶参考。

### 检查项
- `scan-surface-hook`：检查首章或所请求范围内是否明确展现身份反差、赐婚/婚配错位、位阶冲突等钩子，并且第一章或前三章已经安排了具体的钩子交易单元（如赐婚书/封官令/权力位阶对抗）。如果章节或 outline 里没有 hooking 结果，就标记 `hook` 相关 warning。
- `scan-frontload-conflict`：查验章节是否至少在第一轮冲突单元同时出现压迫/陷害与回应/反击，并在报告中指出冲突段落、反击段落及其收益/信息节点。如果出现拖延、只写受压或反击在后续章节才出现，提前提示“冲突前置/反击缺失”。
- `scan-kinship-truth-check`：检查是否先行读取或补齐 `设定集/家族/宅门真值表.md`、`设定集/家族/小型家谱.md`（必要时含 `设定集/官制/官职真值表.md`），并在具体 relation 词汇出现前确认真值。报告中需明确指出每个嫡庶/婚配/位阶词汇的真值来源，防止词汇与真值脱节。

### 备选情况
- 如果 palace-specific adjustments 仅存在于 `state.market_adjustments` 的 summary/pointer，只要 summary 提供了钩子、冲突或亲族真值的提示，就按上述检查处理。若当前路线不属宫斗宅斗或缺少这组 id，则该小节直接不做检查。

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
- 反脸谱化风险
- 内容桶适配
- 包装状态
- 投稿建议

Use `✅ / ⚠️ / ❌` style summaries when helpful.
- Opening-and-plot rules should support opening strength, layering, and progression judgment, but they should not override canon or active bucket law.

## Notes

- This is not a legal or policy compliance guarantee.
- Be conservative: only flag issues you can support from the text.
- When strong-gate policy is present, use it to justify hard submission blockers without re-copying the threshold table into this skill.
- If there is too little data for a reliable decision, say so directly and recommend a narrower precheck or more review first.
- When Fanqie rules stack, evaluate in this order:
  1. canon / state / actual chapter text
  2. active bucket fit
  3. anti-flattening structure fit
  4. writing-technique fit
  5. tagpack fit
- Treat `market_adjustments` as soft platform-fit hints, not as a reason to override the actual chapter text.
- Treat Fanqie content-bucket constraints as upstream targeting rules, not as proof that the project already fits that bucket.
- If a first-batch MVP bucket config exists, prefer its `precheck_focus` over generic bucket commentary.
- If a matching tagpack exists, use it as a second-layer precheck lens, not as a replacement for the bucket.
- If anti-flattening issues are strong enough to imply hollow support cast, fake faction conflict, or protagonist privilege overload, surface them before cosmetic prose notes.

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
- canon / kinship contradictions make current relation-word packaging unsafe
- title / name similarity risk is unresolved
- office-title / power-chain contradictions make current官名包装 unsafe
