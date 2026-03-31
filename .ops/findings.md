# Active Findings

## Current Findings

- 根目录同时存在 `task_plan.md`、`progress.md`、`findings.md`，说明 active ops 状态此前没有单一默认落点。
- `e2e-novel/` 已经承担官方最小 E2E 样本的角色，`smoke/` 更适合作为专项验证资产，而不是第二套官方样本体系。
- `shared/` 的真实语义是 synced boundary，不是普通源码目录。
- `projects/` 是工作区，不应该被当作产品真值或规则文档承载层。
- 根目录 legacy ops 顶部标题与摘要语义已进一步瘦身为更明确的 `legacy` 命名，误判“当前 active 真源”的风险继续下降。
- 当前这条“结构收敛 + active ops 真源治理”线已无建议继续动作，不阻塞转去新的具体治理/维护任务。
- `architecture-open-issues.md` 虽仍位于 `docs/10-进行中/`，但其实际内容已经是全量 `resolved`；将其改成“已收口架构台账”定位，比直接迁移路径更低风险。
- 根目录 `架构问题跟踪.md` 若继续维持“还有哪些架构问题没有收口”的口径，会与正式台账形成双口径，因此已一并对齐。
- `weekly-governance-snapshot-2026-03-31.md` 当前更适合明确为历史快照记录，而不是继续混用“后续已闭环”和“待复检”两种语义。
- 只要保留原始发现事实、同时写清后续闭环状态，就能在不抹平历史的前提下降低治理误判。
- `bucket-profile-slug-mapping.md` 的主要问题不只是 checklist 旧，而是把未落地或已漂移的 slug 方案写成了当前 state / runtime 口径。
- 当前更可靠的真值组合是：`profile-bucket-registry-v1.json` + `scripts/profile_contract.py` + 相关 tests；文档应把它们作为入口，而不是继续内嵌硬编码映射函数。
- `chapter-structure-fields-design.md` 的主要问题不只是未勾选 completion marks，而是正文仍把 state schema / review / precheck 接线写成“建议添加”，而这些入口当前已经存在。
- 当前更可靠的证据组合是：`state-v5-template.json` + `state-schema-v5.json` + `state-schema.md` + `novel-outline/review/precheck` consumer 说明 + 结构审计脚本与测试。
- `v1.5-registry-consumer-and-scan-boundary-review-2026-03-31.md` 的剩余问题不是结论错，而是风险章节里的代表项已经落后于后续文档治理结果。
- 这类复检文档更适合在不改结论的前提下，及时把“代表问题”更新成当前仍成立的泛化风险，而不是继续引用已经闭环的旧案例。
- `governance-maintenance-drill-2026-03-31.md` 的剩余问题也不是结论错，而是“保留项”里继续挂着已经被后续动作闭环的 weekly snapshot 案例。
- 这类 drill 文档更适合保留原始执行过程，但把当前保留项收缩为真正仍需长期盯住的治理纪律。
- 经过本轮收尾复检后，`docs/00-当前有效/` 中剩余仍带阶段语义的文档，大多已经属于计划 / 模板 / 候选排序 / 长期复检类文档，当前不是误写的现状缺口。
- 这意味着“当前有效文档去历史化整理”这条线已经达到收口条件；继续批量清理的收益会明显下降。
- `shared/profiles/README.md` 之前残留的主要问题是：把顶层目录数、标准 profile 数，以及 platform / bucket overlay 覆盖写成了旧阶段状态。
- 当前更准确的口径是：53 个顶层目录，其中 52 个标准 profile、1 个 `crossover/` 特殊容器目录；标准 profile 已完成 52/52 的 `profile-tomato.yaml` 与 `bucket-*.yaml` 覆盖。
- `profile-expansion-first-batch-v1.5.md` 之前残留的主要问题是：把“第一批是谁”与“当前全仓覆盖到哪一步”混在了一起，导致文档继续暗示平台差异拆分还只停留在少数对象上。
- 当前更准确的口径是：第一批仍然是历史首批落地对象，但标准 profile 的平台层与 bucket 层覆盖已经明显前推，不应继续用旧首批状态描述现状。
- `profile-expansion-candidate-priority-v1.5.md` 之前残留的主要问题是：继续把“补 platform_positioning / overlay / profile 收口”当成下一批扩面的首要目标。
- 当前更准确的口径是：标准 profile 的基础覆盖已经补齐，下一批扩面的主要价值在 consumer/readiness 收口、题材质量校准，以及组合/派生题材的后续推进。

## Immediate Follow-up

- 后续新任务优先把当前状态写进 `.ops/`
- 等 legacy root ops 文件的历史正文进一步拆分后，再决定是否做物理迁移或瘦身
- 下一条 active task 默认应转向新的具体治理/维护任务，而不是继续扩写这条结构线。
- 如后续再回到 legacy ops 整理，优先考虑历史正文拆分或附录化，而不是再次改动结构边界。
- 如后续新增新的架构 open item，可直接在 `docs/10-进行中/architecture-open-issues.md` 原路径下重开跟踪，无需重新发明入口。
- 如后续继续做治理文档瘦身，下一类候选更适合落在旧治理报告或 inventory/盘点类文档，而不是再回头处理这组 weekly/biweekly/monthly 文档。
- 如后续继续做当前有效文档去历史化整理，下一类候选更适合落在其他 inventory / 设计稿类文档中把“运行时真值”与“历史设计草稿”继续分开。
- 如后续继续沿这条线推进，更自然的候选会是其他仍带未勾选完成标记、但已被 schema / tests / consumer 吃进去的设计说明文档。
- 如后续继续清理 review / drill 类文档，优先检查“代表项是否已被后续治理闭环”，避免让旧案例继续挂在风险章节里。
- 这条线结案后，下一步更适合转向新的治理 / 维护主线，而不是继续在当前有效文档中做广撒网式语义清理。
- 如后续继续维护 profile 体系文档，优先关注 `crossover/` 特殊 schema 路径与标准 profile contract 之间的边界说明是否仍准确。
- 如后续继续推进 profile 扩面文档，优先区分“历史首批落地说明”和“当前仓库覆盖现状”，避免两者再被混写。
- 如后续真正进入 profile 扩面执行，优先按“consumer/readiness 收口 -> 资产落地”的顺序，而不是重新回头补基础覆盖。
