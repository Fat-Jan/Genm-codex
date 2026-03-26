# Progress Log

## Session: 2026-03-22

### Phase 1: Requirements & Discovery
- **Status:** complete
- **Started:** 2026-03-22 17:50
- Actions taken:
  - 读取 `planning-with-files` 技能说明，确认需要先创建计划文件
  - 读取 `README.md` 与 `docs/00-当前有效/start-here.md`，确认项目结构、默认工作流与技能边界
  - 读取 `docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md`、`docs/90-归档/阶段/phase-9-summary.md`、`docs/90-归档/阶段/phase-9b-quality-loop-design.md`
  - 读取 `skills/novel-outline/SKILL.md`、`skills/novel-review/SKILL.md`、`skills/novel-fix/SKILL.md`
  - 建立本次任务的 `task_plan.md`、`findings.md`、`progress.md`
- Files created/modified:
  - `task_plan.md` (created)
  - `findings.md` (created)
  - `progress.md` (created)

### Phase 2: Framework Design
- **Status:** complete
- Actions taken:
  - 确认新体系承载层为 `docs/anti-flattening-framework/`
  - 固化“12 主模块 + 1 README 索引”的目录结构
  - 确认首轮接线范围为 `novel-outline`、`novel-review`、`novel-fix`
- Files created/modified:
  - `task_plan.md` (updated)
  - `findings.md` (updated)

### Phase 3: Documentation Implementation
- **Status:** complete
- Actions taken:
  - 新建 `docs/anti-flattening-framework/README.md`
  - 新建 12 个主模块文档，覆盖总纲、叙事权、角色分层、动力系统、关系/阵营、冲突后果、场景推进、流派故障、快速修复、工具流、检查规约、案例校准
  - 更新 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md` 暴露新事实
- Files created/modified:
  - `docs/anti-flattening-framework/README.md` (created)
  - `docs/anti-flattening-framework/01-总纲.md` (created)
  - `docs/anti-flattening-framework/02-叙事权与主角特权.md` (created)
  - `docs/anti-flattening-framework/03-角色分层与投入配额.md` (created)
  - `docs/anti-flattening-framework/04-角色动力系统.md` (created)
  - `docs/anti-flattening-framework/05-关系网络与阵营分歧.md` (created)
  - `docs/anti-flattening-framework/06-冲突-信息差-后果链.md` (created)
  - `docs/anti-flattening-framework/07-场景级群像推进.md` (created)
  - `docs/anti-flattening-framework/08-流派故障库.md` (created)
  - `docs/anti-flattening-framework/09-诊断信号与快速修复.md` (created)
  - `docs/anti-flattening-framework/10-工具包与工作流.md` (created)
  - `docs/anti-flattening-framework/11-检查清单与评分规约.md` (created)
  - `docs/anti-flattening-framework/12-案例对照与校准.md` (created)
  - `README.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)

### Phase 4: Skill Wiring
- **Status:** complete
- Actions taken:
  - 为 `novel-outline` 增加反脸谱化规则读取与上游结构约束
  - 为 `novel-review` 增加反脸谱化检查维度、输出摘要与 state 标记建议
  - 为 `novel-fix` 增加局部修复包读取与 rewrite 边界
- Files created/modified:
  - `skills/novel-outline/SKILL.md` (updated)
  - `skills/novel-review/SKILL.md` (updated)
  - `skills/novel-fix/SKILL.md` (updated)

### Phase 5: Verification & Delivery
- **Status:** complete
- Actions taken:
  - 用 `rg` 复查新引用路径
  - 运行 `bash scripts/validate-migration.sh`
  - 确认 12 模块与 `README` 索引文件均存在
  - 记录仓库存在大量无关改动，本次未触碰
- Files created/modified:
  - `progress.md` (updated)

### Phase 6: Extension P0-P2
- **Status:** complete
- Actions taken:
  - 为 `novel-write` 增加反脸谱化读取、正文侧结构约束与规则优先级
  - 为 `novel-precheck` 增加反脸谱化风险检查和输出项
  - 为 `novel-init` 增加 `chapter_meta` 轻量扩展约定说明
  - 更新 `shared/templates/state-v5-template.json` 与 `shared/references/shared/state-schema.md`
  - 扩展 `12-案例对照与校准.md`，加入项目内案例
  - 新建 `docs/anti-flattening-framework/smoke-results-2026-03-22.md`
  - 重新运行迁移结构校验，并验证 JSON 模板可解析
- Files created/modified:
  - `skills/novel-write/SKILL.md` (updated)
  - `skills/novel-precheck/SKILL.md` (updated)
  - `skills/novel-init/SKILL.md` (updated)
  - `shared/templates/state-v5-template.json` (updated)
  - `shared/references/shared/state-schema.md` (updated)
  - `docs/anti-flattening-framework/README.md` (updated)
  - `docs/anti-flattening-framework/11-检查清单与评分规约.md` (updated)
  - `docs/anti-flattening-framework/12-案例对照与校准.md` (updated)
  - `docs/anti-flattening-framework/smoke-results-2026-03-22.md` (created)
  - `README.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)

### Phase 7: Real Chain Smoke
- **Status:** complete
- Actions taken:
  - 复制 `smoke/e2e-gongdou-evil` 为隔离副本 `smoke/e2e-gongdou-evil-antiflattening-20260322`
  - 新建第 7 章章纲，显式写入主动方、防守方、误判点、独立议程与关系残账
  - 写出第 7 章正文并按 `novel-write` 约定更新副本 `.mighty/state.json`
  - 为 `chapter_meta["7"]` 写入 review 结果，路由到 `novel-fix`
  - 对第 7 章做局部 fix，并写回 `fixed_issues / fix_reason / last_fix_time`
  - 完成一轮手工遵循 skill 契约的 precheck 判断
  - 新建真实链路 smoke 文档并补 JSON / 迁移结构校验
- Files created/modified:
  - `smoke/e2e-gongdou-evil-antiflattening-20260322/大纲/章纲/第007章.md` (created)
  - `smoke/e2e-gongdou-evil-antiflattening-20260322/chapters/第007章.md` (created)
  - `smoke/e2e-gongdou-evil-antiflattening-20260322/.mighty/state.json` (updated)
  - `docs/anti-flattening-framework/real-chain-smoke-e2e-gongdou-evil-2026-03-22.md` (created)
  - `progress.md` (updated)

### Phase 8: Real Chain Closure
- **Status:** complete
- Actions taken:
  - 将副本第 7 章从 `6012` 字压缩到 `3071` 字
  - 按第二轮局部 fix 更新 `chapter_meta["7"]`
  - 手工按同一 review 契约完成复审，更新分数、路由和反脸谱化摘要
  - 将真实链路 smoke 文档更新为闭环版本
  - 再次校验副本 state JSON 一致性
- Files created/modified:
  - `smoke/e2e-gongdou-evil-antiflattening-20260322/chapters/第007章.md` (updated)
  - `smoke/e2e-gongdou-evil-antiflattening-20260322/.mighty/state.json` (updated)
  - `docs/anti-flattening-framework/real-chain-smoke-e2e-gongdou-evil-2026-03-22.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 9: Cross-Genre Validation
- **Status:** complete
- Actions taken:
  - 复制 `smoke/e2e-dual-substitute-evil` 为隔离副本 `smoke/e2e-dual-substitute-evil-antiflattening-20260322`
  - 新建第 6 章章纲，明确双女主裂口、机构角色边界和执行人职业防御
  - 写出第 6 章正文并按 `novel-write` 约定写回副本 state
  - 对第 6 章做手工遵循契约的 review，并继续压章到平台上限内
  - 最终将第 6 章收成 `review_score = 88`、`recommended_next_action = novel-write`
  - 新建跨流派交叉验证文档，比较宫斗链和双女主替身链的不同结果
- Files created/modified:
  - `smoke/e2e-dual-substitute-evil-antiflattening-20260322/大纲/章纲/第006章.md` (created)
  - `smoke/e2e-dual-substitute-evil-antiflattening-20260322/chapters/第006章.md` (created)
  - `smoke/e2e-dual-substitute-evil-antiflattening-20260322/.mighty/state.json` (updated)
  - `docs/anti-flattening-framework/cross-genre-smoke-dual-substitute-evil-2026-03-22.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 10: Usage Guidance
- **Status:** complete
- Actions taken:
  - 新建 `workflow-usage-guide-2026-03-22.md`
  - 将宫斗样本与双女主替身样本收束成三类工作流路线
  - 在 `docs/anti-flattening-framework/README.md` 和 `docs/00-当前有效/default-workflows.md` 增加入口
- Files created/modified:
  - `docs/anti-flattening-framework/workflow-usage-guide-2026-03-22.md` (created)
  - `docs/anti-flattening-framework/README.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 11: Realistic Validation
- **Status:** complete
- Actions taken:
  - 复制 `smoke/e2e-qinggan-evil` 为隔离副本 `smoke/e2e-qinggan-evil-antiflattening-20260322`
  - 新建第 4 章章纲，明确现实代价链、公司边界和母亲三十万线
  - 写出第 4 章正文并按 `novel-write` 约定写回副本 state
  - 对第 4 章做手工遵循契约的 review，结论为可直接继续写下一章
  - 新建现实情感交叉验证文档
- Files created/modified:
  - `smoke/e2e-qinggan-evil-antiflattening-20260322/大纲/章纲/第004章.md` (created)
  - `smoke/e2e-qinggan-evil-antiflattening-20260322/chapters/第004章.md` (created)
  - `smoke/e2e-qinggan-evil-antiflattening-20260322/.mighty/state.json` (updated)
  - `docs/anti-flattening-framework/cross-genre-smoke-realistic-divorce-2026-03-22.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 12: System Validation
- **Status:** complete
- Actions taken:
  - 新建 `smoke/e2e-system-antiflattening-20260322` 最小系统流 smoke 项目
  - 补齐总纲、主角卡、关键配角卡、系统规则与第 1-4 章章纲
  - 写出第 4 章正文，验证“系统最快路线”和“人情后果”正面对撞
  - 将第 4 章 review 结果写回 state，结论为可直接继续下一章
  - 新建系统流交叉验证文档，并同步到工作流建议中
- Files created/modified:
  - `smoke/e2e-system-antiflattening-20260322/.mighty/state.json` (created/updated)
  - `smoke/e2e-system-antiflattening-20260322/大纲/总纲.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/大纲/章纲/第001章.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/大纲/章纲/第002章.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/大纲/章纲/第003章.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/大纲/章纲/第004章.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/设定集/角色/主角.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/设定集/角色/方琴.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/设定集/角色/吴建国.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/设定集/角色/何书宁.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/设定集/力量体系.md` (created)
  - `smoke/e2e-system-antiflattening-20260322/chapters/第004章.md` (created)
  - `docs/anti-flattening-framework/cross-genre-smoke-system-taskline-2026-03-22.md` (created)
  - `docs/anti-flattening-framework/workflow-usage-guide-2026-03-22.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 13: Historical Closure
- **Status:** complete
- Actions taken:
  - 新建 `docs/90-归档/阶段/phase-17-summary.md`
  - 在 `README.md` 中补挂阶段总结与参考文档入口
  - 将本轮任务正式沉淀为项目历史结论
- Files created/modified:
  - `docs/90-归档/阶段/phase-17-summary.md` (created)
  - `README.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

## Session: 2026-03-25

### Phase 1: Architecture Discovery
- **Status:** complete
- Actions taken:
  - 读取 `task_plan.md` / `findings.md` / `progress.md` 当前状态
  - 读取 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md`、`docs/00-当前有效/shared-asset-dependency-map.md`
  - 抽样关键 `SKILL.md`、`scripts/`、`shared/`、`tests/`
  - 统计仓库规模与高频路径引用
- Files created/modified:
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 2: Parallel Review
- **Status:** complete
- Actions taken:
  - 并行委派 3 个 explorer agent 审查：
    - `skill/workflow` 层
    - `docs/shared/tests/governance` 层
    - `state/schema/sidecar/path` 扩展层
  - 汇总 agent 结论与主会话交叉验证
- Files created/modified:
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 3: Verification & Synthesis
- **Status:** complete
- Actions taken:
  - 运行 `bash scripts/validate-migration.sh`
  - 运行 `pytest -q`
  - 确认结果：
    - `Migration validation passed`
    - `204 passed, 192 subtests passed`
  - 形成总体判断：
    - 架构方向合理
    - 但 `state/schema/template/script`、`shared` 治理、skill 路径复制、入口文档职责已经出现扩展期漂移信号
- Files created/modified:
  - `task_plan_archive.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 4: Post-Upgrade Recheck
- **Status:** complete
- Actions taken:
  - 基于最新提交 `a953957` 重新审查 transactional / sidecar 升级
  - 阅读新增 contract/script/doc/test：
    - `chapter-transaction-schema`
    - `workflow-state-v2`
    - `build_active_context.py`
    - `build_volume_summaries.py`
    - `import_existing_chapters.py`
    - `post_write_lint.py`
  - 并行委派子代理复核：
    - workflow/transaction
    - state/sidecar/schema
    - docs/shared/governance
  - 重新运行：
    - `bash scripts/validate-migration.sh`
    - `pytest -q`
  - 新结论：
    - transactional / sidecar 方向整体增强了默认工作流
    - 但 `state/schema/template/script` 与 `shared` 治理风险仍是当前最优先收口点
- Files created/modified:
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 5: Open-Issue Ledger
- **Status:** complete
- Actions taken:
  - 新建长期治理台账 `docs/10-进行中/architecture-open-issues.md`
  - 将当前确认但尚未收口的问题按 `open / planned / monitoring / deferred` 分类
  - 在 `docs/INDEX.md` 中补挂入口
  - 明确该台账作为 repo-local 长期真源，MCP memory 仅做协作摘要，不替代此文档
  - 新建根目录提醒入口 `架构问题跟踪.md`，用于日常高可见提醒
- Files created/modified:
  - `docs/10-进行中/architecture-open-issues.md` (created)
  - `docs/INDEX.md` (updated)
  - `架构问题跟踪.md` (created)
  - `findings.md` (updated)
  - `progress.md` (updated)

## Session: 2026-03-24 番茄起盘协议栈与 Compiler 层

### Phase 1: Discovery & Spec Lock
- **Status:** complete
- Actions taken:
  - 读取 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/default-workflows.md` 与现有 `opening-and-plot-framework`
  - 反复调研番茄官方写作区与通用结构资料，比较“成熟剧情架构库 / 单主架构卡 / 协议栈”三种路径
  - 最终确定采用“番茄起盘协议栈 + compiler + 两本账”，并将通用框架降为映射参考
  - 新建正式 spec：`docs/superpowers/specs/2026-03-24-fanqie-launch-stack-design.md`
- Files created/modified:
  - `docs/superpowers/specs/2026-03-24-fanqie-launch-stack-design.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 2: Implementation Planning
- **Status:** complete
- Actions taken:
  - 读取 `writing-plans` 技能要求与现有 `docs/superpowers/plans/` 样式
  - 复查 `tests/test_opening_plot_framework.py`、`tests/test_writing_core_framework.py`、`skills/novel-outline/SKILL.md` 与 `state-schema.md`
  - 固化 v1 落点为“协议栈文档树 + compiler CLI + 轻量写回 + 五个 skill 接线 + 两个真实 smoke artifact”
  - 新建实施计划：`docs/superpowers/plans/2026-03-24-fanqie-launch-stack.md`
- Files created/modified:
  - `docs/superpowers/plans/2026-03-24-fanqie-launch-stack.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

## Session: 2026-03-24 写作基本功与内容标准规则层

### Phase 1: Boundary Lock
- **Status:** complete
- Actions taken:
  - 读取现有 `opening-and-plot-framework`、`anti-flattening-framework`、`fanqie-writing-techniques`、`fanqie-writer-zone-lessons`
  - 确认 `剧情层次` 继续复用 `opening-and-plot-framework`
  - 确认新框架只补 `基本功 / 内容标准 / memory / 包装输入`
- Files created/modified:
  - `docs/superpowers/plans/2026-03-24-writing-core-framework.md` (created)

### Phase 2: Red Test
- **Status:** complete
- Actions taken:
  - 新建 `tests/test_writing_core_framework.py`
  - 运行 `python -m unittest tests.test_writing_core_framework -v`
  - 确认失败点集中在：框架文件缺失、skill 未接线、entry docs 未暴露、state contract 未扩展
- Files created/modified:
  - `tests/test_writing_core_framework.py` (created)

### Phase 3: Docs + Wiring
- **Status:** complete
- Actions taken:
  - 新建 `docs/writing-core-framework/` 全套文档
  - 更新 `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` / `novel-learn`
  - 更新 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md`
  - 更新 `shared/references/shared/state-schema.md`、`shared/templates/state-v5-template.json`、`docs/00-当前有效/state-thinning-and-setting-sync.md`
- Files created/modified:
  - `docs/writing-core-framework/README.md` (created)
  - `docs/writing-core-framework/01-写作基本功总纲.md` (created)
  - `docs/writing-core-framework/02-叙述-镜头-信息投放.md` (created)
  - `docs/writing-core-framework/03-对白-动作-情绪-段落节奏.md` (created)
  - `docs/writing-core-framework/04-剧情层次与多线编排接口.md` (created)
  - `docs/writing-core-framework/05-内容标准与常见失格.md` (created)
  - `docs/writing-core-framework/06-精品审核与投稿前判断.md` (created)
  - `docs/writing-core-framework/07-memory-压缩信号约定.md` (created)
  - `docs/writing-core-framework/08-开篇包装输入接口.md` (created)
  - `skills/novel-outline/SKILL.md` (updated)
  - `skills/novel-write/SKILL.md` (updated)
  - `skills/novel-review/SKILL.md` (updated)
  - `skills/novel-precheck/SKILL.md` (updated)
  - `skills/novel-package/SKILL.md` (updated)
  - `skills/novel-learn/SKILL.md` (updated)
  - `README.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `shared/references/shared/state-schema.md` (updated)
  - `shared/templates/state-v5-template.json` (updated)
  - `docs/00-当前有效/state-thinning-and-setting-sync.md` (updated)

