# 真实项目样本验证：继母换我婚书那夜，太子先开了口 Fanqie P0 输出契约

## 目标

用第二个真实项目验证：

1. 同一套 `fanqie-p0-smoke-template.md` 是否能跨项目复用
2. 在同样的 `宫斗宅斗` bucket 下，另一种更强钩子、更快兑现的开篇线能否也稳定写出：
   - `fanqie_bucket_review_summary`
   - `fanqie_bucket_precheck_summary`

本轮采用**只读跨项目 smoke**：

- 不改正文
- 不写回项目 `state`
- 只验证模板和 bucket 摘要是否能稳定复用

## 样本范围

- 项目：`projects/庶妹换我婚书那夜，太子先开了口`
- 平台：`番茄`
- bucket：`宫斗宅斗`
- review 样本章节：`第003章`
- precheck 样本范围：`第001-003章`

主要参考：

- [总纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/大纲/总纲.md)
- [第001章章纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/大纲/章纲/第001章.md)
- [第002章章纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/大纲/章纲/第002章.md)
- [第003章章纲](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/大纲/章纲/第003章.md)
- [第001章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/chapters/第001章.md)
- [第002章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/chapters/第002章.md)
- [第003章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/chapters/第003章.md)

## 手工 `novel-review` 样本

目标章节：

- [第003章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/chapters/第003章.md)

### 结论

这章单章可过，而且比 `庶女谋略` 更明显地走的是“强钩子、快兑现、章末挂更险局”的宫斗宅斗短中篇开篇路线。

### 样本输出

```md
fanqie_bucket_review_summary:
  bucket: 宫斗宅斗
  bucket_grade: pass
  promise_match: pass
  first_three_status: pass
  primary_failure: none
  top_red_flag: none
  recommended_focus: chapter4 要把“庄子抢旧人”写成真实生死赛跑，避免太子口谕变成万能捷径
```

### 为什么这么判

- `promise_match = pass`
  - 书名和总纲 promise 都是：
    - 继母换婚书
    - 女主当夜翻账反咬
    - 太子很早入场改写规则层
  - 第001-003章都在直接交付这个 promise。
- `first_three_status = pass`
  - 第001章完成“婚书被换 -> 当众反咬 -> 东宫点名”
  - 第002章完成“开匣验真 -> 婚书归手 -> 东宫正式把局抬高”
  - 第003章完成书名里“太子先开了口”的硬兑现，并把局从婚书争夺升级成旧账局
- `bucket_grade = pass`
  - 宫斗宅斗桶在这里走的是更快、更强钩子的路子，但依然满足：
    - 压制链清楚
    - 第一章就见硬压制和反咬
    - 第二章有公开开匣换账
    - 第三章收益很硬，但没有把旧案打穿，而是留下更大的灭口残账

### 当前未构成红灯、但值得继续盯的点

- 第003章的收益很强，容易把后续写成“有东宫口谕就一路通”
- 真正的风险不是口谕够不够爽，而是第004章能不能把“柳氏抢先灭口”写成实打实的阻力
- 如果第004-005章只剩“令签在手所以一路顺”，这条线会从 `pass` 掉到 `warn`

## 手工 `novel-precheck` 样本

目标范围：

- [第001章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/chapters/第001章.md)
- [第002章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/chapters/第002章.md)
- [第003章正文](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口/chapters/第003章.md)

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
  - 这里只代表“作为宫斗宅斗开篇样本 fit”，不等同整书完稿后的最终投稿结论
- `opening_status = pass`
  - 第一屏就直接落“婚书被换”的核心压制，不是慢热铺垫
- `golden_three_status = pass`
  - 第001章：强压制 + 当众反咬 + 东宫点名
  - 第002章：开匣验真，婚书归手，婚书局正式抬高
  - 第003章：太子开口，口谕与令签落地，但旧案入口才刚打开
- `packaging_alignment = aligned`
  - 书名强调“换婚书那夜”“太子先开了口”
  - 前三章正文确实已经交付这两个高概念 promise，没有拖到中后段才兑现

## 跨项目验证价值

### 1. 同一模板可复用

这说明 [fanqie-p0-smoke-template.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/fanqie-p0-smoke-template.md) 不是只适合 `庶女谋略` 这种慢一点的宫斗宅斗线。

它同样适用于：

- 开局更强钩子
- 第一章就高压反咬
- 第三章就给口谕硬兑现

的另一类宫斗宅斗线。

### 2. 同 bucket 内部也能分出不同路数

- `庶女谋略`
  - 更偏“病后立位 -> 花园试探 -> 正院定性”
  - 收益偏稳，残账偏深
- `继母换我婚书那夜，太子先开了口`
  - 更偏“婚书被换 -> 东宫问婚 -> 太子口谕”
  - 钩子更猛，兑现更快

但两条线都还能被同一份 `宫斗宅斗` bucket 契约稳定解释。

### 3. 当前无需急着写回第二个项目

第一条项目已经证明了轻量写回可行。

第二条项目这轮更有价值的是：

- 验证模板复用
- 验证同 bucket 不同路数也能产出具体 summary

因此本轮停在只读 smoke，更干净。

## 结论

在 `继母换我婚书那夜，太子先开了口` 这个真实项目上：

- `fanqie_bucket_review_summary` 可写、且不空
- `fanqie_bucket_precheck_summary` 可写、且不空
- 同一份 Fanqie P0 smoke 模板可跨项目复用
- 当前最有价值的后续动作不是继续加字段，而是：
  - 看第004-005章能否把“口谕到手后的阻力仍然成立”写实
  - 再决定要不要做第二个真实写回样本
