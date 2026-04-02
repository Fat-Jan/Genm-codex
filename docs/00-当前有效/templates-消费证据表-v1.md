# Templates 消费证据表 v1

> 创建时间：2026-03-31
>
> 依据：scripts/tests/skills/docs 中的实际引用

---

## 一、证据采集结果

### 1.1 A类：核心结构模板（Level A 硬消费）

| path | scripts_ref | tests_ref | skills_ref | docs_ref | evidence_level | replacement | notes |
|---|:---:|:---:|:---:|:---:|---|---|---|
| state-schema-v5.json | ✅ 多处 | ✅ 多处 | - | - | **A** | 无 | 状态schema核心，scripts直接读取 |
| state-v5-template.json | ✅ 多处 | ✅ 多处 | - | - | **A** | 无 | 状态模板核心，tests直接读取 |
| state-archive-v1.json | ✅ | - | - | - | **A** | 无 | 状态归档 |
| workflow-state-v2.json | ✅ | ✅ | - | - | **A** | 无 | 工作流状态 |
| workflow-state-v2.schema.json | - | ✅ | - | - | **A** | 无 | 工作流schema |
| profile-bucket-registry-v1.json | ✅ | ✅ | - | - | **A** | 无 | bucket注册表 |
| learned-patterns.schema.json | ✅ | ✅ | - | - | **A** | 无 | 学习模式schema |
| learned-patterns-template.json | - | ✅ | - | - | **A** | 无 | 学习模式模板 |
| sample-manifest-v1.json | ✅ | ✅ | - | - | **A** | 无 | 样本清单 |
| sample-manifest-v1.schema.json | ✅ | ✅ | - | - | **A** | 无 | 样本清单schema |
| market-data-v1.schema.json | ✅ | - | - | - | **A** | 无 | 市场数据schema |
| market-adjustments-v1.schema.json | ✅ | - | - | - | **A** | 无 | 市场调整schema |
| memory-context-v1.schema.json | ✅ | - | - | - | **A** | 无 | 记忆上下文schema |
| content-positioning-v1.schema.json | ✅ | - | - | - | **A** | 无 | 内容定位schema |
| content-positioning-map-v1.json | ✅ | - | - | - | **A** | 无 | 内容定位图，build_content_positioning.py引用 |
| acquire-provider-registry-v1.json | ✅ | - | - | - | **A** | 无 | 获取提供者注册表 |
| skill-merge-map-v1.json | ✅ | - | - | - | **A** | 无 | 技能合并映射 |
| skill-merge-map-v1.schema.json | ✅ | - | - | - | **A** | 无 | 技能合并schema |
| sidecar-freshness-registry-v1.json | ✅ | - | - | - | **A** | 无 | sidecar新鲜度注册表 |
| research-candidates-v1.schema.json | ✅ | - | - | - | **A** | 无 | 研究候选schema |
| profile-contract-v1.schema.json | ✅ validate-migration.sh:102 | - | - | - | **A** | 无 | profile contract schema，validate-migration.sh引用 |

### 1.2 B类：生成辅助模板（Level B/C 软消费）

| path | scripts_ref | tests_ref | skills_ref | docs_ref | evidence_level | replacement | notes |
|---|:---:|:---:|:---:|:---:|---|---|---|
| project/creative-brief.md | - | - | ✅ 3个skill | ✅ | **B** | 无 | creative-brief.md在skills中被声明使用，是生成入口 |
| outline/main-outline.md | - | - | - | ✅ e2e参考 | **C** | 无替代 | e2e-novel/参考资料/README.md 明确列为参考模板 |
| outline/chapter-outline.md | - | - | - | ✅ 目录级搭配 | **C** | 无替代 | 与 main-outline / 角色 / 世界观模板构成手工大纲模板组 |

### 1.3 C类：项目文档（Level B 软消费）

| path | scripts_ref | tests_ref | skills_ref | docs_ref | evidence_level | replacement | notes |
|---|:---:|:---:|:---:|:---:|---|---|---|
| project/ancient-household-truth-sheet.md | - | - | ✅ 2个skill | - | **B** | 无 | novel-outline和novel-init中声明使用 |
| project/ancient-mini-genealogy.md | - | - | ✅ 2个skill | - | **B** | 无 | novel-outline和novel-init中声明使用 |
| project/ancient-office-truth-sheet.md | - | - | ✅ 2个skill | - | **B** | 无 | novel-outline和novel-init中声明使用 |
| project/ancient-power-ladder.md | - | - | ✅ 2个skill | - | **B** | 无 | novel-outline和novel-init中声明使用 |

### 1.4 D/E类：弱消费或参考型手工模板

