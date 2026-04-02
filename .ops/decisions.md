# Active Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-31 | 新建 `project-map.yaml` | 让项目结构边界有单一、机器可读的入口。 |
| 2026-03-31 | 新建 `.ops/` 作为 active ops 默认位置 | 避免根目录继续漂浮新的计划、进度、发现类文件。 |
| 2026-03-31 | 保留根目录 legacy ops 文件 | 先维持历史连续性与旧链接稳定，再决定后续物理迁移。 |
| 2026-03-31 | 明确 `e2e-novel/` 为官方最小 E2E 样本 | 避免 `smoke/`、`projects/`、`e2e-novel/` 争夺同一角色。 |
| 2026-03-31 | 将 active ops 真源治理线收口为阶段总结，并把执行记录归档到 `docs/90-归档/阶段/` | 当前结构已稳定，剩余问题为低风险认知治理，适合结案后转向新任务。 |
| 2026-03-31 | 将根目录 legacy ops 顶部标题与摘要统一瘦身为更明确的 `legacy` 命名 | 进一步降低将仓库根目录误读为当前 active ops 真源的概率，同时不改动历史正文。 |
| 2026-03-31 | 将 `architecture-open-issues.md` 改为“已收口架构台账”定位，并保留原路径 | 当前全量 AOI 已 `resolved`；保链接稳定比立即迁移路径更低风险。 |
| 2026-03-31 | 将 `weekly-governance-snapshot-2026-03-31.md` 收紧为明确的历史快照口径，并同步对齐双周/月度文档 | 保留原始发现事实，同时去掉“当前待复检”误读，是更低风险的治理文档一致性修正。 |
| 2026-03-31 | 将 `bucket-profile-slug-mapping.md` 改为以 registry / runtime / tests 为准的现状入口 | 文档内硬编码映射函数与当前 state/runtime 口径已漂移，直接指向现有真值比继续维护设计草稿更稳。 |
| 2026-03-31 | 将 `chapter-structure-fields-design.md` 改为以 schema / consumer / 审计入口为准的现状文档 | 章结构字段已落地到 state、consumer 与审计测试；继续保留“建议接线 / 待实现”语义会误导接手判断。 |
| 2026-03-31 | 将 registry / consumer 复检文档中的旧代表项改写为当前泛化风险 | 当具体代表项已闭环时，继续挂在风险章节会制造“问题仍存在”的错觉。 |
| 2026-03-31 | 将 governance drill 文档中的已闭环案例移出当前保留项 | 当后续治理已完成闭环时，保留项应回到真正仍需长期盯住的治理纪律。 |
| 2026-03-31 | 将“当前有效文档去历史化整理”定性为已达到收口条件 | 当前剩余阶段语义文档多为刻意保留的计划 / 模板 / 候选 / 复检类文档，继续批量清理收益已明显下降。 |
| 2026-03-31 | 将 `shared/profiles/README.md` 改为以当前目录结构与覆盖数为准的现状说明 | 旧 README 继续传播“54 个 profile / 大部分 overlay 未实现”的过时口径，已不符合当前 profile 资产状态。 |
| 2026-03-31 | 将 `profile-expansion-first-batch-v1.5.md` 改为“历史首批落地 + 当前覆盖现状”双层说明 | 当首批说明页继续用旧阶段覆盖口径描述现状时，会误导扩面准备判断。 |
| 2026-03-31 | 将 `profile-expansion-candidate-priority-v1.5.md` 改为以 consumer/readiness 收口为准的下一批目标 | 当标准 profile 的基础覆盖已补齐后，继续把“补基础文件”当成下一批首要目标会误导扩面顺序。 |
| 2026-04-01 | 将跨宿主基础层正式升级为 `v1.6` 主线 roadmap | 这条线已经有 matrix / projection / doctor / tests 的实现骨架，继续只靠研究稿与单页 memo 承载会造成主线状态与工作区实现脱节。 |
| 2026-04-01 | 将 `v1.6` Phase 1 定性为已完成 | host truth / install adapter / projection / doctor 四个子项均已通过定向测试、doctor 自检和迁移校验，继续把它写成“待补完”会误导后续执行顺序。 |
| 2026-04-01 | `v1.6` Phase 3 继续复用 `skill-merge-map-v1.json` 与 `host-capability-matrix-v1.json` 作为真值，不新增平行手写 registry | 这能用最少的新事实文件完成 registry convergence，同时避免 skill / host 两条线各自再分裂出第二真值中心。 |
| 2026-04-01 | 将跨宿主单页说明迁入 `docs/90-归档/阶段/` 而不是继续保留在根目录 | 当 roadmap、README、`.ops` 和当前有效文档已经接管真值职责后，根目录 memo 更适合作为历史备忘归档。 |
| 2026-04-01 | 将下一版宿主基础层优化方案先定性为 `research`，不直接改动 `v1.6` contract | 当前更优方向已经明确，但仍涉及证据层、能力面模型与 Trae 文档驱动验证，先收成研究提案比直接改动稳定真值更稳。 |
| 2026-04-01 | 将“证据层优先 + Trae 审计优先 + 决策门后置”定为当前最优下一步 | 直接推进 `v2` 仍然过早；先把未知数变成已知，再决定是否重构，能同时最小化误建模风险与迁移成本。 |
| 2026-04-02 | 先落 `host-evidence-ledger-v1` 与 `Trae capability review`，暂不推进 `v2` 数据结构 | 这是当前最优路径中收益最高、风险最低、且不破坏 `v1.6` consumer 的第一步。 |
| 2026-04-02 | 将证据层与 Trae 审计接入最小验证链 | 如果这两个资产不能进入 contract tests、doctor 和结构校验，它们就仍然只是研究材料，不足以支撑后续 `Gate 1` 决策。 |
| 2026-04-02 | `Gate 1` 先停在 `v1.6.1` 级增强，不正式进入有界 `v2` | 当前新增事实主要提升了 Trae 的证据等级，而没有逼出新的主真值结构；`unsupported install + partial/verified capability boundary + evidence ledger` 仍足以表达现状。 |
