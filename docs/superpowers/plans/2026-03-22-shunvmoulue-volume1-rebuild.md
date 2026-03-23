# 庶女谋略第一卷重修 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重写《庶女谋略》第一卷 `001-020` 章章纲到细纲级，并补齐第一卷正文所需的基础设定集，修正第001章身份确认逻辑。

**Architecture:** 以第一卷卷纲四段推进为骨架，先锁统一的人物变化口径和苏府规则层，再分批重写章纲。章纲重写遵循“场景链 + 账本变化 + 外部观感链”三层结构，设定集仅补当前写作刚需，避免提前膨胀后期世界构件。

**Tech Stack:** Markdown, repo-local novel project structure, outline files under `projects/庶女谋略/大纲`, setting files under `projects/庶女谋略/设定集`

---

### Task 1: Lock the first-volume rewrite frame

**Files:**
- Create: `docs/superpowers/specs/2026-03-22-shunvmoulue-volume1-rebuild-design.md`
- Modify: `projects/庶女谋略/大纲/卷纲/第一卷-庶女入局.md`

- [ ] Step 1: Normalize the first-volume structure into four five-chapter phases.
- [ ] Step 2: Encode the shared “病后变了” trigger and the difference between original-book vs current-version change direction.
- [ ] Step 3: Expand the volume outline so each phase has explicit conflict focus, payoff, and carry-over risk.
- [ ] Step 4: Re-read the volume outline and verify it can support all 20 chapter rewrites without contradictions.

Verification:
- Run: `sed -n '1,260p' 'projects/庶女谋略/大纲/卷纲/第一卷-庶女入局.md'`
- Expect: four phase blocks with clearer progression, not just terse summary bullets

### Task 2: Rebuild chapter 001-005 outlines

**Files:**
- Modify: `projects/庶女谋略/大纲/章纲/第001章.md`
- Modify: `projects/庶女谋略/大纲/章纲/第002章.md`
- Modify: `projects/庶女谋略/大纲/章纲/第003章.md`
- Modify: `projects/庶女谋略/大纲/章纲/第004章.md`
- Modify: `projects/庶女谋略/大纲/章纲/第005章.md`

- [ ] Step 1: Rewrite chapter 001 around multi-source identity verification rather than mirror recognition.
- [ ] Step 2: Add the pre-chapter humiliation/illness trigger as the shared basis for “她变了”.
- [ ] Step 3: Expand chapters 002-005 into scene-based outlines with clear offensive/defensive turns.
- [ ] Step 4: Ensure each chapter carries one visible gain and one escalating cost.
- [ ] Step 5: Verify the five chapters form a continuous mini-arc from waking to first backlash.

Verification:
- Run: `for f in projects/庶女谋略/大纲/章纲/第00{1,2,3,4,5}章.md; do echo "===== $f ====="; sed -n '1,240p' "$f"; done`
- Expect: each chapter has scene nodes, observable change markers, and clear next-chapter hook

### Task 3: Rebuild chapter 006-010 outlines

**Files:**
- Modify: `projects/庶女谋略/大纲/章纲/第006章.md`
- Modify: `projects/庶女谋略/大纲/章纲/第007章.md`
- Modify: `projects/庶女谋略/大纲/章纲/第008章.md`
- Modify: `projects/庶女谋略/大纲/章纲/第009章.md`
- Modify: `projects/庶女谋略/大纲/章纲/第010章.md`

- [ ] Step 1: Define the low-position alliance line through 林若雪 without flattening her into a helper tool.
- [ ] Step 2: Turn the father-attention line into conditional resource allocation rather than instant backing.
- [ ] Step 3: Build the public-space pressure sequence: rumor, seat order, meal scene, visible recalculation.
- [ ] Step 4: Land chapter 010 as a small-status shift rather than a decisive victory.
- [ ] Step 5: Verify the outside perception of “二姑娘变了” spreads from family members to servants and dependents.

Verification:
- Run: `for f in projects/庶女谋略/大纲/章纲/第00{6,7,8,9}章.md projects/庶女谋略/大纲/章纲/第010章.md; do echo "===== $f ====="; sed -n '1,240p' "$f"; done`
- Expect: chapters escalate from private friction to wider household recognition

### Task 4: Create chapter 011-015 fine outlines

**Files:**
- Create or Modify: `projects/庶女谋略/大纲/章纲/第011章.md`
- Create or Modify: `projects/庶女谋略/大纲/章纲/第012章.md`
- Create or Modify: `projects/庶女谋略/大纲/章纲/第013章.md`
- Create or Modify: `projects/庶女谋略/大纲/章纲/第014章.md`
- Create or Modify: `projects/庶女谋略/大纲/章纲/第015章.md`

- [ ] Step 1: Translate “父亲开始看见她” into concrete tests, errands, and scrutiny.
- [ ] Step 2: Make the new attention produce more hostility, not comfort.
- [ ] Step 3: Keep the conflict rooted in household order rather than shifting early into high-gate politics.
- [ ] Step 4: Ensure every chapter meaningfully changes at least one relationship ledger.
- [ ] Step 5: Verify the five-chapter block ends with the household clearly reclassifying 苏照棠 as a person to watch.

