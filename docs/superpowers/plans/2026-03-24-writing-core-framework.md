# Writing Core Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land a minimal `写作基本功 / 剧情层次 / 内容标准` method-doc bundle as a repo-local single source of truth, wire it into the default novel workflow, keep memory persistence compressed, and expose the new bundle as packaging input instead of course notes.

**Architecture:** Reuse the proven `docs/ + skill wiring + lightweight state` pattern instead of inventing a new skill or a parallel state center. Add one new framework directory for the missing `基本功 / 内容标准 / packaging input` pieces, explicitly bridge it to the already-finished `opening-and-plot-framework` for `剧情层次`, and keep persistence limited to small actionable signals in `learned_patterns` and `chapter_meta`.

**Tech Stack:** Markdown workflow docs, skill contracts in `SKILL.md`, shared state schema/template docs, Python `unittest`, shell validation via `scripts/validate-migration.sh`

---

### Task 1: Lock The New Framework Boundary Before Writing Files

**Files:**
- Modify: `docs/superpowers/plans/2026-03-24-writing-core-framework.md`
- Read: `docs/opening-and-plot-framework/README.md`
- Read: `docs/anti-flattening-framework/README.md`
- Read: `docs/fanqie-writing-techniques.md`
- Read: `docs/research/fanqie/fanqie-writer-zone-lessons.md`

- [ ] **Step 1: Freeze the single-source decision**

Decide that:
- `剧情层次` keeps `docs/opening-and-plot-framework/` as the existing truth source
- the new framework fills only the missing layers:
  - `写作基本功`
  - `内容标准`
  - `memory 压缩信号约定`
  - `开篇包装输入接口`

- [ ] **Step 2: Freeze the directory name**

Recommended path:

- `docs/writing-core-framework/`

Reason:
- broad enough to include craft + standards + memory contract
- avoids renaming or duplicating `opening-and-plot-framework`
- matches the repo's existing “framework under docs” pattern

- [ ] **Step 3: Freeze module inventory**

Recommended minimal v1 files:

- `docs/writing-core-framework/README.md`
- `docs/writing-core-framework/01-写作基本功总纲.md`
- `docs/writing-core-framework/02-叙述-镜头-信息投放.md`
- `docs/writing-core-framework/03-对白-动作-情绪-段落节奏.md`
- `docs/writing-core-framework/04-剧情层次与多线编排接口.md`
- `docs/writing-core-framework/05-内容标准与常见失格.md`
- `docs/writing-core-framework/06-精品审核与投稿前判断.md`
- `docs/writing-core-framework/07-memory-压缩信号约定.md`
- `docs/writing-core-framework/08-开篇包装输入接口.md`

### Task 2: Add A Red Test For Framework Presence And Contract Wiring

**Files:**
- Create: `tests/test_writing_core_framework.py`

- [ ] **Step 1: Write the failing test**

Add checks for:
- new framework file inventory exists
- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-precheck`
- `novel-package`
- `novel-learn`
  all reference the new framework where appropriate

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_writing_core_framework -v`

Expected:
- FAIL because the directory and path references do not exist yet

- [ ] **Step 3: Keep the scope tight**

Do not test prose content quality. Only test:
- file existence
- expected path references
- state-schema mention of compressed signals
- entry-doc exposure

### Task 3: Create The Missing Project-Layer Docs

**Files:**
- Create: `docs/writing-core-framework/README.md`
- Create: `docs/writing-core-framework/01-写作基本功总纲.md`
- Create: `docs/writing-core-framework/02-叙述-镜头-信息投放.md`
- Create: `docs/writing-core-framework/03-对白-动作-情绪-段落节奏.md`
- Create: `docs/writing-core-framework/04-剧情层次与多线编排接口.md`
- Create: `docs/writing-core-framework/05-内容标准与常见失格.md`
- Create: `docs/writing-core-framework/06-精品审核与投稿前判断.md`
- Create: `docs/writing-core-framework/07-memory-压缩信号约定.md`
- Create: `docs/writing-core-framework/08-开篇包装输入接口.md`

