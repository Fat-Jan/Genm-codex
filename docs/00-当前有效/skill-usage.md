# Genm-codex Skill 使用说明

> 如果你只想快速知道“现在该用哪个 skill”，先读 [start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/start-here.md)。

如果你想看当前默认推荐工作流，读：

- [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/default-workflows.md)

## 已安装的 Skill 名称

安装脚本会把以下目录链接到 `~/.codex/skills/`：

- 一套 plain 名：`novel-*`
- 一套兼容别名：`genm-novel-*`

下面先列兼容别名：

- `genm-novel-init`
- `genm-novel-batch`
- `genm-novel-character`
- `genm-novel-foreshadowing`
- `genm-novel-config`
- `genm-novel-close`
- `genm-novel-fix`
- `genm-novel-genre`
- `genm-novel-index`
- `genm-novel-log`
- `genm-novel-learn`
- `genm-novel-package`
- `genm-novel-scan`
- `genm-novel-polish`
- `genm-novel-precheck`
 - `genm-novel-snapshot`
 - `genm-novel-workflow`
- `genm-novel-query`
- `genm-novel-setting`
- `genm-novel-status`
- `genm-novel-outline`
- `genm-novel-analyze`
- `genm-novel-write`
- `genm-novel-review`
- `genm-novel-resume`
- `genm-novel-retrieve`
- `genm-novel-rewrite`
- `genm-novel-spinoff`
- `genm-novel-sync`
- `genm-novel-test`
- `genm-novel-export`

同时也会创建对应的 plain 名，例如：

- `novel-init`
- `novel-analyze`
- `novel-batch`
- `novel-character`
- `novel-foreshadowing`
- `novel-close`
- `novel-fix`
- `novel-genre`
- `novel-index`
- `novel-log`
- `novel-learn`
- `novel-package`
- `novel-scan`
- `novel-polish`
- `novel-precheck`
- `novel-query`
- `novel-setting`
- `novel-snapshot`
- `novel-spinoff`
- `novel-status`
- `novel-config`
- `novel-test`
- `novel-outline`
- `novel-workflow`
- `novel-write`
- `novel-review`
- `novel-resume`
- `novel-retrieve`
- `novel-rewrite`
- `novel-export`
- `novel-sync`

## 调用名说明

- 上面这些是本地安装链接名
- 在 Codex 会话中，优先使用各个 `SKILL.md` frontmatter 中的 `name` 来触发 skill
- 因此实际提示词里更推荐写：
  - `novel-init`
  - `novel-close`
  - `novel-query`
  - `novel-status`
  - `novel-polish`
  - `novel-genre`
- `genm-novel-*` 更适合表示“这个 skill 已安装到本地”，不适合作为唯一调用名假设

## 推荐使用顺序

最小创作闭环：

1. `novel-init`
2. 古代家族权力题材先补 `宅门真值表 + 小型家谱`
3. 涉及朝堂/东宫/地方官场时再补 `官职真值表 + 权力层级图`
4. `novel-outline`
5. 如果当前项目是番茄平台，补一轮起盘协议栈编译：
   - `python3 scripts/fanqie_launch_stack.py --project-root <project_root> --chapter 003 --chapters 001-003 --mode writeback --writeback`
6. `python3 scripts/setting_gate.py <project_root> --stage outline`
7. `novel-write`
8. `novel-close`
9. 仍未收口时再按结果进入 `novel-rewrite`
10. `novel-export`

补充规则：

- 单章正文现在最好按一个固定的 `chapter transaction` 理解：
  - `gate-check -> draft -> close -> maintenance -> snapshot`
- 如果项目还没有稳定的立项输入，先补 `shared/templates/project/creative-brief.md`
- 上游结构边界见：
  - [upstream-structure-contract.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/upstream-structure-contract.md)
  - [total-outline-structure-contract.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/total-outline-structure-contract.md)
- 单章 `novel-write` 默认会守卫式自动尝试一次 `novel-close`
- `novel-batch` 不会继承这个默认行为
- 如果你只想写本章、不想自动收口，显式传 `skip_close=true`
- `novel-outline` 完成后，默认应先过一次 `setting gate`
- 如果当前项目是番茄平台，`novel-outline` 后先运行一次 `fanqie_launch_stack.py`，把 `.mighty/launch-stack.json` 从 `preselect` placeholder 写成正式 sidecar
  - 命令入口：
    - `python3 scripts/fanqie_launch_stack.py --project-root <project_root> --chapter 003 --chapters 001-003 --mode writeback --writeback`
  - 命令入口：
    - `python3 scripts/setting_gate.py <project_root> --stage outline`
