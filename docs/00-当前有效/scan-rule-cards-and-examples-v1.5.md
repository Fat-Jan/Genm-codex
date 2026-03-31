# `v1.5` Scan 规则卡与样例资产

## 目的

这份文档把 `P2-C` 需要的 scan 规则卡与样例资产收成一页当前有效说明，供 `mimo` 侧文档资产和 `codex` 侧 consumer 读取边界对齐。

---

## 规则卡 1：`report-only`

允许：

- 产出 `.mighty/market-data.json`
- 给出 `confidence`
- 给出 findings / gaps / apply_recommendations

不允许：

- 写 `.mighty/market-adjustments.json`
- 写项目 canon
- 绕过 gate

适用：

- 先看市场信号
- 先看候选线索
- 不进入项目建议层

---

## 规则卡 2：`project-annotate`

允许：

- 在中高可信前提下写 `.mighty/market-adjustments.json`
- 可选写 `.mighty/research-candidates.json`
- 给 package / query / gate 提供 project-local 候选层

不允许：

- 覆盖 shared profile
- 覆盖活动 bucket
- 直接改 `设定集/`
- 形成第二真值中心

---

## 规则卡 3：consumer 边界

### `novel-package`

- 读市场信号
- 补包装判断
- 不改写 canon

### `novel-query`

- 返回 scan 摘要
- 返回 `confidence`
- 返回 project-local 建议层摘要

### `setting gate`

- 只把 scan 结果当 candidate 输入
- 不把 scan 当真值写回层

---

## 当前样例资产入口

- contract：`docs/00-当前有效/scan-result-contract.md`
- smoke 结果：
  - `docs/90-归档/阶段/phase-8a-p0-scan-smoke-results.md`
  - `docs/90-归档/阶段/phase-8a-p1-scan-annotate-smoke-results.md`
- 使用说明：`docs/00-当前有效/novel-scan-usage-and-source-matrix-v1.5.md`

这三类入口共同组成当前 `v1.5` 的 scan 规则卡与样例资产集合。
