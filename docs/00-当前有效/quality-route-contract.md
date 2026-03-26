# 质量路由合同

## 目的

这份文档约束 `novel-review / novel-precheck / novel-package` 在同一项目上使用一致的质量路由语言，避免：

- `review` 说可继续
- `precheck` 说先别投
- `package` 还继续加强包装

## 统一字段

### `route_signal`

最小共享信号：

- `pass`
- `revise_before_submit`
- `packaging_hold`
- `hard_blocker`

## 最小语义

### `pass`

- 当前正文质量与包装状态没有明显 blocker
- 可以继续后续流程

### `revise_before_submit`

- 正文或前 1-3 章承诺兑现还不稳
- 可以继续迭代，但不建议直接投稿

### `packaging_hold`

- 包装层需要暂停加码
- 应先解决正文承载、promise drift 或 gate 风险

### `hard_blocker`

- 存在明确 blocker
- 先修正文、结构或设定问题
- 不应继续包装或投稿推进

## 使用约束

- `novel-review` 负责给出最接近正文的问题归因
- `novel-precheck` 负责把问题解释成“现在适不适合投稿”
- `novel-package` 负责在包装层识别何时应进入 `packaging_hold`

## 不做什么

- 不把这份合同写成新的评分系统
- 不在多个 skill 文案里各自发明不同 blocker 名词
