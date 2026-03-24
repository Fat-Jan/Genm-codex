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

---

# Task Plan: 开篇方法与剧情层次规则层

## Goal
在仓库内落成一组跨题材通用的“开篇方法 + 剧情层次”规则层文档，并将其接入 `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package`，同时补齐入口文档、轻量 state 评分键说明与可执行验证。

## Current Phase
Phase 26

## Phases

### Phase 1: Discovery & Design Lock
- [x] 读取当前计划文件、默认工作流与关键 skill
- [x] 确认承载层为 `docs/`
- [x] 确认范围为“README + 6 个主模块 + 5 个 skill 接线”
- **Status:** complete

### Phase 2: Red Test
- [x] 新增框架存在性与接线测试
- [x] 运行测试并确认先失败
- **Status:** complete

### Phase 3: Framework Docs
- [x] 创建 `docs/opening-and-plot-framework/`
- [x] 写 README 与 6 个主模块
- **Status:** complete

### Phase 4: Skill Wiring
- [x] 更新 `novel-outline`
- [x] 更新 `novel-write`
- [x] 更新 `novel-review`
- [x] 更新 `novel-precheck`
- [x] 更新 `novel-package`
- **Status:** complete

### Phase 5: Entry Docs & State Contract
- [x] 更新 `README.md` / `docs/start-here.md` / `docs/skill-usage.md` / `docs/default-workflows.md`
- [x] 在 `state-schema` / `state-v5-template` 中补充轻量评分键说明
- **Status:** complete

### Phase 6: Verification & Delivery
- [x] 运行新增测试
- [x] 运行 `bash scripts/validate-migration.sh`
- [x] 回写 `findings.md` / `progress.md`
- **Status:** complete

## Key Questions
1. 这套规则应该只做开篇技巧说明，还是要同时覆盖剧情层次与推进链？
2. 是否需要新增 state 顶层结构来保存开篇/层次判断？
3. 第一版题材特化应直接展开，还是只定义接口？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 承载层放在 `docs/opening-and-plot-framework/` | 复用当前项目“方法论文档 + skill 接线”的稳定模式 |
| 第一版做跨题材通用骨架 | 先搭规则底盘，后续再按项目提醒补题材特化 |
| 题材特化只先做接口文档 | 避免第一版无限扩张为资料库 |
| 只做轻量 state 评分键增强，不新造平行顶层结构 | 保持运行态轻量，避免把课程框架做成 memory 总库 |
| 用 `tests/test_opening_plot_framework.py` 做最小红绿验证 | 让文档/skill 合同改动也有可重复验证闭环 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| 大补丁在 `skills/novel-write/SKILL.md` 上下文对齐失败 | 1 | 改为分批小补丁逐文件接线 |

## Notes
- 入口模式对齐 `docs/anti-flattening-framework/`，但不复制其 12 模块体量
- 用户已确认范围为全接线：`outline/write/review/precheck/package`
- 默认优先改文档与 skill 合同，不碰 `shared/` 同步资产内容本体

### Phase 7: Fanqie Priority Overlays
- [x] 基于官方近年活动确定番茄优先分类
- [x] 新增 `fanqie-priority-categories-2026-03.md`
- [x] 为 P0 8 类新增 overlay 骨架
- [x] 为 5 个主 skill 增加按 bucket 读取番茄 P0 overlay 的合同路径
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 8: Fanqie P0 Medium-Depth Cards
- [x] 读取 8 张 overlay 与对应本地 profile / template 资产
- [x] 扩展测试，要求 8 张卡具备统一的中等深度结构
- [x] 将 8 张卡补全为“开篇公式 / 黄金三章最低要求 / 高频故障清单 / precheck 专项检查点”
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 9: Fanqie P0 Checkcards
- [x] 读取现有专项卡模式与 `review / precheck` 接线位点
- [x] 扩展测试，要求新增专项检查卡目录、文件与接线路径
- [x] 为 8 类新增 bucket 级 `review / precheck` 专项检查卡
- [x] 更新 `novel-review` / `novel-precheck` 的条件读取规则
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 10: Fanqie P0 Output Contract
- [x] 确定 `review / precheck` 的最小稳定摘要字段
- [x] 扩展测试，要求输出契约文档、技能字段与轻量 state 约定存在
- [x] 新增 Fanqie P0 输出契约文档
- [x] 更新 `novel-review` / `novel-precheck` 输出契约
- [x] 在 `chapter_meta` 约定中补充轻量 bucket 字段
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 11: Real Project Smoke
- [x] 读取 `projects/庶女谋略` 的 state、总纲、前 1-3 章
- [x] 基于真实项目手工生成一版 `fanqie_bucket_review_summary`
- [x] 基于真实项目手工生成一版 `fanqie_bucket_precheck_summary`