- `novel-write` 现在应先检查 `.mighty/setting-gate.json`
  - 若状态不是 `passed`，先回 gate，不要直接写
  - 若状态是 `blocked` 或 `review_required`，优先看：
    - `blocking_gaps`
    - `review_items`
    - `minimal_next_action`
  - `minimal_next_action.suggested_commands` 现在就是最小处理入口
  - 如果你想要集中入口，不想在多个说明之间跳，直接看：
    - [gate-triage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/gate-triage.md)
- 当前默认强质量门已经接进主线：
  - 写前若缺真值表 / 世界规则 / 时代资料，`novel-write` 应直接阻断，而不是带着脑补开写
  - 收口前若仍存在短章 / 明显缩水 / malformed text / 可证伪设定违和等 hard blocker，`novel-close` 不应判定本章收口成功
  - 单一规则源是：
    - [strong-quality-gate-policy.json](/Users/arm/Desktop/vscode/Genm-codex/docs/strong-quality-gate-policy.json)

已有稿接入：

- 优先运行 `python3 scripts/import_existing_chapters.py <project_root> --from <source>`
- 查看 `.mighty/import-report.json`
- 再走：
  - `novel-index build`
  - `setting gate`
  - `novel-resume`

反脸谱化与群像打磨入口：

- [anti-flattening-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/README.md)
- `novel-outline` 现在会按需读取这组文档来锁角色分层、关系结构、阵营分歧与后果链
- `novel-write` 现在会按需读取这组文档来约束非主角行动、关系负债与场景残账
- `novel-review` 现在会按需把主角特权、角色独立性、关系张力和流派故障纳入结构审查
- `novel-review` 现在默认会把单章问题收成可一次执行的 issue clusters，并在两轮修订仍未收口时上推 `novel-rewrite`
- `novel-close` 现在是默认推荐的单章收口轮入口，内部固定执行 `novel-review -> 单一路由 -> re-review`
- `novel-write` 现在在单章模式下会默认守卫式自动尝试 `novel-close`，并在跳过时说明原因
- `novel-workflow` / `novel-resume` 现在应把单章 chapter transaction 当成默认恢复单元，而不是只看模糊的当前任务状态
- `novel-fix` 现在会在局部修补范围内读取快速修复动作，并尽量一次收口同章的局部问题，而不是把人物补丁偷渡成整章重写
- `novel-polish` 现在默认偏向单次 `all` 向润色，不鼓励把 prose / dialogue / pacing 拆成多轮微修
- `novel-precheck` 现在会在投稿前检查主角特权失衡、阵营单声道和推进过顺风险
- 当当前 bucket 为 `宫斗宅斗` 时，`novel-write` 会自动加一层轻量“故障漏斗”预检，`novel-review` 会自动读取专项判定卡并补充 `gongdou_funnel_summary`
- 专项判定卡入口： [gongdou-zhaidou-fault-funnel-review-card.md](/Users/arm/Desktop/vscode/Genm-codex/docs/gongdou-zhaidou-fault-funnel-review-card.md)

开篇方法与剧情层次入口：

- [opening-and-plot-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/README.md)
- `novel-outline` 现在会按需读取这组文档来锁开篇承诺、前三章兑现路径、主推进线和次级线触动
- `novel-write` 现在会按需读取这组文档来避免背景先行、压力空转和只有事件没有账本变化
- `novel-review` 现在会按需把开篇抓力、层次清晰度和推进有效性纳入结构审查
- `novel-precheck` 现在会在投稿前检查首屏 promise、黄金三章兑现和推进残账
- `novel-package` 现在会按需读取这组文档，把包装承诺和正文实际可兑现节点对齐

写作基本功与内容标准入口：

- [writing-core-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/writing-core-framework/README.md)
- `novel-write` 现在会按需读取这组文档来约束镜头、信息投放、对白动作和段落节奏
- `novel-review` 现在会按需把内容标准失格、执行层风险和包装对齐问题收成可执行问题簇
- `novel-precheck` 现在会按需把精品审核、投稿前判断和包装过度承诺风险纳入最终建议
- `novel-package` 现在会按需读取这组文档，把“开篇方法 / 类型差异 / 精品审核标准”压成包装约束
- `novel-learn` 现在会按这组文档把 memory 收成压缩信号，而不是长篇理论

番茄起盘协议栈入口：

- [fanqie-launch-stack/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/fanqie-launch-stack/README.md)
- `novel-outline` / `novel-write` / `novel-review` / `novel-precheck` / `novel-package` 现在可以按需读取这组文档与 `.mighty/launch-stack.json`
- 这层优先处理：
  - `premise`
  - `pivot`
  - `launch grammar`
  - `retention protocol`

