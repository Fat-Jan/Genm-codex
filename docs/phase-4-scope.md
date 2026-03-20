# Genm-codex 第四阶段范围设计

## 设计结论

第四阶段不再继续无差别扩命令，而是聚焦剩余命令里**仍然有独立价值、且适合 Codex 原生工作流**的那一批。

第四阶段拆成两个子阶段：

- **Phase 4A：编辑控制与回溯层**
- **Phase 4B：写作辅助与专项创作层**

同时明确三类不进入本阶段的命令：

- **暂缓迁移**：外部依赖重、需要单独环境契约
- **低优先级**：更像引导命令，不是核心 skill
- **不建议单独迁移**：已被现有 skill 覆盖或属于历史文档

## 剩余候选盘点

当前 `Genm` 中仍未进入 `Genm-codex` 的主要命令：

- `novel-config`
- `novel-fix`
- `novel-help`
- `novel-learn`
- `novel-precheck`
- `novel-retrieve`
- `novel-scan`
- `novel-snapshot`
- `novel-spinoff`
- `novel-test`
- `novel-tutorial`
- `novel-workflow`

另有一批已定性为历史/参考文档：

- `novel-content-generate-polish`
- `novel-inheritance`
- `novel-outline-intelligent`
- `novel-stats`

## 分类判断

### 一、优先迁移候选

这些命令仍然有明确独立价值，且与当前已迁移体系能自然衔接：

| 命令 | 价值判断 | 依赖风险 | 建议 |
|------|----------|----------|------|
| `novel-fix` | 高 | 中 | 纳入 Phase 4A |
| `novel-snapshot` | 高 | 低 | 纳入 Phase 4A |
| `novel-precheck` | 高 | 中 | 纳入 Phase 4A |
| `novel-workflow` | 中高 | 中高 | 纳入 Phase 4A |
| `novel-retrieve` | 中高 | 中 | 纳入 Phase 4B |
| `novel-spinoff` | 中高 | 中 | 纳入 Phase 4B |

### 二、暂缓迁移

这些命令不是没价值，而是当前迁过去会把环境复杂度重新拉高：

| 命令 | 暂缓原因 |
|------|----------|
| `novel-learn` | 含外部作品学习与自动学习触发设计，需要先定义稳定的外部内容输入契约 |
| `novel-scan` | 强依赖联网扫描和外部数据采集能力，不适合直接塞进当前纯本地技能层 |

### 三、低优先级 / 可不独立迁移

| 命令 | 判断 |
|------|------|
| `novel-config` | 更像环境/提供商引导命令，和 Codex-native 核心写作 skill 的关系较弱 |
| `novel-test` | 也是引导式连接测试命令，迁移价值低于核心创作/管理能力 |
| `novel-tutorial` | 已被 `README + skill-usage + 阶段 smoke 文档` 部分覆盖 |
| `novel-help` | Codex-native 体系中可以继续由仓库文档承担，不需要单独变成 skill |

### 四、不建议迁移

| 命令/文档 | 原因 |
|----------|------|
| `novel-content-generate-polish` | 已定性为历史方案文档 |
| `novel-inheritance` | 平台继承分析参考文档，未闭环 |
| `novel-outline-intelligent` | 历史方案文档，平台口径过时 |
| `novel-stats` | 历史草案，且大量内容可由 `status/index/query` 组合覆盖 |

## Phase 4A：编辑控制与回溯层

### 目标

补齐“写完之后如何修、如何回看、如何投稿前把关、如何跟踪工作流”的控制能力。

### 范围

#### P0

- `novel-fix`
- `novel-snapshot`

#### P1

- `novel-precheck`

#### P2

- `novel-workflow`

### 排序理由

- `fix` 与 `review / polish / rewrite` 直接衔接，价值最高
- `snapshot` 与 `rewrite / resume / index` 都能形成直接补强
- `precheck` 很实用，但属于输出前守门，不如 `fix/snapshot` 基础
- `workflow` 有价值，但依赖恢复契约和任务状态结构，应放在 4A 尾部

### 4A 迁移约束

- `novel-fix` 第一版优先做基于 review 结果的定向修复，不做复杂交互式修补器
- `novel-snapshot` 第一版围绕现有 `chapter_snapshots` 和 `.mighty/snapshots/` 工作，不另起新快照体系
- `novel-precheck` 第一版只做只读预检，不做平台上传自动化
- `novel-workflow` 第一版只做状态查看/更新/恢复协同，不做完整任务编排器

## Phase 4B：写作辅助与专项创作层

### 目标

补齐“写作时快速引用设定”和“衍生创作”这两条仍有独立价值的使用面。

### 范围

#### P0

- `novel-retrieve`

#### P1

- `novel-spinoff`

### 排序理由

- `retrieve` 和当前 `query/character/setting/index` 有重叠，但更偏“写作瞬时引用”，仍有独立场景
- `spinoff` 很有价值，但建立在现有主线项目能力更稳定之后再迁更合适

### 4B 迁移约束

- `novel-retrieve` 第一版不要重复造一个大查询系统，要站在现有：
  - `novel-query`
  - `novel-character`
  - `novel-setting`
  - `novel-index`
  之上做“写作辅助视图”
- `novel-spinoff` 第一版不追求完整多书宇宙系统，优先支持单项目内的轻量番外

## 推荐实施顺序

1. `novel-fix`
2. `novel-snapshot`
3. `novel-precheck`
4. `novel-workflow`
5. `novel-retrieve`
6. `novel-spinoff`

## 版本边界建议

- **`v0.5.0`**：以 `Phase 4A` 为主要封版目标
- **`v0.6.0`**：以 `Phase 4B` 为主要封版目标

## 本阶段明确不做

- 不把 `novel-learn` 与 `novel-scan` 硬塞进第四阶段
- 不迁移纯引导型 `config/test/tutorial/help` 作为高优先级 skill
- 不复活历史方案文档型命令

## 当前推荐下一步

第四阶段正式实施时，先从 **Phase 4A / P0** 开始：

1. `novel-fix`
2. `novel-snapshot`

原因：

- 和当前已有链路耦合最强
- 用户价值高
- 验证路径清楚
- 风险显著低于 `workflow`、`scan`、`learn`
