# Findings & Decisions

## Requirements
- 在当前仓库内自动完成“反脸谱化体系”12 个主模块
- 将该体系接入 `novel-outline` / `novel-review`
- 当前阶段偏“打磨”，因此模板、检查、案例校准都应进入主结构，而不是只做附录
- 新事实需要能被后续工作流与接手者稳定发现

## Research Findings
- 项目级约定要求：复杂任务先调研代码、数据流和现有约定，再实施
- 项目对首次进入仓库的快速入口强调 `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md` 与阶段文档
- `planning-with-files` 适用于超过 5 次工具调用的复杂任务，并要求在项目根创建 `task_plan.md`、`findings.md`、`progress.md`
- `novel-outline` 当前负责上游结构约束，显式读取 `shared` 资产和若干 `docs/` 规则文件，但没有“反脸谱化/群像校准”层
- `novel-review` 当前负责下游质量路由与 state 回写，已有 bucket / technique / tagpack 检查，但没有角色立场、叙事权、群像失衡的统一审计层
- `docs/90-归档/阶段/phase-9-summary.md` 与 `docs/90-归档/阶段/phase-9b-quality-loop-design.md` 已把项目方向收束为“包装生成层 + 质量闭环整合”，新增体系应更像质量闭环扩层，而不是平行新 skill
- `docs/00-当前有效/default-workflows.md` 已把 `novel-outline -> novel-write -> novel-review -> fix/polish/rewrite` 固化为默认主线，因此接线优先级应放在 `outline` 和 `review`
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
  - 并同步挂回 `docs/anti-flattening-framework/README.md` 与 `docs/00-当前有效/default-workflows.md`
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
- 已新增 `docs/90-归档/阶段/phase-17-summary.md`
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
- `docs/00-当前有效/start-here.md`
- `docs/00-当前有效/skill-usage.md`
- `docs/00-当前有效/default-workflows.md`
- `docs/90-归档/阶段/phase-9-summary.md`
- `docs/90-归档/阶段/phase-9b-quality-loop-design.md`
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
- `docs/90-归档/阶段/phase-17-summary.md`
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

# Findings & Decisions: 番茄起盘协议栈与 Compiler 层

## Requirements
- 用户希望在现有项目里找到比“成熟剧情架构库”更好的方案，用于番茄优先路线
- 用户已认可将方案收成正式 spec，并继续进入实施计划
- 第一版目标不是整卷结构，而是“开篇到黄金三章”的起盘与留存闭环

## Research Findings
- 番茄官方“写在落笔前，如何构思一本男频网文小说”更强调：
  - 一句话故事
  - 故事支点
  - 切入事件
  - 三幕式 / 节拍器
  说明平台原生入口并不是“先选一个大结构名”
- 番茄官方“如何稳定剧情，让读者追更不停？”更强调：
  - 首页见山
  - 章末留钩
  - 前十万字稳定
  说明平台级留存规则应该独立成层，而不是藏在某张架构卡里
- 番茄官方“开篇即爆点！三步公式打造高黏性开头（上）”与宫斗经验文都说明：
  - 前三章要不断给期待
  - 主角不应靠低级失误制造压制
  - 早期推进要有真实小兑现与残账
- 通用框架资料（Save the Cat / Story Grid / serial-writing articles）更适合当：
  - 解释语言
  - 映射参考
  - 场景句法校准工具
  而不适合直接作为番茄运行时真源
- 仓库现有最稳定的模式仍然是：
  - `docs/` 承载单一事实源
  - `shared/references/shared/state-schema.md` 承载 state 真值
  - 小脚本承载保守自动化
  - `tests/*.py` 锁文档 / skill / 合同回归
- `opening-and-plot-framework` 已有 Fanqie P0 overlays / checkcards / output contract / smoke 模式，可复用其承载层与测试模式，而不应新造平行框架

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 采用“番茄起盘协议栈 + compiler + 两本账” | 比“单主架构卡”更能表达支点、语法、平台协议、题材义务与场景句法的组合 |
| 运行时对象命名为 `launch_stack` | 比 `plot_architecture_selection` 更贴起盘范围，也避免与整本书结构混淆 |
| 协议栈分为 `Premise / Pivot / Launch Grammar / Retention Protocol / Genre Obligations / Scene Engine` | 保持边界清楚，便于 skill 消费与未来扩展 |
| 第一版仅落实 `Premise / Pivot / Launch Grammar / Retention Protocol / compiler / 轻量写回` | 控制范围，先跑通最有价值的番茄开篇闭环 |
| sidecar 采用 `.mighty/launch-stack.json`，并预留 `.mighty/hook-ledger.json` 与 `.mighty/payoff-ledger.json` | 详细结果与账本不挤进 `state.json`，符合现有轻 state 模式 |
| `state.json` 只镜像 4 个轻字段 | 避免把 `state` 变成第二套方法论中心 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| `writing-plans` 技能默认要求 plan-review subagent，但当前没有用户明确授权委派 | 先由主会话自行写计划并做本地自查；若后续用户明确选择委派执行，再进入 subagent 路线 |

## Resources
- `docs/superpowers/specs/2026-03-24-fanqie-launch-stack-design.md`
- `docs/opening-and-plot-framework/README.md`
- `tests/test_opening_plot_framework.py`
- `tests/test_writing_core_framework.py`
- `shared/references/shared/state-schema.md`
- `https://fanqienovel.com/writer/zone/article/7226296687315124284`
- `https://fanqienovel.com/writer/zone/article/7605818896267870270`
- `https://fanqienovel.com/writer/zone/article/7478303864752455705`
- `https://fanqienovel.com/writer/zone/article/7273042943110283326`
- `https://savethecat.com/tips-and-tactics/free-tool-alert-the-save-the-cat-genre-mapper`
- `https://storygrid.com/wp-content/uploads/2017/04/foolscap-story-grid.pdf`
- `https://storygrid.com/5-commandments-storytelling-revisited/`
- `https://janefriedman.com/serial-novel-writing/`

---

# Findings & Decisions: 2026-03-25 架构审查与扩展路径

## Requirements
- 用户要求检查项目整体架构是否合理
- 用户明确允许使用 agent teams 并行调研
- 需要同时回答“当前是否合理”和“后续继续扩展时应如何处理路径优化、功能新增和治理收口”

## Research Findings
- 当前整体分层方向是合理的：
  - `skills/` 承载行为合同
  - `docs/` 承载方法论与工作流说明
  - `shared/` 承载上游同步资产
  - `scripts/` 承载执行型自动化
  - `projects/` / `smoke/` / `e2e-novel/` 承载样本和验证
- 仓库规模已经进入“架构仍清楚，但承载方式开始变重”的阶段：
  - `skills/` 目录数：31
  - `docs/*.md` 数：271
  - `scripts/` 文件数：20
  - `tests/test_*.py` 数：14
- 高频 skill 已出现规则装载平铺复制：
  - `skills/novel-write/SKILL.md`
  - `skills/novel-review/SKILL.md`
  - `skills/novel-outline/SKILL.md`
  - `skills/novel-precheck/SKILL.md`
  - `skills/novel-package/SKILL.md`
  这些文件都显式列出大量 `../../docs/*` 与 `../../shared/*` 路径，且重复维护规则叠加顺序
- 关键 skill 文档体量已经偏大：
  - `novel-package`: 371 行
  - `novel-precheck`: 350 行
  - `novel-write`: 348 行
  - `novel-review`: 338 行
  - `novel-outline`: 270 行
  - `novel-close`: 197 行
- 全仓 `SKILL.md` 中出现的路径引用已明显偏多：
  - `../../docs/` 383 次
  - `.mighty/` 260 次
  - `设定集/` 117 次
  - `../../shared/` 49 次
- `state` 契约已出现明显漂移：
  - `shared/references/shared/state-schema.md` 声称自己是唯一结构真值
  - 但 `shared/templates/state-v5-template.json` 与其并不同构
  - 明显差异包括：
    - schema 把 `entities.characters.protagonist.location` 写成字符串，模板是对象
    - schema 有 `entities.factions`，模板无该顶层
    - 模板有 `market_adjustments` / `character_states` / `setting_versions` / `dungeons` / `teammates`，schema未完整覆盖
    - `launch_stack_*` 在 schema 的 `chapter_meta` 扩展表中出现，但模板与脚本实际放在 state 顶层
- `shared/` 也已不再是纯镜像：
  - README 仍把它定义为从 `Genm` 同步而来
  - 但仓库里已经存在本仓自增的 `shared/references/*` 与 `shared/templates/*`
  - `sync-shared-from-genm.sh` 仍采用 `rm -rf + cp -R` 的整包覆盖模式，后续有真实覆盖风险
