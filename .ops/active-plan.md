# Active Plan

## Current Focus

- 已完成“`profile-expansion-first-batch-v1.5.md` 事实口径收口”这一具体维护动作。
- 当前建议继续结合并行 lane 的输出，决定样本维护、`crossover` 边界和 profile 扩面准备的下一步落点；这次修订后，第一批扩面说明已不再落后于当前资产覆盖。

## Scope

- 校正 `profile-expansion-first-batch-v1.5.md` 中过时的首批落地口径
- 明确“第一批已落地对象”与“当前标准 profile 已继续扩面”的区别
- 将本轮维护结果写回 active ops 记录

## Not In Scope

- 不做文档物理迁移
- 不修改 `skills/`、`shared/`、`scripts/` 运行逻辑
- 不实际新增 profile / overlay 资产

## Verification

- `bash scripts/validate-migration.sh`
- 回读 `docs/00-当前有效/profile-expansion-first-batch-v1.5.md`
- 必要时复核 `shared/profiles/` 当前覆盖统计

## Closure Status

- `profile-expansion-first-batch-v1.5.md` 已不再把平台差异覆盖说成只停留在首批个别样本。
- 文档现在明确区分：“第一批是谁”与“仓库现状已进一步推进到 52/52 标准 profile 覆盖”。
- 当前这份第一批说明页已更适合作为历史首批落地说明，而不是现状落后描述。