- [ ] **Step 1: Write README as the operator entry**

README must state:
- this framework is not a course dump
- `剧情层次` reuses `docs/opening-and-plot-framework/`
- this framework covers:
  - basic craft
  - content standard
  - compressed memory signal contract
  - package-facing opening input

- [ ] **Step 2: Write the two craft-core docs**

`01-写作基本功总纲.md` should define:
- basic craft is about readable execution, not abstract literary commentary
- craft checks must surface in `write / review / precheck`

`02-叙述-镜头-信息投放.md` should define:
- scene anchoring
- viewpoint stability
- how much information can be front-loaded
- when explanation becomes drag

- [ ] **Step 3: Write the sentence-and-scene execution doc**

`03-对白-动作-情绪-段落节奏.md` should define:
- dialogue should carry conflict or relation shift
- action beats should prevent floating talking heads
- emotion should be shown through scene consequence, not only labels
- paragraph rhythm should help reading speed instead of summarizing the chapter

- [ ] **Step 4: Write the plot-layer bridge doc**

`04-剧情层次与多线编排接口.md` should:
- point to `docs/opening-and-plot-framework/04-剧情层次模型.md`
- point to `docs/opening-and-plot-framework/05-推进链与残账设计.md`
- define what downstream skills should consume from plot layering:
  - primary line
  - touched subline
  - carryover debt
  - chapter-level multi-line reminder

- [ ] **Step 5: Write the content-standard docs**

`05-内容标准与常见失格.md` should compress current signals into executable failure classes such as:
- background-first opening
- floating dialogue
- summary-replacing-drama
- frictionless gain
- false tension without ledger change
- overpromise relative to near-term payoff

`06-精品审核与投稿前判断.md` should define:
- what counts as “can keep reading”
- what counts as “can submit”
- what counts as “package overpromises”
- what should route to `fix` vs `rewrite` vs `precheck fail`

- [ ] **Step 6: Write the memory and packaging interface docs**

`07-memory-压缩信号约定.md` should define only small reusable signals, for example:
- `opening_strategy`
- `multi_line_guardrails`
- `content_standard_alerts`
- `writing_style_preferences`
- `avoid_patterns`

`08-开篇包装输入接口.md` should define what `novel-package` can consume from the writing-core layer:
- opening method cue
- genre-difference cue
- premium-review cue
- overpromise warning
- payoff timing reminder

### Task 4: Wire The Six Consumer Skills

**Files:**
- Modify: `skills/novel-outline/SKILL.md`
- Modify: `skills/novel-write/SKILL.md`
- Modify: `skills/novel-review/SKILL.md`
- Modify: `skills/novel-precheck/SKILL.md`
- Modify: `skills/novel-package/SKILL.md`
- Modify: `skills/novel-learn/SKILL.md`

- [ ] **Step 1: Wire `novel-outline`**

Add conditional reads for:
- `README.md`
- `04-剧情层次与多线编排接口.md`
- `08-开篇包装输入接口.md` only when outline-side promise shaping matters

Use them for:
- chapter-level line ownership
- opening promise legibility
- multi-line reminders that should survive into writing

- [ ] **Step 2: Wire `novel-write`**

Add conditional reads for:
- `01-写作基本功总纲.md`
- `02-叙述-镜头-信息投放.md`
- `03-对白-动作-情绪-段落节奏.md`
- `05-内容标准与常见失格.md`

Use them for:
- avoiding explanation-first drafting
- avoiding floating dialogue
- avoiding summary-compression in scene slots

- [ ] **Step 3: Wire `novel-review`**

Add conditional reads for:
- `01`
- `02`
- `03`
- `05`
- `06`
- `07`

Use them for:
- review findings language
- optional compressed writeback suggestion
- route decisions tied to content-standard failure type

- [ ] **Step 4: Wire `novel-precheck`**

Add conditional reads for:
- `05-内容标准与常见失格.md`
- `06-精品审核与投稿前判断.md`
- `08-开篇包装输入接口.md`

