# Genm-codex `v1.0.0-rc1` Blocker Log

> 历史阶段文档：本文记录的是 `v1.0.0` 正式发布前的 blocker 台账；当前正式状态以 [v1-final-decision.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/v1-final-decision.md) 为准。

## 目的

这份文档记录 RC1 阶段真正值得拦住正式版的 blocker，以及当前已知但不构成 blocker 的观察项。

使用原则：

- **blocker**：会阻止 `v1.0.0`
- **observation**：当前不阻止 `v1.0.0`，但应持续观察

---

## 当前结论

- **已确认 blocker：无**
- **活跃观察项：有，但均不阻塞正式版**

也就是说，当前项目已从“RC 观察与稳定化”推进到“可进入正式版决策”阶段。

---

## Blocker 表

| ID | 类型 | 领域 | 描述 | 状态 |
|----|------|------|------|------|
| B-001 | blocker | - | 当前无已确认 blocker | closed |

---

## 观察项

### O-001 `novel-scan` 仍为实验能力

- 类型：observation
- 领域：实验能力边界
- 状态：open
- 说明：
  - 当前不属于默认工作流
  - 不阻止 `v1.0.0`
  - 但 RC 期间必须继续保持实验标签，不能误入默认主线

### O-002 shared full-copy 仍属可接受但待观察策略

- 类型：observation
- 领域：shared 资产治理
- 状态：open
- 说明：
  - 当前未形成 blocker
  - 但如果未来真实项目暴露同步成本或漂移风险，应重新评估

### O-003 样本项目第 4 章仍建议 `novel-fix`

- 类型：observation
- 领域：样本文本质量
- 状态：closed
- 说明：
  - 原先第 4 章因“即时收益不足 + 章末收束重复”被建议走 `novel-fix`
  - RC 阶段已对第 4 章做定向修补：
    - 补上第一枚青云令的即时收益
    - 把章末直接接回“藏阁 / 父亲血字”线
  - 当前 chapter meta 已显示：
    - `needs_fix = false`
    - `critical_issues = []`
  - 因此该项不再构成活跃观察点

### O-004 `review` 与 `precheck` 对第 4 章的最终判断仍有轻微分叉

- 类型：observation
- 领域：质量路由一致性
- 状态：open
- 说明：
  - 第 4 章在 RC 修补后，章级 review 侧已经不再保留 `needs_fix = true`
  - 但简明番茄 precheck 仍给出 `revise-then-submit`
  - 这说明：
    - review 更偏章级局部质量判断
    - precheck 更偏批量投稿口径与整体批次收益判断
  - 当前看，这更像**口径差异**，不是系统级 blocker
  - 但在 RC 期间仍需继续观察，避免用户误以为两者必然同结论

---

## 记录规则

### 新增 blocker 的条件

只有在出现以下情况之一时，才应新增真正 blocker：

1. 默认工作流主线无法复现
2. 默认能力与文档承诺严重不符
3. `review / precheck / package` 判断明显失真
4. 文档入口再次出现冲突

### 关闭观察项的条件

观察项可关闭，当且仅当：

- 已确认不会阻止正式版
- 或者它已经被证明只属于实验能力范围

---

## 下一步

1. 如果 RC 期间发现新问题，先判断它是 blocker 还是 observation
2. 优先修 blocker
3. observation 只在它开始影响默认工作流时升级
