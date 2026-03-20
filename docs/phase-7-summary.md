# Genm-codex 第七阶段总结

## 范围

第七阶段不再直接扩普通本地 skill，而是转向两类高风险方向的契约与治理：

### Phase 7A：外部趋势扫描契约层

- `novel-scan` 的数据源分层
- 可信度分层
- 退化路径
- “仅报告 / 可回写”的边界

### Phase 7B：shared 资产治理层

- `shared` full-copy 现状分析
- selective-sync 治理方案
- 同步可观测性增强

## 已完成内容

### Phase 7A

已完成：

- [phase-7-scope.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-7-scope.md)
- [phase-7a-scan-contract.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-7a-scan-contract.md)

结论：

- `novel-scan` 不适合在没有稳定外部契约前直接变成默认可用 skill
- 在真正实现前，至少需要：
  - 数据源分层
  - 可信度规则
  - 固定输出结构
  - 明确回写边界

### Phase 7B

已完成：

- [phase-7b-selective-sync-governance.md](/Users/arm/Desktop/vscode/Genm-codex/docs/phase-7b-selective-sync-governance.md)
- [sync-shared-from-genm.sh](/Users/arm/Desktop/vscode/Genm-codex/scripts/sync-shared-from-genm.sh) 新增：
  - `--report`
  - `--domain <profiles|references|templates>`

已验证：

- `--report`
- `--report --domain profiles`

结论：

- 现在还不适合直接切换 selective-sync
- 但已经迈出第一步：
  - 让 shared 同步变得可观测
  - 支持按域查看

## 本阶段带来的变化

到第七阶段结束时，`Genm-codex` 已经不仅有主体 skill 体系，还开始建立更高层的治理能力：

- 外部能力先契约化
- shared 资产先可观测化

这意味着后续高风险能力不再会直接“裸上”，而是先有约束、再有实现。

## 当前结论

第七阶段已经完成到一个**治理与契约检查点**状态。

这不是“`novel-scan` 已完成”，而是：

- `novel-scan` 的实现前约束已写清
- selective-sync 的实现前治理已起步

## 还没做的事

- `novel-scan` 仍未正式实现
- selective-sync 仍未真正切换
- 若要继续，下一步应是：
  - `novel-scan` 的实验性实现
  - 或 `shared` 同步的按域/按子域升级
