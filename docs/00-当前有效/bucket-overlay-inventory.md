# Bucket Overlay Inventory

## 目的

盘点当前 bucket overlay 的实现情况，记录现状、历史背景与后续维护规则，避免后续把历史缺口误判为当前未完成事项。

---

## 当前状态

### Platform Overlay

| profile | platform | 文件 | 状态 |
|---------|----------|------|------|
| urban-superpower | tomato | `profile-tomato.yaml` | ✅ 已实现 |
| system | tomato | `profile-tomato.yaml` | ✅ 已实现 |
| xuanhuan | tomato | `profile-tomato.yaml` | ✅ 已实现 |
| xiuxian | tomato | `profile-tomato.yaml` | ✅ 已实现 |

### Bucket Overlay

| profile | bucket | 文件 | 状态 |
|---------|--------|------|------|
| apocalypse | 科幻末世 | `bucket-apocalypse.yaml` | ✅ 已实现 |
| historical | 历史脑洞 | `bucket-historical.yaml` | ✅ 已实现 |
| melodrama | 豪门总裁 | `bucket-melodrama.yaml` | ✅ 已实现 |
| palace-intrigue | 宫斗宅斗 | `bucket-palace-intrigue.yaml` | ✅ 已实现 |
| realistic | 现实情感 | `bucket-realistic.yaml` | ✅ 已实现 |
| romance | 青春甜宠 | `bucket-romance.yaml` | ✅ 已实现 |
| sweet-romance | 青春甜宠 | `bucket-sweet-romance.yaml` | ✅ 已实现 |
| system | 都市脑洞 | `bucket-system.yaml` | ✅ 已实现 |
| urban-brainhole | 都市脑洞 | `bucket-urban-brainhole.yaml` | ✅ 已实现 |
| urban-daily | 都市日常 | `bucket-urban-daily.yaml` | ✅ 已实现 |
| urban-superpower | 都市脑洞 | `bucket-urban-superpower.yaml` | ✅ 已实现 |
| sweet-youth | 青春甜宠 | `bucket-sweet-youth.yaml` | ✅ 已实现 |
| ceo-romance | 豪门总裁 | `bucket-ceo-romance.yaml` | ✅ 已实现 |
| workplace-romance | 职场婚恋 | `bucket-workplace-romance.yaml` | ✅ 已实现 |
| historical-brainhole | 历史脑洞 | `bucket-historical-brainhole.yaml` | ✅ 已实现 |
| xiuxian | 传统玄幻 | `bucket-xiuxian.yaml` | ✅ 已实现 |
| xuanhuan | 玄幻脑洞 | `bucket-xuanhuan.yaml` | ✅ 已实现 |

---

## 缺口分析

### 1. Bucket Overlay 文件缺失

当前已补齐所有声明了 `fanqie primary_bucket` 的 `bucket-*.yaml` 文件，因此当前**不存在已知缺失项**。后续新增 profile 若继续声明 `fanqie primary_bucket`，也必须同步补 overlay。根据 contract 分层，bucket overlay 应该：

- **路径**: `profiles/<slug>/bucket-<bucket>.yaml`
- **内容**: 只放内容桶差异
- **作用**: 在 platform overlay 之上，进一步特化内容桶规则

### 2. P0 Bucket 历史背景

根据 `fanqie-mvp-buckets.yaml`，当时优先补齐的 P0 bucket 包括：

1. `gongdou_zhai` (宫斗宅斗)
2. `dushi_naodong` (都市脑洞)
3. `dushi_changri` (都市日常)
4. `qingchun_tianchong` (青春甜宠)
5. `haomen_zongcai` (豪门总裁)
6. `zhichang_hunlian` (职场婚恋)
7. `lishi_naodong` (历史脑洞)
8. `xuanhuan_naodong` (玄幻脑洞)

### 3. 当前维护重点

| 维护项 | 当前状态 | 说明 |
|--------|----------|------|
| 已声明 primary_bucket 的 overlay 文件 | ✅ 已补齐 | 当前无已知缺失 |
| 新 profile 新增 primary_bucket 时同步补 overlay | ⏳ 持续维护 | 新增声明时仍需同步补齐 |
| overlay 文件格式一致性 | ⏳ 持续维护 | 后续如新增 overlay，继续保持统一格式 |

---

## 实现方案

### 1. Bucket Overlay 文件结构

```yaml
# profiles/<slug>/bucket-<bucket>.yaml
name: "<bucket display_name>"
description: "<bucket description>"
version: "1.0"

# 只放与 platform overlay 不同的部分
# 例如：特定 bucket 的约束、爽点类型、节奏调整等
```

## 参考实现样例

以下内容保留为“首批 P0 bucket overlay 的参考实现样例”，用于说明当时如何从 bucket 定义落到实际 overlay 文件；它们不是当前待办清单。

### 1. 首批 P0 bucket 样例

