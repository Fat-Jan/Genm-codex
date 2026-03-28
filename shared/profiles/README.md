# Profile 系统

Genm-codex 的题材配置系统，采用目录化结构管理网文题材规则。

---

## 当前状态

- **profile 总数**: 54 个
- **当前分层**: core profile + platform overlay + bucket overlay + reference files
- **当前默认范围**: opening-and-plot-framework、writing-core-framework、anti-flattening-framework、番茄起盘协议栈、Gate Triage

---

## 目录结构

```markdown
shared/profiles/
├── README.md                    # 本文件
├── palace-intrigue/             # 宫斗宅斗
│   ├── profile.yaml             # 核心配置
│   └── reference-notes.md       # 参考扩展
├── xuanhuan/                    # 玄幻
│   ├── profile.yaml
│   └── ...
├── urban-brainhole/             # 都市脑洞
│   ├── profile.yaml
│   └── ...
└── ... (共 54 个 profile)
```

---

## Contract 分层

从 `v1.1` 的 `Profile Contract` 开始，profile 应按下面四层理解：

### 1. Core Profile

- **路径**: `profiles/<slug>/profile.yaml`
- **内容**: 只放题材基础配置
  - `name`
  - `display_name`
  - `description`
  - `version`
  - `template`
  - `pacing`
  - `cool_points`
  - `strand_weights`
  - `constraints`
  - `reader_expectations`
  - `taboos`
  - `progression_constraints`
  - `sub_genres`

### 2. Platform Overlay

- **路径**: `profiles/<slug>/profile-<platform>.yaml`
- **内容**: 只放平台差异
- **当前状态**: 大部分 profile 未实现

### 3. Bucket Overlay

- **路径**: `profiles/<slug>/bucket-<bucket>.yaml`
- **内容**: 只放内容桶差异
- **当前状态**: 大部分 profile 未实现

### 4. Reference Files

- **路径**: `profiles/<slug>/*.md`
- **内容**: 放长文本方法论、样例、扩展说明
- **示例**: `reference-notes.md`

---

## 补充约定

- `scripts/profile_contract.py --describe-layers` 会按这套规则返回 layer descriptor
- `state.genre_profile` 只保留轻量投影，不保留整份 raw profile
- 历史 profile 中混入的长文本区块（如 `dialogue_templates`、`scene_description`）目前视为 **legacy embedded reference**
  - 可以继续存在
  - 但不再视为 core contract 的 authoritative 部分
  - 后续应逐步迁到 reference files

---

## 当前缺口

根据架构审查，当前 profile 系统存在以下缺口：

1. **bucket 分配系统已进入主链**: `build_content_positioning.py` 与 `profile_contract.py` 已能消费 bucket overlay，但下游 consumer 仍未全面使用 bucket 级差异
2. **bucket overlay 已补齐当前所有声明了 `fanqie primary_bucket` 的 profile**: 后续新增 profile 时仍需保持同步
3. **桶名 slug 映射虽已成文，但尚未做成统一 registry**: 宫斗宅斗 vs palace-intrigue vs gongdou_zhai
4. **大部分 profile 没有 platform_positioning**: 54 个 profile 中仍有大量 profile 未补平台定位

相关文档：

- [Bucket / Profile 命名映射规范](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/bucket-profile-slug-mapping.md) - 解决命名漂移
- [Bucket Overlay 缺口清单](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/bucket-overlay-inventory.md) - P0-P2 优先级
- [Profile Expansion Contract](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/profile-expansion-contract.md) - 约束后续扩面工作
- `shared/templates/profile-bucket-registry-v1.json` - 当前 machine-readable bucket/profile registry

---

## 与其他系统的关系

### 与框架的关系

- **opening-and-plot-framework**: 提供开篇方法和剧情层次模型
- **writing-core-framework**: 提供写作基本功和内容标准
- **anti-flattening-framework**: 提供反脸谱化规则
- **profile**: 提供题材特定规则，挂在框架之上

### 与 bucket 的关系

