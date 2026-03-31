# Templates 实际治理结果

> 创建时间：2026-03-31
>
> 本文档记录本轮 templates 域实际执行的治理动作及结果。

---

## 一、本轮实际治理动作

### 1.1 G4 归档执行（5项）

| 文件 | 动作 | 结果 |
|---|---|---|
| chapter-structure/tomato-xiuxian-vol1.yaml | 归档 | ✅ 已归档至 docs/90-归档/阶段/templates-历史模板归档-v1/ |
| chapter-structure/tomato-urban-superpower-vol1.yaml | 归档 | ✅ 已归档 |
| project/foreshadowing.md | 归档 | ✅ 已归档 |
| project/parent-canon-import.md | 归档 | ✅ 已归档 |
| project/universe-canon.md | 归档 | ✅ 已归档 |

### 1.2 G5 最终处置修正（14项，保留文件）

| 文件 | 原计划动作 | 最终动作 | 原因 |
|---|---|---|---|
| project/style-profile.json | 删除候选 | 保留文件、非保护 | 属于 project/index 导航下的手工项目模板组 |
| project/stats.md | 删除候选 | 保留文件、非保护 | 属于 project/index 导航下的手工项目模板组 |
| project/index.md | 删除候选 | 保留文件、非保护 | 手工模板库导航入口，承担索引价值 |
| characters/protagonist.md | 删除候选 | 保留文件、非保护 | e2e 参考资料 README 明确引用 |
| characters/supporting.md | 删除候选 | 保留文件、非保护 | 与角色模板组共同构成手工角色建模模板 |
| characters/minor.md | 删除候选 | 保留文件、非保护 | 与角色模板组共同构成手工角色建模模板 |
| characters/antagonist.md | 删除候选 | 保留文件、非保护 | 与角色模板组共同构成手工角色建模模板 |
| character/character-card.md | 删除候选 | 保留文件、非保护 | 角色卡总模板，服务手工角色建模 |
| entities/entity-relation-graph.md | 删除候选 | 保留文件、非保护 | 与 novel-character graph 语义对应，属关系图模板 |
| 伏笔/伏笔模板.md | 删除候选 | 保留文件、非保护 | 手工伏笔设计模板，具有参考价值 |
| 悬念/悬念模板.md | 删除候选 | 保留文件、非保护 | 手工悬念设计模板，具有参考价值 |
| world/world-building.md | 删除候选 | 保留文件、非保护 | e2e 参考资料 README 明确引用 |
| outline/main-outline.md | 删除候选 | 保留文件、非保护 | e2e 参考资料 README 明确引用，为总纲模板 |
| outline/chapter-outline.md | 删除候选 | 保留文件、非保护 | 与 main-outline 共同组成手工大纲模板组 |

### 1.3 G1/G2/G3 保持不变

- G1（21项 Level A）：保持 protected ✅
- G2（5项 Level B）：保持 protected ✅
- G3（9项 Level C）：保持 protected ✅（前序已确认保护理由，本轮不推翻）

---

## 二、保护名单变化

### 2.1 templates.protected_local_paths 变化

| 状态 | 数量 |
|---|---|
| 基线（起始） | 37 |
| 本轮归档移出 | 0（归档项本来就不在保护名单中） |
| 当前 | 37 |

**结论**：templates.protected_local_paths 保持 37 项不变。

### 2.2 文件系统变化

| 状态 | 数量 |
|---|---|
| 基线（起始） | 70 |
| 本轮归档 | -5 |
| 当前 | 65 |

**结论**：本轮仅执行 G4 归档，不对 G5 14 项做删除处理。

---

## 三、验证结果

| 验证项 | 结果 |
|---|---|
| validate-migration.sh | ✅ 通过 |
| sync report | ✅ 正常输出 |
| 保护名单一致性 | ✅ 无 drift |

---

## 四、G5 最终结论

以下 14 项不再作为“删除候选”处理，而统一定位为：

> **非保护手工参考模板库**

它们不属于运行时硬消费资产，不进入 protected_local_paths；但具有以下价值之一，因此应保留文件：

- docs 级参考入口价值
- 手工写作模板价值
- 模板库导航价值
- 与现有 skill 输出语义的弱耦合价值

---

## 五、归档清单

归档文件已移至：`docs/90-归档/阶段/templates-历史模板归档-v1/`

归档记录文档：`docs/90-归档/阶段/templates-历史模板归档-v1.md`