## 第二阶段已迁入

- `genm-novel-character`
- `genm-novel-foreshadowing`
- `genm-novel-query`
- `genm-novel-setting`
- `genm-novel-status`
- `genm-novel-batch`

## 第三阶段已完成

- `genm-novel-polish`
- `genm-novel-genre`
- `genm-novel-analyze`
- `genm-novel-resume`
- `genm-novel-index`
- `genm-novel-log`

推荐场景：

- 对已写章节做轻量精修，而不是完整重写
- 查看当前项目的题材 profile
- 列出可用题材
- 给项目重新应用指定 profile
- 对已写章节区间做轻量数据分析
- 在中断后快速判断从哪里继续最稳

推荐场景：

- 创建或补完角色卡
- 管理伏笔与回收节奏
- 创建或补完力量体系、势力、地点、物品设定
- 查看角色当前设定
- 调整角色关系
- 顺序批量写作少量章节
- 查看主角当前状态
- 查询活跃伏笔
- 统计项目进度
- 列出角色/物品/地点信息

## 第四阶段已完成

- `genm-novel-fix`
- `genm-novel-snapshot`
- `genm-novel-precheck`
- `genm-novel-workflow`
- `genm-novel-retrieve`
- `genm-novel-spinoff`

推荐场景：

- 根据 review 结果做局部修复
- 查看或加载章节快照
- 在投稿前做只读预检
- 查看当前 workflow 是否空闲
- 获取写作瞬时参考卡
- 在单项目内写轻量番外
- 把稳定角色 / 地点 / 势力从运行态同步回设定集
- 在长项目里把旧章节元数据归档出 `state`
- 把 `learned_patterns / market_adjustments` 从 `state` 旁路到 sidecar 文件
- 用 `scripts/project-maintenance.py` 跑一次完整维护链
- 用 `scripts/post-task-maintenance.py` 把维护链挂在 `write / batch / workflow` 后
- 维护链现在应先跑 `scripts/setting_gate.py <project_root> --stage write-post`
- 用 `scripts/review-sync-queue.py` 处理 `sync-review` 队列
- `sync-setting-assets.py` 现在默认会把低置信候选压进 `sync-review`，而不是直接沉淀成角色卡
- `novel-scan` 现在只应该给 `setting gate` 提供 research candidates，不直接改 canon

## 第五阶段已完成

- `genm-novel-config`
- `genm-novel-test`
- `genm-novel-learn`

推荐场景：

- 检查当前工作区和本机 Codex 配置状态
- 判断是否具备连接测试前置条件
- 从本地章节中学习写作模式并回写 `learned_patterns`

## 第九阶段已完成

- `genm-novel-package`

推荐场景：

- 生成书名候选
- 生成平台适配简介
- 做角色命名提案
- 给开篇钩子做包装层优化
- 输出完整的“书名 + 简介 + 开篇包装”方案
- 古代项目在锁标题前补一轮主角名 / 关系词风控

### ancient route

```text
如果当前项目是宫斗宅斗、古代言情或历史家族权力线，先创建并填写：
- 设定集/家族/宅门真值表.md
- 设定集/家族/小型家谱.md

再进入 novel-outline 和 novel-package。
```

### character

```text
请使用 novel-character skill，为当前项目创建一个新角色并写入设定集/角色/。
```

### foreshadowing

```text
请使用 novel-foreshadowing skill，列出当前项目的活跃伏笔并指出最该优先回收的项。
```

### batch

```text
请使用 novel-batch skill，从第002章开始顺序生成 3 章，并在每章后更新 state。
```

批量写作硬约束：

- **一次性最多 3 章**
- 超过 3 章必须拆批，否则容易出现：
  - 后半段缩水
  - 提纲化短章
  - AI 概述腔

### setting

```text
请使用 novel-setting skill，为当前项目创建或更新一个设定文件。
```

### status

```text
请使用 novel-status skill，总结当前项目状态，给我一个简明 dashboard。
```

### polish

```text
请使用 novel-polish skill，对第001章做一次 `all` 向收口润色，优先解决剩余语言层问题，并同步更新状态元数据。
```

### close

```text
请使用 novel-close skill，对第001章做一次 `auto` 模式单章收口；如果只剩语言层问题，就把压 AI 味放在 `novel-polish` 分支里完成，并在必要时复审。
```

### write-only

```text
请使用 novel-write skill，写第016章，并设置 `skip_close=true`；这次只写正文，不自动进入收口轮。
```

### genre

