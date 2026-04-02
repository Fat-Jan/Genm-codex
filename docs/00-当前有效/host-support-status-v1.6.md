# Host Support Status (`v1.6`)

> Status: `active-reminder`
>
> 本文记录当前 `v1.6` 的宿主支持状态。真值以 `host-capability-matrix-v1.json` 为准，本文只承载可读投影与边界说明。

## 作用

这份文档回答四个问题：

- 当前哪些宿主进入范围
- 每个宿主当前是 `baseline / legacy / experimental` 中的哪一类
- 验证等级到什么程度
- 缺失能力时应该如何退化，而不是误写成“已经完整支持”

## 当前支持表

<!-- host-support-summary:start -->
| 平台 | 状态 | 验证等级 | 安装支持 |
|------|------|----------|----------|
| Claude Code | baseline | partial | symlink |
| Codex | legacy | verified | symlink |
| OpenCode | experimental | partial | symlink |
| OpenCLAW | experimental | partial | symlink |
| Trae | experimental | partial | unsupported |
<!-- host-support-summary:end -->

## 当前宿主明细

<!-- host-support-details:start -->
### Claude Code
- 状态：`baseline`
- 验证等级：`partial`
- 安装支持：`symlink` -> `~/.claude/skills`
- 安装命令：`bash scripts/install-skills.sh claude`
- 能力边界：
  - `skill_discovery`: `partial`
  - `alias`: `partial`
  - `rules_context`: `verified`
  - `hooks`: `verified`
  - `mcp`: `verified`
  - `native_invocation`: `partial`
- 退化策略：若本地 skill 安装或 alias 未物化，仍以 Claude 的 rules、hooks、MCP 与 repo-owned docs 维持 baseline，不因统一抽象反向损伤现有 Claude 工作流。
- 备注：仓库已声明 Claude 安装面，当前会话可直接观察到 Claude rules、hooks、MCP 能力，但仓库内尚无独立 doctor 证明完整本地 skill discovery 与调用闭环。
- 证据：
  - `repo_file` `scripts/install-skills.sh`: 安装脚本声明 claude 目标为 ~/.claude/skills。
  - `repo_file` `docs/00-当前有效/skill-usage.md`: 用户文档列出 Claude Code 安装命令与路径。
  - `runtime_observation` `claude-code-session:2026-04-01`: 当前会话直接证明 Claude Code 存在 rules、hooks 与 MCP 工具面。

### Codex
- 状态：`legacy`
- 验证等级：`verified`
- 安装支持：`symlink` -> `~/.codex/skills`
- 安装命令：`bash scripts/install-skills.sh`
- 能力边界：
  - `skill_discovery`: `verified`
  - `alias`: `verified`
  - `rules_context`: `assumed`
  - `hooks`: `assumed`
  - `mcp`: `assumed`
  - `native_invocation`: `verified`
- 退化策略：必须保持 legacy-compatible：即使 rules、hooks、MCP 仍未统一，也不能让现有 skill、alias 与调用入口断裂。
- 备注：Codex 是当前证据最完整的安装与调用兼容面：安装根、symlink 模式、alias 派生链和 fresh session discovery 都有仓库内证据。
- 证据：
  - `repo_file` `scripts/install-skills.sh`: 安装脚本默认目标是 ~/.codex/skills，并以 symlink 模式物化安装项。
  - `repo_file` `docs/90-归档/迁移与RC/codex-migration-plan.md`: 迁移计划记录 genm-novel-* 安装、fresh Codex session 发现/触发验证与 phase-1 E2E 闭环。
  - `repo_file` `docs/00-当前有效/skill-usage.md`: 用户文档保留 Codex 默认安装与 frontmatter name 调用说明。

### OpenCode
- 状态：`experimental`
- 验证等级：`partial`
- 安装支持：`symlink` -> `~/.config/opencode/skills`
- 安装命令：`bash scripts/install-skills.sh opencode`
- 能力边界：
  - `skill_discovery`: `partial`
  - `alias`: `partial`
  - `rules_context`: `assumed`
  - `hooks`: `assumed`
  - `mcp`: `assumed`
  - `native_invocation`: `assumed`