---

# Task Plan: 番茄起盘协议栈与 Compiler 层

## Goal
在仓库内落成一组“番茄起盘协议栈”规则文档、一个保守的 `launch_stack` compiler CLI、轻量 sidecar/state 约定，并将其最小接入 `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package`。

## Current Phase
Phase 2

## Phases

### Phase 1: Discovery & Spec Lock
- [x] 读取现有 `opening-and-plot-framework` / `writing-core-framework` / 相关测试与技能合同
- [x] 调研番茄官方与通用叙事框架资料，确认“协议栈优于单主架构卡”
- [x] 写出正式 spec：`docs/superpowers/specs/2026-03-24-fanqie-launch-stack-design.md`
- **Status:** complete

### Phase 2: Implementation Planning
- [x] 读取 `writing-plans` 技能与现有计划样式
- [x] 固化 v1 范围为：`Premise / Pivot / Launch Grammar / Retention Protocol / compiler / 轻量写回`
- [x] 写出实施计划：`docs/superpowers/plans/2026-03-24-fanqie-launch-stack.md`
- **Status:** complete

### Phase 3: Contract Red Tests
- [ ] 新增 `tests/test_fanqie_launch_stack.py`
- [ ] 锁 launch-stack 文档树、skill 接线、state 约定、CLI 存在性
- [ ] 运行测试确认先失败
- **Status:** pending

### Phase 4: Launch-Stack Docs
- [ ] 创建 `docs/opening-and-plot-framework/fanqie-launch-stack/`
- [ ] 写 4 层主模块与 compiler contract
- [ ] 写 6 张起盘语法卡
- **Status:** pending

### Phase 5: Compiler CLI
- [ ] 新建 `scripts/fanqie_launch_stack.py`
- [ ] 实现保守 `draft` 推断
- [ ] 实现显式 `writeback`
- **Status:** pending

### Phase 6: Skill Wiring
- [ ] 更新 `novel-outline`
- [ ] 更新 `novel-write`
- [ ] 更新 `novel-review`
- [ ] 更新 `novel-precheck`
- [ ] 更新 `novel-package`
- **Status:** pending

### Phase 7: State & Sidecar Contract
- [ ] 更新 `state-schema` / `state-v5-template`
- [ ] 记录 `.mighty/launch-stack.json` 与 ledger sidecar 约定
- [ ] 对齐 `novel-init` / thin-state 文档
- **Status:** pending

### Phase 8: Smoke & Verification
- [ ] 生成 2 个真实项目 smoke artifact
- [ ] 运行 launch-stack 测试
- [ ] 回归 opening/writing-core 测试与迁移校验
- **Status:** pending

## Key Questions
1. v1 是否应该把“平台留存协议”独立于起盘语法卡，而不是继续塞进 bucket overlay？
2. `launch_stack` 应该只做 sidecar，还是同时写回最小 state 镜像字段？
3. 真实项目 smoke 应优先覆盖哪两种早期起盘类型，才能最快暴露误判？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 用“番茄起盘协议栈”替代“单主架构卡” | 一部书的前期判断常常是支点、语法、平台协议、题材义务的组合，单一卡片太粗 |
| 第一版只做开篇到黄金三章 | 番茄最敏感的留人区间在这里，收益最高且范围可控 |
| 通用框架只做映射参考，不做运行时真源 | Save the Cat / 三幕式 / Story Circle 适合解释和校准，不适合直接当番茄执行规则 |
| 详细结果写 `.mighty/launch-stack.json`，state 只镜像 4 个轻字段 | 延续项目“文档真源 + sidecar 运行结果 + 轻 state”模式 |
| `Hook Ledger / Payoff Ledger` 只在 v1 建立占位合同 | 先跑通协议栈与 compiler，不把第一版拖进重型自动化 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| 尚无 | 0 | 当前处于设计与计划阶段，未进入实现 |