### Phase 4: Verification
- **Status:** complete
- Actions taken:
  - 运行 `python -m unittest tests.test_writing_core_framework -v`
  - 回归 `python -m unittest tests.test_opening_plot_framework -v`
  - 运行 `bash scripts/validate-migration.sh`
  - 读取 `projects/宗门垫底那年，我把废丹卖成了天价` 的 `state / learned-patterns / market-adjustments / 总纲 / 第001-003章`
  - 新建 `docs/writing-core-framework/real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md`
  - 为样本项目补最小 writeback：
    - `.mighty/learned-patterns.json` 增加 `opening_strategy / multi_line_guardrails / content_standard_alerts`
    - `.mighty/state.json` 增加 `chapter_meta["003"].content_standard_flags / packaging_alignment_note`
  - 运行 `python -m json.tool` 校验样本 JSON 文件
- Files created/modified:
  - `docs/writing-core-framework/real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md` (created)
  - `projects/宗门垫底那年，我把废丹卖成了天价/.mighty/learned-patterns.json` (updated)
  - `projects/宗门垫底那年，我把废丹卖成了天价/.mighty/state.json` (updated)
  - `docs/writing-core-framework/README.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 5: Proactive Enhancement
- **Status:** complete
- Actions taken:
  - 复核剩余缺口，确认最值钱的增强项是补第二条异路数真实样本
  - 读取 `projects/离婚冷静期那天，前夫把董事会席位押给了我` 的 `state / learned-patterns / market-adjustments / 总纲 / 第001-003章`
  - 新建 `docs/writing-core-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md`
  - 为第二个样本项目补最小 writeback：
    - `.mighty/learned-patterns.json` 增加 `opening_strategy / multi_line_guardrails / content_standard_alerts`
    - `.mighty/state.json` 增加 `learned_patterns.available_sections`
    - `.mighty/state.json` 增加 `chapter_meta["003"].content_standard_flags / packaging_alignment_note`
  - 再次运行 `python -m json.tool` 校验第二个样本 JSON
  - 再次运行 `python -m unittest tests.test_writing_core_framework -v`
  - 再次运行 `python -m unittest tests.test_opening_plot_framework -v`
  - 再次运行 `bash scripts/validate-migration.sh`
- Files created/modified:
  - `docs/writing-core-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md` (created)
  - `projects/离婚冷静期那天，前夫把董事会席位押给了我/.mighty/learned-patterns.json` (updated)
  - `projects/离婚冷静期那天，前夫把董事会席位押给了我/.mighty/state.json` (updated)
  - `docs/writing-core-framework/README.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 6: Packaging Closure
- **Status:** complete
- Actions taken:
  - 将两条真实样本的 `packaging-needs-update = yes` 继续推进为实际包装文件
  - 新建：
    - `projects/宗门垫底那年，我把废丹卖成了天价/包装/包装方案.md`
    - `projects/离婚冷静期那天，前夫把董事会席位押给了我/包装/包装方案.md`
  - 更新两份 `writing-core-framework` smoke 文档，补 `收口更新`
  - 再次运行：
    - `python -m unittest tests.test_writing_core_framework -v`
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `projects/宗门垫底那年，我把废丹卖成了天价/包装/包装方案.md` (created)
  - `projects/离婚冷静期那天，前夫把董事会席位押给了我/包装/包装方案.md` (created)
  - `docs/writing-core-framework/real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md` (updated)
  - `docs/writing-core-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 7: Regression Guardrails
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_writing_core_framework.py`
  - 新增对以下事实的自动校验：
    - 两份真实 smoke 文档存在
    - 两份样本包装文件存在并包含 `推荐书名 / 推荐简介`
    - 两个样本项目的 `learned-patterns.json` 含 `opening_strategy / multi_line_guardrails / content_standard_alerts`
    - 两个样本项目的 `state.json` 含 `content_standard_flags / packaging_alignment_note`
  - 运行：
    - `python -m unittest tests.test_writing_core_framework -v`
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `tests/test_writing_core_framework.py` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 8: Smoke Automation
- **Status:** complete
- Actions taken:
  - 新建 `scripts/writing_core_smoke.py`
  - 以最小可用边界实现：
    - `draft`
    - `writeback`
    - `save-packaging`
  - 新建 `tests/test_writing_core_smoke.py`
  - 将脚本入口挂回 `docs/writing-core-framework/README.md`
  - 运行：
    - `python -m unittest tests.test_writing_core_smoke -v`
    - `python -m unittest tests.test_writing_core_framework -v`
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `scripts/writing_core_smoke.py` (created)
  - `tests/test_writing_core_smoke.py` (created)
  - `docs/writing-core-framework/README.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 9: Scripted Third Sample
- **Status:** complete
- Actions taken:
  - 使用 `scripts/writing_core_smoke.py` 在 `projects/搬回老小区后，我靠蹭饭认识了整栋楼` 上跑 `writeback + save-packaging`
  - 发现第一次产出的 `都市日常` 包装文案把 outline markdown 标题污染进 synopsis
  - 先为该问题补 RED 测试，再修脚本：
    - 新增 `extract_outline_pitch`
    - 为 `都市日常` 增加专用 packaging 模板
    - 让脚本在 `packaging_status = written` 时显式写 `收口更新`
  - 重生成第三条样本文档与包装产物
  - 将第三条样本纳入 `tests/test_writing_core_framework.py` 回归集合
  - 再次运行：
    - `python -m unittest tests.test_writing_core_smoke -v`
    - `python -m unittest tests.test_writing_core_framework -v`
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `docs/writing-core-framework/real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-2026-03-24.md` (created/updated)
  - `projects/搬回老小区后，我靠蹭饭认识了整栋楼/包装/包装方案.md` (created/updated)
  - `scripts/writing_core_smoke.py` (updated)
  - `tests/test_writing_core_smoke.py` (updated)
  - `tests/test_writing_core_framework.py` (updated)
  - `docs/writing-core-framework/README.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 10: Fourth Sample + Richer Templates
- **Status:** complete
- Actions taken:
  - 为 `scripts/writing_core_smoke.py` 增加 `历史脑洞` 与 `职场婚恋` 的显式 packaging 模板
  - 发现 `历史脑洞` / `职场婚恋` 仍在走 generic 分支后，先补 RED 测试，再做最小实现
  - 修正 `extract_outline_pitch`，让其跳过 fenced code block
  - 使用 `scripts/writing_core_smoke.py` 在 `projects/我在县衙当杂吏，靠翻旧案升了堂` 上跑 `writeback + save-packaging`
  - 生成：
    - `docs/writing-core-framework/real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-2026-03-24.md`
    - `projects/我在县衙当杂吏，靠翻旧案升了堂/包装/包装方案.md`
  - 将第四条样本挂回 `docs/writing-core-framework/README.md`
  - 将第四条样本纳入 `tests/test_writing_core_framework.py` 回归集合
  - 运行：
    - `python -m unittest tests.test_writing_core_smoke -v`
    - `python -m unittest tests.test_writing_core_framework -v`
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `scripts/writing_core_smoke.py` (updated)
  - `tests/test_writing_core_smoke.py` (updated)
  - `tests/test_writing_core_framework.py` (updated)
  - `docs/writing-core-framework/README.md` (updated)
  - `docs/writing-core-framework/real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-2026-03-24.md` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/包装/包装方案.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 11: Fifth Sample + Wider Bucket Templates
- **Status:** complete
- Actions taken:
  - 为 `scripts/writing_core_smoke.py` 增加 `青春甜宠` 与 `都市脑洞` 的显式 packaging 模板
  - 发现 `职场婚恋` 样本的 `总纲` 里存在 fenced yaml，会把 `书名:` 污染进 packaging synopsis
  - 先补 RED 测试，再修 `extract_outline_pitch`，让它跳过整个 fenced block
  - 使用 `scripts/writing_core_smoke.py` 在 `projects/她升职那天，前上司成了我合租室友` 上跑 `writeback + save-packaging`
  - 生成：
    - `docs/writing-core-framework/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md`
    - `projects/她升职那天，前上司成了我合租室友/包装/包装方案.md`
  - 将第五条样本挂回 `docs/writing-core-framework/README.md`
  - 将第五条样本纳入 `tests/test_writing_core_framework.py` 回归集合
  - 运行：
    - `python -m unittest tests.test_writing_core_smoke -v`
    - `python -m unittest tests.test_writing_core_framework -v`
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `scripts/writing_core_smoke.py` (updated)
  - `tests/test_writing_core_smoke.py` (updated)
  - `tests/test_writing_core_framework.py` (updated)
  - `docs/writing-core-framework/README.md` (updated)
  - `docs/writing-core-framework/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md` (created)
  - `projects/她升职那天，前上司成了我合租室友/包装/包装方案.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 12: Sixth Sample + Batch Entry
- **Status:** complete
- Actions taken:
  - 使用 `scripts/writing_core_smoke.py` 在 `projects/转学第一天，我把校草认成了新来的代课老师` 上跑 `writeback + save-packaging`
  - 生成：
    - `docs/writing-core-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md`
    - `projects/转学第一天，我把校草认成了新来的代课老师/包装/包装方案.md`
  - 新建 `scripts/batch_writing_core_smoke.py`
  - 新建 `tests/test_batch_writing_core_smoke.py`
  - 修复 batch 脚本 import 路径问题，确保它能在测试环境下加载 `writing_core_smoke`
  - 将第六条样本和 batch 入口挂回 `docs/writing-core-framework/README.md`
  - 将第六条样本纳入 `tests/test_writing_core_framework.py` 回归集合
  - 运行：
    - `python -m unittest tests.test_batch_writing_core_smoke tests.test_writing_core_smoke tests.test_writing_core_framework tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `docs/writing-core-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md` (created)
  - `projects/转学第一天，我把校草认成了新来的代课老师/包装/包装方案.md` (created)
  - `scripts/batch_writing_core_smoke.py` (created)
  - `tests/test_batch_writing_core_smoke.py` (created)
  - `docs/writing-core-framework/README.md` (updated)
  - `tests/test_writing_core_framework.py` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 13: Seventh Sample + Batch Summary
- **Status:** complete
- Actions taken:
  - 使用 `scripts/writing_core_smoke.py` 在 `projects/我赔光积蓄那天，系统先把违约金打到了账上` 上跑 `writeback + save-packaging`
  - 生成：
    - `docs/writing-core-framework/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md`
    - `projects/我赔光积蓄那天，系统先把违约金打到了账上/包装/包装方案.md`
  - 扩展 `scripts/batch_writing_core_smoke.py`
    - 新增 `summary_report` 写出能力
  - 扩展 `tests/test_batch_writing_core_smoke.py`
    - 校验 batch `writeback + save-packaging + summary_report`
  - 将第七条样本挂回 `docs/writing-core-framework/README.md`
  - 将第七条样本纳入 `tests/test_writing_core_framework.py` 回归集合
  - 运行：
    - `python -m unittest tests.test_batch_writing_core_smoke tests.test_writing_core_smoke tests.test_writing_core_framework tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `docs/writing-core-framework/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md` (created)
  - `projects/我赔光积蓄那天，系统先把违约金打到了账上/包装/包装方案.md` (created)
  - `scripts/batch_writing_core_smoke.py` (updated)
  - `tests/test_batch_writing_core_smoke.py` (updated)
  - `docs/writing-core-framework/README.md` (updated)
  - `tests/test_writing_core_framework.py` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 14: Palace Sidecar + Repo Batch Baseline
- **Status:** complete
- Actions taken:
  - 为 `scripts/writing_core_smoke.py` 增加 `宫斗宅斗` 显式 packaging 模板
  - 增加 sidecar 保存策略：
    - 若 `包装/包装方案.md` 已存在且非空，则写 `包装/包装方案-writing-core.md`
  - 使用 `scripts/writing_core_smoke.py` 在 `projects/庶妹换我婚书那夜，太子先开了口` 上跑 `writeback + save-packaging`
  - 生成：
    - `docs/writing-core-framework/real-project-smoke-继母换我婚书那夜-太子先开了口-2026-03-24.md`
    - `projects/庶妹换我婚书那夜，太子先开了口/包装/包装方案-writing-core.md`
  - 新建仓库内固定 batch 基线：
    - `docs/writing-core-framework/batch-smoke-manifest.json`
    - `docs/writing-core-framework/batch-output/summary-report.json`
    - 3 个固定 batch output smoke 文件
  - 运行：
    - `python -m unittest tests.test_batch_writing_core_smoke tests.test_writing_core_smoke tests.test_writing_core_framework tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `scripts/writing_core_smoke.py` (updated)
  - `docs/writing-core-framework/real-project-smoke-继母换我婚书那夜-太子先开了口-2026-03-24.md` (created)
  - `projects/庶妹换我婚书那夜，太子先开了口/包装/包装方案-writing-core.md` (created)
  - `docs/writing-core-framework/batch-smoke-manifest.json` (created)
  - `docs/writing-core-framework/batch-output/summary-report.json` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md` (created)
  - `tests/test_writing_core_smoke.py` (updated)
  - `tests/test_batch_writing_core_smoke.py` (updated)
  - `tests/test_writing_core_framework.py` (updated)
  - `docs/writing-core-framework/README.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 15: Batch Aggregation Hardening
- **Status:** complete
- Actions taken:
  - 为 `scripts/batch_writing_core_smoke.py` 增加聚合 summary：
    - `generated_at`
    - `mode`
    - `count / success_count / failure_count`
    - `bucket_counts`
    - `packaging_status_counts`
    - `writeback_status_counts`
    - `failed_projects`
  - 修复 batch 对不存在项目不会失败的问题：
    - 显式要求 `.mighty/state.json` 必须存在
    - 将失败项目写入 `failed_projects`，不中断整批
  - 重跑固定 batch 基线，刷新：
    - `docs/writing-core-framework/batch-output/summary-report.json`
    - 3 条固定 batch smoke 文件
  - 运行：
    - `python -m unittest tests.test_batch_writing_core_smoke tests.test_writing_core_smoke tests.test_writing_core_framework tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `scripts/batch_writing_core_smoke.py` (updated)
  - `tests/test_batch_writing_core_smoke.py` (updated)
  - `docs/writing-core-framework/batch-output/summary-report.json` (updated)
  - `docs/writing-core-framework/README.md` (updated)
  - `tests/test_writing_core_framework.py` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 16: Full Batch Baseline Expansion
- **Status:** complete
- Actions taken:
  - 将 `docs/writing-core-framework/batch-smoke-manifest.json` 从 3 项扩到 8 个代表性 bucket
  - 重跑固定 batch output，刷新：
    - `docs/writing-core-framework/batch-output/summary-report.json`
    - 8 条固定 batch smoke 文件
  - 用 `scripts/writing_core_smoke.py` 跑通 `宫斗宅斗` sidecar 样本并确认 `written-sidecar` 规则进入回归
  - 运行：
    - `python -m unittest tests.test_batch_writing_core_smoke tests.test_writing_core_smoke tests.test_writing_core_framework tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `docs/writing-core-framework/batch-smoke-manifest.json` (updated)
  - `docs/writing-core-framework/batch-output/summary-report.json` (updated)
  - `docs/writing-core-framework/batch-output/real-project-smoke-继母换我婚书那夜-太子先开了口-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md` (created)
  - `docs/writing-core-framework/batch-output/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md` (created)
  - `docs/writing-core-framework/README.md` (updated)
  - `tests/test_writing_core_smoke.py` (updated)
  - `tests/test_batch_writing_core_smoke.py` (updated)
  - `tests/test_writing_core_framework.py` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

## Session: 2026-03-24

### Historical Brainhole Minimal Sample
- **Status:** complete
- **Started:** 2026-03-24 13:46 CST
- Actions taken:
  - 在 `projects/我在县衙当杂吏，靠翻旧案升了堂` 新建最小真实项目目录
  - 按 `novel-init` 约定落下 `.mighty/state.json`、sidecar 文件、主角卡、力量体系、世界观口径、官制真值表与权力层级图
  - 读取 `historical-brainhole` profile，并按 `历史脑洞` bucket 约束生成总纲与第001-003章章纲
  - 写出第001-003章正文，满足“第一章落身份困局和制度压力、第二章机制第一次见效、第三章形成小闭环但不打穿主线”
  - 回写 `state` 的 `progress`、`plot_threads`、`knowledge_base`、`chapter_meta`、`summaries_index`
  - 实际运行 `python3 scripts/setting_gate.py <project_root> --stage init`
  - 实际运行 `python3 scripts/setting_gate.py <project_root> --stage outline`
  - 运行 JSON 校验与 `bash scripts/validate-migration.sh`
