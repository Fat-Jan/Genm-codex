# Findings & Decisions

## Requirements
- 在当前仓库内自动完成“反脸谱化体系”12 个主模块
- 将该体系接入 `novel-outline` / `novel-review`
- 当前阶段偏“打磨”，因此模板、检查、案例校准都应进入主结构，而不是只做附录
- 新事实需要能被后续工作流与接手者稳定发现

## Research Findings
- 项目级约定要求：复杂任务先调研代码、数据流和现有约定，再实施
- 项目对首次进入仓库的快速入口强调 `README.md`、`docs/start-here.md`、`docs/skill-usage.md` 与阶段文档
- `planning-with-files` 适用于超过 5 次工具调用的复杂任务，并要求在项目根创建 `task_plan.md`、`findings.md`、`progress.md`
- `novel-outline` 当前负责上游结构约束，显式读取 `shared` 资产和若干 `docs/` 规则文件，但没有“反脸谱化/群像校准”层
- `novel-review` 当前负责下游质量路由与 state 回写，已有 bucket / technique / tagpack 检查，但没有角色立场、叙事权、群像失衡的统一审计层
- `docs/phase-9-summary.md` 与 `docs/phase-9b-quality-loop-design.md` 已把项目方向收束为“包装生成层 + 质量闭环整合”，新增体系应更像质量闭环扩层，而不是平行新 skill
- `docs/default-workflows.md` 已把 `novel-outline -> novel-write -> novel-review -> fix/polish/rewrite` 固化为默认主线，因此接线优先级应放在 `outline` 和 `review`
- 仓库现有规则型文档主要落在 `docs/`，skill 通过相对路径显式读取；`shared/` 更偏源仓库同步资产，不适合作为本次手工维护主承载层
- `validate-migration.sh` 在本轮改动后仍通过，说明新增文档与 skill 接线没有破坏迁移结构校验
- 仓库当前为脏工作树，存在大量本任务无关改动；本次仅局部修改目标文档与 skill，避免误动其他变更
- `novel-write` 与 `novel-precheck` 已完成第二轮接线，反脸谱化不再只停留在 outline/review/fix
- `shared/references/shared/state-schema.md` 和 `shared/templates/state-v5-template.json` 已把反脸谱化 state 写回收成轻量约定：
  - `chapter_meta[N].anti_flattening_flags`
  - `chapter_meta[N].anti_flattening_summary`
  - `dimension_scores` 可附加 `人物立体度 / 关系张力 / 阵营分歧 / 代价感`
- `docs/anti-flattening-framework/smoke-results-2026-03-22.md` 已记录本轮结构烟测与样本校准结果
- 在隔离副本 `smoke/e2e-gongdou-evil-antiflattening-20260322` 上已完成一轮真实链路 smoke：
  - 新建 `第007章` 章纲
  - 写出 `第007章` 正文
  - 将 review 结果写回 `chapter_meta["7"]`
  - 做了一轮局部 `fix`
  - 完成一轮 `precheck` 结论
- 真实链路 smoke 证明：
  - 反脸谱化规则能落进章纲字段
  - 能驱动 review 输出 `anti_flattening_flags` 和 `anti_flattening_summary`
  - 能转成 fix 级别的局部动作
  - 能在 precheck 中成为投稿前风险项
- 真实链路在第二轮压章与复审后已闭环：
  - `chapter_meta["7"].word_count` 从 `6012` 压到 `3071`
  - `review_score` 从 `82` 提到 `88`
  - `recommended_next_action` 从 `novel-fix` 变为 `novel-write`
  - `anti_flattening_flags` 清空为无当前结构性警报
- 第二条交叉验证已在 `smoke/e2e-dual-substitute-evil-antiflattening-20260322` 上完成：
  - 新建第006章章纲与正文
  - `chapter_meta["6"].review_score = 88`
  - `recommended_next_action = novel-write`
  - 当前章不需要 fix 即可通过 review
  - 字数已压到 `4199`，回到平台上限内
  - 说明同一套框架在异题材上可以得到不同但稳定的工作流结果
- 已新增 `docs/anti-flattening-framework/workflow-usage-guide-2026-03-22.md`
  - 把两条真实 smoke 收束成三种典型路线：
    - 直接通过型
    - 局部修补型
    - 上推重构型
  - 并同步挂回 `docs/anti-flattening-framework/README.md` 与 `docs/default-workflows.md`
- 第三条现实情感样本也已完成：
  - 副本：`smoke/e2e-qinggan-evil-antiflattening-20260322`
  - 新建第004章章纲与正文
  - `chapter_meta["4"].review_score = 87`
  - `recommended_next_action = novel-write`
  - 这条线验证了“支持者是否也在保自己的现实秩序”这一类问题