#### gongdou_zhai (宫斗宅斗)

- **profile slug**: palace-intrigue
- **bucket slug**: palace-intrigue
- **fanqie-mvp-bucket slug**: gongdou_zhai
- **display_name**: 宫斗宅斗
- **overlay 文件**: `profiles/palace-intrigue/bucket-palace-intrigue.yaml`
- **内容来源**: `docs/gongdou-zhaidou-fault-funnel-review-card.md`、`docs/opening-and-plot-framework/fanqie-p0-overlays/宫斗宅斗.md`

#### dushi_naodong (都市脑洞)

- **profile slug**: urban-brainhole
- **bucket slug**: urban-brainhole
- **fanqie-mvp-bucket slug**: dushi_naodong
- **display_name**: 都市脑洞
- **overlay 文件**: `profiles/urban-brainhole/bucket-urban-brainhole.yaml`
- **内容来源**: `docs/fanqie-mvp-buckets.yaml`、`docs/fanqie-mvp-bucket-templates.md`

#### dushi_changri (都市日常)

- **profile slug**: urban-daily
- **bucket slug**: urban-daily
- **fanqie-mvp-bucket slug**: dushi_changri
- **display_name**: 都市日常
- **overlay 文件**: `profiles/urban-daily/bucket-urban-daily.yaml`
- **内容来源**: `docs/fanqie-mvp-buckets.yaml`、`docs/fanqie-mvp-bucket-templates.md`

#### qingchun_tianchong (青春甜宠)

- **profile slug**: sweet-youth
- **bucket slug**: sweet-youth
- **fanqie-mvp-bucket slug**: qingchun_tianchong
- **display_name**: 青春甜宠
- **overlay 文件**: `profiles/sweet-youth/bucket-sweet-youth.yaml`
- **内容来源**: `docs/fanqie-mvp-buckets.yaml`、`docs/fanqie-mvp-bucket-templates.md`

#### haomen_zongcai (豪门总裁)

- **profile slug**: ceo-romance
- **bucket slug**: ceo-romance
- **fanqie-mvp-bucket slug**: haomen_zongcai
- **display_name**: 豪门总裁
- **overlay 文件**: `profiles/ceo-romance/bucket-ceo-romance.yaml`
- **内容来源**: `docs/fanqie-mvp-buckets.yaml`、`docs/fanqie-mvp-bucket-templates.md`

#### zhichang_hunlian (职场婚恋)

- **profile slug**: workplace-romance
- **bucket slug**: workplace-romance
- **fanqie-mvp-bucket slug**: zhichang_hunlian
- **display_name**: 职场婚恋
- **overlay 文件**: `profiles/workplace-romance/bucket-workplace-romance.yaml`
- **内容来源**: `docs/fanqie-mvp-buckets.yaml`、`docs/fanqie-mvp-bucket-templates.md`

#### lishi_naodong (历史脑洞)

- **profile slug**: historical-brainhole
- **bucket slug**: historical-brainhole
- **fanqie-mvp-bucket slug**: lishi_naodong
- **display_name**: 历史脑洞
- **overlay 文件**: `profiles/historical-brainhole/bucket-historical-brainhole.yaml`
- **内容来源**: `docs/fanqie-mvp-buckets.yaml`、`docs/fanqie-mvp-bucket-templates.md`

#### xuanhuan_naodong (玄幻脑洞)

- **profile slug**: xuanhuan
- **bucket slug**: xuanhuan
- **fanqie-mvp-bucket slug**: xuanhuan_naodong
- **display_name**: 玄幻脑洞
- **overlay 文件**: `profiles/xuanhuan/bucket-xuanhuan.yaml`
- **内容来源**: `docs/fanqie-mvp-buckets.yaml`、`docs/fanqie-mvp-bucket-templates.md`

---

## 下一步

### 当前阶段（v1.5 后）

1. **保持新增声明即补 overlay**：
   - 新 profile 若新增 `fanqie primary_bucket`，同步补对应 `bucket-*.yaml`

2. **保持 overlay 文件格式一致性**：
   - 新增 overlay 时继续沿用当前结构和字段分层

3. **视需要补模板与一致性检查**：
   - 如后续新增 overlay 频率变高，可再考虑：
     - `shared/templates/bucket-overlay-template.yaml`
     - bucket overlay 一致性检查
     - bucket overlay 与 platform overlay 冲突检查

### 历史实现记录

以下事项已完成，不再属于当前待办：

- P0 bucket overlay 文件已创建
- `profile_contract.py` 已更新
- `build_content_positioning.py` 已更新

---

## 完成标记

- [x] 有独立设计稿（本文件）
- [x] 已区分现状、历史背景与后续维护点
- [x] P0 bucket overlay 文件已创建
- [x] `profile_contract.py` 已更新
- [x] `build_content_positioning.py` 已更新
