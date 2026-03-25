# Genm-codex Phase 5B / P0 Learn Smoke Plan

## 目标

验证 `novel-learn` 第一版的最小可用性。

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 这轮允许更新：
  - `.mighty/state.json` 中的 `learned_patterns`
- 不应假装自动抓取外部链接

## 1. `novel-learn`

### 测试目标

验证它能从现有章节范围中提炼写作模式，并保守更新 `learned_patterns`。

补充目标：

- 能从本地文件学习
- 在当前环境确实可抓取时，能从 retrievable URL 文本学习
- 不引入第二个风格中心

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-learn skill，从第001章到第003章提炼当前项目的写作模式，并保存结果。

要求：
1. 优先读取：
   - `.mighty/state.json`
   - `chapters/第001章.md`
   - `chapters/第002章.md`
   - `chapters/第003章.md`
2. 只做本地内容学习，不要假装抓外部链接
3. 保存后只汇报：
   - 实际操作的项目根目录
   - 你提炼出的主要模式
   - 更新了哪些 `learned_patterns` / `auto_learn_config` 字段
   - 是否改动了其他文件
```

### 通过标准

- 确认正确项目目录
- 学习结果来自本地章节
- 如提供本地文件，学习结果可明确说明来源是本地文件
- 如提供 URL，只有在当前环境真实抓到正文时才算 URL 学习成功
- 更新 `learned_patterns` 合理且不过度夸张
- 仍然优先写入 `.mighty/learned-patterns.json`
- 不新增 `style_profile.json` 这类平行 style center
- 不假装完成外部抓取
