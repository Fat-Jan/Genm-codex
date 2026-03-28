# Genm-codex 默认工作流

## 目的

这份文档定义当前默认推荐给用户的工作流。

它回答两个问题：

1. 如果我是普通用户，我现在最该怎么用
2. 哪些 skill 是默认主线，哪些只是补充或实验能力

---

## 默认工作流 1：新书起盘

适用场景：

- 从零开始一个新项目

推荐顺序：

1. `novel-init`
2. `novel-genre`
3. 古代家族权力题材先补：
   - `设定集/家族/宅门真值表.md`
   - `设定集/家族/小型家谱.md`
   - 涉及朝堂/东宫/地方官场时再补：
     - `设定集/官制/官职真值表.md`
     - `设定集/官制/权力层级图.md`
4. `novel-outline`
   - 先做 `mode=total`
5. 总纲初稿出来后，补当前卷刚需设定：
   - 家族权力题材至少补齐会影响卷一总纲、包装和前三章章纲的规则文件
   - 优先补：
     - 家族/继承/婚配/掌家真值
     - 当前卷要用到的关键人物卡
     - 当前卷要用到的地点 / 势力 / 旧案地点
   - 不默认膨胀到整本书全量设定
6. 需要进入前三章或具体章节规划时，再做 `novel-outline(mode=chapter)`
7. 如果当前项目是番茄平台，起盘协议栈现在默认应在 `setting gate(outline)` 时守卫式自动编译：
   - 触发条件：
     - `.mighty/launch-stack.json` 缺失
     - 或仍是 `preselect` placeholder
   - 手动重编译仍可用：
   - `python3 scripts/fanqie_launch_stack.py --project-root <project_root> --chapter 003 --chapters 001-003 --mode writeback --writeback`
   - 番茄平台项目默认主线应有这层；非番茄项目可跳过
8. `setting gate`
   - `python3 scripts/setting_gate.py <project_root> --stage outline`
   - 对番茄项目，这一步现在也负责守卫式 auto-compile `launch-stack`
9. `novel-package`

目标：

- 建好项目骨架
- 选定题材 / 平台
- 形成总纲与章纲
- 在写正文前补齐或阻断高风险设定缺口
- 形成第一版包装方案
- 尽早锁定角色分层、叙事权边界、关系结构和阵营分歧
- 上游结构边界见：
  - [upstream-structure-contract.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/upstream-structure-contract.md)
  - [total-outline-structure-contract.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/total-outline-structure-contract.md)

最小原则：

- 先有书的方向
- 古代家族权力题材先有谱系真值
- 官场古代题材先有官制真值
- 如项目尚未形成稳定立项输入，先补 `shared/templates/project/creative-brief.md`
- 先有 `总纲`，再有 `章纲`
- 总纲初稿后先补当前卷刚需设定，再冻结前三章章纲
- 设定集默认按“当前卷刚需”更新，不按“整本书全量”更新
- 如果当前项目是番茄平台，`novel-outline` 后跑 `setting gate(outline)` 时应先确保 `.mighty/launch-stack.json` 已进入可用状态
- 总纲完成后先过 `setting gate`
- 再写正文

### 设定集更新时机

在默认主线里，`设定集/` 不应只在项目初始化时创建一次，也不应等写崩后再回填。当前推荐在 3 个时点更新：

1. `总纲初稿后`
   - 把会影响卷一主冲突、包装和前三章章纲的真值先补齐
   - 目标是支持 `novel-outline(mode=chapter)`，不是把整本书设定写满
2. `setting gate(outline)` 被卡住时
   - 先按 `blocking_gaps` 和 `minimal_next_action` 定向补本地设定
   - 只有本地 truth source 仍不足时，才进入外部 research 候选链
3. 正文稳定推进后
   - 当某个角色、地点、势力、物品或规则已经成为稳定 canon，再通过 `novel-sync` / `novel-setting` 回灌到 `设定集/`
   - 不要在写作中途把临时猜测直接冻结成长期真值

### Gate Triage

当 `setting gate` 返回 `blocked` 或 `review_required` 时，优先按这条应急链处理：

