# Genm-codex 第六阶段总结

## 范围

第六阶段不再新增核心写作 skill，而是处理“帮助与教程”这类更适合 docs-first 的能力边界。

### Phase 6A：帮助与教程层

采用 docs-first 方案完成：

- `README`
- `docs/00-当前有效/skill-usage.md`
- `docs/00-当前有效/start-here.md`

### Phase 6B：外部趋势扫描层

- `novel-scan` 继续暂缓

## 已完成内容

### Phase 6A

- 新增 [start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/start-here.md)
- 在 [README.md](/Users/arm/Desktop/vscode/Genm-codex/README.md) 中补齐入口导航
- 在 [skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/skill-usage.md) 中补齐快速跳转说明
- 在 [codex-migration-plan.md](/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/迁移与RC/codex-migration-plan.md) 中记录第六阶段范围

### docs-first 结论

当前这套仓库已经不再需要单独把：

- `novel-help`
- `novel-tutorial`

优先做成正式 skill。  
这两类需求已由文档入口承担。

## 当前结论

第六阶段 A 段已经完成到一个可验收状态。

这意味着当前 `Genm-codex` 已经具备：

- 1 到 5 阶段的主体 skill 体系
- 第 6 阶段的 docs-first 导航入口

## 仍然暂缓 / 未做

- `novel-scan` 继续暂缓
- 历史方案文档仍不迁移
- 后续如果要进入更高阶段，重点会转向：
  - 外部趋势扫描
  - selective-sync
  - 更严格的 release 治理
