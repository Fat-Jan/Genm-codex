# Genm-codex Start Here

## 你现在该从哪里开始

如果你刚打开这个仓库，不需要先理解所有 skill。

按用途走：

### 1. 我想从零开始写一本书

顺序：

1. `novel-init`
2. `novel-genre`
3. 古代家族权力题材先补 `宅门真值表 + 小型家谱`
4. `novel-outline`
   - 先做 `mode=total`
5. 总纲初稿后，先补当前卷刚需设定，再进入 `mode=chapter`
6. 如果当前项目是番茄平台，`setting gate(outline)` 现在会守卫式自动编译 `launch-stack`
7. `setting gate`
8. `novel-package`
9. `novel-write`
10. `novel-close`
11. 必要时再 `novel-rewrite`
12. `novel-export`

补充：

- 单章主线现在最好按一个固定的 `chapter transaction` 理解：
  - `gate-check -> draft -> close -> maintenance -> snapshot`
- 如果立项信息还不稳，先补 `shared/templates/project/creative-brief.md`
- 先有 `总纲`，再有 `章纲`
- 总纲初稿后，先补当前卷刚需设定：
  - 家族/继承/婚配/掌家真值
  - 当前卷关键人物卡
  - 当前卷关键地点 / 势力 / 旧案地点
- 不要在起盘阶段一口气把整本书设定写满
- 上游结构边界优先看：
  - [upstream-structure-contract.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/upstream-structure-contract.md)
  - [total-outline-structure-contract.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/total-outline-structure-contract.md)
- 单章 `novel-write` 默认会守卫式自动尝试一次 `novel-close`
- 如果你这次只想写，不想自动收口，显式加 `skip_close=true`
- 如果当前项目是番茄平台，仍可手动运行：

```text
python3 scripts/fanqie_launch_stack.py --project-root <project_root> --chapter 003 --chapters 001-003 --mode writeback --writeback
```

- 但默认主线里，`setting gate(outline)` 现在应在检测到 sidecar 缺失或仍是 `preselect` placeholder 时自动补编译
- 手动命令主要用于强制重编译或显式检查
- `novel-outline` 完成后，先跑一次 `setting gate` 再开始写：

```text
python3 scripts/setting_gate.py <project_root> --stage outline
```

- 如果 `.mighty/setting-gate.json` 仍是 `blocked`，不要直接进入 `novel-write`
- 现在优先看：
  - `blocking_gaps`
  - `review_items`
  - `minimal_next_action`
- `minimal_next_action.suggested_commands` 会给出最小可执行命令串；先按它处理，再重跑 gate
- 如果 gate 卡住的是本地 truth source，先补 `设定集/`，不是先去外部搜一大圈
- 如果你需要一个集中入口，不想在多个文档之间跳，直接看：
  - [gate-triage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/gate-triage.md)

最小提示词：

```text
请使用 novel-init skill 在当前目录初始化一个小说项目：
title=我的新书，genre=玄幻，platform=番茄，target_chapters=10
```

### 2. 我已经有项目，想知道当前状态

优先用：

- `novel-status`
- `novel-query`
- `novel-index`

最小提示词：

```text
请使用 novel-status skill，给我一个 full 模式的项目状态面板，并额外带上 gate status、blocking_gaps 和 minimal_next_action。
```

补充：

- 如果项目已经引入 `setting gate`，让 `novel-status` 一并汇报：
  - `gate status`
  - `blocking_gaps`
  - `minimal_next_action`
- 如果你只想快速问一句：
  - “现在 gate 卡在哪”
  - “下一步最小动作是什么”
  也可以直接用 `novel-query`

### 3. 我正在写作，想快速引用设定

优先用：

- `novel-retrieve`
- `novel-character`
- `novel-setting`

最小提示词：

```text
请使用 novel-retrieve skill，快速告诉我“某角色/某地点/某物品”现在在项目里是什么定位。
```

### 4. 我写完一章，想修

默认先用：

- `novel-close`

它内部会跑：

- `novel-review`
- 再按结果进入：
  - 局部修补：`novel-fix`
  - 轻量精修：`novel-polish`
  - 定向重写：`novel-rewrite`

如果你是刚用 `novel-write` 写完单章，通常不必再额外提醒一次，默认会先尝试自动进入这条收口链。

如果你关心的是：

- 人物像不像活人
- 群像会不会围着主角转
- 阵营是不是只有一个声道

优先把 `novel-outline`、`novel-write`、`novel-review`、`novel-precheck` 跑成一组，并参考：

- [反脸谱化体系](../anti-flattening-framework/README.md)

如果你关心的是：

- 开头抓不抓人
- 前三章会不会只有承诺没有兑现
- 剧情是不是只有一根线在硬推

