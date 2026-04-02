# Trae Capability Review (`2026-04-02`)

> Status: `research`
>
> 目的：基于官方文档与当前仓库现状，重新审视 Trae 的宿主能力边界，避免继续把它粗暴写成“只有 rules/context”或在证据不足时过早承诺安装支持。

## 结论

截至 **2026-04-02**，Trae 已经不是“完全空白宿主”，而且我们已经补到了本机最小手工验证；但它仍然远远不到“已支持 repo-owned 安装闭环”的程度。

当前最稳的结论是：

- `project_rules`：`doc_verified`
- `user_or_global_rules`：`doc_verified`
- `project_skills`：`doc_verified`
- `global_skills`：`doc_verified`
- `global_skill_path`：`manual_verified`
- `project_skill_discovery_path`：`manual_verified`
- `mcp_registration`：`doc_verified`
- `mcp_agent_binding`：`doc_verified`
- `mcp_project_file_source`：`manual_verified`
- `auto_run_mcp`：`doc_verified`
- `auto_run_commands`：`doc_verified`
- `sandbox`：`doc_verified`
- `sandboxed_command_execution`：`manual_verified`
- `skill_install_materialization`：`unknown`
- `skill_invocation`：`unknown`
- `repo_owned_installability`：`researching`
- `hooks-like automation`：`researching`

因此，当前最优结论已经不再是“继续等手工验证”，而是：

- 先把新增事实收进 `v1.6.1` 级增强
- 暂不进入有界 `v2`
- 继续把 Trae 保持在 `install_mode = unsupported`

---

## 证据来源

官方文档：

- Rules: <https://docs.trae.ai/ide/rules?_lang=en>
- Skills: <https://docs.trae.ai/ide/skills?_lang=en>
- Model Context Protocol: <https://docs.trae.ai/ide/model-context-protocol?_lang=en>
- Add MCP servers: <https://docs.trae.ai/ide/add-mcp-servers?_lang=en>
- Use MCP servers in agents: <https://docs.trae.ai/ide/use-mcp-servers-in-agents?_lang=en>
- Auto-run & security: <https://docs.trae.ai/ide/auto-run-and-security?_lang=en>
- Sandbox: <https://docs.trae.ai/ide/sandbox?_lang=en>

仓库内现状：

- [.trae/rules/project-context.md](/Users/arm/Desktop/vscode/Genm-codex/.trae/rules/project-context.md)
- [.trae/rules/rule.md](/Users/arm/Desktop/vscode/Genm-codex/.trae/rules/rule.md)
- [host-capability-matrix-v1.json](/Users/arm/Desktop/vscode/Genm-codex/shared/templates/host-capability-matrix-v1.json)

---

## 能力面判断

### 1. Rules

官方 Rules 文档明确区分：

- `User Rules`
- `Project Rules`

并明确指出：

- `Project Rules` 位于项目的 `.trae/rules` 目录
- 使用 Markdown
- 仅在当前项目内生效

判断：

- `project_rules = doc_verified`
- `user_or_global_rules = doc_verified`

### 2. Skills

官方 Skills 文档明确区分：

- `Global skills`
- `Project skills`

还展示了 skill 目录结构：

```text
skill-name/
├── SKILL.md
├── examples/
└── templates/
```

这已经足够证明：

- Trae 公开了 skill 体系
- 它支持 project/global 双层 skill 概念
- `SKILL.md` 仍是核心技能入口

但当前仍不知道：

- 全局 skill 的本地路径
- 项目 skill 的发现机制
- 是否支持我们这种 repo-owned symlink / copy 物化

判断：

- `project_skills = doc_verified`
- `global_skills = doc_verified`
- `skill_install_materialization = unknown`
- `skill_invocation = unknown`

### 3. MCP

官方文档已经覆盖：

- MCP 概览
- 添加 MCP server
- 在 agents 中使用 MCP server

`Add MCP servers` 文档说明：

- 可从 Marketplace 添加
- 也可手动添加
- 支持 JSON 配置
- 文中明确提到 `stdio` MCP 和 `HTTP` MCP

`Use MCP servers in agents` 文档说明：

- 内置 `Builder with MCP` 会自动使用已配置 MCP
- custom agents 可在 `Tools - MCP` 中选择 MCP server 及其 tools

判断：

- `mcp_registration = doc_verified`
- `mcp_agent_binding = doc_verified`

### 4. Auto-run / Security

官方 `Auto-run & security` 文档明确提到：

- `Automatically Run MCP`
- `Automatically Run Commands`
- 命令执行支持 `allowlist / denylist`

这说明 Trae 已经公开了：

- agent 自动执行 MCP 的能力
- agent 自动执行命令的能力
- 对自动命令执行的风险控制入口

判断：

- `auto_run_mcp = doc_verified`
- `auto_run_commands = doc_verified`

### 5. Sandbox

官方 `Sandbox` 页面已经公开。

当前从页面标题和页面元信息中至少能确认它覆盖的主题包括：

- file access
- network access
- execute high-risk commands

这足以证明：

- Trae 已经把 sandbox 作为独立能力面公开

但在没有进一步手工使用验证前，仍不应把它直接映射成我们语义里的完整 command hook 或 execution policy system。

判断：

- `sandbox = doc_verified`

### 6. Hooks

当前官方文档没有让我拿到一个和 Codex/Claude “hooks” 完全对等的公开面。

但它已经有：

- auto-run MCP
- auto-run commands
- sandbox / allowlist / denylist

因此更合适的处理方式不是继续问“Trae 有没有 hooks”，而是改成：

- 这些能力是否足以承担我们当前想表达的 `hooks-like automation`

判断：

- `hooks-like automation = researching`

### 7. 最小手工验证结果

