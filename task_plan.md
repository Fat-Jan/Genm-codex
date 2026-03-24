# Task Plan: ISSUES 2026-03-24 状态归档

## Goal
确认 [ISSUES.md](/Users/arm/Desktop/vscode/Genm-codex/ISSUES.md) 中列出的 P0 / P1 / P2 问题是否已在仓库中真实落地修复；补齐遗漏项后，将每个问题在原文中标记状态并归档。

## Current Phase
Complete

## Phases

### Phase 1: Re-check
- [x] 重读 `ISSUES.md`
- [x] 核对相关 skill / 脚本 / 工作流文档
- [x] 确认哪些问题已修、哪些未稳定落地
- **Status:** complete

### Phase 2: Close Remaining Gaps
- [x] 修复 `novel-write` 重复编号
- [x] 补齐 `launch-stack` 触发时机与 placeholder 合同
- [x] 补齐 `novel-learn` / `novel-close` 合同缺口
- [x] 补齐 `docs/INDEX.md` / `smoke/README.md`
- [x] 将 `task_plan.md` 收为单一活跃计划
- **Status:** complete

### Phase 3: Verify & Archive
- [x] 运行问题回归测试
- [x] 运行迁移/全量测试
- [x] 更新 `ISSUES.md` 状态与归档说明
- **Status:** complete

## Notes
- 历史多计划内容已转存到 `task_plan_archive.md`
- 与本轮无关的 `projects/*/.mighty/state.json` 脏改动不触碰