## Notes
- 复用 `docs/opening-and-plot-framework/` 作为承载层，不新造平行顶层框架目录
- 复用现有 `tests/test_opening_plot_framework.py` 与 `tests/test_writing_core_framework.py` 的合同测试模式
- 默认优先落“文档真源 + compiler + 轻量写回”，不直接做黑盒 orchestrator

---

# Task Plan: 写作基本功与内容标准规则层

## Goal
在仓库内落成一组“写作基本功 / 内容标准 / memory 压缩信号 / 开篇包装输入”方法论文档，复用现有 `opening-and-plot-framework` 作为剧情层次真源，并接入 `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` / `novel-learn`。

## Current Phase
Phase 5

## Phases

### Phase 1: Boundary Lock
- [x] 确认 `剧情层次` 不重写，继续复用 `docs/opening-and-plot-framework/`
- [x] 确认新框架仅补 `基本功 / 内容标准 / memory / 包装输入`
- [x] 确认承载层为 `docs/writing-core-framework/`
- **Status:** complete

### Phase 2: Red Test
- [x] 新增 `tests/test_writing_core_framework.py`
- [x] 运行测试并确认先失败
- **Status:** complete

### Phase 3: Docs + Wiring
- [x] 创建 `docs/writing-core-framework/` 8 个文档
- [x] 更新 6 个 consumer skill 的读取合同
- [x] 更新入口文档、state schema、state template 与瘦身说明
- **Status:** complete

### Phase 4: Verification
- [x] 运行 `python -m unittest tests.test_writing_core_framework -v`
- [x] 回归 `python -m unittest tests.test_opening_plot_framework -v`
- [x] 运行 `bash scripts/validate-migration.sh`
- [x] 在真实项目上补一份 `package + precheck + memory writeback` 手工 smoke
- **Status:** complete

### Phase 5: Smoke Automation
- [x] 新增 `scripts/writing_core_smoke.py`
- [x] 新增 `tests/test_writing_core_smoke.py`
- [x] 将脚本入口挂回 `docs/writing-core-framework/README.md`
- [x] 跑完新旧测试与迁移校验
- **Status:** complete

### Phase 6: Scripted Third Sample
- [x] 使用 `scripts/writing_core_smoke.py` 跑通 `都市日常` 真实样本
- [x] 生成第三条样本的 `包装/包装方案.md`
- [x] 将第三条样本纳入 `writing-core-framework` 回归护栏
- **Status:** complete

### Phase 7: Fourth Sample + Richer Templates
- [x] 为 `历史脑洞` 和 `职场婚恋` 增加显式 bucket 包装模板
- [x] 使用 `scripts/writing_core_smoke.py` 跑通 `历史脑洞` 第四条真实样本
- [x] 将第四条样本纳入 `writing-core-framework` 回归护栏
- **Status:** complete

### Phase 8: Fifth Sample + Wider Bucket Templates
- [x] 为 `青春甜宠` 和 `都市脑洞` 增加显式 bucket 包装模板
- [x] 使用 `scripts/writing_core_smoke.py` 跑通 `职场婚恋` 第五条真实样本
- [x] 将第五条样本纳入 `writing-core-framework` 回归护栏
- **Status:** complete

### Phase 9: Sixth Sample + Batch Entry
- [x] 使用 `scripts/writing_core_smoke.py` 跑通 `青春甜宠` 第六条真实样本
- [x] 新增 `scripts/batch_writing_core_smoke.py`
- [x] 将第六条样本与 batch 入口纳入回归护栏
- **Status:** complete