Use them for:
- submission-fit judgment
- packaging-needs-update judgment
- opening promise vs actual delivery judgment

- [ ] **Step 5: Wire `novel-package`**

Add reads for:
- `06-精品审核与投稿前判断.md`
- `08-开篇包装输入接口.md`

Use them for:
- converting “开篇方法 / 类型化开篇差异 / 精品审核标准” into packaging constraints
- preventing titles, synopsis, and opening-hook copy from promising what chapters 1-3 cannot carry

- [ ] **Step 6: Wire `novel-learn`**

Add reads for:
- `07-memory-压缩信号约定.md`

Use it to keep learning outputs compressed and stable instead of turning learned signals into theory dumps.

### Task 5: Formalize The Memory Contract Without Growing State

**Files:**
- Modify: `shared/references/shared/state-schema.md`
- Modify: `shared/templates/state-v5-template.json`
- Modify: `docs/state-thinning-and-setting-sync.md`

- [ ] **Step 1: Document allowed compressed signals**

Add explicit wording that the new framework stores only:
- lightweight learned-pattern summaries
- lightweight chapter-level reminders
- lightweight content-standard warnings

- [ ] **Step 2: Keep top-level state unchanged**

Do not add a new top-level framework block.

Preferred locations:
- `.mighty/learned-patterns.json`
- `state.learned_patterns` summary / pointer
- `chapter_meta[N]` optional lightweight fields

- [ ] **Step 3: Add only small optional keys**

Recommended optional additions:
- `learned_patterns.opening_strategy`
- `learned_patterns.multi_line_guardrails`
- `learned_patterns.content_standard_alerts`
- `chapter_meta[N].content_standard_flags`
- `chapter_meta[N].packaging_alignment_note`

Only land them if they can stay short, stable, and downstream-consumable.

### Task 6: Expose The New Fact In Entry Docs

**Files:**
- Modify: `README.md`
- Modify: `docs/start-here.md`
- Modify: `docs/skill-usage.md`
- Modify: `docs/default-workflows.md`

- [ ] **Step 1: Add the new framework entry**

Mention:
- `docs/writing-core-framework/README.md`

- [ ] **Step 2: Clarify the stack order**

Recommended order:
1. canon / state / bucket law
2. `opening-and-plot-framework`
3. `writing-core-framework`
4. `anti-flattening-framework`
5. local technique flavor

- [ ] **Step 3: Keep single-source wording explicit**

Say directly that:
- `剧情层次` lives primarily in `opening-and-plot-framework`
- the new framework adds execution craft, content standard, memory contract, and packaging-input rules

### Task 7: Verify With The Cheapest Useful Loop

**Files:**
- Modify: `progress.md`
- Modify: `findings.md`
- Modify: `task_plan.md` only if this work is adopted as an active implementation track

- [ ] **Step 1: Run the new targeted test**

Run: `python -m unittest tests.test_writing_core_framework -v`

Expected:
- PASS after wiring

- [ ] **Step 2: Run structure validation**

Run: `bash scripts/validate-migration.sh`

Expected:
- PASS

- [ ] **Step 3: Run one focused manual smoke**

Recommended smoke chain:
- `novel-package`
- `novel-precheck`

Project candidates:
- `projects/宗门垫底那年，我把废丹卖成了天价`
- `projects/离婚冷静期那天，前夫把董事会席位押给了我`

Expected evidence:
- package output references opening promise + payoff timing + overpromise guard
- precheck output can explain whether packaging should tighten

### Task 8: Stop At The Minimal 1.0 Boundary

**Files:**
- No new files beyond those listed above

- [ ] **Step 1: Do not duplicate plot-layer theory**

Do not rewrite the whole `opening-and-plot-framework` into the new framework.

- [ ] **Step 2: Do not store course notes in memory**

Do not add long lecture text to:
- `.mighty/state.json`
- `.mighty/learned-patterns.json`
- `chapter_meta`

- [ ] **Step 3: Do not expand into a platform encyclopedia**

Keep v1 to:
- one new framework directory
- six skill wires
- lightweight memory contract
- one package/precheck smoke
