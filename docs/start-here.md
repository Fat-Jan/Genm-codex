# Genm-codex Start Here

## 你现在该从哪里开始

如果你刚打开这个仓库，不需要先理解所有 skill。

按用途走：

### 1. 我想从零开始写一本书

顺序：

1. `novel-init`
2. `novel-genre`
3. `novel-outline`
4. `novel-package`
5. `novel-write`
6. `novel-close`
7. 必要时再 `novel-rewrite`
8. `novel-export`

补充：

- 单章 `novel-write` 默认会守卫式自动尝试一次 `novel-close`
- 如果你这次只想写，不想自动收口，显式加 `skip_close=true`

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
请使用 novel-status skill，给我一个 full 模式的项目状态面板。
```

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

- [反脸谱化体系](./anti-flattening-framework/README.md)

如果你关心的是：

- 开头抓不抓人
- 前三章会不会只有承诺没有兑现
- 剧情是不是只有一根线在硬推

优先把 `novel-outline`、`novel-write`、`novel-review`、`novel-precheck`、`novel-package` 跑成一组，并参考：

- [开篇方法与剧情层次框架](./opening-and-plot-framework/README.md)

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
4. 想知道完整主线：看 [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/default-workflows.md)
5. 想优先打磨人物、关系和群像：看 [anti-flattening-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/README.md)
6. 想优先打磨开篇抓力、前三章兑现和剧情层次：看 [opening-and-plot-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/README.md)
