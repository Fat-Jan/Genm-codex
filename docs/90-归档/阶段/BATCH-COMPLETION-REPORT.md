# 跨平台实体证据收集状态汇报（事故修复后）

**更新时间**: 2026-03-30  
**文档版本**: v1.5（post-remediation）  
**事实源**:
- `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`
- `docs/10-进行中/cross-platform-entity-evidence-standard-v1.5.md`
- `progress.md`
- `task_plan.md`

---

## 说明

本文件已替换旧的污染口径。

旧版本曾错误声称：
- 全部 45/45 profiles 已完成
- 0 partial
- 多个 batch 使用批量复用 URL 仍被记为 complete

上述口径已作废，不再作为任何后续 agent 或接手者的事实依据。

---

## 当前真实状态

| 类别 | 数量 | 说明 |
|------|------|------|
| `complete` | **50** | 标准 profile 已完成跨平台证据收集 |
| `partial` | **1** | `zhihu-short` 为专项例外 |
| 例外规则 | **1** | `zhihu-short` 不适用默认三平台对齐门槛 |

---

## 完成概览

### Batch 0（6/6 complete）
- `ceo-romance`
- `sweet-youth`
- `xiuxian`
- `ancient-romance`
- `farming`
- `romance`

### Batch 1（6/6 complete）
- `palace-intrigue`
- `historical-brainhole`
- `realistic`
- `workplace-romance`
- `urban-daily`
- `urban-brainhole`

### Batch 2（6/6 complete）
- `sweet-romance`
- `melodrama`
- `substitute`
- `urban-life`
- `female-mystery`
- `modern-brainhole`

### Batch 3（6/6 complete）
- `modern-creative`
- `urban-creative`
- `historical`
- `historical-creative`
- `fantasy-romance`
- `republic-romance`

### Batch 4（6/6 complete）
- `system`
- `urban-superpower`
- `xuanhuan`
- `gaowu`
- `western-fantasy`
- `sci-fi`

### Batch 5（6/6 complete）
- `apocalypse`
- `infinite-flow`
- `mystery-brainhole`
- `mystery-creative`
- `mystery-horror`
- `supernatural`

### Batch 6（6/6 complete）
- `rule-mystery`
- `rule-horror`
- `cthulhu`
- `dark`
- `dark-theme`
- `evil-girl`

### Batch 7（6/6 complete）
- `esports`
- `game-sports`
- `livestream`
- `era`
- `spy-war`
- `war-spy`

### Batch 8（2 complete + 1 exception）
- `fertility` — complete
- `multi-offspring` — complete
- `zhihu-short` — partial（专项例外）

---

## 专项例外

### `zhihu-short`
- 主来源：知乎短篇生态
- 不再要求番茄 / 起点 / 晋江三平台对齐完成门槛
- 其他平台仅可作为“短篇形态参考”
- 未完成原因应表述为：**等待知乎主来源证据收集**

---

## 与项目 workflow 的关系

- 本报告是**状态汇报层**，不是 runtime skill 的直接输入。
- runtime skills 当前真正消费的是：
  - `shared/profiles/*`
  - `scripts/profile_contract.py`
  - `.mighty/state.json -> state.genre_profile`
- 因此 evidence batch 的下一步价值不在本报告本身，而在于：
  1. 清理旧污染口径
  2. 推动 `docs/00-当前有效/genre-ontology-field-decisions-v1.5.md` 下沉决策

---

## 验证

- `bash scripts/validate-migration.sh` → passed ✅
- `python3 -m pytest -q tests/test_profile_contract.py` → 65 passed ✅

---

## 结论

跨平台实体证据收集已经从“污染状态”修回到“可复查、可交接、可继续利用”的状态。

当前唯一保留的 `partial` 不是标准缺口，而是显式声明的专项例外：`zhihu-short`。
