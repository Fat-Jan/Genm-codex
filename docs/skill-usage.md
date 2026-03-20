# Genm-codex Skill 使用说明

## 已安装的 Skill 名称

安装脚本会把以下目录链接到 `~/.codex/skills/`：

- 一套 plain 名：`novel-*`
- 一套兼容别名：`genm-novel-*`

下面先列兼容别名：

- `genm-novel-init`
- `genm-novel-batch`
- `genm-novel-character`
- `genm-novel-foreshadowing`
- `genm-novel-genre`
- `genm-novel-index`
- `genm-novel-log`
- `genm-novel-polish`
- `genm-novel-query`
- `genm-novel-setting`
- `genm-novel-status`
- `genm-novel-outline`
- `genm-novel-analyze`
- `genm-novel-write`
- `genm-novel-review`
- `genm-novel-resume`
- `genm-novel-rewrite`
- `genm-novel-export`

同时也会创建对应的 plain 名，例如：

- `novel-init`
- `novel-query`
- `novel-index`
- `novel-log`
- `novel-status`
- `novel-analyze`
- `novel-polish`
- `novel-genre`
- `novel-resume`

## 调用名说明

- 上面这些是本地安装链接名
- 在 Codex 会话中，优先使用各个 `SKILL.md` frontmatter 中的 `name` 来触发 skill
- 因此实际提示词里更推荐写：
  - `novel-init`
  - `novel-query`
  - `novel-status`
  - `novel-polish`
  - `novel-genre`
- `genm-novel-*` 更适合表示“这个 skill 已安装到本地”，不适合作为唯一调用名假设

## 推荐使用顺序

最小创作闭环：

1. `novel-init`
2. `novel-outline`
3. `novel-write`
4. `novel-review`
5. `novel-rewrite`
6. `novel-export`

## 第二阶段已迁入

- `genm-novel-character`
- `genm-novel-foreshadowing`
- `genm-novel-query`
- `genm-novel-setting`
- `genm-novel-status`
- `genm-novel-batch`

## 第三阶段已起步

- `genm-novel-polish`
- `genm-novel-genre`
- `genm-novel-analyze`
- `genm-novel-resume`
- `genm-novel-index`
- `genm-novel-log`

推荐场景：

- 对已写章节做轻量精修，而不是完整重写
- 查看当前项目的题材 profile
- 列出可用题材
- 给项目重新应用指定 profile
- 对已写章节区间做轻量数据分析
- 在中断后快速判断从哪里继续最稳

推荐场景：

- 创建或补完角色卡
- 管理伏笔与回收节奏
- 创建或补完力量体系、势力、地点、物品设定
- 查看角色当前设定
- 调整角色关系
- 顺序批量写作少量章节
- 查看主角当前状态
- 查询活跃伏笔
- 统计项目进度
- 列出角色/物品/地点信息

### character

```text
请使用 novel-character skill，为当前项目创建一个新角色并写入设定集/角色/。
```

### foreshadowing

```text
请使用 novel-foreshadowing skill，列出当前项目的活跃伏笔并指出最该优先回收的项。
```

### batch

```text
请使用 novel-batch skill，从第002章开始顺序生成 3 章，并在每章后更新 state。
```

### setting

```text
请使用 novel-setting skill，为当前项目创建或更新一个设定文件。
```

### status

```text
请使用 novel-status skill，总结当前项目状态，给我一个简明 dashboard。
```

### polish

```text
请使用 novel-polish skill，对第001章做 prose + pacing 向的轻量润色，并同步更新状态元数据。
```

### genre

```text
请使用 novel-genre skill，列出当前可用题材，并把当前项目应用到 xuanhuan / tomato 对应的 profile。
```

### index

```text
请使用 novel-index skill，为当前项目构建一个轻量索引，并告诉我已索引的章节数和主要实体统计。
```

### log

```text
请使用 novel-log skill，检查当前项目的 trace 日志是否已初始化；如果已初始化，再给我最近 10 条摘要。
```

### query

```text
请使用 novel-query skill，基于当前 state 和 index，列出活跃伏笔，并告诉我哪些章节提到了后山东壁。
```

### status

```text
请使用 novel-status skill，给我一个 full 模式的项目状态面板，重点包含质量状态、伏笔时间线和 index 统计。
```

### analyze

```text
请使用 novel-analyze skill，对第001章到第003章做区间分析，重点看节奏、爽点密度和连续性问题。
```

### resume

```text
请使用 novel-resume skill，基于当前项目状态判断我现在最稳的继续写作入口，并告诉我下一步该用哪个 skill。
```

## 最小 E2E 路线

建议在一个新会话中：

1. 使用 `novel-init` 初始化最小项目
2. 使用 `novel-outline` 生成总纲和第 1-10 章章纲
3. 使用 `novel-write` 写第 1 章
4. 使用 `novel-review` 审查第 1 章
5. 使用 `novel-rewrite` 按审查结果定向重写
6. 使用 `novel-export` 导出第 1 章 txt

## 最小 smoke 提示词

### init

```text
请使用 novel-init skill 在当前目录初始化一个小说项目：
title=E2E样本，genre=玄幻，platform=番茄，target_chapters=10
```

### outline

```text
请使用 novel-outline skill，为当前项目补全总纲并生成第 1-10 章章纲。
```

### write

```text
请使用 novel-write skill，写第001章，目标约 3000 字，并更新 .mighty/state.json。
```

### review

```text
请使用 novel-review skill，审查第001章并把 review 结果写回 .mighty/state.json。
```

### rewrite

```text
请使用 novel-rewrite skill，按 review 结果定向重写第001章，并同步主角卡与状态。
```

### export

```text
请使用 novel-export skill，导出第001章为 txt。
```

## 注意

- 当前第一阶段只保证核心闭环
- 第二阶段能力已迁入并做过 smoke
- 第三阶段当前只起步了 `polish` 和 `genre`
- 第三阶段当前也已进入 `analyze / resume / index`
- 第三阶段已完成 `polish / genre / analyze / resume / index / log`
- `shared/` 资产更新后应重新运行同步脚本
