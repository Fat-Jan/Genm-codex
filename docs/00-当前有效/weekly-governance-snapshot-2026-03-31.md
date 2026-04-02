# Weekly Governance Snapshot 2026-03-31

> 快照日期：2026-03-31
> 执行者：agent（常态治理 weekly snapshot）
> 基线版本：steady-governance-rhythm-v1.md
>
> 当前定位：历史周快照记录。本文保留“当时发现了什么”与“后续如何闭环/确认”的链路，不再表示当前仍存在未解释异常。

---

## 1. 执行摘要

| 项目 | 结果 |
|---|---|
| 本轮是否完成快照 | ✅ 是 |
| 验证是否通过 | ✅ validate-migration.sh 通过 |
| 总体状态是否稳定 | ✅ 稳定，无新增高风险异常 |

---

## 2. 指标快照表

| 域 | protected | local-only | drift | source-only | 结论 |
|---|---:|---:|---:|---:|---|
| profiles | 173 | 110 | 56 | 0 | 稳定，与基线一致 |
| references | 10 | 7 | 5 | 0 | 稳定，与基线一致 |
| templates | 37 | 23 | 31 | 6 | 稳定，与基线一致 |

**基线对比说明**：
- templates drift (31) 与当前基线一致，主要来自本地化编辑的 markdown / template 文件
- source-only (6) 来自 templates 域；当时 weekly snapshot 未做逐路径拆解，后续已完成路径级确认，当前仅保留为历史快照说明
- 无新增 protected 异常膨胀
- 无新增 source-only 异常爆发

---

## 3. validate-migration.sh 结果

```
Migration validation passed
```

✅ 通过，无阻断性问题。

---

## 4. sync-shared-from-genm.sh --report 结果摘要

### profiles
- source files: 63 / target files: 173
- protected local paths: 173
- local-only paths: 110
- same-path drift paths: 56
- source-only paths: 0

### references
- source files: 22 / target files: 29
- protected local paths: 10
- local-only paths: 7
- same-path drift paths: 5
- source-only paths: 0

### templates
- source files: 48 / target files: 65
- protected local paths: 37
- local-only paths: 23
- same-path drift paths: 31
- source-only paths: 6

---

## 5. 本轮记录的异常候选（历史快照）

### 5.1 当时发现的低风险文档残留（后续已闭环 / 已确认）

| path / 范围 | 问题类型 | 证据 | 风险等级 | 当时建议动作 | 后续状态 |
|---|---|---|---|---|---|
| `shared/references/chapter-index-schema.md:L1070` → `post-write-validator.md` | docs 残留引用已归档 orphan 文件 | `chapter-index-schema.md` 当时仍有 `[post-write-validator.md](../validators/post-write-validator.md)` 链接 | 低 | 确认 validator 概念已迁移后，修链或保留 | 后续已修复并在双周复核中闭环 |
| `shared/references/serial-generation-mode.md:L385` → `novel-review.md` | docs 残留引用已归档 orphan 文件 | `serial-generation-mode.md` 当时仍有 `[质量检查流程](./commands/novel-review.md)` 链接 | 低 | 确认 review 已迁移至 SKILL.md 后，修链或保留 | 后续已修复并在双周复核中闭环 |
| `progress.md:L2883-L2884` → orphan 清单项 | 旧 progress 记录残留 | progress.md 当时记录了已归档的 orphan 文件路径 | 低 | 确认归档完成，可后续清理 progress 而非治理问题 | 后续已改写为 legacy 归档路径说明 |

### 5.2 templates source-only 报表项（6项，后续已完成路径级确认）

| 范围 | 当时说明 | 风险等级 | 当时建议动作 | 后续状态 |
|---|---|---|---|---|
| templates source-only paths = 6 | sync report 当时显示存在 6 个 source-only paths，weekly snapshot 阶段尚未逐路径拆解 | 低 | 后续如需专项核实，再做路径级确认，当前仅记录为报表信号 | 后续已通过 `sync-shared-from-genm.sh --report-json --domain templates` 确认 6 条具体路径 |

---

## 6. 本轮无异常项

- profiles 域：未发现新增异常，保护名单稳定
- references 域：未发现新增异常，10个保护项整体健康
- templates 域：protected 保持37项，G5 14项定位已确认为"非保护手工参考模板库"，本轮无变化
- 无新增 orphan 候选（基于本轮轻量扫描）
- 无新增 declared-only 候选（consumer-read-manifest 已在基线中处理）
- 无保护项异常膨胀

---

## 7. 后续复检结论

| 事项 | 问题描述 | 风险 | 建议 |
|---|---|---|---|
| 无新增待主 agent 专项决策项 | 本轮记录的低风险项后续已由双周复核、月度收口与文档口径收紧完成闭环或确认 | 低 | 保留本 weekly snapshot 作为历史快照，无需额外专项动作 |

---

## 8. 本轮执行的动作

本轮为 weekly snapshot，仅执行以下轻量动作：

1. ✅ 读取基线文档（steady-governance-rhythm-v1.md、governance-execution-review-plan.md 等）
2. ✅ 运行 validate-migration.sh（通过）
3. ✅ 运行 sync-shared-from-genm.sh --report（正常输出）
4. ✅ 记录三域指标快照
5. ✅ 初步筛查异常候选
6. ✅ 输出本 snapshot 文档

**本轮未执行任何治理动作。** 当时记录的异常候选已在后续双周复核、月度收口和文档口径收紧中完成闭环或确认。

---

## 9. 结论

**本轮未发现新增高风险异常。**

三域保护名单与基线一致，验证通过，sync report 可解释。本 snapshot 中记录的低风险项已在后续双周复核与月度收口中完成闭环或路径级确认，因此当前保留本文的主要价值是作为“当时发现了什么”的历史快照。

---

> 快照完成时间：2026-03-31
> 下次周快照建议时间：2026-04-07
