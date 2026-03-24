# 开篇方法与剧情层次框架

这组文档用于把“怎么开篇更稳、剧情层次怎么搭、推进为什么不该只剩往前冲”沉淀成可复用的项目规则层。

它不是某个单独流派的技巧附录，而是跨题材通用的结构骨架。

如果当前项目是番茄优先，且你想先锁“这本书到底靠什么起盘、靠什么留人、靠什么完成黄金三章第一次硬兑现”，优先再看：

- [fanqie-launch-stack/README.md](./fanqie-launch-stack/README.md)

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
- [番茄 P0 缺口追踪（2026-03）](./fanqie-p0-gap-tracker-2026-03.md)

当前已经完成 `P0 8 桶` 的真实项目样本覆盖，并开始补第二条样本：

- `宫斗宅斗`
- `青春甜宠`
- `都市脑洞`
- `职场婚恋`
- `都市日常`
- `玄幻脑洞`

对应 smoke / writeback 样本可直接看：

- [庶女谋略](./real-project-smoke-shunvmoulue-fanqie-p0-2026-03-23.md)
- [转学第一天，我把校草认成了新来的代课老师](./real-project-smoke-转学第一天-我把校草认成了新来的代课老师-fanqie-p0-2026-03-24.md)
- [公司裁我那天，系统先赔了我一百万](./real-project-smoke-公司裁我那天-系统先赔了我一百万-fanqie-p0-2026-03-24.md)
- [她升职那天，前上司成了我合租室友](./real-project-smoke-她升职那天-前上司成了我合租室友-fanqie-p0-2026-03-24.md)
- [搬回老小区后，我靠蹭饭认识了整栋楼](./real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-fanqie-p0-2026-03-24.md)
- [宗门垫底那年，我把废丹卖成了天价](./real-project-smoke-宗门垫底那年-我把废丹卖成了天价-fanqie-p0-2026-03-24.md)
- [我在县衙当杂吏，靠翻旧案升了堂](./real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-fanqie-p0-2026-03-24.md)
- [签下离婚协议那天，冷脸总裁改口叫我合伙人](./real-project-smoke-签下离婚协议那天-冷脸总裁改口叫我合伙人-fanqie-p0-2026-03-24.md)
- [我在县衙誊旧档，靠半页供词改了判词](./real-project-smoke-我在县衙誊旧档-靠半页供词改了判词-fanqie-p0-2026-03-24.md)
- [离婚冷静期那天，前夫把董事会席位押给了我](./real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-fanqie-p0-2026-03-24.md)
- [我赔光积蓄那天，系统先把违约金打到了账上](./real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-fanqie-p0-2026-03-24.md)
- [外门药田被夺那天，我靠废丹拍卖赚回了灵石](./real-project-smoke-外门药田被夺那天-我靠废丹拍卖赚回了灵石-fanqie-p0-2026-03-24.md)

如果你想直接生成 smoke 草稿，可运行：

```bash
python3 scripts/fanqie_p0_smoke.py --project-root "<project_root>" --chapter 003 --chapters 001-003
```

可选模式：

- `--mode scaffold`
- `--mode draft`
- `--mode writeback --writeback`

## 技能读取包

在 bucket overlay 之前，番茄项目现在可以先用 `fanqie-launch-stack` 做起盘层判断，再把结果编译给后续的 `outline / write / review / precheck / package`。

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

1. [01-开篇目标与成功标准](./01-开篇目标与成功标准.md)
2. [02-开篇构件与组合公式](./02-开篇构件与组合公式.md)
3. [03-开篇故障与修正](./03-开篇故障与修正.md)
4. [04-剧情层次模型](./04-剧情层次模型.md)
5. [05-推进链与残账设计](./05-推进链与残账设计.md)
6. [06-题材特化接口](./06-题材特化接口.md)

## 番茄优先扩展

- [番茄优先分类清单（2026-03）](./fanqie-priority-categories-2026-03.md)
- [番茄 P0 特化卡](./fanqie-p0-overlays/README.md)
- [番茄 P0 专项检查卡](./fanqie-p0-checkcards/README.md)
- [番茄 P0 输出契约](./fanqie-p0-output-contract.md)
- [番茄 P0 Smoke Template](./fanqie-p0-smoke-template.md)
- [番茄 P0 压力测试结果（2026-03-24）](./fanqie-p0-pressure-results-2026-03-24.md)