- 第四条系统任务线样本也已完成：
  - 副本：`smoke/e2e-system-antiflattening-20260322`
  - 新建最小系统流项目骨架和第004章章纲 / 正文
  - `chapter_meta["4"].review_score = 87`
  - `recommended_next_action = novel-write`
  - 这条线验证了“系统是否把人压成任务对象 / 主角是否吞掉他人人生主权”
- 已新增 `docs/phase-17-summary.md`
  - 正式把本轮工作写入项目阶段历史
  - 结论是：反脸谱化体系已具备作为默认质量链子层长期保留的条件

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 先用 12 模块文档建立方法论单一来源，再做 skill 接线 | 避免把完整规则平铺复制进多个 skill，满足单一事实源 |
| 新体系优先放在 `docs/` 下集中成组 | 与现有规则文档承载层一致，便于 skill 显式读取并避免污染 `shared/` |
| 新增一个 `README.md` 索引但不把它算入 12 模块 | 方便 skill 和入口文档稳定引用，同时保持 12 主模块定义不变 |
| smoke 采用“结构烟测 + 样本校准烟测” | 当前终端环境无法直接跑 Codex skill 黑盒调用，但可以真实验证路径、规则栈兼容性和样本判断点 |
| 真实链路 smoke 采用“手工遵循 skill 契约”的方式执行 | 当前环境没有独立的 skill 调度入口，但可以在同目录结构、同 state 约束下跑出真实产物和状态写回 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| 仓库已有大量无关改动 | 通过局部接线和新目录隔离，避免与现有变更冲突 |

## Resources
- `README.md`
- `docs/start-here.md`
- `docs/skill-usage.md`
- `docs/default-workflows.md`
- `docs/phase-9-summary.md`
- `docs/phase-9b-quality-loop-design.md`
- `docs/anti-flattening-framework/README.md`
- `docs/anti-flattening-framework/01-总纲.md`
- `docs/anti-flattening-framework/11-检查清单与评分规约.md`
- `docs/anti-flattening-framework/12-案例对照与校准.md`
- `docs/anti-flattening-framework/smoke-results-2026-03-22.md`
- `docs/anti-flattening-framework/real-chain-smoke-e2e-gongdou-evil-2026-03-22.md`
- `docs/anti-flattening-framework/cross-genre-smoke-dual-substitute-evil-2026-03-22.md`
- `docs/anti-flattening-framework/workflow-usage-guide-2026-03-22.md`
- `docs/anti-flattening-framework/cross-genre-smoke-realistic-divorce-2026-03-22.md`
- `docs/anti-flattening-framework/cross-genre-smoke-system-taskline-2026-03-22.md`
- `docs/phase-17-summary.md`
- `skills/novel-outline/SKILL.md`
- `skills/novel-review/SKILL.md`
- `skills/novel-fix/SKILL.md`
- `skills/novel-write/SKILL.md`
- `skills/novel-precheck/SKILL.md`
- `skills/novel-init/SKILL.md`
- `shared/references/shared/state-schema.md`
- `shared/templates/state-v5-template.json`
- `smoke/e2e-gongdou-evil-antiflattening-20260322/大纲/章纲/第007章.md`
- `smoke/e2e-gongdou-evil-antiflattening-20260322/chapters/第007章.md`
- `smoke/e2e-gongdou-evil-antiflattening-20260322/.mighty/state.json`
- `smoke/e2e-dual-substitute-evil-antiflattening-20260322/大纲/章纲/第006章.md`
- `smoke/e2e-dual-substitute-evil-antiflattening-20260322/chapters/第006章.md`
- `smoke/e2e-dual-substitute-evil-antiflattening-20260322/.mighty/state.json`
- `smoke/e2e-qinggan-evil-antiflattening-20260322/大纲/章纲/第004章.md`
- `smoke/e2e-qinggan-evil-antiflattening-20260322/chapters/第004章.md`
- `smoke/e2e-qinggan-evil-antiflattening-20260322/.mighty/state.json`
- `smoke/e2e-system-antiflattening-20260322/大纲/总纲.md`
- `smoke/e2e-system-antiflattening-20260322/大纲/章纲/第004章.md`
- `smoke/e2e-system-antiflattening-20260322/chapters/第004章.md`
- `smoke/e2e-system-antiflattening-20260322/.mighty/state.json`
- `/Users/arm/.claude/skills/planning-with-files/.codex/skills/planning-with-files/SKILL.md`

## Visual/Browser Findings
- 本轮任务暂未使用需要单独转存的图像/PDF信息

---
*Update this file after every 2 view/browser/search operations*
*This prevents visual information from being lost*