1. 如确实缺外部 research 线索，可先跑 `novel-scan`
2. 再跑 `setting gate`
3. 若有高风险候选或歧义项，进入 `review-sync-queue`
4. 用 `novel-status` / `novel-resume` / `novel-query` 读取：
   - `gate status`
   - `blocking_gaps`
   - `review_items`
   - `minimal_next_action`

约束：

- `novel-scan -> setting gate -> review-sync-queue` 是候选审阅链，不是 canon 写入链
- gate 未通过时，不直接进入 `novel-write`

进一步说明见：

- [gate-triage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/gate-triage.md)

---

## 默认工作流 2：正文生产

适用场景：

- 已有项目，正在稳定推进章节

默认单章路径现在最好按一个固定的 `chapter transaction` 来理解：

1. `gate-check`
2. `draft`
3. `close`
4. `maintenance`
5. `snapshot`

硬约束：

- **一次性批量生成最多 3 章**
- 超过 3 章，必须拆批

推荐顺序：

1. `novel-write`
   - 写前先确认 `.mighty/setting-gate.json = passed`
   - 若未通过，先回 `python3 scripts/setting_gate.py <project_root> --stage outline`
   - 写前先过资料充分性强门：
     - 需要的真值表 / 规则文件缺失时，直接阻断本章写作
   - 单章默认会守卫式自动尝试一次 `novel-close`
   - 可显式用 `skip_close=true` 跳过
2. `novel-close`
   - 作为默认的单章收口轮入口
   - 内部执行：
     - `post_write_lint`
     - `novel-review`
     - 单一路由：
       - `novel-fix`
       - `novel-polish`
       - `novel-rewrite`
       - 或 `none`
     - 若正文被修改，再做一次 `novel-review`
   - 若强质量门仍有客观 blocker：
     - 不允许把本章标记为已收口
     - 必须回到 `novel-fix` 或 `novel-rewrite`
   - 确定性 lint warning 可以进入修补，但只有 policy-backed blocker 才能阻断 close 成功
3. 每 3-5 章或一个阶段后：
   - `novel-sync`
   - 若最近章节已稳定引入新的角色、地点、势力、物品或规则，再同步回 `设定集/`
4. 每轮正文维护后：
   - 默认自动挂：
     - `scripts/post-task-maintenance.py <project_root> --trigger write|batch|workflow`
   - 手动补跑：
     - `scripts/project-maintenance.py <project_root>`
   - 维护链现在应依次完成：
     - `setting gate(write-post)`
     - sync / guidance split / thin-state
     - `snapshot`
     - `memory-context`
     - `content-positioning`
     - 轻量 trace log 写入
5. 章节很多后：
   - `novel-sync (thin-state)`
6. 单章事务收尾时：
   - 默认优先使用维护链自动生成的 `snapshot`
   - 需要手动重生或比对时，再显式用 `novel-snapshot`
   - 或用 `novel-resume` / `novel-workflow` 判断当前 chapter transaction 卡在哪一步

目标：

- 先把章节写出来
- 再做审查
- 再按问题类型修
- 再把稳定实体沉淀回 `设定集/`
- 再把写后新稳定信息回灌到 `setting gate` 和 `sync-review`
- 再把 `learned / market` 重负载旁路出 `state`
- 再把旧章节元数据归档出 `state`
- 遇到歧义实体时，再收 `sync-review` 队列

推荐规则：

- `novel-close` 是默认的单章收口轮入口，用来显式执行 `review -> route -> re-review`
- 单章 `novel-write` 默认会尝试守卫式自动收口；`novel-batch` 不继承这个默认行为
- `scripts/post-task-maintenance.py --trigger batch` 只拥有 repo-owned `maintenance + snapshot` 尾段，不应被解释成 batch 默认已自动完成 `close`
- `novel-review` 应一次性把问题收成 1-3 个可执行 issue clusters，而不是散成很多微修提示
- 单章默认目标是“一次修订轮收口”：
  - 一次 `novel-fix` 尽量解决全部局部问题
  - 只有当语言层是主要剩余风险时才单独进 `novel-polish`
  - 不鼓励 `fix -> 再补一句 -> 再 polish 一点 -> 再补一句` 这种多轮微修
