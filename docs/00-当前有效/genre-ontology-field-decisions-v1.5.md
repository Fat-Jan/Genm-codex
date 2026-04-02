# 题材本体字段上升决策 (`v1.5`)

## 目的

这份文档是**题材本体字段上升决策**的权威来源。它定义哪些 profile 字段可以被视为"题材本体"（跨平台共识），哪些必须保留为"平台特化"（平台特定实现）。

**读取此文档可以知道：**
- 哪些字段可以上升为题材本体
- 哪些字段必须保留在平台特化层
- 为什么这样决定

---

## 字段分类框架

### 第一层：可上升为题材本体

| 字段类型 | 示例 | 为什么可以上升 |
|---------|------|---------------|
| `strong_tags` 中的高层题材标签 | `穿越`、`权谋`、`系统` | 这些标签跨平台成立，不是番茄特有 |
| `strong_tags` 中的基本关系/冲突类型 | `高门关系`、`婚配错位` | 这类关系在晋江/起点/番茄都成立 |
| `tone_guardrails` 中的高层冲突约束 | `历史感不能散`、`系统奖励不能替代成长` | 这类约束跨平台共识强 |

### 第二层：暂不直接上升

| 字段类型 | 示例 | 为什么不能上升 |
|---------|------|---------------|
| `package_cues` | `首屏点心动事件`、`前三章要有硬兑现` | 这些是番茄消费链的包装约束 |
| 首屏/前三章兑现节奏 | `开篇300字内必须交代主线` | 这是番茄平台的包装偏好 |
| 明显绑定番茄消费链的包装约束 | `金手指出现前置` | 这是番茄的消费习惯，不是题材本体 |

---

## 逐 profile 决策

### `palace-intrigue` (宫斗宅斗)

**可上升为题材本体：**
- `strong_tags`: `高门关系`、`婚配错位`
- `tone_guardrails`: `强压后必须换账`

**暂不直接上升：**
- `package_cues`
- 番茄式首屏推进节奏要求

---

### `historical-brainhole` (历史脑洞)

**可上升为题材本体：**
- `strong_tags`: `穿越`、`权谋`
- `tone_guardrails`: `历史感不能散`、`创意设定必须自洽`

**暂不直接上升：**
- `package_cues`
- 番茄偏好的"一句话讲清主设定"式包装要求

---

### `realistic` (现实题材)

**可上升为题材本体：**
- `strong_tags`: `现实困局`、`成长`
- `tone_guardrails`: `现实代价不能消失`、`治愈不等于无后果`

**暂不直接上升：**
- `package_cues`
- 开篇 300 字内必须交代主线这类平台包装约束

---

### `urban-brainhole` (都市脑洞)

**可上升为题材本体：**
- `strong_tags`: `系统`、`逆袭`
- `tone_guardrails`: `系统奖励不能替代成长`

**暂不直接上升：**
- `package_cues`
- 番茄式首屏推进节奏要求

---

### `mystery-brainhole` (悬疑脑洞)

**可上升为题材本体：**
- `strong_tags`: `脑洞解谜`、`惊喜反转`
- `tone_guardrails`: `创意设定要自洽`

**暂不直接上升：**
- `package_cues`
- 番茄式首屏推进节奏要求

---

## 决策原则

### 为什么 `package_cues` 不能上升？

`package_cues` 是**番茄消费链的包装约束**，不是题材本体。例如：
- `首屏点心动事件` → 这是番茄的消费习惯
- `前三章要有硬兑现` → 这是番茄的节奏偏好

这些约束在起点/晋江/阅文上可能完全不成立。因此不能上升为题材本体。

### 为什么 `strong_tags` 可以上升？

`strong_tags` 中的高层题材标签（如 `穿越`、`权谋`、`系统`）是**跨平台共识**。例如：
- `穿越` → 起点/晋江/番茄都承认这个题材
- `权谋` → 三个平台都有这个分类
- `系统` → 三个平台都有这个流派

这些标签不是番茄特有，而是题材本体。

