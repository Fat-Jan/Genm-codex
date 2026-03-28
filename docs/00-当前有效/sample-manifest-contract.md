# Sample Manifest Contract

## 目的

为 `smoke / regression / high_confidence` 样本建立统一 contract，避免样本库继续只靠索引文档和人工记忆维护。

这份 contract 的定位是：

- `codex` 侧的脚本、suite、consumer 能稳定读取
- `mimo` 侧的样本整理、manifest 实体化、文档扩写有统一门槛

---

## 文件位置

- schema：`shared/templates/sample-manifest-v1.schema.json`
- 实体 manifest：留给 `v1.5` 的样本治理任务落地

---

## 最低字段

每个条目至少要有：

- `sample_id`
- `path`
- `sample_type`
- `trust_tier`
- `platform`
- `bucket`
- `status`
- `notes`

可选字段：

- `verification_targets`

---

## 分层规则

### `smoke`

用于 repo-owned 的自动 smoke 样本。

### `regression`

用于锁真实失败模式、历史退化模式或已知 workflow 故障。

### `high_confidence`

用于正向质量基准和高置信项目参考。

---

## 字段约束

### `sample_type`

- `smoke`
- `project`

### `trust_tier`

- `baseline`
- `derived`
- `regression`
- `high_confidence`
- `bucket_sample`

### `status`

- `active`
- `archived`
- `draft`

---

## 准入规则

### smoke 准入

- 路径稳定
- 可由 repo-owned 命令重跑
- 至少有一条 pytest 或 smoke 入口锁定输出骨架

### regression 准入

- 必须绑定明确风险指纹
- 必须能说明“它在防什么退化”
- 至少有一条自动测试验证

### high_confidence 准入

- 必须是结构稳定、质量可信的项目样本
- 必须说明它作为“质量基准”而不是“失败样本”

---

## `mimo` 可做范围

在 `codex` 先定义完这份 contract 后，`mimo` 可以做：

- 样本 inventory 整理
- sample manifest 实体化
- 样本分层说明文档
- 样本 matrix / 索引整理

但在 contract 出来之前，不建议直接批量造 manifest。
