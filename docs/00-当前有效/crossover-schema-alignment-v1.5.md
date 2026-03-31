# Crossover Schema 对齐 (`v1.5`)

> Status: `active-exception-spec`
>
> 当前定位：
> - `crossover/` 是特殊 schema 容器目录，不计入当前 `52/52` 标准 profile 覆盖口径
> - `crossover/*` 当前仍不进入标准 `profile_contract.py` 消费链
> - 本文的作用是说明例外边界与映射关系，而不是推动立即并轨

## 目的

这份文档定义了 `crossover/*` profile 的 schema 与标准 `profile_contract.py` schema 之间的映射关系。

**为什么需要这份文档？**
- `crossover/evil-female` 和 `crossover/god-of-war` 使用的是 `platform_enrichment/platform_guides` schema
- 它们与标准 `platform_positioning/reader_expectations/golden_three/taboos/strand_weights` schema 不同
- 需要一个映射来理解两者之间的关系，避免混淆

---

## Schema 对比

### 标准 Profile Schema (profile_contract.py)

```yaml
name: "题材名称"
display_name: "显示名称"
description: "题材描述"
version: "版本号"

# 推进阻力
progression_constraints:
  resistance_rule: "..."
  cost_rule: "..."
  partial_payoff_rule: "..."
  residual_risk_rule: "..."

# 读者期待
reader_expectations:
  must_satisfy: [...]
  optional_satisfy: [...]
  absolutely_not: [...]

# 黄金三章
golden_three:
  opening_hook: "..."
  protagonist_intro: "..."
  chapter_end: "..."

# 平台定位
platform_positioning:
  fanqie:
    primary_bucket: "..."
    strong_tags: [...]
    narrative_modes: [...]
    tone_guardrails: [...]
    package_cues: [...]

# 禁忌
taboos:
  - id: "TABOO-001"
    content: "..."
    severity: "..."
    check_point: "..."

# 检查器权重
checker_weights:
  consistency: 1.0
  pacing: 1.0
  ...

# 关联文件
related_files:
  key: value
```

### Crossover Profile Schema

```yaml
name: "题材名称"
version: "版本号"
description: "题材描述"

# 流派细分
sub_genres:
  - "sub_genre_1"
  - "sub_genre_2"

# 核心元素
core_elements:
  - "元素1"
  - "元素2"

# 平台富化
platform_enrichment:
  base_dimensions:
    - id: dimension_id
      name: "维度名称"
  
  platform_guides:
    fanqie:
      enrichment_priority:
        - dimension: dimension_id
          weight: 0.35
      content_focus:
        primary: [...]
        secondary: [...]
    qimao:
      ...
    qidian:
      ...
    jinjiang:
      ...

# 写作指南
writing_guidelines:
  pacing:
    fanqie: "节奏描述"
    qimao: "..."
    qidian: "..."
    jinjiang: "..."
  style_preferences:
    fanqie:
      - "风格描述"
    qimao:
      - "..."
    qidian:
      - "..."
    jinjiang:
      - "..."

# 角色模板
character_templates:
  protagonist:
    core_traits: [...]
    development_arc: [...]
  antagonist:
    common_types: [...]
    defeat_patterns: [...]

# 情节结构
plot_structures:
  common_patterns: [...]
  chapter_templates:
    opening: [...]
    climax: [...]
    ending: [...]

# 伏笔元素
foreshadowing_elements:
  common_hooks: [...]

# 成功指标
success_metrics:
  platform_optimization:
    fanqie: [...]
    qimao: [...]
    qidian: [...]
    jinjiang: [...]

# 元数据
metadata:
  author: "..."
  created_date: "..."
  last_updated: "..."
  tags: [...]
```

---

## 字段映射表

### 标准 Profile → Crossover

