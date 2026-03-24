# Fanqie 规则优先级矩阵

## 目的

这份文档回答一个实操问题：

- 当 `Fanqie-first` 相关规则越来越多时，
- `core constraints`、`bucket`、`技巧规则`、`tagpack` 到底谁优先？
- 如果它们看起来有冲突，该按什么顺序裁决？

这份矩阵的目的就是：

- **防止后续技能接规则时互相打架**

---

## 最终优先级

从高到低，统一按下面顺序执行：

### 1. 硬约束层

包括：

- 大纲
- 设定
- `.mighty/state.json`
- [core-constraints.md](/Users/arm/Desktop/vscode/Genm-codex/shared/references/shared/core-constraints.md)

一句话：

- **先解决“写什么不能错”**

### 2. Fanqie 内容桶层

包括：

- [fanqie-bucket-constraints.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-bucket-constraints.md)
- [fanqie-mvp-buckets.yaml](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-mvp-buckets.yaml)

一句话：

- **再解决“这个桶要求什么”**

### 3. Fanqie 写作技巧层

包括：

- [fanqie-writing-techniques.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-writing-techniques.md)
- [fanqie-writer-zone-lessons.md](/Users/arm/Desktop/vscode/Genm-codex/docs/research/fanqie/fanqie-writer-zone-lessons.md)

一句话：

- **再优化“怎么写得更像番茄会推的内容”**

### 4. Fanqie tagpack 叠加层

包括：

- [fanqie-mvp-tagpacks.yaml](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-mvp-tagpacks.yaml)

一句话：

- **最后处理“同一个桶里，你要往哪种玩法上偏”**

---

## 为什么这么排

### 硬约束不能被覆盖

例如：

- 大纲写了婚书局
- 你就不能因为某篇写作技巧文章说“反转越快越好”，就改成别的故事

同理：

- 设定、state、已有证据链
- 都不该被平台技巧规则推翻

### 桶规则比技巧规则更靠前

因为：

- 桶规则回答的是：
  - 你在写什么消费桶
- 技巧规则回答的是：
  - 这个桶里怎么写得更像样

所以：

- **先选桶，再用技巧优化桶**

### tagpack 只能叠加，不能篡位

例如：

- `恶女 x 宫斗宅斗`

这里：

- 主桶仍然是 `宫斗宅斗`
- `恶女` 只是第二层玩法

不能因为 `恶女` 的某条规则更刺激，就把主桶写歪。

---

## 常见“软冲突”怎么处理

### 1. 人物要更丰富 vs 去 AI 味、少解释

现象：

- 写作技巧鼓励：
  - 回忆
  - 动作
  - 神态
  - 成长过程
- 核心约束又要求：
  - 少解释
  - 少空泛回忆
  - 去 AI 味

裁决：

- 允许增加人物细节
- 但必须满足：
  - 服务当前冲突
  - 服务人物动机
  - 不写成解释性长段

结论：

- **可以更细，但不能更啰嗦**

### 2. 标题更点击 vs 题文一致

现象：

- 技巧规则会推：
  - 关系词
  - 爆点词
  - 高点击表达
- 但包装层又要求：
  - 不过度承诺
  - 题文一致

裁决：

- `package` 可以更点击
- `precheck` 负责拦：
  - 过度标题党
  - 题文偏移

结论：

- **允许点击化，但不允许骗点击**

### 3. 短故事技巧 vs 长篇桶规则

现象：

- 作者专区里很多公开技巧来自短故事或通用教程
- 当前系统里既有长篇桶，也有短篇桶

裁决：

- 短故事规则只能当：
  - 强钩子参考
  - 节奏参考
- 不能直接变成长篇硬规则

结论：

- **短篇技巧可借鉴，不能机械照搬**

### 4. bucket 与 tagpack 方向拉扯

现象：

- `现言甜宠` 要甜点和关系绑定
- `恶女` 又会拉高危险感和控制感

裁决：

- 先保主桶可读性
- 再保 tagpack 风味

结论：

- **主桶优先，tagpack 后置**

---

## 给技能的直接用法

### `novel-package`

按顺序读：

1. 大纲 / state / canon
2. bucket
3. 写作技巧里的标题 / 简介规则
4. tagpack 的标题 / 简介增强点

### `novel-outline`

按顺序读：

1. 大纲法与 state
2. bucket 的开头 / payoff / ending_hook
3. 写作技巧里的黄金三章 / 悬念接力
4. tagpack 的 opening_rule / payoff_rule

### `novel-write`

按顺序读：

1. 当前章纲
2. bucket 的 reader motive / payoff_cycle
3. 写作技巧里的人物活人感、冲突与节奏
4. tagpack 的 protagonist_core / reader_motive

### `novel-review`

按顺序判：

1. 是否违反大纲 / state / canon
2. 是否偏离 bucket
3. 是否有写作技巧层的明显问题
4. 是否没有吃到 tagpack 的增强点

### `novel-precheck`

按顺序判：

1. 题文是否一致、是否违背 canon
2. 是否真正适配这个 bucket
3. 是否达到了番茄技巧层要求的开头和前三章
4. tagpack 有没有成立

---

## 一句话版本

可以把它记成：

- **先别写错**
- **再写对桶**
- **再写得更会转化**
- **最后再加玩法风味**

对应就是：

1. 硬约束
2. bucket
3. 技巧
4. tagpack

---

## 最终结论

目前这些新加的 Fanqie 写作技巧规则：

- **不是新的硬法律**
- **而是第三优先级的优化器**

所以它们不会推翻现有体系。

更准确地说，它们会：

- 强化现有 Fanqie-first 路线
- 补足标题、开头、黄金三章、人物和节奏层
- 帮后续技能更稳定地朝“番茄会推、读者会追”的方向收敛
