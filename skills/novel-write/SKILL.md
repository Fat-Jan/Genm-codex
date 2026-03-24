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
- optional `skip_close`

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
- `../../shared/references/shared/core-constraints.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`
- `../../docs/opening-and-plot-framework/README.md`
- `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`

Read conditionally:

- `大纲/总纲.md` for main-arc alignment
- relevant `设定集/世界观/*.md`
- relevant supporting character files in `设定集/角色/`
- `.mighty/setting-gate.json`
- previous chapter file or summary
- `.mighty/workflow_state.json` when workflow safety must be checked before post-write auto-close
- `.mighty/learned-patterns.json`
- `.mighty/market-adjustments.json`
- current `learned_patterns` summary inside `.mighty/state.json`
- current `market_adjustments` summary inside `.mighty/state.json`
- `../../docs/fanqie-chapter-length-policy.json`
- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-mvp-tagpacks.yaml`
- `../../docs/fanqie-rule-priority-matrix.md`
- `../../docs/fanqie-resistance-and-cost-rules.md`
- `../../docs/gongdou-zhaidou-fault-funnel-review-card.md`
- `../../docs/strong-quality-gate-policy.json`
- `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
- `../../docs/anti-flattening-framework/04-角色动力系统.md`
- `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
- `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
- `../../docs/anti-flattening-framework/07-场景级群像推进.md`
- `../../docs/anti-flattening-framework/08-流派故障库.md`
- `../../docs/anti-flattening-framework/10-工具包与工作流.md`
- `../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
- `../../docs/opening-and-plot-framework/03-开篇故障与修正.md`
- `../../docs/opening-and-plot-framework/04-剧情层次模型.md`
- `../../docs/opening-and-plot-framework/05-推进链与残账设计.md`
- `../../docs/opening-and-plot-framework/06-题材特化接口.md`
- `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md`

## Workflow

1. Read `.mighty/state.json`.
   - determine `meta.platform`
   - determine explicit `content_bucket` if provided
   - otherwise treat current `genre_profile.bucket` as the active Fanqie content bucket when present
   - determine explicit `tagpack` if provided
2. Read `../../shared/references/shared/core-constraints.md`.
3. Read the target chapter outline from `大纲/章纲/第N章.md`.
4. Read required setting files from `设定集/`.
5. Read `../../docs/anti-flattening-framework/README.md` and `../../docs/anti-flattening-framework/01-总纲.md`.
   - also read `../../docs/opening-and-plot-framework/README.md` and `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
6. Load the shared profile matching the project genre from `../../shared/profiles/`.
7. Read any useful local guidance already present in the project:
   - prefer `.mighty/learned-patterns.json`
   - prefer `.mighty/market-adjustments.json`
   - if sidecar files are absent, fall back to `state.learned_patterns` / `state.market_adjustments`
   - when the active bucket is `宫斗宅斗`, explicitly inspect palace-specific adjustment ids when present:
     - `scan-surface-hook`
     - `scan-frontload-conflict`
     - `scan-kinship-truth-check`