- 入口文档存在职责重叠：
  - `README.md`
  - `docs/00-当前有效/start-here.md`
  - `docs/00-当前有效/default-workflows.md`
  - `docs/00-当前有效/skill-usage.md`
  这四者都在重复主流程、命令示例和 sidecar 说明
- 测试护栏是存在的，而且总体运行健康：
  - `bash scripts/validate-migration.sh` 通过
  - `pytest -q` 通过：`204 passed, 192 subtests passed`
- 但测试结构仍偏“存在性 / token / 链接审计”，对运行时契约一致性的保护不足：
  - `tests/test_repo_path_integrity.py` 只抽查极少数 skill/doc
  - `tests/test_fanqie_launch_stack.py` 与 `tests/test_writing_core_framework.py` 主要校验 token 和产物存在
  - 尚缺针对 `state schema <-> template <-> scripts` 的一致性测试

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 判断当前架构“总体合理，但已接近需要收敛治理的拐点” | 分层方向清楚、验证链存在，但单一事实源与路径治理已开始漂移 |
| 将 `state/schema/template/script` 不一致认定为最高优先级问题 | 这是所有后续扩展最容易放大为系统性漂移的根因 |
| 将 `shared` 镜像假设失效认定为第二优先级问题 | 现有同步脚本具备覆盖本仓活依赖的现实风险 |
| 将 skill 规则装载复制认定为第三优先级问题 | 后续每新增一个规则层，维护成本会以乘法方式增长 |
| 将入口文档收敛和 sidecar 注册表视为扩展期必要治理 | 后续新增平台/功能时，否则先失控的是路径和入口，而不是功能本身 |

## Recommended Roadmap
1. P0：统一 `state` 真值
   - 新增机器可校验的 JSON Schema
   - 让 `state-v5-template.json` 与脚本消费字段对齐
   - 为 `setting_gate` / `fanqie_launch_stack` / `thin-state` / `sync` 补一致性测试
2. P1：补三份静态索引
   - `skills manifest`：目录名 / frontmatter 名 / aliases / 是否安装
   - `reference bundle index`：高频规则包与能力包入口
   - `sidecar registry`：文件名 / owner / 镜像字段 / 消费者 / version
3. P1：收敛入口文档职责
   - `docs/00-当前有效/default-workflows.md` 成为唯一工作流真源
   - `docs/00-当前有效/start-here.md` 只保留首次上手入口
   - `docs/00-当前有效/skill-usage.md` 只保留安装名 / 触发名 / 示例
   - `README.md` 只保留最短启动说明和跳转
4. P2：收窄 skill 边界
   - `novel-outline` 不再继续吸纳 bootstrap / truth-sheet 维护职责
   - `novel-write` 不再继续吸纳 maintenance 叙述
   - `novel-sync` 聚焦同步，不再承担 thin-state / guidance split 叙述
5. P2：shared 治理改造
   - 明确区分“源仓同步资产”和“本仓扩展资产”
   - `sync-shared-from-genm.sh --report-json` 输出差异文件、orphan、影响域
   - 给本仓额外 shared 资产建立白名单或独立扩展目录
6. P3：维护链轻量编排
   - 把 `project-maintenance.py` 的硬编码步骤抽成轻量 pipeline manifest
   - 不做插件系统，只做顺序、条件和阻断关系声明

## Risks
- `state` 统一会波及样本项目、smoke 项目和多个脚本，迁移时必须配回归
- skill 路径清单收缩后，模型短期可能少读某些关键文档，需要 smoke 校准
- 安装 manifest 上线后要兼容保留 `novel-*` 与 `genm-novel-*`
- sidecar registry 若继续手工维护，会变成新的第二事实源，因此应优先生成或强测试约束

## Resources
- `README.md`
- `docs/INDEX.md`
- `docs/10-进行中/architecture-open-issues.md`
- `docs/00-当前有效/start-here.md`
- `docs/00-当前有效/default-workflows.md`
- `docs/00-当前有效/skill-usage.md`
- `docs/90-归档/阶段/phase-9-summary.md`
- `docs/90-归档/阶段/phase-7b-selective-sync-governance.md`
- `docs/00-当前有效/shared-asset-dependency-map.md`
- `docs/00-当前有效/state-thinning-and-setting-sync.md`
- `skills/novel-init/SKILL.md`
- `skills/novel-outline/SKILL.md`
- `skills/novel-write/SKILL.md`
- `skills/novel-review/SKILL.md`
- `skills/novel-precheck/SKILL.md`
- `skills/novel-package/SKILL.md`
- `skills/novel-sync/SKILL.md`
- `shared/references/shared/state-schema.md`
- `shared/templates/state-v5-template.json`
- `scripts/install-skills.sh`
- `scripts/validate-migration.sh`
- `scripts/sync-shared-from-genm.sh`
- `scripts/setting_gate.py`
- `scripts/project-maintenance.py`
- `scripts/fanqie_launch_stack.py`
- `tests/test_repo_path_integrity.py`
- `tests/test_markdown_link_audit.py`
- `tests/test_issue_regressions.py`
- `tests/test_setting_gate.py`
- `tests/test_fanqie_launch_stack.py`
- `tests/test_writing_core_framework.py`

## Recheck After Commit `a953957`
- 最新提交 `a953957 Turn Genm-codex into a more transactional and sidecar-driven writing system` 明显扩大了架构审查范围：
  - 新增 `chapter transaction`
  - 新增 `.mighty/active-context.json`
  - 新增 `.mighty/volume-summaries.json`
  - 新增 `.mighty/import-report.json`
  - 新增 `post_write_lint`
- 这次升级的方向整体是加分项：
  - 它没有引入独立 CLI/runtime
  - 仍然围绕现有 `docs + skills + scripts + sidecars` 骨架增强默认工作流
  - `import-report` / `volume-summaries` / `active_context` 的边界总体克制
- 但它也把原本已经存在的两类问题进一步放大：
  1. `state/schema/template/script` 契约未统一
  2. `shared` 仍是可被整域覆盖的同步目录，但现在又继续承载 repo-local contract/template
- 本轮最新确认的问题：
  - `shared/references/shared/state-schema.md` 顶部示例仍是旧 shape，且与 `shared/templates/state-v5-template.json`、`scripts/split-runtime-guidance.py` 的 externalized shape 不一致
  - `scripts/build_active_context.py` 对 `factions.active` / `items.tracked` 的消费 shape 与 `state-schema.md` 不一致，会静默丢失 schema 合法数据
  - `recent_guardrails` 现在既存在 `.mighty/learned-patterns.json`，又被复制进 `.mighty/active-context.json`，有 sidecar freshness drift 风险
  - `shared/references/shared/chapter-transaction-schema.md` 与 `shared/templates/workflow-state-v2.json` 已形成良好契约，但 `project-maintenance.py` / `post-task-maintenance.py` 还没有真正把 workflow-state 写回成机械闭环
  - `scripts/post_write_lint.py` 直接 `import strong_quality_gate`，在根目录执行相关 unittest 时会触发 `ModuleNotFoundError`
  - `scripts/sync-shared-from-genm.sh` 仍保留 `rm -rf + cp -R` 语义，而 `shared/` 已含 repo-only 文件与同名漂移文件，真实覆盖风险仍在
- 本轮重新确认的结论：
  - 当前架构“方向合理，复杂度也有一部分是必要复杂度”
  - 真正值得优先治理的是：
    - `state/schema/template/script` 机械真值层
    - `shared` 同步目录与 repo-local contract 的分离
    - 顶层入口文档职责收口
    - maintenance 最终态与 sidecar 生命周期的一致性验证
- 本轮验证结果：
  - `pytest -q` 通过：`248 passed, 192 subtests passed`
- `bash scripts/validate-migration.sh` 通过
  - 但针对 `post_write_lint` 的定向 unittest 在仓库根实跑会因导入路径报错
- 已新增长期治理台账：
  - `docs/10-进行中/architecture-open-issues.md`
  - 用于记录当前确认但尚未完全收口的问题，而不是继续只停留在会话或 memory 中

---

# Findings & Decisions: 写作基本功与内容标准规则层

## Requirements
- 用户希望把 `写作基本功 / 剧情层次 / 内容标准` 做成类似反脸谱化框架的项目级方法论文档
- `memory` 层只沉淀可执行的压缩信号，不存整套课程
- `包装层` 需要能直接消费“开篇方法 / 类型化开篇差异 / 精品审核标准”

