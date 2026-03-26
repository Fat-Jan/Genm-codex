# Genm-codex 第十七阶段总结

## 阶段定位

第十七阶段不再新增默认工作流能力，也不再围绕“还有没有新 skill 要补”推进。

这一阶段做的事情更像是：

- **把“反脸谱化”从创作讨论，推进成默认质量链里的结构门**

也就是说，项目在 `v1.x` 维护期第一次把一组跨流派、可复用、可验证的结构约束，真正收进了默认写作质量闭环。

---

## 已完成内容

### 1. 反脸谱化体系文档层

新增：

- [anti-flattening-framework/README.md](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/README.md)

并落成 12 个主模块，覆盖：

- 总纲
- 叙事权与主角特权
- 角色分层与投入配额
- 角色动力系统
- 关系网络与阵营分歧
- 冲突 / 信息差 / 后果链
- 场景级群像推进
- 流派故障库
- 诊断信号与快速修复
- 工具包与工作流
- 检查清单与评分规约
- 案例对照与校准

这意味着“人物不扁、关系不假、阵营不齐声、推进不白拿”已经不再是口头建议，而是项目内可引用的规则层。

### 2. 主链 skill 接线

本阶段没有新增新命令，而是把反脸谱化约束接进了默认主链：

- `novel-outline`
- `novel-review`
- `novel-write`
- `novel-fix`
- `novel-precheck`
- `novel-init`

并同步到了：

- [README.md](/Users/arm/Desktop/vscode/Genm-codex/README.md)
- [start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/start-here.md)
- [skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/skill-usage.md)
- [default-workflows.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/default-workflows.md)

这让它不再只是“能读到的理论”，而是默认工作流里的真实输入。

### 3. 轻量 state 约定

本阶段也把结构信号压回了现有 `chapter_meta`，而没有新造平行状态中心：

- `anti_flattening_flags`
- `anti_flattening_summary`
- `dimension_scores` 附加：
  - `人物立体度`
  - `关系张力`
  - `阵营分歧`
  - `代价感`

这保证了：

1. 反脸谱化可以被 review 持久化
2. state 不会因为新体系膨胀成复杂评分数据库

### 4. 四类真实 smoke 证据

本阶段最关键的，不是文档写出来了，而是拿到了真实样本证据：

- [真实链路 Smoke：宫斗宅斗](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/real-chain-smoke-e2e-gongdou-evil-2026-03-22.md)
- [交叉验证：双女主替身白月光](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/cross-genre-smoke-dual-substitute-evil-2026-03-22.md)
- [交叉验证：现实情感](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/cross-genre-smoke-realistic-divorce-2026-03-22.md)
- [交叉验证：系统 / 游戏任务线](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/cross-genre-smoke-system-taskline-2026-03-22.md)

四条样本给出的结果并不一样：

- 宫斗宅斗：
  - `review -> fix -> 再 review`
- 双女主替身：
  - `write -> review` 直接通过
- 现实情感：
  - `write -> review` 直接通过
- 系统任务线：
  - `write -> review` 直接通过

这恰恰证明：

- 反脸谱化体系不是要求所有流派都出同一种问题
- 而是要求同一套框架能在不同流派里给出有区分度、但稳定的工作流判断

### 5. 工作流使用建议

新增：

- [workflow-usage-guide-2026-03-22.md](/Users/arm/Desktop/vscode/Genm-codex/docs/anti-flattening-framework/workflow-usage-guide-2026-03-22.md)

这份文档把样本经验压成了三种可执行路线：

1. 直接通过型
2. 局部修补型
3. 上推重构型

到这一步，反脸谱化体系已经不只是：

- 能发现问题

而是已经可以指导：

- 怎么写
- 怎么审
- 怎么修
- 什么时候继续推进
- 什么时候先停下来补结构

---

## 阶段结论

第十七阶段最重要的结论是：

1. `反脸谱化` 已具备进入默认质量闭环的条件
2. 它不是某个流派的局部技巧，而是跨流派的结构门
3. 项目现在第一次拥有了一套“文档层 + skill 层 + state 层 + 样本层 + 使用层”都打通的结构化质量规则

更直白一点说：

- 以后在这个项目里，“人物不扁、关系不假、阵营不齐声、推进不白拿”应该被当成默认检查项，而不是额外加分项

---

## 当前判断

到第十七阶段这个检查点为止：

- 这套体系已经足够长期保留
- 不需要继续扩主模块
- 后续收益最高的方向不再是长理论，而是：
  - 增加真实调用样本
  - 在真实项目里持续观察它会把哪些问题稳定路由到 `fix / rewrite / precheck`

也就是说，第十七阶段之后，它更适合作为：

- **默认质量链的一部分**

而不是继续当作实验性创作讨论。

---

## 下一步建议

第十七阶段之后，最自然的策略不是继续堆新体系，而是：

1. 在真实项目和后续 smoke 中持续复用这套规则
2. 只在真实调用里发现明显漂移或误判时再调规则
3. 让新增样本优先服务：
   - `review` 路由稳定性
   - `precheck` 的结构风险判断
   - `write` 阶段的前置约束是否足够

一句话说：

- **第十七阶段已经够资格结案，后续进入维护与复用阶段。**
