# `v1.5` Skill Overlap Inventory

> 本文已被 [skill-rationalization-policy.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/skill-rationalization-policy.md) 和 [skill-merge-map-v1.5.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/skill-merge-map-v1.5.md) 消费，保留为过程盘点记录。

## 目的

这份文档完成了 `P1-E` 的 overlap 盘点，不直接触发 skill merge。

它当前只回答：

- 哪些 skill 有明显重叠
- 哪些更适合先做 alias / deprecation 说明
- 哪些应继续视为 protected

---

## 当前应视为 `protected` 的主链与高频入口

当前至少应继续视为 `protected`：

- `novel-init`
- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-close`
- `novel-status`
- `novel-query`
- `novel-precheck`
- `novel-package`
- `novel-scan`

原因很简单：这些 skill 不是单纯命名问题，而是默认工作流、高频 consumer 或实验边界的一部分。

---

## 当前 overlap 最明显的几组

### 1. `novel-retrieve` / `novel-query`

重叠点：

- 都是读项目信息
- 都承担“快速查当前项目事实”的职责

当前建议：

- 先视为 overlap inventory 对象
- 后续更适合走 alias / quick mode，而不是直接删任一入口

### 2. `novel-batch` / `novel-write`

重叠点：

- `novel-batch` 的核心能力仍围绕写作推进
- 差异主要在批量推进和默认不自动 close

当前建议：

- 先保留独立调用面
- 在说明稿中强调它是写作主线的批量变体，而不是完全独立体系

### 3. `novel-workflow` / `novel-resume`

重叠点：

- 都与恢复、状态、事务位置有关
- 都服务于“现在卡在哪、下一步做什么”

当前建议：

- 先保持双入口
- 后续只做职责边界说明，不做立刻合并

### 4. `novel-fix` / `novel-polish` / `novel-rewrite`

重叠点：

- 都是“收口后修章”的动作层
- 对用户来说最容易误解成三套平行修稿系统

当前建议：

- 不做真合并
- 只做说明收口：局部问题→`fix`，语言层→`polish`，结构层/两轮未收口→`rewrite`

---

## 当前更适合先做 alias 说明的部分

### 安装名 alias

继续保留：

- `novel-*`
- `genm-novel-*`

这一层在 `v1.5` 里仍应作为兼容 alias 层，而不是优先裁撤对象。

### 调用面 alias 候选

当前可以先做说明稿，不做实现的候选：

- `novel-retrieve` 作为 `novel-query` 的快速检索面
- `novel-batch` 作为 `novel-write` 的批量推进面

---

## 当前不应做的事

这份 inventory 当前不支持：

- 直接删 skill
- 直接改 frontmatter 名称
- 直接删安装脚本入口
- 直接宣布 `31 -> 25` 已落地

它的作用只是把 overlap 讲清楚，为后续 merge map 文档化做准备。