## Research Findings
- `剧情层次` 这一层已经由 `docs/opening-and-plot-framework/` 跑通，适合继续作为单一事实源复用
- 当前真正缺的不是另一套剧情层次文档，而是：
  - 正文执行层的 `写作基本功`
  - review / precheck 可消费的 `内容标准`
  - `learned_patterns` / `chapter_meta` 可落地的压缩信号约定
  - `novel-package` 可直接读取的开篇包装输入接口
- `shared/references/shared/state-schema.md` 与 `docs/00-当前有效/state-thinning-and-setting-sync.md` 已明确 state 应保持轻量，适合继续把新增信号压在 `learned_patterns` 和 `chapter_meta`
- `docs/fanqie-writing-techniques.md` 与 `docs/research/fanqie/fanqie-writer-zone-lessons.md` 提供了足够的源材料，但此前仍以提炼文档形态存在，没有被重组为新的方法论框架
- 本轮已新增 `docs/writing-core-framework/`，包含：
  - `README.md`
  - `01-写作基本功总纲.md`
  - `02-叙述-镜头-信息投放.md`
  - `03-对白-动作-情绪-段落节奏.md`
  - `04-剧情层次与多线编排接口.md`
  - `05-内容标准与常见失格.md`
  - `06-精品审核与投稿前判断.md`
  - `07-memory-压缩信号约定.md`
  - `08-开篇包装输入接口.md`
- `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` / `novel-learn` 已完成显式读取接线
- `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md` 已增加新框架入口
- `shared/templates/state-v5-template.json` 已增加：
  - `learned_patterns.opening_strategy`
  - `learned_patterns.multi_line_guardrails`
  - `learned_patterns.content_standard_alerts`
  - `chapter_meta[N].content_standard_flags`
  - `chapter_meta[N].packaging_alignment_note`
- `shared/references/shared/state-schema.md` 已把上述字段收成轻量约定，而不是新顶层 state 中心
- 新增测试 `tests/test_writing_core_framework.py` 已完成红绿闭环
- 回归测试 `tests/test_opening_plot_framework.py` 仍通过，说明本轮没有破坏既有开篇框架合同
- `bash scripts/validate-migration.sh` 通过，说明结构层改动没有破坏迁移校验
- 已新增真实样本文档：
  - `docs/writing-core-framework/real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md`
- 已补第二条异路数真实样本文档：
  - `docs/writing-core-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md`
- 已将两条样本最初的 `packaging-needs-update = yes` 继续闭成真实包装产物：
  - `projects/宗门垫底那年，我把废丹卖成了天价/包装/包装方案.md`
  - `projects/离婚冷静期那天，前夫把董事会席位押给了我/包装/包装方案.md`
- 已为这两条样本补自动回归护栏：
  - `tests/test_writing_core_framework.py` 现在会校验：
    - 两份真实 smoke 文档存在
    - 两份 `包装/包装方案.md` 存在且包含标题/简介
    - 两个样本项目的 `learned_patterns` 已含压缩信号
    - 两个样本项目的 `state.chapter_meta["003"]` 已含 `content_standard_flags / packaging_alignment_note`
- 已在样本项目 `projects/宗门垫底那年，我把废丹卖成了天价` 中做最小 writeback：
  - `.mighty/learned-patterns.json` 增加：
    - `opening_strategy`
    - `multi_line_guardrails`
    - `content_standard_alerts`
  - `.mighty/state.json` 增加或刷新：
    - `learned_patterns.available_sections`
    - `chapter_meta["003"].content_standard_flags`
    - `chapter_meta["003"].packaging_alignment_note`
    - `constraints_loaded.includes += docs/writing-core-framework/README.md`
- 这条样本给出的收口判断是：
  - `投稿建议 = ready-now`
  - `packaging-needs-update = yes`
  - 原因不是正文不过关，而是当前项目还没有外层包装文件，且第 4-5 章前不宜把“丹院黑幕已揭开”包装成已兑现卖点
- 已在第二个样本项目 `projects/离婚冷静期那天，前夫把董事会席位押给了我` 中做最小 writeback：
  - `.mighty/learned-patterns.json` 增加：
    - `opening_strategy`
    - `multi_line_guardrails`
    - `content_standard_alerts`
  - `.mighty/state.json` 增加：
    - `learned_patterns.available_sections`
    - `chapter_meta["003"].content_standard_flags`
    - `chapter_meta["003"].packaging_alignment_note`
- 第二条样本给出的收口判断是：
  - `投稿建议 = ready-now`
  - `packaging-needs-update = yes`
  - 原因不是黄金三章不过关，而是“合伙人”位置还没兑现成后续真实控制权，不宜提前包装成已赢下董事会或家族盘
- 现阶段这两条样本的 `packaging-needs-update = yes` 已不再停在判断层，而是已经被消化成新的 `包装/包装方案.md`
- 现阶段这条线不仅有产物，还已有自动测试守护，不会因为后续文档或样本漂移悄悄失效
- 已新增 `scripts/writing_core_smoke.py`
  - 目标是把当前 `writing-core-framework` 的真实样本收口流程收成最小可复用 helper
  - 当前支持：
    - `draft`
    - `writeback`
    - `save-packaging`
  - 当前输出：
    - `packaging_judgment`
    - `precheck_summary`
    - `content_standard_summary`
    - `writeback_preview`
- 已新增 `tests/test_writing_core_smoke.py`
  - 校验 CLI 默认参数
  - 校验真实项目 draft 输出结构
  - 校验临时项目 `writeback + save-packaging` 会真正写回压缩信号和包装文件
- 已用 `scripts/writing_core_smoke.py` 跑通第三条脚本化真实样本：
  - `docs/writing-core-framework/real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-2026-03-24.md`
  - `projects/搬回老小区后，我靠蹭饭认识了整栋楼/包装/包装方案.md`
- 为了避免“能跑但文案脏”的伪闭环，已补 city-daily 质量护栏：
  - `tests/test_writing_core_smoke.py` 现在会拦：
    - outline 标题被错误拼进 synopsis
    - 产出的包装文件含脏 markdown 标题
- `tests/test_writing_core_framework.py` 现在已把第三条脚本化样本也纳入回归集合
- 已为 `writing_core_smoke.py` 增加更细的 bucket 特化模板：
  - `历史脑洞`
  - `职场婚恋`
- 已用 `scripts/writing_core_smoke.py` 跑通第四条脚本化真实样本：
  - `docs/writing-core-framework/real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-2026-03-24.md`
  - `projects/我在县衙当杂吏，靠翻旧案升了堂/包装/包装方案.md`
- `tests/test_writing_core_smoke.py` 现在会校验：
  - `历史脑洞` draft 输出含 `卷宗回响 / 旧案 / 制度压力和翻案脑洞`
  - `职场婚恋` draft 输出含 `升职接锅 / 合租揭面 / 试运行窗口`
- `tests/test_writing_core_framework.py` 现在已把第四条样本也纳入回归集合
- 已继续为 `writing_core_smoke.py` 增加更细的 bucket 特化模板：
  - `青春甜宠`
  - `都市脑洞`
- 已用 `scripts/writing_core_smoke.py` 跑通第五条脚本化真实样本：
  - `docs/writing-core-framework/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md`
  - `projects/她升职那天，前上司成了我合租室友/包装/包装方案.md`
- 为避免 `职场婚恋` 总纲中的 YAML / fenced block 污染包装简介，`extract_outline_pitch` 已升级为跳过整个 fenced block，而不只跳过 fence 标记行
- `tests/test_writing_core_smoke.py` 现在会额外校验：
  - `青春甜宠` draft 输出含 `身份错认 / 学习互助`
  - `都市脑洞` draft 输出含 `到账`
  - `职场婚恋` writeback 产物不再落成 `书名:` 这类脏简介
- `tests/test_writing_core_framework.py` 现在已把第五条样本也纳入回归集合
- 已用 `scripts/writing_core_smoke.py` 跑通第六类常用模板能力：
  - `青春甜宠` draft 模板
  - `都市脑洞` draft 模板
- 已用 `scripts/writing_core_smoke.py` 跑通第五条真实脚本化样本：
  - `docs/writing-core-framework/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md`
  - `projects/她升职那天，前上司成了我合租室友/包装/包装方案.md`
- 当前 `writing_core_smoke.py` 已覆盖的显式 bucket 模板为：
  - `玄幻脑洞`
  - `豪门总裁`
  - `都市日常`
  - `历史脑洞`
  - `职场婚恋`
  - `青春甜宠`
  - `都市脑洞`
