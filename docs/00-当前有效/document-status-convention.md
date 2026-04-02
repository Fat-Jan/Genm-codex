# 文档状态头约定

## 目的

为项目中的 Markdown / JSON / 规划文档提供一套统一的状态标记语义，减少：

- 同类文档状态写法不一致
- 后续整理时对“该不该迁移”产生误判
- 根目录、`docs/10-进行中/`、`docs/20-研究实验/`、`docs/90-归档/` 的状态表达脱节

## 推荐状态类型

### `active-*`
适用于：
- 当前仍生效的入口、规则、标准、提醒、主线 roadmap

示例：
- `active-mainline-roadmap`
- `active-reminder`
- `active-open-issues`
- `active-closure-ledger`
- `active-trial-standard`

### `in-progress-*`
适用于：
- 正在推进、尚未完成收口的协议、提案、执行材料

示例：
- `in-progress-protocol`
- `in-progress-ontology-proposals`

### `supporting-*`
适用于：
- 辅助执行提示词、支持性材料、依附主文档存在的次级文档

示例：
- `supporting-prompt`

### `research`
适用于：
- 研究候选、方案草案、实验材料

### `archived-*`
适用于：
- 已不再作为当前真源，但仍保留回溯价值的文档

示例：
- `archived-mainline-roadmap`
- `archived-issue-log`
- `archived-plan-log`

## 使用建议

### Markdown 文档
建议写在标题下方：

```md
> Status: `active-mainline-roadmap`
>
> 简短说明该文件为什么还在当前目录、是否仍是当前真源。
```

### JSON 文档
如果文档本身属于项目管理/sidecar性质，可增加顶层字段：

```json
"doc_status": "active-machine-readable-sidecar"
```

## 选择原则

如果一个文件：

1. **仍是当前真源或高可见入口** → 用 `active-*`
2. **仍在推进、未收口** → 用 `in-progress-*`
3. **只是辅助材料** → 用 `supporting-*`
4. **只是研究/候选/实验** → 用 `research`
5. **已完成，仅保留回溯** → 用 `archived-*`

## 与目录分层的关系

- `docs/00-当前有效/`：通常对应 `active-*`
- `docs/10-进行中/`：通常对应 `active-*` / `in-progress-*` / `supporting-*`
- `docs/20-研究实验/`：通常对应 `research`
- `docs/90-归档/`：通常对应 `archived-*`

目录不是状态的唯一依据，但应尽量和状态头保持一致。