| 标准字段 | Crossover 等价物 | 映射说明 |
|---------|-----------------|---------|
| `name` | `name` | 直接对应 |
| `display_name` | 无 | Crossover 没有 display_name，需要从 metadata.tags 推断 |
| `description` | `description` | 直接对应 |
| `version` | `version` | 直接对应 |
| `progression_constraints` | 无 | Crossover 没有显式阻力约束，隐含在 plot_structures 中 |
| `reader_expectations` | `core_elements` + `success_metrics` | 核心元素 + 成功指标 |
| `golden_three` | `plot_structures.chapter_templates` | 章节模板 |
| `platform_positioning` | `platform_enrichment.platform_guides` | 平台指南 |
| `taboos` | 无 | Crossover 没有显式禁忌清单，隐含在 style_preferences 中 |
| `checker_weights` | `success_metrics` | 成功指标 |
| `related_files` | 无 | Crossover 没有关联文件 |
| `strand_weights` | `platform_enrichment.base_dimensions` | 维度权重 |
| `sub_genres` | `sub_genres` | 直接对应 |
| `character_templates` | `character_templates` | 直接对应 |
| `foreshadowing_elements` | `foreshadowing_elements` | 直接对应 |

### 平台定位映射

| 标准 `platform_positioning.fanqie` | Crossover `platform_enrichment.platform_guides.fanqie` |
|---|---|
| `primary_bucket` | 无（需从 `sub_genres` 推断） |
| `strong_tags` | `enrichment_priority` 中 weight 最高的维度 |
| `narrative_modes` | 无（需从 `plot_structures` 推断） |
| `tone_guardrails` | `content_focus.secondary` 中的约束 |
| `package_cues` | `content_focus.primary` 中的消费入口 |

---

## Crossover Profile 的当前状态

补充说明：

- 当前 `shared/profiles/README.md` 中的“52 个标准 profile 全量覆盖”不包含 `crossover/`
- `crossover/` 当前仍作为独立 schema 路径保留
- 因此这里的重点不是“还缺哪些基础文件”，而是“何时需要适配、何时保持例外”

### `crossover/evil-female`

**当前 schema**: `platform_enrichment/platform_guides`
**当前平台覆盖**: fanqie, qimao, qidian, jinjiang
**当前维度**: face_slapping, intelligence, relationship, psychological, action_details
**当前状态**: 不属于标准 profile_contract 消费链

### `crossover/god-of-war`

**当前 schema**: `platform_enrichment/platform_guides`
**当前平台覆盖**: fanqie, qimao, qidian, jinjiang
**当前维度**: combat, power_growth, territory, harem, strategy
**当前状态**: 不属于标准 profile_contract 消费链

---

## 对齐策略

### 策略 1: 保持现状（推荐）

- 不修改 crossover 文件的 schema
- 使用本映射文档来理解两者关系
- 当需要消费 crossover 资产时，通过映射函数转换

**优点**: 不破坏现有系统
**缺点**: 需要维护两套 schema

### 策略 2: 统一 schema

- 将 crossover 文件转换为标准 profile schema
- 使用 `platform_positioning` 替代 `platform_enrichment`
- 添加缺失的字段（如 `reader_expectations`、`golden_three`）

**优点**: 统一系统
**缺点**: 需要大量工作，可能破坏现有消费逻辑

### 策略 3: 创建适配层

- 创建一个适配器，将 crossover schema 转换为标准 schema
- 在 `profile_contract.py` 中添加 crossover 支持

**优点**: 不修改原始文件
**缺点**: 需要维护适配器

---

## 当前决策

**采用策略 1: 保持现状**

原因：
1. crossover 文件有其独立的价值（多平台富化）
2. 修改 schema 可能破坏现有消费逻辑
3. 使用映射文档足够理解两者关系
4. 当前不需要统一 schema

---

## 后续工作

### 短期

1. 维护本映射文档
2. 当需要消费 crossover 资产时，使用映射函数转换

### 中期

1. 如果发现 crossover 资产被频繁使用，考虑创建适配层
2. 在 `profile_contract.py` 中添加 crossover 支持

### 长期

1. 考虑是否统一 schema
2. 如果决定统一，制定详细的迁移计划

---

## 更新记录

- `2026-03-28`: 初始版本，覆盖 `crossover/evil-female` 和 `crossover/god-of-war`
- 后续每添加新的 crossover profile 应更新此文档