- 已用 `scripts/writing_core_smoke.py` 跑通第六条真实脚本化样本：
  - `docs/writing-core-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md`
  - `projects/转学第一天，我把校草认成了新来的代课老师/包装/包装方案.md`
- 已新增 `scripts/batch_writing_core_smoke.py`
  - 当前支持通过 manifest + output dir 批量跑多个项目的 `draft` / `writeback`
- 已新增 `tests/test_batch_writing_core_smoke.py`
  - 校验 manifest 参数解析
  - 校验两项目 batch draft 会真实生成多个输出文件
- batch 入口现已支持：
  - `writeback`
  - `save-packaging`
  - `summary_report`
- 已用 `scripts/writing_core_smoke.py` 跑通第七条真实脚本化样本：
  - `docs/writing-core-framework/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md`
  - `projects/我赔光积蓄那天，系统先把违约金打到了账上/包装/包装方案.md`
- 当前 `writing_core_smoke.py` 的显式 bucket 模板已覆盖：
  - `玄幻脑洞`
  - `豪门总裁`
  - `都市日常`
  - `历史脑洞`
  - `职场婚恋`
  - `青春甜宠`
  - `都市脑洞`
- 已用 `scripts/writing_core_smoke.py` 跑通 `宫斗宅斗` 脚本化样本：
  - `docs/writing-core-framework/real-project-smoke-继母换我婚书那夜-太子先开了口-2026-03-24.md`
  - `projects/庶妹换我婚书那夜，太子先开了口/包装/包装方案-writing-core.md`
- 对已有更成熟包装产物的项目，`save-packaging` 现已支持 sidecar 策略：
  - 保留原 `包装/包装方案.md`
  - 新增 `包装/包装方案-writing-core.md`
  - `packaging_status = written-sidecar`
- 已新增仓库内固定 batch 基线：
  - manifest: `docs/writing-core-framework/batch-smoke-manifest.json`
  - output dir: `docs/writing-core-framework/batch-output/`
  - summary report: `docs/writing-core-framework/batch-output/summary-report.json`
- 固定 batch 基线当前已覆盖：
  - `宫斗宅斗`
  - `豪门总裁`
  - `都市日常`
  - `玄幻脑洞`
  - `历史脑洞`
  - `青春甜宠`
  - `职场婚恋`
  - `都市脑洞`
- `docs/writing-core-framework/batch-output/summary-report.json` 现已从原始列表升级为聚合报告，包含：
  - `generated_at`
  - `mode`
  - `count / success_count / failure_count`
  - `bucket_counts`
  - `packaging_status_counts`
  - `writeback_status_counts`
  - `failed_projects`
- 固定 batch output 目录现在已 materialize：
  - `real-project-smoke-继母换我婚书那夜-太子先开了口-2026-03-24.md`
  - `real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md`
  - `real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-2026-03-24.md`
  - `real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md`
  - `real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-2026-03-24.md`
  - `real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md`
  - `real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md`
  - `real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md`
- `tests/test_batch_writing_core_smoke.py` 现在会校验：
  - batch `writeback + save-packaging + summary_report`
  - summary report 中的项目结果统计
- `tests/test_writing_core_framework.py` 现在已把：
  - 第八条宫斗样本
  - 固定 batch manifest
  - 固定 batch output 文件
  一并纳入回归集合

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 新框架命名为 `writing-core-framework` | 让框架名覆盖 craft / standard / memory / packaging input，而不是错误暗示只管剧情 |
| `04-剧情层次与多线编排接口.md` 只做桥接，不做理论重写 | 保持 `opening-and-plot-framework` 作为剧情层次真源 |
| 仅向 `learned_patterns` 与 `chapter_meta` 注入压缩字段 | 符合“只沉淀可执行压缩信号”的 memory 目标 |
| 用真实项目做 report + 最小 writeback，而不是只停在 smoke 文档 | 让 `writing-core-framework` 同时在 package / precheck / memory 三层都落到仓库证据 |
| 第二条样本优先选现实豪门线 | 用和玄幻脑洞明显不同的路数验证“类型化开篇差异”和包装约束不是单题材特化 |
| 自动化优先做最小 smoke helper，而不是上来造完整 workflow 引擎 | 当前最高收益是把手工闭环变成可重复执行的最小工具，而不是过度工程 |
| 第三条样本优先用 `都市日常` 路线并通过脚本生成 | 这样能同时验证跨 bucket 能力和自动化工具链，不只是再手工补一条案例 |
| 第四条样本优先选 `历史脑洞`，同时为 `职场婚恋` 补模板 | 这样既验证另一条完全不同的制度型路线，也让脚本的 bucket 特化能力从 3 类扩到 5 类 |
| 第五条样本优先选 `职场婚恋`，同时补 `青春甜宠 / 都市脑洞` 模板 | 这样既把现实职场关系线也打进真实样本，又把显式模板继续扩到更常用的番茄路数 |
| 第六条样本优先选 `青春甜宠`，同时补 batch 入口 | 这样既补足校园甜宠线真实闭环，也让工具链从单项目执行推进到多项目批处理 |
| 第七条样本优先选 `都市脑洞`，并补 batch summary report | 这样既把最后一类常用都市系统流样本落地，也让批处理入口具备真正可消费的批量结果摘要 |
| `宫斗宅斗` 采用 sidecar 包装文件而不是覆盖现有主包装 | 该项目已有人工收口版包装，脚本化能力应补强而不是破坏已有高质量产物 |
| 固定 batch 基线先用 `draft` 跑 3 条代表性样本 | 这样能拿到稳定、低风险、可持续更新的仓库内批跑基线，再逐步扩到更激进的 writeback 基线 |
| 固定 batch 基线扩到 8 个 representative buckets | 让仓库内长期基线真正覆盖当前显式模板集，而不是只覆盖 3 条轻量样本 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| 大补丁在 `novel-precheck` 上下文对齐失败 | 改为逐文件小补丁，降低 skill 合同修改风险 |

---
*Update this file after every 2 view/browser/search operations*
*This prevents visual information from being lost*

---

# Findings & Decisions: 开篇方法与剧情层次规则层

## Requirements
- 用户希望把“开篇方法 + 剧情层次”落成默认工作流规则层
- 第一版做跨题材通用版，不先绑定单一题材或单一平台桶
- 范围是：文档框架 + `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` 全接线

## Research Findings
- 当前仓库最稳的承载方式仍是：`docs/` 方法论文档作为单一事实源，skill 通过显式相对路径读取
- `docs/anti-flattening-framework/README.md` 已提供成熟模板：
  - `README + 模块文档 + skill 读取包 + 规则优先级`
- `docs/90-归档/阶段/phase-9-summary.md` 说明项目主方向仍是“包装生成层 + 质量闭环整合”，因此新框架应作为默认工作流规则层接入，而不是独立实验能力
- `skills/novel-write/SKILL.md`、`skills/novel-outline/SKILL.md`、`skills/novel-review/SKILL.md` 已支持按需读取多组项目内文档，说明新增框架不需要新建命令
- `skills/novel-review/SKILL.md` 已有 `chapter_meta[chapter].dimension_scores` 写回位点，适合承载轻量增强评分键
- `shared/references/shared/state-schema.md` 已明确：
  - 不要为局部规则新造顶层 state 中心
  - 可通过 `chapter_meta` 和可选评分键做轻量持久化
- `docs/fanqie-writing-techniques.md` 已有对“开头与黄金三章”“剧情稳定与悬念交替”的项目级提炼，可作为这次通用框架的重要参考，而不必从零起草
- 仓库当前是脏工作树，且 `README.md`、`docs/00-当前有效/default-workflows.md`、`docs/00-当前有效/skill-usage.md`、若干 skill 已有未提交改动；本次必须局部增量修改，不能回滚既有内容
- 已新增 `docs/opening-and-plot-framework/`：
  - `README.md`
  - `01-开篇目标与成功标准.md`
  - `02-开篇构件与组合公式.md`
  - `03-开篇故障与修正.md`
  - `04-剧情层次模型.md`
  - `05-推进链与残账设计.md`
  - `06-题材特化接口.md`
- `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` 已完成显式路径接线
- `README.md`、`docs/00-当前有效/start-here.md`、`docs/00-当前有效/skill-usage.md`、`docs/00-当前有效/default-workflows.md` 已补新框架入口
- `shared/references/shared/state-schema.md` 与 `shared/templates/state-v5-template.json` 已补轻量评分键：
  - `开篇抓力`
  - `层次清晰度`
  - `推进有效性`