```text
请使用 novel-genre skill，列出当前可用题材，并把当前项目应用到 xuanhuan / tomato 对应的 profile。
```

### index

```text
请使用 novel-index skill，为当前项目构建一个轻量索引，并告诉我已索引的章节数和主要实体统计。
```

### log

```text
请使用 novel-log skill，检查当前项目的 trace 日志是否已初始化；如果已初始化，再给我最近 10 条摘要。
```

补充：

- 默认工作流现在会在 `setting gate`、`maintenance`、`snapshot` 等关键点写入轻量 trace log
- `novel-log` 现在不再只适用于“已经手工初始化日志的项目”

### fix

```text
请使用 novel-fix skill，基于第001章的 review 结果，一次性处理本章所有局部问题，并告诉我哪些 issue clusters 已收口、哪些必须升级到 rewrite。
```

### snapshot

```text
请使用 novel-snapshot skill，列出当前项目已有的章节快照，并告诉我第001章快照里最关键的状态信息。
```

补充：

- 默认维护链现在会在事务尾段自动生成 snapshot artifact
- `novel-snapshot` 更适合：
  - 手动重生
  - 比较
  - 浏览历史快照
- 如果项目有组合题材定位，维护链也会同时刷新 `.mighty/content-positioning.json`

### precheck

```text
请使用 novel-precheck skill，对第001章到第003章做番茄平台的投稿前预检，并告诉我现在适不适合直接投稿。
```

### workflow

```text
请使用 novel-workflow skill，告诉我当前项目有没有活动中的 workflow；如果没有，就说明现在处于什么状态。
```

### retrieve

```text
请使用 novel-retrieve skill，快速告诉我“后山东壁石门”现在在项目里是什么定位，以及写作时最该记住的约束。
```

### spinoff

```text
请使用 novel-spinoff skill，基于当前项目写一个“林晚照角色篇”的轻量番外，并明确它不是主线正文章节。
```

### config

```text
请使用 novel-config skill，检查当前工作区和本机 Codex 配置里与模型/提供商相关的设置，并告诉我最小下一步。
```

### test

```text
请使用 novel-test skill，判断当前本地配置是否已经具备做连接测试的条件，并告诉我下一步该怎么测。
```

### learn

```text
请使用 novel-learn skill，从第001章到第003章里总结稳定可复用的文风偏好和需要避免的表达模式，并保守回写 learned_patterns。
```

### package

```text
请使用 novel-package skill，为当前项目生成一套包装方案：包含书名候选、两版简介和三条开篇包装建议；如合适，可保存到 包装/。
```

### ancient office route

```text
如果当前项目涉及朝堂、东宫、地方官场、军政或宗室封爵，先创建并填写：
- 设定集/官制/官职真值表.md
- 设定集/官制/权力层级图.md

再进入 novel-outline 和 novel-package。
```

```text
请使用 novel-learn skill，从第001章到第003章提炼当前项目的写作模式，并更新 learned_patterns。
```

### scan

这是一个**实验能力**：

- 当前可用，但不属于默认生产主线
- 默认内置来源只覆盖 `番茄 + 玄幻 + quick`
- `project-annotate` 只有在当前运行达到中高可信时，才会写：
  - `.mighty/market-adjustments.json`
  - `.mighty/state.json -> market_adjustments` 轻量摘要
- 如果结果是 low confidence 或 skeleton，会只保留 `.mighty/market-data.json`

```text
请使用 novel-scan skill，先为当前项目生成一个 report-only 的市场扫描结果文件，并明确说明当前证据可信度。
```

如果你要直接跑最小可执行入口，而不是只靠 skill 提示词，可以用：

```bash
python3 scripts/novel_scan.py <project_root> --platform 番茄 --genre 玄幻 --depth quick --mode report-only
```

补充：

- 当前默认内置来源已覆盖：
  - `番茄 + 玄幻 + quick`
  - `番茄 + 宫斗宅斗 + quick`
- 其他组合建议额外传 `--source-url <url>`
- `--mode project-annotate` 不会绕过可信度门槛
- 如需把外部扫描结果作为 `setting gate` 的可选 research 候选输入，而不是直接改 canon，可额外传：
  - `--emit-research-candidates`
  - 可选 `--research-candidates-file <path>`
- 默认候选 sidecar 为：
  - `.mighty/research-candidates.json`
- 这类候选只应用于：
  - `python3 scripts/setting_gate.py <project_root> --stage outline --candidates-file <path>`
- 候选会进入：
  - `.mighty/setting-gate.json`
  - `.mighty/sync-review.json`
  不会直接写入 `设定集/` 或 canon

