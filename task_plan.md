# Task Plan: 反脸谱化体系十二模块与技能接线

## Goal
在仓库内落成“反脸谱化体系”的 12 个主模块文档，并将其以可执行约束接入 `novel-outline` / `novel-review` / `novel-write` / `novel-fix` / `novel-precheck`，同时补齐 smoke 证据、轻量 state 约定、案例校准，以及一轮真实链路 smoke。

## Current Phase
Phase 5

## Phases

### Phase 1: Requirements & Discovery
- [x] 理解用户目标与项目约束
- [x] 读取相关技能、阶段文档与放置约定
- [x] 记录关键发现到 `findings.md`
- **Status:** complete

### Phase 2: Framework Design
- [x] 固化 12 模块的目录、职责与接口
- [x] 确认文档放置位置与命名约定
- [x] 明确技能接线范围与最小可用变更
- **Status:** complete

### Phase 3: Documentation Implementation
- [x] 编写 12 个模块文档
- [x] 补充总入口或索引文档
- [x] 更新相关阶段/使用文档中的新事实
- **Status:** complete

### Phase 4: Skill Wiring
- [x] 更新 `novel-outline` 的读取与使用规则
- [x] 更新 `novel-review` 的读取与使用规则
- [x] 视需要更新相关辅助 skill 或共享引用
- **Status:** complete

### Phase 5: Verification & Delivery
- [x] 进行结构与引用校验
- [x] 记录验证结果到 `progress.md`
- [x] 总结输出与残余风险
- **Status:** complete

### Phase 6: Extension P0-P2
- [x] 完成反脸谱化 smoke 文档
- [x] 扩展 `novel-write` / `novel-precheck` 接线
- [x] 固化轻量 state 约定与项目内案例校准
- **Status:** complete

### Phase 7: Real Chain Smoke
- [x] 基于隔离副本跑一遍 `outline -> write -> review -> fix -> precheck`
- [x] 记录真实链路样本产物与状态写回
- [x] 输出独立 smoke 结论文档
- **Status:** complete

### Phase 8: Real Chain Closure
- [x] 基于首轮 precheck 结果继续压章
- [x] 补第二轮复审与预检结论
- [x] 将真实链路文档更新为闭环版本
- **Status:** complete

### Phase 9: Cross-Genre Validation
- [x] 复制异题材样本做隔离副本
- [x] 在异题材样本上跑第二条真实链路
- [x] 输出跨流派交叉验证文档
- **Status:** complete

### Phase 10: Usage Guidance
- [x] 将双样本 smoke 结果收束成工作流使用建议
- [x] 在反脸谱化入口和默认工作流中挂入口
- [x] 记录后续推荐扩展方向
- **Status:** complete

### Phase 11: Realistic Validation
- [x] 复制现实情感样本做隔离副本
- [x] 在现实情感样本上完成第三条真实链路
- [x] 输出现实情感交叉验证文档
- **Status:** complete

### Phase 12: System Validation
- [x] 新建系统任务线最小 smoke 项目
- [x] 在系统样本上完成第四条真实链路
- [x] 输出系统流交叉验证文档
- **Status:** complete

### Phase 13: Historical Closure
- [x] 新增 `docs/phase-17-summary.md`
- [x] 将阶段总结入口挂回 `README.md`
- [x] 作为项目历史结论正式结案
- **Status:** complete

## Key Questions
1. 12 个模块应该落在 `docs/`、`shared/` 还是 `skills/` 的哪一层，才能既可维护又可被 skill 复用？
2. `novel-outline` / `novel-review` 目前如何引用项目内方法论文档，接线粒度该落在显式读取路径、检查清单，还是工作流说明？
3. 除了技能文档，还需要在哪些项目级文档里承载“新增事实”，才能满足可接手和可复用要求？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 使用文件化计划管理本次任务 | 任务跨 12 份文档与多个 skill，复杂度高，适合持久化工作记忆 |
| 新体系落在 `docs/anti-flattening-framework/` | 避免污染 `shared/`，同时保留单一事实源并便于 skill 显式读取 |
| 首轮接线聚焦 `novel-outline` / `novel-review` / `novel-fix` | 这三者正好覆盖上游结构、中游评审和下游局部修补 |
| 第二轮扩展接线聚焦 `novel-write` / `novel-precheck` | 这样反脸谱化规则就能覆盖写作、评审、修复、投稿前检查的主链 |
| state 只保留轻量 `chapter_meta` 扩展，不新造平行顶层结构 | 避免把 `.mighty/state.json` 变成新的复杂评分数据库 |
| 真实链路 smoke 使用隔离副本 `smoke/e2e-gongdou-evil-antiflattening-20260322` | 保留现有样本不动，同时拿到可重复的真实 workflow 证据 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| 仓库存在大量与本任务无关的脏工作树改动 | 1 | 仅在目标文档与技能文件中局部修改，不回滚、不覆盖其他改动 |

## Notes
- 优先把新事实放在单一来源，避免在多个 skill 中平行重复定义整套规则
- `shared/` 默认不手改，除非调研确认这里才是正确承载层
- 每完成一轮有意义的修改后同步更新 `progress.md`
