# 开篇方法与剧情层次框架

这组文档用于把“怎么开篇更稳、剧情层次怎么搭、推进为什么不该只剩往前冲”沉淀成可复用的项目规则层。

它不是某个单独流派的技巧附录，而是跨题材通用的结构骨架。

## 使用原则

1. 先看 `01-开篇目标与成功标准.md`，明确开篇到底要完成什么。
2. 做总纲或章纲时，优先读剧情层次与推进链模块。
3. 做正文时，按需读取开篇构件和故障修正模块。
4. 做评审和投稿前检查时，把它当成“开篇承诺 + 层次清晰度 + 推进账本”的检查层。
5. 题材特化第一版只读接口，不要求现在就把所有题材规则铺满。

如果当前项目走的是番茄路线，优先再读：

- [番茄优先分类清单（2026-03）](./fanqie-priority-categories-2026-03.md)
- [番茄 P0 特化卡](./fanqie-p0-overlays/README.md)
- [番茄 P0 专项检查卡](./fanqie-p0-checkcards/README.md)
- [番茄 P0 输出契约](./fanqie-p0-output-contract.md)
- [番茄 P0 Smoke Template](./fanqie-p0-smoke-template.md)
- [番茄 P0 压力测试结果（2026-03-24）](./fanqie-p0-pressure-results-2026-03-24.md)

如果你想直接生成 smoke 草稿，可运行：

```bash
python3 scripts/fanqie_p0_smoke.py --project-root "<project_root>" --chapter 003 --chapters 001-003
```

可选模式：

- `--mode scaffold`
- `--mode draft`
- `--mode writeback --writeback`

## 技能读取包

### `novel-outline` 上游结构包

- `01-开篇目标与成功标准.md`
- `04-剧情层次模型.md`
- `05-推进链与残账设计.md`
- 需要开篇强化或题材特化时再读：
  - `02-开篇构件与组合公式.md`
  - `03-开篇故障与修正.md`
  - `06-题材特化接口.md`

### `novel-write` 写作约束包

- `01-开篇目标与成功标准.md`
- `02-开篇构件与组合公式.md`
- `03-开篇故障与修正.md`
- `04-剧情层次模型.md`
- `05-推进链与残账设计.md`
- 需要题材特化时再读：
  - `06-题材特化接口.md`

### `novel-review` 结构检查包

- `01-开篇目标与成功标准.md`
- `02-开篇构件与组合公式.md`
- `03-开篇故障与修正.md`
- `04-剧情层次模型.md`
- `05-推进链与残账设计.md`
- 需要题材特化时再读：
  - `06-题材特化接口.md`

### `novel-precheck` 投稿前检查包

- `01-开篇目标与成功标准.md`
- `02-开篇构件与组合公式.md`
- `04-剧情层次模型.md`
- `05-推进链与残账设计.md`
- `06-题材特化接口.md`

### `novel-package` 包装承诺包

- `01-开篇目标与成功标准.md`
- `02-开篇构件与组合公式.md`
- `03-开篇故障与修正.md`
- `06-题材特化接口.md`

## 规则优先级

推荐按这个顺序应用：

1. canon / 用户要求 / `.mighty/state.json`
2. active bucket / 平台硬约束 / 已冻结 outline law
3. 开篇方法与剧情层次框架
4. 反脸谱化框架
5. 技巧层优化与风味增强

这意味着这套框架负责“把开篇写成真正的故事入口，把推进写成有账本的推进”，但不能越权覆盖 canon、bucket law 或已经冻结的真值。

## 6 个主模块

1. [01-开篇目标与成功标准](./01-%E5%BC%80%E7%AF%87%E7%9B%AE%E6%A0%87%E4%B8%8E%E6%88%90%E5%8A%9F%E6%A0%87%E5%87%86.md)
2. [02-开篇构件与组合公式](./02-%E5%BC%80%E7%AF%87%E6%9E%84%E4%BB%B6%E4%B8%8E%E7%BB%84%E5%90%88%E5%85%AC%E5%BC%8F.md)
3. [03-开篇故障与修正](./03-%E5%BC%80%E7%AF%87%E6%95%85%E9%9A%9C%E4%B8%8E%E4%BF%AE%E6%AD%A3.md)
4. [04-剧情层次模型](./04-%E5%89%A7%E6%83%85%E5%B1%82%E6%AC%A1%E6%A8%A1%E5%9E%8B.md)
5. [05-推进链与残账设计](./05-%E6%8E%A8%E8%BF%9B%E9%93%BE%E4%B8%8E%E6%AE%8B%E8%B4%A6%E8%AE%BE%E8%AE%A1.md)
6. [06-题材特化接口](./06-%E9%A2%98%E6%9D%90%E7%89%B9%E5%8C%96%E6%8E%A5%E5%8F%A3.md)

## 番茄优先扩展

- [番茄优先分类清单（2026-03）](./fanqie-priority-categories-2026-03.md)
- [番茄 P0 特化卡](./fanqie-p0-overlays/README.md)
- [番茄 P0 专项检查卡](./fanqie-p0-checkcards/README.md)
- [番茄 P0 输出契约](./fanqie-p0-output-contract.md)
- [番茄 P0 Smoke Template](./fanqie-p0-smoke-template.md)
- [番茄 P0 压力测试结果（2026-03-24）](./fanqie-p0-pressure-results-2026-03-24.md)
