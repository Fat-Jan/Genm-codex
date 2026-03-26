# Profile 内容校准与 Bucket 映射口径

## 目的

这份文档把 `v1.1` Phase 4 的外部资料校准结果收成当前有效口径，回答两个问题：

1. `profile` 内容层现在最该承载什么
2. `bucket / strong_tags / narrative_modes / tone_guardrails` 之间当前怎么分工

## 校准资料来源

本轮优先采用番茄官方作者侧资料：

1. 零基础写作速览：新手如何写一个好故事  
   `https://fanqienovel.com/writer/zone/article/7407742604059623448`
2. 新手写作五大避雷针｜让你的故事瞬间“上头”  
   `https://fanqienovel.com/writer/zone/article/7511925003550457881`
3. 封面简介双剑合璧，作品突围在此一举！  
   `https://fanqienovel.com/writer/zone/article/7480101551080489022`
4. 一份使用指南，带你玩转作家帮助中心  
   `https://fanqienovel.com/writer/zone/article/7193632690657034297`

## 校准后对 `profile` 的结论

### 1. `profile` 核心应优先承载“题材基础约束”

当前最值得稳定保留在 core profile 的内容：

- 题材名 / 描述
- 节奏参数
- 爽点密度与间隔
- strand 权重
- 特殊约束
- 读者期待
- taboo / 避雷项

原因：

- 官方资料持续强调：
  - 题材选择
  - 主角身份与特点
  - 主角目标
  - 冲突与对抗
  - 开篇与简介的核心梗/核心冲突
- 这说明 profile 的本体更像：
  - 题材基础配置
  - 而不是大段创作教材集合

### 2. `profile` 不应继续膨胀成长篇素材包

以下内容不应继续被当作 core contract：

- 大段 `dialogue_templates`
- 大段 `scene_description`
- 长篇示例文本

这些内容当前可继续作为 legacy reference 存在，但不再视为 authoritative core config。

### 3. `profile` 需要让“题材可见性”更强

结合官方资料，当前 profile 内容层应更重视：

- 主题材可读性
- 主冲突可读性
- 读者为什么点开
- 读者为什么继续读

这意味着后续 profile 内容升级时，应优先补：

- `opening / hook` 偏好
- `payoff cadence`
- `reader motive`
- `packaging-safe cues`

而不是优先扩对白范例。

## 校准后对 `bucket` 映射的结论

### 1. 当前仍坚持“单主桶”

当前不采用：

- 多主桶并列
- 多 profile 并列

当前采用：

- 一个 `primary_bucket`
- 若干 `strong_tags`
- 若干 `tagpacks`
- 若干 `narrative_modes`
- 若干 `tone_guardrails`

原因：

- 官方平台前台对作品更像：
  - 主分类
  - 页面标签
  - 简介里的结构卖点
- 而不是多个同级主桶并列

### 2. 这几层的职责现在这样分

#### `bucket`

- 主内容桶
- 最先决定读者预期和主线包装方向

#### `strong_tags`

- 平台表层可见标签
- 用于补充主桶，不篡位主桶

#### `tagpacks`

- 主桶上的玩法 overlay
- 仍保持 `base_bucket` 优先

#### `narrative_modes`

- 结构模式
- 例如：
  - `多主题副本`
  - `多角色群像`

#### `tone_guardrails`

- 风味与质量护栏
- 例如：
  - `搞笑轻松`
  - `非套路`
  - `非无脑爽`

## 当前已落地的映射文件

本轮已把第一批映射实改为机器文件：

- `shared/templates/content-positioning-map-v1.json`

当前首批已落地的 profile / platform 映射为：

- `palace-intrigue` / `fanqie`
- `realistic` / `fanqie`
- `xuanhuan` / `fanqie`

对应的 profile 内容字段也已补入：

- `shared/profiles/palace-intrigue/profile.yaml`
- `shared/profiles/realistic/profile.yaml`
- `shared/profiles/xuanhuan/profile-tomato.yaml`

这批映射现在主要服务：

- `content-positioning` sidecar 默认值
- 第一批组合题材 / bucket / tone guardrail 的稳定消费

说明：

- 这仍然是**首批优先 profile** 的实改，不表示所有 profile 已逐一完成同等级校准
- 当前已经足够支撑：
  - 单主桶
  - `strong_tags`
  - `tagpacks`
  - `narrative_modes`
  - `tone_guardrails`
  的实际系统接线

## 对 consumer 的校准口径

### `novel-package`

官方资料明确说明：

- 书名要让读者快速知道题材和主题
- 简介要：
  - 首行点核心梗
  - 冲突开场
  - 300 字内讲主线和人设亮点
  - 结尾留钩

因此包装层当前应优先：

1. 主桶可见
2. 主冲突可见
3. 只在必要时加一个 `strong_tag`
4. `tone_guardrails` 主要做 package-risk filter，而不是都上标题

### `novel-outline`

官方资料强调：

- 先确定题材
- 先确定主角身份
- 先确定目标
- 先确定冲突

因此 outline 层当前应：

- 继续以 `bucket` 决定主 promise
- 用 `narrative_modes` 约束多线和群像
- 用 `tone_guardrails` 防止风味漂移

### `novel-write / novel-review`

官方资料对“避雷”的强调说明：

- 标签成立，不等于执行成立
- 轻松风味不应冲掉代价链
- 简介和正文不能错位

因此：

- `strong_tags` 不能替代主桶
- `narrative_modes` 不能吃掉主入口
- `tone_guardrails` 不能把兑现感和代价感冲没

## 当前映射优先级

后续 consumer 统一消费时，继续保持：

1. canon / outline / state 真值
2. `primary_profile`
3. `primary_bucket`
4. `tagpacks`
5. `narrative_modes`
6. `tone_guardrails`

补充：

- `strong_tags` 是主桶之后的包装/提示增强层
- 不应与 `primary_bucket` 同级竞争

## 当前不做的事

- 不把外部资料直接改写成多主桶引擎
- 不把所有平台表层标签都升成 first-class bucket
- 不把所有风味词直接写进 profile core schema
- 不把包装文章里的技巧直接抄成 raw profile 大段文本

## 一句话结论

当前校准后，`Genm-codex` 对组合题材与平台定位的稳定理解应是：

- `主 profile + 主 bucket + strong_tags + tagpacks + narrative_modes + tone_guardrails`

而不是：

- 多 profile 并列
- 多主桶并列
