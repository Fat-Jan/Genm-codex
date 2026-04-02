# Templates 资产盘点表 v1

> 创建时间：2026-03-31
>
> 盘点范围：shared/templates/**

---

## 一、全量文件清单

共 **70 个文件**，分布在以下目录：

| 目录 | 文件数 |
|---|---|
| 根目录（.json schema） | 21 |
| genres/ | 24 |
| outline/ | 2 |
| project/ | 11 |
| characters/ | 4 |
| chapter-structure/ | 3 |
| entity-relation-graph.md | 1 |
| 伏笔/ | 1 |
| 悬念/ | 1 |
| world/ | 1 |
| character/ | 1 |

---

## 二、按分类初步分类

### 2.1 A类：核心结构模板（state/schema/contract 类）

| path | protected | notes |
|---|:---:|---|
| state-schema-v5.json | ✅ | 状态schema，核心运行模板 |
| state-v5-template.json | ✅ | 状态模板，核心运行模板 |
| state-archive-v1.json | ✅ | 状态归档 |
| workflow-state-v2.json | ✅ | 工作流状态 |
| workflow-state-v2.schema.json | ✅ | 工作流状态schema |
| profile-bucket-registry-v1.json | ✅ | profile bucket注册表 |
| profile-contract-v1.schema.json | ✅ | profile contract schema |
| learned-patterns.schema.json | ✅ | 学习模式schema |
| learned-patterns-template.json | ✅ | 学习模式模板 |
| sample-manifest-v1.json | ✅ | 样本清单 |
| sample-manifest-v1.schema.json | ✅ | 样本清单schema |
| market-data-v1.schema.json | ✅ | 市场数据schema |
| market-adjustments-v1.schema.json | ✅ | 市场调整schema |
| memory-context-v1.schema.json | ✅ | 记忆上下文schema |
| content-positioning-v1.schema.json | ✅ | 内容定位schema |
| content-positioning-map-v1.json | ✅ | 内容定位图 |
| acquire-provider-registry-v1.json | ✅ | 获取提供者注册表 |
| skill-merge-map-v1.json | ✅ | 技能合并映射 |
| skill-merge-map-v1.schema.json | ✅ | 技能合并映射schema |
| sidecar-freshness-registry-v1.json | ✅ | sidecar新鲜度注册表 |
| research-candidates-v1.schema.json | ✅ | 研究候选schema |

### 2.2 B类：生成辅助模板（creative-brief/outline/chapter 结构）

| path | protected | notes |
|---|:---:|---|
| project/creative-brief.md | ✅ | 创意简报，主生成入口 |
| outline/main-outline.md | ✅ | 主大纲模板 |
| outline/chapter-outline.md | ✅ | 章节大纲模板 |

### 2.3 C类：规则/说明伴生模板（validation-rules/checklist 类）

| path | protected | notes |
|---|:---:|---|
| project/style-profile.json | ❌ | 风格profile |
| project/stats.md | ❌ | 统计数据 |
| project/index.md | ❌ | 项目索引 |

### 2.4 D类：历史兼容模板（已被替代但未清理）

| path | protected | notes |
|---|:---:|---|
| chapter-structure/tomato-xiuxian-vol1.yaml | ❌ | 旧版番茄修仙结构 |
| chapter-structure/tomato-urban-superpower-vol1.yaml | ❌ | 旧版番茄都市异能结构 |

### 2.5 E类：说明性/声明性模板（文档提到但无脚本引用）

| path | protected | notes |
|---|:---:|---|
| project/ancient-household-truth-sheet.md | ✅ | 古风家族truth sheet |
| project/ancient-mini-genealogy.md | ✅ | 古风家族小谱系 |
| project/ancient-office-truth-sheet.md | ✅ | 古风官场truth sheet |
| project/ancient-power-ladder.md | ✅ | 古风权力阶梯 |
| project/foreshadowing.md | ❌ | 伏笔模板 |
| project/parent-canon-import.md | ❌ | 父级 canon 导入 |
| project/universe-canon.md | ❌ | 宇宙 canon |
| characters/protagonist.md | ❌ | 主角角色卡 |
| characters/supporting.md | ❌ | 配角角色卡 |
| characters/minor.md | ❌ | 配角角色卡 |
| characters/antagonist.md | ❌ | 反派角色卡 |
| character/character-card.md | ❌ | 角色卡 |
| entities/entity-relation-graph.md | ❌ | 实体关系图 |
| 伏笔/伏笔模板.md | ❌ | 伏笔模板 |
| 悬念/悬念模板.md | ❌ | 悬念模板 |
| world/world-building.md | ❌ | 世界观构建 |

### 2.6 Genre 类（特殊分类）

| path | protected | notes |
|---|:---:|---|
| genres/修仙.md | ✅ | 强保护genre |
| genres/历史古代.md | ✅ | 强保护genre |
| genres/历史脑洞.md | ✅ | 强保护genre |
| genres/宫斗宅斗.md | ✅ | 强保护genre |
| genres/悬疑灵异.md | ✅ | 强保护genre |
| genres/职场婚恋.md | ✅ | 强保护genre |
| genres/西幻.md | ✅ | 强保护genre |
| genres/都市日常.md | ✅ | 强保护genre |
| genres/都市脑洞.md | ✅ | 强保护genre |
| genres/黑暗题材.md | ❌ | 已移出保护名单 |
| genres/都市异能.md | ❌ | 已移出保护名单 |
| genres/规则怪谈.md | ❌ | 已移出保护名单 |
| genres/知乎短篇.md | ❌ | 已移出保护名单 |
| genres/抗战谍战.md | ❌ | 已移出保护名单 |
| genres/悬疑脑洞.md | ❌ | 已移出保护名单 |
| genres/女频悬疑.md | ❌ | 已移出保护名单 |
| genres/直播文.md | ❌ | 已移出保护名单 |
| genres/无限流.md | ❌ | 已移出保护名单 |
| genres/克苏鲁.md | ❌ | 已移出保护名单 |
| genres/高武.md | ❌ | 已移出保护名单 |
| genres/电竞.md | ❌ | 已移出保护名单 |
| genres/种田.md | ❌ | 已移出保护名单 |
| genres/末世.md | ❌ | 已移出保护名单 |
| genres/年代.md | ❌ | 已移出保护名单 |
| genres/现实题材.md | ❌ | 已移出保护名单 |

---

## 三、保护状态统计

| 分类 | 保护中 | 未保护 | 合计 |
|---|:---:|:---:|:---:|
| A类：核心结构 | 21 | 0 | 21 |
| B类：生成辅助 | 3 | 0 | 3 |
| C类：规则说明 | 0 | 3 | 3 |
| D类：历史兼容 | 0 | 2 | 2 |
| E类：说明声明 | 4 | 13 | 17 |
| Genre类 | 9 | 15 | 24 |
| **合计** | **37** | **33** | **70** |

---

## 四、初步观察

1. **A类核心结构全部受保护**（21项），符合预期
2. **B类生成辅助全部受保护**（3项），符合预期
3. **Genre 类有 15 项已移出保护名单但文件仍存在**，需进一步确认是否归档
4. **E类说明性模板有 13 项未受保护**，需进一步确认消费证据
5. **C/D类有 5 项**，需进一步确认是否有消费证据

---

> 后续步骤：根据本盘点表，进行步骤 2.2 消费证据采集。
