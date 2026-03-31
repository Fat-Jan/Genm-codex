# Templates 域巡检报告

> 创建时间：2026-03-31
>
> 本报告为 templates 域系统巡检的完整输出。

---

## 一、执行摘要

本轮 templates 域系统巡检完成了以下工作：

1. **全量盘点**：70 个文件，分布在 genres、outline、project、characters 等目录
2. **消费证据采集**：完成全部文件的 evidence level 判定
3. **治理分组**：G1(21项) / G2(5项) / G3(9项) / G4(5项) / G5(14项)
4. **分批落地**：G4 归档执行（5项），G5 改为观察保留（14项）
5. **验证闭环**：validate-migration.sh 通过，sync report 正常

**核心结论**：templates 域核心结构（A类21项）全部有 scripts/tests 硬消费证据，保护合理。Genre 类（C类9项）前序已确认保护理由，本轮不推翻。G5 的 14 项无消费证据模板按照"不确定时不删"原则改为观察保留。

---

## 二、全量盘点结论

### 2.1 文件统计

| 分类 | 数量 | 说明 |
|---|---|---|
| 核心结构模板 | 21 | A类，schema/contract 类 |
| 生成辅助模板 | 3 | B类，creative-brief/outline 类 |
| 项目文档 | 11 | C/D/E类，truth-sheet/foreshadowing 等 |
| 角色/世界模板 | 7 | E类，character/world 类 |
| Genre 模板 | 24 | C/E类，9项保护中，15项已移出 |
| 历史兼容模板 | 2 | D类，旧版结构 |
| **合计** | **70** | |

### 2.2 目录分布

| 目录 | 文件数 |
|---|---|
| 根目录（.json schema） | 21 |
| genres/ | 24 |
| outline/ | 2 |
| project/ | 11（含已归档5项） |
| characters/ | 4 |
| chapter-structure/ | 3（含已归档2项） |
| entity-relation-graph.md | 1 |
| 伏笔/ | 1 |
| 悬念/ | 1 |
| world/ | 1 |
| character/ | 1 |

---

## 三、证据分级结论

### 3.1 分级统计

| 证据级别 | 数量 | 说明 |
|---|---|---|
| Level A：硬消费 | 21 | scripts/tests 直接引用，缺失会导致流程失败 |
| Level B：强软消费 | 5 | skills 持续引用，实质影响输出 |
| Level C：弱软消费 | 9 | creative-brief 中映射表参考 |
| Level D：声明消费 | 0 | - |
| Level E：历史残留 | 18 | 无消费证据或仅文档提及 |

### 3.2 Level A 核心结构（21项）

所有 Level A 项均有 scripts/tests 直接消费证据，是主流程的核心依赖：

- state-schema-v5.json、state-v5-template.json（状态管理核心）
- workflow-state-v2.json、workflow-state-v2.schema.json（工作流核心）
- profile-bucket-registry-v1.json（profile bucket 核心）
- learned-patterns schema + template（学习模式核心）
- sample-manifest schema + json（样本清单核心）
- market-data、market-adjustments、memory-context schema（数据层核心）
- content-positioning schema + map（内容定位核心）
- acquire-provider-registry-v1.json（来源文本获取核心）
- skill-merge-map schema + json（技能合并核心）
- sidecar-freshness-registry-v1.json（新鲜度管理核心）
- research-candidates-v1.schema.json（研究候选核心）
- profile-contract-v1.schema.json（profile contract 核心）

### 3.3 Level B 强软消费（5项）

| 文件 | skills_ref | 说明 |
|---|---|---|
| project/creative-brief.md | 3个skill | novel-init/novel-outline/novel-package 声明使用 |
| project/ancient-household-truth-sheet.md | 2个skill | novel-init/novel-outline 声明使用 |
| project/ancient-mini-genealogy.md | 2个skill | novel-init/novel-outline 声明使用 |
| project/ancient-office-truth-sheet.md | 2个skill | novel-init/novel-outline 声明使用 |
| project/ancient-power-ladder.md | 2个skill | novel-init/novel-outline 声明使用 |

### 3.4 Level C 弱软消费（9项 Genre）

9项 genre 文件在 creative-brief.md 映射表中被参考，但非直接读取：

- genres/修仙.md、历史古代.md、历史脑洞.md、宫斗宅斗.md
- genres/悬疑灵异.md、职场婚恋.md、西幻.md
- genres/都市日常.md、都市脑洞.md

**说明**：这9项前序已确认保护理由（"强联动组或 creative-brief 默认映射主入口"），本轮维持 protected。

---

## 四、治理动作结果

### 4.1 执行动作汇总

