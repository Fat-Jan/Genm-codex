# Registry / Consumer 维护实战演练 2026-03-31

> 执行模板来源：
> [maintenance-specialized-template-pack-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/maintenance-specialized-template-pack-v1.md) 中的“模板 A：Registry / Consumer 维护执行模板”。
>
> 目的：用已经落地的专项执行模板，真实跑一轮维护检查，验证模板是否足够可执行、输出是否足够可复检。

---

## 一、输入材料

**思考强度：L1 + L2**

本轮按模板实际读取：

- [bucket-overlay-inventory.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/bucket-overlay-inventory.md)
- [novel-scan-usage-and-source-matrix-v1.5.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/novel-scan-usage-and-source-matrix-v1.5.md)
- [scan-result-contract.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/scan-result-contract.md)
- [novel-query](file:///Users/arm/Desktop/vscode/Genm-codex/skills/novel-query/SKILL.md)
- [v1.5-registry-consumer-and-scan-boundary-review-2026-03-31.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/v1.5-registry-consumer-and-scan-boundary-review-2026-03-31.md)

---

## 二、执行摘要

**思考强度：L3**

本轮使用“Registry / Consumer 维护执行模板”做了一次真实专项演练，结论如下：

1. Registry / Consumer 维护模板可直接用于真实执行
2. 本轮未发现新的结构缺口或边界越权问题
3. 发现 1 项低风险文档一致性残留：
   - `v1.5-registry-consumer-and-scan-boundary-review-2026-03-31.md` 中对 `bucket-overlay-inventory.md` 的描述仍停留在“基本一致 / 还可继续整理”
4. 该问题已在本轮直接修正
5. 本轮不需要升级为专项治理或边界裁决

---

## 三、检查结果表

**思考强度：L3 + L4**

| 项目 | 当前状态 | 证据 | 结论 | 风险 | 建议动作 |
|---|---|---|---|---|---|
| bucket 是否仍是单主桶 | 稳定 | `profile-calibration-and-bucket-mapping.md`（前序复检已确认） | 保持单主桶设计 | 低 | 无需动作 |
| bucket overlay 是否仍被错误写成待实现 | 当前已基本现状化 | `bucket-overlay-inventory.md` 当前已明确“无已知缺失项”“参考实现样例”“历史实现记录” | 当前文档语义健康 | 低 | 无需动作 |
| novel-scan 是否仍可消费但不主链化 | 稳定 | `novel-scan-usage-and-source-matrix-v1.5.md`、`scan-result-contract.md` | 边界清楚 | 低 | 无需动作 |
| consumer 是否把 sidecar 当 soft guidance 而非真值 | 稳定 | `novel-query/SKILL.md`、`scan-result-contract.md` | 当前未见越权读取 | 低 | 无需动作 |
| 复检文档是否与最新现状一致 | 存在轻微滞后表述 | `v1.5-registry-consumer-and-scan-boundary-review-2026-03-31.md` 第 2.2 节仍写“基本一致 / 可继续整理” | 属于低风险历史残留 | 低 | 本轮已直接修正 |

---

## 四、已处理项

**思考强度：L2**

本轮已直接处理：

1. 更新 [v1.5-registry-consumer-and-scan-boundary-review-2026-03-31.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/v1.5-registry-consumer-and-scan-boundary-review-2026-03-31.md)
   - 将第 2.2 节的结论从“基本一致”更新为“是”
   - 将“还可以继续做一次轻量去历史化整理”更新为“当前已基本完成现状化整理”
   - 明确该项当前不再构成需继续处理的文档一致性问题

---

## 五、保留项

**思考强度：L4**

本轮未发现需要继续保留的中高风险项。

仍需长期持续复检、但本轮不构成问题的边界包括：

1. `novel-scan` 不得主链化
2. `novel-scan` 产物不得改 canon
3. 新增 consumer 不得把 registry / sidecar 数据误当真值入口

这些属于长期边界守护项，不属于本轮未闭环问题。

---

## 六、是否需要升级

**思考强度：L4**

**结论：不需要。**

原因：

- 本轮仅发现 1 项低风险文档一致性残留
- 已在本轮直接修正
- 未发现结构缺口、边界越权或真实未闭环项

---

## 七、模板实战结果评价

**思考强度：L3**

本次实战说明：

1. “模板 A：Registry / Consumer 维护执行模板”可以直接驱动真实检查
2. 模板要求的输入、步骤、边界和输出结构足够完整
3. 主 agent 可直接复检本轮交付，无需额外重建检查框架

因此，这份专项执行模板不是纸面规则，而是已经通过了一次真实维护任务验证。