Verification:
- Run: `for f in projects/庶女谋略/大纲/章纲/第01{1,2,3,4,5}章.md; do echo "===== $f ====="; sed -n '1,240p' "$f"; done`
- Expect: a coherent mid-volume pressure block, not placeholder summaries

### Task 5: Create chapter 016-020 fine outlines

**Files:**
- Create or Modify: `projects/庶女谋略/大纲/章纲/第016章.md`
- Create or Modify: `projects/庶女谋略/大纲/章纲/第017章.md`
- Create or Modify: `projects/庶女谋略/大纲/章纲/第018章.md`
- Create or Modify: `projects/庶女谋略/大纲/章纲/第019章.md`
- Create or Modify: `projects/庶女谋略/大纲/章纲/第020章.md`

- [ ] Step 1: Introduce the marriage-position line through rumor, ranking, and evaluative talk.
- [ ] Step 2: Bind “高嫁未必是救命” to specific examples and fears, not abstract monologue.
- [ ] Step 3: Build volume-end pressure around future placement, not immediate escape fantasy.
- [ ] Step 4: End chapter 020 with a clear first-volume close and second-volume launch vector.
- [ ] Step 5: Verify the whole first volume now ends on “站稳半步，但代价更高”.

Verification:
- Run: `for f in projects/庶女谋略/大纲/章纲/第01{6,7,8,9}章.md projects/庶女谋略/大纲/章纲/第020章.md; do echo "===== $f ====="; sed -n '1,240p' "$f"; done`
- Expect: marriage pressure emerges as the next structural threat

### Task 6: Add first-volume writing-support settings

**Files:**
- Create: `projects/庶女谋略/设定集/世界观/时代与年号口径.md`
- Create: `projects/庶女谋略/设定集/家族/苏府家规与日常规矩.md`
- Create: `projects/庶女谋略/设定集/地点/苏府宅院结构与动线.md`
- Create: `projects/庶女谋略/设定集/家族/婚配礼制与议亲流程.md`
- Create: `projects/庶女谋略/设定集/势力/苏府人际关系账.md`

- [ ] Step 1: Lock time period, court/household phrasing, and everyday etiquette assumptions.
- [ ] Step 2: Document household rule points that create recurring first-volume pressure.
- [ ] Step 3: Map the physical movement paths inside 苏府 to support scene staging.
- [ ] Step 4: Document marriage negotiation flow so rumors and pressure points are consistent.
- [ ] Step 5: Build a relationship ledger that records who fears whom, who watches whom, and who changes stance when.

Verification:
- Run: `for f in 'projects/庶女谋略/设定集/世界观/时代与年号口径.md' 'projects/庶女谋略/设定集/家族/苏府家规与日常规矩.md' 'projects/庶女谋略/设定集/地点/苏府宅院结构与动线.md' 'projects/庶女谋略/设定集/家族/婚配礼制与议亲流程.md' 'projects/庶女谋略/设定集/势力/苏府人际关系账.md'; do echo \"===== $f =====\"; sed -n '1,260p' \"$f\"; done`
- Expect: each file answers concrete writing questions, not abstract slogans

### Task 7: Align chapter 001 prose with the new outline

**Files:**
- Modify: `projects/庶女谋略/chapters/第001章.md`
- Modify: `projects/庶女谋略/.mighty/state.json`

- [ ] Step 1: Rewrite the opening so identity recognition closes through objects, naming, and timeline cues.
- [ ] Step 2: Preserve the current chapter’s role as a fast opening while removing “look in mirror => know exact identity”.
- [ ] Step 3: Update summary/state fields only if the rewritten chapter materially changes tracked facts.
- [ ] Step 4: Verify the chapter still ends on the flower-garden appointment hook.

Verification:
- Run: `sed -n '1,260p' 'projects/庶女谋略/chapters/第001章.md'`
- Expect: credible identity confirmation chain and the same chapter-end forward motion

### Task 8: Perform structure and continuity checks

**Files:**
- Modify if needed: `projects/庶女谋略/.mighty/state.json`

- [ ] Step 1: Read back the volume outline, chapter outlines, settings, and chapter 001 as one continuous packet.
- [ ] Step 2: Check naming, age, rank, and relationship consistency against existing setting truths.
- [ ] Step 3: Check that “她变了” is externally visible but not personality replacement.
- [ ] Step 4: Check that no early chapter over-exposes the high-dimension game premise.
- [ ] Step 5: Record any residual risks for later正文 writing.

Verification:
- Run: `jq empty 'projects/庶女谋略/.mighty/state.json'`
- Expect: no JSON errors
- Run: `rg -n '照镜|铜镜|变了|婚配|月例' 'projects/庶女谋略/大纲/章纲' 'projects/庶女谋略/chapters/第001章.md' 'projects/庶女谋略/设定集'`
- Expect: mirror is no longer the sole identity proof; change/marriage/monthly stipend lines are traceable across files
