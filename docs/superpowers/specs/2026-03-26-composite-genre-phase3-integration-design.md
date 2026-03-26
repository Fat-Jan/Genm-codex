# 组合题材支持：Phase 3 整合说明

Date: 2026-03-26

## 目标

为 `Genm-codex` 补一层“组合题材 / 多主题卖点 / 群像结构模式”的稳定整合说明，供后续 Phase 3 的 consumer 收口直接使用。

这份说明的定位不是：

- 现在立刻改动 `A4` 已收口的写集
- 现在立刻实现复杂多 profile 混合
- 另起一套平行 runtime

它的定位是：

- 在 `A4` 已统一 `profile` consumer 入口之后
- 给后续 `novel-outline / novel-write / novel-review / novel-package` 增加一层可控的“组合题材 support”
- 且不破坏当前 `主 profile + 主 bucket + 轻 state + sidecar` 的总架构

## 触发背景

近期番茄前台越来越常见的作品定位不是单一题材名，而是：

- 一个主分类 / 主内容桶
- 若干平台可见标签
- 若干简介里的结构性卖点

以 `https://fanqienovel.com/page/7496026299845053465` 为例，2026-03-26 可见前台组织方式是：

- 主分类：`科幻末世`
- 页面标签：`穿越 / 末世 / 大佬 / 搞笑轻松`
- 简介结构卖点：`成长主线 / 多主题副本 / 多角色群像 / 偶尔爆杀 / 非套路 / 非无脑爽`

这说明番茄前台当前更像：

- `主桶 + 标签 + 结构卖点`

而不是：

- 多个同级主桶并列
- 多个同级 profile 并列

因此，本项目不应把“组合题材支持”直接理解成“复杂多 profile 混合器”。

## 当前系统已经支持什么

当前架构对组合题材已经具备 4 个关键支点：

### 1. 主桶层

当前系统已把 `content_bucket` / `genre_profile.bucket` 作为番茄主桶入口。

这层已经被：

