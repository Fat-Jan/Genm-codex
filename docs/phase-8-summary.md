# Genm-codex 第八阶段总结

## 范围

第八阶段进入实验实现区，承接第七阶段的两类前置工作：

### Phase 8A：`novel-scan` report-only 实验版

- 不默认回写 profile
- 允许产出 `.mighty/market-data.json`
- 明确来源、可信度与 gaps

### Phase 8B：shared 同步的可观测增强

- `--report-json`
- 按域报告继续增强

## 验证结果

### Phase 8A

- `novel-scan`：通过

其中：

- `report-only`：已通过
- `project-annotate`：已通过
- 已生成真实的 `.mighty/market-data.json`
- 已在项目内 `market_adjustments` 下写入项目级建议
- 本次拿到官方番茄榜单快照
- 明确保留：
  - `confidence`
  - `gaps`
  - 不默认回写 profile

### Phase 8B

- `sync-shared-from-genm.sh --report-json`：通过

其中：

- 已能输出 machine-readable 的 shared 摘要
- 已验证：
  - `--report-json`
  - `--report-json --domain templates`

## 本阶段带来的变化

到第八阶段结束时，`Genm-codex` 已经开始具备：

- 高风险能力的实验性实现
- shared 资产治理的机器可读输出

这意味着后续如果继续推进：

- `novel-scan` 可以从 report-only 往更深层实验演进
- shared 治理也可以从“看得到”走向“按域切换”

## 当前结论

第八阶段已经完成到一个**实验实现检查点**状态。

## 还没做的事

- `novel-scan` 仍未进入默认生产模式
- selective-sync 仍未真正切换
- 若要继续，下一步将进入更高风险实验：
  - `novel-scan` 的 project-annotate / apply-suggestion 边界
  - shared 同步从报告模式进到真正按域同步