这次手工验证没有再停在文档层，而是直接读取了本机 Trae / Trae CN 的 runtime 日志、sandbox 配置与本地目录。

#### 7.1 `Global skills` 的本地路径

本机上已经拿到宿主变体级的实际路径：

- `Trae CN`：`~/.trae-cn/skills`
- `Trae`：`~/.trae/skills`

证据：

- `~/.trae-cn/skills/` 目录实际存在，且包含本地 `SKILL.md`
- `Trae CN` 日志明确打印 `global skills path=/Users/arm/.trae-cn/skills`
- `Trae` 日志明确打印 `global skills path=/Users/arm/.trae/skills`

判断：

- “全局 skill 路径未知”这一项已经可以关闭
- 但它是宿主变体相关事实，不等于 repo-managed install 已闭环

#### 7.2 `Project skills` 的发现方式

当前仓库已经拿到明确的 runtime path scan 证据：

- Trae CN 会扫描当前工作区的 `<repo>/.trae/skills`
- 在本仓库里，它实际扫描的是 `/Users/arm/Desktop/vscode/Genm-codex/.trae/skills`
- 当目录不存在时，会写出 `Skills directory does not exist`

判断：

- `project skills` 不是纯 UI-only 抽象
- 至少“repo-owned 目录发现路径存在”这件事已经被手工验证

#### 7.3 repo-owned 安装/落盘是否就能直接工作

这项仍然**不能**直接下结论为已支持。

因为同一批日志还显示：

- `[SkillTool] using remote definition`

这说明：

- 本地 path scan 已存在
- 但实际 skill invocation 仍可能走 remote definition
- “把一个本地 skill 丢进 `.trae/skills/` 就一定能被启用并调用”这件事，当前还没有闭环证据

判断：

- `repo_owned_installability = researching`
- `skill_invocation = unknown`

#### 7.4 MCP 是否支持 project-owned file source

这项现在已经从文档级进入 runtime 级。

本机 Trae CN 的两类证据同时出现：

- 动态配置日志把 `$WORKSPACE_FOLDER/.trae/mcp.json` 加进 `sandbox_ro_list`
- 当前仓库对应的 sandbox 配置文件实际包含 `/Users/arm/Desktop/vscode/Genm-codex/.trae/mcp.json`

判断：

- `project-owned .trae/mcp.json` 已经进入实际运行路径
- 因此“Trae 的 MCP 只能靠 UI 手填、不能吃 file source”这个假设不成立

#### 7.5 `Auto-run + sandbox` 是否足以承担 hooks-like automation

这次手工验证已经能证明两件事：

- Trae 的命令执行确实能跑在 `execEnv=sandbox`
- 实际命令会经 `trae-sandbox` 执行

但当前采样到的日志里，`run_script_show` 事件仍然是：

- `is_auto_run = 0`

这意味着我们现在能确认的是：

- sandboxed command execution 是 runtime fact
- full hooks-like automation 仍未闭环

判断：

- `sandboxed_command_execution = manual_verified`
- `hooks-like automation = researching`

---

## 当前仍未解决的问题

以下问题现在仍然决定 Trae 是否能进入更高承诺级别：

1. repo-owned local skill 在 `.trae/skills/` 落盘后，是否能被直接启用并调用？
2. local path scan 与 `using remote definition` 的优先级关系到底是什么？
3. `Auto-run + sandbox` 是否足以承担我们需要的 hooks-like automation？

---

## 对当前 repo 的意义

这份审计意味着：

- 当前把 Trae 写成“只有 rules/context”已经明显偏保守
- 但直接把 Trae 升成 installable host 仍然过早
- 当前新增事实主要是在提升证据等级，而不是逼出新的主真值结构

更稳的下一步是：

1. 把这些结论写进证据层与 `v1.6` 投影
2. 把 Trae 的宿主判断继续保持在“unsupported install + partial capability boundary”
3. 不为了已经拿到的新事实提前发起 `v2`

---

## Gate 1 判断

### 结论

`Gate 1` 的结论是：

- **停在 `v1.6.1` 级增强**
- **不正式进入有界 `v2`**

### 为什么现在不进 `v2`

因为当前拿到的新增事实，仍然可以被现有结构清楚承载：

- `install_mode = unsupported` 仍然成立
- `supports_* + degrade_policy + notes` 仍然能表达当前承诺边界
- 更细的差异已经可以放进 `host-evidence-ledger-v1`

换句话说，当前真正被解决的是：

- Trae 不再只是“只有 rules/context”
- Trae 的 `project/global skills`、`project-owned MCP file source`、`sandboxed command execution` 已经有了更高证据等级

而当前**还没有**出现的，是下面这些会逼出 `v2` 的条件：

- 出现一个必须按 capability-level 承诺、而 `v1` 完全表达不下的宿主状态
- 证据层与承诺层之间已经形成真实维护负担
- 新 consumer 已经无法继续直接吃 `v1`

### 当前更准确的行动

因此，这轮更准确的行动不是“升级 schema”，而是：

1. 把 Trae 的 `rules_context / skill_discovery / mcp` 边界在 `v1.6.1` 中收紧
2. 继续保持 `install_mode = unsupported`
3. 把剩余未知数收缩为：
   - local skill invocation
   - repo-owned installability
   - hooks-like automation

---

## 建议动作

1. 将本审计中的手工验证条目写入 `host-evidence-ledger-v1`
2. 在 `host-capability-matrix-v1` 与 `host-support-status-v1.6` 中反映更准确的 Trae 边界
3. 继续保持：
   - `install_mode = unsupported`
   - `Gate 1 = stay on v1.6.1`
4. 只有当后续真的证明：
   - 需要 capability-level 承诺
   - 或 `v1` 已经表达不下
   才重新打开有界 `v2`