| 治理组 | 数量 | 动作 | 状态 |
|---|---|---|---|
| G1 | 21 | 保持 protected | ✅ 完成 |
| G2 | 5 | 保持 protected | ✅ 完成 |
| G3 | 9 | 保持 protected | ✅ 完成（前序确认） |
| G4 | 5 | 归档 | ✅ 已归档 |
| G5 | 14 | 观察保留 | ✅ 保留（未删除） |

### 4.2 G4 归档详情

已归档至 `docs/90-归档/阶段/templates-历史模板归档-v1/`：

| 文件 | 归档原因 |
|---|---|
| chapter-structure/tomato-xiuxian-vol1.yaml | 旧版番茄修仙结构，已被新workflow取代 |
| chapter-structure/tomato-urban-superpower-vol1.yaml | 旧版番茄都市异能结构，已被新workflow取代 |
| project/foreshadowing.md | 伏笔模板概念已迁移 |
| project/parent-canon-import.md | 父级canon导入概念已迁移 |
| project/universe-canon.md | 宇宙canon概念已迁移 |

### 4.3 G5 观察保留详情

14 项无消费证据模板按"不确定时不删"原则保留观察：

| 文件 | 待确认事项 |
|---|---|
| project/style-profile.json | 确认 creative-brief 流程中是否引用 |
| project/stats.md | 确认项目统计使用场景 |
| project/index.md | 确认项目索引用途 |
| characters/protagonist.md | 确认角色卡模板是否还在使用 |
| characters/supporting.md | 确认角色卡模板是否还在使用 |
| characters/minor.md | 确认角色卡模板是否还在使用 |
| characters/antagonist.md | 确认角色卡模板是否还在使用 |
| character/character-card.md | 确认是否有替代模板 |
| entities/entity-relation-graph.md | 确认实体关系图用途 |
| 伏笔/伏笔模板.md | 确认伏笔追踪机制是否迁移 |
| 悬念/悬念模板.md | 确认悬念模板用途 |
| world/world-building.md | 确认世界观构建模板用途 |
| outline/main-outline.md | 确认大纲模板是否还在使用 |
| outline/chapter-outline.md | 确认章节大纲模板是否还在使用 |

---

## 五、当前状态快照

### 5.1 sync-governance.json templates.protected_local_paths

| 指标 | 数值 |
|---|---|
| 基线 | 37 项 |
| 本轮变化 | 0 项（归档项不在保护名单中） |
| 当前 | 37 项 |

### 5.2 文件系统

| 指标 | 基线 | 当前 |
|---|---|---|
| templates 文件总数 | 70 | 65 |
| 归档文件 | 0 | 5 |

### 5.3 保护名单结构

| 分类 | 数量 |
|---|---|
| 核心结构（.json schema） | 21 |
| Genre 保护项 | 9 |
| 生成辅助（creative-brief/outline） | 3 |
| 项目文档（truth-sheet/power-ladder） | 4 |
| **合计** | **37** |

---

## 六、验证结果

| 验证项 | 结果 |
|---|---|
| validate-migration.sh | ✅ 通过 |
| sync-shared-from-genm.sh --report | ✅ 正常输出 |
| 保护名单一致性 | ✅ 无 drift |
| 归档文件完整性 | ✅ 5项已归档 |

---

## 七、待观察项

以下事项需留待下一轮进一步评估：

1. **Genre 类 9 项的保护级别**：目前沿用前序治理结论继续保护，后续仅在出现更强反证时重新评估
2. **outline/main-outline.md 和 outline/chapter-outline.md**：当前可作为手工参考模板组保留，但仍缺少明确程序消费证据，后续如做模板库瘦身可继续确认

---

## 八、待下轮处理项

| 优先级 | 事项 | 说明 |
|---|---|---|
| 低 | outline 2项确认 | 后续如做模板库瘦身，再确认是否继续保留为手工参考模板组 |
| 低 | Genre 9项保护级别重新评估 | 仅当出现更强反证时重新评估 |

---

## 九、交付物清单

| 交付物 | 路径 | 状态 |
|---|---|---|
| templates-资产盘点表-v1.md | docs/00-当前有效/ | ✅ |
| templates-消费证据表-v1.md | docs/00-当前有效/ | ✅ |
| templates-治理决策表-v1.md | docs/00-当前有效/ | ✅ |
| templates-实际治理结果.md | docs/00-当前有效/ | ✅ |
| templates-域巡检报告.md | docs/00-当前有效/ | ✅ |
| templates-历史模板归档-v1/ | docs/90-归档/阶段/ | ✅ |

---

## 十、版本记录

| 版本 | 日期 | 更新内容 |
|---|---|---|
| v1 | 2026-03-31 | 初始版本，完成 templates 域系统巡检 |