- 新增测试 `tests/test_opening_plot_framework.py` 已完成红绿闭环：
  - 红灯：框架文件、skill 路径、入口文档和评分键说明缺失
  - 绿灯：`python -m unittest tests.test_opening_plot_framework -v` 通过
- `bash scripts/validate-migration.sh` 通过，说明新增框架与接线没有破坏迁移结构
- 番茄官方近年活动可支持第一批特化优先级判断：
  - 2025-12-26《2026年番茄小说年度作家福利》明确列出 2026 新引力重点主分类：
    - `豪门总裁`
    - `宫斗宅斗`
    - `职场婚恋`
    - `青春甜宠`
    - `都市日常`
    - `玄幻脑洞`
    - `都市脑洞`
    - `历史脑洞`
  - 2025-07-11《2025夏季灵感·暑期征文活动》再次出现：
    - `玄幻脑洞`
    - `都市脑洞`
    - `都市日常`
    - `历史脑洞`
    - `青春甜宠`
  - 2026-03-20《山河遐思，历史映照》提供了历史文化向补充梯队：
    - `历史古代`
    - `东方仙侠`
    - `传统玄幻`
    - `年代`
    - `都市脑洞`
    - `历史脑洞`
- 已新增：
  - `docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/README.md`
  - `docs/opening-and-plot-framework/fanqie-p0-overlays/*.md` 共 8 张 P0 特化卡
- `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` 已增加：
  - `../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
  - `../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md`
  的条件读取路径
- 已基于本地 `shared/templates/genres/*.md` 与 `shared/profiles/*/profile*.yaml`，把 8 张 P0 卡统一升级为中等深度版
- 当前 8 张卡统一结构为：
  - `开篇公式`
  - `黄金三章最低要求`
  - `剧情层次重点`
  - `高频故障清单`
  - `precheck 专项检查点`
- 扩展后的 `tests/test_opening_plot_framework.py` 现在不仅校验文件存在和接线，还校验 8 张 P0 卡的统一结构
- 已新增 `docs/opening-and-plot-framework/fanqie-p0-checkcards/`，包含 8 张 bucket 级专项检查卡
- `fanqie-p0-checkcards/` 与 `fanqie-p0-overlays/` 的职责已经分开：
  - `overlays` 负责“怎么写”
  - `checkcards` 负责“review / precheck 优先看什么、拦什么”
- `novel-review` 与 `novel-precheck` 已新增：
  - `../../docs/opening-and-plot-framework/fanqie-p0-checkcards/<bucket>.md`
  的条件读取路径
- 新增专项检查卡结构统一为：
  - `自动触发范围`
  - `对 novel-review`
  - `对 novel-precheck`
  - `核心检查问题`
  - `红灯判定`
- 已新增 `docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
- `novel-review` 现在允许在命中 Fanqie P0 bucket 时输出：
  - `fanqie_bucket_review_summary`
- `novel-precheck` 现在允许在命中 Fanqie P0 bucket 时输出：
  - `fanqie_bucket_precheck_summary`
- `shared/references/shared/state-schema.md` 与 `shared/templates/state-v5-template.json` 已补轻量 bucket 字段：
  - `fanqie_bucket_flags`
  - `fanqie_bucket_summary`
- 这些字段仍然挂在 `chapter_meta` 下，没有新造顶层状态中心
- 已对真实项目 `projects/庶女谋略` 做只读样本验证：
  - `meta.platform = 番茄`
  - `meta.genre = 宫斗宅斗`
  - 可稳定写出 `fanqie_bucket_review_summary`
  - 可稳定写出 `fanqie_bucket_precheck_summary`
- 样本文档：
  - `docs/opening-and-plot-framework/real-project-smoke-shunvmoulue-fanqie-p0-2026-03-23.md`
- 初步结论：
  - `庶女谋略` 前三章的宫斗宅斗开篇样本当前可判 `submission_fit = fit`
  - 第003章的 bucket review 可判 `bucket_grade = pass`
  - 但第004-005章必须尽快把“知足守礼”转成具体资源压缩，否则 bucket 档位会掉到 `warn`
- 现在已经把真实样本写回到：
  - `projects/庶女谋略/.mighty/state.json -> chapter_meta["003"]`
- 实际写回字段为：
  - `fanqie_bucket_flags = []`
  - `fanqie_bucket_summary.bucket = "宫斗宅斗"`
  - `fanqie_bucket_summary.bucket_grade = "pass"`
  - `fanqie_bucket_summary.recommended_focus = "chapter4-5 要尽快把“知足守礼”转成具体的月例、药材、炭火、针线压缩，不要只停在口风层"`
- 这说明：
  - 正向 bucket 判断也可以稳定写回
  - 不必等到出现红灯才有 bucket 字段
- 已新增可复用 smoke 模板：
  - `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`
- 该模板现在提供：
  - 项目前提检查
  - `novel-review` 样本模板
  - `novel-precheck` 样本模板
  - 可选写回记录模板
  - 最终结论模板
- 这意味着后续换别的番茄项目时，不需要再从零发明 smoke 文档结构
- 已完成第二个真实项目的跨项目 smoke：
  - `projects/庶妹换我婚书那夜，太子先开了口`
- 产物：
  - `docs/opening-and-plot-framework/real-project-smoke-hunshu-taizi-fanqie-p0-2026-03-23.md`
- 结论：
- 同一份 `fanqie-p0-smoke-template.md` 可跨项目复用
- 即使同属 `宫斗宅斗`，不同开篇强度与兑现速度的项目也能稳定产出 bucket 摘要
- 当前第二个项目更适合先停在只读 smoke，而不是立刻做第二次真实写回
- 已新增脚本：
  - `scripts/fanqie_p0_smoke.py`
- 第一版已实现：
  - `scaffold`
  - `draft`（默认）
  - `writeback`
- 当前 v1 已验证的行为：
  - `parse_args` 默认 `mode = draft`
  - `infer_bucket` 优先 `genre_profile.bucket`，回退 `meta.genre`
  - unsupported bucket 自动降级为 `scaffold-only`
  - `draft` 模式对 `宫斗宅斗` 可生成非空 bucket 摘要草稿
  - `writeback` 模式必须显式带确认标志
  - `writeback` 只写：
    - `fanqie_bucket_flags`
    - `fanqie_bucket_summary`
  - 若目标章节已有 bucket 摘要，默认报 `conflict` 不覆盖
- 脚本已对两个真实项目完成 `draft` 模式试跑：
  - `projects/庶女谋略`
  - `projects/庶妹换我婚书那夜，太子先开了口`
- `v1.1` 已新增：
  - `confidence`
  - `evidence_count`
  - `evidence_sources`
  - `writeback_preview`
- `v1.1` 已支持读取本地 sidecar：
  - `.mighty/market-adjustments.json`
  - `.mighty/learned-patterns.json`
- sidecar 当前只作为辅助信号使用：
  - 进入 `signals_used`
  - 参与 `confidence` 与 preview 信息
  - 不覆盖主 bucket 判断
- 对非 `宫斗宅斗` 的其他 P0 bucket，当前策略是：
  - 证据足够时可生成 `draft`
  - 但 `bucket_grade / submission_fit` 先保持 `draft`
  - `confidence` 默认偏低
- 已完成 `fanqie_p0_smoke.py v1.1` 的样本压测矩阵：
  - `projects/庶女谋略`
  - `projects/庶妹换我婚书那夜，太子先开了口`
  - `smoke/e2e-tianchong`
  - `smoke/e2e-tianchong-evil`
  - `smoke/e2e-qinggan-evil-antiflattening-20260322`
  - `smoke/e2e-dual-substitute-evil-antiflattening-20260322`
  - `smoke/e2e-system-antiflattening-20260322`
- 压测结果表明：
  - `宫斗宅斗` 路线可稳定输出 `high confidence draft`
  - `现言甜宠 -> 青春甜宠` alias 已生效，但仍受证据门槛约束：
    - `smoke/e2e-tianchong-evil` 与 `smoke/e2e-dual-substitute-evil-antiflattening-20260322` 当前可输出 `low confidence draft`
    - `smoke/e2e-tianchong` 当前因证据不足降级为 `scaffold-only`
  - `现实情感 / 系统流` 当前会保守降级成 `scaffold-only`
  - 工具当前边界清晰，没有因为“番茄项目”而假装高置信命中
- 新增结果文档：
  - `docs/opening-and-plot-framework/fanqie-p0-pressure-results-2026-03-24.md`
