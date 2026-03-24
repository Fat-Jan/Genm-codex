---
name: state-schema
purpose: state.json 统一结构定义，作为所有模块的单一事实源
version: "1.0"
---

<context>
此文件定义 state.json 的完整结构，所有涉及状态存储的模块必须引用此文件。
禁止在其他文件中重复定义或修改此结构。如需更新，请修改本文件。
</context>

<instructions>

## State.json 完整结构

```json
{
  "entities": {
    "characters": {
      "protagonist": {
        "name": "",
        "power": { "realm": "", "level": "", "layer": 0 },
        "location": "",
        "inventory": [],
        "abilities": [],
        "status": [],
        "current_goals": [],
        "recent_events": []
      },
      "active": []
    },
    "items": { "tracked": [] },
    "locations": { "current": "", "previous": "", "visited": [] },
    "factions": { "active": [] }
  },
  "plot_threads": {
    "foreshadowing": { "active": [], "resolved": [] }
  },
  "knowledge_base": {
    "reader_knows": [],
    "protagonist_knows": [],
    "protagonist_unknown": []
  },
  "reading_power_state": {
    "active_hooks": [],
    "hook_history": [],
    "micro_fulfillment_log": [],
    "cool_point_log": []
  },
  "chapter_snapshots": {},
  "summaries_index": {},
  "updated_at": ""
}
```

---

## 一、实体结构 (entities)

### 1.1 主角结构 (entities.characters.protagonist)

```json
{
  "name": "林轩",
  "power": {
    "realm": "炼气",
    "level": "三层",
    "layer": 3
  },
  "location": "青云宗内门",
  "inventory": ["青云剑", "入门令牌"],
  "abilities": ["基础剑法", "青云诀一层"],
  "status": ["健康"],
  "current_goals": ["突破炼气四层", "参加宗门大比"],
  "recent_events": ["突破炼气期", "结识李青云"]
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 主角姓名 |
| power | object | 境界信息（结构化） |
| power.realm | string | 境界名称（如：炼气、筑基、金丹） |
| power.level | string | 境界等级（如：一层、三层） |
| power.layer | number | 层数（用于数值比较） |
| location | string | 当前位置 |
| inventory | string[] | 持有物品列表 |
| abilities | string[] | 已掌握能力/功法 |
| status | string[] | 状态标签（健康、受伤等） |
| current_goals | string[] | 当前目标列表 |
| recent_events | string[] | 最近发生的重要事件 |

### 1.2 活跃角色结构 (entities.characters.active)

```json
[
  {
    "name": "李青云",
    "role": "supporting",
    "identity": "青云宗内门弟子",
    "relation_to_protagonist": "师兄",
    "power": {
      "realm": "筑基",
      "level": "三层",
      "layer": 3
    },
    "first_appearance": 15,
    "last_mention": 18,
    "status": "active"
  }
]
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 角色姓名 |
| role | string | 角色类型：protagonist/supporting/antagonist/minor |
| identity | string | 身份描述 |
| relation_to_protagonist | string | 与主角关系 |
| power | object | 境界信息（结构化，同主角） |
| first_appearance | number | 首次出场章节 |
| last_mention | number | 最近提及章节 |
| status | string | 状态：active/archived/dead |

### 1.3 物品结构 (entities.items)

```json
{
  "tracked": [
    {
      "name": "青云剑",
      "type": "武器",
      "rank": "玄品下阶",
      "owner": "林轩",
      "status": "持有",
      "first_appearance": 12
    }
  ]
}
```

### 1.4 地点结构 (entities.locations)

```json
{
  "current": "青云宗内门",
  "previous": "青云宗外门",
  "visited": ["青云宗外门", "后山", "青云宗内门", "藏经阁"]
}
```

### 1.5 势力结构 (entities.factions)