- 退化策略：当前只承认安装投影面；在 discovery、invocation、context 与 MCP 未核验前，不把它写成完整宿主承诺。
- 备注：仓库当前仅对 OpenCode 给出安装路径与用户文档投影，没有更多本地已验证闭环证据。
- 证据：
  - `repo_file` `scripts/install-skills.sh`: 安装脚本声明 opencode 目标为 ~/.config/opencode/skills。
  - `repo_file` `docs/00-当前有效/skill-usage.md`: 用户文档列出 OpenCode 安装命令与路径。

### OpenCLAW
- 状态：`experimental`
- 验证等级：`partial`
- 安装支持：`symlink` -> `~/.openclaw/skills`
- 安装命令：`bash scripts/install-skills.sh openclaw`
- 能力边界：
  - `skill_discovery`: `partial`
  - `alias`: `partial`
  - `rules_context`: `assumed`
  - `hooks`: `assumed`
  - `mcp`: `assumed`
  - `native_invocation`: `assumed`
- 退化策略：与 OpenCode 同级处理：先承认安装投影，不提前承诺完整 skill host 体验。
- 备注：仓库对 OpenCLAW 给出安装路径与文档示例，但尚无 hooks、MCP、native invocation 的闭环验证。
- 证据：
  - `repo_file` `scripts/install-skills.sh`: 安装脚本声明 openclaw 目标为 ~/.openclaw/skills。
  - `repo_file` `docs/00-当前有效/skill-usage.md`: 用户文档列出 OpenCLAW 安装命令与路径。
  - `repo_file` `.trae/rules/project-context.md`: Trae 项目上下文文件把 ~/.openclaw/skills 作为示例路径提及。

### Trae
- 状态：`experimental`
- 验证等级：`partial`
- 安装支持：`unsupported`
- 能力边界：
  - `skill_discovery`: `partial`
  - `alias`: `assumed`
  - `rules_context`: `verified`
  - `hooks`: `assumed`
  - `mcp`: `partial`
  - `native_invocation`: `assumed`
- 退化策略：以 rules/context + project/global skill path discovery + project-owned .trae/mcp.json 作为最小接入面；不承诺 skill 安装、alias、native invocation 或 hooks，缺失能力时退回文件直读与 repo-owned docs。
- 备注：Trae 当前已拿到官方文档 + 本机日志的 project/global skill path、project-owned .trae/mcp.json file source 与 sandbox command 执行证据；但 install-skills.sh 仍未把它列为安装目标，且 SkillTool 日志仍显示 using remote definition，因此暂不承诺 install / invocation / hooks 闭环。
- 证据：
  - `repo_file` `.trae/rules/project-context.md`: Trae 项目上下文文件存在，并定义调用约定与项目入口。
  - `repo_file` `.trae/rules/rule.md`: Trae 规则文件存在，说明已具备最小 rules/context 投影面。
  - `runtime_observation` `trae-cn-log:2026-03-31:skill-path-scan`: Trae CN 日志明确打印 global skills path=/Users/arm/.trae-cn/skills，并在当前仓库扫描 /Users/arm/Desktop/vscode/Genm-codex/.trae/skills。
  - `runtime_observation` `trae-cn-log:2026-03-31:project-mcp-sandbox`: Trae CN sandbox 配置对当前仓库加入 .trae/mcp.json 只读白名单，说明 project-owned MCP file source 已进入实际运行路径。
  - `runtime_observation` `trae-cn-log:2026-03-31:remote-skill-definition`: 同一批日志显示 [SkillTool] using remote definition，说明本地 path scan 已存在，但 invocation 仍不能按 repo-owned 安装闭环承诺。
<!-- host-support-details:end -->

## 当前边界

- `host-capability-matrix-v1.json` 是宿主事实真值
- `host-evidence-ledger-v1.json` 记录 supporting evidence，包括 repo file、runtime observation 与 official doc
- `skill-usage.md` 负责安装表与简化支持表
- 本文负责更完整的宿主支持状态、退化策略与证据说明
- `doctor_host_foundation.py` 负责验证 matrix / install / alias / projection / doc 是否仍一致
