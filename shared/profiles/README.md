# Profile 系统

Genm 的题材配置系统，采用目录化结构管理网文题材规则。

---

## 目录结构

```markdown
profiles/
├── README.md                    # 本文件
├── xuanhuan/                    # 玄幻题材
│   ├── profile.yaml             # 核心配置
│   ├── cultivation-levels.md    # 境界体系
│   ├── power-systems.md         # 力量体系
│   ├── cool-points.md           # 爽点设计
│   └── plot-patterns.md         # 剧情模式
├── urban-superpower/            # 都市异能（待创建）
│   └── ...
└── romance/                     # 言情（待创建）
    └── ...
```

---

## Profile 文件说明

### profile.yaml - 核心配置

每个题材的核心配置文件，包含以下部分：

```yaml
# 基本信息
name: 玄幻                    # 题材名称
display_name: 玄幻修仙         # 显示名称
description: 描述文本           # 题材描述
version: 3.0                   # 版本号

# 子流派定义
sub_genres:
  traditional:
    name: 传统修仙
    description: 经典修仙路线
    core_points: [境界突破, 越级挑战]
    pacing: slow

# 节奏参数
pacing:
  type: 慢热
  tension_ratio: "3:7"
  typical_chapter_length: 5000

# 爽点配置
cool_points:
  density: 0.8                  # 每千字爽点密度
  max_interval: 1500            # 最大间隔
  preferred_types: [...]        # 偏好类型

# Strand 权重
strand_weights:
  quest: 55
  fire: 25
  constellation: 20

# 禁忌清单
taboos:
  - id: TABOO-001
    content: "禁忌内容"
    severity: critical
```

### 扩展文件

| 文件 | 说明 |
|------|------|
| `cultivation-levels.md` | 境界体系设计规则 |
| `power-systems.md` | 力量体系和金手指设计 |
| `cool-points.md` | 爽点类型和设计方法 |
| `plot-patterns.md` | 常用剧情模式 |

---

## 使用方法

### 1. 加载 Profile

通过 genre-adapter Skill 自动加载：

```bash
/novel-genre genre=玄幻
```

或自动检测：

```bash
/novel-genre --detect
```

### 2. 创建新题材

1. 创建目录 `profiles/{题材名}/`
2. 创建 `profile.yaml` 核心配置
3. 根据需要创建扩展 .md 文件

### 3. Profile 合并

当项目包含多个题材时，系统会自动合并配置：

```yaml
# 主题材 + 副题材
主题材: 玄幻
副题材: 系统流

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

## 与旧系统兼容

系统同时支持两种 Profile 格式：

1. **目录化格式**（推荐）：`profiles/xuanhuan/profile.yaml`
2. **单文件格式**：`profiles/修仙.profile.yaml`

加载优先级：
1. 目录化 `profile.yaml`
2. 单文件 `.profile.yaml`
3. 降级到通用配置

---

## 扩展开发

### 添加新题材

```bash
# 创建目录
mkdir profiles/新题材

# 创建配置文件
touch profiles/新题材/profile.yaml
```

### profile.yaml 模板

```yaml
name: 新题材
display_name: 新题材显示名
description: 题材描述

pacing:
  type: 标准
  tension_ratio: "5:5"

cool_points:
  density: 1.0
  max_interval: 1500
  preferred_types:
    - type: 爽点类型
      weight: 1.0

strand_weights:
  quest: 50
  fire: 30
  constellation: 20

taboos:
  - id: TABOO-001
    content: "禁忌内容"
    severity: critical
```

---

## 版本历史

- **v3.0**: 目录化结构，分离配置和规则文档
- **v2.0**: 单文件 .profile.yaml 格式
- **v1.0**: 硬编码流派规则