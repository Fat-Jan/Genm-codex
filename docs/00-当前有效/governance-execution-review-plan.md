# Genm-codex 共享资产治理 — 执行与复检闭环方案

> 本文件用于：交给其他 agent 从头到尾完整执行一轮共享资产治理，执行完毕后由主 agent（你）统一复检并判定成功与否。
>
> 执行者只需按本文件顺序推进，无需中途回来确认。低风险动作默认执行，高风险动作才标记升级。
>
> 复检者（主 agent）按本文末的「复检标准」和「复检 Checklist」对结果进行统一审查。

---

## 一、背景与目标

### 1.1 项目现状

Genm-codex 是一个包含 shared 共享资产、skills 技能库、scripts 脚本、tests 测试、docs 文档的结构化项目。

当前已完成以下工作：
- shared/profiles 域系统性巡检（50 complete / 1 partial zhihu-short exception）
- shared/references 域系统性巡检（10 个保护项整体健康）
- templates 域 genre 保护名单三轮收缩（16 项移出）
- references 域边缘保护项收缩（chapter-index-schema.md / serial-generation-mode.md）
- 5 个 SKILL 中 consumer-read-manifest 声明降级
- 3 个 orphan 资产清理与归档
- profiles 稳定保留门槛清单已沉淀
- 阶段报告已收口

这些成果默认有效，本轮执行不得推翻。

### 1.2 本轮总体目标

1. **补齐 templates 域系统巡检**（当前唯一未完整收口的核心域）
2. **统一 profiles / references / templates 三域治理逻辑**
3. **将经验固化为可执行规则**
4. **增强验证与报告能力**
5. **整体收口并提交复检**

本轮执行不是推翻重来，而是在已有基线上继续推进，最终由主 agent 复检通过才算成功。

---

## 二、执行范围

本轮覆盖以下范围：

- `shared/profiles/**`
- `shared/references/**`
- `shared/templates/**`
- `shared/validators/**`
- `skills/**`
- `scripts/**`
- `tests/**`
- `docs/**`
- `shared/sync-governance.json`

---

## 三、总体执行原则

执行者必须严格遵循以下原则，否则最终复检会判定为方法不合格：

1. **先盘点、后搜证、再分级、再决策、再落地、再验证、再报告**——不允许跳过步骤直接改名单
2. **真实消费优先于声明存在**——文档写了、skill 提到了不等于真实运行依赖；scripts 装载、tests 约束、运行投影优先级更高
3. **不做大爆破**——禁止对 sync-governance.json 或 shared 目录做一轮性大规模清空式修改，必须按批次推进
4. **不确定时不删，先观察保留**——宁可留观察项，不能为了收缩而激进删除
5. **有替代关系时先归档，不直接删**
6. **每批次落地后必须跑验证**，验证通过才算当前批次完成
7. **所有执行必须留下清单、证据表、决策依据和结果记录**，没有记录的视为未执行

---

## 四、证据分级体系

对每个资产的消费强度按以下级别判断：

| 证据级别 | 定义 | 治理动作倾向 |
|---|---|---|
| **Level A：硬消费** | 被 scripts 直接读取；被主流程真实装载；被 tests 直接依赖；缺失会导致流程失败 | 继续保护 |
| **Level B：强软消费** | 被多个 skill/doc/workflow 持续引用；与主流程强绑定；虽非直接读取但实质影响输出 | 保护或观察保留，需补强证据 |
| **Level C：弱软消费** | 仅少量文档/单点 skill 引用；运行影响不稳定；缺失不一定立即暴露 | 倾向降级或观察保留 |
| **Level D：声明消费** | 仅在文档、清单、说明中声明存在；没有 scripts/tests/运行链证据 | 移出保护名单，必要时保留文件但降级治理级别 |
| **Level E：历史残留** | 已有替代机制；当前链路无直接使用；仅出于兼容或遗留保留 | 归档候选或删除候选 |

---

## 五、统一治理术语定义

执行者必须使用以下统一定义，不得自行发明其他分类词：

- **稳定保留**：结构完整 + 运行可投影 + 测试有兜底 + 证据链完整 + 无需 exception
- **观察保留**：证据尚不充分，但风险较高暂时保留的项；需要补证
- **保护降级**：从 protected_local_paths 移出，但文件本身保留
- **归档**：移出保护名单 + 放入 `docs/90-归档/` 并保留兼容说明
- **删除**：从文件系统中移除；通常只用于确认无任何消费且无兼容价值的项
- **例外 / exception**：结构不完整但有合理原因暂时保留的项；必须有 exception_type 说明

---

## 六、执行阶段与任务

执行分 5 个阶段顺序推进，不得跳阶段。

---

### 阶段 1：基线冻结

**目标**：确认本轮起始状态，防止执行中来回推翻。

