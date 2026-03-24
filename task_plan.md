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
Phase 18

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
