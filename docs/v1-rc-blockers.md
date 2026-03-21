# Genm-codex `v1.0.0-rc1` Blocker Log

## 目的

这份文档记录 RC1 阶段真正值得拦住正式版的 blocker，以及当前已知但不构成 blocker 的观察项。

使用原则：

- **blocker**：会阻止 `v1.0.0`
- **observation**：当前不阻止 `v1.0.0`，但应持续观察

---

## 当前结论

- **已确认 blocker：无**
- **活跃观察项：有**

也就是说，当前项目已进入“RC 观察与稳定化”阶段，而不是“RC 紧急修复”阶段。

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
- 状态：open
- 说明：
  - 当前第 4 章 `recommended_next_action = novel-fix`
  - 这是样本文本层问题，不是系统级 blocker
  - 仍可作为 RC 期间继续修正文样本

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
