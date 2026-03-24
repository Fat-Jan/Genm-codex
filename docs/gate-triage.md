# Gate Triage

## 目的

这份文档把 `setting gate` 被卡住时的最小处理链路收成一个固定入口，避免在 `README`、`start-here`、`skill-usage` 和各 skill 说明之间来回跳。

它回答三个问题：

1. 什么时候该进入 triage
2. triage 的最小链路是什么
3. 进入后优先看哪些字段和命令

## 何时进入

当 `.mighty/setting-gate.json` 出现以下任一情况时，进入 triage：

- `status = blocked`
- `status = review_required`
- 写作前不确定当前项目是否具备继续 `novel-write` 的条件

## 最小链路

默认按这条顺序处理：

1. `novel-scan`
2. `setting gate`
3. `review-sync-queue`
4. `novel-status` / `novel-resume` / `novel-query`

也就是：

- `novel-scan -> setting gate -> review-sync-queue`

注意：

- 这是一条候选审阅链，不是 canon 写入链
- `research-candidates` 只进入 review queue，不直接写 `设定集/`
- gate 没过之前，不直接进入 `novel-write`

## 优先读哪些字段

当 gate 未通过时，优先读：

- `status`
- `blocking_gaps`
- `review_items`
- `minimal_next_action`

其中最关键的是：

- `minimal_next_action`

它会告诉你：

- 当前最小该做什么
- 为什么是这一步
- `suggested_commands`

## 最小命令链

```bash
python3 scripts/novel_scan.py <project_root> --platform 番茄 --genre 宫斗宅斗 --depth quick --mode project-annotate --emit-research-candidates
python3 scripts/setting_gate.py <project_root> --stage outline --candidates-file .mighty/research-candidates.json
python3 scripts/review-sync-queue.py <project_root> --list
```

如果当前项目已经卡住，但不确定卡在哪，也可以直接走查询入口：

```text
请使用 novel-query skill，告诉我当前 setting gate 的状态、blocking_gaps 和 minimal_next_action。
```

```text
请使用 novel-status skill，给我一个 full 模式的项目状态面板，并额外带上 gate status、blocking_gaps 和 minimal_next_action。
```

```text
请使用 novel-resume skill，如果当前项目被 setting gate 卡住，就优先告诉我 minimal_next_action 和最稳的下一步。
```

## 路由规则

### 1. 缺本地 truth source

常见信号：

- `kinship_truth`
- `office_truth`
- `world_rule_support`

默认动作：

- 优先补本地设定
- 由 `minimal_next_action.action = novel-setting` 引导

### 2. 高风险 research candidate

常见信号：

- `review_items[*].source = mcp`
- `requires_user_confirmation = true`

默认动作：

- 先看 `review-sync-queue`
- 不直接把候选事实写入 canon

### 3. 只是想知道能不能继续写

默认动作：

- 用 `novel-status` 看整体状态
- 用 `novel-resume` 看最稳下一步
- 用 `novel-query` 做单点追问

## 入口关系

这份文档是 triage 专用收口页。

相关入口：

- [README.md](/Users/arm/Desktop/vscode/Genm-codex/README.md)
- [start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/start-here.md)
- [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/default-workflows.md)
- [skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/skill-usage.md)

相关脚本与文件：

- [setting_gate.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/setting_gate.py)
- [novel_scan.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/novel_scan.py)
- [review-sync-queue.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/review-sync-queue.py)
- `.mighty/setting-gate.json`
- `.mighty/research-candidates.json`
- `.mighty/sync-review.json`
