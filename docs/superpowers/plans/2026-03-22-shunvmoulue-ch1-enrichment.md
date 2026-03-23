# 庶女谋略第001章丰满化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不推进第002章和第003章正文的前提下，把《庶女谋略》第001章写得更丰满，并锁住黄金三章的节奏分工。

**Architecture:** 先用黄金三章分工明确第001章的边界，再对第001章做“压迫感 + 心理转向 + 场景起落”三合一增强。重写后第001章承担判断与立局功能，不吞掉第002章的公开亮相戏，也不吞掉第003章的继母定性戏。

**Tech Stack:** Markdown, repo-local novel project files under `projects/庶女谋略`, state tracking in `.mighty/state.json`

---

### Task 1: Lock golden-three boundaries

**Files:**
- Create: `docs/superpowers/specs/2026-03-22-shunvmoulue-ch1-golden-three-design.md`
- Modify if needed: `projects/庶女谋略/大纲/章纲/第001章.md`
- Modify if needed: `projects/庶女谋略/大纲/章纲/第002章.md`
- Modify if needed: `projects/庶女谋略/大纲/章纲/第003章.md`

- [ ] Step 1: Confirm chapter 001 only carries judgment and setup, not public payoff.
- [ ] Step 2: Confirm chapter 002 carries first public deviation from the old script.
- [ ] Step 3: Confirm chapter 003 is a “定性章”, not a full war chapter.
- [ ] Step 4: Adjust chapter-outline wording only if current phrasing risks overlap.

Verification:
- Run: `sed -n '1,220p' 'projects/庶女谋略/大纲/章纲/第001章.md'`
- Run: `sed -n '1,220p' 'projects/庶女谋略/大纲/章纲/第002章.md'`
- Run: `sed -n '1,220p' 'projects/庶女谋略/大纲/章纲/第003章.md'`
- Expect: each chapter has a distinct role with no duplicated payoff

### Task 2: Rebuild chapter 001 internal arc

**Files:**
- Modify: `projects/庶女谋略/chapters/第001章.md`

- [ ] Step 1: Expand the wake-up section with more concrete bodily aftermath from punishment and fever.
- [ ] Step 2: Keep identity verification multi-source and credible.
- [ ] Step 3: Strengthen 小桃’s role as both exposition carrier and first witness of change.
- [ ] Step 4: Add more concrete pressure residues from the previous night without writing a full flashback chapter.
- [ ] Step 5: Clarify why “not going to the garden” equals surrendering interpretive control.
- [ ] Step 6: End with a stronger transition from West Courtyard to the larger household order.

Verification:
- Run: `sed -n '1,320p' 'projects/庶女谋略/chapters/第001章.md'`
- Expect: fuller single-chapter arc with stronger bodily pressure, clearer emotional turns, and preserved chapter-end hook

### Task 3: Sync minimal state updates

**Files:**
- Modify: `projects/庶女谋略/.mighty/state.json`

- [ ] Step 1: Update word count and summary if chapter length or tracked facts change.
- [ ] Step 2: Preserve current project status without falsely advancing later chapters.
- [ ] Step 3: Verify JSON validity.

Verification:
- Run: `jq empty 'projects/庶女谋略/.mighty/state.json'`
- Expect: no JSON errors

### Task 4: Continuity check against golden-three pacing

**Files:**
- Modify if needed: `projects/庶女谋略/chapters/第001章.md`

- [ ] Step 1: Check that chapter 001 does not include actual garden confrontation.
- [ ] Step 2: Check that father does not appear in person in chapter 001.
- [ ] Step 3: Check that 王氏 does not formally enter the stage yet.
- [ ] Step 4: Check that chapter 001 ends with anticipation, not payoff.

Verification:
- Run: `rg -n '苏文渊|王氏|花园|赴约' 'projects/庶女谋略/chapters/第001章.md'`
- Expect: references exist, but no full payoff scenes from chapters 002 or 003 are pre-consumed
