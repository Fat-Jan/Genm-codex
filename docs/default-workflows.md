# Genm-codex 默认工作流

## 目的

这份文档定义当前默认推荐给用户的工作流。

它回答两个问题：

1. 如果我是普通用户，我现在最该怎么用
2. 哪些 skill 是默认主线，哪些只是补充或实验能力

---

## 默认工作流 1：新书起盘

适用场景：

- 从零开始一个新项目

推荐顺序：

1. `novel-init`
2. `novel-genre`
3. `novel-outline`
4. `novel-package`

目标：

- 建好项目骨架
- 选定题材 / 平台
- 形成总纲与章纲
- 形成第一版包装方案

最小原则：

- 先有书的方向
- 再写正文

---

## 默认工作流 2：正文生产

适用场景：

- 已有项目，正在稳定推进章节

推荐顺序：

1. `novel-write`
2. `novel-review`
3. 根据 review 路由进入：
   - `novel-fix`
   - `novel-polish`
   - `novel-rewrite`

目标：

- 先把章节写出来
- 再做审查
- 再按问题类型修

推荐规则：

- 局部问题 -> `novel-fix`
- 语言层问题 -> `novel-polish`
- 结构层问题 -> `novel-rewrite`

---

## 默认工作流 3：投稿准备

适用场景：

- 已有一批章节，准备对外发布

推荐顺序：

1. `novel-precheck`
2. `novel-package`
3. `novel-export`

目标：

- 先判断能不能投
- 再看包装要不要更新
- 最后导出

推荐规则：

- `precheck = ready-now` 且 `packaging-needs-update = no`
  - 可以直接进入导出
- `precheck = revise-then-submit`
  - 先回正文修
- `packaging-needs-update = yes`
  - 先回包装层

当前已验证的番茄女频样本里，最靠近这条工作流完成态的是：

- [fanqie-evil-gongdou-submission-assessment.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-evil-gongdou-submission-assessment.md)
  - `恶女 x 宫斗宅斗`
  - 结论：`ready-now`

---

## 默认工作流 4：持续学习

适用场景：

- 已经写了一批章节，希望风格更稳

推荐顺序：

1. `novel-learn`
2. `novel-status`

可选补充：

- `novel-query`
- `novel-retrieve`

目标：

- 从已有正文中提炼可复用模式
- 让写作偏好稳定沉淀

---

## 默认工作流中的辅助能力

这些不是主链，但很常用：

### 项目状态 / 查询

- `novel-status`
- `novel-query`
- `novel-index`

### 快速引用

- `novel-retrieve`

### 设定维护

- `novel-character`
- `novel-setting`
- `novel-foreshadowing`

### 恢复与回溯

- `novel-snapshot`
- `novel-resume`
- `novel-workflow`

---

## 当前不属于默认工作流的能力

### `novel-scan`

原因：

- 仍属于实验能力
- 它能提供市场信号，但不该成为每个用户默认要跑的步骤

---

## 当前 Fanqie-first 真实状态

- 第一条内部生产模板：
  - `恶女 x 宫斗宅斗`
- 首个可投样本：
  - `恶女 x 宫斗宅斗`
- 第二条生产模板候选：
  - `恶女 x 现实情感`
- 第三条实验线：
  - `恶女 x 现言甜宠`

### `novel-config` / `novel-test`

原因：

- 更像环境和连接引导
- 不是日常写作主线

### `novel-help` / `novel-tutorial`

原因：

- 当前已由 docs-first 承担

---

## 最短建议

如果你不知道该用哪个 skill，先套这条判断：

1. 没项目：`init -> genre -> outline -> package`
2. 有项目想继续写：`write -> review -> fix/polish/rewrite`
3. 想投稿：`precheck -> package -> export`
4. 想稳住风格：`learn -> status`

---

## 一句话结论

当前默认主线已经不是“堆很多命令”，而是：

- 起盘
- 写作
- 审查修正
- 包装
- 投稿准备
- 持续学习

这 6 步。
