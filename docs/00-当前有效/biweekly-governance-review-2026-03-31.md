# 双周治理异常复核 2026-03-31

> 执行时间：2026-03-31
> 复核类型：常态治理 / 双周异常复核
> 基线文档：
>
> - `docs/00-当前有效/steady-governance-rhythm-v1.md`
> - `docs/00-当前有效/governance-execution-review-plan.md`
> - `docs/00-当前有效/weekly-governance-snapshot-2026-03-31.md`
> - `docs/00-当前有效/shared-asset-governance-phase-report-v1.md`

---

## 一、执行摘要

本轮双周异常复核已完成，验证通过，**未发现新增高风险异常**。

本轮结论：

1. **shared 三域状态整体稳定**
   - profiles：protected 173 / local-only 110 / drift 56
   - references：protected 10 / local-only 7 / drift 5
   - templates：protected 37 / local-only 23 / drift 31 / source-only 6
2. **上一轮 weekly snapshot 中的 2 个 references 残留 orphan 链接已被修复**
3. **progress.md 中仍保留已归档 orphan 路径记录**，但这属于历史进展记录残留，不构成新的治理异常
4. **未发现新的 orphan 候选、declared-only 候选或保护名单异常膨胀**

综合判断：当前项目处于**稳定的常态治理状态**，无需重新发起专项治理。

---

## 二、复核范围

本轮重点复核了以下范围：

- `shared/references/**`
- `shared/templates/**`
- `shared/validators/**`
- `docs/00-当前有效/**`
- `progress.md`
- `shared/sync-governance.json`

重点复核对象包括：

1. 上一轮 weekly snapshot 中记录的 3 处低风险文档残留引用
2. `chapter-index-schema.md` / `serial-generation-mode.md` 的后续状态
3. 已归档 orphan 文件是否仍有主路径残留引用
4. sync report 中 shared 三域指标是否出现异常变化

---

## 三、验证结果

### 3.1 validate-migration

命令：

```bash
bash scripts/validate-migration.sh
```

结果：

- ✅ `Migration validation passed`

### 3.2 sync report

命令：

```bash
bash scripts/sync-shared-from-genm.sh --report
```

结果摘要：

| 域 | protected | local-only | drift | source-only | 结论 |
| --- | ---: | ---: | ---: | ---: | --- |
| profiles | 173 | 110 | 56 | 0 | 稳定 |
| references | 10 | 7 | 5 | 0 | 稳定 |
| templates | 37 | 23 | 31 | 6 | 稳定 |

说明：

- profiles / references / templates 的 protected 数量均与当前基线一致
- templates 的 `source-only 6` 已完成路径级确认，对应 6 个上游存在、目标侧缺失的模板路径
- 未发现 protected 数量异常波动或 drift 异常爆发

---

## 四、异常复核结果表

| path / 范围 | 问题类型 | 证据 | 风险等级 | 建议动作 | 是否已处理 |
| --- | --- | --- | --- | --- | --- |
| `shared/references/chapter-index-schema.md` | 上轮残留链接复核 | 当前已不再命中 `post-write-validator.md` | 低 | 记为已闭环 | ✅ 已处理 |
| `shared/references/serial-generation-mode.md` | 上轮残留链接复核 | 当前已不再命中 `commands/novel-review.md` | 低 | 记为已闭环 | ✅ 已处理 |
| `progress.md:L2883-L2884` | 历史记录残留 | 仍保留已归档 orphan 路径，仅作历史进度记录 | 低 | biweekly 复核定性为历史记录残留；当前已在 `progress.md` 中改写为 legacy 归档路径说明 | ✅ 已处理 |
| `templates source-only paths = 6` | 报表项路径级确认 | 当前已确认对应 6 个上游存在、目标侧缺失的模板路径 | 低 | `sync-shared-from-genm.sh --report-json --domain templates` 输出的 `source_only_paths` 明细；记为已确认报表来源，暂不升级为专项 | ✅ 已确认 |
| `weekly-governance-snapshot-2026-03-31.md` | 历史快照口径收紧 | 文档当前已明确为“历史周快照记录”，并将后续闭环状态写明 | 低 | 保留历史快照事实，同时避免继续误读为当前异常 | ✅ 已处理 |

---

## 五、本轮已直接确认 / 闭环事项

本轮确认以下事项已完成闭环：

1. `chapter-index-schema.md` 中对 `post-write-validator.md` 的残留链接已修复
2. `serial-generation-mode.md` 中对 `commands/novel-review.md` 的残留链接已修复
3. references 域未出现新的 orphan 链接扩散
4. sync-governance.json 未出现异常增减或结构异常

---

## 六、待主 agent 决策项

本轮**无新增必须升级给主 agent 的中高风险事项**。

当前已无仍未闭环的低风险观察项。

`progress.md` 的 orphan 历史路径已改写为 legacy 归档说明；templates `source-only 6` 已完成路径级确认；`weekly-governance-snapshot-2026-03-31.md` 也已明确为历史快照记录，因此这三项均不再属于未解释观察项。

---

## 七、结论

### 7.1 本轮是否发现新增高风险异常

**未发现新增高风险异常。**

### 7.2 当前治理状态是否稳定

**稳定。**

当前项目已从专项治理切换到常态治理，shared 三域状态保持一致，验证链正常，最近一轮 weekly snapshot 中的核心低风险问题与历史快照口径均已闭环。

### 7.3 是否需要启动专项治理

**不需要。**

建议继续按 `steady-governance-rhythm-v1.md` 执行：

- 每周：快照
