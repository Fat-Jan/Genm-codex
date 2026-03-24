# 番茄起盘协议栈

这组文档用于把“番茄项目在开篇到黄金三章阶段，究竟该靠什么起盘、靠什么留人、靠什么兑现”收成一层可执行规则。

它不是整本书的大结构理论库，也不是把外部课程原文搬进仓库。

它只解决 5 个问题：

- 一句话故事怎么压缩
- 当前起盘主要靠什么支点
- 前 1-3 章最适合采用什么推进语法
- 平台级留存协议是什么
- 这些判断如何编译给 `outline / write / review / precheck / package`

## 使用原则

1. 先读 [01-premise-layer](./01-premise-layer.md)，锁一句话故事。
2. 再读 [02-pivot-layer](./02-pivot-layer.md)，判断主要起盘支点。
3. 再读 [03-launch-grammar-layer](./03-launch-grammar-layer.md)，给前 1-3 章选推进语法。
4. 任何番茄项目都要过 [04-retention-protocol-layer](./04-retention-protocol-layer.md)。
5. 最后按 [05-compiler-contract](./05-compiler-contract.md) 编译成下游输入。

## 与现有框架的关系

- 它挂在 `opening-and-plot-framework` 下，不另起平行框架。
- 它先于 bucket overlay，但不替代 bucket overlay。
- 它不覆盖 canon、state 真值、bucket 硬约束或已冻结 outline law。

## 当前范围

第一版只覆盖：

- 开篇
- 第 001-003 章
- 早期 promise / hook / 第一次硬兑现

第一版不覆盖：

- 第 004-010 章的中段推进
- 整卷结构
- 整本书结构

## 组成

1. [Premise Layer](./01-premise-layer.md)
2. [Pivot Layer](./02-pivot-layer.md)
3. [Launch Grammar Layer](./03-launch-grammar-layer.md)
4. [Retention Protocol Layer](./04-retention-protocol-layer.md)
5. [Compiler Contract](./05-compiler-contract.md)
6. [六张起盘语法卡](./launch-grammars/README.md)

## 运行结果

运行时统一产物叫：

- `.mighty/launch-stack.json`

详细账本 sidecar 预留为：

- `.mighty/hook-ledger.json`
- `.mighty/payoff-ledger.json`

`state.json` 只镜像轻字段，不承载长篇分析。