**执行动作**：
1. 读取当前有效的治理文档（phase report、profile-stability-threshold-checklist、execution checklist、review checklist）
2. 记录 `sync-governance.json` 当前版本和 snapshot
3. 跑 `bash scripts/sync-shared-from-genm.sh --report` 记录当前 sync report 数值
4. 记录已归档/已删除/已降级项清单
5. 形成「本轮起始基线表」

**交付物**：
- `本轮起始基线.md`，包含：当前 sync-governance 版本、当前 sync report snapshot、当前有效文档清单、已归档/已删除/已降级项清单

**成功标准**：执行者不再反复问"当前算不算已经完成"，所有后续判断以此基线为起点。

---

### 阶段 2：templates 域系统巡检（重点）

**目标**：补齐当前三大核心 shared 域中唯一尚未完整收口的 templates 域。

**执行动作**：

**步骤 2.1：全量盘点**
- 列出 `shared/templates/**` 全部文件
- 标记哪些已在 `sync-governance.json` 的 `templates.protected_local_paths` 中
- 按以下 5 类做初步分类：
  - A：核心结构模板（state/schema/contract 类）
  - B：生成辅助模板（creative-brief/outline/chapter 结构）
  - C：规则/说明伴生模板（validation-rules/checklist 类）
  - D：历史兼容模板（已被替代但未清理）
  - E：说明性/声明性模板（文档提到但无脚本引用）

**交付物**：`templates-资产盘点表-v1.md`

| path | category | protected | suspected_usage | notes |
|---|---|---:|---|---|

**步骤 2.2：消费证据采集**
- 对每个模板搜索 scripts / tests / skills / docs 中的引用关系
- 判断每个模板的证据级别（A/B/C/D/E）
- 标记替代关系（是否有更新的机制已替代）

**交付物**：`templates-消费证据表-v1.md`

| path | scripts_ref | tests_ref | skills_ref | docs_ref | evidence_level | replacement | notes |
|---|---:|---:|---:|---:|---|---|---|

**步骤 2.3：分组决策**
将所有模板分成 5 个治理组：

| 治理组 | 条件 | 动作 |
|---|---|---|
| G1：必须继续保护 | Level A 或核心运行模板或主链条依赖明显 | 保持 protected |
| G2：观察保留 | Level B 或消费链不够强但删除风险高 | 保持 protected + 标记补证 |
| G3：保护降级 | Level C/D 且文件可保留但没必要强保护 | 移出 protected，文件保留 |
| G4：归档候选 | Level E 且有替代关系或历史兼容意义 | 移出 protected + 归档 |
| G5：删除候选 | Level E 且无消费、无兼容价值、无归档必要 | 删除文件 |

**交付物**：`templates-治理决策表-v1.md`

| path | evidence_level | group | action | risk | reason | alternative |
|---|---|---|---|---|---|---|

**步骤 2.4：分批落地**
按以下顺序执行（低风险优先）：

1. 先处理 G3（保护降级）
2. 再处理 G4（归档候选）
3. 再处理 G5（删除候选）
4. 最后处理 G2（观察保留）

每批落地动作包括：
- 更新 `sync-governance.json`
- 创建归档说明（如需要）
- 修正文档引用（如需要）
- 补测试/补说明（如需要）
- 跑 `bash scripts/validate-migration.sh`
- 跑 `bash scripts/sync-shared-from-genm.sh --report`
- 记录变更摘要

**交付物**：每批执行后的变更记录 + 最终 `templates-实际治理结果.md`

**步骤 2.5：巡检报告**
输出 `templates-域巡检报告.md`，包含：
- 执行摘要
- 全量盘点结论
- 证据分级结论
- 治理动作结果
- 当前状态快照
- 验证结果
- 待观察项
- 待下轮处理项

**成功标准**：
- templates 域全部资产有分类
- 所有保护项有证据级别
- 至少一轮低风险治理落地完成
- 验证通过
- 有正式巡检报告

---

### 阶段 3：三域统一治理规则

**目标**：把 profiles / references / templates 的治理逻辑统一成可复用总框架。

**执行动作**：
1. 抽取三域共同判断骨架（参考 profiles 稳定保留门槛清单的结构）
2. 统一定义：稳定保留 / 观察保留 / 保护降级 / 归档 / 删除 / 例外
3. 统一「保护收缩」准入/退出条件
4. 统一 exception 管理机制（可接受类型、证据要求、保留周期、复审周期）
5. 统一归档标准（什么可归档、归档命名、兼容说明要求）
6. 形成域内补充规则（如某域有特殊性）

**交付物**：`shared-asset-governance-unified-rules.md`

**成功标准**：执行者后续面对新资产可直接用此框架判断，无需重新发明标准。

---

### 阶段 4：自动化与验证增强

**目标**：把高频治理判断接入工具，减少人工记忆。