如果当前问题先卡在“正文抓取不稳定”，而你需要一个不阻塞调研的获取层，可以先用：

```bash
python3 scripts/acquire_source_text.py <url> --pretty
```

说明：

- 默认顺序是 `fetch MCP -> direct HTML extract -> search fallback`
- 现在会返回 provider 诊断信息，说明当前 `fetch` / `search fallback` 实际来自：
  - CLI
  - env
  - project `.mighty/config.json`
  - `~/.codex/config.toml`
  - 或 registry default
- 如果没有配置 `--fetch-cmd` / `GENM_FETCH_MCP_CMD`，`fetch` 阶段会自动退到 `r.jina.ai` reader proxy
- 如果没有配置 `--search-cmd` / `GENM_SEARCH_FALLBACK_CMD`，`search fallback` 会自动退到 `Bing RSS`
- 如需只看 provider 解析结果，可运行：

```bash
python3 scripts/acquire_source_text.py <url> --show-provider-config --pretty
```

- 如需显式绑定某个项目级 provider，可在 `.mighty/config.json` 中配置：
  - `acquire_source_text.fetch_provider`
  - `acquire_source_text.search_provider`
- 会统一返回 `status / source_type / failure_reason / attempts`
- 重点是稳定返回结构化结果，不是承诺任意站点都能拿到完整正文
- 默认 `--min-body-chars = 300`，过短页面会被判成不足正文；做连通性检查时可临时降到 `50`
- 如需持久化域名跳过策略，可额外传 `--policy-file <path>`

### query

```text
请使用 novel-query skill，基于当前 state 和 index，列出活跃伏笔，并告诉我哪些章节提到了后山东壁。
```

如果你想直接查询 gate 状态，也可以这样问：

```text
请使用 novel-query skill，告诉我当前 setting gate 的状态、blocking_gaps 和 minimal_next_action。
```

### status

```text
请使用 novel-status skill，给我一个 full 模式的项目状态面板，并额外带上 gate status、blocking_gaps 和 minimal_next_action。
```

### analyze

```text
请使用 novel-analyze skill，对第001章到第003章做区间分析，重点看节奏、爽点密度和连续性问题。
```

### resume

```text
请使用 novel-resume skill，如果当前项目被 setting gate 卡住，就优先告诉我 minimal_next_action 和最稳的下一步。
```

## 最小 E2E 路线

建议在一个新会话中：

1. 使用 `novel-init` 初始化最小项目
2. 使用 `novel-outline` 生成总纲和第 1-10 章章纲
3. 使用 `novel-write` 写第 1 章
4. 使用 `novel-review` 审查第 1 章
5. 使用 `novel-rewrite` 按审查结果定向重写
6. 使用 `novel-export` 导出第 1 章 txt

## 最小 smoke 提示词

### init

```text
请使用 novel-init skill 在当前目录初始化一个小说项目：
title=E2E样本，genre=玄幻，platform=番茄，target_chapters=10
```

### outline

```text
请使用 novel-outline skill，为当前项目补全总纲并生成第 1-10 章章纲。
```

### write

```text
请使用 novel-write skill，写第001章，目标约 3000 字，并更新 .mighty/state.json。
```

### review

```text
请使用 novel-review skill，审查第001章并把 review 结果写回 .mighty/state.json。
```

### rewrite

```text
请使用 novel-rewrite skill，按 review 结果定向重写第001章，并同步主角卡与状态。
```

### export

```text
请使用 novel-export skill，导出第001章为 txt。
```

## 注意

- 当前第一阶段只保证核心闭环
- 第二阶段能力已迁入并做过 smoke
- 第三阶段当前只起步了 `polish` 和 `genre`
- 第三阶段当前也已进入 `analyze / resume / index`
- 第三阶段已完成 `polish / genre / analyze / resume / index / log`
- 第四阶段已完成 `fix / snapshot / precheck / workflow / retrieve / spinoff`
- 第五阶段已完成 `config / test / learn`
- 第八阶段当前已进入 `scan`
- `shared/` 资产更新后，先运行：
  - `bash scripts/sync-shared-from-genm.sh --report`
- 需要机器可读差异时，再看：
  - `bash scripts/sync-shared-from-genm.sh --report-json`
- 重点确认：
  - `protected_local_paths`
  - `local_only_paths`
  - `unexpected_local_only_paths`
  - `drift_paths`
  - `source_only_paths`
- 当前默认会阻断 `same-path drift overwrite`
- 只有在明确确认后，才显式使用：
  - `bash scripts/sync-shared-from-genm.sh --allow-drift-overwrite --domain <references|templates|profiles>`
