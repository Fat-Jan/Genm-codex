# 架构未决问题台账

## 目的

这份文档记录 `Genm-codex` 当前已经确认、但暂未完全收口的架构问题。

它的用途不是替代当前任务计划，而是作为长期治理台账，回答：

1. 哪些问题已经被正式确认
2. 为什么这次没有一起修完
3. 延后会带来什么风险
4. 什么时候应该重新打开处理

## 使用规则

- 只记录已经确认、值得跨会话持续跟踪的问题
- 每条问题都应带上触发重审条件，不写“以后再看”式空话
- 当前任务内的临时发现优先写进 `findings.md`
- 一旦某条问题被解决，应在本文件中标记 `resolved`，并补对应提交或文档链接
- MCP memory 可以记录“最近关注了哪些问题”，但本文件才是长期真源

## 状态说明

- `open`：已确认，尚未开始
- `planned`：已确认，已有明确处理方向
- `monitoring`：暂不改，但持续观察
- `deferred`：当前有意延后
- `resolved`：已完成收口

## 台账

### AOI-001 `state/schema/template/script` 契约漂移

- Status: `resolved`
- Scope:
  - `shared/references/shared/state-schema.md`
  - `shared/templates/state-v5-template.json`
  - `scripts/split-runtime-guidance.py`
  - `scripts/build_active_context.py`
  - 相关 sidecar consumer
- Problem:
  - `state-schema.md` 自称是单一事实源，但顶部结构示例和当前运行 shape 已不一致
  - `learned_patterns` / `market_adjustments` 在模板中仍偏 inline，而脚本已经 externalize 成 sidecar pointer
  - `build_active_context.py` 对 `items.tracked` / `factions.active` 的消费 shape 与 schema 不一致
- Why not fixed now:
  - 需要统一 canonical contract，并同步调整模板、脚本和测试，不适合在架构审查会话里边看边改
- Risk if deferred:
  - 后续每加一个 sidecar 或状态字段，漂移会继续扩大
  - 同一项目在不同脚本/skill 下看到的 state 解释可能不一致
- Trigger to revisit:
  - 下一次新增 `state` 字段
  - 下一次新增/修改 sidecar mirror 字段
  - 下一次做 `workflow_state` 正式落盘时
- Planned direction:
  - 引入真正机器可校验的 canonical schema
  - 明确定义 externalized 之后的 `state` pointer shape
  - 统一 `items` / `factions` / `launch_stack_*` 的 canonical shape
- Resolution:
  - 已新增机器可校验 schema：
    - `shared/templates/state-schema-v5.json`
    - `shared/templates/learned-patterns.schema.json`
    - `shared/templates/workflow-state-v2.schema.json`
    - `shared/templates/state-archive-v1.json`
  - `shared/templates/state-v5-template.json` 已补齐 `entities.factions`
  - `shared/references/shared/state-schema.md` 已更新到当前 runtime shape，并补 externalized 兼容约定
  - `scripts/build_active_context.py` 已支持 `items` / `factions` 的字符串/对象双形态
  - 已新增 `tests/test_state_contracts.py`
  - 验证：
    - `pytest -q tests/test_state_contracts.py tests/test_active_context.py tests/test_inkos_growth_plan.py tests/test_setting_gate.py`
    - `pytest -q`
    - `bash scripts/validate-migration.sh`

### AOI-002 `shared/` 同步目录与本仓 contract/template 混放

- Status: `resolved`
- Scope:
  - `shared/references/`
  - `shared/templates/`
  - `shared/sync-governance.json`
  - `scripts/sync-shared-from-genm.sh`
- Problem:
  - `shared/` 仍被文档描述为上游同步目录
  - 但仓库里已经存在 repo-owned 的 contract/template，例如：
    - `shared/references/shared/chapter-transaction-schema.md`
    - `shared/templates/workflow-state-v2.json`
  - 历史同步脚本缺少对 local-only 与 same-path drift 的保护
- Why not fixed now:
  - shared mixed-ownership 风险已完成脚本级收口；后续主要是持续维护 allowlist 和文档边界
- Risk if deferred:
  - 如果后续新增 repo-local shared 文件但不进 governance manifest，真实 sync 仍可能误伤
- Trigger to revisit:
  - 下一次修改 `shared/references/*`
  - 下一次修改 `shared/templates/*`
  - 下一次准备从 `Genm` 真正同步 shared
- Planned direction:
  - 继续维护 governance manifest
  - 对新增 repo-local shared 资产同步补 allowlist / 报告护栏