**执行动作**：
1. 审视现有 `scripts/validate-migration.sh` 和 `scripts/sync-shared-from-genm.sh --report` 的输出能力
2. 识别可自动化的判断：名单项文件不存在 / declared-only 候选 / orphan 候选 / drift 异常增多 / 保护项证据弱化
3. 补必要测试（如有新增 contract test 需求）
4. 增强 sync report 可读性（如有必要改进格式或字段）

**注意**：第一阶段自动化以"发现问题"为主，不引入高破坏性自动删除。

**交付物**：增强后的脚本改动说明或新增测试结果

**成功标准**：后续类似治理不再完全依赖人工搜索。

---

### 阶段 5：整体收口与提交复检

**目标**：将本轮所有执行结果统一汇总，形成可复检的完整交付物。

**执行动作**：
1. 汇总全部变更（对比基线）
2. 给出前后对比（保护名单变化 / 归档清单 / 删除清单 / 降级清单）
3. 说明本轮未完成项
4. 给出下一轮建议入口
5. 确保所有文档、名单、文件状态一致

**交付物**：
- `本轮整体治理报告.md`（执行摘要 + 各阶段结果 + 前后对比 + 验证结果 + 待观察项 + 待下轮项）
- `本轮变更清单.md`（列出所有改动的文件及其改动内容摘要）

**成功标准**：主 agent（复检者）能仅凭这两份文档判断本轮是否成功，无需重新搜索上下文。

---

## 七、默认执行规则（减少反复确认）

### 7.1 默认直接推进的事项

以下动作无需回来确认，执行者直接执行：

- 建立和更新盘点表、证据表、决策表
- 对 Level D/E 且无替代的 declared-only 模板提出降级建议
- 对 Level E 且有替代关系的历史模板提出归档建议
- 对 Level A 硬消费项保留保护
- 对文档/报告/阶段总结做同步更新
- 每批次后跑验证脚本和 sync report
- 更新 sync-governance.json 中的保护名单（低风险批次）
- 创建归档说明文件

### 7.2 默认暂停并升级的事项

以下动作必须标记升级，不自行决定：

- 要移出保护的对象属于核心 schema / 核心 contract / 主流程模板（Level A）
- 要进行 shared 目录结构重构
- 发现现有规则彼此矛盾
- 发现某项改动可能影响主流程输出
- 要引入 breaking change
- 要大规模重写 sync-governance.json 结构
- 遇到证据严重矛盾无法自行判断的情况

升级方式：在变更清单中标记 `[需要主 agent 确认]`，附上矛盾点说明，等待主 agent 回复后再决定。

### 7.3 默认风险处理规则

- 不确定时 → 不删，先观察保留
- 有替代关系时 → 不直接删，先归档
- 仅文档引用时 → 不当作硬消费
- 仅 skill 声明时 → 不自动视为保护必要
- 证据薄弱但风险高时 → 先保留并补证
- 争议项 → 进入 G2 观察保留，不强行归类

---

## 八、执行者必须提交的交付物清单

复检时没有以下任一项，直接降低复检评分：

1. `本轮起始基线.md`
2. `templates-资产盘点表-v1.md`
3. `templates-消费证据表-v1.md`
4. `templates-治理决策表-v1.md`
5. `templates-实际治理结果.md`
6. `templates-域巡检报告.md`
7. `shared-asset-governance-unified-rules.md`（或确认沿用现有规则并注明）
8. `本轮整体治理报告.md`
9. `本轮变更清单.md`
10. `bash scripts/validate-migration.sh` 的输出结果
11. `bash scripts/sync-shared-from-genm.sh --report` 的输出结果

---

## 九、复检标准（由主 agent 执行）

主 agent 收到执行者的全部交付物后，按以下标准进行复检。

### 9.1 方法合规性检查

执行者是否遵循了「先盘点、后搜证、再分级、再决策、再落地、再验证、再报告」的顺序？跳过步骤者视为方法不合格。

### 9.2 证据充分性检查

- 是否把文档声明误当成运行依赖？（docs/skills 引用 ≠ 硬消费）
- 是否把 skill 声明误当成保护必要？
- 是否遗漏了 scripts/tests 中的真实证据？
- 是否有明显证据薄弱却激进修改的情况？

### 9.3 决策稳健性检查

- 该保留的是否保留了？（Level A 是否都还在保护名单）
- 该降级的是否降级了？（Level D/E 是否移出保护名单）
- 该归档的是否归档了？（Level E + 有替代关系的是否进了归档流程）
- 是否存在"为了收缩而收缩"的激进行为？

### 9.4 验证闭环检查

- 是否跑了 validate-migration.sh？输出是否 clean？
- sync report 是否可解释？（保护名单变化是否有对应记录）
- 有无新增异常？（drift / orphan 异常爆发）
- 文档、名单、文件状态是否一致？

