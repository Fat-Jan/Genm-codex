# Genm-codex Phase 8A / P0 Scan Smoke Plan

## 目标

验证 `novel-scan` report-only 实验版的最小可用性。

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 这轮不要求真实联网抓取结果
- 允许写入：
  - `.mighty/market-data.json`
- 不允许默认回写 profile

## 1. `novel-scan`

### 测试目标

验证它在缺少可信外部数据时，不会伪造趋势，而是生成一个低可信度的 report-only 结果骨架。

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-scan skill，做一次 report-only 扫描：

- platform=番茄
- genre=玄幻
- depth=quick

要求：
1. 如果当前运行中没有可信外部数据，不要伪造趋势结论
2. 仍然要生成 `.mighty/market-data.json`
3. 结果里必须明确：
   - source plan
   - confidence
   - gaps
4. 不要改动 shared profile 或项目主状态

完成后只汇报：
- 实际操作的项目根目录
- 是否成功生成 `.mighty/market-data.json`
- 当前是实报告还是 skeleton
- confidence 是什么
- 是否改动了除 `.mighty/market-data.json` 外的其他文件
```

### 通过标准

- 确认正确项目目录
- 成功生成 `.mighty/market-data.json`
- 在缺数据时明确给出低可信度而不是伪造趋势
- 不改动 shared profile / 主状态
