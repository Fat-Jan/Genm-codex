# Findings Archive: 文档治理与安全归档方案（规划阶段）

> Status: `archived-findings-log`
>
> 本文件从 `findings.md` 中拆出，保留文档治理与安全归档专题结论。`findings.md` 主文件只保留导航入口与跨专题索引。

# Findings & Decisions: 文档治理与安全归档方案（规划阶段）

## Requirements
- 用户希望先梳理一轮“安全的文档治理与归档方案”，而不是立即大规模搬文件
- 目标是减少入口文档过长、历史与当前混杂、文件状态不透明、读入成本高的问题
- 约束是：不能影响 runtime / skill / script 行为，不能破坏项目功能

## Research Findings
- 当前仓库并不是纯文档仓库，`skills/*/SKILL.md` 会显式读取大量 `docs/*` 路径
- `README.md`、`docs/INDEX.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md` 已承担真实入口职责，属于“可瘦身但不可随意迁移”的文件
- `runtime-boundary-adr.md` 明确要求不引入第二真值中心，因此文档治理不能通过新的一套平行索引/状态系统替代现有 repo truth
- `docs/INDEX.md` 已经具备状态目录分层雏形：`00-当前有效 / 10-进行中 / 20-研究实验 / 90-归档`
- 当前真正的问题不是“马上归档所有老文档”，而是：入口文档越来越长、历史增量持续堆回主入口、接手者难以一眼判断文档状态

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 文档优先分成“不可动 / 可瘦身 / 可归档候选 / 仅补状态”四类 | 比直接说“哪些能归档”更贴合当前风险结构 |
| 优先在 `docs/INDEX.md` 和目录 README 中表达状态，而不是先大规模改文件名 | 改动成本更低，也更不容易破坏现有链接 |
| 物理归档放到第二阶段，并要求先检查显式路径引用 | 避免把 still-active 文档搬走后导致 runtime/skill 失效 |
| 后续治理改为“制度化整理”而非继续零散迁移 | 统一分类边界、根目录保留原则与状态标签语义，比继续零散搬文件收益更高 |

## Candidate Classification

### 不可动（路径级不可迁移）
- `README.md`
- `docs/INDEX.md`
- `docs/00-当前有效/start-here.md`
- `docs/00-当前有效/skill-usage.md`
- `docs/00-当前有效/default-workflows.md`
- `docs/00-当前有效/runtime-boundary-adr.md`

### 可瘦身（保留原路径）
- `README.md`
- `docs/00-当前有效/start-here.md`
- `docs/00-当前有效/skill-usage.md`
- `progress.md`
- `task_plan.md`

### 可归档候选 / 已处理结果
- `session-progress-2026-03-28.md` → 已迁入 `docs/90-归档/阶段/`
- `architecture-review-2026-03-28.md` → 已迁入 `docs/90-归档/阶段/`
- `cross-platform-support-plan.md` → 已迁入 `docs/20-研究实验/`
- `BATCH-COMPLETION-REPORT.md` → 已迁入 `docs/90-归档/阶段/`
- `v1.1-roadmap.md` / `v1.2-roadmap.md` / `v1.3-deferred-directions.md` → 已迁入 `docs/90-归档/阶段/`
- `v1.4-roadmap-review-2026-03-28.md` / `使用流程总览.md` → 已迁入 `docs/90-归档/阶段/`

## `docs/10-进行中/` 核心文件状态
- `cross-platform-entity-evidence-standard-v1.5.md` → `active-trial-standard`
- `profile-upgrade-evidence-protocol-v1.5.md` → `in-progress-protocol`
- `cross-platform-entity-evidence-agent-prompt-v1.5.md` → `supporting-prompt`
- `architecture-open-issues.md` → `active-open-issues`
- `batch-cross-platform-evidence-pack-v1.5.md` → `active-evidence-body`
- `batch-evidence-sidecar.json` → `active-machine-readable-sidecar`
- `batch-ontology-proposals.json` → `in-progress-ontology-proposals`

## Governance Deepening

### 根目录保留原则
- `docs/00-当前有效/root-retention-policy.md`

### 文档状态头制度
- `docs/00-当前有效/document-status-convention.md`

### 当前结论
- 文档治理专题已从 `findings.md` 主文件中拆出为独立附录
- 后续继续推进治理时，可优先更新本附录，再在主文件中保留导航入口