- Files created/modified:
  - `docs/superpowers/plans/2026-03-24-historical-brainhole-county-yamen-sample.md` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/state.json` (created/updated)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/learned-patterns.json` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/market-adjustments.json` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/setting-gate.json` (created/updated by script)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/大纲/总纲.md` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/大纲/章纲/第001章.md` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/大纲/章纲/第002章.md` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/大纲/章纲/第003章.md` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/chapters/第001章.md` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/chapters/第002章.md` (created)
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/chapters/第003章.md` (created)
  - `progress.md` (updated)

## Session: 2026-03-24

### Real Project Sample: 豪门总裁最小真实样本
- **Status:** complete
- Actions taken:
  - 新建项目 `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人`
  - 按 `novel-init` 最小骨架创建 `.mighty/`、`大纲/`、`设定集/`、`chapters/`
  - 基于番茄 `豪门总裁` bucket 生成总纲与第001-003章章纲
  - 写出第001-003章正文，锁定“资源压制 + 关系错位 + 高压升级 + 小兑现”链条
  - 首轮 `setting_gate(init|outline)` 因企业权力层级缺失被挡回，补齐 `设定集/官制/官职真值表.md` 与 `设定集/官制/权力层级图.md`
  - 重跑 `python3 scripts/setting_gate.py <project_root> --stage init`
  - 重跑 `python3 scripts/setting_gate.py <project_root> --stage outline`
  - 运行 `wc -m` 确认前三章长度分别为 `2401 / 2484 / 2493`
  - 运行 `python3 scripts/fanqie_p0_smoke.py --project-root <project_root> --chapter 003 --chapters 001-003`，生成该项目的 P0 smoke draft
- Files created/modified:
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/.mighty/state.json` (created/updated)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/.mighty/learned-patterns.json` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/.mighty/market-adjustments.json` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/.mighty/setting-gate.json` (generated)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/大纲/总纲.md` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/大纲/章纲/第001章.md` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/大纲/章纲/第002章.md` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/大纲/章纲/第003章.md` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/chapters/第001章.md` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/chapters/第002章.md` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/chapters/第003章.md` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/设定集/官制/官职真值表.md` (created)
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/设定集/官制/权力层级图.md` (created)
  - `docs/opening-and-plot-framework/real-project-smoke-签下离婚协议那天-冷脸总裁改口叫我合伙人-fanqie-p0-2026-03-24.md` (generated)
  - `progress.md` (updated)

## Session: 2026-03-23 开篇方法与剧情层次规则层

### Phase 1: Discovery & Design Lock
- **Status:** complete
- Actions taken:
  - 读取当前 `task_plan.md`、`findings.md`、`progress.md`
  - 读取 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md`
  - 读取 `docs/90-归档/阶段/phase-9-summary.md`、`docs/90-归档/阶段/phase-17-summary.md`、`docs/fanqie-writing-techniques.md`
  - 读取 `skills/novel-outline/SKILL.md`、`skills/novel-write/SKILL.md`、`skills/novel-review/SKILL.md`、`skills/novel-query/SKILL.md`、`skills/novel-package/SKILL.md`
  - 确认新框架承载层、模块体量与接线范围
  - 写入设计说明与实施计划：
    - `docs/superpowers/specs/2026-03-23-opening-and-plot-framework-design.md`
    - `docs/superpowers/plans/2026-03-23-opening-and-plot-framework.md`
- Files created/modified:
  - `docs/superpowers/specs/2026-03-23-opening-and-plot-framework-design.md` (created)
  - `docs/superpowers/plans/2026-03-23-opening-and-plot-framework.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

## Session: 2026-03-24 Research Candidate Handoff

### Phase 1: Minimal Candidate Handoff
- **Status:** complete
- Actions taken:
  - 新建 `docs/superpowers/plans/2026-03-24-research-candidate-handoff.md`，把最小改动范围固定为 `novel_scan -> research-candidates -> setting_gate`
  - 为 `setting_gate` 增加 `--candidates-file` 和 `load_candidates_file()`，允许从 sidecar 读取 research candidates
  - 为 `novel_scan` 增加 `--emit-research-candidates` / `--research-candidates-file`，并只在保守 truth-gap 条件下写出 `.mighty/research-candidates.json`
  - 将宫斗宅斗下的 `scan-kinship-truth-check` 收成最小候选 `嫡庶婚配真值补证`
  - 更新 `docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md`、`skills/novel-scan/SKILL.md`，明确 candidate-only 边界
  - 运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `docs/superpowers/plans/2026-03-24-research-candidate-handoff.md` (created)
  - `scripts/setting_gate.py` (updated)
  - `scripts/novel_scan.py` (updated)
  - `tests/test_setting_gate.py` (updated)
  - `tests/test_novel_scan.py` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `skills/novel-scan/SKILL.md` (updated)

### Phase 2: Gate Next-Action Closure
- **Status:** complete
- Actions taken:
  - 为 `setting_gate` 增加 `minimal_next_action` 结构化输出，统一返回最小建议动作与命令串
  - 对缺本地 truth source 的阻断结果，路由到 `novel-setting`
  - 对高风险 research candidate 的阻断结果，路由到 `review-sync-queue`
  - 更新 `docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`skills/novel-write/SKILL.md`，让调用侧优先读取 `minimal_next_action`
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `scripts/setting_gate.py` (updated)
  - `tests/test_setting_gate.py` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `skills/novel-write/SKILL.md` (updated)
  - `progress.md` (updated)

### Phase 3: Resume/Status Gate Awareness
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_setting_gate.py`，要求 `novel-resume` / `novel-status` skill 契约显式读取 `.mighty/setting-gate.json` 与 `minimal_next_action`
  - 更新 `skills/novel-resume/SKILL.md`，让恢复逻辑在 gate 未通过时优先暴露 `blocking_gaps / review_items / minimal_next_action`
  - 更新 `skills/novel-status/SKILL.md`，让状态面板把 gate 视为写作 readiness 控制点，而不是只看 chapter/state 进度
  - 更新 `docs/00-当前有效/start-here.md` 中的状态/恢复入口说明，明确 gate 卡住时应优先读 `minimal_next_action`
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `tests/test_setting_gate.py` (updated)
  - `skills/novel-resume/SKILL.md` (updated)
  - `skills/novel-status/SKILL.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `progress.md` (updated)

### Phase 4: Query Gate Awareness
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_setting_gate.py`，要求 `novel-query` skill 契约显式读取 `.mighty/setting-gate.json` 与 `minimal_next_action`
  - 更新 `skills/novel-query/SKILL.md`，支持查询 `setting gate` 状态、`blocking_gaps`、`review_items` 与 `minimal_next_action`
  - 更新 `docs/00-当前有效/start-here.md` 与 `docs/00-当前有效/skill-usage.md`，明确 gate 状态也可以通过 `novel-query` 直接查询
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `tests/test_setting_gate.py` (updated)
  - `skills/novel-query/SKILL.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `progress.md` (updated)

### Phase 5: Gate Prompt UX Alignment
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_setting_gate.py`，要求 `docs/00-当前有效/start-here.md` 与 `docs/00-当前有效/skill-usage.md` 提供统一的 gate-aware `novel-status` / `novel-resume` / `novel-query` 最小提示词
  - 更新 `docs/00-当前有效/start-here.md` 中的状态与恢复入口，把 `novel-status` / `novel-resume` 的示例提示词统一为 gate-aware 版本
  - 更新 `docs/00-当前有效/skill-usage.md` 中的 `status` / `resume` / `query` 示例提示词，统一收成 gate-aware 体验入口
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `tests/test_setting_gate.py` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `progress.md` (updated)

### Phase 6: Gate Triage Main Entry
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_setting_gate.py`，要求 `README.md` 与 `docs/00-当前有效/default-workflows.md` 增加 `Gate Triage` 入口
  - 更新 `README.md`，加入 `novel-scan -> setting gate -> review-sync-queue` 的最小 triage 链和命令示例
  - 更新 `docs/00-当前有效/default-workflows.md`，加入 `Gate Triage` 小节，明确 triage 不是 canon 写入链
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `tests/test_setting_gate.py` (updated)
  - `README.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `progress.md` (updated)

### Phase 7: Gate Triage Guide
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_setting_gate.py`，要求存在独立的 `docs/00-当前有效/gate-triage.md`，且能从 `README.md`、`docs/00-当前有效/default-workflows.md`、`docs/00-当前有效/start-here.md` 找到
  - 新建 `docs/00-当前有效/gate-triage.md`，集中说明 `novel-scan -> setting gate -> review-sync-queue` 的 triage 链、关键字段和最小命令
  - 在 `README.md`、`docs/00-当前有效/default-workflows.md`、`docs/00-当前有效/start-here.md` 中补挂该指南入口
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `tests/test_setting_gate.py` (updated)
  - `docs/00-当前有效/gate-triage.md` (created)
  - `README.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `progress.md` (updated)

### Phase 8: Gate Triage Rollout Summary
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_setting_gate.py`，要求存在独立的 `docs/gate-triage-rollout-2026-03-24.md`，并能从 `README.md` 找到
  - 新建 `docs/gate-triage-rollout-2026-03-24.md`，把本轮改动沉成独立历史记录
  - 更新 `README.md`，在 Gate Triage 区和参考文档区补挂 rollout 总结入口
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `tests/test_setting_gate.py` (updated)
  - `docs/gate-triage-rollout-2026-03-24.md` (created)
  - `README.md` (updated)
  - `progress.md` (updated)

### Phase 9: Maintenance-Mode Alignment
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_setting_gate.py`，要求 `docs/00-当前有效/v1-maintenance-mode.md` 明确把 gate triage 归档为默认工作流维护的一部分
  - 更新 `docs/00-当前有效/v1-maintenance-mode.md`，把 `setting gate` 卡住后的 triage 体验问题列为默认主线修复示例，并补挂 `gate-triage.md`
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `tests/test_setting_gate.py` (updated)
  - `docs/00-当前有效/v1-maintenance-mode.md` (updated)
  - `progress.md` (updated)

### Phase 10: Redundancy Cleanup
- **Status:** complete
- Actions taken:
  - 审计 `gate triage` 相关入口，确认最大冗余点在 `README.md` 的摘要段与独立指南重复
  - 将 `README.md` 的 Gate Triage 区收成摘要层，只保留最小链路、核心字段与文档入口
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `README.md` (updated)
  - `progress.md` (updated)

### Phase 11: Roadmap Classification Cleanup
- **Status:** complete
- Actions taken:
  - 审计 `v1.1-roadmap.md`，确认 `gate triage` 不应被误读成 `v1.1` 新主线候选
  - 更新 `docs/00-当前有效/v1.1-roadmap.md`，明确 `setting gate` 的 triage / recovery 收口属于 `v1.0.x` 默认主线稳定化，而不是 `v1.1` 新能力方向
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `docs/00-当前有效/v1.1-roadmap.md` (updated)
  - `progress.md` (updated)

### Phase 12: Current-Facing Doc Alignment
- **Status:** complete
- Actions taken:
  - 对 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md` 做当前入口一致性抽查
  - 修正 `docs/00-当前有效/skill-usage.md` 中 `novel-status` gate-aware 提示词表述，使其与 `docs/00-当前有效/start-here.md` 保持一致
  - 在 `docs/00-当前有效/skill-usage.md` 的 gate 使用说明段补挂 `gate-triage.md` 入口，减少“先看哪里”的歧义
  - 再次运行 `python3 -m unittest tests.test_acquire_source_text tests.test_setting_gate tests.test_novel_scan -v`，确认通过
- Files created/modified:
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `progress.md` (updated)

### Phase 2: Red Test
- **Status:** complete
- Actions taken:
  - 新增 `tests/test_opening_plot_framework.py`，用于校验新框架文件、skill 接线、入口文档暴露与 state schema 评分键说明
  - 运行 `python -m unittest tests.test_opening_plot_framework -v`
  - 确认在实现前按预期失败：
    - 新框架目录不存在
    - 5 个 skill 尚未引用新文档
    - 入口文档未暴露新框架
    - state schema 尚未记录新评分键
- Files created/modified:
  - `tests/test_opening_plot_framework.py` (created)

### Phase 3: Framework Docs
- **Status:** complete
- Actions taken:
  - 新建 `docs/opening-and-plot-framework/README.md`
  - 新建 6 个主模块，覆盖开篇目标、构件公式、故障修正、剧情层次、推进链与题材特化接口
- Files created/modified:
  - `docs/opening-and-plot-framework/README.md` (created)
  - `docs/opening-and-plot-framework/01-开篇目标与成功标准.md` (created)
  - `docs/opening-and-plot-framework/02-开篇构件与组合公式.md` (created)
  - `docs/opening-and-plot-framework/03-开篇故障与修正.md` (created)
  - `docs/opening-and-plot-framework/04-剧情层次模型.md` (created)
  - `docs/opening-and-plot-framework/05-推进链与残账设计.md` (created)
  - `docs/opening-and-plot-framework/06-题材特化接口.md` (created)

### Phase 4: Skill Wiring
- **Status:** complete
- Actions taken:
  - 为 `novel-outline` 增加开篇承诺、前三章兑现路径、主推进线与残账读取规则
  - 为 `novel-write` 增加开篇故障防护、层次清晰度和推进账本约束
  - 为 `novel-review` 增加开篇抓力、层次清晰度和推进有效性审查点
  - 为 `novel-precheck` 增加黄金三章、主线/次级线与推进残账预检
  - 为 `novel-package` 增加开篇 promise 与正文承载力对齐规则
- Files created/modified:
  - `skills/novel-outline/SKILL.md` (updated)
  - `skills/novel-write/SKILL.md` (updated)
  - `skills/novel-review/SKILL.md` (updated)
  - `skills/novel-precheck/SKILL.md` (updated)
  - `skills/novel-package/SKILL.md` (updated)

### Phase 5: Entry Docs & State Contract
- **Status:** complete
- Actions taken:
  - 在 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md` 暴露新框架入口
  - 在 `shared/references/shared/state-schema.md` 与 `shared/templates/state-v5-template.json` 中补充 `开篇抓力 / 层次清晰度 / 推进有效性`
- Files created/modified:
  - `README.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `shared/references/shared/state-schema.md` (updated)
  - `shared/templates/state-v5-template.json` (updated)

### Phase 6: Verification & Delivery
- **Status:** complete
- Actions taken:
  - 重新运行 `python -m unittest tests.test_opening_plot_framework -v`，结果 `OK`
  - 运行 `bash scripts/validate-migration.sh`，结果 `Migration validation passed`
  - 回写 `task_plan.md`、`findings.md`、`progress.md`
- Files created/modified:
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 7: Fanqie Priority Overlays
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_opening_plot_framework.py`，先为番茄优先分类清单和 P0 overlay 骨架加红灯断言
  - 运行 `python -m unittest tests.test_opening_plot_framework -v`，确认新增文档和 skill 读取路径在实现前失败
  - 新建 `docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
  - 新建 `docs/opening-and-plot-framework/fanqie-p0-overlays/README.md`
  - 新建 8 张番茄 P0 特化卡：
    - `宫斗宅斗`
    - `职场婚恋`
    - `青春甜宠`
    - `豪门总裁`
    - `都市日常`
    - `玄幻脑洞`
    - `都市脑洞`
    - `历史脑洞`
  - 更新 `docs/opening-and-plot-framework/README.md` 与 `06-题材特化接口.md`
  - 为 `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` 增加：
    - `fanqie-priority-categories-2026-03.md`
    - `fanqie-p0-overlays/<bucket>.md`
    的条件读取路径
  - 重新运行 `python -m unittest tests.test_opening_plot_framework -v`，结果 `OK`
  - 重新运行 `bash scripts/validate-migration.sh`，结果 `Migration validation passed`
- Files created/modified:
  - `tests/test_opening_plot_framework.py` (updated)
  - `docs/opening-and-plot-framework/README.md` (updated)
  - `docs/opening-and-plot-framework/06-题材特化接口.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/README.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/宫斗宅斗.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/职场婚恋.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/青春甜宠.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/豪门总裁.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/都市日常.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/玄幻脑洞.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/都市脑洞.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/历史脑洞.md` (created)
  - `skills/novel-outline/SKILL.md` (updated)
  - `skills/novel-write/SKILL.md` (updated)
  - `skills/novel-review/SKILL.md` (updated)
  - `skills/novel-precheck/SKILL.md` (updated)
  - `skills/novel-package/SKILL.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 8: Fanqie P0 Medium-Depth Cards
- **Status:** complete
- Actions taken:
  - 读取 8 张现有 overlay，以及对应的 `shared/templates/genres/*.md` / `shared/profiles/*/profile*.yaml`
  - 扩展 `tests/test_opening_plot_framework.py`，要求 8 张 P0 卡必须包含：
    - `开篇公式`
    - `黄金三章最低要求`
    - `高频故障清单`
    - `precheck 专项检查点`
  - 运行测试并确认新增结构断言在实现前失败
  - 将 8 张 P0 卡统一升级成中等深度版，并保留 `剧情层次重点`
  - 更新 `docs/opening-and-plot-framework/fanqie-p0-overlays/README.md`
  - 重新运行 `python -m unittest tests.test_opening_plot_framework -v`，结果 `OK`
  - 重新运行 `bash scripts/validate-migration.sh`，结果 `Migration validation passed`
- Files created/modified:
  - `tests/test_opening_plot_framework.py` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/README.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/宫斗宅斗.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/职场婚恋.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/青春甜宠.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/豪门总裁.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/都市日常.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/玄幻脑洞.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/都市脑洞.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/历史脑洞.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 9: Fanqie P0 Checkcards
