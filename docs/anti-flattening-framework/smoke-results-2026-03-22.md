# 反脸谱化体系 Smoke Results

日期：2026-03-22

## 目标

验证三件事：

1. `P0`：12 模块与首轮接线是否已经形成可读、可引用、可校验的规则层
2. `P1`：`novel-write` / `novel-precheck` 是否已经接上这层规则
3. `P2`：state 轻量写回约定与案例校准是否已经具备单一事实源

## 类型说明

本轮是**结构烟测 + 样本校准烟测**，不是在线运行 Codex skill 的交互式黑盒烟测。

也就是说，本轮验证的是：

- 路径是否存在
- skill 文档是否按需读取正确规则
- 规则顺序是否和现有 bucket / technique / canon 顺序兼容
- 样本项目里是否能找到真实的反脸谱化判断点

## 结果

- `P0`: pass
- `P1`: pass
- `P2`: pass

## P0 结果

### 观察点

- `docs/anti-flattening-framework/` 下 12 模块和 `README.md` 均存在
- `validate-migration.sh` 通过
- 首轮接线已经覆盖：
  - `novel-outline`
  - `novel-review`
  - `novel-fix`

### 实际结论

- 反脸谱化体系已经从讨论稿变成项目内规则层
- 不是散落在 skill 里的零碎措辞
- 也没有污染 `shared/` 同步资产层

## P1 结果

### 观察点

- `novel-write` 新增了：
  - 反脸谱化规则读取
  - 非主角行动可见性
  - 关系负债 / 阵营摩擦
  - 场景残账与代价链
- `novel-precheck` 新增了：
  - 主角特权失衡检查
  - 角色独立性检查
  - 阵营单声道风险检查
  - 推进过顺 / 零代价风险检查

### 顺序兼容性

两者都把规则顺序收成：

1. canon / state / actual text or chapter outline
2. active bucket
3. anti-flattening structure fit
4. writing-technique fit
5. tagpack fit

这与当前 Fanqie 规则栈兼容，没有让新体系越权覆盖老约束。

## P2 结果

### state 约定

- `shared/references/shared/state-schema.md` 已明确：
  - `chapter_meta[N].anti_flattening_flags`
  - `chapter_meta[N].anti_flattening_summary`
- `shared/templates/state-v5-template.json` 已为 `dimension_scores` 预留：
  - `人物立体度`
  - `关系张力`
  - `阵营分歧`
  - `代价感`
- `novel-init` 已明确 `chapter_meta` 是这些轻量结构信号的承载层

### 案例校准

- `12-案例对照与校准.md` 已从抽象例子扩到项目内案例
- 目前已吸收：
  - `e2e-novel` 第004章：临时盟友动机仍需自利理由
  - `e2e-novel` 第005章：能力兑现需要代价钉死
  - `smoke/e2e-gongdou-evil`：单声道风险需要前置监视

## 样本校准摘要

### 样本 1：`e2e-novel`

从 `chapter_meta["4"]` 和 `chapter_meta["5"]` 可见：

- 现有 review 已经能自然暴露“盟友动机不足”和“能力代价发虚”这两类问题
- 这说明新体系不是凭空制造维度，而是在收拢已有问题语言

### 样本 2：`smoke/e2e-gongdou-evil`

从总纲与 `chapter_meta` 可见：

- 当前样本主线节奏很强
- 但如果后续支持者全都只会递证据、站队、开门，极易滑向宫斗线常见的“阵营单声道”
- 这说明 `precheck` 引入反脸谱化检查是合理的，因为它能在投稿前发现“文本还能读，但结构快塌了”的风险

## 结论

本轮 smoke 足以确认：

1. 反脸谱化体系已经是项目内稳定规则层
2. 它不只接在 `outline/review/fix`，也已经进入 `write/precheck`
3. state 写回策略保持轻量，没有新造平行数据库
4. 案例库已经开始从抽象方法论转向项目内校准器

这足以把 `P0`、`P1`、`P2` 都视为**已落地**。
