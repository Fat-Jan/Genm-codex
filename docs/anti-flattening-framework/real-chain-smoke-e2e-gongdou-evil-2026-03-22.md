# 反脸谱化体系真实链路 Smoke

日期：2026-03-22

## 目标

在一个隔离副本上，真实走一遍：

- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-fix`
- `novel-precheck`

验证反脸谱化规则不是只存在于文档和 skill 文案里，而是能落到样本项目产物与 state 信号中。

## 使用样本

- 底本：`smoke/e2e-gongdou-evil`
- 隔离副本：`smoke/e2e-gongdou-evil-antiflattening-20260322`

这样可以保证：

- 不污染现有 smoke 样本
- 仍使用项目内真实题材、真实 state、真实目录结构

## 执行顺序

### 1. Outline

新增：

- `smoke/e2e-gongdou-evil-antiflattening-20260322/大纲/章纲/第007章.md`

本次章纲明确写入了：

- 主动方 / 防守方
- 关键误判
- 独立议程
- 关系残账
- 阵营分歧

这一步验证了 `novel-outline` 侧的新规则不只是抽象原则，而是能落成章纲字段。

### 2. Write

新增：

- `smoke/e2e-gongdou-evil-antiflattening-20260322/chapters/第007章.md`

并更新：

- `smoke/e2e-gongdou-evil-antiflattening-20260322/.mighty/state.json`

写作结果要点：

- 第 7 章把“翻窗婆子 -> 冯忠 -> 佛堂匣角 -> 天亮前抢账”这条线接了起来
- 支持者没有写成单声道：
  - 族叔支持继续查，是为了先保族面
  - 二房老婶愿意封门，是为了切割二房，不是为了替谢云昭撑腰
- 对立面也不是纯纸片：
  - 赵婆子怕的是儿子契书
  - 冯忠靠“最干净的手”这一位置挡刀
  - 伯爷护的不是一句体面，而是整条男人线

### 3. Review

真实写回：

- `chapter_meta["7"].review_score = 82`
- `chapter_meta["7"].recommended_next_action = "novel-fix"`
- `chapter_meta["7"].anti_flattening_flags`
- `chapter_meta["7"].anti_flattening_summary`

本轮 review 判断：

- **通过点**
  - 赵婆子、族叔、二房老婶、冯忠都有各自议程
  - 群像没有塌成纯功能位
  - 本章胜利是“锁定范围”，不是“直接全赢”
- **主要问题**
  - 正文字数超出桶和章纲规划
  - 主角前半章的信息命中率偏高，来源提示略虚
  - 佛堂高潮的对立面反制偏弱

这说明反脸谱化 review 维度确实能产出和原质量维度不同的判断。

### 4. Fix

局部修补后，真实写回：

- `chapter_meta["7"].last_fix_time`
- `chapter_meta["7"].fix_count = 2`
- `chapter_meta["7"].fixed_issues`
- `chapter_meta["7"].fix_reason`

本轮 fix 分两次完成：

- 补了谢云昭为什么会把怀疑落到“赵婆子儿子契书 / 钥匙房差事”这层
- 补了佛堂门前伯爷、冯忠、族叔、二房老婶的即时反制和切割动作
- 第二轮把第 7 章从 `6012` 字压到 `3071` 字，去掉了夜审和佛堂段的重复说明

本轮 fix **没有**做的是：

- 没有重写章节功能
- 没有改事件顺序

这符合 `novel-fix` 的定位：局部修，不偷渡重写。

### 5. Re-review

第二轮 fix 后，手工按同一 review 契约复审，真实写回：

- `chapter_meta["7"].review_score = 88`
- `chapter_meta["7"].recommended_next_action = "novel-write"`
- `chapter_meta["7"].anti_flattening_flags = []`

复审后的判断：

- 长度已经回到章纲区间
- 主角信息来源已落地
- 佛堂段的对立面反制已成立
- 主要剩下的是后续章节要继续维持族叔 / 二房老婶的分歧，不让支持者重新滑回单声道

### 6. Precheck

这一环分两次判断。

#### 第一轮预检结论

- `overall readiness`: `revise-then-submit`
- `packaging-needs-update`: `no`

#### 必须修复

- 第 7 章字数明显高于当前桶和章纲规划，投稿前需要再压一轮
- 第 7 章虽然经过 fix，但还没有新一轮 review 覆盖

#### 建议修复

- 继续压偏厅夜审的重复判断句
- 再收紧佛堂段的冲门、对峙、见空缝之间的节奏

#### 反脸谱化判断

- **正面**
  - 主角没有靠“所有人都自动支持我”推进
  - 族叔、二房老婶、赵婆子、冯忠各自站在不同成本线上
  - 本章赢的是范围，不是答案，残账和风险都留住了
- **风险**
  - 主角视角仍然偏强，一旦后续继续由她一人命名和判断所有人，群像会重新往“主角吞世界”滑

#### 第二轮预检结论

在第二轮压章和复审后，这条链已经可以给出：

- `overall readiness`: `ready-now`
- `packaging-needs-update`: `no`

原因：

- 第 7 章字数已压回合理区间
- review 覆盖已刷新
- 反脸谱化风险由“当前问题”降为“后续维护提醒”

## 关键证据

### 结构证据

- 新章纲已把反脸谱化字段写实
- 新章节已体现群像分歧和关系残账

### state 证据

`chapter_meta["7"]` 已有：

- `recommended_next_action`
- `anti_flattening_flags`
- `anti_flattening_summary`
- `fixed_issues`
- 第二轮复审后的更高分和更轻的风险状态

### 工作流证据

这条链已经证明：

1. 反脸谱化规则可以进入 outline
2. 可以影响正文写法
3. 可以在 review 中形成结构诊断
4. 可以在 fix 中转成局部动作
5. 可以在 precheck 中变成投稿前风险判断
6. 还能在第二轮修订后把 `revise-then-submit` 推到 `ready-now`

## 结论

这轮真实链路 smoke 足以确认：

- 反脸谱化体系不再只是方法论文档
- 它已经能落到项目副本的章纲、正文、state 与投稿前判断里
- `novel-outline -> novel-write -> novel-review -> novel-fix -> novel-precheck` 这条主链，已经具备反脸谱化约束的最小可用闭环

当前仍保留的现实问题也很清楚：

- 写作侧后续仍要更稳地控制章节长度，避免每次都靠 fix 回压
- 反脸谱化最大的风险不再在本章，而在后续是否还能维持支持者之间的不同算盘

但这些都属于下一轮打磨问题，不再是“这套规则能不能落地”的问题。
