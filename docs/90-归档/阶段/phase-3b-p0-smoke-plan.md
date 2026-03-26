# Genm-codex Phase 3B / P0 Smoke Plan

## 目标

验证 `novel-index` 的最小可用性。

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 这轮允许写入 `.mighty/index.json`
- 除索引文件外，不应改动其他项目文件

## 1. `novel-index`

### 测试目标

验证它能真实构建一个轻量项目索引，并基于索引返回基础统计。

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-index skill，执行一次完整 build。

要求：
1. 读取：
   - `.mighty/state.json`
   - `chapters/`
2. 构建轻量索引到 `.mighty/index.json`
3. 只做第一版最小索引，不做重型实体抽取
4. 完成后只汇报：
   - 实际操作的项目根目录
   - 是否成功生成 `.mighty/index.json`
   - 已索引章节数
   - 主要统计项
   - 是否改动了除 `.mighty/index.json` 以外的其他文件
```

### 通过标准

- 确认正确项目目录
- 成功生成 `.mighty/index.json`
- 章节数与当前已写章节基本一致
- 返回至少一组基础统计
- 不误改其他项目文件
