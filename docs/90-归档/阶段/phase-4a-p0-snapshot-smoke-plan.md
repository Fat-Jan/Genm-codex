# Genm-codex Phase 4A / P0 Snapshot Smoke Plan

## 目标

验证 `novel-snapshot` 第一版的最小可用性。

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 这轮优先验证：
  - `list`
  - `load`
- 默认走只读路径，不修改任何文件

## 1. `novel-snapshot`

### 测试目标

验证它能列出已有快照，并把第001章快照作为一个可读的历史上下文载入。

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-snapshot skill，完成两件事：

1. 列出当前项目已有的章节快照
2. 加载第001章快照，并告诉我其中最关键的状态信息

要求：
1. 优先读取：
   - `.mighty/state.json` 里的 `chapter_snapshots`
2. 如有必要，再参考 `.mighty/snapshots/`
3. 不要改动任何文件

完成后只汇报：
- 实际操作的项目根目录
- 当前有哪些快照
- 第001章快照里最关键的状态信息
- 你主要依赖的是 state、filesystem，还是两者结合
- 是否改动了任何文件
```

### 通过标准

- 确认正确项目目录
- 能列出当前已有快照
- 能成功加载第001章快照
- 能给出快照里的核心状态
- 不修改任何文件
