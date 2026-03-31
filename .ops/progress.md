# Active Progress

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
