# Content Positioning Smoke 2026-03-26

## 目的

验证 `content-positioning` 在三类样本上的当前表现：

1. 正向职场婚恋样本
2. 正向都市脑洞样本
3. 边界样本（bucket 不稳定）

本轮 smoke 在临时副本上执行，不直接改真实项目目录。

## 样本

### 1. `projects/代理续约那天，我和前搭档被公司按进了同一套合租房`

- 当前结果：
  - `primary_bucket = 职场婚恋`
  - `primary_profile = ""`
  - `strong_tags = ["先婚后爱", "办公室暧昧"]`
  - `narrative_modes = ["双线并进"]`
  - `tone_guardrails = ["职场不能悬浮", "感情线与事业线不能割裂"]`
- 说明：
  - 当前 bucket-only fallback 已可工作
  - 说明 `content-positioning` 不再只服务“主 profile 已稳定”的项目

### 2. `projects/公司裁我那天，系统先赔了我一百万`

- 当前结果：
  - `primary_profile = urban-brainhole`
  - `primary_bucket = 都市脑洞`
  - `strong_tags = ["系统", "逆袭"]`
  - `narrative_modes = ["多主题副本"]`
  - `tone_guardrails = ["节奏不能拖沓", "金手指不能替代逻辑"]`
- 说明：
  - 当前 contract 在“主 profile 已稳定”的样本上表现正常
  - `write / review / package` 现在已经可以吃到这组 overlay

### 3. `smoke/e2e-system-antiflattening-20260322`

- 当前结果：
  - `primary_profile = ""`
  - `primary_bucket = ""`
  - overlays 全空
- 说明：
  - 这是当前预期内的保守结果
  - 这条线用于验证：
    - 当 bucket 不稳定时，系统不会胡乱补定位
  - 也说明后续如果要支持这类边界项目，还要继续扩：
    - bucket fallback
    - narrative/tone only mode

## 当前结论

- `content-positioning` 对“主 profile 稳定”的项目已经可用
- 对“只有 bucket / 没有稳定 loaded profile”的项目，bucket-only fallback 现在也已可用
- 边界样本（无 profile、无 bucket）当前仍保持保守空输出，这符合当前 contract