### Phase 10: Seventh Sample + Batch Summary
- [x] 使用 `scripts/writing_core_smoke.py` 跑通 `都市脑洞` 第七条真实样本
- [x] 为 batch 入口补 `writeback + save-packaging + summary_report`
- [x] 将第七条样本与 batch summary 能力纳入回归护栏
- **Status:** complete

### Phase 11: Palace Sidecar + Repo Batch Baseline
- [x] 使用 `scripts/writing_core_smoke.py` 跑通 `宫斗宅斗` 脚本化样本
- [x] 在已有包装文件存在时落 `包装方案-writing-core.md` sidecar，不覆盖人工收口版
- [x] 将 batch 能力落成仓库内固定 manifest + fixed output dir + summary report 基线
- **Status:** complete

### Phase 12: Batch Aggregation + Full Baseline
- [x] 为 batch summary 增加聚合统计与失败收集
- [x] 将固定 batch baseline 从 3 项扩到 8 个代表性 bucket
- [x] 跑通固定 batch output 与全量回归
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 新框架命名为 `docs/writing-core-framework/` | 避免和现有 `opening-and-plot-framework` 重叠，同时覆盖 craft + standard + memory + package 输入 |
| `剧情层次` 继续复用原框架 | 避免重写同一套结构理论，保持单一事实源 |
| memory 只收压缩信号，不造新顶层区块 | 保持 `.mighty/state.json` 轻量，符合既有 state 设计 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| 大补丁在 `skills/novel-precheck/SKILL.md` 上下文对齐失败 | 1 | 改为分批小补丁，先改 state / 入口文档，再逐个 skill 接线 |
- [x] 产出只读 smoke 文档，不污染活项目 state
- **Status:** complete

### Phase 12: Real Project Writeback
- [x] 扩展测试，要求真实项目 state 出现 `chapter_meta["003"].fanqie_bucket_*`
- [x] 将 `第003章` 的 bucket 样本真实写回 `projects/庶女谋略/.mighty/state.json`
- [x] 将 smoke 文档从只读验证更新为写回验证
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 13: Reusable Smoke Template
- [x] 扩展测试，要求新增 `fanqie-p0-smoke-template.md` 且在框架入口中可发现
- [x] 编写可复用的 Fanqie P0 smoke 模板文档
- [x] 更新框架入口
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 14: Cross-Project Smoke
- [x] 读取第二个真实项目的 state、总纲、前 1-3 章
- [x] 按可复用 smoke 模板生成第二份跨项目样本
- [x] 产出第二份真实项目 smoke 文档
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 15: Smoke Tool Planning
- [x] 写 `fanqie_p0_smoke.py` 的设计文档
- [x] 写实现计划文档
- **Status:** complete

### Phase 16: Smoke Tool V1
- [x] 新增 `tests/test_fanqie_p0_smoke.py`
- [x] 实现 `scripts/fanqie_p0_smoke.py` 的 CLI、helper、scaffold、draft、writeback v1
- [x] 更新框架入口与 smoke 模板中的脚本调用说明
- [x] 运行脚本测试、框架回归测试与迁移校验
- [x] 试跑两个真实项目的 `draft` 模式
- **Status:** complete

### Phase 17: Smoke Tool V1.1
- [x] 为 `draft` 输出增加 `confidence / evidence_count / evidence_sources`
- [x] 读取本地 `market_adjustments / learned_patterns`
- [x] 增加 `writeback_preview`
- [x] 对更多 P0 bucket 提供保守的 low-confidence draft
- [x] 运行脚本测试、框架回归测试与迁移校验
- **Status:** complete

### Phase 18: Pressure Matrix
- [x] 选择支持桶与非支持桶样本
- [x] 批量运行 `fanqie_p0_smoke.py`
- [x] 汇总 `draft / scaffold-only` 结果
- [x] 输出压力测试文档
- **Status:** complete

### Phase 19: Real P0 Project Validation
- [x] 读取两个真实非宫斗 P0 项目的 state、总纲、前 1-3 章
- [x] 生成两份真实项目 smoke 文档
- [x] 确认 `青春甜宠 / 都市脑洞` 两条线都能产出结构化 `draft`
- [x] 将结论写入 findings / progress
- **Status:** complete

