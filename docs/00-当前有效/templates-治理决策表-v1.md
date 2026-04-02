# Templates 治理决策表 v1

> 创建时间：2026-03-31
>
> 决策依据：templates-资产盘点表-v1.md + templates-消费证据表-v1.md

---

## 一、治理分组

### G1：必须继续保护（Level A）

**条件**：Level A 硬消费，或核心运行模板主链条依赖明显

| path | evidence_level | action | risk | reason | alternative |
|---|:---:|---|---|---|---|
| state-schema-v5.json | **A** | 保持 protected | 无 | scripts直接读取，tests直接依赖 | 无 |
| state-v5-template.json | **A** | 保持 protected | 无 | tests直接读取，state contracts核心 | 无 |
| state-archive-v1.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| workflow-state-v2.json | **A** | 保持 protected | 无 | scripts直接读取，tests直接依赖 | 无 |
| workflow-state-v2.schema.json | **A** | 保持 protected | 无 | tests直接依赖 | 无 |
| profile-bucket-registry-v1.json | **A** | 保持 protected | 无 | scripts直接读取，tests直接依赖 | 无 |
| learned-patterns.schema.json | **A** | 保持 protected | 无 | scripts直接读取，tests直接依赖 | 无 |
| learned-patterns-template.json | **A** | 保持 protected | 无 | tests直接依赖 | 无 |
| sample-manifest-v1.json | **A** | 保持 protected | 无 | scripts直接读取，tests直接依赖 | 无 |
| sample-manifest-v1.schema.json | **A** | 保持 protected | 无 | scripts直接读取，tests直接依赖 | 无 |
| market-data-v1.schema.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| market-adjustments-v1.schema.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| memory-context-v1.schema.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| content-positioning-v1.schema.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| content-positioning-map-v1.json | **A** | 保持 protected | 无 | build_content_positioning.py引用 | 无 |
| acquire-provider-registry-v1.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| skill-merge-map-v1.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| skill-merge-map-v1.schema.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| sidecar-freshness-registry-v1.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| research-candidates-v1.schema.json | **A** | 保持 protected | 无 | scripts直接读取 | 无 |
| profile-contract-v1.schema.json | **A** | 保持 protected | 无 | validate-migration.sh引用 | 无 |

**G1 总结**：21项，全部保持 protected，风险：无

---

### G2：观察保留（Level B）

**条件**：Level B 强软消费，消费链不够强但删除风险高

| path | evidence_level | action | risk | reason | alternative |
|---|:---:|---|---|---|---|
| project/creative-brief.md | **B** | 保持 protected | 低 | 3个skill声明使用，是novel-init和novel-outline的生成入口 | 无 |
| project/ancient-household-truth-sheet.md | **B** | 保持 protected | 低 | novel-outline和novel-init中声明使用 | 无 |
| project/ancient-mini-genealogy.md | **B** | 保持 protected | 低 | novel-outline和novel-init中声明使用 | 无 |
| project/ancient-office-truth-sheet.md | **B** | 保持 protected | 低 | novel-outline和novel-init中声明使用 | 无 |
| project/ancient-power-ladder.md | **B** | 保持 protected | 低 | novel-outline和novel-init中声明使用 | 无 |

**G2 总结**：5项，全部保持 protected，风险：低（skills声明引用）

---

### G3：保护降级（Level C）

**条件**：Level C 弱软消费，文件可保留但没必要强保护

| path | evidence_level | action | risk | reason | alternative |
|---|:---:|---|---|---|---|
| genres/修仙.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考，非直接读取 | 无替代，但风险低 |
| genres/历史古代.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考 | 无替代 |
| genres/历史脑洞.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考 | 无替代 |
| genres/宫斗宅斗.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考 | 无替代 |
| genres/悬疑灵异.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考 | 无替代 |
| genres/职场婚恋.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考 | 无替代 |
| genres/西幻.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考 | 无替代 |
| genres/都市日常.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考 | 无替代 |
| genres/都市脑洞.md | **C** | 降级保护 | 低 | 仅在creative-brief映射表中参考 | 无替代 |

**G3 总结**：9项，降级保护（从protected移出），但文件保留

**⚠️ 注意**：这9项genre文件是前序治理已确认的"强保护项"，虽然当前证据为Level C，但前序报告明确说明"当前保留的 genre 保护项均为强联动组或 creative-brief 默认映射主入口"。**本轮不应推翻前序结论**。建议重新归类为"观察保留"而非"保护降级"。

**修正**：基于前序治理决策历史，这9项应保持 protected。

---

### G4：归档候选（Level E + 有替代或历史兼容意义）

**条件**：Level E，无消费证据，有替代关系或历史兼容意义

| path | evidence_level | action | risk | reason | alternative |
|---|:---:|---|---|---|---|
| chapter-structure/tomato-xiuxian-vol1.yaml | **E** | 归档 | 低 | 旧版番茄修仙结构，已被新workflow取代 | 无实际替代但已过时 |
| chapter-structure/tomato-urban-superpower-vol1.yaml | **E** | 归档 | 低 | 旧版番茄都市异能结构，已被新workflow取代 | 无实际替代但已过时 |
| project/foreshadowing.md | **E** | 归档 | 低 | 伏笔模板概念已迁移至其他机制 | 无消费证据 |
| project/parent-canon-import.md | **E** | 归档 | 低 | 父级canon导入概念已迁移至其他机制 | 无消费证据 |
| project/universe-canon.md | **E** | 归档 | 低 | 宇宙canon概念已迁移至其他机制 | 无消费证据 |

