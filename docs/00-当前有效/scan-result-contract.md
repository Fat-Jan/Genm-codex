# Scan Result Contract

## 目的

把 `novel-scan` 当前已经在产出的三类结果，收成稳定 contract：

- `.mighty/market-data.json`
- `.mighty/market-adjustments.json`
- `.mighty/research-candidates.json`

这份 contract 先解决两件事：

1. 明确 `report-only` / `project-annotate` 的模式边界
2. 明确 consumer 能读什么、不能覆盖什么

---

## 三类结果文件

### 1. `.mighty/market-data.json`

这是 scan 的主结果文件。

无论是 `report-only` 还是 `project-annotate`，都应先产出它。

它负责记录：

- 本轮扫描的目标
- source plan
- 实际来源
- findings
- `confidence`
- gaps
- `apply_recommendations`

### 2. `.mighty/market-adjustments.json`

这是 project-local 的低风险建议 sidecar。

它只在以下条件同时满足时允许写入：

- `mode = project-annotate`
- `report_kind = real_report`
- `confidence.overall in {medium, high}`

它不能成为：

- canon
- shared profile 重写入口
- 直接覆盖项目当前 bucket 的强制来源

### 3. `.mighty/research-candidates.json`

这是给 `setting gate` / review queue 的候选输入。

它只保存 candidate，不保存 canon。

它的定位是：

- 供 `setting gate` 使用
- 供 review queue 使用

它不能成为：

- 直接写 `设定集/` 的权威
- 绕过 gate 的研究事实层

---

## 模式边界

### `report-only`

只允许：

- 产出 `.mighty/market-data.json`
- 给出 `confidence`
- 给出 findings / gaps / 建议

不允许：

- 写 `.mighty/market-adjustments.json`
- 写项目 state 摘要
- 改 canon

### `project-annotate`

允许：

- 在中高可信证据下写 `.mighty/market-adjustments.json`
- 写 project-local 的轻量 state 摘要
- 可选写 `.mighty/research-candidates.json`

不允许：

- 覆盖 shared profile
- 覆盖活动 bucket
- 直接改 `设定集/`
- 不能覆盖 canon

---

## `confidence` 语义

当前 contract 只要求 3 档：

- `low`
- `medium`
- `high`

最低约束：

- `low`
  - 不得写 `market-adjustments`
  - 只允许保留 `market-data`
- `medium`
  - 可以写 `market-adjustments`
  - 但 consumer 必须仍把它当 soft guidance
- `high`
  - 可以作为更强的 project-local guidance
  - 但仍不等于 canon

---

## Consumer 读取边界

### `novel-package`

可读：

- `.mighty/market-adjustments.json`
- `.mighty/market-data.json`

用途：

- 补包装层的市场信号
- 不改写 canon

### `novel-query`

可读：

- `.mighty/market-data.json`
- `.mighty/market-adjustments.json`

用途：

- 返回当前 scan 结果
- 返回 `confidence`
- 返回 project-local 的建议层摘要

### `setting gate`

可读：

- `.mighty/research-candidates.json`

用途：

- 进入 gate candidate 流程
- 不直接写真值

---

## 最低验证门

这组 contract 至少要过：

- `tests/test_scan_result_contract.py`
- `tests/test_novel_scan.py`
- `bash scripts/validate-migration.sh`

---

## 非目标

当前这份 contract 不解决：

- `novel-scan` 进入默认工作流
- CI 自动联网扫描
- 直接重写 `shared/profiles/`
- 把 scan 当成 canon
