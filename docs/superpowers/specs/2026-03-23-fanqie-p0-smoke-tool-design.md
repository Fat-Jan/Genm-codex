# Fanqie P0 Smoke Tool 设计说明

## 背景

当前仓库已经落成了：

- `opening-and-plot-framework/`
- `fanqie-p0-overlays/`
- `fanqie-p0-checkcards/`
- `fanqie-p0-output-contract.md`
- `fanqie-p0-smoke-template.md`

并且已经在两个真实项目上拿到了：

- 一次只读 smoke
- 一次轻量写回样本
- 一次跨项目只读 smoke

下一步收益最高的，不是继续扩文档，而是补一个**二合一 smoke 工具**，把“骨架生成”和“摘要草稿生成”并到一个入口里。

## 目标

提供一个最小可用工具，面向番茄 `P0` bucket 项目：

1. 生成 smoke 文档骨架
2. 在证据足够时，生成 `fanqie_bucket_review_summary / fanqie_bucket_precheck_summary` 草稿
3. 默认不写回 `state`
4. 只有显式确认或显式参数时，才允许写回 `chapter_meta`

## 核心设计

### 推荐形态

做成一个命令行脚本，暂定：

`python3 scripts/fanqie_p0_smoke.py`

### 模式分层

#### 1. `scaffold`

只生成 smoke 文档骨架：

- 项目信息
- 目标章节 / 范围
- 引用路径
- 空的 review/precheck 模板块

#### 2. `draft`（默认）

在 `scaffold` 基础上，进一步填：

- `fanqie_bucket_review_summary` 草稿
- `fanqie_bucket_precheck_summary` 草稿
- 简短判断依据

但必须明确标成：

- `draft`
- `需人工确认`

#### 3. `writeback`

在 `draft` 基础上，允许把轻量 bucket 字段写回：

- `chapter_meta[N].fanqie_bucket_flags`
- `chapter_meta[N].fanqie_bucket_summary`

这个模式必须显式开启，不能默认触发。

## 默认行为

默认模式采用：

- `draft`

原因：

- 比 `scaffold` 更有实际价值
- 但比默认直接写回更安全

## 安全护栏

### 1. 默认禁止自动写回

不带 `--writeback` 时：

- 绝不修改项目 `state`

### 2. 证据不足自动降级

以下情况自动降级为 `scaffold-only`：

- 项目 bucket 不明确
- 目标章节缺失
- 章纲或正文不足以支持判断
- 当前样本范围明显不足以判断黄金三章

### 3. 摘要必须带证据来源

草稿至少应说明：

- 基于哪些章节
- 基于哪些章纲
- 为什么判 `pass / warn / fail`

### 4. 写回前检查冲突

若目标 `chapter_meta[N]` 已存在：

- `fanqie_bucket_summary`
- `fanqie_bucket_flags`

则默认先提示冲突，不直接覆盖。

## 输入建议

### 必填

- `project_root`

### 条件必填

- `chapter`
  - 生成 review 样本时
- `chapters`
  - 生成 precheck 样本时

### 可选

- `mode=scaffold|draft|writeback`
- `bucket`
  - 默认从 `state.genre_profile.bucket` 或 `meta.genre` 推断
- `output`
  - 自定义 smoke 文档输出路径

## 输出建议

### 文档输出

默认产物落在：

- `docs/opening-and-plot-framework/real-project-smoke-<slug>-fanqie-p0-<date>.md`

### 结构

直接复用现有 `fanqie-p0-smoke-template.md`：

- 项目范围
- `novel-review` 样本
- `novel-precheck` 样本
- 可选写回记录
- 结论

## 状态写回约束

### 允许写回的字段

- `fanqie_bucket_flags`
- `fanqie_bucket_summary`

### 不允许自动写回的字段

- `review_score`
- `review_grade`
- `recommended_next_action`

原因：

- 这些字段更接近正式 review 产物
- 不能由 smoke 工具越权生成

## 为什么不做“一键全自动”

当前不做：

- 读项目
- 自动判断
- 自动写回
- 自动改文档

的一键黑盒工具。

原因是：

- bucket 判断还需要人工兜底
- 真实项目差异大
- 当前最稳的阶段是“半自动工具 + 人工确认”

## 验证思路

### 第一层

结构测试：

- 脚本存在
- 文档入口存在
- 参数帮助存在

### 第二层

最小样本测试：

- 对一个已知 `宫斗宅斗` 项目生成 smoke 草稿
- 检查文档里出现：
  - `fanqie_bucket_review_summary`
  - `fanqie_bucket_precheck_summary`

### 第三层

手工 smoke：

- 复用 `庶女谋略`
- 复用 `庶妹换我婚书那夜，太子先开了口`

## 当前建议

优先做：

- 一个脚本
- 三个模式
- 默认 `draft`
- 默认不写回

不在第一版里做：

- 多 bucket 混合判断
- 市场信号自动拉取
- 自动调用其他技能