- **Status:** complete
- Actions taken:
  - 读取 `docs/gongdou-zhaidou-fault-funnel-review-card.md`，确认现有 bucket 级专项卡模式
  - 扩展 `tests/test_opening_plot_framework.py`，要求新增：
    - `fanqie-p0-checkcards/` 目录与 8 张卡
    - `novel-review` / `novel-precheck` 的新读取路径
    - 8 张卡的统一结构
  - 运行测试并确认在实现前失败
  - 新建 `docs/opening-and-plot-framework/fanqie-p0-checkcards/README.md`
  - 为 8 类新增专项检查卡，统一覆盖：
    - `自动触发范围`
    - `对 novel-review`
    - `对 novel-precheck`
    - `核心检查问题`
    - `红灯判定`
  - 更新 `docs/opening-and-plot-framework/README.md` 与 `fanqie-p0-overlays/README.md`
  - 更新 `skills/novel-review/SKILL.md` / `skills/novel-precheck/SKILL.md`
  - 重新运行 `python -m unittest tests.test_opening_plot_framework -v`，结果 `OK`
  - 重新运行 `bash scripts/validate-migration.sh`，结果 `Migration validation passed`
- Files created/modified:
  - `tests/test_opening_plot_framework.py` (updated)
  - `docs/opening-and-plot-framework/README.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/README.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/README.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/宫斗宅斗.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/职场婚恋.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/青春甜宠.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/豪门总裁.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/都市日常.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/玄幻脑洞.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/都市脑洞.md` (created)
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/历史脑洞.md` (created)
  - `skills/novel-review/SKILL.md` (updated)
  - `skills/novel-precheck/SKILL.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 10: Fanqie P0 Output Contract
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_opening_plot_framework.py`，要求：
    - 新增 `fanqie-p0-output-contract.md`
    - `novel-review` 包含 `fanqie_bucket_review_summary`
    - `novel-precheck` 包含 `fanqie_bucket_precheck_summary`
    - `state-schema` 包含 `fanqie_bucket_flags / fanqie_bucket_summary`
  - 运行测试并确认在实现前失败
  - 新建 `docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
  - 更新 `docs/opening-and-plot-framework/README.md`
  - 更新 `shared/references/shared/state-schema.md` 与 `shared/templates/state-v5-template.json`
  - 更新 `skills/novel-review/SKILL.md` / `skills/novel-precheck/SKILL.md`
  - 重新运行 `python -m unittest tests.test_opening_plot_framework -v`，结果 `OK`
  - 重新运行 `bash scripts/validate-migration.sh`，结果 `Migration validation passed`
- Files created/modified:
  - `tests/test_opening_plot_framework.py` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-output-contract.md` (created)
  - `docs/opening-and-plot-framework/README.md` (updated)
  - `shared/references/shared/state-schema.md` (updated)
  - `shared/templates/state-v5-template.json` (updated)
  - `skills/novel-review/SKILL.md` (updated)
  - `skills/novel-precheck/SKILL.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 11: Real Project Smoke
- **Status:** complete
- Actions taken:
  - 读取 `projects/庶女谋略/.mighty/state.json`
  - 读取总纲与第001-003章章纲 / 正文
  - 基于真实项目手工生成一版 `fanqie_bucket_review_summary`
  - 基于真实项目手工生成一版 `fanqie_bucket_precheck_summary`
  - 新建只读 smoke 文档，记录判断依据与结论，不直接写回活项目 state
- Files created/modified:
  - `docs/opening-and-plot-framework/real-project-smoke-shunvmoulue-fanqie-p0-2026-03-23.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 12: Real Project Writeback
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_opening_plot_framework.py`，要求 `projects/庶女谋略/.mighty/state.json` 中存在：
    - `chapter_meta["003"].fanqie_bucket_flags`
    - `chapter_meta["003"].fanqie_bucket_summary.bucket = 宫斗宅斗`
  - 运行测试并确认在写回前失败
  - 将 `第003章` 的轻量 bucket 样本真实写回 `projects/庶女谋略/.mighty/state.json`
  - 更新 `real-project-smoke-shunvmoulue-fanqie-p0-2026-03-23.md`，把样本结论从“只读验证”改成“轻量写回样本验证”
  - 重新运行 `python -m unittest tests.test_opening_plot_framework -v`，结果 `OK`
  - 重新运行 `bash scripts/validate-migration.sh`，结果 `Migration validation passed`
  - 额外用 JSON 读取确认：
    - `fanqie_bucket_summary.bucket = 宫斗宅斗`
    - `fanqie_bucket_flags = []`
- Files created/modified:
  - `tests/test_opening_plot_framework.py` (updated)
  - `projects/庶女谋略/.mighty/state.json` (updated)
  - `docs/opening-and-plot-framework/real-project-smoke-shunvmoulue-fanqie-p0-2026-03-23.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 13: Reusable Smoke Template
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_opening_plot_framework.py`，要求：
    - `fanqie-p0-smoke-template.md` 存在
    - `docs/opening-and-plot-framework/README.md` 能发现该模板入口
    - 模板包含可复用的固定章节结构
  - 运行测试并确认在实现前失败
  - 新建 `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`
  - 更新 `docs/opening-and-plot-framework/README.md`
  - 重新运行 `python -m unittest tests.test_opening_plot_framework -v`，结果 `OK`
  - 重新运行 `bash scripts/validate-migration.sh`，结果 `Migration validation passed`
- Files created/modified:
  - `tests/test_opening_plot_framework.py` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md` (created)
  - `docs/opening-and-plot-framework/README.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 14: Cross-Project Smoke
- **Status:** complete
- Actions taken:
  - 读取 `projects/庶妹换我婚书那夜，太子先开了口/.mighty/state.json`
  - 读取该项目总纲与第001-003章章纲 / 正文
  - 基于 `fanqie-p0-smoke-template.md` 生成第二份真实项目 smoke
  - 新建 `real-project-smoke-hunshu-taizi-fanqie-p0-2026-03-23.md`
  - 保持本轮为只读 smoke，不改第二个项目 state
  - 重新运行 `python -m unittest tests.test_opening_plot_framework -v`，结果 `OK`
  - 重新运行 `bash scripts/validate-migration.sh`，结果 `Migration validation passed`
- Files created/modified:
  - `docs/opening-and-plot-framework/real-project-smoke-hunshu-taizi-fanqie-p0-2026-03-23.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 15: Smoke Tool Design
- **Status:** complete
- Actions taken:
  - 基于当前框架、真实样本与模板，收束“二合一 smoke 工具”的设计
  - 明确默认模式为 `draft`
  - 明确默认禁止 `writeback`
  - 新建设计文档：
    - `docs/superpowers/specs/2026-03-23-fanqie-p0-smoke-tool-design.md`
- Files created/modified:
  - `docs/superpowers/specs/2026-03-23-fanqie-p0-smoke-tool-design.md` (created)
  - `progress.md` (updated)

### Phase 16: Smoke Tool Implementation Planning
- **Status:** complete
- Actions taken:
  - 读取 `fanqie-p0-smoke-tool-design.md`
  - 对照 `tests/test_novel_scan.py` 与 `scripts/novel_scan.py` 的脚本/测试风格
  - 写出实现计划：
    - `docs/superpowers/plans/2026-03-23-fanqie-p0-smoke-tool.md`
- Files created/modified:
  - `docs/superpowers/plans/2026-03-23-fanqie-p0-smoke-tool.md` (created)
  - `task_plan.md` (updated)
  - `progress.md` (updated)

### Phase 17: Smoke Tool V1 Implementation
- **Status:** complete
- Actions taken:
  - 新建 `tests/test_fanqie_p0_smoke.py`
  - 按 TDD 依次补红灯与绿灯：
    - CLI 默认模式 / 显式模式 / bucket 推断 / 写回护栏
    - helper：`load_state` / `normalize_chapter_key` / `slugify_project_title` / `default_output_path`
    - `scaffold` 模式
    - `draft` 模式
    - `writeback` 模式
  - 新建并实现 `scripts/fanqie_p0_smoke.py`
  - 更新 `docs/opening-and-plot-framework/README.md`
  - 更新 `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`
  - 运行：
    - `python -m unittest tests.test_fanqie_p0_smoke -v`
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
  - 试跑：
    - `python3 scripts/fanqie_p0_smoke.py --project-root "projects/庶女谋略" --chapter 003 --chapters 001-003 --output /tmp/fanqie-p0-shunv-smoke.md`
    - `python3 scripts/fanqie_p0_smoke.py --project-root "projects/庶妹换我婚书那夜，太子先开了口" --chapter 003 --chapters 001-003 --output /tmp/fanqie-p0-hunshu-smoke.md`
- Files created/modified:
  - `tests/test_fanqie_p0_smoke.py` (created)
  - `scripts/fanqie_p0_smoke.py` (created)
  - `docs/opening-and-plot-framework/README.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 18: Smoke Tool V1.1
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_fanqie_p0_smoke.py`，增加：
    - `confidence`
    - `evidence_count`
    - `evidence_sources`
    - `writeback_preview`
    - `load_sidecars`
    - 非 `宫斗宅斗` P0 bucket 的保守 `draft`
  - 先运行红灯，确认新增能力缺失时测试失败
  - 更新 `scripts/fanqie_p0_smoke.py`：
    - 新增 `load_sidecars`
    - 读取本地 `market-adjustments.json` / `learned-patterns.json`
    - 为 `draft` 输出补 `confidence / evidence_count / evidence_sources`
    - 新增 `writeback_preview`
    - 对其它 P0 bucket 提供低置信 `draft`
  - 更新：
    - `docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
    - `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`
  - 运行：
    - `python -m unittest tests.test_fanqie_p0_smoke -v`
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `bash scripts/validate-migration.sh`
  - 试跑：
    - `projects/庶女谋略`
    - `projects/庶妹换我婚书那夜，太子先开了口`
- Files created/modified:
  - `scripts/fanqie_p0_smoke.py` (updated)
  - `tests/test_fanqie_p0_smoke.py` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-output-contract.md` (updated)
  - `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 19: Pressure Matrix
- **Status:** complete
- Actions taken:
  - 批量运行 `fanqie_p0_smoke.py` 于：
    - `projects/庶女谋略`
    - `projects/庶妹换我婚书那夜，太子先开了口`
    - `smoke/e2e-tianchong`
    - `smoke/e2e-tianchong-evil`
    - `smoke/e2e-qinggan-evil-antiflattening-20260322`
    - `smoke/e2e-dual-substitute-evil-antiflattening-20260322`
    - `smoke/e2e-system-antiflattening-20260322`
  - 汇总结果：
    - 两个 `宫斗宅斗` 项目输出 `draft`
    - 两个 `现言甜宠` 代理样本在 alias 后输出 `draft`
    - 一个 `现言甜宠` 代理样本因证据不足降级为 `scaffold-only`
    - 两个非 P0 样本保守降级为 `scaffold-only`
  - 新建结果文档：
    - `docs/opening-and-plot-framework/fanqie-p0-pressure-results-2026-03-24.md`
  - 更新 `docs/opening-and-plot-framework/README.md`
- Files created/modified:
  - `docs/opening-and-plot-framework/fanqie-p0-pressure-results-2026-03-24.md` (created)
  - `docs/opening-and-plot-framework/README.md` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 20: Real P0 Project Validation
- **Status:** complete
- Actions taken:
  - 读取 `projects/转学第一天，我把校草认成了新来的代课老师` 的 state、总纲、前 1-3 章
  - 读取 `projects/公司裁我那天，系统先赔了我一百万` 的 state、总纲、前 1-3 章
  - 对两个真实项目分别运行：
    - `python3 scripts/fanqie_p0_smoke.py --project-root "<project_root>" --chapter 003 --chapters 001-003`
  - 新增两份真实项目 smoke 文档：
    - `real-project-smoke-转学第一天-我把校草认成了新来的代课老师-fanqie-p0-2026-03-24.md`
    - `real-project-smoke-公司裁我那天-系统先赔了我一百万-fanqie-p0-2026-03-24.md`
  - 确认两条线都稳定输出：
    - `fanqie_bucket_review_summary`
    - `fanqie_bucket_precheck_summary`
    - `confidence`
    - `evidence_count`
    - `signals_used`
    - `writeback_preview`
  - 初始结论：
    - `青春甜宠` 真实项目：可稳定进入 `draft`
    - `都市脑洞` 真实项目：可稳定进入 `draft`
  - 后续同日已继续收紧到：
    - `青春甜宠`：`medium confidence`, `pass / fit`
    - `都市脑洞`：`medium confidence`, `warn / fit`
- Files created/modified:
  - `docs/opening-and-plot-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-fanqie-p0-2026-03-24.md` (created)
  - `docs/opening-and-plot-framework/real-project-smoke-公司裁我那天-系统先赔了我一百万-fanqie-p0-2026-03-24.md` (created)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

### Phase 21: Third Real Writeback Sample
- **Status:** complete
- Actions taken:
  - 扩展 `tests/test_opening_plot_framework.py`，要求 `都市脑洞` 真实项目的 `chapter_meta["003"]` 存在 `fanqie_bucket_summary.bucket = 都市脑洞`
  - 运行红灯，确认写回前测试失败
  - 将 `projects/公司裁我那天，系统先赔了我一百万/.mighty/state.json` 中：
    - `chapter_meta["003"].fanqie_bucket_summary.bucket = 都市脑洞`
    - `bucket_grade = warn`
    - 其余保持轻量
  - 更新对应 smoke 文档，明确这是一条中置信轻量写回样本
  - 运行：
    - `python -m unittest tests.test_opening_plot_framework -v`
    - `python -m unittest tests.test_fanqie_p0_smoke -v`
    - `bash scripts/validate-migration.sh`
  - 额外确认：
    - `fanqie_bucket_summary.bucket = 都市脑洞`
    - `fanqie_bucket_summary.bucket_grade = warn`
- Files created/modified:
  - `projects/公司裁我那天，系统先赔了我一百万/.mighty/state.json` (updated)
  - `docs/opening-and-plot-framework/real-project-smoke-公司裁我那天-系统先赔了我一百万-fanqie-p0-2026-03-24.md` (updated)
  - `tests/test_opening_plot_framework.py` (updated)
  - `task_plan.md` (updated)
  - `findings.md` (updated)
  - `progress.md` (updated)

## Session: 2026-03-23

### Out-of-band Maintenance: novel-scan 信任边界与文档口径校正
- **Status:** complete
- Actions taken:
  - 为 `scripts/novel_scan.py` 增加回归测试，覆盖低可信 `project-annotate` 禁止写回、`report-only` 清理陈旧 sidecar、以及番茄总榜 query 变体过滤
  - 收紧 `project-annotate` 写回门槛，仅在当前结果达到中高可信时写 `.mighty/market-adjustments.json` 与 `state.json` 轻量摘要
  - 修复 `report-only` 模式下遗留 `market_adjustments` sidecar/state 的陈旧数据问题
  - 修复番茄总榜 URL 带 query string 时未被排除、进而污染 tag 推断的问题
  - 对齐 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/90-归档/阶段/phase-7a-scan-contract.md`、`docs/fanqie-content-data-layer.md` 与 `skills/novel-scan/SKILL.md` 的实验态与写回边界说明
- Verification:
  - `python3 -m pytest -q tests/test_novel_scan.py`
  - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `scripts/novel_scan.py` (updated)
  - `tests/test_novel_scan.py` (updated)
  - `skills/novel-scan/SKILL.md` (updated)
  - `docs/90-归档/阶段/phase-7a-scan-contract.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/fanqie-content-data-layer.md` (updated)
  - `README.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `progress.md` (updated)

### Out-of-band Prototype: 番茄私有码位字体映射
- **Status:** complete
- Actions taken:
  - 新建 `scripts/prototype_fanqie_font_map.py`，把番茄子集字体去混淆原型收成独立脚本，不污染 `novel_scan` 主逻辑
  - 为原型补最小测试，覆盖私有码位提取、唯一签名解映射、近似候选排序、建议映射门槛
  - 实测确认番茄榜单页是自定义 webfont 私有码位混淆，不是普通编码错误
  - 实测确认 exact glyph hash 不足以直接命中，但基于归一化轮廓片段的近似匹配可把样例中的 ` /  /  / ` 分别推到 `天 / 三 / 生 / 无`
  - 通过原型样例得到建议解码：`天渊 沐潇三生 无系统`
- Verification:
  - `python3 -m pytest -q tests/test_novel_scan.py tests/test_fanqie_font_map_prototype.py`
  - `bash scripts/validate-migration.sh`
- Files created/modified:
  - `scripts/prototype_fanqie_font_map.py` (created)
  - `tests/test_fanqie_font_map_prototype.py` (created)
  - `progress.md` (updated)

## Session: 2026-03-23

### Workflow Tuning: 章节修订单章收敛模式
- **Status:** complete
- Actions taken:
  - 将 `docs/00-当前有效/default-workflows.md` 的正文生产主线调整为“review -> 单章收敛修订轮 -> 单次复审”
  - 更新 `skills/novel-review/SKILL.md`，要求默认把问题收成 1-3 个 issue clusters，并在两轮修订未收口时升级 `novel-rewrite`
  - 更新 `skills/novel-fix/SKILL.md`，要求一次修订轮尽量收口同章局部问题，并吸收顺手可做的轻量措辞修补
  - 更新 `skills/novel-polish/SKILL.md`，要求默认使用单次 `all` 向润色，不再鼓励多轮微修
  - 更新 `docs/00-当前有效/skill-usage.md` 的推荐顺序与示例提示词，使新工作流可直接照抄执行
  - 运行 `bash scripts/validate-migration.sh`，确认结构校验通过
