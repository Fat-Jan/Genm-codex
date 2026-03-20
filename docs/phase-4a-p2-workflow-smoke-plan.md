# Genm-codex Phase 4A / P2 Workflow Smoke Plan

## 目标

验证 `novel-workflow` 第一版的最小可用性。

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 第一轮优先验证：
  - `status`
- 默认走只读路径，不修改任何文件

## 1. `novel-workflow`

### 测试目标

验证它在没有 `.mighty/workflow_state.json` 的情况下，能否正确返回“无活动 workflow / 空闲状态”，而不是报错或伪造任务。

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-workflow skill，检查当前 workflow 状态。

要求：
1. 优先检查 `.mighty/workflow_state.json`
2. 如果文件不存在，要明确告诉我当前是“无活动 workflow / 空闲状态”
3. 不要改动任何文件

完成后只汇报：
- 实际操作的项目根目录
- 当前 workflow 状态
- 你的判断依据
- 下一步建议
- 是否改动了任何文件
```

### 通过标准

- 确认正确项目目录
- 正确识别 `workflow_state.json` 不存在
- 正确返回空闲/无活动 workflow
- 不伪造任务状态
- 不修改任何文件
