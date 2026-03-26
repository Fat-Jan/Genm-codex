# Genm-codex `v1.0.0` 边界定义

> 历史阶段文档：本文记录的是正式发布前的边界判断；当前正式状态以 [v1-final-decision.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/v1-final-decision.md) 为准。

## 目的

这份文档定义：

- 什么能力已经可以视为默认稳定
- 什么能力仍属于实验或专家能力
- 哪些条件满足后，项目才适合进入 `v1.0.0`

它不是发布承诺，而是版本边界判断基线。

---

## 当前结论

截至 `v0.14.0` 之后的当前检查点，项目已经具备**接近 1.0 的主体能力面**，但还不建议直接发布 `v1.0.0`。

原因不是“能力不够多”，而是：

1. 默认工作流还没正式收口
2. 实验能力和默认能力的边界还没完全对外说清
3. `novel-scan` 仍然处于实验轨道
4. shared 同步虽然仍保留 full-copy 主路径，但治理语义已经升级

---

## 默认稳定能力

以下能力可以视为当前默认稳定主线的一部分：

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

### 4. 项目支撑

- `novel-status`
- `novel-query`
- `novel-retrieve`
- `novel-index`
- `novel-snapshot`
- `novel-resume`
- `novel-workflow`
- `novel-character`
- `novel-setting`
- `novel-foreshadowing`
- `novel-learn`

这些能力当前已经满足：

- 有明确 skill 形态
- 有至少一轮结构校验
- 有样本级 smoke 或 E2E 证据
- 有文档化阶段记录

---

## 实验能力

以下能力仍然应视为实验或专家能力：

### `novel-scan`

原因：

- 依赖外部趋势源
- 可信度和证据质量不稳定
- 目前虽已有：
  - `report-only`
  - `project-annotate`
  但仍不适合作为默认主工作流的一部分

### shared 同步治理增强

包括：

- `--report`
- `--domain`
- `--report-json`
- `shared/sync-governance.json`
- 默认阻断 `same-path drift overwrite`
- `--allow-drift-overwrite`
- sync 后恢复 protected local paths

这些能力当前更偏工程治理，不应被包装成普通写作者的默认流程。

当前判断补充：

- shared 同步仍然保留 full-copy 主路径
- 但已经不是“可无脑整包覆盖”的旧语义
- 当前正式接受的说法应是：
  - `governance-aware full-copy`
  - 有报告
  - 有 drift block
  - 有 protected local restore

### MCP memory / 调度融合

允许：

- 记录跨会话协作摘要
- 记录最近关注的问题编号
- 记录下一步建议或恢复提示

不允许：

- 复制 `state.json` / `state-archive.json` / `设定集/` 全量 canon
- 复制 `.mighty/learned-patterns.json` / `.mighty/market-adjustments.json` / `.mighty/active-context.json` 正文
- 让 memory 成为新的项目真值层

结论：

- 本地文件仍是唯一真值
- MCP memory 只做协调记忆，不做 canon 真源

### monolithic runtime / plugin framework

当前默认骨架仍然是：

- `docs + skills + scripts + sidecars`

明确不进入当前主线的方向：

- 独立 daemon
- 独立 scheduler
- plugin framework
- orchestration runtime

后续如果要增强，只能优先增强现有主线，不另起一套平行运行时。

---

## 当前明确不作为默认主线的内容

以下内容当前不需要阻塞 `v1.0.0`：

- `novel-help`
- `novel-tutorial`
- `novel-config`
- `novel-test`
- 历史草案类命令

原因：

- 它们不是核心写作质量链的一部分
- 很多已经 docs-first 化
- 缺它们不会破坏默认工作流

---

## `v1.0.0` 前置门槛

要进入 `v1.0.0`，至少满足下面 5 条：

### 1. 默认工作流文档化

必须有一份正式默认工作流文档，明确：

- 新书起盘
- 正文生产
- 投稿准备
- 持续学习

### 2. 默认能力与实验能力边界清晰

必须明确写清：

- 哪些能力默认推荐
- 哪些能力仅限实验或专家使用

### 3. 质量路由稳定

至少要满足：

- `review` 能给出稳定路由
- `precheck` 能给出稳定投稿建议
- `package` 能对正文承载和包装更新给出稳定判断

### 4. 样本验证闭环完整

至少有一个项目样本证明：

- 起盘
- 写作
- 审查
- 修复/润色/重写
- 包装
- 投稿前预检

这一整链可实际工作。

### 5. 文档入口统一

README、start-here、skill-usage 不能再互相打架。

---

## 当前还差什么

从今天这个检查点看，离 `v1.0.0` 最近的差距主要只剩：

1. 默认工作流正式文档
2. README / start-here / skill-usage 进一步统一
3. 对 `novel-scan` 的实验边界再明确一次

换句话说：

**现在更像“差一轮产品边界收口”，而不是“差很多实现”。**

---

## 当前判断

### 现在适合什么版本

- 继续维持 `0.x`
- 最近一个合理检查点是 `v0.15.0`

### 什么时候再讨论 `v1.0.0`

当默认工作流和实验边界都正式落文档后，再重新评估。

---

## 一句话结论

`Genm-codex` 现在已经接近 `1.0` 的主体能力面，但**还没到应该直接叫 `v1.0.0` 的时候**。  
下一步最值钱的是把“默认工作流”和“实验边界”正式收口。