| path | scripts_ref | tests_ref | skills_ref | docs_ref | evidence_level | replacement | notes |
|---|:---:|:---:|:---:|:---:|---|---|---|
| project/style-profile.json | - | - | - | ✅ project/index | **C** | 无 | 项目模板索引中的一部分，属于手工参考模板 |
| project/stats.md | - | - | - | ✅ project/index | **C** | 无 | 项目模板索引中的一部分，属于手工参考模板 |
| project/index.md | - | - | - | ✅ 模板导航 | **C** | 无 | 手工模板库导航入口 |
| project/foreshadowing.md | - | - | - | - | **E** | 无 | 已归档 |
| project/parent-canon-import.md | - | - | - | - | **E** | 无 | 已归档 |
| project/universe-canon.md | - | - | - | - | **E** | 无 | 已归档 |
| characters/protagonist.md | - | - | - | ✅ e2e参考 | **C** | 无 | e2e-novel/参考资料/README.md 明确列为参考模板 |
| characters/supporting.md | - | - | - | ✅ 模板组搭配 | **C** | 无 | 与 protagonist/minor/antagonist 组成角色模板组 |
| characters/minor.md | - | - | - | ✅ 模板组搭配 | **C** | 无 | 与 protagonist/supporting/antagonist 组成角色模板组 |
| characters/antagonist.md | - | - | - | ✅ 模板组搭配 | **C** | 无 | 与 protagonist/supporting/minor 组成角色模板组 |
| character/character-card.md | - | - | - | ✅ 模板组搭配 | **C** | 无 | 角色卡总模板，服务手工角色建模 |
| entities/entity-relation-graph.md | - | - | ✅ novel-character(graph) 语义对应 | - | **C** | 无 | 实体关系图模板，与 novel-character graph 输出语义一致 |
| 伏笔/伏笔模板.md | - | - | - | ✅ 模板组搭配 | **C** | 无 | 手工伏笔设计模板，属参考模板库组成部分 |
| 悬念/悬念模板.md | - | - | - | ✅ 模板组搭配 | **C** | 无 | 手工悬念设计模板，属参考模板库组成部分 |
| world/world-building.md | - | - | - | ✅ e2e参考 | **C** | 无 | e2e-novel/参考资料/README.md 明确列为参考模板 |
| chapter-structure/tomato-xiuxian-vol1.yaml | - | - | - | ✅ e2e参考 | **E** | 无替代 | 仅在参考资料README中提及，已归档 |
| chapter-structure/tomato-urban-superpower-vol1.yaml | - | - | - | ✅ e2e参考 | **E** | 无替代 | 仅在参考资料README中提及，已归档 |

### 1.5 Genre 类（Level C 弱软消费）

| path | scripts_ref | tests_ref | skills_ref | docs_ref | evidence_level | replacement | notes |
|---|:---:|:---:|:---:|:---:|---|---|---|
| genres/修仙.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/历史古代.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/历史脑洞.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/宫斗宅斗.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/悬疑灵异.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/职场婚恋.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/西幻.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/都市日常.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/都市脑洞.md | - | - | - | ✅ creative-brief | **C** | 无替代 | creative-brief中做映射表参考 |
| genres/黑暗题材.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/都市异能.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/规则怪谈.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/知乎短篇.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/抗战谍战.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/悬疑脑洞.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/女频悬疑.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/直播文.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/无限流.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/克苏鲁.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/高武.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/电竞.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/种田.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/末世.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/年代.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |
| genres/现实题材.md | - | - | - | - | **E** | 无替代 | 已移出保护名单但文件存在 |

---

## 二、证据分级统计

| 证据级别 | 数量 | 说明 |
|---|---|---|
| **Level A：硬消费** | 21 | scripts/tests直接引用，缺失会导致流程失败 |
| **Level B：强软消费** | 5 | skills持续引用，实质影响输出 |
| **Level C：弱软消费/参考型消费** | 23 | creative-brief 映射参考，或 docs/模板组语义支撑的手工模板库 |
| **Level D：声明消费** | 0 | - |
| **Level E：历史残留** | 7 | 已归档或无进一步参考价值 |

---

## 三、关键发现

1. **A类21项全部有scripts/tests直接消费证据**，保护合理
2. **B类5项有skills声明引用**，creative-brief是生成入口，4个truth-sheet/power-ladder在skills中被引用
3. **C类除9项genre文件外，还存在一组 docs/模板库层面的手工参考模板**，不属于运行时硬消费，但有明显参考价值
4. **原先判为 G5 删除候选的14项，并非纯废件**，更准确的定位是“非保护手工参考模板库”
5. **E类仅剩已归档或无进一步参考价值的历史项**

---

> 后续步骤：根据本证据表，进行 G5 结论修正与常态治理收口。