- `novel-close` 一次只应走一条主路由，不允许在同一轮里 `fix + polish`
- 当同章已经发生 2 轮修订尝试且关键问题仍未消失时，默认升级到 `novel-rewrite`
- 局部问题 -> `novel-fix`
- 语言层问题且结构已稳 -> `novel-polish`
- 结构层问题或两轮修订未收口 -> `novel-rewrite`
- 批量写作 -> 最多 `3` 章 / 批，并在每批后过质量门
- `skip_close=true` 只在你明确想要“这次只写不收口”时使用
- `novel-review` 默认也应检查：
  - 开篇承诺是否在前 1-3 章可见且有近期兑现路径
  - 剧情是否能分清主推进线和被触动的次级线
  - 推进是否真的改变了信息、关系、代价或残账账本
  - 主角特权是否吃掉他人人生
  - 关键角色是否只剩功能位
  - 关系 / 阵营是否写成单声道
  - 推进是否留下真实代价与残账
- `novel-write` 应尽量在正文阶段就避免把配角写成按钮
- 当前章若暴露出“下一章依赖的新真值尚未落盘”，先补 `设定集/` 再继续写，不要靠上下文记忆硬撑
- `novel-precheck` 应把人物/关系/阵营失衡视为投稿前风险，而不只看平台节奏
- 强拦截规则只认：
  - [strong-quality-gate-policy.json](/Users/arm/Desktop/vscode/Genm-codex/docs/strong-quality-gate-policy.json)
  - 不在多个 skill 文案里重复维护阈值

反脸谱化工作流参考：

- 完整文档：[anti-flattening-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/README.md)
- QUICK 速查卡：[anti-flattening-framework/QUICK.md](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/QUICK.md)
- rule-cache：[anti-flattening-framework/rule-cache.json](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/rule-cache.json)

开篇与剧情层次工作流参考：

- 完整文档：[opening-and-plot-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/README.md)
- QUICK 速查卡：[opening-and-plot-framework/QUICK.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/QUICK.md)
- rule-cache：[opening-and-plot-framework/rule-cache.json](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/rule-cache.json)

写作基本功与内容标准工作流参考：

- 完整文档：[writing-core-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/writing-core-framework/README.md)
- QUICK 速查卡：[writing-core-framework/QUICK.md](/Users/arm/Desktop/vscode/Genm-codex/docs/writing-core-framework/QUICK.md)
- rule-cache：[writing-core-framework/rule-cache.json](/Users/arm/Desktop/vscode/Genm-codex/docs/writing-core-framework/rule-cache.json)

番茄起盘协议栈参考：

- [fanqie-launch-stack/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/opening-and-plot-framework/fanqie-launch-stack/README.md)

---

## 默认工作流 3：投稿准备

适用场景：

- 已有一批章节，准备对外发布

推荐顺序：

1. `novel-precheck`
2. `novel-package`
3. `novel-export`

目标：

- 先判断能不能投
- 再看包装要不要更新
- 最后导出

推荐规则：

- `precheck = ready-now` 且 `packaging-needs-update = no`
  - 可以直接进入导出
- `precheck = revise-then-submit`
  - 先回正文修
- `packaging-needs-update = yes`
  - 先回包装层

当前已验证的番茄女频样本里，最靠近这条工作流完成态的是：

- [fanqie-evil-gongdou-submission-assessment.md](/Users/arm/Desktop/vscode/Genm-codex/docs/research/fanqie/fanqie-evil-gongdou-submission-assessment.md)
  - `恶女 x 宫斗宅斗`
  - 当前状态：`do-not-submit`，待补谱系与命名风控

---

## 默认工作流 4：持续学习

适用场景：

- 已经写了一批章节，希望风格更稳

推荐顺序：

1. `novel-learn`
2. `novel-status`

可选补充：

- `novel-query`
- `novel-retrieve`
- `novel-analyze`