- 已完成第二条真实写回样本：
  - 项目：`projects/转学第一天，我把校草认成了新来的代课老师`
  - 章节：`chapter_meta["003"]`
  - 写回字段：
    - `fanqie_bucket_flags = []`
    - `fanqie_bucket_summary.bucket = "青春甜宠"`
    - `fanqie_bucket_summary.bucket_grade = "pass"`
- 这说明：
  - `青春甜宠` 已从“低置信草稿”推进到“中置信、可给出 `pass / fit` 的轻量写回样本”
  - 当前轻量写回仍然只落 `fanqie_bucket_flags / fanqie_bucket_summary`，不越权改正式 review 主字段
- 现已完成第三条真实写回样本：
  - 项目：`projects/公司裁我那天，系统先赔了我一百万`
  - 章节：`chapter_meta["003"]`
  - 写回字段：
    - `fanqie_bucket_flags = []`
    - `fanqie_bucket_summary.bucket = "都市脑洞"`
    - `fanqie_bucket_summary.bucket_grade = "warn"`
- 这说明：
  - `都市脑洞` 真实项目也已完成中置信轻量写回样本
  - 当前工具已拥有：
    - `宫斗宅斗` 高置信写回样本
    - `青春甜宠` 中置信写回样本
    - `都市脑洞` 中置信写回样本
- 已完成两个真实非宫斗 P0 项目验证：
  - `projects/转学第一天，我把校草认成了新来的代课老师`
  - `projects/公司裁我那天，系统先赔了我一百万`
- 结果：
  - `青春甜宠` 真实项目可稳定输出结构化 `draft`，并已收紧到 `medium confidence + pass / fit`
  - `都市脑洞` 真实项目可稳定输出结构化 `draft`，并已收紧到 `medium confidence + warn / fit`
  - 两条线都能输出：
    - `fanqie_bucket_review_summary`
    - `fanqie_bucket_precheck_summary`
    - `confidence`
    - `evidence_count`
    - `signals_used`
    - `writeback_preview`
  - 当前两条线的 `confidence` 已提升到 `medium`
  - 当前判断收束为：
    - `青春甜宠`：`pass / fit`
    - `都市脑洞`：`warn / fit`
  - 这说明非宫斗 P0 真实项目已经从“能跑”推进到“能给更明确的结构判断”
- 已继续扩到另外三条真实非宫斗 P0 项目：
  - `projects/她升职那天，前上司成了我合租室友`
  - `projects/搬回老小区后，我靠蹭饭认识了整栋楼`
  - `projects/宗门垫底那年，我把废丹卖成了天价`
- 这三条线当前都已满足：
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`
  - `chapter_meta["003"]` 已完成轻量 writeback
- 为支撑这轮扩展，`fanqie_p0_smoke.py` 新增了三类真实 bucket 抓手：
  - `职场婚恋`：`代理 / 甲方 / 合租 / 试运行`
  - `都市日常`：`燃气 / 白板 / 换饭 / 康复`
  - `玄幻脑洞`：`碎纹丹秤 / 废火丹 / 外门小集 / 灵石`
- `writeback` 路径还补了两个真实边界：
  - 空占位 `fanqie_bucket_summary = {}` 不再误判为冲突
  - 同一 summary 重跑时返回 `already-written`，不再把真实样本误报成冲突
- 已新增 `docs/opening-and-plot-framework/fanqie-p0-gap-tracker-2026-03.md`
  - 把当前已覆盖桶、仍缺真实样本的桶、推荐补桶顺序和下一批项目提示词固化下来
  - 当前推荐顺序为：
    - 第三条 `都市脑洞`
    - 第三条 `豪门总裁`
    - 第三条 `玄幻脑洞`
    - 第三条 `历史脑洞`
- 已继续补齐最后两个 `P0` 缺口桶：
  - `projects/我在县衙当杂吏，靠翻旧案升了堂`
  - `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人`
- 当前这两条线也已满足：
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`
  - `chapter_meta["3"/"003"]` 已完成轻量 writeback
- `fanqie_p0_smoke.py` 进一步补了两类真实 bucket 抓手：
  - `历史脑洞`：`县衙 / 旧案 / 卷宗 / 主簿房`
  - `豪门总裁`：`离婚协议 / 董事会 / 合伙人 / 试运营`
- 为兼容新项目 state，还补了一个写回边界：
  - `chapter_meta` 若使用 `3 / 003` 这样的双风格键，脚本会优先回写到项目当前已存在的键风格
- 到这里，当前 `P0 8 桶` 已全部完成至少 1 条真实项目 smoke + 轻量 writeback 样本
- 已新增第二条 `历史脑洞` 真实样本：
  - `projects/我在县衙誊旧档，靠半页供词改了判词`
  - 当前也已收敛到 `confidence = medium / pass / fit`
  - 这说明 `历史脑洞` 当前门槛已经不只由单一县衙旧案样本支撑
- 已继续补第二条样本：
  - `豪门总裁`：`projects/离婚冷静期那天，前夫把董事会席位押给了我`
  - `都市脑洞`：`projects/我赔光积蓄那天，系统先把违约金打到了账上`
  - `玄幻脑洞`：`projects/外门药田被夺那天，我靠废丹拍卖赚回了灵石`
- 这三条当前已分别收敛到：
  - `豪门总裁`：`medium / pass / fit`
  - `都市脑洞`：`medium / warn / fit`
  - `玄幻脑洞`：`medium / pass / fit`
- 已继续补第二条样本：
  - `职场婚恋`：`projects/代理续约那天，我和前搭档被公司按进了同一套合租房`
  - `青春甜宠`：`projects/广播站误放表白信那天，我和学神被迫参加学习互助`
  - `都市日常`：`projects/母亲复健那年，我把楼道白板改成了换饭地图`
- 这三条当前已分别收敛到：
  - `职场婚恋`：`medium / pass / fit`
  - `青春甜宠`：`medium / pass / fit`
  - `都市日常`：`medium / pass / fit`
- 到这里，当前 `P0 8 桶` 已全部完成双样本覆盖

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 新框架目录命名为 `docs/opening-and-plot-framework/` | 同时覆盖开篇方法与剧情层次，且便于 skill 用英文目录稳定引用 |
| 结构采用 `README + 6 个主模块` | 对齐现有方法论框架风格，同时控制第一版体量 |
| 为 `review` / `state-schema` 增加可选评分键 `开篇抓力 / 层次清晰度 / 推进有效性` | 让接线不止停在“能读到规则”，还能轻量沉淀结果 |
| 通过 Python `unittest` 先加失败测试 | 让本轮文档/合同改动也有最小可重复验证闭环 |
| 番茄第一批特化先做 `P0 8 类` overlay，而不是一次性铺满全部官方赛道 | 控制范围，同时优先覆盖官方高频扶持分类和仓库现有资产 |
| P0 8 类先统一做到中等深度 | 让 8 类都具备可执行性，同时保留后续再继续深挖的空间 |
| `review / precheck` 再补一层专项检查卡，而不是把检查逻辑塞回 overlay | 让写作规则和检查规则保持边界清晰 |
| 输出契约与轻量 state 约定一起补 | 让 bucket 级规则能被稳定消费，同时不把 state 做重 |
| `fanqie_p0_smoke.py` 第一版只强支持单 bucket、本地资料和保守写回 | 先把半自动 smoke 工具做稳，不越权替代主链 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| 工作树存在大量无关变更 | 仅在目标文件中局部追加，不回滚、不覆盖既有改动 |
| 大补丁在 `novel-write` 处因上下文漂移失败 | 改为按文件分批补丁，避免一次性大范围上下文匹配 |