### 9.5 结果可持续性检查

- 是否留下了清晰的规则文档？（统一治理规则是否形成）
- 后续是否能继续按此方法推进？
- 是否减少了未来频繁确认的成本？

### 9.6 复检 Checklist

| 检查项 | 通过 | 部分通过 | 不通过 |
|---|---|---|---|
| 基线冻结完成 | 有完整基线表和 snapshot | 有基线但不完整 | 无基线或 snapshot |
| templates 全量盘点 | 100% 覆盖，有分类 | 部分遗漏 | 大面积遗漏 |
| templates 证据采集 | 每个保护项都有 evidence_level | 部分缺失 | 大面积缺失 |
| templates 决策分组 | 每个模板都有 G1~G5 归类 | 部分归类 | 未归类 |
| G3/G4/G5 批次落地 | 至少完成一轮且验证通过 | 部分落地 | 未落地 |
| templates 巡检报告 | 有正式报告且内容完整 | 有但不完整 | 无报告 |
| 统一治理规则 | 有统一规则文档 | 有但不完整 | 无 |
| 变更清单 | 有且可追溯 | 有但不完整 | 无 |
| validate-migration | clean | 有警告但可解释 | 失败 |
| sync report | 可解释 | 有小异常但可解释 | 大面积异常 |
| 方法合规性 | 全程顺序执行 | 部分跳步 | 严重跳步 |
| 证据充分性 | 无明显误判 | 少量误判 | 大面积误判 |
| 决策稳健性 | 无激进修改 | 少量激进 | 大面积激进 |
| 整体交付物 | 11 项全部提交 | 缺 1~3 项 | 缺 4 项以上 |

---

## 十、复检结论分级

主 agent 最终给出以下四种结论之一：

### A. 复检通过

- 方法合规
- 证据充分
- 决策稳健
- 验证闭环
- 交付物完整

→ 本轮治理成功，可进入下一轮。

### B. 基本通过

- 主体工作合格
- 少量边缘项需补充说明或小修正（不超过 3 处）

→ 小修后视为通过，主 agent 确认后进入下一轮。

### C. 部分通过

- 有成果，但方法或证据不够完整
- 3~5 处需要返工

→ 指定返工范围，执行者修正后重新提交复检。

### D. 不通过

- 方法严重跳步
- 证据大面积薄弱
- 决策激进或存在重大遗漏
- 验证未闭环

→ 需按正确方法重做对应部分后重新提交复检。

---

## 十一、复检后处置

- **通过 / 基本通过**：主 agent 宣布本轮成功，更新阶段报告，项目进入下一轮。
- **部分通过**：主 agent 列出具体返工项，执行者修正后重新提交复检（限一次返工机会）。
- **不通过**：主 agent 详细说明问题，执行者需重做对应部分后重新提交复检（限一次返工机会）。

---

## 十二、当前项目基线参考

执行者从本轮起始基线开始，不应推翻以下已确认的结论：

### sync-governance.json 当前状态（v1.2）

- templates protected：37 项
- references protected：10 项
- profiles protected：173 项
- genre 保护名单（9 项）：修仙 / 历史古代 / 历史脑洞 / 宫斗宅斗 / 悬疑灵异 / 职场婚恋 / 西幻 / 都市日常 / 都市脑洞

### profiles 域已知状态

- 50 complete，全部 ontology_ready = true
- 1 partial exception（zhihu-short，exception_type: zhihu-primary-source）
- cthulhu 和 livestream 经复核已确认稳定保留

### references 域已知状态

- 10 个保护项整体健康，无需大规模收缩

### 已完成归档

- novel-review-commands-legacy.md
- template-validation-rules-legacy.md
- post-write-validator-legacy.md

### 已完成降级

- consumer-read-manifest.md 从 required-like 降级为 reference-like（5 个 SKILL）

---

## 十三、关键文件路径参考

执行过程中需要频繁读取和修改的文件路径：

- `shared/sync-governance.json` — 保护名单源头
- `scripts/sync-shared-from-genm.sh` — sync report
- `scripts/validate-migration.sh` — 迁移验证
- `docs/00-当前有效/shared-asset-governance-phase-report-v1.md` — 当前阶段报告
- `docs/00-当前有效/profile-stability-threshold-checklist-v1.md` — profiles 稳定保留门槛清单（参考模板）
- `shared/profiles/**` — profiles 资产目录
- `shared/references/**` — references 资产目录
- `shared/templates/**` — templates 资产目录
- `docs/90-归档/` — 归档目录

---

> **最后提醒**：执行者不需要每步都回来确认。低风险事项按默认规则直接推进。遇到高风险或不确定事项才标记升级。所有执行结果按交付物清单要求留好记录。没有记录的动作视为未执行。
