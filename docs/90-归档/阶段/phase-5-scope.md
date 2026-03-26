# Genm-codex 第五阶段范围设计

## 设计结论

第五阶段不再扩核心创作链，而是处理前四阶段之后剩下的两类能力：

- **环境与连接引导**
- **学习与外部趋势能力**

同时明确：

- `help / tutorial` 更适合作为文档与入口文案维护，不一定值得继续单独 skill 化
- `scan` 依赖外部数据采集与联网能力，不能和本地纯 skill 层混为一谈

## 剩余候选盘点

当前仍未迁入 `Genm-codex` 的命令主要有：

- `novel-config`
- `novel-test`
- `novel-help`
- `novel-tutorial`
- `novel-learn`
- `novel-scan`

另有已定性为历史/参考文档的：

- `novel-content-generate-polish`
- `novel-inheritance`
- `novel-outline-intelligent`
- `novel-stats`

## 阶段划分

### Phase 5A：环境与连接引导层

目标：

- 补齐 Codex-native 体系里的本地配置检查与连接测试引导

范围：

- `novel-config`
- `novel-test`

定位：

- 这两者都是引导式能力，不是自动化控制器
- 重点是：
  - 检查
  - 解释
  - 引导
  - 本地写入建议

### Phase 5B：学习与外部趋势层

目标：

- 处理“从内容中学习”和“从外部趋势中学习”的能力边界

范围：

- `novel-learn`

暂缓：

- `novel-scan`

定位：

- `novel-learn` 可先做“本地内容学习 / 外部文本导入学习”
- `novel-scan` 因为强依赖联网扫描与外部平台采集，继续延后

## 单独说明

### `novel-help`

不建议继续单独 skill 化。

原因：

- Codex-native 体系更适合通过：
  - `README`
  - `skill-usage.md`
  - 各阶段 smoke 文档
  来承担帮助入口

### `novel-tutorial`

不建议在第五阶段优先 skill 化。

原因：

- 目前已有：
  - `README`
  - `skill-usage.md`
  - 多阶段 smoke 提示词
  已经承担了大部分教程职责
- 如果以后要做，也更像“面向用户的交互教程壳”，不一定该优先做成核心 skill

## 实施顺序

1. `novel-config`
2. `novel-test`
3. `novel-learn`

## 版本边界建议

- **`v0.7.0`**：以 `Phase 5A` 为主要封版目标
- **`v0.8.0`**：如继续推进 `novel-learn`，可作为 `Phase 5B` 版本

## 本阶段明确不做

- 不迁移 `novel-help` 为正式 skill
- 不优先迁移 `novel-tutorial`
- 不在第五阶段强推 `novel-scan`
- 不复活历史方案文档型命令

## 当前推荐下一步

第五阶段正式实施时，先从 **Phase 5A / P0** 开始：

1. `novel-config`
2. `novel-test`

原因：

- 它们最适合先收掉剩余的“引导式环境能力”
- 和前四阶段的本地 skill 体系冲突最小
- 比 `learn / scan` 更容易在当前环境里做出稳定第一版
