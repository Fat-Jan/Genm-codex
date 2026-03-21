# Genm-codex `v1.0.0-rc1` 执行记录

## 目的

这份文档记录 RC 的实际执行状态。

和 [v1-rc-plan.md](/Users/arm/Desktop/vscode/Genm-codex/docs/v1-rc-plan.md) 的区别是：

- `v1-rc-plan.md` 讲 RC 应该怎么跑
- 本文档讲 RC 现在跑到了哪一步

---

## 当前状态

- RC 计划：已定义
- RC 执行：已发起
- 当前判断：已进入 `v1.0.0-rc1` 阶段，后续以 blocker 收集与稳定化为主

---

## 默认工作流执行状态

### 1. 新书起盘

- 状态：pass
- 路径：
  - `novel-init`
  - `novel-genre`
  - `novel-outline`
  - `novel-package`

证据：

- `e2e-novel` 已由起盘流程建立
- 已存在：
  - `.mighty/state.json`
  - `大纲/总纲.md`
  - 章纲目录
  - `包装/简介方案.md`

### 2. 正文生产

- 状态：pass
- 路径：
  - `novel-write`
  - `novel-review`
  - `novel-fix` / `novel-polish` / `novel-rewrite`

证据：

- 已写到第 4 章：
  - `e2e-novel/chapters/第004章.md`
- review 已写回：
  - `recommended_next_action = novel-fix`
- `fix / polish / rewrite` 路由均已有前序 smoke 证据

### 3. 投稿准备

- 状态：pass
- 路径：
  - `novel-precheck`
  - `novel-package`
  - `novel-export`

证据：

- `precheck` 已能给出：
  - `ready-now`
  - `packaging-needs-update: no`
- 包装方案已存在：
  - `e2e-novel/包装/简介方案.md`
- 导出样本已存在：
  - `e2e-novel/exports/第001章.txt`

### 4. 持续学习

- 状态：pass
- 路径：
  - `novel-learn`
  - `novel-status`

证据：

- `learned_patterns` 已更新到第 4 章
- `novel-status` 路径已有前序 smoke 证据

---

## 样本项目执行状态

### `e2e-novel`

- 状态：pass
- 已知覆盖：
  - 起盘
  - 正文
  - 审查
  - 路由
  - 包装
  - 投稿前预检

---

## 文档入口一致性

- README：已有
- start-here：已有
- skill-usage：已有
- default-workflows：已有
- v1-boundary：已有

状态：pass

说明：

- 当前默认入口文档已与默认工作流和实验边界保持一致

---

## 当前 blocker

- 暂无明确 blocker
- 当前观察项见：
  - [v1-rc-blockers.md](/Users/arm/Desktop/vscode/Genm-codex/docs/v1-rc-blockers.md)

---

## 下一步

1. 继续收集真实使用中的 blocker
2. 继续观察：
   - `novel-scan` 是否仍然保持在实验边界之外
   - 默认工作流在真实小说项目中的稳定性
3. 仅修 blocker，不再扩大默认能力范围
