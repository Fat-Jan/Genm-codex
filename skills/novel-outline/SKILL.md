---
name: novel-outline
description: Generate or refine the total outline and chapter outline files for a Codex-managed novel project using the shared profiles, references, and current project state.
---

# Novel Outline

Use this skill after project initialization, or when the user wants to generate or revise the story outline.

Also read `../../docs/00-当前有效/upstream-structure-contract.md` and treat `shared/templates/project/creative-brief.md` as the preferred lightweight project-brief input when the project has not yet stabilized its core premise.

## Inputs

- `mode`: `total` or `chapter`
- optional `start`
- optional `count`
- optional `content_bucket`
- optional multi-option request

## Preconditions

- `.mighty/state.json` exists
- `设定集/` exists
- `大纲/` exists
- Shared assets exist:
  - `../../shared/profiles/`
  - `../../shared/references/`
  - `../../shared/templates/`

## Required shared reads

Read `../../shared/references/shared/consumer-read-manifest.md` first.

Shared bundles to apply here:

- `baseline-core`
- `launch-stack`
- `content-positioning`
- `fanqie-bucket`

Always read:

- `../../shared/references/shared/core-constraints.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`
- `../../docs/opening-and-plot-framework/README.md`
- `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
- `../../docs/writing-core-framework/README.md`
- `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
- `../../docs/opening-and-plot-framework/fanqie-launch-stack/05-compiler-contract.md`

## Conditional reads

Read these when they exist, and prioritize them for ancient-family-power routes:

- `设定集/家族/宅门真值表.md`
- `设定集/家族/小型家谱.md`
- `设定集/官制/官职真值表.md`
- `设定集/官制/权力层级图.md`
- `.mighty/content-positioning.json`

Also read these when generating or materially revising outlines, especially for multi-character, multi-faction, romance, politics, transmigration, or “活人感/反脸谱化” requests:

- `../../docs/anti-flattening-framework/02-叙事权与主角特权.md`
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
- `../../docs/writing-core-framework/04-剧情层次与多线编排接口.md`
- `../../docs/writing-core-framework/08-开篇包装输入接口.md`
- `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
- `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md`

## Workflow

1. Read `.mighty/state.json` for `meta.title`, `meta.genre`, `meta.platform`, and current `genre_profile.bucket` when present.
   - if no explicit `content_bucket` input is provided, treat `genre_profile.bucket` as the active Fanqie content bucket
   - if `.mighty/content-positioning.json` exists, treat it as the preferred project-facing composite-positioning sidecar
   - treat `state.genre_profile` as the primary runtime projection for profile-derived rhythm/constraint hints
2. Read `../../shared/references/shared/core-constraints.md`.
   - also read `../../docs/anti-flattening-framework/README.md` and `../../docs/anti-flattening-framework/01-总纲.md`
   - also read `../../docs/opening-and-plot-framework/README.md` and `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
   - also read `../../docs/writing-core-framework/README.md`
   - also read `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md` and `../../docs/opening-and-plot-framework/fanqie-launch-stack/05-compiler-contract.md`
   - if `.mighty/launch-stack.json` exists, prefer its current launch-side compiler hints over recomputing a separate launch guess inside this skill
