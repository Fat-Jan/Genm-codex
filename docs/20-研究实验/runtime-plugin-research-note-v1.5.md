# `v1.5` Runtime / Plugin 研究稿

> 当前生效边界以 [runtime-boundary-adr.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/runtime-boundary-adr.md) 为准；本文保留为研究记录，不是执行面真值。

## 目的

这份草案服务于 `P1-F`，只做研究，不做实装方案。

当前研究问题不是“要不要立刻引入 runtime / plugin”，而是：

- 哪些外部方式可能增强 agent 调用知识
- 它们与当前边界哪里兼容，哪里冲突
- 为什么 `v1.5` 只保留研究稿和边界说明

---

## 当前边界

`v1.5` 当前边界仍是：

- `repo truth + sidecar + MCP`

也就是说：

- repo file 仍是项目真值
- sidecar 是受控辅助层
- MCP 是只读 consumer 层
- 不引入新的 daemon / scheduler / plugin framework / orchestration runtime

---

## 可研究的方向

### 1. 更稳定的 read path

研究重点：

- agent 如何更稳定读取 repo-owned truth
- sidecar 如何更稳定被消费
- 不同入口下如何减少“读散文件 + 读过量规则”的成本

### 2. 更清晰的 consumer 接入方式

研究重点：

- contract / ADR / registry / manifest 这些中间层如何帮助 consumer 读取
- 哪些能力适合继续 docs-first
- 哪些能力适合逐步 machine-readable

### 3. 外部增强方式比较

研究重点：

- 不同接入方式的收益
- 它们是否会带来第二真值中心
- 它们是否会绕过 gate / canon / sidecar 边界

---

## 当前不进入 `v1.5` 实装的原因

### 1. 当前收益小于复杂度

仓库当前主线已经具备：

- 可恢复 workflow
- 可读 sidecar
- 可读 MCP 路径

所以新增 runtime / plugin framework 的收益，目前小于它带来的故障面。

### 2. 容易形成第二真值中心

只要新的系统开始持有：

- 项目 canon
- gate 结论
- profile / scan / setting 的权威状态

它就会和当前 repo truth 冲突。

### 3. 容易借研究名义偷渡实装

`v1.5` 当前最危险的不是“完全不研究”，而是边研究边偷偷变成新的运行时中心。

所以边界必须先写死：

- 可以比较
- 可以写设计稿
- 可以做 ADR
- 不能直接上 runtime / daemon / plugin framework

---

## 与 `novel-scan` 的边界关系

`novel-scan` 当前可以继续推进 contract 和 consumer 接线，但不应成为 runtime 研究的借口。

尤其不允许：

- 借 runtime 注入把 scan 结果写成新真值
- 绕过 gate / canon / sidecar 读取边界
- 把 market 信号提升为项目权威事实

---

## 当前研究稿的输出要求

在 `v1.5` 里，这类研究稿最适合输出：

- 边界说明
- 风险清单
- 非目标清单
- 不同接入方式的优缺点对比

而不适合输出：

- 实装路线图
- daemon 设计
- plugin framework 设计
- 新真值写回路径
