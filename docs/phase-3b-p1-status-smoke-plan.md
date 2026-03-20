# Genm-codex Phase 3B / P1 Status Smoke Plan

## 目标

验证增强版 `novel-status` 的最小可用性。

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 默认走只读状态汇总，不修改任何项目文件
- 优先利用：
  - `.mighty/state.json`
  - `.mighty/index.json`

## 1. `novel-status`

### 测试目标

验证它能输出比第二阶段更完整的状态面板，至少覆盖：

- 进度
- 质量
- 伏笔时间线 / 风险桶
- index 统计

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-status skill，给我一个 full 模式的项目状态面板。

要求：
1. 优先读取：
   - `.mighty/state.json`
   - `.mighty/index.json`
2. 输出至少包含：
   - 进度概览
   - 质量状态
   - 伏笔状态或时间线
   - index 统计
   - 下一步建议
3. 如果某项来自 index，请说明
4. 不要改动任何文件

完成后只汇报：
- 实际操作的项目根目录
- 面板里的主要结论
- 你主要依赖的是 state、index，还是两者结合
- 是否改动了任何文件
```

### 通过标准

- 确认正确项目目录
- 给出完整面板而不是只有简短摘要
- 覆盖进度、质量、伏笔、index 统计
- 明确数据来源
- 不修改任何文件
