# 番茄起盘协议栈设计

Date: 2026-03-24

## 目标

为 `Genm-codex` 增加一层面向番茄优先工作流的“起盘协议栈”，用于稳定驱动：

- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-precheck`
- `novel-package`

这层设计只服务“开篇到黄金三章”的起盘闭环，不试图一版覆盖整卷或整本书的全周期结构。

它的职责不是做一套理论资料库，而是把“番茄平台真正影响留人、追读、早期兑现”的结构信号收成系统可消费的软规则输入。

## 问题

当前仓库已经有：

- `opening-and-plot-framework`
- `anti-flattening-framework`
- `writing-core-framework`
- Fanqie P0 bucket overlays / checkcards / output contracts

这些层已经能处理：

- 开篇目标
- 剧情层次
- 推进账本
- 内容标准
- 人物立体度
- bucket 级平台化约束

但还缺一层更靠前的“番茄起盘选择器”，去解决以下问题：

1. 系统知道“开篇应该有钩子”，但还不知道这本书到底主要靠什么起盘。
2. 系统知道“三幕式 / Save the Cat / Story Circle”这些框架存在，但它们离番茄场景太远，不适合作为运行时真源。
3. 仅用 bucket 很难稳定决定前 1-3 章该交付什么，因为同 bucket 内部的起盘方式差异很大。
4. 当前流程可以做 `review -> route -> precheck`，但还缺一个更早的、能统一解释“第一页、章末、第二悬念、第一次硬兑现”的平台级协议层。

## 为什么“主架构卡”还不够

前一版思路是：先做 6 张“番茄主架构卡”，再让系统从中选主架构。

这比单纯收集通用叙事理论要好，但仍然有 3 个问题：

1. “主架构”这个名字会误导系统把它当成整本书的总结构，而第一版实际只想管开篇与黄金三章。
2. 平台级留存规则，例如：
   - 首页见山
   - 章末留钩
   - 第二悬念接力
   - 前三章第一次硬兑现
   - 主角不靠低级失误制造压制
   不应该埋在某张卡里，它们更像跨题材的协议层。
3. 一部书的前期判断往往不是“单一卡片”能完整表达的，它常常同时包含：
   - 一个起盘支点
   - 一种推进语法
   - 一组平台级留存规则
   - 一组题材义务
   - 一套场景推进句法

因此，更合适的不是“主架构卡系统”，而是“协议栈系统”。

## 设计总结

采用：

`番茄起盘协议栈 + compiler + 两本账`

而不是：

- 单一“主架构卡”
- 大而全的剧情架构资料库
- 直接把通用西方结构当运行时规则

这个协议栈由 6 层组成：

1. `Premise Layer`
2. `Pivot Layer`
3. `Launch Grammar Layer`
4. `Retention Protocol Layer`
5. `Genre Obligations Layer`
6. `Scene Engine Layer`

运行时不直接输出“这本书是三幕式还是 Story Circle”，而是输出一个轻量 `launch_stack`。

再由一层 `compiler` 把 `launch_stack` 编译成各 skill 能吃的输入：

- `outline_focus`
- `chapter_1_3_targets`
- `review_watchpoints`
- `precheck_risks`
- `package_guardrails`

## 为什么这一层更符合番茄

### 1. 番茄官方写作课的入口不是“先选大结构”

番茄 2023-04-26 的“写在落笔前，如何构思一本男频网文小说”把入口组织为：

- 一句话故事
- 故事支点
- 切入事件
- 三幕式 / 节拍器

这说明平台原生语境里，更先于“大结构名称”的，是：

- 作品靠什么起盘
- 从哪里切进去
- 为什么第一屏能留下人

因此，系统优先判断 `premise + pivot + launch grammar`，比优先判断“主架构卡”更贴平台。

### 2. 番茄更关心留人和追读协议

番茄 2026-02-21 的“如何稳定剧情，让读者追更不停？”更强调：

- 首页见山
- 章末留钩
- 前十万字稳定

这类规则不是某个题材专属，而是平台级协议。

因此，必须单独抽出一层 `Retention Protocol Layer`，而不是把它塞进任何单一卡里。

### 3. 通用结构仍有价值，但更适合做映射参考

Save the Cat、三幕式、Story Circle、七点式依然有价值，但在本项目中，它们更适合作为：

- 解释语言
- 映射参考
- 校准工具

而不是番茄运行时真源。

## 协议栈结构

### 1. Premise Layer

职责：

- 锁一句话故事
- 明确主矛盾、目标、行动方向

目标不是写 marketing logline，而是给系统一个足够稳定的起盘压缩句。

建议输出：

- `premise_line`
- `premise_keywords`
- `promise_axis`

### 2. Pivot Layer

职责：

- 判断作品主要靠什么“故事支点”起盘

第一版建议的 `pivot_family`：

- `character-conflict`
- `rule-world`
- `gift-system`
- `mystery-gap`
- `transgressive-action`
- `inciting-event`

这层优先级高于“哪种结构名”，因为它更接近番茄原生起书方法。

建议输出：

- `primary_pivot`
- `secondary_pivot`
- `pivot_confidence`

### 3. Launch Grammar Layer

职责：

- 给系统一套前 1-3 章的推进语法

第一版保留 6 张“起盘语法卡”，但不再叫“主架构卡”：

- `oppression-breakout`
- `bonding-reversal`
- `rule-trial`
- `resource-climb`
- `investigation-reveal`
- `ensemble-return`

这层回答的问题不是“整本书属于哪种结构”，而是：

- 前三章最适合怎么推
- 第一次硬兑现该长什么样
- 场景推进最常见的句法是什么

建议输出：

- `launch_grammar.primary`
- `launch_grammar.candidates`
- `launch_grammar.confidence`

### 4. Retention Protocol Layer

职责：

- 把平台级留人规则独立出来

第一版建议固定一组默认协议：

- `first-page-hook`
- `chapter-end-hook`
- `hook-handover`
- `first-hard-payoff`
- `half-win-with-residual`
- `no-foolish-humiliation`
- `early-stability`

这层不选型，只加载和校正。

建议输出：

- `retention_protocol.enabled_rules`
- `retention_protocol.violations`
- `retention_protocol.priority_rules`

### 5. Genre Obligations Layer

职责：

- 处理题材或 bucket 在开篇与黄金三章阶段“必须交什么”

这层不负责平台通用协议，也不负责具体推进语法。

它负责的是类似 Story Grid 的：

- conventions
- obligatory moments

在项目语境里，它应该优先从现有 bucket overlays / checkcards 读取，而不是新造平行标准。

建议输出：

- `genre_obligations.required_beats`
- `genre_obligations.required_absences`
- `genre_obligations.bucket_overlays_used`

### 6. Scene Engine Layer

职责：

- 给单场景和单章一个统一推进句法

第一版建议只支持两种轻模板，二选一：

1. `Goal -> Conflict -> Outcome/Disaster -> Reaction -> Dilemma -> Decision`
2. `Inciting Incident -> Progressive Complications -> Crisis -> Climax -> Resolution`

这层不定义整本书，只定义局部推进语法。

建议输出：

- `scene_engine.name`
- `scene_engine.watchpoints`

## 两本账

### 1. Hook Ledger

职责：

- 记录已经埋下的钩子
- 这些钩子希望读者期待什么
- 预计在哪一章或哪一阶段回应
- 是否已经过量堆叠

最小字段建议：

- `hook_id`
- `hook_type`
- `promise`
- `planted_in`
- `expected_payoff_window`
- `status`

### 2. Payoff Ledger

职责：

- 记录已经完成的小兑现、反转、阶段胜利与代价残留

最小字段建议：

- `payoff_id`
- `payoff_type`
- `delivered_in`
- `cost_left`
- `next_residual`

为什么要有两本账：

- 避免系统只会埋钩，不会回收
- 避免系统只会给爽点，不留后果
- 让 `precheck` 和 `package` 有证据判断当前 promise 是否已兑现

## Compiler 设计

协议栈本身不直接供所有 skill 逐层消费。

运行时需要一层 `compiler` 做轻量编译，把 `launch_stack` 转成统一下游输入。

第一版 compiler 输出建议固定为：

- `outline_focus`
- `chapter_1_3_targets`
- `review_watchpoints`
- `precheck_risks`
- `package_guardrails`

这样做的原因：

- 避免每个 skill 自己解释协议栈
- 避免不同 skill 读出不同结论
- 把运行期消费接口稳定下来

## 选择与锁定流程

### 阶段 1：预选

触发时机：

- `novel-init`
- `novel-genre`

输入：

- `platform`
- `genre`
- `bucket`
- `title hook`
- 初始 `premise_line`

输出：

- `primary_pivot`
- `launch_grammar` 候选
- `confidence`

这一步只做预选，不锁死。

### 阶段 2：正式锁定

触发时机：

- `novel-outline`

输入增加：

- 总纲
- 主要冲突
- 关系轴
- 升级轴
- 黄金三章承诺

输出：

- 第一版正式 `launch_stack`
- compiler 结果

### 阶段 3：黄金三章后校正

触发时机：

- `novel-precheck` 针对第 001-003 章时

行为：

- 默认只做校正，不做频繁漂移
- 若真实文本与当前 `launch_stack` 长期严重偏离，允许一次高阈值重选

不允许：

- 每章自动漂移
- 根据单次 review 临时换语法

## 运行结果契约

我建议运行期对象叫 `launch_stack`，而不是 `plot_architecture_selection`。

原因：

- 它表达的是组合协议，而不是单一卡片选型
- 名字更贴“起盘”而不是“全书结构”

建议字段：

- `version`
- `phase`
- `premise_line`
- `primary_pivot`
- `secondary_pivot`
- `launch_grammar`
- `retention_protocol`
- `genre_obligations`
- `scene_engine`
- `compiler_output`
- `hook_ledger_summary`
- `payoff_ledger_summary`
- `confidence`
- `drift_signal`
- `reselect_note`

## 写回策略

详细结果不直接塞进 `.mighty/state.json`。

建议：

- 详细对象写到 sidecar：
  - `.mighty/launch-stack.json`
  - `.mighty/hook-ledger.json`
  - `.mighty/payoff-ledger.json`
- `state` 只镜像轻字段：
  - `active_launch_grammar`
  - `active_primary_pivot`
  - `launch_stack_phase`
  - `launch_stack_drift_signal`

原则：

- 文档是真源
- sidecar 是运行结果
- state 只保留主链路由需要的最小字段

## 各 Skill 的消费边界

### `novel-outline`

消费：

- `premise_line`
- `primary_pivot`
- `launch_grammar`
- `genre_obligations`
- `outline_focus`
- `chapter_1_3_targets`

### `novel-write`

消费：

- `retention_protocol.priority_rules`
- `scene_engine`
- `chapter_1_3_targets`

### `novel-review`

消费：

- `review_watchpoints`
- `retention_protocol.violations`
- `hook_ledger_summary`
- `payoff_ledger_summary`

输出新增：

- `launch_alignment`
- `drift_signal`

### `novel-precheck`

消费：

- `precheck_risks`
- `retention_protocol`
- `hook_ledger_summary`
- `payoff_ledger_summary`

### `novel-package`

消费：

- `premise_line`
- `package_guardrails`
- `payoff_ledger_summary`

目的：

- 防止包装 promise 超过正文实际承载

## 与现有框架的关系

### 与 `opening-and-plot-framework`

- 新层应挂在其下
- 复用其“开篇目标 / 推进链 / 题材特化”结构
- 不重写已有 P0 overlays / checkcards

### 与 `writing-core-framework`

- 新层不接管正文技法
- 只决定起盘约束和早期兑现协议

### 与 `anti-flattening-framework`

- 新层不处理人物立体度主体逻辑
- 但其 `review_watchpoints` 可把“主角是否吃掉他人行动权”作为开篇风险之一

## 非目标

第一版明确不做：

- 整卷或整本全周期架构系统
- 每章自动换架构
- 直接把通用结构理论作为运行时真源
- 把完整推理过程塞进 `state`
- 把 bucket 规则重新复制一遍到新层

## 为什么这个方案优于“剧情架构资料库”

如果只做资料库：

- 系统不会自动消费
- 规则仍然散在 `outline / review / precheck / package` 之间
- 不足以支撑未来更强的自动 loop

如果只做“单主架构卡”：

- 会把平台协议、题材义务、场景句法混成一层
- 无法稳定解释真实的番茄早期留存问题

协议栈方案的好处是：

1. 分层清楚
2. 更贴番茄原生起盘逻辑
3. 更适合自动编译到 skill 消费接口
4. 更适合未来自动 loop 做闭环判断

## 第一版落地建议

第一版只落：

1. `Premise Layer`
2. `Pivot Layer`
3. `Launch Grammar Layer`
4. `Retention Protocol Layer`
5. compiler 最小合同
6. sidecar 设计

暂不落：

- 完整 `Genre Obligations` 重构
- 完整 `Hook Ledger / Payoff Ledger` 自动写回
- 多阶段中段推进扩展

也就是：

先把“协议栈骨架 + compiler 接口 + 留存协议层”跑通，再继续把账本写回自动化做深。

## 验收标准

这份设计被视为成立，至少需要满足：

1. 新层不与已有三个框架形成平行冲突
2. 能解释为什么“番茄起盘协议栈”比“单主架构卡”更合理
3. 能给后续实现提供清晰的文件边界、状态边界和 skill 消费边界
4. 范围被限制在开篇与黄金三章，不无限扩张

## 参考来源

- 番茄官方：写在落笔前，如何构思一本男频网文小说
  - https://fanqienovel.com/writer/zone/article/7226296687315124284
- 番茄官方：如何稳定剧情，让读者追更不停？
  - https://fanqienovel.com/writer/zone/article/7605818896267870270
- 番茄官方：开篇即爆点！三步公式打造高黏性开头（上）
  - https://fanqienovel.com/writer/zone/article/7478303864752455705
- 番茄官方：浅谈宫斗宅斗创作经验
  - https://fanqienovel.com/writer/zone/article/7273042943110283326
- Save the Cat：Genre Mapper
  - https://savethecat.com/tips-and-tactics/free-tool-alert-the-save-the-cat-genre-mapper
- Save the Cat：Beat Sheet Example
  - https://savethecat.com/beat-sheets/the-true-grit-beat-sheet
- Story Grid：Foolscap Global Story Grid
  - https://storygrid.com/wp-content/uploads/2017/04/foolscap-story-grid.pdf
- Story Grid：The 5 Commandments of Storytelling
  - https://storygrid.com/5-commandments-storytelling-revisited/
- Jane Friedman：The Joys (and Perils) of Serial Novel Writing
  - https://janefriedman.com/serial-novel-writing/
