# Genm-codex `v1.0.0-rc1` 计划

> 历史阶段文档：本文记录的是 `v1.0.0` 正式发布前的 RC 计划；当前正式状态以 [v1-final-decision.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/v1-final-decision.md) 为准。

## 目标

RC 的目的不是继续扩能力，而是验证：

- 当前默认工作流是否已经足够稳定
- 默认能力和实验能力的边界是否足够清晰
- 是否可以从 `0.x` 过渡到正式 `1.0`

---

## RC 范围

RC 只覆盖默认工作流和默认稳定能力。

### 1. 新书起盘

- `novel-init`
- `novel-genre`
- `novel-outline`
- `novel-package`

### 2. 正文生产

- `novel-write`
- `novel-review`
- `novel-fix`
- `novel-polish`
- `novel-rewrite`

### 3. 投稿准备

- `novel-precheck`
- `novel-package`
- `novel-export`

### 4. 持续学习

- `novel-learn`
- `novel-status`

### 5. 支撑能力

- `novel-query`
- `novel-retrieve`
- `novel-index`
- `novel-snapshot`
- `novel-resume`
- `novel-workflow`
- `novel-character`
- `novel-setting`
- `novel-foreshadowing`

---

## RC 不包含什么

以下能力不纳入 RC 通过条件：

- `novel-scan`
- shared 治理增强：
  - `--report`
  - `--domain`
  - `--report-json`
- docs-first 的 `help / tutorial`
- 环境引导型 `config / test`

原因：

- 它们要么是实验能力
- 要么不是默认写作主线
- 要么不应阻塞正式版默认工作流

---

## RC 验证项

### A. 默认工作流验证

必须至少验证：

1. 可以从零起盘
2. 可以连续写作并审查
3. 可以走 `fix / polish / rewrite` 分流
4. 可以输出包装并判断包装是否需要更新
5. 可以跑投稿前预检
6. 可以导出
7. 可以做学习回写

### B. 样本项目验证

至少保留一个样本项目进行完整验证：

- `e2e-novel`

### C. 文档入口验证

必须检查：

- README
- start-here
- skill-usage
- default-workflows
- v1-boundary

这些入口是否一致。

---

## RC 风险

### 1. 默认工作流与真实体验不一致

如果文档推荐的主线在真实使用中不顺，RC 不能通过。

### 2. 包装层过度承诺

如果 `novel-package` 给出的包装明显超出正文承载力，RC 不能通过。

### 3. 质量路由失真

如果 `review / precheck` 的判断在相似样本里明显不稳定，RC 不能通过。

### 4. 实验能力误入主线

如果 `novel-scan` 等实验能力开始影响默认流程判断，RC 应挂起。

---

## RC 通过后的动作

如果 RC 通过：

1. 补最终总结
2. 整理 release note
3. 再进入正式 `v1.0.0`

如果 RC 不通过：

1. 回退到 `0.x`
2. 只修 blocker
3. 再次发起 RC
