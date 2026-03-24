# 番茄 P0 Smoke Template

## 适用场景

当你想在一个真实项目上验证：

- 当前项目是否命中某个番茄 `P0` bucket
- `fanqie_bucket_review_summary` 是否能写得具体
- `fanqie_bucket_precheck_summary` 是否能写得具体
- 是否值得把轻量 bucket 结论写回 `chapter_meta`

就用这份模板。

它是**人工执行 smoke 的 runbook**，不是自动脚本。

如果你不想手工起草整份文档，可先用：

```bash
python3 scripts/fanqie_p0_smoke.py --project-root "<project_root>" --chapter 003 --chapters 001-003
```

脚本会先生成这份结构的 `draft` 版 smoke 文档，再由你人工确认。

## 使用步骤

### 1. 先确认项目前提

- `.mighty/state.json` 存在
- `meta.platform = 番茄`
- `meta.genre` 或 `genre_profile.bucket` 已能映射到某个 `P0` bucket

记录：

```md
项目：
平台：
bucket：
目标章节：
目标范围：
```

### 2. 读取最少上下文

至少读：

- `.mighty/state.json`
- `大纲/总纲.md`
- 目标章节对应章纲
- 目标章节正文
- 若做黄金三章预检，再读第001-003章章纲 / 正文

### 3. 先做 `novel-review` 样本

- 选一个最适合代表当前 bucket 的目标章节
- 优先选：
  - 开篇关键章
  - 明显兑现章
  - 或正要暴露问题的转折章

### 4. 再做 `novel-precheck` 样本

- 对开篇类 bucket，优先检查第001-003章
- 对非开篇类 bucket，也至少要检查一个能代表当前 promise 的章节范围

### 5. 决定是否写回

只有当 bucket 结论已经足够稳定时，才考虑写回：

- `chapter_meta[N].fanqie_bucket_flags`
- `chapter_meta[N].fanqie_bucket_summary`

如果仍只是探索判断，先停在只读 smoke。

## `novel-review` 样本模板

```md
## 手工 `novel-review` 样本

目标章节：

- `第NNN章正文：<project_root>/chapters/第NNN章.md`

### 结论

一句话说明这一章在当前 bucket 下是否成立。

### 样本输出

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

### 为什么这么判

- `promise_match =`
- `first_three_status =`
- `bucket_grade =`

### 当前未构成红灯、但值得继续盯的点

- ...
```

## `novel-precheck` 样本模板

```md
## 手工 `novel-precheck` 样本

目标范围：

- `第001章正文：<project_root>/chapters/第001章.md`
- `第002章正文：<project_root>/chapters/第002章.md`
- `第003章正文：<project_root>/chapters/第003章.md`

### 样本输出

```md
fanqie_bucket_precheck_summary:
  bucket:
  submission_fit:
  opening_status:
  golden_three_status:
  packaging_alignment:
  top_blocker:
```

### 为什么这么判

- `submission_fit =`
- `opening_status =`
- `golden_three_status =`
- `packaging_alignment =`
```

## 可选写回记录

如果本轮决定写回，补这一段：

```md
## 写回记录

写回位置：

- `.mighty/state.json -> chapter_meta["NNN"]`

写回字段：

- `fanqie_bucket_flags`
- `fanqie_bucket_summary`

写回原因：

- 当前 bucket 结论已足够稳定
- 该章节可作为后续 bucket 化 review 的参考锚点
```

## 最后结论模板

```md
## 结论

在 `<项目名>` 这个真实项目上：

- `fanqie_bucket_review_summary` 可写 / 不稳定 / 为空
- `fanqie_bucket_precheck_summary` 可写 / 不稳定 / 为空
- 是否建议写回 `chapter_meta`：
  - yes / no
- 当前最有价值的后续动作：
  - ...
```

## 注意

- 不要把 smoke 写成“要求全部通过”的表演
- 要记录真实的 `warn` 和 `top_blocker`
- 如果样本不够，不要硬写满字段