### Phase 20: Second Real Writeback Sample
- [x] 为 `青春甜宠` 真实项目补第二条写回样本测试
- [x] 将 `第003章` 的 bucket 样本轻量写回项目 state
- [x] 更新对应 smoke 文档
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 21: Third Real Writeback Sample
- [x] 为 `都市脑洞` 真实项目补第三条写回样本测试
- [x] 将 `第003章` 的 bucket 样本轻量写回项目 state
- [x] 更新对应 smoke 文档
- [x] 运行测试与迁移校验
- **Status:** complete

### Phase 22: Record Sync & Final Verification
- [x] 将 `青春甜宠 / 都市脑洞` 的最终判断同步到 `findings.md` / `progress.md`
- [x] 更新压力测试文档，纳入两个真实非宫斗 P0 项目与当前最终结论
- [x] 重新运行脚本测试、框架回归测试与迁移校验
- **Status:** complete

### Phase 23: Additional Non-Palace P0 Validation
- [x] 为 `职场婚恋 / 都市日常 / 玄幻脑洞` 三个真实项目新增 smoke 约束测试
- [x] 收紧 `fanqie_p0_smoke.py` 的三类 bucket 强信号判定
- [x] 修复 `writeback` 输出会把 smoke 文档回退成空模板的问题
- [x] 修复空占位字段导致的假冲突，并补幂等 `already-written` 路径
- [x] 将三条真实项目的 `chapter_meta["003"]` 轻量写回并复跑验证
- **Status:** complete

### Phase 24: Gap Tracker & Next-Hop Handoff
- [x] 新增 `fanqie-p0-gap-tracker-2026-03.md`
- [x] 在框架 README 中暴露剩余桶缺口与下一跳入口
- [x] 用测试锁住 gap tracker 与样本入口发现性
- **Status:** complete

### Phase 25: P0 Full Coverage Validation
- [x] 为 `历史脑洞 / 豪门总裁` 两个真实项目新增 smoke 约束测试
- [x] 收紧 `fanqie_p0_smoke.py` 的两类 bucket 强信号判定
- [x] 兼容 `chapter_meta` 的 `3 / 003` 双键风格，并升级 legacy bucket 占位写回
- [x] 将两条真实项目的 `chapter_meta["003"/"3"]` 轻量写回并复跑验证
- [x] 将压力结果与 gap tracker 更新为 `P0 8 桶全覆盖`
- **Status:** complete

### Phase 26: Second-Sample Expansion
- [x] 新建第二条 `豪门总裁 / 都市脑洞 / 玄幻脑洞` 真实项目样本
- [x] 为三条样本补最小运行态文件、总纲、章纲和前三章正文
- [x] 运行 `draft -> writeback` 并确认 smoke 文档落地
- [x] 将 gap tracker 与 pressure results 更新为新的优先级
- **Status:** complete

## Additional Decisions
| Decision | Rationale |
|----------|-----------|
| 第一批番茄特化采用 `P0 8 类 + P1 补充梯队` | 先覆盖近年官方反复扶持且仓库已有资产的主分类 |
| P0 先选 `宫斗宅斗 / 职场婚恋 / 青春甜宠 / 豪门总裁 / 都市日常 / 玄幻脑洞 / 都市脑洞 / 历史脑洞` | 2025-2026 官方活动反复出现，且适合当前默认工作流直接消费 |
| skill 只增加 `fanqie-priority-categories-2026-03.md` 与 `fanqie-p0-overlays/<bucket>.md` 的条件读取路径 | 让特化仍然维持 overlay 模式，而不是重写通用框架 |
| 8 张 P0 卡统一升级为中等深度版，而不是只深做 2-3 张 | 保持覆盖面，同时避免一步写成过深、过散的专项手册 |
| bucket 级专项检查使用单独 `fanqie-p0-checkcards/` 目录 | 将“怎么写”与“怎么审 / 怎么拦”分层，避免 overlay 卡承担过多职责 |
| `review / precheck` 用单独输出契约承接 Fanqie P0 卡 | 让 bucket 规则真正进入稳定输出，而不只停在“按需读取” |
| `fanqie_p0_smoke.py` v1.1 对更多 P0 bucket 只给低置信草稿 | 扩覆盖面，但不把 smoke 工具伪装成全自动判断器 |