### 为什么 `tone_guardrails` 可以上升？

高层 `tone_guardrails`（如 `历史感不能散`）是**题材共识**，不是平台偏好。例如：
- `历史感不能散` → 起点/晋江/番茄都要求历史题材要有历史感
- `系统奖励不能替代成长` → 三个平台都要求系统流要有成长逻辑

这些约束跨平台成立，可以视为题材本体。

---

## 使用规范

### 新增 profile 时

1. 先检查是否有 `platform_positioning.fanqie`
2. 如果有，按此文档的字段分类框架判断哪些可以上升
3. 将可上升字段写入 core profile
4. 将平台特化字段保留在 bucket overlay 或 platform overlay

### 修改现有 profile 时

1. 检查修改的字段是否属于"可上升"类别
2. 如果是，修改 core profile
3. 如果不是，修改对应的 overlay 文件

---

## 更新记录

- `2026-03-28`: 初始版本，覆盖 `palace-intrigue`、`historical-brainhole`、`realistic`、`urban-brainhole`、`mystery-brainhole` 五个 profile
- 后续每轮交叉压深化应补充更多 profile 的决策

### `ancient-romance`

**名称**: 古言

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `apocalypse`

**名称**: 末世

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `ceo-romance`

**名称**: 豪门总裁

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `cthulhu`

**名称**: 克苏鲁

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `dark`

**名称**: 黑暗题材

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `dark-theme`

**名称**: 黑暗题材

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `dramatic-romance`

**名称**: 狗血言情

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `era`

**名称**: 年代

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `esports`

**名称**: 电竞

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `evil-girl`

**名称**: 恶女题材

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `fantasy-romance`

**名称**: 幻想言情

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `farming`

**名称**: 种田

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `female-mystery`

**名称**: 女频悬疑

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `fertility`

**名称**: 多子多福

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `game-sports`

**名称**: 游戏体育

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `gaowu`

**名称**: 高武

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `historical`

**名称**: 历史古代

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `historical-creative`

**名称**: 历史脑洞

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `infinite-flow`

**名称**: 无限流

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `livestream`

**名称**: 直播文

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `melodrama`

**名称**: 狗血言情

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `modern-brainhole`

**名称**: 现言脑洞

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `modern-creative`

**名称**: 现言脑洞

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `multi-offspring`

**名称**: 多子多福

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `mystery-creative`

**名称**: 悬疑脑洞

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `mystery-horror`

**名称**: 悬疑灵异

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `republic-romance`

**名称**: 民国言情

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `romance`

**名称**: 言情

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `rule-horror`

**名称**: 规则怪谈

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `rule-mystery`

**名称**: 规则怪谈

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `sci-fi`

**名称**: 科幻

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `spy-war`

**名称**: 抗战谍战

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `substitute`

**名称**: 替身文

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `supernatural`

**名称**: 悬疑灵异

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `sweet-romance`

**名称**: 青春甜宠

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `sweet-youth`

**名称**: 青春甜宠

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `system`

**名称**: 系统流

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `urban-creative`

**名称**: 都市脑洞

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `urban-daily`

**名称**: 都市日常

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `urban-life`

**名称**: 都市日常

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `urban-superpower`

**名称**: 都市异能

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `war-spy`

**名称**: 抗战谍战

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `western-fantasy`

**名称**: 西幻

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `workplace-romance`

**名称**: 职场婚恋

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `xiuxian`

**名称**: 修仙

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `xuanhuan`

**名称**: 玄幻

**可上升为题材本体**:

- 已具备跨平台证据，当前可稳定上升为题材本体命名；具体入口见 `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏

---

### `zhihu-short`

**名称**: 知乎短篇

**可上升为题材本体**:

- 专项例外：`zhihu-short` 的题材本体判断应以知乎短篇生态为主来源，不适用默认三平台证据对齐门槛

**暂不直接上升**:

- `package_cues`
- 首屏/前三章兑现节奏
- 番茄 / 起点 / 晋江短篇形态参考

---
