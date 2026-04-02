# 本周变更（2026-03-30 至 2026-04-05）

## 2026-04-02 周四

### 今日变更

- [x] 新增 `v1.6.1-roadmap.md`，将 `Gate 1` 后的 host evidence closure / hardening lane 正式收成 follow-up roadmap
- [x] 更新 `README.md`、`docs/INDEX.md`、`v1.6-roadmap.md`，明确 `v1.6` 继续保持唯一 mainline，`v1.6.1` 是当前 follow-up
- [x] 同步 `.ops/active-plan.md`、`.ops/progress.md`、`.ops/findings.md`、`.ops/decisions.md`，让 active ops 真源切到 `v1.6.1` 当前状态
- [x] 更新 `docs/00-当前有效/document-status-convention.md`，补 `active-follow-up-roadmap` 状态示例
- [x] 更新 `docs/00-当前有效/host-support-status-v1.6.md`，补 `v1.6.1` follow-up 指针与当前 evidence gap 提示
- [x] 细化 `v1.6.1-roadmap.md` 的 Evidence gap 台账，将后续动作拆成 invocation / automation / asset boundary / promotion readiness 四个执行块
- [x] 在 `.ops/active-plan.md` 中明确 `v1.6.1` 的下一步执行顺序：先做 invocation / automation 证据收口，再做 asset boundary + projection / doctor hardening，最后才看 `Gate 2`
- [x] 将下一步最小产出物收口为 `evidence matrix`、最小 `smoke / trace`、`asset-boundary / host-query contract` 与 `doctor / projection checklist`
- [x] 将 `v1.6.1-roadmap.md` 从偏 evidence gap checklist 的表达重构为更接近 `v1.6-roadmap.md` 的大 phase + status roadmap 视角
- [x] 将 `.ops/active-plan.md` 的 `Immediate Next Steps` 改写为 `Current Phase View`，避免继续用小任务顺序表达当前 follow-up
- [x] 将 `.ops/progress.md`、`.ops/findings.md` 与 `.ops/decisions.md` 进一步收紧为 phase-driven follow-up 口径，避免 active ops 残留 checklist / next-candidate 叙事
- [x] 修复 `shared/templates/host-evidence-ledger-v1.json` 中 Trae MCP runtime evidence 的结构残缺，恢复 evidence ledger 的有效记录
- [x] 收紧 `shared/templates/host-capability-matrix-v1.json` 与 `docs/00-当前有效/host-support-status-v1.6.md` 的 Trae 边界措辞，明确 path scan / allowlisted file source 不等于已跟踪 repo asset
- [x] 运行 Phase 2 收口验证链并全部通过：state contracts、host projection/doc tests、doctor 与 migration validation
- [x] 将 `v1.6.1` `Phase 2: Evidence Boundary Closure` 正式回写为完成态，并把 active ops 当前状态同步到收口结果
- [x] 修复 `workflow_state` 对 `maintenance_report_file` / `snapshot_file` 的绝对路径持久化问题，改为保存项目内相对路径
- [x] 兼容 `knowledge-projection` 对旧格式 workflow artifact 路径的解析，并限制只认可当前项目 `.mighty` 下的 repo-owned artifact
- [x] 为 `project-maintenance` 增加 repo-owned tail 前置校验，阻止 `gate-check` 等前序阶段被错误跳关到 `snapshot`
- [x] 调整 `project-maintenance` 的 report 写盘顺序，确保同轮 `knowledge-projection` / `workflow-health` 不再因 `maintenance-report.json` 尚未落盘而误报
- [x] 补充 workflow 回归测试：相对路径、旧 checkout 兼容、外部路径拒绝、repo-owned tail 准入与 maintenance 顺序回归
- [x] 收紧 snapshot 完成态校验：归一化后的 `snapshot_file` 必须是当前项目 `.mighty/snapshots/` 下真实存在的文件，缺失 sidecar 不再推进 completed
- [x] 调整 `project-maintenance` 的 snapshot 异常收口：`mark_snapshot_complete` 失败时将 `maintenance-report.json` 明确回写为 `failed`，不再残留 `running`
- [x] 补充缺失 snapshot sidecar 的回归测试，并将文件存在性检查从 `exists()` 收紧为 `is_file()`
- [x] 在本地缺少 `black` / `ruff` 的情况下，按 Black 风格手工整理 `project-maintenance`、`workflow_state_utils` 与 maintenance tolerance 测试文件
- [x] 补强 `project-maintenance` 尾段 report 写盘 contract：在 `knowledge_projection` 前写当前结果、在 `knowledge_projection` 后重写 report、在 `workflow_health` 后落最终 report，确保消费者读取到同轮最新状态且最终 steps 完整
- [x] 扩展 maintenance tolerance 回归，新增 `knowledge_projection` 失败与 `workflow_health` 失败两条用例，分别锁定中段重写与最终重写 report 的时序 contract
- [x] 修复 `build_project_knowledge_projection.py` 的 sidecar 路径归一化缺口，先 `resolve(strict=False)` 再做 project-root / repo-owned 边界校验，阻断 `..` 路径穿越绕过
- [x] 扩展 knowledge projection 回归，新增 `snapshot_file` 路径穿越用例，锁定 `.mighty/snapshots/../../..` 逃逸场景必须判为缺失 artifact
- [x] 将根目录 `task_plan.md` / `progress.md` / `findings.md` 进一步收成 legacy stub / archive navigation，并把完整历史正文分别固化到 `task_plan_archive.md`、`docs/90-归档/阶段/root-progress-legacy-archive.md`、`docs/90-归档/阶段/root-findings-legacy-archive.md`
- [x] 同步 `README.md`、`docs/INDEX.md`、`docs/00-当前有效/start-here.md`、`.ops/README.md`、`AGENTS.md`、`project-map.yaml`、`docs/00-当前有效/root-retention-policy.md`、`docs/90-归档/README.md`，统一 `.ops/` 为 active truth、root 三件套为 legacy stub 的口径
- [x] 修正 stale references 与 machine-readable sidecar：将 `shared/references/chapter-index-schema.md`、`docs/10-进行中/architecture-open-issues.md`、`docs/10-进行中/batch-evidence-sidecar.json`、`docs/10-进行中/cross-platform-entity-evidence-agent-prompt-v1.5.md` 对齐到 `.ops/active-plan.md` / `.ops/progress.md` / `.ops/findings.md`
- [x] 扩展 `tests/test_issue_regressions.py`，锁定 `progress.md` / `findings.md` 的 legacy stub 约束以及 stale reference / sidecar 的 `.ops` 指针回归
- [x] 在 `docs/00-当前有效/skill-usage.md` 顶部补充 Codex / Claude Code 接手提示，并追加回归断言，进一步降低把 root 三件套误判为当前主入口的概率
- [x] 将 `.git/config lock` 规避方案固化为规则：全局 `~/.claude/CLAUDE.md` 为并行 Agent 增加 worktree 例外，仓库级 `AGENTS.md` 明确 review/search agent 默认避免并发创建 git worktree