---

# Task Plan: 番茄起盘协议栈与 Compiler 层

## Goal
在仓库内落成“番茄起盘协议栈”文档树、保守 `launch_stack` compiler CLI、轻量 sidecar/state 合同，并将其最小接入 `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package`。

## Current Phase
Phase 8

## Phases

### Phase 1: Discovery & Spec Lock
- [x] 调研番茄官方与通用结构资料
- [x] 将“主架构卡”收束成“起盘协议栈 + compiler + 两本账”
- [x] 固化正式 spec
- **Status:** complete

### Phase 2: Contract Red Tests
- [x] 新增 `tests/test_fanqie_launch_stack.py`
- [x] 锁文档树、CLI、skill/state 合同
- [x] 运行红测确认缺口
- **Status:** complete

### Phase 3: Launch-Stack Docs
- [x] 创建 `docs/opening-and-plot-framework/fanqie-launch-stack/`
- [x] 写 4 层主模块与 compiler contract
- [x] 写 6 张起盘语法卡
- **Status:** complete

### Phase 4: Compiler CLI
- [x] 新建 `scripts/fanqie_launch_stack.py`
- [x] 实现保守 `draft` 推断
- [x] 实现显式 `writeback`
- **Status:** complete

### Phase 5: Skill Wiring
- [x] 更新 `novel-outline`
- [x] 更新 `novel-write`
- [x] 更新 `novel-review`
- [x] 更新 `novel-precheck`
- [x] 更新 `novel-package`
- **Status:** complete

### Phase 6: State & Sidecar Contract
- [x] 更新 `state-schema` / `state-v5-template`
- [x] 补 `novel-init` / thin-state sidecar 说明
- [x] 保持 state 只镜像 4 个轻字段
- **Status:** complete

### Phase 7: Entry Docs
- [x] 更新 `README.md`
- [x] 更新 `docs/start-here.md`
- [x] 更新 `docs/skill-usage.md`
- [x] 更新 `docs/default-workflows.md`
- [x] 更新 `docs/opening-and-plot-framework/README.md`
- **Status:** complete

### Phase 8: Smoke & Verification
- [x] 生成 2 个真实项目 launch-stack smoke artifact
- [x] 运行 `tests.test_fanqie_launch_stack`
- [x] 回归 `tests.test_opening_plot_framework`
- [x] 运行 `bash scripts/validate-migration.sh`
- **Status:** complete

## Key Questions
1. 平台级留存协议应该继续藏在 bucket overlay 里，还是独立成层？
2. `launch_stack` 结果应该写多重，才不会把 `state` 再次做胖？
3. 第一版最小 smoke 应覆盖哪两种起盘类型，才能最快暴露误判？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 用“番茄起盘协议栈”替代“单主架构卡” | 更符合番茄起盘的真实组合结构 |
| 通用框架只做映射参考 | 避免把 Save the Cat / Story Circle 误当运行时真源 |
| 详细结果写 `.mighty/launch-stack.json` | 保持 `state` 轻量，延续 sidecar 模式 |
| 第一版只做开篇到黄金三章 | 收益最高且范围可控 |
| 真实 smoke 先覆盖关系驱动与资源驱动 | 能最快暴露两类常见误判 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| worktree 内 `tests/test_writing_core_framework.py` 缺失 | 1 | 明确记录该 worktree 基于干净 `HEAD`，本轮最终验证不包含这组仅存在于用户当前脏工作树的测试 |

## Notes
- launch-stack 最初在隔离 worktree 内实现，并已完成 rebase onto `main`
- 最终验证证据是：
  - `python3 -m unittest tests.test_fanqie_launch_stack -v`
  - `python3 -m unittest tests.test_opening_plot_framework -v`
  - `bash scripts/validate-migration.sh`
