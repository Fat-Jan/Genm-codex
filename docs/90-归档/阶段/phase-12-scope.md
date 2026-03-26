# Genm-codex 第十二阶段范围设计

## 设计结论

前十一阶段已经把迁移、整合、默认工作流和 `v1.0.0` 边界基本写清。

第十二阶段不再继续扩大能力面，而是开始正式核验：

- **离 `v1.0.0` 还差哪些门槛**

因此第十二阶段的主线是：

- `v1.0.0` 前置门槛核验

---

## 核心目标

把 [v1-boundary.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/v1-boundary.md) 里的前置门槛，变成一份真正可检查的清单和一份带结论的 readiness assessment。

---

## Phase 12A：门槛清单化

### 目标

把 `v1.0.0` 的前置条件拆成 checklist，而不是继续停留在原则层。

### 第一版产物

- `docs/90-归档/迁移与RC/v1-readiness-checklist.md`

建议至少包含：

1. 默认工作流已成文
2. 默认能力 / 实验能力边界已成文
3. 包装层判断稳定
4. 质量路由稳定
5. 样本闭环验证完整
6. 入口文档一致
7. 实验能力未误导默认工作流

---

## Phase 12B：状态判定

### 目标

对 checklist 中每一项给出状态：

- `pass`
- `partial`
- `fail`
- `deferred`

### 第一版产物

- `docs/90-归档/迁移与RC/v1-readiness-assessment.md`

建议包含：

- 每项状态
- 对应证据
- blocker 列表
- 当前建议：
  - 继续 `0.x`
  - 进入 `v1.0.0-rc`

---

## 不做什么

第十二阶段暂不做：

- 新能力迁移
- shared 同步策略切换
- `novel-scan` 正式化
- 直接发布 `v1.0.0`

---

## 版本边界建议

- **`v0.16.0`**
  - 如果 checklist 和 readiness assessment 落地

- **`v1.0.0-rc1`**
  - 仅当 assessment 明确显示没有 blocker

---

## 当前推荐下一步

如果继续自动推进，第十二阶段最合理的第一项是：

1. 先写 `v1-readiness-checklist.md`
2. 再写 `v1-readiness-assessment.md`

这会把 `1.0` 讨论从感觉判断变成证据判断。