3. Load the relevant shared profile for rhythm and reader expectations.
   - first prefer the lightweight projection already present in `state.genre_profile`
   - only if additional detail is still needed, inspect the raw profile via `../../scripts/profile_contract.py`
   - when using raw profile detail, follow the contract layers:
     - core profile
     - platform overlay when it exists
     - bucket overlay when it exists
     - reference files for long-form guidance
   - do not treat arbitrary embedded long-form sections in raw profile YAML as authoritative core config
   - when doing total-outline generation or any outline refinement that clearly depends on人物立体度、群像关系、阵营冲突、穿书/穿越/系统/权谋等高风险题材，also read:
     - `../../docs/anti-flattening-framework/02-叙事权与主角特权.md`
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
     - `../../docs/writing-core-framework/04-剧情层次与多线编排接口.md`
     - `../../docs/writing-core-framework/08-开篇包装输入接口.md` when the outline pass is also shaping outward opening promise
     - `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
     - `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md` when the active Fanqie bucket matches a P0 overlay file
   - use them as outline-side structure rules for:
     - opening promise and first-three delivery shape
     - first conflict / first payoff placement when opening strength matters
     - primary line vs touched subline clarity
     - event, information-gap, cost, and residue chaining
     - protagonist privilege boundaries
     - role tier allocation
     - independent character motives
     - relation / faction splits
     - conflict, information-gap, and cost loops
     - scene-level residual consequence design
     - chapter-level line ownership and touched-subline reminders
     - opening promise shaping that should survive into writing and packaging without overpromising
   - when content-positioning exists, also apply:
     - `narrative_modes` as outline-side structure overlays
     - `tone_guardrails` as route filters
     - `strong_tags` only as emphasis cues, not as equal-priority bucket replacements
4. If the platform is 番茄 and a `content_bucket` is explicitly given, or a current `genre_profile.bucket` exists, or the user clearly asks for Fanqie-first outline refinement:
   - read `../../docs/fanqie-content-buckets.md`
   - read `../../docs/fanqie-bucket-constraints.md`
   - if the current bucket is one of the first-batch MVP buckets, prefer reading `../../docs/fanqie-mvp-buckets.yaml`
   - use `../../docs/fanqie-mvp-bucket-templates.md` as a fallback explanatory reference
   - treat those bucket rules as upstream outline constraints, not as mere packaging hints
5. If Fanqie outline constraints are active, also read:
   - `../../docs/fanqie-content-data-layer.md`
   - `../../docs/fanqie-writing-techniques.md`
   - `../../docs/fanqie-rule-priority-matrix.md`
   - `../../docs/fanqie-resistance-and-cost-rules.md`
   - project-local `.mighty/market-adjustments.json` when it exists
   - when the active bucket is `宫斗宅斗` or another ancient-family-power route, also read `../../shared/references/writing/ancient-household-kinship-guide.md`
   - when the project涉及朝堂/东宫/地方官场/军政/封爵，也 read `../../shared/references/writing/ancient-office-hierarchy-guide.md`
   - use them only as outline-side optimization rules for:
     - first-page hook clarity
     - golden-three payoff timing
     - suspense handoff
     - map-shift smoothness
     - outline recommendation patterns
     - kinship / birth-order consistency
     - office / power-chain consistency
     - resistance / cost / partial-payoff design
   - when the active bucket is `宫斗宅斗`, explicitly consume palace-specific adjustment ids when present:
     - `scan-surface-hook`
       - front-load婚配错位 / 赐婚 / 和离 / 权臣高门关系冲突 into total-outline premise and first 1-3 chapter hooks
     - `scan-frontload-conflict`
       - ensure the opening chapter group contains at least one visible pressure->counter or pressure->ledger-shift unit
     - `scan-kinship-truth-check`
       - do not freeze outward relation words in total outline or chapter outline until household truth files can support嫡庶 / 齿序 / 婚配法统
   - do not let writing-technique rules override outline law or active bucket
6. If this is an ancient-family-power route and either kinship file is missing:
   - create `设定集/家族/宅门真值表.md` from `../../shared/templates/project/ancient-household-truth-sheet.md` or a minimal equivalent
   - create `设定集/家族/小型家谱.md` from `../../shared/templates/project/ancient-mini-genealogy.md` or a minimal equivalent
   - report that the route has been forced into a truth-first flow
7. If this is an ancient-family-power route and the story clearly depends on court / palace / local-office / military rank logic:
   - create `设定集/官制/官职真值表.md` from `../../shared/templates/project/ancient-office-truth-sheet.md` or a minimal equivalent
   - create `设定集/官制/权力层级图.md` from `../../shared/templates/project/ancient-power-ladder.md` or a minimal equivalent
   - report that the route has been forced into an office-truth flow
8. For `mode=total`:
   - create or update `大纲/总纲.md`
   - include hook, premise, main conflict, arc direction, and ending direction
   - when opening-and-plot rules are active, explicitly lock:
     - opening promise
     - first-three chapter exchange / payoff path
     - main line and the most important supporting line
     - which early gain should leave residual risk
   - when anti-flattening rules are active, explicitly lock:
     - protagonist privilege boundary
     - role tiers for core cast / important support / functional roles
     - at least one relation-structure tension per core relation cluster
     - at least one intra-faction route split where the story uses factions or alliances
     - conflict cost and residual-risk shape for major arc wins
   - when `narrative_modes` contains values such as `多主题副本` or `多角色群像`, also explicitly lock:
     - 副本切换的主入口
     - 当前章群像里的 active mover / defender / 独立议程
     - 多主题推进不应吃掉主桶 promise
   - when bucket constraints are active, also align:
     - opening speed
     - payoff cycle
     - bucket-style conflict density
     - title / synopsis promise consistency
     - title-pattern and outline-pattern consistency when Fanqie content-data-layer signals exist
      - resistance / cost patterns when Fanqie resistance rules are active
      - if the bucket is ancient-family-power, explicitly lock:
        - minimal household schema
        - protagonist mother source
        - opponent relation source
        - daughter / son birth-order map when `二姑娘` or similar terms appear
        - core office-title schema when title / synopsis / conflict depends on官场 or宫廷权力
   - if the kinship files are still mostly empty, write a provisional total outline and clearly mark which relation words are not yet safe to freeze into packaging
   - if the office truth files are still mostly empty, do not freeze官场权力型承诺 as final wording
9. For `mode=chapter`:
   - create `大纲/章纲/第N章.md`
   - include chapter goal, conflict, reveal, hook, and continuity notes
   - when opening-and-plot rules are active, also include:
     - the chapter’s primary line
     - which secondary line is touched but not fully resolved
     - when the chapter is in 1-3, where the opening conflict and first exchange land on page
     - what residue, debt, or unsettled question carries into the next chapter
   - when anti-flattening rules are active, also include:
     - active mover / defender in the key scene
     - which supporting role or opposing role has an independent agenda in the chapter
     - the likely misread / information gap driving the scene
     - the relationship, risk, or cost residue left for the next chapter
   - when bucket constraints are active, also align:
     - current bucket’s opening rule
     - current bucket’s payoff timing
     - current bucket’s pacing density
     - current bucket’s ending or carryover expectation
     - current bucket’s primary reader motive when a first-batch MVP template exists
     - current bucket’s tag pack when a first-batch MVP template exists
     - current data-layer `opening_patterns`
     - current data-layer `golden_three_expectation`
     - current data-layer `handoff_patterns`
     - current data-layer `resistance_patterns`
     - current data-layer `cost_patterns`
     - current data-layer `partial_payoff_patterns`
   - if the chapter depends on ancient-family-power kinship logic, keep chapter称谓 consistent with the truth sheet even when the broader total outline is still provisional
   - if palace-specific adjustments exist, the chapter outline should also make explicit:
     - where the first婚配/位阶 pressure point lands on page
     - which ledger changes in the chapter
     - which relation word or称谓 has already passed truth-sheet validation
   - if the chapter depends on office hierarchy, keep官名、节制链、称呼 consistent with the office truth sheet even when the broader total outline is still provisional
10. Keep chapter outlines specific enough for writing, but short enough to maintain.
11. If the user asks for multiple options, present 2-3 outline variants before locking one in.
12. After a real outline pass, run `setting gate(outline)`:
   - preferred helper: `python3 scripts/setting_gate.py <project_root> --stage outline`
   - use it as a hard gate before writing
   - let it do local-first setting enrichment and write `.mighty/setting-gate.json`
   - if the gate result is `blocked`, stop before handing off to `novel-write`
   - if the gate queues high-risk review items, report them explicitly instead of pretending the project is ready to draft
13. Report which outline files were created or updated, whether `setting gate(outline)` passed, and mention the bucket when one was used.
   - if anti-flattening rules were active, also mention the main structural locks or warnings applied

## 宫斗宅斗路线的宫廷市场调整

### 触发条件
- 先检查显式输入 `content_bucket`，再回到 `.mighty/state.json` 中的 `genre_profile.bucket`。当任一项是 `宫斗宅斗`，或者 `meta.genre`/`genre_profile.bucket` 字段明显包含 “宫斗”、“宅斗” 等关键词，并且项目当前处于古代家族权力、嫡庶/婚配、朝堂权谋等线索上，就把当前路线判为宫斗宅斗；否则即便 `market_adjustments` 里存在 palace-specific id，该段调整也不应用。
- 仅在判定为宫斗宅斗后，才读取 `.mighty/market-adjustments.json`（优先），或者当该文件缺失时使用 `state.market_adjustments` 的 summary/指针。其他 bucket 仍然可以访问通用 `market_adjustments`，但下面三条 palace-specific id 不能跨桶生效：`scan-surface-hook`、`scan-frontload-conflict`、`scan-kinship-truth-check`。

### 约束释义
- `scan-surface-hook`：把包装/总纲/章纲前三章的钩子当作硬约束。总纲要提前写出身份反差、赐婚/婚配错位、权力位阶冲突等钩子元素，并在章纲里指明哪一段承担“高概念+低位冲突”的交易单元；如果已经出现赐婚书、封官诏那类物件，明确指出第一章或前三章的“钩子搏杀”节点。
- `scan-frontload-conflict`：要求章纲和写作流程把首轮冲突（陷害/压迫/权谋联动）与反击/反运作落在同一轮剧情中，不能只留单边压制。总纲在节奏刻度上要锁定“压制→反击→初步收益”链条，章纲需写清冲突地点、反击动作与收益/信息节点。
- `scan-kinship-truth-check`：在首次使用嫡庶/赐婚/位阶关系词前，强制读取或补齐 `设定集/家族/宅门真值表.md`、`设定集/家族/小型家谱.md`（必要时包括 `设定集/官制/官职真值表.md`），把关系真值写成可查证的事实（如“嫡长女坐正房，庶妹母亲是某豪门余血”），并在总纲/章纲/包装描述中注明真值来源，确保词汇和描述不会偏离设定。

### 备选情况
- 当 only `state.market_adjustments` 提供 summary/pointer 时，只要 summary 里提到钩子、前置冲突或亲族真值的提示，就照上述逻辑落地。若 palace-specific amendment 缺失或当前线路不属宫斗宅斗，该部分直接跳过。

## Output files

- `大纲/总纲.md`
- `大纲/章纲/第N章.md`
- for ancient-family-power routes, may also create or update:
  - `设定集/家族/宅门真值表.md`
  - `设定集/家族/小型家谱.md`
  - `设定集/官制/官职真值表.md`
  - `设定集/官制/权力层级图.md`

## Notes

- Treat `大纲/总纲.md` as the law for later writing steps.
- If the user asks for broad ideation, provide multiple outline options before locking one in.
- Do not generate chapter writing content here; this skill ends at outline artifacts.
- If Fanqie bucket rules are active, they should guide outline shape before packaging and before prose generation.
- Anti-flattening rules should improve人物、关系、阵营与后果结构, but cannot override canon, state truth, or active bucket law.
- Opening-and-plot rules should improve开篇承诺、层次清晰度与推进账本, but cannot override canon, state truth, or active bucket law.
- If ancient kinship constraints are active and the minimal household schema cannot be made self-consistent, stop short of a “final” outline and return the inconsistency first.
- For ancient-family-power routes, the preferred order is:
  1. household truth sheet
  2. mini genealogy
  3. office truth sheet
  4. power ladder
  5. total outline
  6. packaging
- When both Fanqie bucket constraints and writing-technique rules are active, apply them in this order:
  1. canon / state / total outline
  2. active bucket
  3. anti-flattening structure rules
  4. Fanqie content-data-layer guidance
  5. writing-technique optimization
  6. tagpack flavor if later requested downstream
- If a first-batch MVP bucket config exists, prefer its hook / payoff / carryover style over generic bucket phrasing.
