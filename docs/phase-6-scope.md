# Genm-codex 第六阶段范围设计

## 设计结论

到第五阶段结束后，剩余未处理项已经不再是核心创作能力，而是两类边缘但仍有价值的能力：

- **帮助与教程层**
- **外部趋势扫描层**

这一阶段不再追求“继续堆一批新 skill”，而是要明确：

1. 哪些内容更适合 docs-first
2. 哪些内容需要依赖外部能力，不能在当前纯本地节奏里硬推进

## 剩余项盘点

当前仍未迁入 `Genm-codex` 的命令主要有：

- `novel-help`
- `novel-tutorial`
- `novel-scan`

以及已明确不建议迁移的历史/参考文档：

- `novel-content-generate-polish`
- `novel-inheritance`
- `novel-outline-intelligent`
- `novel-stats`

## 阶段划分

### Phase 6A：帮助与教程层

目标：

- 把现有分散在 README、skill-usage、阶段 smoke 文档里的使用引导整理成更稳定的 docs-first 入口

范围：

- `novel-help`
- `novel-tutorial`

策略：

- 默认不强制 skill 化
- 优先通过：
  - `README`
  - `docs/skill-usage.md`
  - 新增的教程/导航文档
  来承担帮助和教程职责

只有当 docs-first 方案明显不够用时，才考虑再单独 skill 化

### Phase 6B：外部趋势扫描层

目标：

- 明确 `novel-scan` 在 Codex-native 体系中的定位与边界

范围：

- `novel-scan`

策略：

- 继续暂缓正式迁移
- 在没有稳定外部采集契约前，不直接做成默认可用 skill
- 先保留为“未来联网增强层”的候选

## 为什么这样分

### `novel-help`

更像入口索引，而不是能力本身。  
在 Codex-native 体系里，用户真正需要的不是“再开一个帮助命令”，而是：

- 能快速找到该用哪个 skill
- 能快速找到一条最小可执行提示词

这更适合文档承担。

### `novel-tutorial`

本质上也是引导体验问题。  
目前已经有：

- `README`
- `skill-usage.md`
- 多阶段 smoke 提示词

它们已经覆盖了大量新手引导职责。

### `novel-scan`

它有价值，但它和前五阶段所有 skill 的共性不一样：

- 强依赖外部平台
- 强依赖联网抓取
- 强依赖数据源稳定性

这类能力如果硬塞进当前本地 skill 节奏，只会重新制造不稳定边界。

## 推荐实施顺序

1. 先做 `Phase 6A`
2. 再决定 `Phase 6B` 是否有足够条件启动

## 版本边界建议

- **`v0.9.0`**：如果完成 docs-first 帮助/教程收口
- **`v1.0.0`**：只有在你确认：
  - 当前主体迁移已经足够稳定
  - 文档入口清晰
  - 版本边界明确
  才值得讨论

## 本阶段明确不做

- 不迁移历史方案文档型命令
- 不在没有稳定外部契约前强推 `novel-scan`
- 不为了追求“命令全覆盖”而继续制造低价值 skill

## 当前推荐下一步

第六阶段正式实施时，先做 **Phase 6A / docs-first 收口**：

1. 整理帮助入口
2. 整理新手教程入口
3. 给现有 skill 和阶段文档建立清晰导航

这一步做完后，再决定是否值得往 `v0.9.0` 推进。
