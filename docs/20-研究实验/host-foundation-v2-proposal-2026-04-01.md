# `v1.6+` 跨宿主基础层优化方案（深度提案）

> Status: `research`
>
> 本文不是当前真值，而是基于已完成的 `v1.6` 宿主基础层，对“下一版更优设计”做出的结构化提案。

## 一句话结论

当前 `v1.6` 已经是一个**可交付、可验证、可接手**的版本，但还不是长期最优版本。

更优方案不是继续在 `host-capability-matrix-v1.json` 上叠字段，而是把宿主适配升级为：

- **承诺层**
- **证据层**
- **能力面适配层**

并且把 `Trae` 从“整宿主 unsupported / partial”这种粗粒度表达，改造成“按能力面逐项判定”的模型。

---

## 1. 为什么 `v1.6` 还不够优

`v1.6` 当前的优点已经很明确：

- 有单一宿主真值：`host-capability-matrix-v1.json`
- 有消费层：`install-skills.sh`、projection、doctor
- 有当前有效文档：`skill-usage.md`、`host-support-status-v1.6.md`
- 有定向测试和最小验证链

但它仍有四个结构性不足：

### 1.1 承诺和证据混在一起

当前 `host-capability-matrix-v1.json` 同时承担：

- 项目承诺
- 证据引用
- 运行时观察
- 退化策略

这让它在“当前对外怎么表述”和“为什么能这么表述”之间没有明确层次。

后果是：

- 证据更新会推动主真值频繁改动
- runtime observation 更容易污染长期 contract
- `verified / partial / assumed` 的升级路径不够清晰

### 1.2 宿主级字段过于粗粒度

当前字段是：

- `install_mode`
- `supports_mcp`
- `supports_rules_context`
- `supports_native_invocation`

这对 `Codex / Claude` 勉强够用，但对 `Trae` 不够表达力。

以 Trae 为例，官方文档已经显示它至少公开了：

- `Project Rules`
- `User Rules`
- `Global skills`
- `Project skills`
- `MCP servers`
- `MCP in agents`
- `Auto-run MCP`
- `Auto-run commands`
- `Sandbox`

如果仍用单个 `install_mode = unsupported` 或单个 `supports_mcp = assumed` 表达，就会把“部分面已明确支持、但 skill 安装路径未知”的情况压扁掉。

### 1.3 适配逻辑仍以“宿主分支”思考

当前设计更像：

- 对 `codex` 怎么做
- 对 `claude` 怎么做
- 对 `trae` 怎么做

更优的设计应该是：

- `project_rules` 这个能力面，各宿主怎么支持
- `global_skills` 这个能力面，各宿主怎么支持
- `mcp_registration` 这个能力面，各宿主怎么支持
- `agent_tool_binding` 这个能力面，各宿主怎么支持
- `auto_run_commands` 这个能力面，各宿主怎么支持

也就是说，适配单位应该逐步从“宿主”转到“能力面”。

### 1.4 Trae 的问题不是“要不要支持”，而是“支持面到底有哪些”

当前 `v1.6` 对 Trae 的保守处理是合理的，但不够精确。

真正的缺口不是：

- “Trae 完全不支持”

而是：

- Trae 的哪些能力面已有官方文档
- 哪些能力面需要本地手工验证
- 哪些能力面不适合通过 repo-owned 脚本接管

这说明 Trae 下一步不该直接进入“安装适配实现”，而应该先进入“官方文档 + 最小手工验证”的研究 lane。

---

## 2. 更优方案：三层模型

### 2.1 承诺层

承诺层回答：

> 项目当前**对外承诺**到什么程度？

建议新增：

- `shared/templates/host-support-policy-v2.json`
- `shared/templates/host-support-policy-v2.schema.json`

它只保留：

- `host_id`
- `status`
- `verification_level`
- `surfaces`
- `degrade_policy`
- `notes`

不直接内嵌大量证据正文。

### 2.2 证据层

证据层回答：

