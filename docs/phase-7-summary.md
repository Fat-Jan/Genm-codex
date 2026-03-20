# Genm-codex 第七阶段总结

## 范围

第七阶段不再直接扩普通本地 skill，而是转向两类高风险方向的契约与治理：

### Phase 7A：外部趋势扫描契约层

- `novel-scan` 的数据源分层
- 可信度分层
- 退化路径
- “仅报告 / 可回写”的边界

### Phase 7B：shared 资产治理层

- full-copy 现状分析
- selective-sync 治理方案
- shared 同步可观测性增强
- shared 依赖映射

## 已完成内容

### Phase 7A

已完成：

- [phase-7-scope.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-7-scope.md)
- [phase-7a-scan-contract.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-7a-scan-contract.md)

结论：

- `novel-scan` 暂不直接实现
- 先明确：
  - 数据源分层
  - 可信度规则
  - 固定输出结构
  - 回写边界

### Phase 7B

已完成：

- [phase-7b-selective-sync-governance.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-7b-selective-sync-governance.md)
- [shared-asset-dependency-map.md](/Users/arm/Desktop/vscode/Genm-codex/docs/shared-asset-dependency-map.md)
- [sync-shared-from-genm.sh](/Users/arm/Desktop/vscode/Genm-codex/scripts/sync-shared-from-genm.sh) 已补：
  - `--report`
  - `--domain <profiles|references|templates>`

已验证：

- `--report`
- `--report --domain profiles`
- `--report --domain references`

结论：

- 现在仍不直接切 selective-sync
- 但已经完成：
  - shared 同步的可观测性起步
  - shared 依赖面的文档化

## 本阶段带来的变化

到第七阶段结束时，`Genm-codex` 已经不只是有“能力实现”，还开始有：

- 高风险外部能力的契约边界
- shared 资产治理的可观测基础

这意味着后续再处理：

- `novel-scan`
- selective-sync

时，不会再从零开始摸边界。

## 当前结论

第七阶段已经完成到一个**治理与契约检查点**状态。

它不代表：

- `novel-scan` 已实现
- selective-sync 已切换

它代表：

- 这两条高风险方向已经被约束清楚，并且迈出了第一步低风险落地

## 还没做的事

- `novel-scan` 仍未正式实现
- selective-sync 仍未真正切换
- 若要继续，下一步应是：
  - `novel-scan` 的实验性实现
  - 或 shared 同步从“报告模式”进到“按域同步真正切换”
