# 真实项目样本验证：庶女谋略 Fanqie P0 输出契约

## 目标

用真实项目 `projects/庶女谋略` 验证：

1. `fanqie_bucket_review_summary` 会不会空
2. `fanqie_bucket_precheck_summary` 会不会空
3. 这两个摘要在宫斗宅斗路线里是否足够具体可用

本轮采用**轻量写回样本验证**：

- 不改正文
- 只把 `第003章` 的 bucket 级摘要轻量写回项目 `state`

## 样本范围

- 项目：`projects/庶女谋略`
- 平台：`番茄`
- bucket：`宫斗宅斗`
- review 样本章节：`第003章`
- precheck 样本范围：`第001-003章`

主要参考：

- [总纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/大纲/总纲.md)
- [第001章章纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/大纲/章纲/第001章.md)
- [第002章章纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/大纲/章纲/第002章.md)
- [第003章章纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/大纲/章纲/第003章.md)
- [第001章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/chapters/第001章.md)
- [第002章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/chapters/第002章.md)
- [第003章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/chapters/第003章.md)

## 手工 `novel-review` 样本

目标章节：

- [第003章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/chapters/第003章.md)

### 结论

这章单章可过，而且和前三章整体配合后，`宫斗宅斗` 的开篇 promise 是成立的。

### 样本输出

```md
fanqie_bucket_review_summary:
  bucket: 宫斗宅斗
  bucket_grade: pass
  promise_match: pass
  first_three_status: pass
  primary_failure: none
  top_red_flag: none
  recommended_focus: chapter4-5 要尽快把“知足守礼”转成具体的月例、药材、炭火、针线压缩，不要只停在口风层
```

### 为什么这么判

- `promise_match = pass`
  - 开篇 promise 是“庶女病后醒来，在低位秩序里不按原样退”，第001-003章都在兑现这一点。
- `first_three_status = pass`
  - 第001章完成身份闭合和赴约决策
  - 第002章完成第一次公开试探与不退
  - 第003章没有把冲突打满，而是把结果转成更危险的正院定性和资源压缩预告
- `bucket_grade = pass`
  - 这一桶要的不是前三章立刻大翻盘，而是要有：
    - 明确压迫对象
    - 明确礼法和嫡庶差
    - 至少一次压迫 -> 回应
    - 第三章把“赢得太满”压住，留下更大的残账

### 当前未构成红灯、但值得继续盯的点

- 第003章的硬收益不是“翻盘”，而是“清楚看见对手将从资源分配动手”
- 这类写法成立，但要求第004-005章必须尽快把资源压缩写实
- 如果后续两章只是继续定性、不兑现资源层代价，`bucket_grade` 会从 `pass` 掉到 `warn`

## 手工 `novel-precheck` 样本

目标范围：

- [第001章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/chapters/第001章.md)
- [第002章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/chapters/第002章.md)
- [第003章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/chapters/第003章.md)

### 样本输出

```md
fanqie_bucket_precheck_summary:
  bucket: 宫斗宅斗
  submission_fit: fit
  opening_status: pass
  golden_three_status: pass
  packaging_alignment: aligned
  top_blocker: none
```

### 为什么这么判

- `submission_fit = fit`
  - 这里只代表“作为宫斗宅斗开篇样本是 fit”，不等同全书正式投稿结论
- `opening_status = pass`
  - 第一屏就有身体痛感、错位、受辱余波和邀约压力，不是平铺背景
- `golden_three_status = pass`
  - 第一章确认人和局
  - 第二章完成第一次公开试探
  - 第三章把花园结果转成正院视角下的重新定性，并明确后续刀口
- `packaging_alignment = aligned`
  - [总纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/大纲/总纲.md) 的一句话简介强调：
    - 穿成庶女
    - 靠原著记忆在内宅求生、借势翻身
  - 前三章正文确实在交付这条主 promise，没有跑成纯元叙事或纯设定说明

## 这轮验证的价值

### 1. 新字段不是空名词

这两个新增字段在真实样本里都能写出具体内容：

- `fanqie_bucket_review_summary`
- `fanqie_bucket_precheck_summary`

### 2. 它们和现有规则层不打架

- 不替代 `anti_flattening_summary`
- 不替代 `gongdou_funnel_summary`
- 更像是“当前 bucket 下，这章 / 这三章到底有没有按路数交付”的摘要层

### 3. 它们已能轻量写回 `chapter_meta`

本轮已对 [state.json](/Users/arm/Desktop/vscode/Genm-codex/projects/庶女谋略/.mighty/state.json) 写回：

- `chapter_meta["003"].fanqie_bucket_flags`
- `chapter_meta["003"].fanqie_bucket_summary`

当前写回策略是：

- `fanqie_bucket_flags = []`
- `fanqie_bucket_summary` 保留正向 bucket 判断与下一步 focus

这样可以验证：

- 正向 bucket 判断也能稳定落库
- 字段不会被迫只有“报错时才存在”

## 结论

在 `庶女谋略` 这个真实宫斗宅斗项目上：

- `fanqie_bucket_review_summary` 可写、且不空
- `fanqie_bucket_precheck_summary` 可写、且不空
- `chapter_meta["003"].fanqie_bucket_summary` 已完成真实样本写回
- 当前最有价值的后续动作不是继续扩字段，而是：
  - 真的把第004-005章的资源压缩兑现写出来
  - 再看这两个 summary 在“从 promise 到代价落地”的过渡段会不会开始发散