> 我们为什么能做出这些承诺？

建议新增：

- `shared/templates/host-evidence-ledger-v1.json`
- `shared/templates/host-evidence-ledger-v1.schema.json`

证据项建议支持：

- `official_doc`
- `repo_file`
- `runtime_observation`
- `manual_verification`
- `doctor_result`

每条证据至少记录：

- `id`
- `host_id`
- `surface`
- `kind`
- `ref`
- `summary`
- `verified_at`
- `confidence`

这样未来升级状态时，只需要追加 ledger，不必频繁重写主承诺文件。

### 2.3 能力面适配层

能力面适配层回答：

> 每个宿主在每个能力面到底怎么接？

建议把“宿主适配”拆为这些最小能力面：

- `project_rules`
- `user_or_global_rules`
- `project_skills`
- `global_skills`
- `skill_install_materialization`
- `skill_invocation`
- `mcp_registration`
- `mcp_agent_binding`
- `auto_run_mcp`
- `auto_run_commands`
- `sandbox`

每个能力面都用统一结构描述：

- `state`
- `mode`
- `evidence_refs`
- `fallback`
- `owner_adapter`

其中：

- `state`：`verified / doc_verified / partial / assumed / unsupported`
- `mode`：
  - `path_symlink`
  - `path_copy`
  - `project_dir`
  - `ui_json`
  - `ui_select`
  - `agent_bind`
  - `not_applicable`

---

## 3. 对当前 `v1.6` 最关键的设计调整

### 3.1 保留 `v1`，不要原地硬改

不建议直接把 `host-capability-matrix-v1.json` 原地升级成复杂结构。

更优做法是：

1. 保留 `v1` 作为当前稳定 contract
2. 在研究阶段并行引入 `policy-v2 + evidence-ledger-v1`
3. 先让 projection / doctor 同时支持两层
4. 等 `v2` 成熟后，再决定是否把 `v1` 退为兼容投影

这样能避免：

- 当前 `v1.6` consumer 全部一起改
- 安装脚本和文档被研究态结构拖着走

### 3.2 用 projection 保持兼容

更优的迁移方式不是让所有 consumer 直接吃 `v2`，而是：

```text
host-support-policy-v2
  + host-evidence-ledger-v1
    -> compatibility projection
      -> host-capability-matrix-v1 (compat)
      -> host-support-status doc
      -> doctor summary
```

这样：

- 老 consumer 继续吃 `v1`
- 新 doctor 和 support doc 可以先吃 `v2`
- 迁移成本可控

### 3.3 `install_mode` 应降级为“某一个能力面”的字段

当前 `install_mode` 是宿主级字段，这在长期上不够优。

更优做法是把它收窄成：

- `skill_install_materialization.mode`

因为：

- `Trae` 可能不支持我们这种全局 symlink 安装
- 但它可能仍支持 `project_skills`
- 也可能支持 `global_skills`，只是路径和导入机制不同

所以未来不应再用一个宿主级 `install_mode` 决定整宿主的安装能力。

---

## 4. Trae 的更优研究策略

### 4.1 当前已知的官方公开面

基于 **2026-04-01** 的官方文档，可以确认 Trae 已公开这些页面：

- `Rules`
- `Skills`
- `Model Context Protocol`
- `Add MCP servers`
- `Use MCP servers in agents`
- `Auto-run & security`
- `Sandbox`

从这些文档能确认的最低事实有：

### 已可判为 `doc_verified` 的面

- `project_rules`
  - 官方明确提到 `Project Rules`
  - 并指出规则文件位于 `.trae/rules`
- `user_or_global_rules`
  - 官方明确提到 `User Rules`
- `mcp_registration`
  - 官方明确支持通过 marketplace 和手动 JSON 添加 MCP server
- `mcp_agent_binding`
  - 官方明确支持把 MCP server 绑定到内置 agent 和 custom agents
- `auto_run_mcp`
  - 官方明确有 `Automatically Run MCP`