- Files created/modified:
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `skills/novel-review/SKILL.md` (updated)
  - `skills/novel-fix/SKILL.md` (updated)
  - `skills/novel-polish/SKILL.md` (updated)
  - `progress.md` (updated)

### Workflow Tuning: `novel-close` 单章收口轮
- **Status:** complete
- Actions taken:
  - 新建 `skills/novel-close/SKILL.md`，固化 `review -> 单一路由 -> re-review` 契约
  - 新建 `skills/novel-close/agents/openai.yaml`
  - 更新 `scripts/install-skills.sh`，为 `novel-close` 创建 plain / genm 双别名
  - 更新 `scripts/validate-migration.sh`，把 `novel-close` 纳入迁移结构校验
  - 更新 `shared/references/shared/state-schema.md` 与 `shared/templates/state-v5-template.json`，补充 `last_close_*` 轻量字段
  - 更新 `README.md`、`docs/00-当前有效/default-workflows.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/start-here.md`，把 `novel-close` 挂进默认正文生产入口
  - 更新 `skills/novel-write/SKILL.md`、`skills/novel-review/SKILL.md`、`skills/novel-polish/SKILL.md`、`skills/novel-fix/SKILL.md`，对齐新收口轮的相邻提示
  - 运行迁移结构校验和技能安装校验，确认新 skill 可发现、可安装