**G4 总结**：5项，归档候选

---

### G5：非保护手工参考模板库（Level C，保留文件）

**条件**：无运行时硬消费，但存在 docs 级参考价值、模板组导航价值或人工写作模板价值

| path | evidence_level | action | risk | reason | alternative |
|---|:---:|---|---|---|---|
| project/style-profile.json | **C** | 保留文件、非保护 | 低 | 由 project/index 导航，属于项目模板组组成部分 | 无 |
| project/stats.md | **C** | 保留文件、非保护 | 低 | 由 project/index 导航，属于项目模板组组成部分 | 无 |
| project/index.md | **C** | 保留文件、非保护 | 低 | 手工模板库导航入口，承担索引价值 | 无 |
| characters/protagonist.md | **C** | 保留文件、非保护 | 低 | e2e 参考资料 README 明确引用 | 无 |
| characters/supporting.md | **C** | 保留文件、非保护 | 低 | 与角色模板组共同构成手工角色建模模板 | 无 |
| characters/minor.md | **C** | 保留文件、非保护 | 低 | 与角色模板组共同构成手工角色建模模板 | 无 |
| characters/antagonist.md | **C** | 保留文件、非保护 | 低 | 与角色模板组共同构成手工角色建模模板 | 无 |
| character/character-card.md | **C** | 保留文件、非保护 | 低 | 角色卡总模板，服务手工角色建模 | 无 |
| entities/entity-relation-graph.md | **C** | 保留文件、非保护 | 低 | 与 novel-character graph 语义对应，属关系图模板 | 无 |
| 伏笔/伏笔模板.md | **C** | 保留文件、非保护 | 低 | 手工伏笔设计模板，具有明显参考价值 | 无 |
| 悬念/悬念模板.md | **C** | 保留文件、非保护 | 低 | 手工悬念设计模板，具有明显参考价值 | 无 |
| world/world-building.md | **C** | 保留文件、非保护 | 低 | e2e 参考资料 README 明确引用 | 无 |
| outline/main-outline.md | **C** | 保留文件、非保护 | 低 | e2e 参考资料 README 明确引用，为总纲模板 | 无 |
| outline/chapter-outline.md | **C** | 保留文件、非保护 | 低 | 与 main-outline 共同组成手工大纲模板组 | 无 |

**G5 总结**：14项，不再视为删除候选；统一改判为“非保护手工参考模板库”。

---

### 已处理项（无需重复处理）

以下项在本轮开始前已从 protected 移出，文件仍存在但已降级：

| path | 原状态 | 当前状态 | 说明 |
|---|---|---|---|
| genres/黑暗题材.md | protected | 非保护 | 前序第三批已移出 |
| genres/都市异能.md | protected | 非保护 | 前序第三批已移出 |
| genres/规则怪谈.md | protected | 非保护 | 前序第三批已移出 |
| genres/知乎短篇.md | protected | 非保护 | 前序第二批已移出 |
| genres/抗战谍战.md | protected | 非保护 | 前序第三批已移出 |
| genres/悬疑脑洞.md | protected | 非保护 | 前序第二批已移出 |
| genres/女频悬疑.md | protected | 非保护 | 前序第二批已移出 |
| genres/直播文.md | protected | 非保护 | 前序第一批已移出 |
| genres/无限流.md | protected | 非保护 | 前序第三批已移出 |
| genres/克苏鲁.md | protected | 非保护 | 前序第一批已移出 |
| genres/高武.md | protected | 非保护 | 前序第三批已移出 |
| genres/电竞.md | protected | 非保护 | 前序第三批已移出 |
| genres/种田.md | protected | 非保护 | 前序第三批已移出 |
| genres/末世.md | protected | 非保护 | 前序第三批已移出 |
| genres/年代.md | protected | 非保护 | 前序第二批已移出 |
| genres/现实题材.md | protected | 非保护 | 前序第二批已移出 |

---

## 二、治理动作汇总

| 治理组 | 数量 | 动作 | 说明 |
|---|---|---|---|
| G1 | 21 | 保持 protected | Level A，无风险 |
| G2 | 5 | 保持 protected | Level B，低风险，前序已确认 |
| G3 (修正) | 9 | 保持 protected | Level C，前序已确认保护理由，不推翻 |
| G4 | 5 | 归档 | Level E + 历史兼容 |
| G5 | 14 | 保留文件、非保护 | 手工参考模板库，不进入删除流程 |

---

## 三、本轮实际治理动作

基于"不确定时不删，先观察保留"原则及补充复核结果，本轮执行以下低风险动作：

1. **G4 归档**（5项）：低风险历史兼容模板归档
2. **G5 结论修正**（14项）：从删除候选/观察保留修正为非保护手工参考模板库

**⚠️ 不执行**：
- G3 的9项 genre 降级（前序已确认保护理由，不推翻）
- 任何 protected_local_paths 的增加动作
- 对 G5 14 项执行删除动作

---

> 后续步骤：围绕 G5 这组手工参考模板，进入常态治理而非删除治理。
