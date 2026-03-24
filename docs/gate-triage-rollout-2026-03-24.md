# Gate Triage Rollout 2026-03-24

## 摘要

这次收口的不是一个新默认命令，而是一条围绕 `setting gate` 的完整处理链：

- research candidate handoff
- gate 阻断结果结构化
- status / resume / query 消费 gate
- 主入口文档和独立 triage 指南

更直接地说：

- `setting gate` 不再只是“卡住或通过”
- 它现在已经能给出：
  - `blocking_gaps`
  - `review_items`
  - `minimal_next_action`

并且这组结果已经被：

- `novel-write`
- `novel-status`
- `novel-resume`
- `novel-query`

消费。

## 本轮落成内容

### 1. research candidate handoff

新增了从外部研究到 gate 的最小输入缝：

- `novel-scan` 可选写 `.mighty/research-candidates.json`
- `setting_gate.py --candidates-file` 可读入候选

这条链的定位是：

- candidate-only
- review-first
- not canon

### 2. gate next action

`setting gate` 结果现在会返回：

- `minimal_next_action`

它至少回答三件事：

1. 现在最小该做什么
2. 为什么是这一步
3. 对应命令是什么

默认路由目前包括：

- 缺本地 truth source -> `novel-setting`
- 高风险 research candidate -> `review-sync-queue`

### 3. gate-aware consumers

以下入口现在都能消费 gate 结果：

- `novel-write`
- `novel-status`
- `novel-resume`
- `novel-query`

这意味着用户不需要手动翻 `.mighty/setting-gate.json` 才知道下一步。

### 4. 文档入口统一

这条链已经被挂到：

- `README.md`
- `docs/default-workflows.md`
- `docs/start-here.md`
- `docs/skill-usage.md`
- `docs/gate-triage.md`

## 实际意义

这次工作的意义不是“多接了一个实验能力”，而是：

1. 把 `novel-scan` 的研究结果关进了 review 边界
2. 把 `setting gate` 从阻断点提升成真正的工作流控制点
3. 让状态、恢复、查询入口都能读懂 gate，而不是只靠 `novel-write`

所以它的价值更接近：

- 默认工作流的维护性增强

而不是：

- 又多了一个新功能点

## 当前边界

这轮明确没有做：

- 直接把 research candidate 写进 canon
- 把 `novel-scan` 纳入默认主线
- 引入新的 memory / graph 真相层
- 修改 `shared/` 资产同步策略

## 相关文档

- [gate-triage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/gate-triage.md)
- [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/default-workflows.md)
- [start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/start-here.md)
- [skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/skill-usage.md)
