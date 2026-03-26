# Genm-codex 质量闭环整合设计

## 目标

把当前已经存在的高价值写作 skill，整合成一个更一致的质量闭环：

- `novel-write`
- `novel-review`
- `novel-fix`
- `novel-polish`
- `novel-rewrite`
- `novel-precheck`
- `novel-learn`

这份设计先解决“指标和衔接”，不先解决“再造新命令”。

---

## 当前问题

### 1. 质量口径分散

当前不同 skill 会看这些问题：

- AI 痕迹
- 节奏
- 爽点
- 连续性
- 追读力
- 平台适配

但它们没有完全统一到同一套可复用指标。

### 2. 修复路径不够明确

现在虽然已经有：

- `review`
- `fix`
- `polish`
- `rewrite`
- `precheck`

但不同问题到底走哪条修复路径，还没有完全收紧。

### 3. 学习回写没有真正闭环

`novel-learn` 已经存在，但目前还没有明确要求这些 learned signals 在：

- `write`
- `polish`
- `precheck`

里怎样优先生效。

---

## 统一质量模型

建议把当前写作质量统一成这 7 个主维度：

1. **hook_strength**
   - 开篇钩子速度
   - 章末钩子强度
   - 追读牵引

2. **payoff_density**
   - 爽点兑现密度
   - 小回报节奏

3. **continuity**
   - 角色状态连续性
   - 世界观与战力连续性
   - 伏笔衔接

4. **platform_fit**
   - 平台文风
   - 平台节奏
   - 平台偏好匹配

5. **anti_ai_risk**
   - 解释替代展示
   - 泛化句式
   - 对称/模板化表达
   - 无效填充

6. **prose_control**
   - 语言力度
   - 场景清晰度
   - 对话有效性

7. **reader_pull**
   - 章节内驱动力
   - 下一章欲望

---

## Skill 角色分工

### `novel-write`

职责：

- 按当前 state 和 outline 生成正文
- 吃 genre / platform 约束
- 在后续版本中，显式吃 `learned_patterns`

不负责：

- 自己给自己打 review 分
- 假装已经完成投稿前质量检查

### `novel-review`

职责：

- 输出统一质量模型下的问题与优势
- 明确哪些属于：
  - `fix`
  - `polish`
  - `rewrite`

### `novel-fix`

适用：

- 明确、局部、目标清晰的问题

例如：

- 某几段解释过重
- 某处 hook 不够强
- 某条 review issue 可局部修正

### `novel-polish`

适用：

- 不改结构，只改语言层质量

例如：

- 去 AI 味
- 节奏微调
- 对话更自然
- 描写更稳

### `novel-rewrite`

适用：

- 结构级重做
- 情节顺序或章节功能需要明显重建

### `novel-precheck`

职责：

- 投稿前最终门
- 汇总：
  - 平台适配
  - 已知 review 覆盖
  - AI 风险
  - 当前 readiness

### `novel-learn`

职责：

- 从局部章节或用户样本中学偏好
- 只保守更新：
  - `writing_style_preferences`
  - `high_point_preferences`
  - `avoid_patterns`

后续应反哺：

- `write`
- `polish`
- `precheck`

---

## 建议的修复路由

### 路由 1：局部问题

`review -> fix`

适用：

- 问题小
- 不需要改结构

### 路由 2：语言问题

`review -> polish`

适用：

- AI 味
- 表达钝
- 节奏松
- 描写弱

### 路由 3：结构问题

`review -> rewrite`

适用：

- 章节功能错误
- 情节顺序失效
- 爽点/钩子失灵且需要重构

### 路由 4：投稿前总检

`write/rewrite -> review -> fix/polish/rewrite -> precheck`

这是建议收紧成默认的高质量投稿链。

---

## 第一轮整合建议

### P0

- 不改命令数量
- 不造新质量中心文件
- 先统一文档与 skill 里的质量口径

### P1

- 让 `review` 明确输出“推荐路由”
- 让 `precheck` 明确引用已有 review 覆盖度
- 让 `learn` 的 `avoid_patterns` 和 `high_point_preferences` 在 `write/polish` 中被显式读取

### P2

- 视效果决定是否补一个统一质量摘要字段到 state
- 但不要过早把 state 变成复杂评分数据库

---

## 结论

当前真正缺的，不是更多写作命令，而是：

- 统一的质量指标语言
- 更清晰的修复路由
- `learn` 对写作链的真实反哺

所以质量闭环整合应该作为第九阶段并行线推进，而不是继续放在后面无限延迟。
