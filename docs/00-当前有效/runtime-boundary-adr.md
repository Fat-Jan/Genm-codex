# Runtime Boundary ADR

## 结论

`v1.5` 继续维持当前边界：

- `repo truth + sidecar + MCP`

不进入：

- daemon
- scheduler
- plugin framework
- orchestration runtime

也不允许形成：

- 第二真值中心

---

## 为什么

当前主线已经有：

- repo truth
- sidecar
- MCP read path

这些已经能满足：

- workflow 可恢复
- agent 可读取
- sidecar 可审计

再引入 runtime/daemon 的收益，当前小于复杂度和故障面。

---

## `v1.5` 允许做的

- runtime / plugin 研究
- ADR / 边界说明
- 非实装的设计稿
- 对比不同接入方式的优缺点

## `v1.5` 不允许做的

- 引入新的 daemon
- 引入新的 scheduler
- 引入 plugin framework
- 引入 orchestration runtime
- 让新的系统持有项目 canon

研究可以做，但不进 v1.5 实装。

---

## 与 `novel-scan` 的关系

`novel-scan` 当前可以继续做 contract 和 consumer 接线，但：

- 不能借机变成第二真值中心
- 不能通过 runtime 注入绕过 gate / canon / sidecar 边界

---

## 与 MCP 的关系

MCP 在当前边界里的定位仍然是：

- read-only consumer layer
- 帮 agent 稳定读取 repo-owned truth / sidecar

它不是 runtime truth，也不是写回中心。
