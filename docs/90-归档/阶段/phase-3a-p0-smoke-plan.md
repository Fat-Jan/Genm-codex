# Genm-codex Phase 3A / P0 Smoke Plan

## 目标

验证以下两个新迁入 skill 的最小可用性：

- `novel-polish`
- `novel-genre`

项目目录统一使用：

- `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

## 测试约束

所有提示词都应显式声明：

- 只允许操作目标项目目录
- 如果上下文不是目标目录，则停止
- 除非测试目标需要，不额外修改无关文件

## 1. `novel-polish`

### 测试目标

验证单章轻量润色闭环是否可用，并确认它不会把“润色”误做成“重写”。

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-polish skill，对第003章执行一次轻量润色：

- chapter=3
- aspect=prose

要求：
1. 只做 prose 向精修，不改主线事件
2. 不把这次任务升级成 rewrite
3. 保存润色结果，并更新 `.mighty/state.json`
4. 如创建了备份，也在结果中说明

完成后只汇报：
- 实际操作的项目根目录
- 是否成功保存润色后的第003章
- 更新了哪些 state 字段
- 是否创建了备份文件
- 你为什么判定这次属于 polish 而不是 rewrite
```

### 通过标准

- 确认正确项目目录
- 成功保存 `chapters/第003章.md`
- 更新最少一组 polish 元数据
- 没有声称自己进行了结构性重写

## 2. `novel-genre`

### 测试目标

验证可用题材枚举和 profile 应用能力。

### 推荐提示词

```text
硬约束：只允许操作这个项目目录
/Users/arm/Desktop/vscode/Genm-codex/e2e-novel

如果你当前上下文不是这个目录，先切换到这个目录，再继续。
如果不能确认自己正在读取这个目录，就停止，不要继续。

在确认目录正确后，再使用 novel-genre skill，完成两件事：

1. 列出当前可用题材
2. 对当前项目执行一次 profile 检查与应用确认

要求：
- 先读取当前 `.mighty/state.json`
- 如果当前项目已经是 `玄幻 / 番茄`，不要乱改题材，只确认并重新应用对应 profile
- 输出中明确说明使用的是哪个 profile 文件
- 保存后只汇报：
  - 实际操作的项目根目录
  - 当前项目题材与平台
  - 使用了哪个 profile 文件
  - 更新了哪些 state 字段
  - 是否真的改动了题材，还是只是重新对齐 profile
```

### 通过标准

- 确认正确项目目录
- 能列出可用题材
- 能明确指出当前项目 profile 文件
- `state.json` 的 `genre_profile` / `platform_config` 更新逻辑合理
