# Genm-codex Phase 4B / P1 Spinoff Smoke Plan

## 目标

验证 `novel-spinoff` 第一版的最小可用性。

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 这轮允许生成一个明确标识的番外文件
- 不应假装进入多书宇宙系统

## 1. `novel-spinoff`

### 测试目标

验证它能在当前单项目内写一个轻量番外，并明确标识它不是主线正文章节。

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-spinoff skill，写一个轻量番外：

- type=角色篇
- focus_character=林晚照
- chapter=番外1
- word_count=1800

要求：
1. 只使用当前单项目作为 canon 来源
2. 不要假装进入 `.mighty/books/` 多书结构
3. 结果必须明确标识为番外，而不是主线第004章之类的正文章节
4. 保存后只汇报：
   - 实际操作的项目根目录
   - 输出文件路径
   - 这是哪种番外
   - 你用了哪些 canon 约束
   - 是否改动了 `.mighty/state.json`
```

### 通过标准

- 确认正确项目目录
- 成功生成明确标识的番外文件
- 不伪装多书结构
- 能说明 canon 约束
- 不错误推进主线章节号