## Resources
- `README.md`
- `docs/00-当前有效/start-here.md`
- `docs/00-当前有效/skill-usage.md`
- `docs/00-当前有效/default-workflows.md`
- `docs/90-归档/阶段/phase-9-summary.md`
- `docs/90-归档/阶段/phase-17-summary.md`
- `docs/fanqie-writing-techniques.md`
- `docs/00-当前有效/state-thinning-and-setting-sync.md`
- `docs/anti-flattening-framework/README.md`
- `docs/anti-flattening-framework/11-检查清单与评分规约.md`
- `docs/opening-and-plot-framework/README.md`
- `docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
- `docs/opening-and-plot-framework/02-开篇构件与组合公式.md`
- `docs/opening-and-plot-framework/03-开篇故障与修正.md`
- `docs/opening-and-plot-framework/04-剧情层次模型.md`
- `docs/opening-and-plot-framework/05-推进链与残账设计.md`
- `docs/opening-and-plot-framework/06-题材特化接口.md`
- `docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/README.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/宫斗宅斗.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/职场婚恋.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/青春甜宠.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/豪门总裁.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/都市日常.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/玄幻脑洞.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/都市脑洞.md`
- `docs/opening-and-plot-framework/fanqie-p0-overlays/历史脑洞.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/README.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/宫斗宅斗.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/职场婚恋.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/青春甜宠.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/豪门总裁.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/都市日常.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/玄幻脑洞.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/都市脑洞.md`
- `docs/opening-and-plot-framework/fanqie-p0-checkcards/历史脑洞.md`
- `docs/opening-and-plot-framework/fanqie-p0-output-contract.md`
- `docs/opening-and-plot-framework/real-project-smoke-shunvmoulue-fanqie-p0-2026-03-23.md`
- `docs/opening-and-plot-framework/fanqie-p0-smoke-template.md`
- `docs/opening-and-plot-framework/real-project-smoke-hunshu-taizi-fanqie-p0-2026-03-23.md`
- `docs/opening-and-plot-framework/fanqie-p0-pressure-results-2026-03-24.md`
- `docs/opening-and-plot-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-fanqie-p0-2026-03-24.md`
- `docs/opening-and-plot-framework/real-project-smoke-公司裁我那天-系统先赔了我一百万-fanqie-p0-2026-03-24.md`
- `scripts/fanqie_p0_smoke.py`
- `tests/test_fanqie_p0_smoke.py`
- `skills/novel-outline/SKILL.md`
- `skills/novel-write/SKILL.md`
- `skills/novel-review/SKILL.md`
- `skills/novel-precheck/SKILL.md`
- `skills/novel-package/SKILL.md`
- `tests/test_opening_plot_framework.py`
- `shared/templates/genres/宫斗宅斗.md`
- `shared/templates/genres/职场婚恋.md`
- `shared/templates/genres/都市日常.md`
- `shared/templates/genres/都市脑洞.md`
- `shared/templates/genres/历史脑洞.md`
- `shared/profiles/palace-intrigue/profile.yaml`
- `shared/profiles/workplace-romance/profile.yaml`
- `shared/profiles/sweet-romance/profile.yaml`
- `shared/profiles/sweet-youth/profile.yaml`
- `shared/profiles/ceo-romance/profile.yaml`
- `shared/profiles/urban-daily/profile.yaml`
- `shared/profiles/urban-brainhole/profile.yaml`
- `shared/profiles/historical-brainhole/profile.yaml`
- `shared/profiles/xuanhuan/profile-tomato.yaml`
- `projects/庶女谋略/.mighty/state.json`
- `projects/庶女谋略/大纲/总纲.md`
- `projects/庶女谋略/大纲/章纲/第001章.md`
- `projects/庶女谋略/大纲/章纲/第002章.md`
- `projects/庶女谋略/大纲/章纲/第003章.md`
- `projects/庶女谋略/chapters/第001章.md`
- `projects/庶女谋略/chapters/第002章.md`
- `projects/庶女谋略/chapters/第003章.md`
- `projects/庶妹换我婚书那夜，太子先开了口/.mighty/state.json`
- `projects/庶妹换我婚书那夜，太子先开了口/大纲/总纲.md`
- `projects/庶妹换我婚书那夜，太子先开了口/大纲/章纲/第001章.md`
- `projects/庶妹换我婚书那夜，太子先开了口/大纲/章纲/第002章.md`
- `projects/庶妹换我婚书那夜，太子先开了口/大纲/章纲/第003章.md`
- `projects/庶妹换我婚书那夜，太子先开了口/chapters/第001章.md`
- `projects/庶妹换我婚书那夜，太子先开了口/chapters/第002章.md`
- `projects/庶妹换我婚书那夜，太子先开了口/chapters/第003章.md`
- `shared/references/shared/state-schema.md`
- `shared/templates/state-v5-template.json`

---

# Findings & Decisions: 番茄起盘协议栈与 Compiler 层

## Requirements
- 为番茄优先路线新增一层比“成熟剧情架构库”更可执行的起盘规则层
- 第一版只覆盖开篇到黄金三章
- 结果需要能被 `outline / write / review / precheck / package` 直接消费

## Research Findings
- 番茄官方课程更强调：
  - 一句话故事
  - 故事支点
  - 切入事件
  - 首页见山
  - 章末留钩
  而不是先选抽象结构名
- 仅用“主架构卡”仍然太粗，因为真实起盘同时涉及：
  - 支点
  - 推进语法
  - 平台级留存协议
  - 题材义务
  - 场景句法
- 仓库现有最稳模式仍然是：
  - `docs/` 做单一事实源
  - `scripts/` 做保守自动化
  - `state.json` 保持轻
  - sidecar 承担详细运行结果
- `opening-and-plot-framework` 已有稳定入口和回归测试，适合作为承载层

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 命名为 `launch_stack` | 避免与整本书总结构混淆 |
| 文档树放在 `docs/opening-and-plot-framework/fanqie-launch-stack/` | 复用现有方法论文档承载层 |
| 运行结果写 `.mighty/launch-stack.json` | 保持 `state` 轻量且可恢复 |
| `state` 只镜像 4 个轻字段 | 避免新造平行状态中心 |
| 第一版固定 compiler 输出 5 组下游输入 | 避免每个 skill 自己解释协议栈 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| 隔离 worktree 基于干净 `HEAD`，不包含用户当前脏工作树里的 `writing-core` 测试集 | 将其明确记录为“待整合后再跑”的回归项，不在该 worktree 内伪造通过 |

## Resources
- `docs/superpowers/specs/2026-03-24-fanqie-launch-stack-design.md`
- `docs/superpowers/plans/2026-03-24-fanqie-launch-stack.md`
- `docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
- `scripts/fanqie_launch_stack.py`
- `tests/test_fanqie_launch_stack.py`

---

# Findings & Decisions: 信息架构状态化重构

## Requirements
- 用户明确要求不要继续只靠文档内容解释状态，而要让文件夹本身表达状态
- 用户指出这不是单个文档的问题，而是整个项目的通病
- 用户要求直接按最优方案执行，而不是继续停留在方案层

## Research Findings
- 当前仓库的核心问题不是“缺少索引”，而是“文件系统不表达状态”
- 根层 `docs/` 之前把以下几类文档混放：
  - 当前有效入口
  - 未决问题
  - 评审简报
  - phase / release / RC / migration 历史
- 这种混放导致：
  - 不打开文件就无法判断当前状态
  - “已完成 / 进行中 / 归档”无法靠目录感知
  - 日常使用成本高，且容易误把历史文档当成当前真源
- 仅增加 `架构问题跟踪.md` 这种入口文件不够，必须把状态分类写进目录结构

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 采用状态目录，而不是继续补更多索引页 | 用户的核心诉求是“看文件夹就知道状态” |
| 保留 `docs/INDEX.md` 在根层 | 根层仍需要一个总导航，但它应导航状态目录，而不是掩盖状态目录 |
| 保留根目录 `架构问题跟踪.md` | 解决日常高可见提醒问题，但不让它成为第二真相 |
| 第一轮只重排根层状态型文档，不动主题框架目录 | `anti-flattening` / `opening-and-plot` / `writing-core` 是主题真源，不是状态混乱主因 |
| 顺手修复同类脚本导入脆弱性 | 这属于这轮全仓结构调整暴露出来的真实同类问题，值得一起收口 |

## Result
- 已形成可见状态目录：
  - `docs/00-当前有效/`
  - `docs/10-进行中/`
  - `docs/20-研究实验/`
  - `docs/90-归档/`
- 根层 `docs/INDEX.md` 已变成状态目录导航页
- 根目录 `架构问题跟踪.md` 继续保留为高可见提醒入口
- 这轮之后，用户无需先点开文件，光看目录即可区分：
  - 当前仍有效
  - 还在跟踪
  - 研究/实验
  - 历史归档

## Verification
- `pytest -q` 通过：`248 passed, 192 subtests passed`
- `bash scripts/validate-migration.sh` 通过
- `python -m unittest tests.test_post_write_lint -v` 通过

---

# Findings & Decisions: AOI-001 `state/schema/template/script` 收口

## Requirements
- 不再让 `state-schema.md` 只做口头权威
- 不再让 `state-v5-template.json` 的 `$schema` 指向不存在文件
- 不再让 `build_active_context.py` 靠自造简化 shape 消费 `items` / `factions`
- 让这层问题从“台账问题”变成“真正关闭的问题”

## Research Findings
- 对当前仓库，最合适的收口方式不是继续扩写 Markdown，而是补真实 machine schema
- `learned_patterns` / `market_adjustments` 的核心问题不是应不应该旁路，而是：
  - 旁路后的 pointer summary 形态没有被正式纳入 contract
