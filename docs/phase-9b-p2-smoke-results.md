# Phase 9B / P2 Smoke Results

## Target

Validate the next low-risk integration step:

- `novel-precheck`
- `novel-learn`

## Smoke 1: Precheck with learned + market signals

### Result

- pass

### What was directly observed

- the run stayed inside:
  - `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
- it explicitly read:
  - `.mighty/state.json`
  - `.mighty/market-data.json`
  - chapter texts `第001章` to `第004章`
  - related outlines
- it explicitly checked:
  - `learned_patterns_present = true`
  - `market_adjustments_present = true`
  - `market_adjustment_items = 3`
- it remained read-only

### Final reported conclusion

The concise rerun returned a stable user-facing conclusion:

- chapters 1-3 are ready enough as a strong opening batch
- chapter 4 still needs a clearer immediate payoff before a 1-4 batch submission
- learned patterns were actually used
- market adjustments were actually used
- final recommendation was:
  - publish 1-3 now, or
  - revise chapter 4 before publishing 1-4 together

### Practical conclusion

`novel-precheck` is no longer treating platform-fit as only profile heuristics. It is now demonstrably consuming both learned style signals and project-local market adjustments in its final recommendation.

---

## Smoke 2: Learn chapter 1-4 and save

### Result

- pass

### Observed behavior

- the run stayed inside:
  - `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
- it read:
  - `.mighty/state.json`
  - `第001章` to `第004章`
- it updated only the intended areas:
  - `learned_patterns.writing_style_preferences`
  - `learned_patterns.high_point_preferences`
  - `learned_patterns.avoid_patterns`
  - `auto_learn_config.last_auto_learn`
  - `auto_learn_config.last_auto_learn_chapter`

### Learned outputs now visible

- dialogue style became more concrete and downstream-usable
- description density became more scene-specific
- pacing preference became chapter-structure aware
- high-point preferences became more tactical and payoff-oriented
- avoid-patterns became more explicit for downstream polish / precheck use
- `last_auto_learn_chapter` advanced to `4`

### Practical conclusion

`novel-learn` is now producing outputs that are more directly consumable by:

- `novel-write`
- `novel-polish`
- `novel-precheck`

---

## Overall conclusion

- `novel-precheck`: pass
- `novel-learn`: pass

This is enough to confirm that the second integration layer of the quality loop is materially working.