- Resolution:
  - 已新增 `shared/sync-governance.json` 作为 repo-local protected paths manifest
  - `scripts/sync-shared-from-genm.sh` 已进入 governance-aware sync 模式：
    - `--report-json` 输出 `protected_local_paths / local_only_paths / unexpected_local_only_paths / drift_paths / source_only_paths`
    - 默认阻断 `same-path drift overwrite`
    - 真实 sync 后恢复 governance allowlist 中的 protected local paths
  - 已新增 `tests/test_shared_sync_governance.py`
  - 已将 `shared/sync-governance.json` 纳入 `bash scripts/validate-migration.sh`

### AOI-003 `chapter transaction` maintenance 尾段已机械闭环

- Status: `resolved`
- Scope:
  - `shared/references/shared/chapter-transaction-schema.md`
  - `shared/templates/workflow-state-v2.json`
  - `skills/novel-workflow/SKILL.md`
  - `skills/novel-resume/SKILL.md`
  - `scripts/project-maintenance.py`
  - `scripts/post-task-maintenance.py`
- Problem:
  - 事务顺序已经定义清楚：
    - `gate-check -> draft -> close -> maintenance -> snapshot`
  - 维护链之前缺少真实 `.mighty/workflow_state.json` 写回
  - 当前已补 maintenance -> snapshot 的机械状态推进，但 `draft / close / snapshot` 仍未各自拥有独立写回执行点
- Why not fixed now:
  - 当前先把最稳定、最可验证的 maintenance 段收成真实状态写回，剩余 phase owner 仍需后续逐段补齐
- Risk if deferred:
  - `novel-resume` 现在能在 maintenance 之后读到真实 checkpoint，但 maintenance 之前的恢复仍有推断成分
- Trigger to revisit:
  - 下一次增强 `novel-workflow`
  - 下一次增强 `novel-resume`
  - 下一次扩充 `maintenance` phase 行为
- Planned direction:
  - 已由 `project-maintenance.py` / `post-task-maintenance.py` 真实写回 `workflow_state.json`
  - 后续若继续增强，可再补 `draft / close / snapshot` 的 phase owner 写回
- Resolution:
  - 已新增 `scripts/workflow_state_utils.py`
  - `scripts/project-maintenance.py` / `scripts/post-task-maintenance.py` 现在会真实写回 `.mighty/workflow_state.json`
  - maintenance 完成后会把：
    - `current_step` 推进到 `snapshot`
    - `last_successful_checkpoint` 写成 `maintenance`
    - `maintenance_report_file` 写入当前任务参数
  - 已由 `tests/test_inkos_growth_plan.py` 覆盖 maintenance 尾段的真实 checkpoint 写回

### AOI-004 `active-context` 第二提示中心风险已收口

- Status: `resolved`
- Scope:
  - `scripts/build_active_context.py`
  - `.mighty/active-context.json`
  - `.mighty/learned-patterns.json`
  - `skills/novel-write/SKILL.md`
  - `skills/novel-status/SKILL.md`
  - `skills/novel-query/SKILL.md`
- Problem:
  - `active-context` 的定位是当前写作上下文侧栏，这个方向是对的
  - 历史实现直接复制了 `recent_guardrails`，会让它有长成第二提示真值中心的风险
- Why not fixed now:
  - 当前复制风险已收口，后续重点变成“新增字段时不要再次复制 canon/guidance 正文”
- Risk if deferred:
  - 后续若有人继续往 `active-context` 塞长文本 guidance，会重新引入 freshness drift
- Trigger to revisit:
  - 下一次给 `active-context` 增加字段
  - 下一次出现 guardrail/staleness 相关 bug
- Planned direction:
  - 保持 projection/pointer 角色
  - 新增字段优先做摘要，不复制完整 guidance
- Resolution:
  - `scripts/build_active_context.py` 已改为输出 `guardrail_summary`
  - `active-context` 不再复制 `recent_guardrails` 正文，只保留：
    - 是否存在
    - 各类约束条目数量
    - `expires_after_chapter`
    - sidecar 来源指针
  - 已由 `tests/test_active_context.py` 覆盖

### AOI-005 顶层入口文档职责已收口

- Status: `resolved`
- Scope:
  - `README.md`
  - `docs/INDEX.md`
  - `docs/00-当前有效/default-workflows.md`
  - `docs/00-当前有效/start-here.md`
  - `docs/00-当前有效/skill-usage.md`
- Problem:
  - 二级入口已经比过去更一致
  - 但顶层入口仍偏重，`README.md` 继续承担大量参考和流程事实
  - `INDEX` 还没有完全成为唯一导航
- Why not fixed now:
  - 需要和这轮 workflow/contract 收口一起做，否则容易改完又漂
- Risk if deferred:
  - 入口事实继续在多个文档重复维护
  - 后续功能并入时，容易出现“二级入口已更新、顶层入口未更新”
- Trigger to revisit:
  - 下一次新增默认工作流步骤
  - 下一次新增长期 sidecar / 入口文档