8. When the chapter route is multi-character, multi-faction, relationship-heavy, politics-heavy, transmigration, system-driven, or the user explicitly asks for人物活人感/反脸谱化:
   - read:
     - `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
     - `../../docs/anti-flattening-framework/04-角色动力系统.md`
     - `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
     - `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
     - `../../docs/anti-flattening-framework/07-场景级群像推进.md`
     - `../../docs/anti-flattening-framework/08-流派故障库.md`
     - `../../docs/anti-flattening-framework/10-工具包与工作流.md`
   - use them as prose-side structural constraints for:
     - keeping supporting cast from collapsing into pure function roles
     - preserving non-protagonist goals in scenes
     - showing relation debt / power asymmetry where relevant
     - keeping gains earned through visible resistance and cost
     - leaving scene residue for the next chapter
9. When the chapter is in 1-3, or the request clearly depends on stronger opening pull, clearer multi-line progression, or chapter-level layering:
   - read:
     - `../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
     - `../../docs/opening-and-plot-framework/03-开篇故障与修正.md`
     - `../../docs/opening-and-plot-framework/04-剧情层次模型.md`
     - `../../docs/opening-and-plot-framework/05-推进链与残账设计.md`
     - `../../docs/opening-and-plot-framework/06-题材特化接口.md`
     - `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
     - `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md` when the active Fanqie bucket matches a P0 overlay file
   - use them as prose-side structure rules for:
     - keeping the opening promise legible on page in early chapters
     - avoiding background-first openings and pressure-only openings
     - making the chapter’s primary line and touched subline readable
     - ensuring an event also changes information, cost, or residue ledgers
10. If the platform is 番茄 and a bucket is explicitly given, or current `genre_profile.bucket` exists, or the task is clearly bucket-aware:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those as upstream prose constraints for:
     - opening speed
     - payoff timing
     - conflict density
     - chapter-end carryover
11. If Fanqie writing is active, also read:
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - `../../docs/fanqie-chapter-length-policy.json`
   - `../../docs/fanqie-resistance-and-cost-rules.md`
   - when the active bucket is `宫斗宅斗`, also read `../../docs/gongdou-zhaidou-fault-funnel-review-card.md`
   - use them as third-layer prose optimization rules for:
     - first-page hook clarity
     - golden-three delivery
     - character vividness
     - suspense handoff and map-shift smoothness
     - chapter-length baseline
     - visible resistance
     - visible cost
     - partial payoff instead of frictionless resolution
     - when the active bucket is `宫斗宅斗`, run a lightweight funnel preflight before drafting:
       - lock one effective transaction unit with a concrete contested object
       - ensure the chapter will change at least one of power / information / relationship / resource ledgers
       - ensure one non-protagonist role carries an independent agenda in the core scene
       - block summary-only progression, threat-only carryover, and authority-only shortcut wins
     - when palace-specific adjustments exist, additionally enforce:
       - `scan-surface-hook`
         - front-load婚配错位 / 赐婚 / 和离 / 高门关系压力 in the first visible movement when the route depends on them
       - `scan-frontload-conflict`
         - do not postpone the first meaningful反击 / 换账 if this chapter is part of the opening pressure unit
       - `scan-kinship-truth-check`
         - reject convenient relation words or称谓 that the current household truth sheet cannot support
   - do not let writing-technique rules override canon, chapter purpose, or active bucket
12. If an explicit `tagpack` is given, or the request clearly asks for a tag-pack route such as `恶女`:
   - read `../../docs/fanqie-mvp-tagpacks.yaml`
   - prefer a tagpack whose `base_bucket` matches the active `content_bucket`
   - treat the chosen tagpack as a second-layer overlay on top of the bucket, not as a replacement for the bucket
13. Load high-value shared references from `../../shared/references/` only as needed.
14. Before drafting, check `.mighty/setting-gate.json`.
   - if it is missing, stale relative to the current outline pass, or not in `passed` status, stop before writing
   - route back to `setting gate(outline)`:
     - preferred helper: `python3 scripts/setting_gate.py <project_root> --stage outline`
   - do not bypass this gate just because the relevant facts seem obvious from recent context
15. Before drafting, run a strong pre-write source gate when the chapter clearly depends on kinship truth, office truth, world rules, era-sensitive objects, decor, rites, or household rules.
   - read `../../docs/strong-quality-gate-policy.json`
   - treat it as the single rule source for required truth files
   - if the required truth source is missing, stop before writing
   - report the blocking gap explicitly and route the user to the smallest upstream action such as:
     - `novel-setting`
     - `novel-character`
     - `novel-scan` only when external research is truly needed
   - do not hallucinate missing truth just to satisfy the chapter
16. If a previous chapter exists, read the prior chapter summary or chapter file for continuity.
17. Write `chapters/第N章.md` aligned to:
   - current state
   - target chapter outline
   - genre/platform expectations
   - learned style preferences when they are concrete
   - learned avoid-patterns when they are concrete
   - project-local market suggestions when they are relevant and low-risk
   - active Fanqie bucket constraints when they exist
   - active resistance/cost constraints when they exist:
     - key gain must meet visible resistance
     - visible cost must remain on page
     - major alliance or evidence should not arrive frictionlessly
     - chapter-end win should usually leave residual risk
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
   - active anti-flattening rules when they exist:
     - supporting characters should not only appear as buttons or mouthpieces
     - at least one meaningful non-protagonist intention should stay visible in a key scene when the route needs群像
     - important gains should leave relation, risk, or cost residue
     - relation or faction support should not read as frictionless auto-alignment
   - active opening-and-plot rules when they exist:
     - in early chapters, the opening promise should be legible before background explanation takes over
     - opening chapters should not only stack pressure; they should show at least one visible exchange, misread, or ledger change
     - the chapter should make its primary line readable and avoid letting every change collapse into one flat event stream
     - important progress should leave information, relation, risk, or cost residue for the next chapter
   - when the active bucket is `宫斗宅斗` and the funnel card is active:
     - do not let the chapter pass as summary-only progression
     - make the contested object, blocker, and changed ledger legible on page
     - avoid resolving the chapter mainly through one authority shortcut
     - keep at least one key non-protagonist role from collapsing into pure delivery or reaction
     - if `scan-surface-hook` exists, keep the opening conflict legible on page instead of hiding it in background exposition
     - if `scan-frontload-conflict` exists, close the chapter after at least one concrete pressure->counter exchange
     - if `scan-kinship-truth-check` exists, keep kinship / title words consistent with the truth sheet even in dialogue shorthand
     - and, when Fanqie chapter-length policy exists:
       - if `word_count` is not explicitly provided, treat the current bucket's preferred chapter range as the default target
18. Update `.mighty/state.json` with:
   - `progress.current_chapter`
   - `progress.total_words`
   - `progress.last_write_chapter`
   - `progress.last_write_time`
   - `chapter_meta`
   - `chapter_snapshots`
   - `summaries_index`
19. Do not write review scores here unless an actual review step was run.
20. After the base write succeeds, attempt a guarded automatic `novel-close` by default.
    - run this only for a normal single-chapter `novel-write`
    - do not inherit this behavior into `novel-batch`
    - if `skip_close=true`, do not attempt auto-close and report that it was intentionally skipped
    - otherwise attempt `novel-close` only when all guards pass:
      - `.mighty/state.json` exists
      - `大纲/章纲/第N章.md` exists
      - the chapter file was written successfully
      - current workflow state is not clearly failed or malformed when workflow state exists
      - the user did not explicitly request a write-only pass
    - if guards fail, do not fake execution; report the exact skip reason
    - if auto-close fails after the chapter was written, keep the write as successful and report the post-write close failure clearly
21. After a real writing round, the preferred maintenance hook remains:
    - `scripts/post-task-maintenance.py <project_root> --trigger write`
    which should call the maintenance chain for `setting gate(write-post)`, stable entities, runtime guidance, and state thinning.
    - maintenance is not the place where prose mutation or `novel-close` execution should live

## 宫斗宅斗路线的宫廷市场调整

### 触发条件
- 先确认显式输入的 `content_bucket`，再依赖 `.mighty/state.json` 中的 `genre_profile.bucket`（或 `meta.genre`）来判定当前路线是否属于宫斗宅斗。只要 bucket 是 `宫斗宅斗`，或者 genre 里有 “宫斗”、“宅斗” 之类关键词并且故事明显围绕古代家族权力/婚配/嫡庶冲突展开，就把当前任务视为宫斗宅斗；否则不再消费 palace-specific adjustments。
- 仅在上述判定成立时，才尝试加载 palace-specific 市场调整：优先读取 `.mighty/market-adjustments.json` 的调整列表，文件缺失时再回退到 `.mighty/state.json -> market_adjustments` 的 summary/pointer。只处理 `id` 为 `scan-surface-hook`、`scan-frontload-conflict`、`scan-kinship-truth-check` 的条目，其它 bucket 也能读通用市场建议，但这三条不能跨桶生效。

### 写作约束
- `scan-surface-hook`：要求写作在首章或前三章明确交代强钩子，突出身份反差、赐婚/婚配错位、位阶冲突或其他高概念元素，并把“钩子交易单元”写成有物件/场景的组合。不仅在开头预告，也要在章纲里指明具体的段落/动作负责这个钩子（比如第一章通过赐婚书/封官令展开钩子冲突）。
- `scan-frontload-conflict`：在写作中把陷害/压制等主要冲突简明地放入首轮剧情单元，并让反击或策略回应在相邻段落完成，避免只写受压后拖延到后面。还要在章纲里明确冲突段落、反击动作、收益/信息节点之间的节奏链条，让编写时不会跳过这一“压迫→反击→初步收益”路径。
- `scan-kinship-truth-check`：在写任何嫡庶、赐婚、位阶、家权等关系词之前，预先读取或补全相关 truth sheet（至少包括 `设定集/家族/宅门真值表.md`、`设定集/家族/小型家谱.md`，必要时也要查 `设定集/官制/官职真值表.md`），并把关系真值转化成可查证事实（如“嫡长女代表正室血脉，庶妹同父异母”）。章纲与章节内容也要标注这些词的真值来源，避免因外延词汇违反既定真值。

### 备选情况
- 如果 palace-specific adjustments 只写在 `state.market_adjustments` 的 summary/pointer 中，只要 summary 里有关于钩子、前置冲突或亲族真值的提示，就按上述逻辑执行。当前线路不属于宫斗宅斗或未提供该组 id 时，此段直接跳过。

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
- optional write summary including:
  - whether auto-close was attempted
  - whether it ran or was skipped
  - route used or skip reason when available

## Failure handling

- If `.mighty/state.json` is missing, stop and route back to `novel-init`.
- If the target chapter outline is missing, stop and route back to `novel-outline`.
- If continuity-critical state is ambiguous, prefer using the existing state file over guessing from prose.
- Do not invent new top-level state sections unless strictly required.

## Notes

- Keep writing aligned to the outline and current state.
- Strong write-time blocking rules must resolve from `../../docs/strong-quality-gate-policy.json`, not from duplicated prose thresholds in this skill.
- Do not invent structural state fields ad hoc; prefer extending the existing `.mighty/state.json` shape conservatively.
- Treat learned-pattern sidecar data as a preference signal, not a hard rule.
- Treat market-adjustment sidecar data as packaging or pacing guidance, not as a reason to break canon or outline purpose.
- Opening-and-plot rules should improve开篇承诺、层次清晰度和推进账本, but they should not override canon, bucket law, or the already-frozen chapter purpose.
- `novel-write` does not inline `review -> route -> re-review`; guarded post-write convergence should hand off to `novel-close`.
- When Fanqie rules stack, apply them in this order:
  1. canon / state / chapter outline
  2. active bucket
  3. anti-flattening structure rules
  4. writing-technique optimization
  5. tagpack overlay
- When Fanqie bucket constraints are active, use them to tighten chapter rhythm and hook delivery, not to override canon, chapter purpose, or already established plot logic.
- When Fanqie resistance rules are active, prefer fast scenes with earned gains over frictionless automatic progression.
- If a first-batch MVP bucket config exists, prefer its reader-motive and payoff style over generic bucket language.
- If a matching tagpack exists, use it as a second-layer style/positioning overlay after bucket selection, not as a substitute for the bucket.
- Anti-flattening rules should make people and factions act like real participants in the chapter, but they do not authorize changing the outline goal or smuggling a rewrite into ordinary writing.
- When the active bucket is `宫斗宅斗`, the funnel card should be used as a light preflight, not as a full review pass; it is there to stop thin transaction skeletons from becoming finished chapters.