- `items.tracked` / `factions.active` 当前最现实的 canonical 处理不是强推单形态，而是：
  - schema 支持字符串 / 对象双形态
  - consumer 统一做 name-normalization
- `python -m unittest` 路径下的导入稳定性不该只修一个脚本，同类 sibling-import 脚本应一起收口

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 新增真实 JSON Schema 文件，而不是继续只依赖 Markdown | 让测试和脚本可以验证机器真值 |
| 保留 `state-schema.md` 作为语义说明层 | docs-first 仍有价值，不需要打掉 |
| `learned_patterns` / `market_adjustments` 在 schema 中允许 inline + externalized 双形态 | 兼容现有数据与旁路路径 |
| `items` / `factions` 在 schema 与 consumer 中都接受字符串/对象双形态 | 解决当前 consumer/fixture/template 差异而不破坏旧项目 |
| 同类 sibling-import 脚本一起修导入路径 | 避免“今天修一个，明天炸另一个” |

## Result
- `AOI-001` 已可从 open issues 中关闭
- 机器真值层已落地，consumer、模板与验证门被同一层约束
- 后续再新增 `state` 字段或旁路字段时，不再只能靠人工同步记忆

## Verification
- `pytest -q tests/test_state_contracts.py tests/test_active_context.py tests/test_inkos_growth_plan.py tests/test_setting_gate.py` 通过：`40 passed`
- `python -m unittest tests.test_post_write_lint -v` 通过：`7 tests OK`
- `pytest -q` 通过：`254 passed, 192 subtests passed`
- `bash scripts/validate-migration.sh` 通过

---

# Findings & Decisions: AOI-002 / AOI-003 / AOI-004 / AOI-006 治理收口推进

## Requirements
- 不再让 `shared` 真同步仍然是“整包覆盖 + 口头提醒”
- 不再让 `maintenance` 只在 stdout 里声称自己属于 chapter transaction
- 不再让 `active-context` 复制 `recent_guardrails` 正文
- 不再让治理问题只停在 open issue 文案里，没有测试和入口文档配套

## Research Findings
- 真实仓库里 `shared/references` 同时存在：
  - repo-local local-only files
  - same-path drift files
  因此仅靠“先 `--report` 再人工小心”不够，必须让脚本默认阻断危险覆盖。
- `project-maintenance.py` / `post-task-maintenance.py` 之前只输出：
  - `transaction_phase = maintenance`
  - `next_transaction_step = snapshot`
  但没有真实更新 `.mighty/workflow_state.json`，导致 `novel-resume` 只能读到理想契约，看不到真实 checkpoint。
- `active-context` 复制 `recent_guardrails` 会制造 sidecar freshness drift：
  - 细节真值已在 `.mighty/learned-patterns.json`
  - `active-context` 更适合只保留 prompt-assembly 需要的 guardrail summary

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 引入 `shared/sync-governance.json` | 给 repo-local shared 文件一个机器可读的保护清单，而不是继续靠文档提醒 |
| `sync-shared-from-genm.sh` 默认阻断 drift overwrite | 让危险覆盖从“容易发生”变成“需要显式确认才会发生” |
| sync 后恢复 protected local paths | 保留 full-copy 主路径，同时保护 repo-local contract/template |
| 将 maintenance -> snapshot 写回 `workflow_state.json` | 先把最稳定、最可验证的事务尾段变成真实 checkpoint |
| `active-context` 只保留 `guardrail_summary` | 保持 projection / pointer 角色，不制造第二提示真值中心 |
| 用 targeted tests 锁治理语义 | 这些问题不该只靠 README 和记忆维持 |

## Result
- `AOI-002` 已具备脚本级收口条件：
  - governance manifest
  - drift block
  - allowlist restore
  - report-json 差异输出
- `AOI-003` 已完成 maintenance 段机械闭环，剩余问题缩窄到：
  - `draft`
  - `close`
  - `snapshot`
  的 phase owner 写回
- `AOI-004` 当前复制风险已收口，`active-context` 回到摘要/指针角色
- `AOI-006` 当前最关键的治理护栏已补齐：
  - shared drift / allowlist
  - maintenance 最终态
  - 入口文档同步

## Verification
- `python3 -m unittest tests.test_shared_sync_governance -v` 通过
- `pytest -q tests/test_inkos_growth_plan.py tests/test_setting_gate.py` 通过：`25 passed`
- `pytest -q tests/test_active_context.py tests/test_inkos_growth_plan.py` 通过：`25 passed`
- `bash scripts/sync-shared-from-genm.sh --report-json --domain references` 通过
- `bash scripts/validate-migration.sh` 通过

---

# Findings & Decisions: `v1.3` 候选池预研

## Requirements
- 不把 `v1.3` 继续做成“大而全补线”
- 优先列入对默认工作流、质量链和 profile/positioning 可用面最有价值的项
- 不把已明确 `deferred` 或已明确排除的实验/架构方向偷渡进主线

## Research Findings
- `v1.2` 已把 `content-positioning` 做到“主 profile 稳定 + bucket-only fallback 可用”，但 coverage 仍处于首批状态：
  - `content-positioning-map-v1.json` 仅覆盖 11 个 profile
  - `bucket_defaults` 仅覆盖 6 个 bucket
  - `shared/profiles/` 中仍有 38 个 profile 缺 `platform_positioning`
  - 仍有 25 个 profile 保留 `opening_templates`
  - 仍有 25 个 profile 保留 `dialogue_templates`
  - 仍有 11 个 profile 保留 `scene_description`
- `review / precheck / package` 的质量路由一致性，和“真实小说项目上的默认工作流稳定性”，已经被 `docs/00-当前有效/v1-maintenance-mode.md` 明确列为当前 `v1.x` 的首要维护重点。
- `Fanqie-first` 路线目前仍缺：
  - 已冻结内部生产模板
  - 首个可投样本
  - 宫斗宅斗重验结果
- `workflow_state` 当前仍只有 maintenance/snapshot 尾段 owner 真正落盘，`draft / close / gate-check` 的 phase owner 语义还主要分散在 skill prose 和脚本约定里。
- 本地复核还发现一个具体缺口：`scripts/workflow_state_utils.py` 的 `mark_snapshot_complete()` 目前仍会把 `TRANSACTION_STEPS` 全量并入 `completed_steps`，这会把“未真实记录过的前序 phase”一并表现成完成态；这更适合收进 `v1.3` 的“事务契约 + 运行证据链统一”主题里处理，而不是零碎热修。
- 高频 consumer skill 的规则装载协议已经明显复制：
  - `novel-outline`
  - `novel-write`
  - `novel-review`
  - `novel-package`
  都在手写大段读档清单；问题已经不是“文案长”，而是“规则装载协议分散”。
- `setting_gate.py` 当前同时承担：
  - truth-gap 检测
  - local card materialization
  - launch-stack auto compile
  - gate state 写回
  - sync-review 写回
  - trace 写回
  职责已经跨 analyzer / mutator / orchestrator 三层。

## Recommended `v1.3` Themes
1. **质量路由一致性**
   - 聚焦 `review / precheck / package` 对同一项目给出更一致的判断口径。
2. **默认工作流稳定性与恢复体验**
   - 聚焦 `gate triage`、维护链、恢复建议、事务证据链。
3. **高频技能规则栈 manifest 化**
   - 把 `outline/write/review/package` 的规则装载清单收成共享 manifest/bundle。
4. **事务契约 + sidecar freshness registry**
   - 统一 `workflow/resume/log/maintenance` 的状态语义与 sidecar 过期/重建判断。
5. **content-positioning 第二轮扩面**
   - 继续补高价值 profile / bucket，并扩到 `hook/payoff/motive` 级字段。
6. **Fanqie-first 样本冻结**
   - 推出首条冻结内部模板和首个可投样本。

## Do Not Promote Into `v1.3`
- 不把 `novel-scan` 偷渡进默认主线；继续保持实验能力边界。
- 不重开 monolithic runtime / plugin framework 方向。
- 不把 `skills manifest / sidecar registry / pipeline manifest` 作为脱离用户价值的纯治理项目来做；只有服务上述主线时才进入范围。
- 不重新讨论 `novel-log` 是否回到默认主线；`v1.2` 已给出“专家辅助能力”结论。

## Recommended Order
1. `质量路由一致性`
2. `默认工作流稳定性与恢复体验`
3. `高频技能规则栈 manifest 化`
4. `事务契约 + sidecar freshness registry`
5. `content-positioning` 第二轮扩面
6. `Fanqie-first` 样本冻结