- Files created/modified:
  - `skills/novel-close/SKILL.md` (created)
  - `skills/novel-close/agents/openai.yaml` (created)
  - `scripts/install-skills.sh` (updated)
  - `scripts/validate-migration.sh` (updated)
  - `shared/references/shared/state-schema.md` (updated)
  - `shared/templates/state-v5-template.json` (updated)
  - `README.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `skills/novel-write/SKILL.md` (updated)
  - `skills/novel-review/SKILL.md` (updated)
  - `skills/novel-polish/SKILL.md` (updated)
  - `skills/novel-fix/SKILL.md` (updated)
  - `progress.md` (updated)

### Workflow Tuning: `novel-write` 默认守卫式自动收口
- **Status:** complete
- Actions taken:
  - 更新 `skills/novel-write/SKILL.md`，新增 `skip_close` 输入与单章写作后的 guarded auto-close 契约
  - 更新 `skills/novel-close/SKILL.md`，明确其是 `novel-write` 的 post-write handoff 执行器
  - 更新 `README.md`、`docs/00-当前有效/default-workflows.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`
    - 单章 `novel-write` 默认会守卫式自动尝试一次 `novel-close`
    - `novel-batch` 不继承该默认行为
    - 显式传 `skip_close=true` 可跳过
  - 进行边界核查：
    - `skills/novel-batch/SKILL.md` 未引入 auto-close
    - `scripts/post-task-maintenance.py` 未引入 prose mutation
  - 运行 `bash scripts/validate-migration.sh`，确认结构校验通过
- Files created/modified:
  - `skills/novel-write/SKILL.md` (updated)
  - `skills/novel-close/SKILL.md` (updated)
  - `README.md` (updated)
  - `docs/00-当前有效/default-workflows.md` (updated)
  - `docs/00-当前有效/start-here.md` (updated)
  - `docs/00-当前有效/skill-usage.md` (updated)
  - `progress.md` (updated)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| 计划文件创建 | 项目根存在 `task_plan.md` / `findings.md` / `progress.md` | 三个文件创建成功 | 成功 | ✓ |
| 迁移结构校验 | `bash scripts/validate-migration.sh` | 校验通过 | `Migration validation passed` | ✓ |
| 模块文件存在性 | 检查 `docs/anti-flattening-framework/` 下 12 模块 + `README` | 全部存在 | `missing=none` | ✓ |
| state 模板可解析 | `python3` 加载 `shared/templates/state-v5-template.json` | JSON 合法 | `state-v5-template.json: ok` | ✓ |
| 真实 smoke state 可解析 | `python3` 加载副本 `.mighty/state.json` | JSON 合法 | `smoke state json: ok` | ✓ |
| 二轮压章一致性 | 比对副本第007章正文实际字数与 `chapter_meta["7"].word_count` | 两者一致 | `3071 / 3071` | ✓ |
| 双女主副本 state 可解析 | `python3` 加载双女主副本 `.mighty/state.json` | JSON 合法 | `dual smoke state json: ok` | ✓ |
| 双女主副本字数一致性 | 比对副本第006章正文实际字数与 `chapter_meta["6"].word_count` | 两者一致 | `4199 / 4199` | ✓ |
| 现实情感副本 state 可解析 | `python3` 加载现实情感副本 `.mighty/state.json` | JSON 合法 | `qinggan state json: ok` | ✓ |
| 现实情感副本字数一致性 | 比对副本第004章正文实际字数与 `chapter_meta["4"].word_count` | 两者一致 | `4209 / 4209` | ✓ |
| 系统副本 state 可解析 | `python3` 加载系统副本 `.mighty/state.json` | JSON 合法 | `system smoke state json: ok` | ✓ |
| 系统副本字数一致性 | 比对副本第004章正文实际字数与 `chapter_meta["4"].word_count` | 两者一致 | `3525 / 3525` | ✓ |
| `novel-close` 迁移结构校验 | `bash scripts/validate-migration.sh` | 校验通过 | `Migration validation passed` | ✓ |
| `novel-close` 安装脚本校验 | `bash scripts/install-skills.sh` | 安装成功 | `Installed Genm-codex skills into /Users/arm/.codex/skills` | ✓ |
| `novel-close` 本地链接存在性 | `ls -l ~/.codex/skills | rg "novel-close|genm-novel-close"` | 两个链接均存在 | `novel-close` / `genm-novel-close` symlink ok | ✓ |
| `novel-write` auto-close 迁移结构校验 | `bash scripts/validate-migration.sh` | 校验通过 | `Migration validation passed` | ✓ |
| `novel-batch` 边界检查 | `rg -n "novel-close|auto-close|skip_close" skills/novel-batch/SKILL.md` | 无匹配 | `exit 1 (no matches)` | ✓ |
| 维护链边界检查 | `rg -n "novel-close|auto-close" scripts/post-task-maintenance.py` | 无匹配 | `exit 1 (no matches)` | ✓ |

## Error Log
| Timestamp | Error | Attempt | Resolution |
|-----------|-------|---------|------------|
| 2026-03-22 17:49 | 无历史 session catchup 输出 | 1 | 视为无待恢复上下文，继续初始化本次计划 |
| 2026-03-22 18:13 | 仓库存在大量无关改动 | 1 | 仅在目标文档和技能文件中局部修改，不回滚其他改动 |

## 5-Question Reboot Check
| Question | Answer |
|----------|--------|
| Where am I? | 所有执行阶段已完成，等待交付 |
| Where am I going? | 向用户交付 `P0/P1/P2`、四类样本真实链路 smoke 和跨流派交叉验证结果 |
| What's the goal? | 在仓库内落成反脸谱化体系并把它接进默认写作质量链 |
| What have I learned? | 已确认这套规则可以以轻量 state 约定和项目内案例方式稳定延伸 |
| What have I done? | 已完成 12 模块、5 个主链 skill 接线、state 约定、案例扩编、四类样本真实链路 smoke 与跨流派交叉验证 |

---
*Update after completing each phase or encountering errors*

## Session Update: 2026-03-22 18:40

- 已完成“推进不能太顺”工程阶段的系统改造：
  - `core-constraints` 上收
  - Fanqie 覆盖层收口
  - 主链技能接入
  - shared profile 通用字段补齐
  - 全部 genre 模板补齐“推进阻力与代价”
  - 跨流派回归验证完成
- 已完成真实项目章纲重生验证：
  - `projects/庶妹换我婚书那夜，太子先开了口/大纲/章纲/第002章.md`
  - `projects/庶妹换我婚书那夜，太子先开了口/大纲/章纲/第003章.md`
- 已开始执行分流矩阵第一档对象：
  - `smoke/e2e-gongdou-evil`
  - 已重生章纲：
    - `第002章.md`
    - `第003章.md`
    - `第004章.md`
    - `第005章.md`
    - `第006章.md`
- 已并行推进第二个第一档对象：
  - `smoke/e2e-dual-substitute-evil`
  - 已重生章纲：
    - `第002章.md`
    - `第003章.md`

## Session Update: 2026-03-22 23:20

- 已新增 `宫斗宅斗` bucket 专用的故障漏斗判定卡：
  - `docs/gongdou-zhaidou-fault-funnel-review-card.md`
- 已将该判定卡自动接入：
  - `skills/novel-review/SKILL.md`
  - `skills/novel-write/SKILL.md`
- 当前行为约定：
  - `novel-review` 在 active bucket 为 `宫斗宅斗` 时强制先跑故障漏斗
  - `novel-write` 在 active bucket 为 `宫斗宅斗` 时先做轻量漏斗预检
- 已更新使用文档：
  - `docs/00-当前有效/skill-usage.md`

- 当前判断：
  - 这条线的正文后续更适合 `rewrite`
  - 不建议继续直接补第4-5章正文

## Session Update: 2026-03-22 11:05

- 已为 `smoke/e2e-dual-substitute-evil` 补齐第004章章纲：
  - `大纲/章纲/第004章.md`
- 已写出第004章正文：
  - `chapters/第004章.md`
  - 本章定位为“发布会后的第一轮反扑”，强调：
    - 贺氏立即反扑并收走解释权
    - 双女主第一次明显不对齐
    - 证据只推进到 `B-17` 借阅路径，不直接打穿主线
- 已回写 `smoke/e2e-dual-substitute-evil/.mighty/state.json`：
  - `progress.current_chapter = 4`
  - `progress.total_words = 12688`
  - 新增 `chapter_meta[4]`
  - 新增 `chapter_snapshots[4]`
  - 新增 `summaries_index[4]`
- 当前这条 smoke 已可自然续写第005章，但更稳的下一步是先对第004章做一轮 `novel-review`，确认“同盟裂口 + 借阅记录线”有没有压准。

## Session Update: 2026-03-22 11:15

- 已完成 `smoke/e2e-dual-substitute-evil` 第004章 review：
  - 第004章评为可继续推进，无结构级返工点
  - review 元数据已回写到 `.mighty/state.json`
- 已补齐第005章章纲：
  - `大纲/章纲/第005章.md`
  - 本章把 `B-17` 从借阅痕迹推进到外部执行人 `闻策咨询 / 应岚`
- 已写出第005章正文：
  - `chapters/第005章.md`
  - 本章同步落下两层代价：
    - `姜栀` 被公开往“偷档报复”上挂
    - `双女主` 同盟仍维持交易态，没有回甜
- 已回写 `smoke/e2e-dual-substitute-evil/.mighty/state.json`：
  - `progress.current_chapter = 5`
  - `progress.total_words = 15940`
  - 新增 `chapter_meta[5]`
  - 新增 `chapter_snapshots[5]`
  - 新增 `summaries_index[5]`

## Session Update: 2026-03-22 11:26

- 已补齐 `smoke/e2e-dual-substitute-evil` 第006章章纲：
  - `大纲/章纲/第006章.md`
  - 本章目标是验证中段不会滑回“抓到人就全招”
- 已写出第006章正文：
  - `chapters/第006章.md`
  - 本章只推进到：
    - `B-17` 只是 `Q版样张`
    - 真实项目名为 `归位计划3.2`
    - 应岚只向 `柏宁` 交稿
  - 没有直接写穿最终设局人
- 本章同步落下两层代价：
  - `偷拍视频/律师函` 继续反咬姜栀
  - `许知微` 发现姜栀私开录音后，同盟裂口扩大
- 已回写 `smoke/e2e-dual-substitute-evil/.mighty/state.json`：
  - `progress.current_chapter = 6`
  - `progress.total_words = 19374`
  - 新增 `chapter_meta[6]`
  - 新增 `chapter_snapshots[6]`
  - 新增 `summaries_index[6]`
  - 新增伏笔 `f5: 柏宁接口线`

## Session Update: 2026-03-22 11:31

- 已完成 `smoke/e2e-dual-substitute-evil` 第004-006章集中 review
  - 结论：中段总体稳住了“阻力 / 代价 / 半兑现”，没有滑回顺推打穿
  - 评分：
    - 第004章：`86 / A-`
    - 第005章：`85 / A-`
    - 第006章：`84 / B+`
- review 主要残余问题：
  - `林特助` 连续两章承担开门与报线索功能，功能桥倾向偏强
  - 第006章机场外部压力更多停留在高压背景，动作层阻断还可再实一点
- 已回写 `.mighty/state.json`：
  - 第005章、第006章 review 分数与维度
  - `anti_flattening_flags`
  - `anti_flattening_summary`
  - `quality_metrics.last_review_chapter = 6`

## Session Update: 2026-03-22 11:40

- 已补齐 `smoke/e2e-dual-substitute-evil` 第007章章纲：
  - `大纲/章纲/第007章.md`
  - 本章专门用来验证：
    - `柏宁` 不会一堵全招
    - 外部阻断会真正落到动作层
    - `林特助` 不再只是无成本功能桥
- 已写出第007章正文：
  - `chapters/第007章.md`
  - 本章只推进到：
    - `双总办会签`
    - `归位计划3.2会签页半张照片`
    - `今夜八点前终稿再归档`
  - 没有直接写出最终拍板人
- 已回写 `smoke/e2e-dual-substitute-evil/.mighty/state.json`：
  - `progress.current_chapter = 7`
  - `progress.total_words = 23149`
  - 新增 `chapter_meta[7]`
  - 新增 `chapter_snapshots[7]`
  - 新增 `summaries_index[7]`
  - 新增伏笔 `f6: 终稿归档点`
- 本章还额外把上轮 review 残余问题压进了正文结果：
  - `林特助` 收到正式撤岗通知
  - 酒店的镜头、安保和门卡冻结都落成了动作阻断，不再只是背景压迫

## Session Update: 2026-03-22 11:50

- 已完成 `smoke/e2e-dual-substitute-evil` 第007章单章 review
  - 评分：`87 / A-`
  - 结论：第007章基本解决了上轮 review 的两个残余问题
    - 外部阻断已落到动作层
    - `林特助` 已付出真实岗位与权限成本
- 当前仅保留一个低位残余风险：
  - `柏宁失口 + 会签页同场出现` 让推进效率略高
  - 后续第008章不宜再连续使用同场掉口风 / 同场掉文件的推进方式
- 已回写 `.mighty/state.json`：
  - `chapter_meta[7].review_score = 87`
  - `chapter_meta[7].anti_flattening_flags`
  - `quality_metrics.last_review_chapter = 7`

## Session Update: 2026-03-22 11:58

- 已按第007章 review 建议推进 `smoke/e2e-dual-substitute-evil` 第008章：
  - `大纲/章纲/第008章.md`
  - `chapters/第008章.md`
- 本章刻意避开了“同场失口 + 同场掉文件”的重复推进方式，改为：
  - `格式识别`
  - `联合责任签字`
  - `流转日志 / 交接箱标签`
- 本章只推进到：
  - `潮汐会馆闭门会`
  - `贺氏董事办主任沈蔚`
  - `许太太办公室`
  - `承川线体面保留`
  - 仍未直接拿到终稿正文
- 已回写 `smoke/e2e-dual-substitute-evil/.mighty/state.json`：
  - `progress.current_chapter = 8`
  - `progress.total_words = 26621`
  - 新增 `chapter_meta[8]`
  - 新增 `chapter_snapshots[8]`
  - 新增 `summaries_index[8]`
  - 新增伏笔 `f7: 沈蔚会签线`

## Session Update: 2026-03-22 12:38

- 已补齐 `smoke/e2e-dual-substitute-evil` 第009章：
  - `大纲/章纲/第009章.md`
  - `chapters/第009章.md`
- 本章把“真正设局层浮面”压成了两类证据：
  - `终稿封页：知微归位 / 姜线退场`
  - `门外录音：姜线必须有出口 / 先保承川线体面`
- 同时保留了未完全兑现：
  - 没拿到终稿全文
  - 会馆内部已启动版本替换
- 已回写 `smoke/e2e-dual-substitute-evil/.mighty/state.json`：
  - `progress.current_chapter = 9`
  - `progress.total_words = 30180`
  - 新增 `chapter_meta[9]`
  - 新增 `chapter_snapshots[9]`
  - 新增 `summaries_index[9]`
  - 新增伏笔 `f8: 版本替换`

## Session Update: 2026-03-22 12:40

- 已完成 `smoke/e2e-dual-substitute-evil` 第007-009章集中 review
  - 评分：
    - 第007章：`87 / A-`
    - 第008章：`88 / A-`
    - 第009章：`89 / A-`
- 结论：
  - 这条 smoke 到后段仍然没有滑回“顺理成章一路打穿”
  - 真相是分层浮面的，不是自动掉落
  - 双女主关系没有被剧情自动缝合
- 当前只剩两个低位残余风险：
  - 第008章制度入口打得较顺，但仍在可接受范围
  - 第009章“版本替换”信息还部分依赖 `林特助` 耳听，若继续写第010章，不宜再重复依赖他补内幕
- 已回写 `.mighty/state.json`：
  - 第008章、第009章 review 分数与维度
  - `anti_flattening_flags`
  - `quality_metrics.last_review_chapter = 9`

## Session Update: 2026-03-22 12:45

- 已按“保留为已完成验证样本”收口 `smoke/e2e-dual-substitute-evil`
- 已更新候选线与对照文档：
  - `docs/research/fanqie/fanqie-evil-dual-female-substitute-candidate.md`
  - `docs/research/fanqie/fanqie-evil-variant-comparison.md`
- 已在 `docs/sample-remediation-priority-matrix-2026-03-22.md` 增加后续注记：
  - 该样本已不再属于待回收对象
  - 当前定位改为 **已完成验证样本闭环**
- 当前这条样本的系统结论为：
  - `golden three -> chapter 9 validation sample -> chapter 7-9 review closure`
  - 可作为第四条候选实验线的已验证样本保留

## Session Update: 2026-03-22 19:10

- 已将根目录中文入口文档接入 `README.md`：
  - 新增 `使用流程总览.md` 阅读入口
- 已将 shared 同步的主入口改为只读预检：
  - `bash scripts/sync-shared-from-genm.sh --report`
- 已为以下历史阶段文档补充“当前以正式版决策文档为准”的提示：
  - `docs/00-当前有效/v1-boundary.md`
  - `docs/90-归档/迁移与RC/v1-readiness-assessment.md`
  - `docs/90-归档/迁移与RC/v1-rc-plan.md`
  - `docs/90-归档/迁移与RC/v1-rc-exit-criteria.md`
  - `docs/90-归档/迁移与RC/v1-rc-blockers.md`

## Session Update: 2026-03-23 13:30

- 已为 `novel-write` 增加守卫式自动收口契约：
  - 单章写作默认尝试 `novel-close`
  - 支持显式 `skip_close=true`
  - `novel-batch` 不继承该默认行为
- 已明确 `novel-close` 是 post-write handoff 的执行器：
  - `novel-write` 决定是否触发
  - `novel-close` 负责 `review -> route -> re-review`
- 已更新用户入口文档：
  - `README.md`
  - `docs/00-当前有效/default-workflows.md`
  - `docs/00-当前有效/start-here.md`
  - `docs/00-当前有效/skill-usage.md`
- 已完成边界核查：
  - `skills/novel-batch/SKILL.md` 未引入 auto-close
  - `scripts/post-task-maintenance.py` 未引入 prose mutation
- 已运行迁移结构校验：
  - `bash scripts/validate-migration.sh`
  - 结果：`Migration validation passed`

## Session Update: 2026-03-23 15:56

- 已按 `novel-close` 的单路由收口方式处理 `projects/庶女谋略` 第016章：
  - 先做一轮新复审，判断为 `novel-fix` 尺度
  - 不走 `polish` / `rewrite`
- 已备份原稿到：
  - `projects/庶女谋略/.mighty/backup/第016章-20260323-closure-before-fix.md`
- 已将第016章正文压缩并收束为聚焦版：
  - 保留 `针线房尺头单 -> 礼数分层 -> 林姨娘误读 -> 林若雪口风 -> 出入记名 -> 册页实物` 主链
  - 删除大段重复解释
  - 补入“主动记账”动作，避免整章只剩被动观察
- 已回写 `projects/庶女谋略/.mighty/state.json`：
  - `chapter_meta[016].fix_count = 1`
  - `chapter_meta[016].review_score = 87`
  - `chapter_meta[016].recommended_next_action = none`
  - 新增 `last_close_*` 元数据
  - 同步更新 `chapter_snapshots[016]`、`summaries_index[016]`
  - `progress.total_words = 66444`
- 本轮收口残余：
  - 第016章当前字数仍略高于目标上限，但已回到可控区间

## Session Update: 2026-03-23 16:21

- 已按 `novel-write` 写出 `projects/庶女谋略` 第017章，并保留默认 post-write close：
  - 核心交易单元锁定为“庚帖条目与婚配比较”
  - 让 `王氏 / 苏文渊 / 小桃` 在同一条婚配账上呈现不同立场
  - 章末把“出门见客”收成明确的“带去给人看”
- 本轮判断不以字数为第一优先：
  - 以是否言之有物、是否推进婚配线、是否把人物位置关系写清为主
  - 不为满足章长限制而机械增删无效内容
- 已回写 `projects/庶女谋略/.mighty/state.json`：
  - `progress.current_chapter = 17`
  - 新增 `chapter_meta[017]`
  - 新增 `chapter_snapshots[017]`
  - 新增 `summaries_index[017]`
  - 更新主角 `status / current_goals / recent_events`
  - 新增 suspense：`后日出门时谁会真正把苏照棠看进眼里`
- 已按守卫式自动收口记录：
  - `last_close_route = none`
  - `review_score = 88`
  - 下一章建议：尽快把“被看”兑现成具体场面

## Session Update: 2026-03-23 16:40

- 已按 `novel-batch` 的安全上限连续写出 `projects/庶女谋略` 第018-020章：
  - `018`：把婚配线从“相看前准备”推进到“嫡庶价码明码化”
  - `019`：把婚配压力从府内安排推进到寺会相看现场
  - `020`：完成“高嫁未必是路”的卷末认知翻面，并自然挂出第二卷“借势破局”
- 本轮遵循“三章链”而不是单章孤立写法：
  - `定价 -> 相看 -> 认知翻面`
  - 每章都保留有效交易单元，不为凑字数回填空内容
- 已回写 `projects/庶女谋略/.mighty/state.json`：
  - `progress.current_chapter = 20`
  - `progress.total_words = 95797`
  - 新增 `chapter_meta[018-020]`
  - 新增 `chapter_snapshots[018-020]`
  - 新增 `summaries_index[018-020]`
  - 更新主角 `status / current_goals / recent_events`
  - 更新 suspense：
    - 保留 `苏照棠的名字会被送去谁家相看`
    - 新增 `苏照棠会借谁的势改写自己的婚配去处`
    - 结清 `后日出门时谁会真正把苏照棠看进眼里`
- 已运行批量质量门并通过：
  - `python3 scripts/check-batch-quality-gate.py projects/庶女谋略 --start 18 --end 20 --batch-count 3 --write-report`
  - 结果：`status = pass`
- 已运行维护钩子：
  - `python3 scripts/post-task-maintenance.py projects/庶女谋略 --trigger batch --batch-count 3`
  - 结果：`ran-maintenance`

## Session Update: 2026-03-24 00:30

- 已在 `projects/转学第一天，我把校草认成了新来的代课老师` 创建最小可跑的番茄 `青春甜宠` 项目骨架：
  - `.mighty/state.json`
  - `.mighty/learned-patterns.json`
  - `.mighty/market-adjustments.json`
  - `大纲/总纲.md`
  - `设定集/角色/主角.md`
  - `设定集/力量体系.md`
- 已按 `novel-outline` 最小样本要求落出第001-003章章纲，并锁定：
  - 第001章：误认身份强情绪入口
  - 第002章：食堂/操场场景中的互动升级与误判
  - 第003章：广播站试音 + 学习互助表的小兑现
- 已写出第001-003章正文，且没有扩写到第004章以后：
  - `第001章 = 2278`
  - `第002章 = 2296`
  - `第003章 = 2401`
- 已回写 `projects/转学第一天，我把校草认成了新来的代课老师/.mighty/state.json`：
  - `progress.current_chapter = 3`
  - `progress.total_words = 6975`
  - 新增 `chapter_meta[001-003]`
  - 新增 `summaries_index[001-003]`
  - 显式锁定 `genre_profile.bucket = 青春甜宠`
- 已完成最小验证：
  - JSON sidecar / state 全部可解析
  - `python3 scripts/fanqie_p0_smoke.py --project-root "projects/转学第一天，我把校草认成了新来的代课老师" --chapter 003 --chapters 001-003 --mode draft`
  - 已生成 smoke draft：
    - `docs/opening-and-plot-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-fanqie-p0-2026-03-24.md`

## Session Update: 2026-03-23 17:05

- 已按“先补完整卷前段章纲，再继续正文”的思路，为 `projects/庶女谋略` 新建第二卷前段 `021-030` 全套章纲：
  - `021-023`：借势起手
  - `024-026`：第一次换账，并把高门旧闻推上台面
  - `027-030`：外家抬价、借差立位、成国公府前影与阶段收束
- 本轮补纲不是零散补三章，而是把第二卷前段先锁成一条完整推进链：
  - 从 `借风入账` 起手
  - 到 `风不是巧合` 收第一阶段
- 已确认十份新章纲都具备可直接写作的基本结构：
  - `核心问题`
  - `章节目标`
  - `场景拆解`
  - `本章账本`
  - `章末钩子`
- 下一步可以直接按三章工作流规则卡，从 `021-023` 开始连续写正文，不需要再回补第二卷前段方向

## Session Update: 2026-03-23 17:11

- 已按三章工作流规则卡连续写出 `projects/庶女谋略` 第021-023章：
  - `021`：借寺会余风入账，第一次摸到回礼名册
  - `022`：从名册和旧备注里坐实冯家二房这门不利婚事
  - `023`：借苏文渊“照规矩慢慢来”的口气，把冯家口风先往后拖住半步
- 本轮仍以内容推进为第一标准：
  - `借差事入门 -> 看账辨轻重 -> 顺手换账`
  - 没有为了满足软门槛回填无效段落
- 已回写 `projects/庶女谋略/.mighty/state.json`：
  - `progress.current_chapter = 23`
  - `progress.total_words = 102523`
  - 新增 `chapter_meta[021-023]`
  - 新增 `chapter_snapshots[021-023]`
  - 新增 `summaries_index[021-023]`
  - 更新主角 `status / current_goals / recent_events`
  - suspense 变更：
    - 结清 `苏照棠会借谁的势改写自己的婚配去处`
    - 新增 `旧礼例册里的成国公府名字后面到底连着谁`
- 已运行批量质量门：
  - `python3 scripts/check-batch-quality-gate.py projects/庶女谋略 --start 21 --end 23 --batch-count 3 --write-report`
  - 结果：`status = warn`
  - 原因：三章均低于软下限，但无 `fail` 级问题
- 已运行维护钩子：
  - `python3 scripts/post-task-maintenance.py projects/庶女谋略 --trigger batch --batch-count 3`
  - 结果：`ran-maintenance`

## Session Update: 2026-03-23 17:57

- 已继续按同一工作流写出 `projects/庶女谋略` 第024-026章：
  - `024`：旧礼例册中第一次完整碰到“成国公府、寄居顾氏、旧例沿此”
  - `025`：林若雪带来半句旧闻，让寄居表姑娘第一次从“旧账”变成“人影”
  - `026`：通过被抹掉的残字，把婚配账与旧闻账正式并到一起，并挂出下一轮小宴新局
- 本轮未触发额外 MCP 补设定：
  - 当前项目内设定文件足够支持这组三章
  - 仍未进入必须外查官制/礼制/高门谱系细则的阶段
- 已回写 `projects/庶女谋略/.mighty/state.json`：
  - `progress.current_chapter = 26`
  - `progress.total_words = 109274`
  - 新增 `chapter_meta[024-026]`
  - 新增 `chapter_snapshots[024-026]`
  - 新增 `summaries_index[024-026]`
  - 更新主角 `status / current_goals / recent_events`
  - suspense 变更：
    - 结清 `旧礼例册里的成国公府名字后面到底连着谁`
    - 新增 `那位被抹掉名字的寄居表姑娘究竟留下了什么`
- 已运行批量质量门：
  - `python3 scripts/check-batch-quality-gate.py projects/庶女谋略 --start 24 --end 26 --batch-count 3 --write-report`
  - 结果：`status = warn`
  - 原因：三章均低于软下限，但无 `fail` 级问题
- 已运行维护钩子：
  - `python3 scripts/post-task-maintenance.py projects/庶女谋略 --trigger batch --batch-count 3`
  - 结果：`ran-maintenance`

## Session Update: 2026-03-23 18:12

- 已继续按同一三章工作流写出 `projects/庶女谋略` 第027-029章：
  - `027`：王家外家正式开始替主角抬价，主角锁定“借结果主义”这条路
  - `028`：借小宴席次与迎客差事，把“可用”换成更主动的一寸位置
  - `029`：成国公府第一次从旧册残影变成现实中的外院来往名目
- 本轮未触发额外 MCP 补设定：
  - 当前项目内家谱、势力、角色卡仍足够支撑这一组推进
  - 还没进入必须外查官制/礼制细则的阶段
- 已回写 `projects/庶女谋略/.mighty/state.json`：
  - `progress.current_chapter = 29`
  - `progress.total_words = 115640`
  - 新增 `chapter_meta[027-029]`
  - 新增 `chapter_snapshots[027-029]`
  - 新增 `summaries_index[027-029]`
  - 更新主角 `status / current_goals / recent_events`
  - suspense 变更：
    - 结清 `那位被抹掉名字的寄居表姑娘究竟留下了什么`
    - 新增 `成国公府外院正在动的这条线，会把苏照棠引到谁身上`
- 已运行批量质量门：
  - `python3 scripts/check-batch-quality-gate.py projects/庶女谋略 --start 27 --end 29 --batch-count 3 --write-report`
  - 结果：`status = warn`
  - 原因：三章均低于软下限，但无 `fail` 级问题
- 已运行维护钩子：
  - `python3 scripts/post-task-maintenance.py projects/庶女谋略 --trigger batch --batch-count 3`
  - 结果：`ran-maintenance`

## Session Update: 2026-03-23 18:23

- 已继续按同一三章工作流写出 `projects/庶女谋略` 第030-032章：
  - `030`：把 `021-030` 的并账判断正式收成“风不是巧合”
  - `031`：在小宴现场把主角从“被看的人”换成“在场有用的人”
  - `032`：通过三房转出的回帖与“顾氏旧份并销”，第一次真正坐实顾含真后嫁裴氏旁支三房
- 本轮按既有项目设定直接写作，未触发额外 MCP 补资料：
  - 当前家谱、势力、角色卡仍足够支撑 `030-032`
  - 尚未进入必须外查高门礼制或官制的节点
- 已回写 `projects/庶女谋略/.mighty/state.json`：
  - `progress.current_chapter = 32`
  - `progress.total_words = 121710`
  - 新增 `chapter_meta[030-032]`
  - 新增 `chapter_snapshots[030-032]`
  - 新增 `summaries_index[030-032]`
  - 更新主角 `status / current_goals / recent_events`
  - suspense 变更：
    - 结清 `成国公府外院正在动的这条线，会把苏照棠引到谁身上`
    - 新增 `裴氏旁支三房后面那个仍在动的人到底是谁`
- 已运行批量质量门：
  - `python3 scripts/check-batch-quality-gate.py projects/庶女谋略 --start 30 --end 32 --batch-count 3 --write-report`
  - 结果：`status = warn`
  - 原因：三章均低于软下限，但无 `fail` 级问题
- 已运行维护钩子：
  - `python3 scripts/post-task-maintenance.py projects/庶女谋略 --trigger batch --batch-count 3`
  - 结果：`ran-maintenance`

## Session Update: 2026-03-23 18:45

- 已按 review 结论对 `projects/庶女谋略` 第030-032章做一轮有价值的润色扩写：
  - `030`：补强“并账推进”从抽象判断落到现实触点与前文记忆上的重量
  - `031`：补入小宴中的具体试探与口风抬价，让“照人局”更像现场而非结果汇报
  - `032`：补强“三房线”背后仍连着活人的危险感与现实阻力
- 本轮明确执行新的章节硬线：
  - 正文在“内容有效”前提下，每章不少于 `3000` 字
- 已同步更新 `projects/庶女谋略/.mighty/state.json`：
  - `progress.total_words = 124645`
  - `chapter_meta[030-032].word_count` 全部刷新到最新版本
  - `chapter_snapshots[030-032].word_count` 全部刷新到最新版本
  - `meta.updated_at / progress.last_write_time` 同步更新
- 已重新运行批量质量门并通过：
  - `python3 scripts/check-batch-quality-gate.py projects/庶女谋略 --start 30 --end 32 --batch-count 3 --write-report`
  - 结果：`status = pass`
- 已重新运行维护钩子：
  - `python3 scripts/post-task-maintenance.py projects/庶女谋略 --trigger batch --batch-count 3`
  - 结果：`ran-maintenance`

## Session Update: 2026-03-23 19:34

- 已按默认流程先补后写，为 `projects/庶女谋略` 新建并消费第033-035章章纲：
  - `033`：外院缺口
  - `034`：名字半露
  - `035`：活人接线
- 已继续按同一三章工作流写出第033-035章：
  - `033`：借外院礼货与回帖缺口，继续往里争位置
  - `034`：把活人线大致锁进裴则安这一层
  - `035`：把“先锁位置，再锁活人”正式收成下一阶段策略
- 本轮明确满足当前章节硬线：
  - `033 = 3002`
  - `034 = 3001`
  - `035 = 3000`
- 本轮未触发额外 MCP 补设定：
  - 当前项目内设定仍足够支撑这一组三章
  - 尚未进入必须外查更细高门礼制 / 官制节点
- 已回写 `projects/庶女谋略/.mighty/state.json`：
  - `progress.current_chapter = 35`
  - `progress.total_words = 133648`
  - 新增 `chapter_meta[033-035]`
  - 新增 `chapter_snapshots[033-035]`
  - 新增 `summaries_index[033-035]`
  - 更新主角 `status / current_goals / recent_events`
  - suspense 变更：
    - 结清 `裴氏旁支三房后面那个仍在动的人到底是谁`
    - 新增 `苏照棠还能再争到哪一层位置，去继续摸裴则安和顾含真旧案`
- 已运行批量质量门并通过：
  - `python3 scripts/check-batch-quality-gate.py projects/庶女谋略 --start 33 --end 35 --batch-count 3 --write-report`
  - 结果：`status = pass`
- 已运行维护钩子：
  - `python3 scripts/post-task-maintenance.py projects/庶女谋略 --trigger batch --batch-count 3`
  - 结果：`ran-maintenance`

## Session Update: 2026-03-24 Fanqie P0 非宫斗与第二写回样本

- 已验证两个真实非宫斗 P0 项目：
  - `projects/转学第一天，我把校草认成了新来的代课老师`
  - `projects/公司裁我那天，系统先赔了我一百万`
- 两个项目都成功生成真实项目 smoke 文档：
  - 初始都能稳定进入 `draft`
  - 后续已在下一节继续收紧为 `medium confidence`
- 已新增 `现言甜宠 -> 青春甜宠` alias，并验证 `smoke/e2e-tianchong*` 可输出 `low confidence draft`
- 已把 `青春甜宠` 项目的 `第003章` 做成第二条真实写回样本：
  - `chapter_meta["003"].fanqie_bucket_flags = []`
  - `chapter_meta["003"].fanqie_bucket_summary.bucket = "青春甜宠"`
  - `chapter_meta["003"].fanqie_bucket_summary.bucket_grade = "pass"`
- 已运行验证：
  - `python -m unittest tests.test_fanqie_p0_smoke -v`
  - `python -m unittest tests.test_opening_plot_framework -v`
  - `bash scripts/validate-migration.sh`
  - 结果全部通过

## Session Update: 2026-03-24 青春甜宠与都市脑洞收紧并完成第三写回样本

- 已继续收紧 `青春甜宠` 判断：
  - 当前真实项目 smoke 从 `low confidence draft` 提升到 `medium confidence`
  - `fanqie_bucket_review_summary.bucket_grade = pass`
  - `fanqie_bucket_precheck_summary.submission_fit = fit`
- 已继续收紧 `都市脑洞` 判断：
  - 当前真实项目 smoke 从 `low confidence draft` 提升到 `medium confidence`
  - `fanqie_bucket_review_summary.bucket_grade = warn`
  - `fanqie_bucket_precheck_summary.submission_fit = fit`
- 已把 `都市脑洞` 项目的 `第003章` 做成第三条真实写回样本：
  - `chapter_meta["003"].fanqie_bucket_summary.bucket = "都市脑洞"`
  - `chapter_meta["003"].fanqie_bucket_summary.bucket_grade = "warn"`
- 已运行验证：
  - `python -m unittest tests.test_fanqie_p0_smoke -v`
  - `python -m unittest tests.test_opening_plot_framework -v`
  - `bash scripts/validate-migration.sh`
  - 结果全部通过

## Session Update: 2026-03-24 Fanqie P0 记录层对齐与最终校验

- 已将 `task_plan.md` / `findings.md` / `progress.md` / 压力测试文档 同步到当前真实状态：
  - `宫斗宅斗`：高置信写回样本
  - `青春甜宠`：中置信写回样本，`pass / fit`
  - `都市脑洞`：中置信写回样本，`warn / fit`
- 已把两个真实非宫斗 P0 项目的最终结论写回文档层，避免记录层继续保留旧的 `low confidence / draft-only` 说法
- 当前 `fanqie_p0_smoke` 线的阶段性闭环已明确：
  - 规则层已接入
  - 工具层已验证
  - 真实项目 smoke 已覆盖
  - 真实项目轻量写回已覆盖三类样本

## Session Update: 2026-03-24 Additional Non-Palace P0 Expansion

- 已新增三条真实非宫斗 P0 项目的 smoke 与写回闭环：
  - `职场婚恋`：`projects/她升职那天，前上司成了我合租室友`
  - `都市日常`：`projects/搬回老小区后，我靠蹭饭认识了整栋楼`
  - `玄幻脑洞`：`projects/宗门垫底那年，我把废丹卖成了天价`
- 已为三条线补 bucket 抓手并通过真实文本校准：
  - `职场婚恋`：`代理 / 甲方 / 合租 / 试运行`
  - `都市日常`：`燃气 / 白板 / 换饭 / 康复`
  - `玄幻脑洞`：`碎纹丹秤 / 废火丹 / 外门小集 / 灵石`
- 当前三条线都已稳定收敛到：
  - `confidence = medium`
  - `fanqie_bucket_review_summary.bucket_grade = pass`
  - `fanqie_bucket_precheck_summary.submission_fit = fit`
- 已把三条项目的 `chapter_meta["003"]` 轻量写回：
  - `fanqie_bucket_flags = []`
  - `fanqie_bucket_summary.bucket = 职场婚恋 / 都市日常 / 玄幻脑洞`
  - `fanqie_bucket_summary.bucket_grade = pass`
- 已修复两个工具边界问题：
  - `writeback` 模式不再把 smoke 文档回退成空模板
  - 已存在但为空的 bucket 占位字段可正常写回；相同 summary 的重复写回返回 `already-written`
- 已运行验证：
  - `python -m unittest tests.test_fanqie_p0_smoke -v`
  - `python -m unittest tests.test_opening_plot_framework -v`
  - `bash scripts/validate-migration.sh`
  - 结果全部通过

## Session Update: 2026-03-24 Gap Tracker Handoff

- 已新增 [fanqie-p0-gap-tracker-2026-03.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/fanqie-p0-gap-tracker-2026-03.md)
  - 明确已覆盖的真实桶
  - 明确下一步该补的是第二条真实样本，而不是空桶
  - 给出下一批推荐顺序和可直接开工的项目提示词
- 已把 gap tracker 入口挂回 [opening-and-plot-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/README.md)
- 已扩展 `tests/test_opening_plot_framework.py`
  - 校验 gap tracker 文档存在
  - 校验 README 暴露真实样本与 gap tracker 入口

## Session Update: 2026-03-24 P0 Full Coverage

- 已验证并写回最后两个 `P0` 缺口桶：
  - `历史脑洞`：`projects/我在县衙当杂吏，靠翻旧案升了堂`
  - `豪门总裁`：`projects/签下离婚协议那天，冷脸总裁改口叫我合伙人`
- 已为两条线补 bucket 抓手并通过真实文本校准：
  - `历史脑洞`：`县衙 / 旧案 / 卷宗 / 主簿房`
  - `豪门总裁`：`离婚协议 / 董事会 / 合伙人 / 试运营`
- 当前这两条线都已稳定收敛到：
  - `confidence = medium`
  - `fanqie_bucket_review_summary.bucket_grade = pass`
  - `fanqie_bucket_precheck_summary.submission_fit = fit`
- 已兼容 `chapter_meta` 的 `3 / 003` 双键风格，并把两条项目写回到各自现有键位
- 当前 `P0 8 桶` 已全部具备：
  - 真实项目 smoke
  - 轻量 bucket 写回样本
  - 回归测试约束

## Session Update: 2026-03-24 Second Historical Brainhole Sample

- 已新增第二条 `历史脑洞` 真实项目：
  - `projects/我在县衙誊旧档，靠半页供词改了判词`
- 已补齐：
  - `.mighty/state.json`
  - `.mighty/market-adjustments.json`
  - `.mighty/learned-patterns.json`
  - `总纲 / 第001-003章章纲 / 第001-003章正文`
- 已跑通：
  - `draft`
  - `writeback`
- 当前结果：
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`

