# Active Plan

## Current Focus

- 最优路径的第二步已经完成：Trae 最小手工验证已补齐到本机 runtime 证据。
- 当前 focus 已从“进入 Trae 手工验证”切换为“按 `Gate 1` 结论维持 `v1.6.1` 级增强，不进入有界 `v2`”。

## Scope

- 保留已落地的证据层、Trae 审计结果与最小手工验证结果
- 将 `Gate 1` 结论收口为 `v1.6.1` 级增强，而不是结构升级
- 维持当前 `v1.6` consumer 与研究层新增资产之间的兼容关系

## Not In Scope

- 不新增 runtime / plugin / daemon
- 不直接升级到完整 `v2`
- 不在没有手工验证前把 Trae 改成 installable host

## Verification

- `pytest -q tests/test_state_contracts.py -k 'host_capability_matrix or host_evidence_ledger'`
- `pytest -q tests/test_install_skills_matrix.py tests/test_host_support_projection.py tests/test_host_support_status_doc.py tests/test_host_foundation_doctor.py tests/test_skill_alias_plan.py tests/test_trae_capability_review_doc.py`
- `python3 scripts/doctor_host_foundation.py --json`
- `bash scripts/validate-migration.sh`
- 回读 `docs/20-研究实验/host-foundation-optimal-path-2026-04-01.md`
- 回读 `docs/20-研究实验/trae-capability-review-2026-04-02.md`

## Closure Status

- legacy / 过渡文档的 `v1.5` 残留时态也已收口：`task_plan.md`、`current-processing-plan-phased-v1.md` 与 `v1.5-next-mainline-preparation-2026-03-31.md` 现在都明确标成历史判断，不再误导为当前主线说明。
- 当前主线入口残留已收口：`start-here.md`、`skill-usage.md`、`root-retention-policy.md` 与 `.trae/rules/project-context.md` 不再把 `v1.5` 误写成当前主线。
- 当前仓库已经同时具备：
  - `v1.6` 已完成的宿主基础层
  - 下一轮决策所需的证据层
  - Trae 官方文档驱动的能力面审计基线
  - Trae 本机 runtime 最小手工验证结果
- `Gate 1` 已收口：当前新增事实仍属于证据等级提升，不足以触发有界 `v2`；仓库应停在 `v1.6.1` 级增强。
