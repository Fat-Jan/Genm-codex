# Genm-codex `v1.0.0` Readiness Assessment

## 评估目的

这份文档基于：

- [v1-readiness-checklist.md](/Users/arm/Desktop/vscode/Genm-codex/docs/v1-readiness-checklist.md)
- [v1-boundary.md](/Users/arm/Desktop/vscode/Genm-codex/docs/v1-boundary.md)

对当前项目是否适合进入 `v1.0.0` 候选期做正式判定。

---

## 总结结论

### 总体判断

- **当前不建议直接发布 `v1.0.0`**
- **当前可以进入 `v1.0.0-rc1` 讨论期**

原因不是还缺很多能力，而是：

- 默认能力面已经够
- 默认工作流已经成文
- 样本链路也已基本闭环
- 但仍值得先经历一轮更正式的 RC 式稳定化检查

也就是说：

**当前状态更像“没有明显 blocker，但还应先走一次 RC”，而不是“还远没到 1.0”。**

---

## Checklist Assessment

### 1. 默认工作流已成文

- 状态：`pass`
- 证据：
  - [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/default-workflows.md)
  - [start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/start-here.md)

判断：

- 已覆盖：
  - 新书起盘
  - 正文生产
  - 投稿准备
  - 持续学习

---

### 2. 默认能力 / 实验能力边界已成文

- 状态：`pass`
- 证据：
  - [v1-boundary.md](/Users/arm/Desktop/vscode/Genm-codex/docs/v1-boundary.md)

判断：

- 默认稳定能力与实验能力已经明确区分
- `novel-scan` 仍明确在实验区

---

### 3. 包装层判断稳定

- 状态：`pass`
- 证据：
  - [phase-10a-p0-smoke-results.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-10a-p0-smoke-results.md)
  - [phase-10a-p1-smoke-results.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-10a-p1-smoke-results.md)
  - [简介方案.md](/Users/arm/Desktop/vscode/Genm-codex/e2e-novel/包装/简介方案.md)

判断：

- `novel-package` 不只是会生成包装候选
- 已能判断：
  - 正文承载状态
  - 现有包装是否需要更新

---

### 4. 质量路由稳定

- 状态：`pass`
- 证据：
  - [phase-10b-p0-smoke-results.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-10b-p0-smoke-results.md)
  - [phase-10b-p1-smoke-results.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-10b-p1-smoke-results.md)
  - [state.json](/Users/arm/Desktop/vscode/Genm-codex/e2e-novel/.mighty/state.json)

判断：

- `novel-review` 已能把 `recommended_next_action` 写回 state
- `novel-precheck` 已能给出：
  - `ready-now`
  - `revise-then-submit`
  - `packaging-needs-update: yes|no`

---

### 5. 样本闭环验证完整

- 状态：`pass`
- 证据：
  - [e2e-novel](/Users/arm/Desktop/vscode/Genm-codex/e2e-novel)
  - [第004章.md](/Users/arm/Desktop/vscode/Genm-codex/e2e-novel/chapters/第004章.md)
  - [简介方案.md](/Users/arm/Desktop/vscode/Genm-codex/e2e-novel/包装/简介方案.md)
  - 各阶段 smoke / E2E 结果文档

判断：

- 样本项目已经覆盖：
  - 起盘
  - 写作
  - 审查
  - 修复/润色/重写
  - 包装
  - 投稿前预检

---

### 6. 文档入口一致

- 状态：`pass`
- 证据：
  - [README.md](/Users/arm/Desktop/vscode/Genm-codex/README.md)
  - [start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/start-here.md)
  - [skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/skill-usage.md)

判断：

- 当前三份入口文档已经对齐到：
  - 默认工作流
  - 默认能力
  - 实验能力边界

---

### 7. 实验能力未误导默认工作流

- 状态：`pass`
- 证据：
  - [v1-boundary.md](/Users/arm/Desktop/vscode/Genm-codex/docs/v1-boundary.md)
  - [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/default-workflows.md)

判断：

- `novel-scan` 仍然明确在实验区
- shared 治理增强也没有被写成普通用户默认步骤

---

## Blocker Assessment

### 当前 blocker

- 无明确 `fail` 级 blocker

### 当前仍值得谨慎的点

- `novel-scan` 仍为实验能力，不适合作为默认推荐
- shared full-copy 策略虽然当前可接受，但如果未来要进更强产品化，仍值得再评估

这些点目前更适合视为：

- **非 blocker**
- 但仍需在 RC 阶段继续观察

---

## 当前建议

### 不建议

- 现在就直接打 `v1.0.0`

### 建议

- 先进入 **`v1.0.0-rc1` 候选讨论期**
- 同时保留：
  - `novel-scan` 实验标签
  - shared 治理增强的非默认定位

---

## 一句话结论

`Genm-codex` 当前已经具备**进入 `v1.0.0-rc1` 讨论期**的条件，  
但还不建议跳过 RC，直接进入正式 `v1.0.0`。
