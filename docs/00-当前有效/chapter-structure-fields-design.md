# 章纲结构字段设计

> Status: `active-reference-spec`
>
> 当前已落地入口：
> - state template / schema：`shared/templates/state-v5-template.json`、`shared/templates/state-schema-v5.json`
> - state doc：`shared/references/shared/state-schema.md`
> - consumer 说明：`skills/novel-outline/SKILL.md`、`skills/novel-review/SKILL.md`、`skills/novel-precheck/SKILL.md`
> - 结构审计：`scripts/audit_chapter_structure_repetition.py`、`scripts/audit_precheck_structure_risks.py`

## 目的

把章纲的“结构维度”从散落的规则压成可枚举、可检查、可写回的字段，并说明这些字段当前已经落地到哪些 schema、consumer 和审计入口。

---

## 六个核心字段

### 1. `conflict_type` - 冲突类型

**定义**: 本章核心冲突的来源类型。

**枚举值**:

| 值 | 说明 | 示例 |
|----|------|------|
| `resource` | 资源争夺 | 钱、物、地盘、名额 |
| `identity` | 身份暴露/错位 | 真假千金、卧底暴露 |
| `information` | 信息差/误判 | 我知道你不知道、你以为我知道 |
| `power` | 权力博弈 | 争权、夺位、派系斗争 |
| `relationship` | 关系破裂/修复 | 背叛、和解、试探、切割 |
| `rule` | 规则冲突 | 家法、门规、法律、系统规则 |
| `time` | 时间窗口 | 期限、倒计时、机会稍纵即逝 |
| `moral` | 道德困境 | 两难选择、代价交换 |

**最小用途**:

- `novel-outline`: 锁定本章冲突来源
- `novel-review`: 检查冲突是否有具体来源，不是空喊立场
- `novel-write`: 写作时聚焦冲突来源

---

### 2. `protagonist_arc` - 主角弧线

**定义**: 本章主角的状态变化方向。

**枚举值**:

| 值 | 说明 | 示例 |
|----|------|------|
| `suppress` | 被压制 | 被冤枉、被排挤、被威胁 |
| `test` | 试探/布局 | 试探对手、布置陷阱、收集证据 |
| `exchange` | 交换/博弈 | 讨价还价、利益交换、以退为进 |
| `breakthrough` | 突破/反击 | 反击成功、突破困境、逆转局势 |
| `cost` | 付出代价 | 暴露底牌、失去资源、树敌 |
| `revelation` | 顿悟/发现 | 发现真相、看清局势、理解对手 |
| `choice` | 抉择/放弃 | 选择立场、放弃利益、改变路线 |

**最小用途**:

- `novel-outline`: 锁定本章主角状态变化
- `novel-review`: 检查主角是否有真实变化，不是一直赢或一直惨
- `novel-write`: 写作时聚焦主角状态变化

---

### 3. `opponent_mode` - 对手模式

**定义**: 本章对手的主要行动模式。

**枚举值**:

| 值 | 说明 | 示例 |
|----|------|------|
| `direct` | 直接压制 | 当面威胁、公开打压、正面冲突 |
| `indirect` | 间接施压 | 背后使绊、借刀杀人、制造舆论 |
| `trap` | 设局/陷阱 | 请君入瓮、引蛇出洞、栽赃陷害 |
| `test` | 试探/摸底 | 旁敲侧击、观察反应、测试底线 |
| `alliance` | 联合/借力 | 拉拢盟友、借势压人、联合对抗 |
| `retreat` | 退让/蛰伏 | 暂时退让、积蓄力量、等待时机 |
| `internal` | 内部分歧 | 阵营内斗、路线分裂、利益冲突 |

**最小用途**:

- `novel-outline`: 锁定本章对手行动模式
- `novel-review`: 检查对手是否有真实反制，不是只负责生气和放狠话
- `novel-write`: 写作时聚焦对手行动模式

---

### 4. `gain_type` - 收获类型

**定义**: 本章主角的主要收获类型。

**枚举值**:

| 值 | 说明 | 示例 |
|----|------|------|
| `resource` | 资源获取 | 钱、物、地盘、名额 |
| `information` | 信息获取 | 知道真相、发现秘密、获得情报 |
| `relationship` | 关系变化 | 获得盟友、化解误会、建立信任 |
| `power` | 权力获取 | 升职、获得授权、掌握把柄 |
| `moral` | 道义优势 | 获得同情、占据道德高地、赢得人心 |
| `none` | 无收获 | 本章没有明显收获，只有代价或铺垫 |

**最小用途**:

- `novel-outline`: 锁定本章主角收获
- `novel-review`: 检查推进是否有真实收获，不是白拿或无收获
- `novel-write`: 写作时聚焦主角收获

---

### 5. `cost_visibility` - 代价可见性

**定义**: 本章主角付出代价的可见程度。

**枚举值**:

| 值 | 说明 | 示例 |
|----|------|------|
| `explicit` | 明确代价 | 明确失去资源、暴露底牌、树敌 |
| `implicit` | 隐含代价 | 暗示风险、埋下隐患、留下把柄 |
| `delayed` | 延迟代价 | 本章看不出，但后续会爆发 |
| `none` | 无代价 | 本章没有明显代价 |

**最小用途**:

- `novel-outline`: 锁定本章代价可见性
- `novel-review`: 检查推进是否有代价，不是纯收益
- `novel-write`: 写作时聚焦代价设计

---

### 6. `chapter_end_style` - 章末风格

**定义**: 本章结尾的驱动方式。

**枚举值**:

| 值 | 说明 | 示例 |
|----|------|------|
| `hook` | 悬念钩子 | 留下未解问题、意外发现、突然变故 |
| `residue` | 残账留存 | 留下关系债、信息债、风险债、权力债 |
| `escalation` | 升级加压 | 局势更紧张、风险更高、对手更强 |
| `revelation` | 真相揭示 | 揭示秘密、看清局势、发现真相 |
| `choice` | 抉择前置 | 面临选择、必须决定、没有退路 |
| `payoff` | 兑现收账 | 完成反击、收获结果、结清旧账 |
| `closure` | 阶段收口 | 完成阶段目标、暂时平静、准备下一阶段 |

**最小用途**:

- `novel-outline`: 锁定本章结尾驱动方式
- `novel-review`: 检查章末是否有驱动，不是"无事发生"
- `novel-write`: 写作时聚焦章末设计

---

## Consumer 使用说明

### novel-outline

- **写入时机**: 创建章纲时
- **字段来源**: 作者手动填写或根据章纲内容自动推断
- **使用方式**: 
  - 锁定本章的结构维度，作为写作约束
  - 检查章纲是否覆盖了关键结构维度
  - 输出章纲时附带结构字段

### novel-write

- **读取时机**: 开始写作前
- **使用方式**:
  - 根据 `conflict_type` 聚焦冲突来源
  - 根据 `protagonist_arc` 设计主角状态变化
  - 根据 `opponent_mode` 设计对手行动模式
  - 根据 `gain_type` 设计主角收获
  - 根据 `cost_visibility` 设计代价可见性
  - 根据 `chapter_end_style` 设计章末驱动

### novel-review

- **读取时机**: 审查时
- **使用方式**:
  - 检查实际内容是否符合声明的结构字段
  - 输出 `chapter_structure_summary`，包含 `declared`、`actual` 和 `drift`
  - 如果 `drift` 不为空，说明实际内容与声明不符，需要修正

### novel-precheck

- **读取时机**: 投稿前检查
- **使用方式**:
  - 检查连续章节的结构重复性
  - 检查 `conflict_type`、`protagonist_arc`、`chapter_end_style` 是否连续重复
  - 输出结构重复警告

---

## 字段组合规则

### 合理组合示例

| conflict_type | protagonist_arc | opponent_mode | gain_type | cost_visibility | chapter_end_style |
|---------------|-----------------|---------------|-----------|-----------------|-------------------|
| resource | suppress | direct | none | explicit | hook |
| identity | test | indirect | information | implicit | residue |
| information | exchange | trap | relationship | delayed | escalation |
| power | breakthrough | alliance | power | none | payoff |

### 不合理组合示例

| conflict_type | protagonist_arc | opponent_mode | gain_type | cost_visibility | chapter_end_style |
|---------------|-----------------|---------------|-----------|-----------------|-------------------|
| resource | breakthrough | none | resource | none | payoff |
| - 问题: 冲突太顺，没有对手，没有代价 | | | | | |
| identity | suppress | direct | none | none | closure |
| - 问题: 一直惨，没有收获，没有驱动 | | | | | |

---

## 与现有系统的关系

### 与 state schema 的关系

当前已在 `state-v5-template.json`、`state-schema-v5.json` 与 `state-schema.md` 的 `chapter_meta.chapter_structure` 中落地：

```json
{
  "chapter_meta": {
    "chapter_structure": {
      "conflict_type": "resource",
      "protagonist_arc": "suppress",
      "opponent_mode": "direct",
      "gain_type": "none",
      "cost_visibility": "explicit",
      "chapter_end_style": "hook"
    }
  }
}
```

### 与框架的关系

- **opening-and-plot-framework**: 提供 `conflict_type` 和 `chapter_end_style` 的理论基础
- **anti-flattening-framework**: 提供 `opponent_mode` 和 `cost_visibility` 的理论基础
- **writing-core-framework**: 提供 `protagonist_arc` 和 `gain_type` 的理论基础

### 与 review / precheck 的关系

当前 consumer 已按以下思路读取和复核这些字段：

- `novel-review`
  - 对比 declared `chapter_structure` 与实际内容交付
- `novel-precheck`
  - 检查连续章节结构重复、零代价突破和无低谷 runs
- `audit_chapter_structure_repetition.py` / `audit_precheck_structure_risks.py`
  - 对 `chapter_meta.chapter_structure` 做轻量结构审计

一个典型的 review 摘要形态可以类似：

```json
{
  "chapter_structure_summary": {
    "declared": {
      "conflict_type": "resource",
      "protagonist_arc": "suppress",
      "opponent_mode": "direct",
      "gain_type": "none",
      "cost_visibility": "explicit",
      "chapter_end_style": "hook"
    },
    "actual": {
      "conflict_type": "resource",
      "protagonist_arc": "suppress",
      "opponent_mode": "none",
      "gain_type": "none",
      "cost_visibility": "none",
      "chapter_end_style": "closure"
    },
    "drift": ["opponent_mode", "cost_visibility", "chapter_end_style"]
  }
}
```

---

## 完成标记

- [x] 有独立设计稿（本文件）
- [x] 明确字段定义、枚举值和最小用途（本文件）
- [x] 与 state schema 对接（`shared/templates/state-v5-template.json`、`shared/templates/state-schema-v5.json`、`tests/test_state_contracts.py`）
- [x] 与 review / precheck 读取链对接（`skills/novel-review/SKILL.md`、`skills/novel-precheck/SKILL.md`、`skills/novel-outline/SKILL.md`）
- [x] 有测试样本能验证字段有效性（`tests/test_state_contracts.py`、`tests/test_chapter_structure_repetition.py`、`tests/test_precheck_structure_risks.py`）
