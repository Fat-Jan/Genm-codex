# Genm-codex 第八阶段范围设计

## 设计结论

第八阶段不再是“稳定主线迁移”，而是**实验实现阶段**。

它承接第七阶段已经完成的两类前置工作：

- `novel-scan` 契约
- shared 资产治理

目标不是一次性把高风险能力做成正式版，而是先做：

- 可控实验
- 只读或弱副作用实现
- 可回退的演进

## 阶段划分

### Phase 8A：`novel-scan` 实验性 report-only 实现

目标：

- 在不默认回写 profile 的前提下，落一个可用的 report-only `novel-scan`

边界：

- 允许整理外部来源
- 允许产出 `.mighty/market-data.json`
- 不默认修改 `shared/profiles/`
- 不默认修改项目主状态

优先级：

- 先支持：
  - `report-only`
  - `project-annotate`
- 暂不支持：
  - `apply-suggestion`

当前进展：

- `report-only`：已完成
- `project-annotate`：进入实验实现

### Phase 8B：shared 同步的可观测升级

目标：

- 在不直接切 selective-sync 的前提下，继续增强 shared 同步可观测性

候选方向：

- `--report-json`
- 变更摘要文件
- 缺失资产探测
- skill 级受影响面提示

暂不做：

- 默认 selective-sync 切换
- 大规模 shared 路径改写

## 推荐实施顺序

1. `Phase 8A`
   - 先做 `novel-scan` 的 report-only 本地结果文件落盘
2. `Phase 8B`
   - 再做 shared 同步报告增强

## 版本边界建议

- **`v0.11.0`**：如果 `novel-scan` report-only 实验版稳定
- **`v0.12.0`**：如果 shared 同步可观测能力进一步增强

## 风险说明

### `novel-scan`

- 仍然属于高风险能力
- 即使进入实验实现，也必须保持：
  - 可信度分层
  - 明确来源
  - 不夸大结论

### shared 同步

- 一旦触及真实 selective-sync，就会影响大量 skill 的 shared 路径假设
- 所以第八阶段只建议继续“可观测升级”，不建议直接切换同步策略

## 当前推荐下一步

如果继续自动推进，第八阶段最合理的第一项是：

1. 为 `novel-scan` 做一个 **report-only 实验版**
2. 输出 `.mighty/market-data.json`
3. 明确标注来源和可信度

这是当前仍可控、且价值最高的实验方向。
