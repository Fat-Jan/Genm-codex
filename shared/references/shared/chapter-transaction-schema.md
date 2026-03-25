---
name: chapter-transaction-schema
purpose: 定义单章生产的固定 chapter transaction 契约
version: "1.0"
---

# Chapter Transaction Schema

本文件定义 `Genm-codex` 的单章 `chapter transaction`。

目标不是引入新的工作流引擎，而是把现有主线固定成一个可恢复、可诊断、可汇报的最小事务链。

## 固定步骤

单章默认事务顺序固定为：

1. `gate-check`
2. `draft`
3. `close`
4. `maintenance`
5. `snapshot`

这些步骤共同构成一个完整的 `chapter transaction`。

## 步骤说明

### `gate-check`

- 输入：
  - `.mighty/setting-gate.json`
  - 相关 outline / setting truth
- 目的：
  - 在正文生成前确认当前章节允许进入 prose generation
- 失败语义：
  - 停在 `gate-check`
  - 优先返回 `minimal_next_action`

### `draft`

- 执行者：
  - `novel-write`
- 目的：
  - 生成本章正文并完成基础 state 写回
- 成功证据：
  - 章节文件已写入
  - 基础 `state` 更新完成

### `close`

- 执行者：
  - `novel-close`
- 目的：
  - 执行 `review -> route -> re-review`
- 边界：
  - `close` 是 bounded convergence phase，不负责 maintenance

### `maintenance`

- 执行者：
  - `scripts/post-task-maintenance.py`
  - `scripts/project-maintenance.py`
- 目的：
  - 执行 `setting gate(write-post)`、sync、guidance split、thin-state
- 边界：
  - `maintenance` 不负责 prose mutation

### `snapshot`

- 执行者：
  - `novel-snapshot` 或等价的持久化快照路径
- 目的：
  - 为 resume / compare / rollback 提供当前事务完成后的状态证据

## 终态

事务允许的终态：

- `completed`
- `failed`
- `cancelled`
- `blocked`

推荐恢复规则：

- 停在 `gate-check`：
  - 先解 gate blocker，再继续
- 停在 `draft`：
  - 先确认章节文件与 state 是否已落盘
- 停在 `close`：
  - 优先回 `novel-close`
- 停在 `maintenance`：
  - 先补完 maintenance，再进入 `snapshot`
- 停在 `snapshot`：
  - 优先补快照，再报告事务完成

## 状态约定

工作流状态建议记录：

- `current_step`
- `completed_steps`
- `failed_steps`
- `pending_steps`
- `last_successful_checkpoint`

这些字段应服务于 `novel-workflow` 和 `novel-resume`，用于计算最稳的恢复点，而不是构成新的事实源。
