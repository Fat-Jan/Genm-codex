---
name: novel-outline
description: Generate or refine the total outline and chapter outline files for a Codex-managed novel project using the shared profiles, references, and current project state.
---

# Novel Outline

Use this skill after project initialization, or when the user wants to generate or revise the story outline.

## Inputs

- `mode`: `total` or `chapter`
- optional `start`
- optional `count`
- optional `content_bucket`
- optional multi-option request

## Preconditions

- `.mighty/state.json` exists
- `大纲/` exists
- Shared assets exist:
  - `../../shared/profiles/`
  - `../../shared/references/`
  - `../../shared/templates/`

## Required shared reads

Always read:

- `../../shared/references/shared/core-constraints.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`

## Conditional reads

Read these when they exist, and prioritize them for ancient-family-power routes:

- `设定集/家族/宅门真值表.md`
- `设定集/家族/小型家谱.md`
- `设定集/官制/官职真值表.md`
- `设定集/官制/权力层级图.md`

Also read these when generating or materially revising outlines, especially for multi-character, multi-faction, romance, politics, transmigration, or “活人感/反脸谱化” requests:

- `../../docs/anti-flattening-framework/02-叙事权与主角特权.md`
- `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
- `../../docs/anti-flattening-framework/04-角色动力系统.md`
- `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
- `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
- `../../docs/anti-flattening-framework/07-场景级群像推进.md`
- `../../docs/anti-flattening-framework/08-流派故障库.md`
- `../../docs/anti-flattening-framework/10-工具包与工作流.md`

## Workflow

1. Read `.mighty/state.json` for `meta.title`, `meta.genre`, `meta.platform`, and current `genre_profile.bucket` when present.
   - if no explicit `content_bucket` input is provided, treat `genre_profile.bucket` as the active Fanqie content bucket
2. Read `../../shared/references/shared/core-constraints.md`.
   - also read `../../docs/anti-flattening-framework/README.md` and `../../docs/anti-flattening-framework/01-总纲.md`
3. Load the relevant shared profile for rhythm and reader expectations.
   - when doing total-outline generation or any outline refinement that clearly depends on人物立体度、群像关系、阵营冲突、穿书/穿越/系统/权谋等高风险题材，also read:
     - `../../docs/anti-flattening-framework/02-叙事权与主角特权.md`
     - `../../docs/anti-flattening-framework/03-角色分层与投入配额.md`
     - `../../docs/anti-flattening-framework/04-角色动力系统.md`
     - `../../docs/anti-flattening-framework/05-关系网络与阵营分歧.md`
     - `../../docs/anti-flattening-framework/06-冲突-信息差-后果链.md`
     - `../../docs/anti-flattening-framework/07-场景级群像推进.md`
     - `../../docs/anti-flattening-framework/08-流派故障库.md`
     - `../../docs/anti-flattening-framework/10-工具包与工作流.md`
   - use them as outline-side structure rules for:
     - protagonist privilege boundaries
     - role tier allocation
     - independent character motives
     - relation / faction splits
     - conflict, information-gap, and cost loops
     - scene-level residual consequence design
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
   - when anti-flattening rules are active, explicitly lock:
     - protagonist privilege boundary
     - role tiers for core cast / important support / functional roles
     - at least one relation-structure tension per core relation cluster
     - at least one intra-faction route split where the story uses factions or alliances
     - conflict cost and residual-risk shape for major arc wins
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
   - if the chapter depends on office hierarchy, keep官名、节制链、称呼 consistent with the office truth sheet even when the broader total outline is still provisional
10. Keep chapter outlines specific enough for writing, but short enough to maintain.
11. If the user asks for multiple options, present 2-3 outline variants before locking one in.
12. Report which outline files were created or updated, and mention the bucket when one was used.
   - if anti-flattening rules were active, also mention the main structural locks or warnings applied

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
