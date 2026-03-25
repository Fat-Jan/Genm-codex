# memory 压缩信号约定

## 目标

memory 层只沉淀下游技能能直接消费的小信号，不存整套课程，不存长段理论。

## 原则

1. 优先写入 `.mighty/learned-patterns.json`
2. `state.json` 只保留轻量摘要 / 指针
3. 章节级信号落在 `chapter_meta[N]`
4. 不为本框架新增平行顶层状态中心

## 推荐信号

### `learned_patterns`

- `writing_style_preferences`
- `high_point_preferences`
- `avoid_patterns`
- `opening_strategy`
- `multi_line_guardrails`
- `content_standard_alerts`
- `recent_guardrails`

### `chapter_meta[N]`

- `content_standard_flags`
- `packaging_alignment_note`

## 写法要求

### `opening_strategy`

只保留一两句能执行的描述，例如：

- `异常先行，首屏先见交易单元`
- `关系绑定先行，第二章前给第一次换账`

### `multi_line_guardrails`

只保留当前项目正在用的多线提醒，例如：

- `主线优先药田夺回，副线只轻触师门站位`

### `content_standard_alerts`

只保留重复出现的失格提醒，例如：

- `避免背景先行`
- `避免悬浮对白`

### `recent_guardrails`

只保留当前下一章最值得执行的短期 guardrails，必须保持轻量、可过期、可替换。

推荐字段：

- `must_avoid`
- `must_preserve`
- `next_chapter_watchpoints`
- `expires_after_chapter`

示例：

```json
{
  "must_avoid": ["不要再回滑到解释腔"],
  "must_preserve": ["赔付到账后的代价感"],
  "next_chapter_watchpoints": ["下一章必须留下新的关系残账"],
  "expires_after_chapter": 5
}
```

约束：

- `recent_guardrails` 只服务近一两章，不升级成长期风格理论
- 默认保存在 `.mighty/learned-patterns.json`
- `state.json` 只保留 sidecar 摘要 / 指针，不复制整段 guardrails
- 新的 review 证据可以替换旧的 `recent_guardrails`
- `novel-learn` 不应因为参考文本学习而覆盖仍在生效的短期 guardrails

### `content_standard_flags`

只在单章失格明确时写，例如：

- `background-first`
- `floating-dialogue`
- `summary-replacing-drama`

### `packaging_alignment_note`

只保留一句对齐判断，例如：

- `当前正文承接卖点不足，包装需收紧兑现节点`

## 禁止项

- 不存长篇课程笔记
- 不存逐章理论讲解
- 不把 review 全文复制进 memory
