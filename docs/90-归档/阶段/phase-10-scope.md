# Genm-codex 第十阶段范围设计

## 设计结论

第十阶段不再围绕“还缺什么命令”展开，而是围绕第九阶段已经显现出来的两个高价值方向继续推进：

- **包装层与市场信号收敛**
- **质量闭环从建议走向稳定路由**

第九阶段已经证明：

1. 包装层值得存在
2. 市场信号已经能进入项目级状态
3. 质量链已经不只是零散技能，而是开始出现系统性

第十阶段的目标，就是把这三点进一步压实。

---

## Phase 10A：包装与市场信号收敛

### 目标

让 `novel-package` 不只是“会生成包装文案”，而是能更稳定地吸收：

- `market_adjustments`
- `genre`
- `precheck` 反馈
- 当前项目进度

并将这些信号转成更稳定的包装输出。

### 核心问题

当前 `novel-package` 已经可用，但还存在这些边界：

- 市场信号已经能读，但还没有形成统一的包装优先级模型
- 包装输出和 `precheck` 之间还没有明确回流关系
- 标题 / 简介 / 开篇包装还没有统一“推荐主方案 + 次方案”的结构规范

### 建议推进项

1. 统一包装输出结构
   - 推荐方案
   - 备选方案
   - 放弃理由
2. 让包装层显式吸收：
   - `market_adjustments`
   - `precheck` 的 must-fix / should-fix
3. 限定包装层边界：
   - 仍然不默认改正文
   - 仍然不默认改 shared profile

---

## Phase 10B：质量闭环稳定路由

### 目标

让当前已经存在的质量链：

- `write`
- `review`
- `fix`
- `polish`
- `rewrite`
- `precheck`
- `learn`

从“能配合工作”变成“路由更稳、判断更一致”。

### 核心问题

当前第九阶段已经做了第一轮整合，但还缺：

- `review` 推荐动作的进一步稳定化
- `precheck` 对 review 覆盖度和 packaging readiness 的更明确引用
- `learn` 输出在 downstream 使用时的优先级约定
- “什么时候 fix / 什么时候 polish / 什么时候 rewrite” 的更稳定边界

### 建议推进项

1. 收紧 review 路由规范
   - 局部问题 -> `fix`
   - 语言问题 -> `polish`
   - 结构问题 -> `rewrite`
2. 让 `precheck` 明确输出：
   - ready now
   - revise then submit
   - packaging needs update
3. 让 `learn` 输出更像“下游可消费信号”而不是“分析报告”

---

## 推荐实施顺序

1. `Phase 10A / P0`
   - 包装层输出结构标准化
2. `Phase 10B / P0`
   - review / precheck 路由一致性收紧
3. `Phase 10A / P1`
   - packaging 与 market-adjustments 深度结合
4. `Phase 10B / P1`
   - learn 输出的 downstream 优先级固化

---

## 不做什么

第十阶段暂不做：

- 新的低价值 help/tutorial 命令
- shared profile 自动重写
- 大规模 state schema 重构
- 一步到位的 `v1.0.0`

---

## 版本边界建议

- **`v0.14.0`**
  - 如果包装层输出结构与质量路由收紧落地

- **`v0.15.0`**
  - 如果包装层和市场信号进一步真正收敛

---

## 当前推荐下一步

如果继续自动推进，第十阶段最自然的第一项是：

1. 先统一 `novel-package` 的输出结构
2. 再收紧 `review / precheck` 的动作路由

这样能延续第九阶段的主线，而不会重新掉回命令堆叠。