优先把 `novel-outline`、`novel-write`、`novel-review`、`novel-precheck`、`novel-package` 跑成一组，并参考：

- [开篇方法与剧情层次框架](../opening-and-plot-framework/README.md)

如果你关心的是：

- 正文是不是总在解释、不在演出
- 对白是不是悬浮
- 包装 promise 会不会超过正文承载

优先把 `novel-write`、`novel-review`、`novel-precheck`、`novel-package`、`novel-learn` 跑成一组，并参考：

- [写作基本功与内容标准框架](../writing-core-framework/README.md)

如果你走的是番茄优先路线，而且想先知道“这本书主要靠什么起盘、主要靠什么留人”，再加一层：

- [番茄起盘协议栈](../opening-and-plot-framework/fanqie-launch-stack/README.md)

### 批量写作特别提醒

- **一次性最多只生成 3 章**
- `novel-batch` 默认**不会**在每章后自动跑 `novel-close`
- 超过 3 章很容易出现：
  - 字数断崖
  - 提纲化短章
  - 概述代替演出
  - AI 摘要腔
- 所以后面如果你要批量推进，默认按：
  - `3章一批 -> review/质量门 -> 再继续`

### 5. 我想投稿前检查一下

优先用：

- `novel-precheck`
- `novel-package`
- `novel-export`

### 6. 我想看历史状态或恢复上下文

优先用：

- `novel-snapshot`
- `novel-resume`
- `novel-workflow`

补充：

- 如果你是被 gate 卡住后中断的，优先让 `novel-resume` 把：
  - `.mighty/setting-gate.json`
  - `minimal_next_action`
  一起读出来，再决定是不是能继续写

最小提示词：

```text
请使用 novel-resume skill，如果当前项目被 setting gate 卡住，就优先告诉我 minimal_next_action 和最稳的下一步。
```

### 7. 我发现设定集和当前正文 / state 脱节了

优先用：

- `novel-sync`
- 再按需用：
  - `novel-character`
  - `novel-setting`

最小提示词：

```text
请使用 novel-sync skill，把当前项目里最近稳定出现的角色、地点和势力同步回设定集。
```

如果项目已经写了很多章，还可以进一步做：

```text
请使用 novel-sync skill，以 thin-state 模式把旧章节元数据归档出 state，只保留最近章节窗口。
```

如果你想一次性做完同步、指导数据旁路和 state 瘦身，可以直接运行：

```text
python3 scripts/project-maintenance.py <project_root>
```

如果你想把维护链挂在写作完成后自动执行，优先用：

```text
python3 scripts/post-task-maintenance.py <project_root> --trigger write
```

这个维护链现在应包含：

- `setting gate(write-post)`
- `sync + thin-state`
- `snapshot`
- `memory-context`
- `content-positioning`
- 轻量 trace log

也就是说：

- `workflow_state` 现在不只会推进到 `snapshot`
- 默认维护尾段会真实写出 snapshot artifact
- 并同时产出安全的 `memory-context` 摘要
- 如果项目声明了组合题材定位，也会刷新 `content-positioning` sidecar

### 8. 已有稿接入

优先用：

- `python3 scripts/import_existing_chapters.py <project_root> --from <source>`

然后看：

- `.mighty/import-report.json`

再继续：

- `novel-index build`
- `setting gate`
- `novel-resume`

如果你想知道一个单章事务现在停在哪，优先看：

- `novel-workflow`
- `novel-resume`
- `novel-snapshot`

## 阶段能力地图

### 核心闭环

- init
- outline
- write
- review
- rewrite
- export

### 中台能力

- query
- status
- character
- setting
- foreshadowing
- batch

### 增强能力

- polish
- genre
- analyze
- resume
- index
- log

### 编辑与辅助能力

- fix
- snapshot
- precheck
- workflow
- retrieve
- spinoff

### 环境与学习能力

- config
- test
- learn

## 还没有纳入默认工作流的内容

- `novel-scan`
  - 目前已是可用的实验能力
  - 适合在明确需要外部市场信号时单独运行
  - 但仍不属于默认主工作流的一部分

- `novel-help` / `novel-tutorial`
  - 当前由这份文档、README 和 `skill-usage.md` 承担职责

## 最后建议

如果你不知道从哪个 skill 开始：

1. 先读项目当前目录的 `.mighty/state.json` 是否存在
2. 不存在：从 `novel-init` 开始
3. 存在：先跑 `novel-status`
4. 想知道完整主线：看 [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/default-workflows.md)
5. 想优先打磨人物、关系和群像：看 [anti-flattening-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/README.md)
6. 想优先打磨开篇抓力、前三章兑现和剧情层次：看 [opening-and-plot-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/README.md)
7. 想优先打磨正文执行、内容标准、memory 压缩信号和开篇包装承诺：看 [writing-core-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/writing-core-framework/README.md)
