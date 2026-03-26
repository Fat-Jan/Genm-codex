# Genm-codex `v1.0.0` 正式发布决策

## 结论

**建议现在正式发布 `v1.0.0`。**

---

## 决策依据

### 1. 当前无 blocker

依据：

- [v1-rc-blockers.md](/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/迁移与RC/v1-rc-blockers.md)

当前没有已确认 blocker。

### 2. 默认工作流已闭环

依据：

- [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/default-workflows.md)
- [v1-rc-execution-log.md](/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/迁移与RC/v1-rc-execution-log.md)

当前默认工作流已经在样本项目上形成完整闭环：

- 起盘
- 正文
- 审查
- 修复/润色/重写
- 包装
- 投稿前预检
- 导出
- 学习

### 3. 默认能力与实验能力边界清晰

依据：

- [v1-boundary.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/v1-boundary.md)

当前：

- 默认稳定能力已明确
- `novel-scan` 等实验能力已明确排除在默认工作流之外

### 4. 剩余观察项不阻塞正式版

当前仍在台账中的观察项主要是：

- `novel-scan` 仍为实验能力
- shared 当前采用 governance-aware full-copy，同步路径已收口，但 allowlist 仍需持续维护
- `review / precheck` 的判断口径存在颗粒度差异

这些都：

- 不属于默认工作流的结构性断裂
- 不阻塞默认稳定能力
- 已有明确边界说明

因此不构成正式版 blocker。

### 5. RC 期间样本文本问题已被消化

例如：

- 样本项目第 4 章的关键观察项已被定向修复
- 文本级观察项已关闭

说明 RC 并不是只停留在文档层，而是已经实际消化了样本问题。

---

## 为什么不是继续停在 RC

继续停在 `rc1` 的理由通常应当是：

- 仍有 blocker
- 默认工作流主线还不稳
- 默认 / 实验边界仍然模糊

但当前这三条都已经不成立。

如果继续无限期停在 RC，收益会越来越低，也会让版本语义开始失真。

---

## 正式版的边界

### `v1.0.0` 包含

- 默认工作流
- 默认稳定能力
- 已验证样本闭环
- 文档入口统一

### `v1.0.0` 不承诺

它并不意味着：

- 所有实验能力都已经正式稳定
- `novel-scan` 已进入默认主线
- shared 同步治理已终局完成

换句话说：

**正式版承诺的是默认主线稳定，不是所有边缘能力都终局稳定。**

---

## 建议动作

1. 正式发 `v1.0.0`
2. 保留：
   - `novel-scan` 实验标签
   - shared 治理增强的非默认定位
3. 后续进入：
   - `v1.x` 稳定演进阶段

---

## 一句话结论

当前的默认写作工作流、质量路由和包装层已经足够支撑正式版。  
因此，**现在可以结束 `rc1`，进入正式 `v1.0.0`。**
