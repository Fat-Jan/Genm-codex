# Genm-codex `v1.0.0` 前置门槛清单

## 目的

把 `v1.0.0` 讨论从抽象原则变成可逐项核验的 checklist。

每一项都应该能回答：

- 是否满足
- 证据在哪
- 是否阻塞 `1.0`

---

## Checklist

### 1. 默认工作流已成文

要求：

- 必须存在正式文档
- 必须覆盖：
  - 新书起盘
  - 正文生产
  - 投稿准备
  - 持续学习

证据目标：

- `docs/default-workflows.md`

### 2. 默认能力 / 实验能力边界已成文

要求：

- 必须明确哪些是默认稳定能力
- 必须明确哪些仍是实验能力

证据目标：

- `docs/v1-boundary.md`

### 3. 包装层判断稳定

要求：

- `novel-package` 不只会给候选
- 还能判断：
  - 正文承载状态
  - 现有包装是否需要更新

证据目标：

- `docs/phase-10a-p0-smoke-results.md`
- `docs/phase-10a-p1-smoke-results.md`

### 4. 质量路由稳定

要求：

- `novel-review` 能稳定给出下一步动作
- `novel-precheck` 能稳定给出投稿建议
- `recommended_next_action` 可写回 state

证据目标：

- `docs/phase-10b-p0-smoke-results.md`
- `docs/phase-10b-p1-smoke-results.md`
- `e2e-novel/.mighty/state.json`

### 5. 样本闭环验证完整

要求：

- 至少有一个样本项目覆盖：
  - 起盘
  - 写作
  - 审查
  - 修复/润色/重写
  - 包装
  - 投稿前预检

证据目标：

- `e2e-novel`
- Phase 1-10 各轮 smoke / E2E 文档

### 6. 文档入口一致

要求：

- `README.md`
- `docs/start-here.md`
- `docs/skill-usage.md`

三者不能互相冲突。

证据目标：

- 入口文档实际内容

### 7. 实验能力未误导默认工作流

要求：

- `novel-scan` 仍被明确标为实验
- shared 治理增强不被包装成普通用户默认流程

证据目标：

- `docs/v1-boundary.md`
- `docs/default-workflows.md`

---

## 状态标记规则

后续 assessment 统一使用：

- `pass`
- `partial`
- `fail`
- `deferred`

其中：

- `pass`：有足够证据，当前已满足
- `partial`：方向已对，但证据还不够完整
- `fail`：当前不满足，且会阻塞 `1.0`
- `deferred`：目前不解决，但也不阻塞 `1.0`