- Planned direction:
  - `README` 退回薄入口
  - `INDEX` 做唯一导航
  - `default-workflows` 做唯一流程真源
- Resolution:
  - `README.md` 已收薄为最短启动说明和关键治理边界入口
  - `docs/INDEX.md` 已作为状态目录导航页保留在根层
  - `docs/00-当前有效/default-workflows.md` 继续承担默认工作流真源
  - `docs/00-当前有效/start-here.md` 保留首次上手入口
  - `docs/00-当前有效/skill-usage.md` 保留调用名 / 触发名 / 使用提醒

### AOI-006 验证门已覆盖当前关键治理风险

- Status: `resolved`
- Scope:
  - `scripts/validate-migration.sh`
  - `tests/test_*.py`
  - `scripts/sync-shared-from-genm.sh`
  - `scripts/project-maintenance.py`
  - `scripts/post_write_lint.py`
- Problem:
  - 当前验证对 token、存在性、局部脚本行为覆盖较多
  - 当时对以下风险覆盖不足：
    - `shared` 漂移 / overwrite
    - maintenance 最终态顺序
    - `shared` overlay / allowlist 语义
- Why not fixed now:
  - 当前三类护栏已补；后续主要是继续随 shared / workflow 语义演化补测试
- Risk if deferred:
  - 若后续扩 shared governance 或 transaction phase owner 而不补测试，仍会再次出现“测试绿但治理不稳”
- Trigger to revisit:
  - 下一次修改验证脚本
  - 下一次修改 maintenance 链
  - 下一次调整 `shared` 或 state contract
- Planned direction:
  - 对新增 shared governance 或 transaction phase 再继续加 targeted tests
- Resolution:
  - 已新增 `tests/test_shared_sync_governance.py`
    - 覆盖 `--report-json`
    - 覆盖 unexpected local-only block
    - 覆盖 same-path drift block
    - 覆盖 `--allow-drift-overwrite`
    - 覆盖 protected local restore
  - 已补 `tests/test_inkos_growth_plan.py`
    - 覆盖 maintenance 后 `workflow_state.json` 的 `current_step = snapshot`
    - 覆盖 `last_successful_checkpoint = maintenance`
    - 覆盖 existing workflow state 的 maintenance 更新
  - 已将 `shared/sync-governance.json` 纳入 `scripts/validate-migration.sh`

### AOI-007 MCP memory / 调度层融合边界已正式化

- Status: `resolved`
- Scope:
  - MCP memory
  - `novel-resume`
  - `novel-workflow`
  - `novel-status`
  - `novel-query`
  - `.mighty/*` sidecars
- Problem:
  - 当前仓库已经很适合和 MCP memory 做跨会话协调融合
  - 但仍未正式定义：
    - 哪些本地文件是唯一真值
    - 哪些 sidecar 允许映射到 memory
    - memory 能记录哪些摘要，不能记录哪些 canon 内容
- Why not fixed now:
  - 需要先把本地 contract/sidecar/shared 边界收口，否则外接 memory 会放大本地不一致
- Risk if deferred:
  - MCP memory 可能变成第二真值中心
  - 调度层可能重定义本地 transaction phase
- Trigger to revisit:
  - 下一次明确接入 MCP memory / 状态调度
  - 下一次为 agent 协作增加跨会话恢复能力
- Planned direction:
  - 先完成本地协议化重构
  - 再定义“本地真值 vs MCP 协调记忆”的映射规范
- Resolution:
  - 已在 `docs/00-当前有效/v1-boundary.md` 明确：
    - 本地文件仍是唯一真值
    - MCP memory 只做协调记忆，不做 canon 真源
    - 不允许复制 `state.json` / `state-archive.json` / `设定集/` 全量 canon
    - 不允许复制 sidecar 正文作为第二真值

### AOI-008 保持不引入 monolithic runtime / plugin framework 边界

- Status: `resolved`
- Scope:
  - 全项目架构边界
- Problem:
  - 当前很容易被“继续抽象”推向独立 daemon / plugin / orchestration runtime
  - 这会把 `Genm-codex` 从 docs-driven workflow system 推成另一个产品形态
- Why not fixed now:
  - 这是有意保留的边界，不是待开发能力
- Risk if deferred:
  - 后续新功能可能在无明确边界的情况下逐渐偷渡进平行运行时
- Trigger to revisit:
  - 下一次有人提议引入统一 runtime / scheduler / daemon / plugin system
- Planned direction:
  - 保持 `docs + skills + scripts + sidecars` 主体骨架
  - 任何增强优先落在现有主线，而不是平行架构
- Resolution:
  - 已在 `README.md` 与 `docs/00-当前有效/v1-boundary.md` 明确：
    - 默认骨架保持 `docs + skills + scripts + sidecars`
    - 不进入独立 daemon / scheduler / plugin framework / orchestration runtime 路线
