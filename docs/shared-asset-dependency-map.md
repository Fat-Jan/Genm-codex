# Genm-codex Shared Asset Dependency Map

## 目的

这份文档记录当前各个已迁移 skill 对 `shared` 资产的依赖关系，用于支持：

- selective-sync 前置评估
- shared 缺失排查
- 按域同步设计

## 依赖分层

### A. 强依赖 `profiles`

这些 skill 明确依赖 genre / platform profile：

| Skill | 依赖类型 | 说明 |
|------|----------|------|
| `novel-init` | 强依赖 | 初始化时需要解析 profile 并生成项目骨架 |
| `novel-write` | 强依赖 | 写作时需要 genre/platform 规则 |
| `novel-outline` | 强依赖 | 大纲生成依赖 profile 节奏与结构规则 |
| `novel-review` | 强依赖 | 评审要结合 profile 约束 |
| `novel-genre` | 强依赖 | 直接读取和应用 profile |
| `novel-analyze` | 中强依赖 | 可选使用 profile 作为分析标尺 |
| `novel-precheck` | 中强依赖 | 可选使用 platform profile 做投稿前比对 |

### B. 强依赖 `references`

这些 skill 更依赖通用写作/质量参考：

| Skill | 依赖类型 | 说明 |
|------|----------|------|
| `novel-write` | 强依赖 | 读取高价值 references 做写作约束 |
| `novel-review` | 强依赖 | 评审维度与反 AI 约束来自 references |
| `novel-rewrite` | 强依赖 | 重写时依赖 continuity / quality 参考 |
| `novel-export` | 中强依赖 | 导出规则和格式约束来自 references |
| `novel-outline` | 中强依赖 | 结构化大纲时会参考 shared references |

### C. 强依赖 `templates`

这些 skill 需要 starter files 或模板：

| Skill | 依赖类型 | 说明 |
|------|----------|------|
| `novel-init` | 强依赖 | 初始化骨架和 starter files 直接来自 templates |
| `novel-outline` | 中依赖 | 可复用 outline / chapter-structure 模板 |

### D. 低或无 shared 依赖

这些 skill 主要依赖项目内文件，不以 shared 为核心输入：

| Skill | 依赖类型 | 说明 |
|------|----------|------|
| `novel-query` | 低 | 优先读 state/index，必要时才看项目内文件 |
| `novel-status` | 低 | 主要依赖 state/index |
| `novel-character` | 低 | 主要依赖角色文件与 state |
| `novel-setting` | 低 | 主要依赖设定文件与 state |
| `novel-foreshadowing` | 低 | 主要依赖 state |
| `novel-batch` | 低 | 主要依赖大纲与 state |
| `novel-fix` | 低 | 主要依赖 review 元数据与章节文本 |
| `novel-snapshot` | 低 | 主要依赖 state 与 snapshots |
| `novel-workflow` | 低 | 主要依赖 workflow_state/state |
| `novel-retrieve` | 低 | 主要依赖 state/index/设定文件 |
| `novel-spinoff` | 低 | 主要依赖当前项目 canon 文件 |
| `novel-config` | 无 | 主要依赖本地 config 文件 |
| `novel-test` | 无 | 主要依赖本地 config 文件 |
| `novel-learn` | 无 | 主要依赖本地章节与 state |
| `novel-log` | 无 | 主要依赖 `.mighty/logs/trace.jsonl` |
| `novel-index` | 无 | 主要依赖章节与 state |

## 按域同步影响面

### 仅同步 `profiles`

影响最大：

- `novel-init`
- `novel-write`
- `novel-outline`
- `novel-review`
- `novel-genre`
- `novel-analyze`
- `novel-precheck`

### 仅同步 `references`

影响最大：

- `novel-write`
- `novel-review`
- `novel-rewrite`
- `novel-export`
- `novel-outline`

### 仅同步 `templates`

影响最大：

- `novel-init`
- `novel-outline`

## 当前建议

如果后续要从 full-copy 往 selective-sync 演进，最稳的第一步是：

1. 保持 full-copy 仍可用
2. 先支持按域同步：
   - `profiles`
   - `references`
   - `templates`
3. 不先做按单 skill 同步

## 备注

- 这份映射是基于当前 `SKILL.md` 中显式写出的 shared 路径和实际调用方式整理的
- 后续每次改 shared 路径假设，都应同步更新本文件