目标：

- 从已有正文中提炼可复用模式
- 让写作偏好稳定沉淀

---

## 默认工作流中的辅助能力

这些不是主链，但很常用：

### 项目状态 / 查询

- `novel-status`
- `novel-query`
- `novel-index`

补充：

- 如果项目已经跑过维护链，`novel-status` / `novel-query` 现在也应优先读取：
  - `.mighty/workflow-health.json`
  - `.mighty/quality-audit.json`
  - `.mighty/knowledge-projection.json`
  用来快速判断 workflow artifact 是否失真，以及当前 sidecar / transaction 健康概览。

### 快速引用

- `novel-retrieve`

### 区间分析 / 诊断

- `novel-analyze`

### 设定维护

- `novel-character`
- `novel-setting`
- `novel-foreshadowing`
- `novel-sync`

### 恢复与回溯

- `novel-snapshot`
- `novel-resume`
- `novel-workflow`

### 已有稿接入

- 先用 `scripts/import_existing_chapters.py <project_root> --from <source>`
- 查看 `.mighty/import-report.json`
- 再走：
  - `novel-index build`
  - `setting gate`
  - `novel-resume`

---

## 当前不属于默认工作流的能力

### `novel-scan`

原因：

- 仍属于实验能力
- 它能提供市场信号，但不该成为每个用户默认要跑的步骤
- 如果明确需要外部 research 来辅助 `setting gate`，也只应通过可选候选 sidecar 进入 review queue
- 不允许因为 `novel-scan` 结果存在，就直接改写 `设定集/` 或跳过本地 truth gate

### `novel-log`

原因：

- 当前更适合作为**已接线的专家辅助能力**
- 虽然 trace log 现在已有真实写入方
- 但默认恢复 / 诊断主链仍优先：
  - `novel-workflow`
  - `novel-resume`
  - `novel-snapshot`
- 它更适合：
  - 排障
  - 只读检查关键事件
  - 事后诊断

### `novel-spinoff`

原因：

- 这是明确的边角创作能力，不是正文主线推进的一部分
- 只有用户明确想写：
  - 番外
  - 角色篇
  - IF线
  时才应进入
- 默认不应让它混入：
  - 主线章节推进
  - `progress.current_chapter`
  - 当前投稿与质量闭环

---

## 当前 Fanqie-first 真实状态

- 第一条内部生产模板：
  - `职场婚恋 x 合租反绑定`
  - 冻结样本：
    - `她升职那天，前上司成了我合租室友`
- 首个可投样本：
  - `她升职那天，前上司成了我合租室友`
- 第二条生产模板候选：
  - `恶女 x 现实情感`
- 第三条实验线：
  - `恶女 x 现言甜宠`
- 第四条候选实验线：
  - `恶毒女配 x 双女主替身白月光`
- 待重验样本：
  - `恶女 x 宫斗宅斗`
- 当前冻结与路由 smoke：
  - `docs/20-研究实验/fanqie-first-frozen-template-2026-03-26.md`
  - `docs/20-研究实验/quality-route-smoke-2026-03-26.md`

### `novel-config` / `novel-test`

原因：

- 更像环境和连接引导
- 不是日常写作主线

### `novel-help` / `novel-tutorial`

原因：

- 当前已由 docs-first 承担

---

## 最短建议

如果你不知道该用哪个 skill，先套这条判断：

1. 没项目：`init -> genre -> outline -> package`
   - 古代家族权力题材：`init -> 家族真值表/小家谱 -> outline -> package`
   - 古代官场/宫廷权力题材：`init -> 家族真值表/官职真值表 -> outline -> package`
2. 有项目想继续写：`write -> review -> fix/polish/rewrite`
3. 想投稿：`precheck -> package -> export`
4. 想稳住风格：`learn -> status`
5. 设定集长期不更新：`sync -> character/setting`

---

## 一句话结论

当前默认主线已经不是“堆很多命令”，而是：

- 起盘
- 写作
- 审查修正
- 包装
- 投稿准备
- 持续学习

这 6 步。
