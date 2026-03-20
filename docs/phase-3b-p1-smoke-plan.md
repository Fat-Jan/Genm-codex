# Genm-codex Phase 3B / P1 Smoke Plan

## 目标

验证扩展版 `novel-query` 的最小可用性。

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 默认走只读查询，不修改任何项目文件
- 优先利用：
  - `.mighty/state.json`
  - `.mighty/index.json`

## 1. `novel-query`

### 测试目标

验证它不仅能查当前 state，还能在索引存在时回答更强的“章节提及 / 模板统计 / 结构化轻查询”问题。

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-query skill，回答以下三件事：

1. 列出当前活跃伏笔
2. 告诉我哪些章节提到了“后山东壁”
3. 给我一个 project-stats 风格的简要概览

要求：
1. 优先读取：
   - `.mighty/state.json`
   - `.mighty/index.json`
2. 如果某项答案来自 index，请明确说
3. 不要改动任何文件

完成后只汇报：
- 实际操作的项目根目录
- 这三项查询结果
- 你主要依赖的是 state、index，还是两者结合
- 是否改动了任何文件
```

### 通过标准

- 确认正确项目目录
- 活跃伏笔回答正确
- 能给出“后山东壁”关联章节
- 能给出项目概览
- 明确说明是否用了 index
- 不修改任何文件