```json
{
  "active": [
    {
      "name": "剑阁",
      "type": "宗门势力",
      "stance": "neutral",
      "relation_to_protagonist": "中立",
      "first_appearance": 3,
      "key_members": ["李青云", "王长老"]
    }
  ]
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 势力名称 |
| type | string | 势力类型：宗门势力/家族/联盟/组织 |
| stance | string | 立场：friendly/neutral/hostile |
| relation_to_protagonist | string | 与主角关系描述 |
| first_appearance | number | 首次出现章节 |
| key_members | string[] | 关键成员列表 |

---

## 二、剧情线索结构 (plot_threads)

### 2.1 伏笔结构 (plot_threads.foreshadowing)

```json
{
  "active": [
    {
      "id": "FS-001",
      "name": "神秘身世",
      "description": "主角的身世之谜",
      "planted_chapter": 1,
      "expected_resolve": "15-25",
      "status": "pending",
      "importance": "high",
      "mentions": [1, 5, 10]
    }
  ],
  "resolved": [
    {
      "id": "FS-002",
      "name": "玉佩秘密",
      "planted_chapter": 5,
      "resolved_chapter": 15,
      "resolution": "玉佩是上古传承之物"
    }
  ]
}
```

**伏笔状态**:

| 状态 | 说明 |
|------|------|
| planted | 刚埋设，尚未提及 |
| pending | 待回收，已有提及 |
| warning | 超期警告，接近预期回收上限 |
| overdue | 已超期，需要尽快回收 |
| resolved | 已回收 |

---

## 三、知识库结构 (knowledge_base)

```json
{
  "reader_knows": [
    "主角有神秘身世",
    "玉佩是传承之物"
  ],
  "protagonist_knows": [
    "自己有神秘身世"
  ],
  "protagonist_unknown": [
    "身世真相",
    "玉佩完整功能"
  ]
}
```

**字段说明**:

| 字段 | 说明 |
|------|------|
| reader_knows | 读者已知但主角可能不知道的信息 |
| protagonist_knows | 主角已知的信息 |
| protagonist_unknown | 主角尚不知道的重要信息（用于信息差管理） |

---

## 四、追读力状态结构 (reading_power_state)

### 4.1 活跃钩子 (active_hooks)

```json
[
  {
    "id": "hook_001",
    "type": "mystery",
    "introduced_chapter": 15,
    "content": "神秘玉佩的来历",
    "strength": "strong",
    "status": "active"
  }
]
```

**钩子类型**:

| 类型 | 说明 |
|------|------|
| crisis | 危机钩 |
| mystery | 悬念钩 |
| desire | 渴望钩 |
| emotion | 情绪钩 |
| choice | 选择钩 |

**钩子状态**:

| 状态 | 说明 |
|------|------|
| active | 活跃中 |
| partially_fulfilled | 部分兑现 |
| fulfilled | 已兑现 |

### 4.2 钩子历史 (hook_history)

```json
[
  {
    "chapter": 16,
    "hook_type": "crisis",
    "strength": "strong",
    "fulfilled_in": 17
  }
]
```

### 4.3 微兑现日志 (micro_fulfillment_log)

```json
[
  {
    "chapter": 16,
    "types": ["MF-02", "MF-04"],
    "count": 2,
    "details": ["与女主关系进展", "获得灵石奖励"]
  }
]
```

**微兑现类型**:

| ID | 类型 |
|----|------|
| MF-01 | 信息兑现 |
| MF-02 | 关系兑现 |
| MF-03 | 能力兑现 |
| MF-04 | 资源兑现 |
| MF-05 | 认可兑现 |
| MF-06 | 情绪兑现 |
| MF-07 | 线索兑现 |

### 4.4 爽点日志 (cool_point_log)

```json
[
  {
    "chapter": 16,
    "pattern": "CP-01",
    "execution": "complete",
    "intensity": "high"
  }
]
```

**执行状态**:

| 状态 | 说明 |
|------|------|
| complete | 完整执行 |
| partial | 部分执行 |
| failed | 执行失败 |

---

## 五、章节快照结构 (chapter_snapshots)

```json
{
  "15": {
    "chapter": 15,
    "created_at": "2026-03-14T10:30:00Z",
    "word_count": 5200,

    "protagonist_state": {
      "name": "林轩",
      "power": {
        "realm": "炼气",
        "level": "三层",
        "layer": 3
      },
      "location": {
        "current": "青云宗内门",
        "previous": "青云宗外门"
      },
      "inventory": ["青云剑", "入门令牌", "神秘玉佩"],
      "abilities": ["基础剑法", "青云诀一层"],
      "status": ["健康"],
      "current_goals": ["突破炼气四层", "参加宗门大比"]
    },

    "active_characters": [
      {
        "name": "李青云",
        "role": "师兄",
        "relation": "友好",
        "last_interaction": 15
      }
    ],

    "active_foreshadowing": [
      {
        "id": "FS-001",
        "name": "神秘身世",
        "status": "pending",
        "planted_chapter": 1
      }
    ],

    "knowledge_state": {
      "reader_knows": ["主角有神秘身世", "玉佩是传承之物"],
      "protagonist_knows": ["自己有神秘身世"],
      "protagonist_doesnt_know": ["身世真相", "玉佩完整功能"]
    },

    "new_entities": [
      {"type": "character", "name": "王长老", "role": "minor"},
      {"type": "location", "name": "藏经阁三层"}
    ],

    "key_events": [
      "林轩进入藏经阁",
      "发现功法秘籍",
      "与王长老对话"
    ],

    "summary": "林轩在李青云的引荐下进入藏经阁，获得重要功法，同时埋下新的伏笔。",

    "quality_metrics": {
      "overall": 82,
      "dimensions": {
        "爽点": 85,
        "一致性": 80,
        "节奏": 78,
        "OOC": 90,
        "连续性": 85,
        "追读力": 75
      }
    }
  }
}
```

---

## 五、章节元数据扩展约定 (chapter_meta)

`chapter_meta` 保持可扩展，但扩展必须落在单章级，不得额外新造平行顶层状态中心。

推荐字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| review_score | number | 当前章节总评 |
| review_grade | string | 当前章节评级 |
| review_time | string | 最近 review 时间 |
| dimension_scores | object | 评审维度分数 |
| recommended_next_action | string | `none/fix/polish/rewrite/write` 等路由建议 |
| anti_flattening_flags | string[] | 反脸谱化风险标签，保持轻量 |
| anti_flattening_summary | object | 可选结构摘要，记录主角特权、关系、阵营、代价链等问题 |
| fanqie_bucket_flags | string[] | 命中番茄 bucket 时的轻量风险标签 |
| fanqie_bucket_summary | object | 可选 bucket 级摘要，记录当前主故障与红灯 |
| content_standard_flags | string[] | 当前章节明确命中的内容标准失格标签 |
| packaging_alignment_note | string | 当前章节与外层包装承诺的轻量对齐说明 |
| active_launch_grammar | string | 当前生效的起盘语法，详细结果见 `.mighty/launch-stack.json` |
| active_primary_pivot | string | 当前主要起盘支点，详细结果见 `.mighty/launch-stack.json` |
| launch_stack_phase | string | 当前起盘协议栈阶段，如 `draft/locked/reselected` |
| launch_stack_drift_signal | string | 当前起盘协议栈漂移信号，如 `none/watch/strong` |
| last_close_time | string | 最近一次 `novel-close` 执行时间 |
| last_close_route | string | 最近一次 `novel-close` 选择的主路由 |
| last_close_review_score_before | number | 最近一次 `novel-close` 首轮 review 分数 |
| last_close_review_score_after | number | 最近一次 `novel-close` 末轮 review 分数 |

### 反脸谱化轻量约定

- `anti_flattening_flags` 只记录明显结构风险，不做大段分析存储
- `anti_flattening_summary` 只有在 review 明确识别到关键问题时才写
- 不为反脸谱化单独创建新的顶层 state 区块

### 番茄 bucket 轻量约定

- `fanqie_bucket_flags` 只在 bucket 级红灯清晰时写
- `fanqie_bucket_summary` 只保留主故障、红灯和 bucket 档位，不存长段评语
- 不为 bucket 专项检查单独创建新的顶层 state 区块

### 写作基本功压缩信号约定

- `learned_patterns.opening_strategy` 只保留当前项目可执行的开篇策略
- `learned_patterns.multi_line_guardrails` 只保留当前项目仍在生效的多线编排提醒
- `learned_patterns.content_standard_alerts` 只保留重复出现、值得下游消费的失格提醒
- `chapter_meta[N].content_standard_flags` 只在单章失格明确时写
- `chapter_meta[N].packaging_alignment_note` 只保留一句包装承诺对齐判断
- 这些字段都应保持轻量，不存课程长文

### 起盘协议栈轻量约定

- `active_launch_grammar` / `active_primary_pivot` 只记录当前生效结论
- `launch_stack_phase` / `launch_stack_drift_signal` 只记录阶段与漂移风险
- 详细 `launch_stack` 结果、候选与 compiler 输出，应保存在 `.mighty/launch-stack.json`
- 不为起盘协议栈新增顶层长分析区块

### `dimension_scores` 附加键约定

除已有质量维度外，可追加：

- `开篇抓力`
- `层次清晰度`
- `推进有效性`
- `人物立体度`
- `关系张力`
- `阵营分歧`
- `代价感`

这些键是可选增强项，不要求每次 review 全量写入，但一旦写入应保持语义稳定

---

## 六、摘要索引结构 (summaries_index)

```json
{
  "1": "主角获得金手指",
  "2": "进入宗门，开始修炼",
  "3": "突破炼气一层"
}
```

---

## 七、字段命名规范

### 7.1 命名规则

- 统一使用 **camelCase** 驼峰命名
- 禁止使用 snake_case 或 kebab-case
- 布尔字段以 `is_`、`has_` 开头（如 `is_resolved`）

### 7.2 时间戳格式

- 使用 ISO 8601 格式：`2026-03-14T10:30:00Z`
- 存储于 `updated_at` 字段

### 7.3 ID 格式

- 伏笔：`FS-001`、`FS-002`（FS = Foreshadowing）
- 事件：`E-001`、`E-002`
- 钩子：`hook_001`、`hook_002`

---

## 八、版本兼容性

### 8.1 结构变更规则

1. 新增字段：向后兼容，可直接添加
2. 删除字段：需要迁移脚本，保留废弃字段一段时间
3. 重命名字段：需要迁移脚本，同时支持新旧字段名

### 8.2 迁移示例

从旧结构（level 为字符串）迁移到新结构（power 为对象）：

```javascript
// 迁移前
"protagonist": {
  "name": "林轩",
  "level": "炼气一层"
}

// 迁移后
"protagonist": {
  "name": "林轩",
  "power": {
    "realm": "炼气",
    "level": "一层",
    "layer": 1
  }
}
```

---

## 九、引用说明

所有涉及 state.json 结构的模块必须在文档开头引用本文件：

```markdown
> **结构定义**: 参考 [state-schema.md](./state-schema.md)
```

</instructions>
