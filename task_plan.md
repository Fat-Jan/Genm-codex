# Task Plan: 2026-03-25 架构审查与扩展路径方案

## Goal
审查 `Genm-codex` 当前整体架构是否合理，识别技能层、文档/共享资产层、状态/sidecar 层和路径治理层的主要风险，并给出后续功能扩展时的结构优化与路径治理方案。

## Current Phase
Complete

## Phases

### Phase 1: Discovery
- [x] 读取 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md`
- [x] 检查 `task_plan.md` / `findings.md` / `progress.md` 当前状态
- [x] 抽样关键 `SKILL.md`、核心脚本、状态模板与测试
- **Status:** complete

### Phase 2: Parallel Review
- [x] 并行审查 `skill/workflow` 层
- [x] 并行审查 `docs/shared/tests/governance` 层
- [x] 并行审查 `state/schema/sidecar/path` 扩展风险
- **Status:** complete

### Phase 3: Verification & Synthesis
- [x] 运行 `bash scripts/validate-migration.sh`
- [x] 运行 `pytest -q`
- [x] 汇总主会话与子代理发现，形成优化方案
- **Status:** complete

## Key Questions
1. 当前“`skills + docs + scripts + shared + sidecars`”分层是否仍保持单一事实源，还是已经开始多点漂移？
2. 后续再新增规则层、平台能力或维护链时，最先失控的会是路径、契约还是文档入口？
3. 哪些地方应当收敛成 manifest / index / registry，哪些地方继续保持 docs-first 即可？

## Notes
- 本轮为只读架构审查；除 planning files 外不修改业务文件
- 已使用并行 agent teams 做分层调研
- 仓库仍存在与本轮无关的 `projects/*/.mighty/state.json` 脏改动，不触碰
