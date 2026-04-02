# Active Ops

`.ops/` 是当前任务运行态的默认落点。

这里存放：

- `active-plan.md`：当前执行计划
- `progress.md`：当前阶段进度
- `findings.md`：当前阶段结论与阻塞
- `decisions.md`：结构与流程决策
- `archive/`：关闭后的计划与记录

约束：

- 新任务默认把 active state 写到这里，不再把新的 `task_plan.md`、`progress.md`、`findings.md` 直接放到仓库根目录。
- 根目录现有 `task_plan.md`、`progress.md`、`findings.md` 先保留，作为 legacy 入口与历史连续性承载层。
- 推荐接手顺序：先读 `active-plan.md`，再读 `progress.md`，再读 `findings.md`；只有在追历史链路或旧链接时才回读根目录 legacy ops 文件。
- 当结论变成长期稳定规则时，把它提升到 `docs/00-当前有效/` 或其他 durable docs，而不是一直停留在 `.ops/`。
