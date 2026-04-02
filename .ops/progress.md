# Active Progress

## 2026-04-02

- 对 `task_plan.md`、`current-processing-plan-phased-v1.md` 与 `v1.5-next-mainline-preparation-2026-03-31.md` 再做一轮最小收尾：把仍残留的 `v1.5` 当前态表述改成显式历史态/过渡态，并补充 `v1.6` 当前主线指针。
- 扩展 `tests/test_issue_regressions.py`，新增 legacy `v1.5` 文档必须显式声明历史定位的回归，防止后续又把这些过渡文档误写回当前主线说明。
- 第二轮收尾验证通过：
  - `pytest -q tests/test_issue_regressions.py` -> `24 passed`
  - `bash scripts/validate-migration.sh` -> passed
  - `python3 scripts/doctor_host_foundation.py` -> all checks pass

- 收掉 `start-here.md`、`skill-usage.md`、`root-retention-policy.md` 与 `.trae/rules/project-context.md` 中仍会把 `v1.5` 误读为当前主线的入口残留；当前口径统一为 `v1.6` 当前主线，`v1.5` 历史治理 lane / 直接上游参考。
- 扩展 `tests/test_issue_regressions.py`，新增 `v1.6` mainline entry consistency 回归，并将 `task_plan.md` 的旧标题断言改成符合当前 legacy archive + `.ops/active-plan.md` 指针语义的校验。
- 收尾验证通过：
  - `pytest -q tests/test_issue_regressions.py tests/test_host_support_projection.py tests/test_host_support_status_doc.py tests/test_setting_gate.py tests/test_shared_sync_governance.py tests/test_inkos_growth_plan.py tests/test_v14_doc_assets.py tests/test_worldview_motif_boundary.py tests/test_fanqie_launch_stack.py tests/test_opening_plot_framework.py tests/test_writing_core_framework.py` -> `132 passed`
  - `bash scripts/validate-migration.sh` -> passed
  - `python3 scripts/doctor_host_foundation.py` -> all checks pass
- 对本机 `Trae` / `Trae CN` 运行目录、日志与 sandbox 配置做最小手工验证，补到 project/global skills path、project-owned `.trae/mcp.json` file source 与 sandbox command execution 的 runtime 证据。
- 确认 `Trae CN` 会扫描当前仓库的 `.trae/skills` 路径，并在目录缺失时记录 `Skills directory does not exist`；同时确认 `SkillTool` 仍显示 `using remote definition`，因此 repo-owned local invocation 仍未闭环。
- 扩展 `host-evidence-ledger-v1.json`，新增 Trae manual verification 条目，覆盖 global skills、skill discovery、MCP file source、sandbox 与 skill invocation boundary。
- 更新 `host-capability-matrix-v1.json` 与 `host-support-status-v1.6.md`，把 Trae 从“只到 rules/context 面”的旧口径收紧为更准确的 `verified/partial/unsupported` 组合。
- 回写 `docs/20-研究实验/trae-capability-review-2026-04-02.md`，让文档从“等待手工验证”升级为“包含最小手工验证与 Gate 1 结论”的研究稿。
- 完成 `Gate 1` 判断：停在 `v1.6.1` 级增强，不正式进入有界 `v2`。

## 2026-04-01

- 新增 `v1.6-roadmap.md`，将跨宿主基础层正式收成当前主线 roadmap。
- 将 `README.md` 从 `v1.5` 当前主线切换为 `v1.6` 当前主线，并明确 `v1.5` 退为稳定基线与直接上游参考。
- 更新 `docs/INDEX.md`，让文档索引优先暴露 `v1.6-roadmap.md`，同时把 `v1.5-roadmap.md` 标成高可见上游参考。
- 更新 `.ops/active-plan.md`，使 active ops 当前 focus 与 `v1.6` 主线一致。
- 将 `v1.5-roadmap.md` 的状态头收口为 `archived-mainline-roadmap`，避免与 `v1.6-roadmap.md` 同时声称自己是当前主线。
- 复核并确认 `v1.6` Phase 1 四个子项均已完成：host matrix、install adapter、projection、doctor 当前都能通过定向测试与 doctor 自检。
- 运行 `python3 scripts/doctor_host_foundation.py --json`，结果为 `ok: true`，当前六项检查全部通过。
- 为 `render_skill_alias_plan.py` 增加 registry 投影输出，并让 `tests/test_skill_alias_plan.py` 覆盖当前 skill / alias registry 语义。
- 新增 `docs/00-当前有效/host-support-status-v1.6.md`，将宿主支持状态、退化策略与证据投影成当前有效文档。
- 新增 `tests/test_host_support_status_doc.py`，并扩展 `doctor_host_foundation.py` 以验证 host support doc 不漂移。
- 将根目录跨宿主单页 memo 迁入 `docs/90-归档/阶段/v1.6-host-foundation-implementation-memo.md`，完成 `Phase 2-C` 去冲突。
- 将 `v1.6-roadmap.md` 中 `Phase 2-C`、`Phase 3-A`、`Phase 3-B`、`Phase 3-C` 全部收口为 `[done]`。
- 新增 `docs/20-研究实验/host-foundation-v2-proposal-2026-04-01.md`，将下一版更优方案收成研究提案，重点提出“承诺层 + 证据层 + 能力面适配层”与 Trae 官方文档驱动研究 lane。
- 新增 `docs/20-研究实验/host-foundation-optimal-path-2026-04-01.md`，将“超高强度思考后的最优路径”收口为决策稿：先做证据层与 Trae capability audit，再通过显式决策门判断是否真的需要 `v2`。
- 新增 `shared/templates/host-evidence-ledger-v1.schema.json` 与 `host-evidence-ledger-v1.json`，作为最优路径中的第一步证据层资产。
- 新增 `docs/20-研究实验/trae-capability-review-2026-04-02.md`，将 Trae 按能力面拆成 `doc_verified / unknown / researching` 的审计基线。
- 扩展 `tests/test_state_contracts.py`、`doctor_host_foundation.py` 与 `validate-migration.sh`，让证据层与 Trae 审计进入最小验证链。
- 定向验证通过：
  - `tests/test_state_contracts.py -k 'host_capability_matrix or host_evidence_ledger'` -> `17 passed`
  - `tests/test_install_skills_matrix.py tests/test_host_support_projection.py tests/test_host_support_status_doc.py tests/test_host_foundation_doctor.py tests/test_skill_alias_plan.py tests/test_trae_capability_review_doc.py` -> `34 passed`
  - `python3 scripts/doctor_host_foundation.py --json` -> `ok: true`
  - `bash scripts/validate-migration.sh` -> passed