### 遇到的问题

- `.ops/decisions.md` 的表格风格与当前 markdownlint 期望不一致，需要收紧到仓库当前使用的 table style
- `document-status-convention.md` 在快速补丁后出现空行诊断，需要整体回写为规范 Markdown
- `host-support-status-v1.6.md` 仍有 projection 生成的 Markdown 风格告警；当前优先保证 truth / projection / doctor exact-match，lint 风格留待后续 hardening 处理
- workflow 尾段修复时，Codex review 暴露出三个高优先级缺口：状态机允许从前序阶段跳关、maintenance-report 写盘时序会让同轮 projection/health 误报失败，以及 knowledge projection 读侧存在未归一化 `..` 路径穿越校验缺口
- review agent 在同仓并发创建 worktree 时多次触发 `.git/config` 写锁竞争，导致审查阶段间歇性退化到主线程手动复核

### 提炼的规则

- `v1.6` 下的收口 lane 应优先建 follow-up roadmap，而不是轻易升格为新的 mainline 版本
- host / MCP 相关增强优先复用现有 repo-owned read-only query 面，不先新造重型 MCP
- `promotion readiness` / `Gate 2` 不应前置；先补调用与自动化证据，再谈承诺升级
- 对 projection 生成且受 doctor 精确比对的文档，优先保证 truth 一致性；Markdown 风格修饰应放在不破坏 exact-match contract 的后续 hardening 中处理
- 只要 sidecar 会被跨 checkout 或示例项目复用，持久化格式就不能携带机器相关绝对路径
- repo-owned tail 的状态写回必须校验前序 checkpoint；不能让 `maintenance/snapshot` 成为跳过 `gate-check/draft/close` 的快捷通道
- snapshot 完成态只能建立在当前项目内真实存在的 repo-owned sidecar 文件之上；归一化旧路径不等于可以直接判定成功
- 当 snapshot 结算失败时，`maintenance-report.json` 必须显式落成 `failed`，不能把下游诊断留在 `running` 中间态
- 对会被 downstream sidecar 消费的 `maintenance-report.json`，既要在消费者执行前写出当前结果，也要在消费者完成后重写一次，确保磁盘上的 `steps` 与最终失败态完整反映本轮执行
- 凡是从 workflow sidecar 读取 artifact 路径的读侧工具，必须先做 `resolve(strict=False)` 归一化，再校验 project-root 与 repo-owned 前缀；不能只看字符串前缀
- 多个独立 agent 默认应并行，但只要任务会创建 git worktree，就要把 `.git/config` 写锁竞争纳入调度判断：review/search 优先非 worktree，必须 worktree 时优先串行，先排查 lock 再重试
