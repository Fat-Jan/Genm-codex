# 番茄 P0 输出契约

## 目标

让 `fanqie-p0-overlays/` 与 `fanqie-p0-checkcards/` 不只停留在“会读这些文档”，而是能稳定落进：

- `novel-review` 的输出摘要
- `novel-precheck` 的投稿前摘要
- 必要时的轻量 `chapter_meta` 写回

## 适用范围

仅在以下条件成立时启用：

- `platform = 番茄`
- 当前 `content_bucket` 或 `genre_profile.bucket` 命中 `fanqie-p0-overlays/` 与 `fanqie-p0-checkcards/` 中的对应 bucket

## 对 `novel-review`

当命中 Fanqie P0 bucket 时，review 输出可额外附加：

```md
fanqie_bucket_review_summary:
  bucket:
  bucket_grade:
  promise_match:
  first_three_status:
  primary_failure:
  top_red_flag:
  recommended_focus:
```

### 字段解释

- `bucket`
  - 当前命中的番茄 bucket
- `bucket_grade`
  - `pass / warn / fail`
- `promise_match`
  - 开篇 promise 是否和当前正文兑现情况一致
- `first_three_status`
  - 前三章交付状态，可写 `pass / weak / fail`
- `primary_failure`
  - 当前最主要的 bucket 级失败点
- `top_red_flag`
  - 当前最该优先修的红灯
- `recommended_focus`
  - 下一轮修订最该优先处理的一个方向

## 对 `novel-precheck`

当命中 Fanqie P0 bucket 时，precheck 输出可额外附加：

```md
fanqie_bucket_precheck_summary:
  bucket:
  submission_fit:
  opening_status:
  golden_three_status:
  packaging_alignment:
  top_blocker:
```

### 字段解释

- `bucket`
  - 当前命中的番茄 bucket
- `submission_fit`
  - 当前文本对该 bucket 的适配状态，可写 `fit / weak / off-route`
- `opening_status`
  - 开篇 promise 是否成立
- `golden_three_status`
  - 黄金三章交付状态
- `packaging_alignment`
  - 包装 promise 与正文是否一致
- `top_blocker`
  - 当前最影响投稿的 bucket 级阻断点

## 对 `chapter_meta`

如果 `novel-review` 已经明确识别出稳定的 bucket 级红灯，可轻量写回：

- `chapter_meta[N].fanqie_bucket_flags`
- `chapter_meta[N].fanqie_bucket_summary`

推荐形态：

```json
{
  "fanqie_bucket_flags": ["promise-mismatch", "golden-three-under-delivered"],
  "fanqie_bucket_summary": {
    "bucket": "职场婚恋",
    "bucket_grade": "warn",
    "primary_failure": "恋爱在走，职场没动",
    "top_red_flag": "career-line-too-thin"
  }
}
```

原则：

- 只记轻量结论，不存长段分析
- 只在问题明确时写，不要求每章都写
- 不新增顶层 state 中心