- `auto_run_commands`
  - 官方明确有 `Automatically Run Commands`，并支持 allowlist / denylist
- `sandbox`
  - 官方有单独 `Sandbox` 文档

### 仍不能判为 `verified` 的面

- `project_skills`
- `global_skills`
- `skill_install_materialization`
- `skill_invocation`

原因不是“官方没提到 skills”，而是：

- 还没确认本地技能目录和发现机制
- 还没确认是否支持 repo-owned symlink/copy 安装
- 还没确认调用方式是目录扫描、导入、还是 UI/Marketplace 流程

### 当前不该轻易承诺的面

- `hooks`

更优做法是把它从“假设 Trae 有没有 hooks”改成：

- 先看 `auto_run + security + sandbox` 是否已经足够承担我们当前想表达的“hooks-like automation”职责

换句话说，不要强行把 Trae 映射成 Codex/Claude 语义里的 hooks。

### 4.2 Trae 研究 lane 的最小任务集

建议单开一条小研究 lane，只回答 5 个问题：

1. `Global skills` 的本地落盘路径是什么？
2. `Project skills` 的发现方式是什么？
3. Trae 是否支持 repo-owned 目录直接落盘后自动发现？
4. MCP 配置是否支持 project-owned file source，还是纯 UI 配置？
5. `Auto-run + sandbox` 是否足够覆盖我们当前想表达的 hooks-like automation？

### 验收标准

只有回答完这 5 个问题，Trae 才应从当前状态继续推进。

否则最优策略仍是：

- `rules/context = partial 或 doc_verified`
- `skills = doc_verified / runtime_unknown`
- `mcp = doc_verified`
- `skill_install_materialization = unsupported 或 unknown`

而不是一口气把 Trae 写成“已支持”。

---

## 5. 建议实施顺序

### Phase A：研究与分层准备

- 新增 `host-evidence-ledger-v1`
- 给 `host` 证据类型加上 `official_doc`
- 起草 `host-support-policy-v2`
- 新建 Trae capability review 文档

### Phase B：兼容投影层

- 从 `policy-v2 + evidence-ledger-v1` 投影出：
  - `host-capability-matrix-v1` 兼容视图
  - `host-support-status` 文档
  - `doctor` 摘要输出

### Phase C：Trae 聚焦验证

- 用官方文档 + 最小手工验证把 Trae 的能力面逐项判级
- 只在拿到明确证据后升级：
  - `doc_verified -> partial`
  - `partial -> verified`

### Phase D：是否推进到 `v1.7`

只有当下面条件满足时，才值得把这条线升成下一轮正式 roadmap：

- `policy-v2` 稳定
- `evidence-ledger-v1` 稳定
- Trae 至少 3 个关键能力面拿到明确 doc 或 runtime 证据
- 兼容 projection 不导致现有 `v1.6` consumer 漂移

---

## 6. 非目标

这份方案明确不建议：

- 继续往 `v1.6` 的 `host-capability-matrix-v1.json` 硬塞更多字段
- 直接把 Trae 的 `install_mode` 改成已支持
- 为每个宿主单独发明一套新的配置脚本
- 在没有证据的前提下把 Trae、OpenCode、OpenCLAW 全部拉齐承诺
- 借机引入 runtime / plugin / daemon 新真值中心

---

## 7. 最终建议

如果只选一个最优动作，我建议是：

- **先做 `host-evidence-ledger-v1 + Trae capability review`，不要先改安装脚本。**

因为当前 `v1.6` 缺的已经不是“能不能安装”，而是：

- 我们究竟应该承诺什么
- 哪些承诺有官方文档支撑
- 哪些承诺只有本地 runtime 观察
- 哪些能力面本来就不该按 `install_mode` 这种单字段来表达

一句话说：

- `v1.6` 已经够用；下一版更优方案的核心，不是“再多支持一个宿主”，而是把**宿主承诺、证据、能力面**三者彻底解耦。