- **bucket**: 内容桶，如"宫斗宅斗"、"都市脑洞"
- **profile**: 题材配置，如"palace-intrigue"、"urban-brainhole"
- **当前状态**: bucket 和 profile 的映射关系不明确，需要建立规范 slug 映射

### 与 platform 的关系

- **platform**: 平台，如"番茄"、"起点"
- **当前状态**: 大部分 profile 没有 platform overlay，平台差异未分离

---

## 使用方法

### 1. 加载 Profile

通过 novel-genre Skill 自动加载：

```bash
/novel-genre genre=宫斗宅斗
```

或自动检测：

```bash
/novel-genre --detect
```

### 2. 创建新 Profile

1. 创建目录 `shared/profiles/<slug>/`
2. 创建 `profile.yaml` 核心配置
3. 根据需要创建 `reference-notes.md` 等参考文件

### 3. Profile 合并

当项目包含多个题材时，系统会自动合并配置：

```yaml
# 主题材 + 副题材
主题材: 宫斗宅斗
副题材: 权谋

合并规则:
  - 基础配置取主题材
  - 特殊规则叠加
  - 冲突时取更严格值
```

---

## 配置项详解

### 节奏参数

| 参数 | 说明 | 建议值 |
|------|------|--------|
| `type` | 节奏类型 | 慢热/标准/快 |
| `tension_ratio` | 张弛比例 | "3:7" ~ "5:5" |
| `typical_chapter_length` | 典型章长 | 4000-6000 |

### 爽点配置

| 参数 | 说明 | 平台差异 |
|------|------|----------|
| `density` | 每千字爽点数 | 起点0.8, 七猫1.5 |
| `max_interval` | 最大间隔字数 | 1200-1500 |

### Strand 权重

| Strand | 说明 | 典型值 |
|--------|------|--------|
| `quest` | 任务推进 | 40-60% |
| `fire` | 冲突爆发 | 20-35% |
| `constellation` | 世界观铺垫 | 15-25% |

### 禁忌严重程度

| 级别 | 说明 | 处理方式 |
|------|------|----------|
| `critical` | 严重违规 | 阻止发布 |
| `warning` | 警告级别 | 提示修改 |
| `info` | 提示信息 | 记录日志 |

---

## 扩展开发

### 添加新 Profile

```bash
# 创建目录
mkdir shared/profiles/<slug>

# 创建配置文件
touch shared/profiles/<slug>/profile.yaml

# 可选：创建参考文件
touch shared/profiles/<slug>/reference-notes.md
```

### profile.yaml 模板

```yaml
name: <题材名>
display_name: <题材显示名>
description: <题材描述>
version: "3.0"
template: templates/genres/<题材名>.md

progression_constraints:
  resistance_rule: "关键推进必须遭遇真实阻力，不能自动到账。"
  cost_rule: "重要收益应伴随可见代价、暴露或资源损耗。"
  partial_payoff_rule: "阶段胜利以局部收益为主，不宜一次打穿主线矛盾。"
  residual_risk_rule: "每次推进后都应保留残留风险，避免章节收口过满。"

sub_genres:
  <子流派名>:
    name: "<子流派显示名>"
    description: "<子流派描述>"
    core_points: [<核心爽点>]
    pacing: <节奏>
    examples: [<示例作品>]

pacing:
  type: <节奏类型>
  tension_ratio: "<张弛比例>"
  typical_chapter_length: <典型章长>

cool_points:
  density: <爽点密度>
  max_interval: <最大间隔>
  preferred_types:
    - type: <爽点类型>
      weight: <权重>
      description: "<描述>"
      triggers: [<触发词>]
      note: "<注意事项>"

strand_weights:
  quest: <任务推进权重>
  fire: <冲突爆发权重>
  constellation: <世界观铺垫权重>

taboos:
  - id: <禁忌ID>
    content: "<禁忌内容>"
    severity: <严重程度>
```

---

## 版本历史

- **v3.0**: 目录化结构，分离配置和规则文档（当前版本）
- **v2.0**: 单文件 .profile.yaml 格式
- **v1.0**: 硬编码流派规则