## 2026-03-31

- 新增 `project-map.yaml`，显式定义主真值、官方 E2E、synced/workspace/verfication 边界。
- 建立 `.ops/`，将 active plan / progress / findings / decisions 收敛到单一默认位置。
- 保留根目录 `task_plan.md`、`progress.md`、`findings.md` 作为 legacy 连续性承载层，避免破坏旧链接和历史导航。
- 对齐项目级 `AGENTS.md` 与 `README.md`，让代理和接手者优先读结构边界，而不是猜目录语义。
- 新增 `docs/90-归档/阶段/phase-18-summary.md`，将这一轮“结构收敛 + active ops 真源治理”正式收口为阶段总结。
- 将一次性治理记录移入 `docs/90-归档/阶段/active-ops-canonicalization-governance-2026-03-31.md`，避免 `docs/00-当前有效/` 继续承载阶段性执行记录。
- 对根目录 `progress.md`、`findings.md`、`task_plan.md` 顶部标题与摘要小节做命名层瘦身，进一步降低把 legacy 文件误读为当前 active 真源的概率。
- 将 `docs/10-进行中/architecture-open-issues.md` 收口为“已收口架构台账”定位，并同步对齐 `docs/10-进行中/README.md`、`docs/INDEX.md`、`架构问题跟踪.md` 与状态约定。
- 将 `weekly-governance-snapshot-2026-03-31.md` 中仍偏“待复检”的文案收紧为历史快照口径，并同步对齐 `biweekly-governance-review-2026-03-31.md` 与 `monthly-governance-phase-close-2026-03.md`。
- 将 `bucket-profile-slug-mapping.md` 中的过时映射草稿与“待实现”清单收口为 registry / runtime / 测试证据入口，并同步对齐 `shared/profiles/README.md` 的相关说明。
- 将 `chapter-structure-fields-design.md` 中的“建议接线 / 待实现”表述收口为当前 schema、consumer 与结构审计入口，并同步更新去历史化整理记录。
- 将 `v1.5-registry-consumer-and-scan-boundary-review-2026-03-31.md` 中已过时的 inventory 代表项改写为当前一般性回归风险说明，使其与前面几轮 inventory/design 文档收口结果一致。
- 将 `governance-maintenance-drill-2026-03-31.md` 中已闭环的 weekly snapshot 条目从当前保留项中移出，使其与后续 weekly/biweekly/monthly 的闭环状态保持一致。
- 对 `docs/00-当前有效/` 做收尾复检，并在 `current-effective-docs-hygiene-log-2026-03-31.md` 中写明：当前剩余阶段语义文档主要属于刻意保留的计划 / 模板 / 候选 / 复检类文档，这条低风险整理线已可结案。
- 校正 `shared/profiles/README.md` 中过时的 profile 计数与 overlay 覆盖描述：当前为 53 个顶层目录、52 个标准 profile，且标准 profile 已实现 52/52 的 `profile-tomato.yaml` 与 `bucket-*.yaml` 覆盖。
- 校正 `profile-expansion-first-batch-v1.5.md` 中过时的首批扩面口径：第一批仍是历史首批落地点，但当前标准 profile 已进一步推进到 52/52 的 `platform_positioning`、`profile-tomato.yaml` 与 `bucket-*.yaml` 覆盖。
- 校正 `profile-expansion-candidate-priority-v1.5.md` 中过时的下一批扩面目标：当前优先级已不再围绕“补基础 platform_positioning / overlay 文件”，而转向 consumer/readiness 收口与题材质量校准。