## Session Update: 2026-03-24 Second-Sample Expansion

- 已新增第二条 `豪门总裁` 真实样本：
  - `projects/离婚冷静期那天，前夫把董事会席位押给了我`
- 已新增第二条 `都市脑洞` 真实样本：
  - `projects/我赔光积蓄那天，系统先把违约金打到了账上`
- 已新增第二条 `玄幻脑洞` 真实样本：
  - `projects/外门药田被夺那天，我靠废丹拍卖赚回了灵石`
- 三条样本均已补齐最小项目骨架、总纲、章纲、前三章和 sidecar
- 三条样本均已跑通：
  - `draft`
  - `writeback`
- 当前结果：
  - `豪门总裁`：`medium / pass / fit`
  - `都市脑洞`：`medium / warn / fit`
  - `玄幻脑洞`：`medium / pass / fit`

## Session Update: 2026-03-24 Final Double-Sample Coverage

- 已新增第二条 `职场婚恋` 真实样本：
  - `projects/代理续约那天，我和前搭档被公司按进了同一套合租房`
- 已新增第二条 `青春甜宠` 真实样本：
  - `projects/广播站误放表白信那天，我和学神被迫参加学习互助`
- 已新增第二条 `都市日常` 真实样本：
  - `projects/母亲复健那年，我把楼道白板改成了换饭地图`
- 三条样本均已补齐最小项目骨架、总纲、章纲、前三章和 sidecar
- 三条样本均已跑通：
  - `draft`
  - `writeback`
- 当前结果：
  - `职场婚恋`：`medium / pass / fit`
  - `青春甜宠`：`medium / pass / fit`
  - `都市日常`：`medium / pass / fit`
- 到这里，`P0 8 桶` 已全部完成双样本覆盖

## Session Update: 2026-03-24 番茄起盘协议栈与 Compiler 层

- 已新增 `docs/opening-and-plot-framework/fanqie-launch-stack/`
  - `README`
  - 4 层主模块
  - 6 张起盘语法卡
  - `compiler contract`
- 已新增 `scripts/fanqie_launch_stack.py`
  - 支持保守 `draft`
  - 支持显式 `writeback`
  - 生成 `.mighty/launch-stack.json`
  - 只镜像 4 个轻字段到 `state`
- 已新增 `tests/test_fanqie_launch_stack.py`
- 已更新：
  - `novel-outline`
  - `novel-write`
  - `novel-review`
  - `novel-precheck`
  - `novel-package`
  - `novel-init`
  - `state-schema`
  - `state-v5-template`
  - `README.md`
  - `docs/00-当前有效/start-here.md`
  - `docs/00-当前有效/skill-usage.md`
  - `docs/00-当前有效/default-workflows.md`
  - `docs/00-当前有效/state-thinning-and-setting-sync.md`
- 已生成两条真实 smoke：
  - `离婚冷静期那天，前夫把董事会席位押给了我`
  - `宗门垫底那年，我把废丹卖成了天价`
- 已完成验证：
  - `python3 -m unittest tests.test_fanqie_launch_stack -v`
  - `python3 -m unittest tests.test_opening_plot_framework -v`
  - `bash scripts/validate-migration.sh`
- 已将实现分支 rebase 到当前 `main`，准备继续整合

## Session Update: 2026-03-25 ISSUES Follow-up Audit

- 用户指出上一轮“测试修了但文档未真实落地”的漏检问题后，重新做了文件系统级复核
- 新增 `tests/test_issue_regressions.py`
  - 锁 `ISSUES.md` 原始 10 项问题的最终落地状态
- 新增 `tests/test_repo_path_integrity.py`
  - 锁 3 个 skill 的相对 repo 路径
  - 锁 6 个关键 README / 规则文档的本地链接可解析
- 重新补齐并验证：
  - `task_plan.md` 收为单一活跃计划
  - `docs/INDEX.md`
  - `docs/research/fanqie/README.md`
  - `smoke/README.md`
  - `ISSUES.md` 每条问题的“已处理并归档”状态
