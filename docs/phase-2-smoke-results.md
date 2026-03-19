# Genm-codex 第二阶段 Smoke Results

## 环境

- 项目目录: `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
- 目标: 验证第二阶段已迁入 skill 的最小可用性

---

## 1. `genm-novel-query`

- 首轮结果: fail
- 原因:
  - 首次测试读取到了错误项目上下文，返回了与 `e2e-novel` 不匹配的数据

### 复测

- 提示词:
  硬约束：只允许操作这个项目目录  
  `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

  你必须先明确回显你实际读取的项目根目录。  
  如果不是 `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`，立刻停止，不要继续。

  在确认目录正确后，再使用 genm-novel-query skill，只基于这个项目回答下面三个问题，并且禁止引用其他项目或旧测试样本：

  1. 主角现在什么境界？
  2. 当前有哪些活跃伏笔？
  3. 当前项目进度到第几章、累计多少字？

  要求：
  - 优先读取 `.mighty/state.json`
  - 如果答案和这个 state 文件不一致，要直接说明
  - 不要改动任何文件
- 预期:
  - 主角境界接近：锻体境 / 九重
  - 活跃伏笔至少包含：古镜来历、后山东壁石门
  - 项目进度接近：第 1 章、3152 字
- 实际:
  - 实际操作目录：`/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
  - 主角境界：锻体境九重
  - 活跃伏笔：
    - 古镜来历
    - 后山东壁石门
  - 项目进度：
    - 第1章
    - 3152字
  - 明确说明与 `.mighty/state.json` 一致
  - 未改动任何文件
- 结果: pass（复测通过）
- 备注:
  - 说明该 skill 可用，但调用时应带强目录约束以避免串到旧项目上下文

---

## 2. `genm-novel-status`

- 提示词:
  请先确认你当前读取的项目根目录路径。
  目标项目必须是：
  `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
  只有在确认你读取的是这个项目后，才继续使用 genm-novel-status skill，输出一个简明 dashboard，包含：
  1. 当前章节
  2. 总字数
  3. 主角当前状态
  4. 活跃伏笔
  5. 下一步建议
  如果当前上下文不是这个目录，请先切换到该项目再执行。
- 预期:
  - 明确回显目标项目路径
  - 当前章节接近：第1章
  - 总字数接近：3152
  - 主角状态接近：沈照 / 锻体境九重 / 后山废井
  - 活跃伏笔包含：古镜来历、后山东壁石门
- 实际:
  - 已明确确认项目根目录为 `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
  - 返回 dashboard：
    - 当前章节：第1章
    - 总字数：3152（并额外指出与章节文件字符统计不一致）
    - 主角当前状态：沈照 / 锻体境九重 / 后山废井
    - 活跃伏笔：古镜来历、后山东壁石门
    - 下一步建议：推进第2章并兑现后山东壁伏笔
- 结果: pass
- 备注:
  - 发现了一个潜在一致性问题：状态字数与章节文件字符数统计不一致，后续可单独排查

---

## 3. `genm-novel-character`

- 提示词:
  硬约束：只允许操作这个项目目录  
  `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

  如果你当前上下文不是这个目录，先切换到这个目录，再继续。  
  如果不能确认自己正在读取这个目录，就停止，不要继续。

  在确认目录正确后，再使用 genm-novel-character skill，在这个项目里创建一个新角色：

  姓名：林晚照  
  身份：外门药庐女弟子  
  核心性格：机敏、嘴硬、心软  
  与主角关系：潜在盟友  
  动机：想借外门大比摆脱药庐杂役身份

  要求：
  1. 写入 `设定集/角色/`
  2. 只做最小可用角色卡，不要过度展开
  3. 不改动 `设定集/角色/主角.md`
  4. 完成后只汇报：
     - 你实际操作的项目根目录
     - 新角色文件路径
     - 写入了哪些核心字段
     - 是否改动了 `.mighty/state.json`
- 预期:
  - 正确确认项目根目录
  - 成功创建新角色文件
  - 内容至少包含：姓名、身份、性格、动机、与主角关系
  - 不改动主角文件
  - 最好不改 `state.json`
- 实际:
  - 实际操作目录：`/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
  - 新角色文件：`设定集/角色/林晚照.md`
  - 写入核心字段：姓名、身份、故事定位、核心性格、当前动机、与主角关系、关联说明
  - `.mighty/state.json` 未改动
- 结果: pass
- 备注:
  - 这是一个很干净的只写角色文件的最小通过案例

---

## 4. `genm-novel-setting`

- 提示词:
  硬约束：只允许操作这个项目目录  
  `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

  如果你当前上下文不是这个目录，先切换到这个目录，再继续。  
  如果不能确认自己正在读取这个目录，就停止，不要继续。

  在确认目录正确后，再使用 genm-novel-setting skill，在这个项目里创建一个地点设定：

  `type=location`  
  `action=create`  
  `name=后山东壁石门`

  要求：
  1. 写入 `设定集/地点/`
  2. 只做最小可用设定，不要展开成长篇设定百科
  3. 内容至少包含：
     - 地点名称
     - 地点用途
     - 氛围/危险性
     - 与主线的关系
  4. 不要改动 `设定集/力量体系.md`
  5. 除非必须，不要改动 `.mighty/state.json`

  完成后只汇报：
  - 实际操作的项目根目录
  - 新设定文件路径
  - 写入了哪些核心字段
  - 是否改动了 `.mighty/state.json`
