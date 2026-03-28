# `v1.5` `novel-scan` 使用说明与 source matrix

## 目的

这份文档收口 `P1-D`，只为 `novel-scan` 补两层说明：

1. 当前应该怎么理解 `novel-scan` 的使用位置。
2. 当前来源层、可信度层和消费去向如何对齐。

当前不把 `novel-scan` 写成默认主链必经步骤，也不把它写成 canon 写回系统。

---

## 当前定位

`novel-scan` 在 `v1.5` 的定位是：

- 实验能力
- contract 已收口
- consumer 可以读取其 sidecar
- 但它不是默认 workflow 必经步骤

也就是说，`novel-scan` 的价值在于“给 market / packaging / gate review 候选层补证据”，而不是改写本地真值。

---

## 推荐使用场景

### 1. `report-only`

适用于：

- 想先看市场信号
- 想补 packaging 参考
- 想获得低风险候选信息

输出重点：

- `.mighty/market-data.json`
- `confidence`
- findings / gaps / apply_recommendations

### 2. `project-annotate`

适用于：

- 已有项目，需要 project-local 的软建议层
- 需要给 gate / review queue 准备候选

输出重点：

- `.mighty/market-data.json`
- 条件满足时的 `.mighty/market-adjustments.json`
- 可选 `.mighty/research-candidates.json`

但无论如何，都不能把它当 canon 写回入口。

---

## source matrix

| 来源层 | 主要产物 | 可信度作用 | 当前 consumer |
|---|---|---|---|
| source plan | 扫描目标、范围、平台、题材、深度 | 解释本轮扫描为什么这么扫 | `market-data` |
| actual sources | 真实来源列表 | 支撑 `confidence.reason` | `market-data` |
| findings | 热门题材、标签、开篇模式、爽点模式、平台备注 | 形成可消费市场信号 | `market-data` |
| apply recommendations | 轻量建议 | 给 package / query 提供补充参考 | `market-data` |
| project-local adjustments | 项目局部建议层 | 仅在中高可信时可写 | `market-adjustments` |
| research candidates | 候选研究线索 | 进入 gate / review queue，而不写真值 | `research-candidates` |

---

## 可信度分层

### `low`

- 只允许保留 `market-data`
- 不得写 `market-adjustments`
- 更适合做“先看信息，不做项目建议”

### `medium`

- 可以写 `market-adjustments`
- 但 consumer 必须把它当 soft guidance
- 适合 package / query 层读取摘要

### `high`

- 可以形成更强的 project-local guidance
- 但仍不等于 canon
- 适合进入 package / gate 候选层

---

## 当前 consumer 去向

### `novel-package`

当前应把 scan 读取成：

- 包装参考信号
- 市场提示层
- 不能改写 canon

### `novel-query`

当前应把 scan 读取成：

- 当前 scan 结果摘要
- `confidence`
- project-local 建议层摘要

### `setting gate`

当前应把 scan 读取成：

- research candidate 输入
- review queue 候选
- 不直接真值落盘

---

## 非目标

`v1.5` 当前明确不做：

- 把 `novel-scan` 变成默认主链步骤
- 借 `novel-scan` 改写 `shared/profiles/`
- 借 `novel-scan` 绕过 gate / canon / sidecar 边界

所以这份文档的作用是“帮助正确使用和消费”，不是“提升 novel-scan 权限”。
