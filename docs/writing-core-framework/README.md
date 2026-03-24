# 写作基本功与内容标准框架

这组文档用于把“写作基本功 / 内容标准 / memory 压缩信号 / 开篇包装输入”收成项目内单一事实源。

它**不是课程 dump**，也不是把外部教程全文搬进仓库。它只保留能被 `outline / write / review / precheck / package / learn` 消费的可执行规则。

## 边界

- `剧情层次` 与推进账本，继续复用 [opening-and-plot-framework](../opening-and-plot-framework/README.md)
- 这组框架只补当前缺口：
  - `写作基本功`
  - `内容标准`
  - `memory` 压缩信号约定
  - `开篇包装输入`

## 使用原则

1. 先用 `01-写作基本功总纲.md` 锁“正文执行”到底在检查什么。
2. 需要控制镜头、叙述和信息投放时，读 `02-叙述-镜头-信息投放.md`。
3. 需要控制对白、动作、情绪和段落节奏时，读 `03-对白-动作-情绪-段落节奏.md`。
4. 需要把本框架和现有剧情层次框架接起来时，读 `04-剧情层次与多线编排接口.md`。
5. 做 review / precheck 时，优先用 `05-内容标准与常见失格.md` 和 `06-精品审核与投稿前判断.md`。
6. 做 learn / state 写回时，只读 `07-memory-压缩信号约定.md`，不要把整套理论塞进 memory。
7. 做 package 时，优先读 `08-开篇包装输入接口.md`，把正文能承载的 promise 转成包装约束。

## 技能读取包

### `novel-outline`

- `04-剧情层次与多线编排接口.md`
- 需要开篇 promise 整形时再读：
  - `08-开篇包装输入接口.md`

### `novel-write`

- `01-写作基本功总纲.md`
- `02-叙述-镜头-信息投放.md`
- `03-对白-动作-情绪-段落节奏.md`
- `05-内容标准与常见失格.md`

### `novel-review`

- `01-写作基本功总纲.md`
- `02-叙述-镜头-信息投放.md`
- `03-对白-动作-情绪-段落节奏.md`
- `05-内容标准与常见失格.md`
- `06-精品审核与投稿前判断.md`
- `07-memory-压缩信号约定.md`

### `novel-precheck`

- `05-内容标准与常见失格.md`
- `06-精品审核与投稿前判断.md`
- `08-开篇包装输入接口.md`

### `novel-package`

- `06-精品审核与投稿前判断.md`
- `08-开篇包装输入接口.md`

### `novel-learn`

- `07-memory-压缩信号约定.md`

## 样本证据

- [宗门垫底那年，我把废丹卖成了天价：手工 smoke](./real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md)
- [离婚冷静期那天，前夫把董事会席位押给了我：手工 smoke](./real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md)
- [搬回老小区后，我靠蹭饭认识了整栋楼：脚本化 smoke](./real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-2026-03-24.md)
- [我在县衙当杂吏，靠翻旧案升了堂：脚本化 smoke](./real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-2026-03-24.md)
- [她升职那天，前上司成了我合租室友：脚本化 smoke](./real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md)
- [转学第一天，我把校草认成了新来的代课老师：脚本化 smoke](./real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md)
- [我赔光积蓄那天，系统先把违约金打到了账上：脚本化 smoke](./real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md)
- [继母换我婚书那夜，太子先开了口：脚本化 smoke](./real-project-smoke-继母换我婚书那夜-太子先开了口-2026-03-24.md)

如果你不想手工起草整份 smoke，可先用：

```bash
python3 scripts/writing_core_smoke.py --project-root "<project_root>" --chapters 001-003
```

若要把 smoke 继续推进成最小 writeback 与包装产物，可用：

```bash
python3 scripts/writing_core_smoke.py --project-root "<project_root>" --chapters 001-003 --mode writeback --writeback --save-packaging
```

如果你要一次跑多个项目，可用：

```bash
python3 scripts/batch_writing_core_smoke.py --manifest "<manifest.json>" --output-dir "<out_dir>" --mode draft
```

仓库内固定基线：

- manifest: [batch-smoke-manifest.json](./batch-smoke-manifest.json)
- output dir: [batch-output](/Users/arm/Desktop/vscode/Genm-codex/docs/writing-core-framework/batch-output)

## 规则优先级

推荐顺序：

1. canon / 用户要求 / `.mighty/state.json`
2. active bucket / 平台硬约束 / 已冻结 outline law
3. `opening-and-plot-framework`
4. `writing-core-framework`
5. `anti-flattening-framework`
6. 技巧层优化与风味增强

## 文档清单

1. [01-写作基本功总纲](./01-写作基本功总纲.md)
2. [02-叙述-镜头-信息投放](./02-叙述-镜头-信息投放.md)
3. [03-对白-动作-情绪-段落节奏](./03-对白-动作-情绪-段落节奏.md)
4. [04-剧情层次与多线编排接口](./04-剧情层次与多线编排接口.md)
5. [05-内容标准与常见失格](./05-内容标准与常见失格.md)
6. [06-精品审核与投稿前判断](./06-精品审核与投稿前判断.md)
7. [07-memory-压缩信号约定](./07-memory-压缩信号约定.md)
8. [08-开篇包装输入接口](./08-开篇包装输入接口.md)
