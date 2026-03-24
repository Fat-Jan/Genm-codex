# Fanqie P0 Smoke Draft: 广播站误放表白信那天，我和学神被迫参加学习互助

> 当前结果为 `draft`，并已执行轻量 writeback。

## 适用范围

- 项目：`projects/广播站误放表白信那天，我和学神被迫参加学习互助`
- bucket：`青春甜宠`
- review 样本章节：`003`
- precheck 样本范围：`001-003`

- confidence：`medium`
- evidence_count: `7`

## 证据来源

- `projects/广播站误放表白信那天，我和学神被迫参加学习互助/.mighty/state.json`
- `projects/广播站误放表白信那天，我和学神被迫参加学习互助/大纲/章纲/第003章.md`
- `projects/广播站误放表白信那天，我和学神被迫参加学习互助/chapters/第003章.md`
- `projects/广播站误放表白信那天，我和学神被迫参加学习互助/大纲/章纲/第001章.md`
- `projects/广播站误放表白信那天，我和学神被迫参加学习互助/chapters/第001章.md`
- `projects/广播站误放表白信那天，我和学神被迫参加学习互助/大纲/章纲/第002章.md`
- `projects/广播站误放表白信那天，我和学神被迫参加学习互助/chapters/第002章.md`

## 辅助信号

evidence_sources: 7
signals_used: learned_patterns, market_adjustments

## 手工 `novel-review` 样本

```md
fanqie_bucket_review_summary:
  bucket: 青春甜宠
  recommended_focus: 下一章要尽快把当前残账兑现成具体阻力，避免收益过满。
  bucket_grade: pass
  promise_match: pass
  first_three_status: pass
  primary_failure: none
  top_red_flag: none
```

## 手工 `novel-precheck` 样本

```md
fanqie_bucket_precheck_summary:
  bucket: 青春甜宠
  submission_fit: fit
  opening_status: pass
  golden_three_status: pass
  packaging_alignment: aligned
  top_blocker: none
```

## writeback 预览

```md
writeback_preview:
  chapter: 003
  fields: ['fanqie_bucket_flags', 'fanqie_bucket_summary']
  bucket: 青春甜宠
  confidence: medium
  status: written
```

## 结论

- 当前已写回 `chapter_meta["003"]` 的轻量 bucket 字段，writeback_status = `written`。