- `novel-genre`
- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-package`

共同消费。

### 2. tagpack 叠加层

当前系统已接受 `tagpack` 作为主桶上的第二层 overlay，而不是新的主桶。

已存在的文档约定已经明确：

- `tagpack` 只能叠加
- 不应篡位主桶
- 应优先匹配 `base_bucket`

### 3. 群像 / 多线 / 反脸谱化层

当前系统已经有稳定的“群像、多阵营、多角色独立性”规则承载层：

- `docs/anti-flattening-framework/`
- `docs/opening-and-plot-framework/04-剧情层次模型.md`
- `docs/writing-core-framework/04-剧情层次与多线编排接口.md`

因此，“多角色群像”本身并不是缺失能力，而是缺少一个更明确的 project-facing 声明位置。

### 4. 起盘协议层

当前 `launch-stack` 已能处理：

- premise
- pivot
- launch grammar
- retention protocol

它已经能覆盖“前 1-3 章靠什么起盘、靠什么留人”的早期组合判断。

## 当前还缺什么

当前缺的不是“能不能写组合题材”，而是“组合题材在运行时应该放哪、怎么被下游统一消费”。

最主要的缺口有 4 个：

### 1. 缺 project-facing 组合声明 contract

当前 `state.genre_profile` 主要稳定承载：

- `loaded`
- `节奏`
- `爽点密度`
- `strand权重`
- `特殊约束`
- `bucket`

但没有一个稳定位置承载：

- `tagpacks[]`
- `narrative_modes[]`
- `tone_guardrails[]`
- `strong_tags[]`

### 2. 缺 consumer 统一读法

虽然 `tagpack` 已出现在多个 skill 的输入中，但更多还是：

- 用户显式传入
- skill 局部读取文档后临时消费

还没有把“组合题材定位”统一成一个 project-level 可持续读取对象。

### 3. `launch-stack` 第一版仍偏早期

设计稿中规划了：

- `Genre Obligations Layer`
- `Scene Engine Layer`

但第一版落地仍以开篇到黄金三章为主，还没有自然承载“副本式多主题推进”或“长期群像编排模式”的 project-level 声明。

### 4. 缺“结构模式”和“风味护栏”的分层

像下面这些词不应被混当成同一级题材：

- `多主题副本`
- `多角色群像`
- `搞笑轻松`
- `非套路`
- `非无脑爽`

它们更适合分别进入：

- 结构模式
- 叙事模式
- 语气/风味护栏

## 不推荐的方案

### 1. 不推荐现在直接做多主桶并列

不建议把项目直接建模成：

- `科幻末世 + 穿越 + 末世 + 大佬 + 搞笑轻松`

这类多个同级 `bucket`

原因：

- 番茄前台公开组织方式本来就不是多个主桶并列
- 当前本项目自己的规则也更偏：
  - `主 profile`
  - `主 content_bucket`
  - `2~4 个强标签`
- 多主桶并列会立刻带来：
  - 冲突裁决
  - 优先级矩阵膨胀
  - consumer 不确定性

### 2. 不推荐现在直接做多 profile merge

不建议现在引入：

- 多 profile 混算
- 多 profile 权重融合
- profile orchestration runtime

原因：

- 当前 `A4` 刚完成的是统一 profile 入口
- 不是 profile 混合器
- 过早引入混合层会直接破坏当前刚收紧的 consumer contract

### 3. 不推荐把所有组合卖点塞进 `state.json`

不建议把大量说明性文本直接写进 `state.json`。

当前项目已经多次收敛出的稳定原则仍然应该保留：

- `state` 只保轻量镜像
- 详细分析进 sidecar

## 推荐的最小运行时模型

推荐采用：

- `主 profile`
- `主 bucket`
- `强标签 / tagpack`
- `结构模式`
- `风味护栏`

而不是：

- 多主桶
- 多 profile 并列

### A. `state.json` 轻量镜像

建议只在 `state` 的轻量区保留最小可消费字段。

建议新增或明确允许的轻字段：

```json
{
  "genre_profile": {
    "loaded": "shared/profiles/...",
    "bucket": "科幻末世",
    "tagpacks": ["穿越生存", "供应商流"],
    "strong_tags": ["末世", "大佬"],
    "narrative_modes": ["多主题副本", "多角色群像"],
    "tone_guardrails": ["搞笑轻松", "非套路", "非无脑爽"]
  }
}
```

说明：

- `bucket` 仍然是主桶
- `tagpacks` 用于主桶上的玩法 overlay
- `strong_tags` 记录平台表层标签
- `narrative_modes` 记录结构模式
- `tone_guardrails` 记录风味与质量护栏

### B. sidecar 承载详细编译结果

建议把更详细的组合解释放到单独 sidecar，而不是塞回 `state`。

建议 sidecar 名称：

- `.mighty/content-positioning.json`

建议职责：

- 记录组合定位的完整解释
- 记录主桶为何这样选
- 记录哪些标签只作为风味，哪些进入实际 consumer 约束
- 给下游 skill 输出压缩消费结果

建议形态：

```json
{
  "version": "1.0",
  "primary_profile": "urban-brainhole",
  "primary_bucket": "科幻末世",
  "tagpacks": [],
  "strong_tags": ["穿越", "末世", "大佬"],
  "narrative_modes": ["多主题副本", "多角色群像"],
  "tone_guardrails": ["搞笑轻松", "非套路", "非无脑爽"],
  "compiler_output": {
    "outline_overlays": [],
    "write_overlays": [],
    "review_lenses": [],
    "package_cues": []
  }
}
```

## 推荐的 consumer 消费顺序

后续统一消费时，建议始终按这个顺序：

1. canon / outline / state 真值
2. `primary_profile`
3. `primary_bucket`
4. `tagpacks`
5. `narrative_modes`
6. `tone_guardrails`

这个顺序的意思是：

- 结构真值优先
- 主桶优先于玩法
- 玩法优先于结构模式修饰
- 风味护栏最后收口

## 对各 consumer 的最小接线建议

### `novel-genre`

职责：

- 负责写入和展示项目当前的组合定位
- 不负责直接生成正文约束细节

后续最小新增：

- `show` 时展示：
  - 主桶
  - tagpacks
  - narrative modes
  - tone guardrails
- `apply` 时允许更新这几组轻字段

### `novel-outline`

职责：

- 把组合定位转成结构约束

后续最小新增：

- `narrative_modes` 影响：
  - 章纲层的主线 / 次线 / 副本切换说明
  - 群像章节的 active mover / defender / 独立议程
- `tone_guardrails` 影响：
  - 是否允许过度苦大仇深
  - 是否允许套路化强压后无换账

### `novel-write`

职责：

- 把组合定位转成正文执行护栏

后续最小新增：

- `narrative_modes` 影响：
  - 副本切换时是否保持主入口
  - 群像是否仍有交易单元而不散
- `tone_guardrails` 影响：
  - 轻松不等于无代价
  - 非套路不等于反套路而反套路
  - 非无脑爽不等于完全取消兑现

### `novel-review`

职责：

- 把组合定位转成审查视角

后续最小新增：

- 检查“标签成立但主桶跑偏”
- 检查“群像存在但主入口消失”
- 检查“副本切换过快导致承诺漂移”
- 检查“轻松风味把代价链冲没了”

### `novel-package`

职责：

- 把组合定位转成包装提示，而不是把所有标签都塞进标题

后续最小新增：

- 明确哪些标签适合上首屏
- 明确哪些只能留在简介第二层
- 明确哪些只该作为 package guardrail，不应直接外显

## 推荐的 Phase 3 接入顺序

后续真正实现时，建议按下面顺序进入 Phase 3，而不是一次全铺：

### Step 1

先补 `state-schema` / `state template` / sidecar contract。

目标：

- 先有稳定对象
- 再让 consumer 读它

### Step 2

先接 `novel-genre` 与 `novel-package`。

原因：

- 这两者最接近 project-facing 声明层
- 改动风险比 `write / review` 小

### Step 3

再接 `novel-outline`。

原因：

- 大纲是结构约束的最好入口
- 能先把组合定位转成章纲 law

### Step 4

最后接 `novel-write` 与 `novel-review`。

原因：

- 这两者最容易把组合定位写成过重规则
- 放到最后更容易守住边界

## 与 `B3` / `C2` 的关系

### 与 `B3. launch-stack auto-compile` 的关系

这份组合题材 support 不是 `launch-stack` 的替代。

更合适的关系是：

- `launch-stack` 继续处理前 1-3 章的起盘与留存
- `content-positioning` 处理 project-level 的组合定位

后续可选接法：

- `launch-stack` 读取 `narrative_modes` / `tone_guardrails`
- 但不必要求它第一版就吸收全部组合解释

### 与 `C2. bucket 与题材映射校准` 的关系

这份说明本质上是 `C2` 的前置输入。

`C2` 后续要解决的是：

- 哪些 tagpack 稳定存在
- 哪些强标签只是包装层标签
- 哪些 `narrative_modes` 真的值得做成平台级组合模式

因此，当前先定义字段和边界是合理的；具体映射的市场校准应晚于这一步。

## 非目标

当前明确不做：

- 多主桶并列引擎
- 多 profile 权重融合
- 把所有组合词都做成 first-class bucket
- 新造 monolithic runtime
- 在当前 A4 已收口写集上直接追加未校准实现

## 一句话结论

当前最稳的组合题材支持路径不是：

- “去网上找一个成熟大方案整体替换”

而是：

- 在现有 `主 profile + 主 bucket + tagpack + 群像/多线规则 + launch-stack` 架构上，
- 补一层轻量 `content-positioning` contract，
- 并在后续 Phase 3 按 `genre/package -> outline -> write/review` 的顺序接入。
