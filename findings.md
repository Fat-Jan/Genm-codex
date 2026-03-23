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
- `docs/phase-9-summary.md` 说明项目主方向仍是“包装生成层 + 质量闭环整合”，因此新框架应作为默认工作流规则层接入，而不是独立实验能力
- `skills/novel-write/SKILL.md`、`skills/novel-outline/SKILL.md`、`skills/novel-review/SKILL.md` 已支持按需读取多组项目内文档，说明新增框架不需要新建命令
- `skills/novel-review/SKILL.md` 已有 `chapter_meta[chapter].dimension_scores` 写回位点，适合承载轻量增强评分键
- `shared/references/shared/state-schema.md` 已明确：
  - 不要为局部规则新造顶层 state 中心
  - 可通过 `chapter_meta` 和可选评分键做轻量持久化
- `docs/fanqie-writing-techniques.md` 已有对“开头与黄金三章”“剧情稳定与悬念交替”的项目级提炼，可作为这次通用框架的重要参考，而不必从零起草
- 仓库当前是脏工作树，且 `README.md`、`docs/default-workflows.md`、`docs/skill-usage.md`、若干 skill 已有未提交改动；本次必须局部增量修改，不能回滚既有内容
- 已新增 `docs/opening-and-plot-framework/`：
  - `README.md`
  - `01-开篇目标与成功标准.md`
  - `02-开篇构件与组合公式.md`
  - `03-开篇故障与修正.md`
  - `04-剧情层次模型.md`
  - `05-推进链与残账设计.md`
  - `06-题材特化接口.md`
- `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` 已完成显式路径接线
- `README.md`、`docs/start-here.md`、`docs/skill-usage.md`、`docs/default-workflows.md` 已补新框架入口
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
- `docs/start-here.md`
- `docs/skill-usage.md`
- `docs/default-workflows.md`
- `docs/phase-9-summary.md`
- `docs/phase-17-summary.md`
- `docs/fanqie-writing-techniques.md`
- `docs/state-thinning-and-setting-sync.md`
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
