# 新一轮具体治理/维护任务 2026-03-31

> 已从 `docs/00-当前有效/` 迁入 `docs/90-归档/阶段/`。本文件保留为本轮 active ops 真源治理的具体执行记录，默认不再作为当前有效规则入口。

> 任务类型：结构收敛后的 active ops 真源治理
>
> 目标：顺着当前仓库已经确立的 `.ops/` 作为 canonical active ops home 的规则，完成一轮低风险、可验证的具体治理动作：把根目录 legacy ops 文件与 `.ops/` 的分工关系再收紧一步，让接手者更少误判“哪里才是当前活动真源”。

---

## 一、任务选择依据

**思考强度：L3**

本轮没有再重复做 registry / sample / governance 模板演练，而是选择了一个新的、真实且低风险的治理任务：

> **active ops 真源治理：收紧根目录 legacy ops 文件与 `.ops/` 当前真源的边界。**

选择原因：

1. `progress.md` 顶部已经明确写明：`.ops/` 是当前 canonical active ops home
2. `findings.md`、`task_plan.md` 也都已补相同的结构收敛说明
3. `.ops/README.md`、`.ops/active-plan.md`、`.ops/progress.md`、`.ops/findings.md` 已经形成当前 active state 的真实承载层
4. 但根目录 legacy ops 文件顶部摘要仍保留了较多“当前主任务 / 当前下一步”语义，容易让后续接手者继续把根目录当成 active 真源

因此，这一轮最合适的具体治理动作不是大规模迁移，而是：

- **让根目录 legacy ops 文件更明确地退回“历史导航 / 兼容入口”角色**
- **让 `.ops/` 更明确地承担当前 active state 真源角色**

---

## 二、本轮实际检查范围

**思考强度：L2**

本轮读取并对比了：

- [progress.md](file:///Users/arm/Desktop/vscode/Genm-codex/progress.md)
- [findings.md](file:///Users/arm/Desktop/vscode/Genm-codex/findings.md)
- [task_plan.md](file:///Users/arm/Desktop/vscode/Genm-codex/task_plan.md)
- [.ops/README.md](file:///Users/arm/Desktop/vscode/Genm-codex/.ops/README.md)
- [.ops/active-plan.md](file:///Users/arm/Desktop/vscode/Genm-codex/.ops/active-plan.md)
- [.ops/progress.md](file:///Users/arm/Desktop/vscode/Genm-codex/.ops/progress.md)
- [.ops/findings.md](file:///Users/arm/Desktop/vscode/Genm-codex/.ops/findings.md)
- 以及 README / AGENTS 中对 `.ops/` 的说明入口

---

## 三、检查结果

**思考强度：L3 + L4**

### 3.1 当前已稳定的事实

1. `.ops/` 已经成为当前 active ops 的默认落点
2. `.ops/README.md` 对 active-plan / progress / findings / decisions 的职责说明清楚
3. README 与 AGENTS 已将 `.ops/` 暴露为当前任务接手的优先入口
4. 根目录 `progress.md` / `findings.md` / `task_plan.md` 已补充“结构收敛说明”，明确它们是 legacy 入口

### 3.2 当前仍存在的轻微认知风险

根目录 legacy ops 文件虽然已经声明“新的 active state 默认写入 `.ops/`”，但它们的顶部摘要仍然保留了大量类似：

- `当前推进中的主线`
- `当前主任务`
- `当前下一步`
- `当前新增判断`

这类标题会让接手者在视觉上仍把根目录文件误读为“当前 active 真源”。

### 3.3 风险定性

- 风险等级：**低**
- 性质：**文档认知治理问题，不是结构缺口**
- 处理原则：**优先补一份明确的治理记录，不直接大改根目录 legacy 文件的大段摘要结构**

这样可以避免一次性重写大量历史导航内容，同时把“下一轮若继续治理，应该改什么”说清楚。

---

## 四、本轮治理动作

**思考强度：L3**

本轮已完成：

1. 明确将“active ops 真源治理”定义为一轮独立的具体治理任务
2. 固化本轮检查范围、已知现状、风险点与处理原则
3. 将当前结论写成正式文档，作为下一步是否继续精修根目录 legacy ops 摘要结构的依据

本轮**未直接重写**根目录 `progress.md` / `findings.md` / `task_plan.md` 的顶部摘要，原因是：

- 它们当前已经承担“历史导航与兼容入口”角色
- 大改标题和摘要结构虽然可做，但会影响历史连续性与现有导航习惯
- 更适合先通过正式治理记录把边界说清，再决定是否做第二轮瘦身

---

## 五、后续建议动作

**思考强度：L4**

如果继续推进这一条治理线，建议按以下顺序：

1. 先对根目录 `progress.md` / `task_plan.md` / `findings.md` 的顶部摘要做一次**命名层面瘦身**，把：
   - “当前主任务 / 当前下一步 / 当前推进中的主线”
   逐步改成更明确的：
   - “legacy 导航摘要 / 历史接手摘要 / 历史连续性提示”

2. 在 `.ops/README.md` 中补一个更明确的“接手顺序”，例如：
   - 先读 `.ops/active-plan.md`
   - 再读 `.ops/progress.md`
   - 再按需回读根目录 legacy 文件

3. 如后续确认历史导航已经足够稳定，再考虑是否把根目录 legacy ops 文件顶部摘要继续瘦身一轮

---

## 六、本轮结论

**思考强度：L3**

本轮已成功开启一轮新的、真实的具体治理任务：**active ops 真源治理**。

结论是：

- 当前 `.ops/` 作为 canonical active ops home 的结构已经成立
- 当前主要剩余问题不在结构实现，而在根目录 legacy ops 文件顶部摘要的认知语义仍略偏“当前 active”
- 这属于低风险、可分阶段推进的文档治理任务
- 本轮已完成问题定性与正式记录，为下一步更细的摘要瘦身提供依据
