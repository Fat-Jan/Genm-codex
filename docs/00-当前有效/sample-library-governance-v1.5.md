# `v1.5` 样本库治理

## 目的

`v1.5` 里，样本库治理的重点不是继续把样本写成一张越来越长的索引页，而是把“人可读索引 + machine-readable manifest + 回归用途说明”三者对齐。

这份文档收口 `P1-B`，只回答三件事：

1. 当前样本分哪些层。
2. 每层样本主要拿来做什么。
3. 后续维护时，哪些动作可以交给 `mimo`，哪些仍要等 `codex` consumer 接线。

---

## 当前样本分层

### 1. `smoke / baseline`

对应当前稳定的端到端样本，如：

- `smoke/e2e-gongdou/`
- `smoke/e2e-gongdou-evil/`
- `smoke/e2e-qinggan/`
- `smoke/e2e-qinggan-evil/`
- `smoke/e2e-tianchong/`
- `smoke/e2e-tianchong-evil/`
- `smoke/e2e-dual-substitute-evil/`

这一层的定位是：

- repo-owned 的自动 smoke
- 默认框架与 workflow 骨架的稳定回归入口
- 新 contract / 新 consumer 的最小验证样本

### 2. `smoke / derived`

对应从基线样本派生出来的验证副本，如：

- `smoke/e2e-gongdou-evil-antiflattening-20260322/`
- `smoke/e2e-qinggan-evil-antiflattening-20260322/`
- `smoke/e2e-system-antiflattening-20260322/`
- `smoke/e2e-dual-substitute-evil-antiflattening-20260322/`

这一层的定位是：

- 验证某个框架、规则层或专项流程是否真的打通
- 保留“基线样本 + 某次扩层”的可比较关系
- 不替代 baseline，只补充派生证据

### 3. `project / regression`

当前典型样本：

- `projects/成婚前三日，我先改了侯府嫁妆单/`

这一层的定位是：

- 绑定明确退化风险
- 说明“它在防什么回归”
- 给结构扫描、质量门和后续 consumer 提供真实失败指纹

### 4. `project / high_confidence`

当前典型样本：

- `projects/庶女谋略/`
- `projects/庶妹换我婚书那夜，太子先开了口/`

这一层的定位是：

- 作为质量基准和正向参考
- 给 bucket 校准、project 观察和质量判断提供高置信样本
- 不承担“失败模式展示”的职责

### 5. `project / bucket_sample`

当前典型样本包括：

- 修仙
- 豪门总裁
- 青春甜宠
- 都市脑洞
- 都市日常
- 历史脑洞
- 职场婚恋

这一层的定位是：

- 给 bucket / profile 扩面提供真实落点
- 作为题材覆盖面样本，而不是最高质量样本
- 优先回答“这个 bucket 有没有真实项目承载”

---

## 推荐标签口径

为避免索引页、人肉记忆和后续 manifest 实体化再次漂移，`v1.5` 建议统一只保留以下标签轴：

- `sample_type`
  - `smoke`
  - `project`
- `trust_tier`
  - `baseline`
  - `derived`
  - `regression`
  - `high_confidence`
  - `bucket_sample`
- `status`
  - `active`
  - `archived`
  - `draft`

不建议再平行发明新的主标签体系。

---

## 样本维护规则

### 新增样本

新增前先回答：

1. 它属于 `smoke` 还是 `project`。
2. 它的 `trust_tier` 是什么。
3. 它要防什么风险，或代表什么质量基准。
4. 它有没有稳定路径和可复用说明。

如果这四个问题答不清，就先不要把样本纳入正式样本库。

### 更新样本

更新样本时，优先更新：

- 样本用途
- 分层归属
- 是否仍为 `active`
- 是否需要追加 `verification_targets`

而不是只改样本文本，不更新说明。

### 清理样本

样本清理前至少确认：

- 不再被现有 smoke / regression / docs 引用
- 已经有更稳定的替代样本
- 对应索引和 manifest 能同步移除或归档

---

## `mimo` 当前可直接推进的部分

在 `v1.5` 当前阶段，`mimo` 可以直接推进：

- 样本 inventory 整理
- 分层说明文档
- 样本 matrix 草案
- 人可读索引补充

当前不应由 `mimo` 直接推进：

- 新 schema 设计
- consumer 行为定义
- 测试入口改造

这些仍与 `codex` 侧的 contract / consumer 工作绑定。

---

## 与 manifest 的关系

`sample-library-index.md` 继续保留为人读入口，但在 `v1.5` 中应逐步降级为“说明页”，而不是样本真值中心。

当前推荐关系是：

- manifest：machine-readable 真值入口
- 本文：治理与分层说明
- sample-library-index：人可读索引页

这样可以把“真值、治理、浏览”三层分开。