- 额外修复了上一轮没有横向扫出的路径问题：
  - `skills/novel-genre/SKILL.md`
  - `skills/novel-analyze/SKILL.md`
  - `skills/novel-precheck/SKILL.md`
  - `docs/opening-and-plot-framework/README.md`
  - `docs/anti-flattening-framework/README.md`
  - `docs/writing-core-framework/README.md`
  - `docs/writing-core-framework/04-剧情层次与多线编排接口.md`
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/README.md`
  - `docs/opening-and-plot-framework/fanqie-p0-checkcards/README.md`
- 最新验证：
  - `python3 -m unittest tests.test_issue_regressions -v`
  - `python3 -m unittest tests.test_repo_path_integrity -v`
  - `bash scripts/validate-migration.sh`
  - `python3 -m unittest`
  - 结果：`203 tests` 全绿
- 额外的全仓 Markdown 链接审计还剩 `16` 处未解析项：
  - 其中 `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md` 的 `/absolute/path/...` 为模板占位
  - 其余主要集中在 `shared/` 同步资产里的历史引用，不属于当前默认工作流面向用户的断链

## Session Update: 2026-03-25 Shared Link Closure

- 没有停在“给清单”，而是继续把 `shared/` 与模板层剩余断链全部处理完
- 已修复：
  - `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`
    - 将 `/absolute/path/...` 伪链接改成纯占位文本
  - `shared/references/serial-generation-mode.md`
  - `shared/references/chapter-index-schema.md`
  - `shared/references/shared/state-schema.md`
- 已新增兼容文档，接回历史引用：
  - `shared/references/truth-files-spec.md`
  - `shared/references/truth-files-guide.md`
  - `shared/references/commands/novel-review.md`
  - `shared/validators/post-write-validator.md`
- 已新增可复用审计脚本：
  - `scripts/audit_local_links.py`
  - 特点：忽略 fenced code block，只审计真实 Markdown 本地链接
- 已新增测试：
  - `tests/test_markdown_link_audit.py`
- 最新验证：
  - `python3 scripts/audit_local_links.py`
  - `python3 -m unittest tests.test_markdown_link_audit tests.test_repo_path_integrity tests.test_issue_regressions -v`
  - `bash scripts/validate-migration.sh`
  - `python3 -m unittest`
  - 当前结果：`204 tests` 全绿，Markdown 本地链接审计结果为 `NO_BROKEN_LOCAL_MARKDOWN_LINKS`

## Session Update: 2026-03-25 信息架构状态化重构

- 不再停留在“加一个提醒文档”，而是直接按状态重排 `docs/` 根层信息架构
- 已新增状态目录：
  - `docs/00-当前有效/`
  - `docs/10-进行中/`
  - `docs/20-研究实验/`
  - `docs/90-归档/`
- 已迁移根层状态型文档：
  - 当前有效入口与治理文档迁入 `docs/00-当前有效/`
  - 架构未决问题台账迁入 `docs/10-进行中/`
  - 评审简报迁入 `docs/20-研究实验/`
  - `phase-*`、`releases/*`、`v1-rc*`、`v1-readiness*`、迁移计划文档迁入 `docs/90-归档/`
- 保留 `docs/INDEX.md` 在根层，改成状态目录导航页
- 为 4 个状态目录补充 `README.md`
- 保留根目录 `架构问题跟踪.md` 作为高可见提醒入口，不再让“是否仍未收口”只能靠点开文档判断
- 已做全仓引用清理：
  - 旧路径 `docs/start-here.md` / `docs/default-workflows.md` / `docs/skill-usage.md` / `docs/gate-triage.md` 等已清空残留引用
  - `README.md`、`AGENTS.md`、`ISSUES.md`、`tests/*`、`skills/*`、`docs/*` 已同步更新
- 迁移后发现并顺手修复了同类导入脆弱性：
  - `scripts/post_write_lint.py`
  - `scripts/setting_gate.py`
  - `scripts/check-batch-quality-gate.py`
  - `scripts/sync-setting-assets.py`
  - 现在即使在仓库根以 `python -m unittest` 路径加载，也能找到 `strong_quality_gate`
- 本轮验证：
  - `pytest -q tests/test_issue_regressions.py tests/test_markdown_link_audit.py tests/test_opening_plot_framework.py tests/test_writing_core_framework.py tests/test_fanqie_launch_stack.py tests.test_inkos_growth_plan.py tests/test_active_context.py tests/test_volume_summaries.py`
    - `90 passed, 189 subtests passed`
  - `python -m unittest tests.test_post_write_lint -v`
    - `7 tests OK`
  - `pytest -q`
    - `248 passed, 192 subtests passed`
  - `bash scripts/validate-migration.sh`
    - passed

## Session Update: 2026-03-25 AOI-001 收口

- 已直接处理 `AOI-001 state/schema/template/script 契约漂移`
- 已新增机器真值层文件：
  - `shared/templates/state-schema-v5.json`
  - `shared/templates/learned-patterns.schema.json`
  - `shared/templates/workflow-state-v2.schema.json`
  - `shared/templates/state-archive-v1.json`
- 已同步修正：
  - `shared/templates/state-v5-template.json`
    - `$schema` 指向真实 schema
    - 补齐 `entities.factions`
  - `shared/references/shared/state-schema.md`
    - 更新到当前 runtime shape
    - 明确 externalized pointer 兼容约定
  - `scripts/build_active_context.py`
    - 支持 `items` / `factions` 的字符串/对象双形态
  - `scripts/post_write_lint.py`
  - `scripts/setting_gate.py`
  - `scripts/check-batch-quality-gate.py`
  - `scripts/sync-setting-assets.py`
    - 补 sibling-import 自举路径，保证 `python -m unittest` 路径稳定
- 已新增测试：
  - `tests/test_state_contracts.py`
- 最新验证：
  - `pytest -q tests/test_state_contracts.py tests/test_active_context.py tests/test_inkos_growth_plan.py tests/test_setting_gate.py`
    - `40 passed`
  - `python -m unittest tests.test_post_write_lint -v`
    - `7 tests OK`
  - `pytest -q`
    - `254 passed, 192 subtests passed`
  - `bash scripts/validate-migration.sh`
    - passed

## Session Pause: 2026-03-25 AOI Follow-up Execution

- 用户要求按未收口架构项的优先级从高到低继续处理，并在全部完成后再统一汇报。
- 本轮已确认执行顺序：
  - `AOI-002` `shared` 治理
  - `AOI-003` `chapter transaction` 机械闭环
  - `AOI-006` 治理验证门
  - `AOI-004` `active-context` 边界
  - `AOI-005` 入口文档职责收口
  - `AOI-007` MCP memory / 调度边界
  - `AOI-008` runtime / plugin 边界固化
- 已完成的调研与归并：
  - 对比 `../Genm/build/{profiles,references,templates}` 与本仓 `shared/{profiles,references,templates}`，确认 `shared` 不只是“本地有额外文件”，还存在大量“同路径内容漂移”的文件。
  - 明确 `AOI-002` 需要的最低治理语义：
    - 机器可读的 ownership / preserve manifest
    - report-only 差异输出
    - 默认阻断 same-path drift overwrite
    - 真实 sync 时只恢复 allowlist 中的 repo-local 文件
- 已落盘的中间工件：
  - 新增 `shared/sync-governance.json`
    - 记录当前 `references` / `templates` 域中需要保护的 repo-local 文件路径
- 当前暂停点：
  - `scripts/sync-shared-from-genm.sh` 已开始重写，但仍处于**未验证的中间态**；目标逻辑已确定为：
    - 支持 governance file
    - 支持 env override 便于测试
    - `--report-json` 输出 local-only / drift / source-only
    - 默认阻断 same-path drift 覆盖
    - sync 后恢复 allowlist 中的 protected local paths
  - 由于用户中途要求暂停，本轮尚未完成：
    - 脚本自检
    - 定向测试
    - `progress/findings/task ledger` 的收口更新
- 恢复后第一步建议：
  1. 先修完 `scripts/sync-shared-from-genm.sh` 的中间态问题（数组声明/循环位置/语法自检）
  2. 新增 `tests/test_shared_sync_governance.py`
  3. 运行该测试和 `bash scripts/validate-migration.sh`
  4. 再进入 `AOI-003 workflow_state` 真正闭环

## Session Update: 2026-03-25 AOI-002 / AOI-003 / AOI-004 / AOI-006 收口推进

- 已完成 `AOI-002 shared` 治理脚本收口：
  - 新增 `shared/sync-governance.json`
  - `scripts/sync-shared-from-genm.sh` 改为 governance-aware sync
  - `--report-json` 现在输出：
    - `protected_local_paths`
    - `local_only_paths`
    - `unexpected_local_only_paths`
    - `drift_paths`
    - `source_only_paths`
  - 默认阻断 `same-path drift overwrite`
  - 真实 sync 后会恢复 governance allowlist 中的 protected local paths
- 已完成 `AOI-003` 的第一段机械闭环：
  - 新增 `scripts/workflow_state_utils.py`
  - `scripts/project-maintenance.py` / `scripts/post-task-maintenance.py` 现在会真实写回 `.mighty/workflow_state.json`
  - maintenance 完成后会把：
    - `current_step` 推进到 `snapshot`
    - `last_successful_checkpoint` 写成 `maintenance`
- 已完成 `AOI-004 active-context` 风险收口：
  - `scripts/build_active_context.py` 不再复制 `recent_guardrails` 正文
  - 改为只写 `guardrail_summary`
- 已完成 `AOI-006` 的当前验证门补齐：
  - 新增 `tests/test_shared_sync_governance.py`
  - 扩展 `tests/test_inkos_growth_plan.py`
  - `scripts/validate-migration.sh` 现在要求 `shared/sync-governance.json`
- 已同步更新：
  - `README.md`
  - `docs/00-当前有效/v1-boundary.md`
  - `docs/00-当前有效/skill-usage.md`
  - `docs/00-当前有效/state-thinning-and-setting-sync.md`
  - `docs/10-进行中/architecture-open-issues.md`
- 本轮验证：
  - `python3 -m unittest tests.test_shared_sync_governance -v`
    - `4 tests OK`
  - `pytest -q tests/test_inkos_growth_plan.py tests/test_setting_gate.py`
    - `25 passed`
  - `pytest -q tests/test_active_context.py tests/test_inkos_growth_plan.py`
    - `25 passed`
  - `bash scripts/sync-shared-from-genm.sh --report-json --domain references`
    - 成功输出本仓真实 `protected/local-only/drift/source-only` 统计
  - `bash scripts/validate-migration.sh`
    - passed
- 最终总回归：
  - `pytest -q`
    - `262 passed, 192 subtests passed`
  - `bash scripts/validate-migration.sh`
    - passed
  - `bash scripts/sync-shared-from-genm.sh --report --domain references`
    - 成功输出 governance-aware report
## Session Update: 2026-03-25 半联动能力排查

- 继续排查仓库里是否还有类似 `fetch MCP / MCP memory` 这种“能力存在但未真正联动”的项。
- 结论：
  - `fetch MCP`：半联动
    - `scripts/acquire_source_text.py` 已支持外部 provider 注入，但仓库还没有 workspace 级 provider 声明与统一 registry。
  - `MCP memory`：边界已定义，但尚未形成真实 project-local mapping。
  - `launch-stack`：仍依赖 `novel-outline` 之后的手动编译触发。
  - `snapshot`：transaction 状态已推进到 `snapshot`，但 artifact 仍未自动生成。
  - `novel-log`：读链已存在，但缺默认 trace writer / init path。
- 同时确认以下项不应误判为“未联动缺口”：
  - `novel-config`
  - `novel-test`
  - `novel-scan`
  这些当前是有意边界或实验边界，不属于默认主线漏接。
- 已将上述结果补进：
  - `docs/00-当前有效/v1.1-roadmap.md`
## Session Update: 2026-03-25 `v1.1-roadmap` 根目录化与状态化

- 按用户要求，将 `v1.1-roadmap` 提升为仓库根目录主文件：
  - `v1.1-roadmap.md`
- 新 roadmap 现在明确记录任务状态：
  - `[done]`
  - `[in_progress]`
  - `[planned]`
  - `[blocked]`
  - `[deferred]`
- `docs/00-当前有效/v1.1-roadmap.md` 已改成入口指针，不再双维护完整内容。
- `README.md` 已补根目录 roadmap 入口。
- `scripts/validate-migration.sh` 与 `tests/test_issue_regressions.py` 已新增对根目录 roadmap 的护栏。
- 已将 `v1.1-roadmap.md` 补成执行编排版：
  - Phase 1：Profile Contract 串行收口
  - Phase 2：默认工作流补线 与 MCP/fetch 接线并行
  - Phase 3：consumer 串行收口
  - Phase 4：外部资料校准
  - 并补充了推荐 worker 拆分与串行依赖
## Session Update: 2026-03-25 `Profile Contract` Phase 1 开工

- 已直接开始 `v1.1-roadmap` 的 Phase 1，而不是继续拆计划。
- 已新增：
  - `scripts/profile_contract.py`
    - 对现有异构 profile 做兼容标准化
    - 只解析 contract 所需顶层区块，绕开后段伪 YAML 风格块
    - 提供 `profile -> state.genre_profile` 的轻量投影
  - `shared/templates/profile-contract-v1.schema.json`
  - `tests/test_profile_contract.py`
- 当前结果：
  - 全仓 `shared/profiles/*/profile.yaml` 已能收进同一套 contract shape
  - 已验证 `word_count / word_count_range`
  - 已验证 `density / density_required`
  - 已验证 `must_not / never_violate`
  - 已验证 `checkpoint / check_point / id / ID` 等异构字段的兼容归一
- 已同步：
  - `scripts/validate-migration.sh`
  - `v1.1-roadmap.md` 中 `A1 / A2` 状态改为 `in_progress`
- 本轮验证：
  - `python3 -m unittest tests.test_profile_contract -v`
    - `4 tests OK`
- `Profile Contract` Phase 1 已完成：
  - `A1` 统一 profile schema
  - `A2` 明确 profile -> state.genre_profile 投影契约
  - `A3` 建立 core/platform/bucket/reference 分层 contract
- 额外完成：
  - `shared/profiles/README.md` 已补分层 contract
  - `shared/references/shared/state-schema.md` 已补 `genre_profile` 投影说明
  - `v1.1-roadmap.md` 中 `A1/A2/A3` 已改为 `done`
- 最终验证：
  - `pytest -q tests/test_profile_contract.py tests/test_issue_regressions.py`
    - `18 passed`
  - `bash scripts/validate-migration.sh`
    - passed
## Session Update: 2026-03-26 A4 consumer 入口统一完成

- 已完成 `A4`：统一 `profile` consumer 入口。
- 已更新：
  - `skills/novel-init/SKILL.md`
  - `skills/novel-genre/SKILL.md`
  - `skills/novel-outline/SKILL.md`
  - `skills/novel-write/SKILL.md`
  - `skills/novel-review/SKILL.md`
  - `skills/novel-package/SKILL.md`
- 当前统一口径：
  - `novel-genre` / `state.genre_profile` 是 profile 主入口
  - raw profile 只在缺少额外细节时通过 `scripts/profile_contract.py` 解读
  - raw profile 按 `core profile -> platform overlay -> bucket overlay -> reference files` 顺序消费
  - legacy embedded 长文本不再视为 authoritative core config
- 已新增测试：
  - `tests/test_profile_consumers.py`
- 本轮验证：
  - `pytest -q tests/test_profile_contract.py tests/test_profile_consumers.py tests/test_issue_regressions.py`
    - `19 passed`
  - `bash scripts/validate-migration.sh`
    - passed
## Session Update: 2026-03-26 Phase 2 完成

- 已完成 `v1.1-roadmap` 的 Phase 2：
  - `B1` fetch provider registry / workspace config
  - `B2` MCP memory project-local mapping
  - `B3` launch-stack auto-compile trigger
  - `B4` snapshot owner 收口
  - `B5` trace logging 接线
- 主要落地：
  - 新增 `shared/templates/acquire-provider-registry-v1.json`
  - 新增 `shared/templates/memory-context-v1.schema.json`
  - 新增 `scripts/trace_log.py`
  - 新增 `scripts/generate_snapshot.py`
  - 新增 `scripts/build_memory_context.py`
  - `scripts/acquire_source_text.py` 现在支持 provider registry / project config / codex config / provider diagnostics
  - `scripts/setting_gate.py` 现在会在番茄项目 `stage=outline` 时守卫式 auto-compile `launch-stack`
  - `scripts/project-maintenance.py` / `scripts/post-task-maintenance.py` 现在会生成 snapshot artifact、memory-context，并把 workflow_state 收口到 completed
- 已同步更新：
  - `docs/00-当前有效/default-workflows.md`
  - `docs/00-当前有效/start-here.md`
  - `docs/00-当前有效/skill-usage.md`
  - `docs/00-当前有效/state-thinning-and-setting-sync.md`
  - `v1.1-roadmap.md`
- 已新增/扩展测试：
  - `tests/test_acquire_source_text.py`
  - `tests/test_phase2_helpers.py`
  - `tests/test_setting_gate.py`
  - `tests/test_inkos_growth_plan.py`
  - `tests/test_issue_regressions.py`
- 最终验证：
  - `pytest -q`
    - `280 passed, 192 subtests passed`
  - `bash scripts/validate-migration.sh`
    - passed
## Session Update: 2026-03-26 组合题材结论延后接入约束

- 用户要求：
  - `A4` 已收口的当前写集，暂不回写这次新增的组合题材结论。
  - 后续统一按 `docs/superpowers/specs/2026-03-26-composite-genre-phase3-integration-design.md` 在 Phase 3 consumer 整合时接入。
  - 并在 `C2` 中补充映射校准范围。
- 已同步到：
  - `v1.1-roadmap.md`
    - `Phase 3` 增加“组合题材结论延后接入”约束
    - `C2` 增加“组合题材 / 多主题卖点 / 群像结构模式”映射校准范围
## Session Update: 2026-03-26 Phase 3 完成

- 已完成 `Phase 3 consumer 收口`：
  - 新增 `genre_profile` 组合题材轻字段：
    - `tagpacks`
    - `strong_tags`
    - `narrative_modes`
    - `tone_guardrails`
    - `positioning_sidecar`
  - 新增 `scripts/build_content_positioning.py`
  - 新增 `shared/templates/content-positioning-v1.schema.json`
  - 默认维护链现在会刷新 `.mighty/content-positioning.json`
- 已接入的 consumer：
  - `novel-genre`
  - `novel-package`
  - `novel-outline`
  - `novel-write`
  - `novel-review`
- 当前 Phase 3 约束已遵守：
  - 组合题材结论只在 Phase 3 接入
  - 未提前回写到 A4 当时已收口的写集历史阶段
- 已同步更新：
  - `shared/templates/state-v5-template.json`
  - `shared/templates/state-schema-v5.json`
  - `shared/references/shared/state-schema.md`
  - `docs/00-当前有效/default-workflows.md`
  - `docs/00-当前有效/start-here.md`
  - `docs/00-当前有效/skill-usage.md`
  - `docs/00-当前有效/state-thinning-and-setting-sync.md`
  - `v1.1-roadmap.md`
- 已新增/扩展测试：
  - `tests/test_content_positioning.py`
  - `tests/test_profile_contract.py`
  - `tests/test_profile_consumers.py`
  - `tests/test_issue_regressions.py`
  - `tests/test_state_contracts.py`
- 本轮验证：
  - `pytest -q tests/test_profile_contract.py tests/test_profile_consumers.py tests/test_content_positioning.py tests/test_issue_regressions.py tests/test_state_contracts.py tests/test_phase2_helpers.py`
    - `31 passed`
## Session Update: 2026-03-26 Phase 4 完成

- 已完成 `Phase 4`：外部资料校准 / C1 / C2。
- 主要落地：
  - 新增当前有效校准文档：
    - `docs/00-当前有效/profile-calibration-and-bucket-mapping.md`
  - 已将该文档挂到：
    - `README.md`
    - `docs/INDEX.md`
  - `v1.1-roadmap.md` 中：
    - `C1` 已改为 `done`
    - `C2` 已改为 `done`
    - `Phase 4` 已改为 `done`
- 当前校准结论：
  - `profile` core 继续承载题材基础约束，不继续膨胀成长篇素材包
  - 继续坚持单主桶
  - `strong_tags / tagpacks / narrative_modes / tone_guardrails` 的职责边界已正式化
  - 组合题材 / 多主题卖点 / 群像结构模式 已纳入映射校准范围
- 最终验证：
  - `pytest -q`
    - `284 passed, 192 subtests passed`
  - `bash scripts/validate-migration.sh`
    - passed
## Session Update: 2026-03-26 Phase 4 口径修正

- 按严谨口径修正 `v1.1-roadmap.md`：
  - `C1` 改为 `in_progress`
  - `C2` 改为 `in_progress`
  - `Phase 4` 改为 `in_progress`
- 当前已完成的是：
  - `Phase 4A`：官方资料校准口径收口
- 当前尚未完成的是：
  - `Phase 4B`：逐 profile 内容升级 / 映射实改 / smoke 验证
- 这样避免把“文档结论收口”误读成“内容层实改已经全部完成”。
## Session Update: 2026-03-26 Phase 4B 首批实改完成

- 已完成首批优先 profile 的内容层实改与映射实改：
  - `shared/templates/content-positioning-map-v1.json`
  - `shared/profiles/palace-intrigue/profile.yaml`
  - `shared/profiles/realistic/profile.yaml`
  - `shared/profiles/xuanhuan/profile-tomato.yaml`
- `content-positioning` builder 现在会优先消费映射默认值，用于：
  - `primary_bucket`
  - `strong_tags`
  - `narrative_modes`
  - `tone_guardrails`
  - `package_cues`
- 当前按“首批优先范围”口径，`Phase 4` 已可收口为 `done`。
## Session Update: 2026-03-26 `v1.2-roadmap` 联网标注

- 已先验证联网能力再给 `v1.2-roadmap` 打标签。
- 已确认：
  - 当前会话可联网
  - `scripts/acquire_source_text.py` 可真实抓取番茄官方页面
- 已为 `v1.2-roadmap` 中各项补：
  - `[local]`
  - `[hybrid]`
  - `[online]`
- 用于区分：
  - 本地结构工作
  - 本地+外部校准混合工作
  - 明显依赖外部资料的工作
## Session Update: 2026-03-26 v1.2 断点恢复与继续推进

- 已恢复当前进度并确认：
  - `A1 / A2 / B2 / C1` 现处于 `in_progress`
- 已完成的本地推进：
  - 扩了第一批 5 个 profile 的 `content-positioning` 映射
  - 为这 5 个 profile 下沉了 `platform_positioning`
  - `B2` 第一批已完成：
    - `urban-brainhole`
    - `workplace-romance`
    - `palace-intrigue`
    - `xiuxian`
    已将主要 legacy embedded reference 收回到 `reference-notes.md`
- 已新增 smoke 文档：
  - `docs/20-研究实验/content-positioning-smoke-2026-03-26.md`
- 当前 smoke 结论：
  - `主 profile` 稳定的项目，`content-positioning` 已可用
  - 只有 `bucket`、没有稳定 `loaded profile` 的项目，当前仍偏保守
## Session Update: 2026-03-27 v1.2 收口

- 已完成 `v1.2` 的主线项：
  - `A1` 扩大 `content-positioning` 映射覆盖
  - `A2` 扩大 `platform_positioning` 下沉范围
  - `B1` 首批 profile 内容字段校准
  - `B2` 主线 profile 的 legacy embedded reference 清理
  - `C1/C2` smoke 与交叉样本验证
  - `D2` `novel-log` 去留判断
- 当前保留 `D1 novel-scan` 为 `deferred`，不阻塞 `v1.2` 收口。
