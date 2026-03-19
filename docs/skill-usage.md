# Genm-codex Skill 使用说明

## 已安装的 Skill 名称

安装脚本会把以下目录链接到 `~/.codex/skills/`：

- `genm-novel-init`
- `genm-novel-batch`
- `genm-novel-character`
- `genm-novel-foreshadowing`
- `genm-novel-query`
- `genm-novel-setting`
- `genm-novel-status`
- `genm-novel-outline`
- `genm-novel-write`
- `genm-novel-review`
- `genm-novel-rewrite`
- `genm-novel-export`

## 推荐使用顺序

最小创作闭环：

1. `genm-novel-init`
2. `genm-novel-outline`
3. `genm-novel-write`
4. `genm-novel-review`
5. `genm-novel-rewrite`
6. `genm-novel-export`

## 第二阶段已迁入

- `genm-novel-character`
- `genm-novel-foreshadowing`
- `genm-novel-query`
- `genm-novel-setting`
- `genm-novel-status`
- `genm-novel-batch`

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
请使用 genm-novel-character skill，为当前项目创建一个新角色并写入设定集/角色/。
```

### foreshadowing

```text
请使用 genm-novel-foreshadowing skill，列出当前项目的活跃伏笔并指出最该优先回收的项。
```

### batch

```text
请使用 genm-novel-batch skill，从第002章开始顺序生成 3 章，并在每章后更新 state。
```

### setting

```text
请使用 genm-novel-setting skill，为当前项目创建或更新一个设定文件。
```

### status

```text
请使用 genm-novel-status skill，总结当前项目状态，给我一个简明 dashboard。
```

## 最小 E2E 路线

建议在一个新会话中：

1. 使用 `genm-novel-init` 初始化最小项目
2. 使用 `genm-novel-outline` 生成总纲和第 1-10 章章纲
3. 使用 `genm-novel-write` 写第 1 章
4. 使用 `genm-novel-review` 审查第 1 章
5. 使用 `genm-novel-rewrite` 按审查结果定向重写
6. 使用 `genm-novel-export` 导出第 1 章 txt

## 最小 smoke 提示词

### init

```text
请使用 genm-novel-init skill 在当前目录初始化一个小说项目：
title=E2E样本，genre=玄幻，platform=番茄，target_chapters=10
```

### outline

```text
请使用 genm-novel-outline skill，为当前项目补全总纲并生成第 1-10 章章纲。
```

### write

```text
请使用 genm-novel-write skill，写第001章，目标约 3000 字，并更新 .mighty/state.json。
```

### review

```text
请使用 genm-novel-review skill，审查第001章并把 review 结果写回 .mighty/state.json。
```

### rewrite

```text
请使用 genm-novel-rewrite skill，按 review 结果定向重写第001章，并同步主角卡与状态。
```

### export

```text
请使用 genm-novel-export skill，导出第001章为 txt。
```

## 注意

- 当前第一阶段只保证核心闭环
- 第二批能力尚未迁入
- `shared/` 资产更新后应重新运行同步脚本