- 预期:
  - 正确确认项目根目录
  - 成功创建新地点设定文件
  - 内容至少包含：地点名称、用途、氛围/危险性、与主线关系
  - 不改动力量体系文件
  - 最好不改 `state.json`
- 实际:
  - 实际操作目录：`/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
  - 新设定文件：`设定集/地点/后山东壁石门.md`
  - 写入核心字段：地点名称、地点用途、氛围、危险性、与主线的关系
  - `.mighty/state.json` 未改动
- 结果: pass
- 备注:
  - 这是一个很干净的只写设定文件的最小通过案例

---

## 5. `genm-novel-foreshadowing`

- 提示词:
  硬约束：只允许操作这个项目目录  
  `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

  如果你当前上下文不是这个目录，先切换到这个目录，再继续。  
  如果不能确认自己正在读取这个目录，就停止，不要继续。

  在确认目录正确后，再使用 genm-novel-foreshadowing skill，完成两件事：
  1. 列出当前项目的活跃伏笔
  2. 指出最该优先回收的一项，并说明理由

  要求：
  - 优先读取 `.mighty/state.json`
  - 不要修改任何文件
  - 结果尽量简洁

  完成后只汇报：
  - 实际操作的项目根目录
  - 当前活跃伏笔有哪些
  - 你认为最该优先回收的是哪一项
  - 是否改动了任何文件
- 预期:
  - 正确确认项目根目录
  - 列出活跃伏笔
  - 对优先回收项给出合理理由
  - 不改任何文件
- 实际:
  - 实际操作目录：`/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
  - 当前活跃伏笔：
    - 古镜来历
    - 后山东壁石门
  - 推荐优先回收项：后山东壁石门
  - 理由：其预计回收区间更近（第2-3章），且直接对应当前主线推进
  - 未改动任何文件
- 结果: pass
- 备注:
  - 这是一个干净的只读伏笔状态查询案例

---

## 6. `genm-novel-batch`

- 提示词:
  硬约束：只允许操作这个项目目录  
  `/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`

  如果你当前上下文不是这个目录，先切换到这个目录，再继续。  
  如果不能确认自己正在读取这个目录，就停止，不要继续。

  在确认目录正确后，再使用 genm-novel-batch skill，先不要直接写作，而是先评估：

  如果要从第002章开始顺序批量写 2 章，
  当前项目是否已经具备前置条件？

  请检查：
  - `.mighty/state.json`
  - `大纲/章纲/第002章.md`
  - `大纲/章纲/第003章.md`
  - 当前主角和伏笔状态是否足以支撑顺序续写

  要求：
  1. 先只做“可不可写”的判断
  2. 如果可以，说明为什么
  3. 如果不可以，明确阻塞项
  4. 不要改动任何文件

  完成后只汇报：
  - 实际操作的项目根目录
  - 结论：可批量写 / 不可批量写
  - 关键依据
  - 是否改动了任何文件
- 预期:
  - 正确确认项目根目录
  - 能判断批量写前置条件是否具备
  - 理由与现有 state / 章纲 / 伏笔状态一致
  - 不改文件
- 实际:
  - 实际操作目录：`/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
  - 结论：可批量写
  - 关键依据：
    - `.mighty/state.json` 存在，且 `current_chapter = 1`
    - `第002章`、`第003章` 章纲都存在且连续性信息完整
    - 主角当前状态与第 2-3 章目标衔接
    - 活跃伏笔 `后山东壁石门`、`古镜来历` 与第 2-3 章递进链条匹配
  - 未改动任何文件
- 结果: pass
- 备注:
  - 这是一个很好的“顺序批量写作 readiness”检查案例

---

## 阶段性结论

- `genm-novel-query`: fail（首次上下文指错项目）
- `genm-novel-status`: pass
- `genm-novel-character`: pass
- `genm-novel-setting`: pass
- `genm-novel-foreshadowing`: pass
- `genm-novel-batch`: pass（readiness check）

### 深验证：真实顺序写作

- 实际:
  - 实际操作目录：`/Users/arm/Desktop/vscode/Genm-codex/e2e-novel`
  - 成功生成：
    - `chapters/第002章.md`
    - `chapters/第003章.md`
  - 并且按顺序在每章后更新了 `.mighty/state.json`
  - 更新了：
    - `meta.updated_at`
    - `progress.current_chapter`
    - `progress.total_words`
    - `progress.last_write_chapter`
    - `progress.last_write_time`
    - `progress.milestones.golden_three_completed`
    - `entities.characters.protagonist.*`
    - `entities.items.*`
    - `entities.locations.*`
    - `plot_threads.foreshadowing.*`
    - `plot_threads.suspense.*`
    - `plot_threads.main_quest.progress`
    - `knowledge_base.*`
    - `chapter_meta.2`
    - `chapter_meta.3`
    - `chapter_snapshots.2`
    - `chapter_snapshots.3`
    - `summaries_index.2`
    - `summaries_index.3`
    - `dungeons.current`
- 结果: pass
- 备注:
  - 说明 `genm-novel-batch` 已从 readiness 验证推进到真实顺序写作验证

### 总结

第二阶段当前已迁入的能力，经过修正后 smoke 结果为：

- `genm-novel-query`: pass（复测通过）
- `genm-novel-status`: pass
- `genm-novel-character`: pass
- `genm-novel-setting`: pass
- `genm-novel-foreshadowing`: pass
- `genm-novel-batch`: pass（真实顺序写作已通过）

后续建议：

1. 如继续验证，可进入“可写型 smoke”或更长链路验证
2. 如继续扩展能力，可进入更高阶模式而不是继续补基础 CRUD 类 skill
