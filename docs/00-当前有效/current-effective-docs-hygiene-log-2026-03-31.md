# 当前有效文档去历史化整理记录 2026-03-31

> 目的：记录本轮对 `docs/00-当前有效/` 的低风险“去历史化整理”动作，说明哪些文档已完成现状化修正，哪些仍可后续继续清理。
>
> 范围：仅覆盖本轮实际处理的低风险文档一致性项，不重写长期保留的阶段计划、模板或复检说明。

---

## 一、本轮处理结论

**思考强度：L3 深度**

本轮已完成一轮低风险优先的“当前有效文档去历史化整理”，目标是让 `docs/00-当前有效/` 更贴近“现状真源”而不是“历史计划集合”。

本轮实际完成的处理包括：

1. 继续整理 [bucket-overlay-inventory.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/bucket-overlay-inventory.md)
   - 将“历史 P0 待实现语义”进一步改写为：
     - 当前维护重点
     - 历史实现记录
     - 参考实现样例
2. 整理 [bucket-profile-slug-mapping.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/bucket-profile-slug-mapping.md)
   - 将“待实现 checklist + 文档内硬编码映射函数”收紧为：
     - registry 真值入口
     - runtime 解析入口
     - 当前 state 投影口径
     - 已存在的测试证据
3. 整理 [chapter-structure-fields-design.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/chapter-structure-fields-design.md)
   - 将“建议接线 + 未勾选完成标记”收紧为：
     - 当前 schema / template 落点
     - 当前 outline / review / precheck consumer 入口
     - 已存在的结构审计与测试证据
4. 保留了真正应当保留的计划型文档，不强行去历史化，例如：
   - [current-processing-plan-phased-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/current-processing-plan-phased-v1.md)
   - [monthly-governance-phase-close-template-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/monthly-governance-phase-close-template-v1.md)
   - [governance-execution-review-plan.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/governance-execution-review-plan.md)
5. 识别出一批“仍包含历史阶段语义，但不一定应立即改写”的文档，后续如继续做文档瘦身，可再按风险分层处理

---

## 二、本轮已处理项

### 2.1 `bucket-overlay-inventory.md`
**思考强度：L2 + L3**

已完成的修正：

- 文档目的改为“记录现状、历史背景与后续维护规则”
- 缺口分析中明确“当前不存在已知缺失项”
- 原“缺口优先级”改为“当前维护重点”
- 原“短期 / 中期 / 长期”改为：
  - 当前阶段维护
  - 历史实现记录
- 原“优先实现 P0 Bucket”改为“参考实现样例”，明确这些是历史样例，不是当前待办
- 完成标记已与当前现状一致

当前效果：

- 该文档已不再容易被误读为“overlay 仍有大量未实现项”
- 保留了历史实现信息，但已降级为参考背景

### 2.2 `bucket-profile-slug-mapping.md`
**思考强度：L2 + L3**

已完成的修正：

- 增加当前 authoritative truth 说明：
  - `shared/templates/profile-bucket-registry-v1.json`
  - `scripts/profile_contract.py`
- 将 `state.genre_profile.bucket` 的口径明确为“当前 bucket 名称 / display_name”，不再误写成 slug
- 移除已经与实际 registry / runtime 脱节的文档内硬编码映射函数示例
- 将完成标记改为与当前现状一致，并补测试 / 脚本证据

当前效果：

- 该文档不再把未落地方案写成当前运行时事实
- 读者可以直接顺着 registry、runtime 和测试入口继续下钻，而不是复制文档里的过时映射字典

### 2.3 `chapter-structure-fields-design.md`
**思考强度：L2 + L3**

已完成的修正：

- 增加当前已落地入口说明：
  - `state-v5-template.json`
  - `state-schema-v5.json`
  - `state-schema.md`
  - `novel-outline` / `novel-review` / `novel-precheck`
  - 结构审计脚本
- 将“建议在 state schema 中添加”改为“当前已落地”
- 将“在 review 输出中添加”改为“当前 consumer 读取方式 + 典型摘要形态”
- 将完成标记改为与当前 schema / consumer / tests 现状一致

当前效果：

- 该文档不再把已经落地的章结构字段写成未来设计项
- 接手者可以直接顺着 schema、consumer 和审计测试继续下钻

---

## 三、本轮未主动改写项

**思考强度：L4 审慎**

以下文档虽然仍包含阶段、下一步、优先级或计划语义，但本轮没有主动改写，原因是它们本身就是“计划 / 模板 / 复检 / 扩面候选”文档，不能简单按“去历史化”处理：

1. [profile-expansion-candidate-priority-v1.5.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/profile-expansion-candidate-priority-v1.5.md)
   - 本质是候选排序文档，保留优先级语义是合理的

2. [profile-expansion-first-batch-v1.5.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/profile-expansion-first-batch-v1.5.md)
   - 本质是“第一批扩面完成说明”，仍承担阶段边界说明作用

3. [crossover-schema-alignment-v1.5.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/crossover-schema-alignment-v1.5.md)
   - 是 schema 对齐与策略文档，不适合简单做现状化压平

4. [project-knowledge-mcp.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/project-knowledge-mcp.md)
   - 仍保留“后续增强方向”，但属于产品边界说明，不是失真待办

5. [v1.5-next-mainline-preparation-2026-03-31.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/v1.5-next-mainline-preparation-2026-03-31.md)
   - 本身就是阶段判断文档，保留“下一步顺序”是合理的

---

## 四、后续若继续整理，建议顺序

**思考强度：L3 + L4**

如果后续继续做文档去历史化整理，建议优先顺序如下：

1. **Inventory / 盘点类文档**
   - 优先处理那些“标题像现状盘点，但正文仍像历史待办”的文档

2. **完成说明 / 阶段报告类文档**
   - 仅补“后续以新文档为准”的状态提示
   - 不直接重写其原始阶段结论

3. **计划 / 模板 / 策略类文档**
   - 默认不动
   - 除非它们的现状指向已经明显失真

---

## 五、本轮结论

**思考强度：L3 深度**

本轮文档去历史化整理已完成一轮低风险清理，重点成果是继续把 `bucket-overlay-inventory.md` 从“历史计划感”收口为“现状 + 历史样例 + 维护规则”文档，把 `bucket-profile-slug-mapping.md` 从“设计草稿 + 待实现 checklist”收口为“registry / runtime / 测试证据”入口，并把 `chapter-structure-fields-design.md` 从“建议接线”收口为“schema / consumer / 审计入口”文档。当前 `docs/00-当前有效/` 中仍存在一些带阶段语义的文档，但它们大多属于“本来就应该保留阶段属性”的文档类型，不宜为追求整齐而强行改写。

---

## 六、收尾判断

**思考强度：L4 审慎**

在补完本轮多轮低风险清理后，再次回扫 `docs/00-当前有效/`，当前剩余仍明显带有“阶段 / 下一步 / 优先级 / 持续复检”语义的文档，已主要集中在以下几类：

1. **计划 / 阶段判断文档**
   - `current-processing-plan-phased-v1.md`
   - `v1.5-next-mainline-preparation-2026-03-31.md`

2. **候选 / 排序 / 扩面文档**
   - `profile-expansion-candidate-priority-v1.5.md`
   - `profile-expansion-first-batch-v1.5.md`

3. **模板 / 检查清单 / 执行模板**
   - `maintenance-specialized-template-pack-v1.md`
   - `sample-regression-maintenance-checklist-v1.md`
   - `monthly-governance-phase-close-template-v1.md`

4. **复检 / 演练 / 长期维护面文档**
   - `v1.5-sample-regression-maintenance-review-2026-03-31.md`
   - `p0f-motif-input-layer-review-2026-03-31.md`
   - `registry-consumer-maintenance-drill-2026-03-31.md`
   - `sample-regression-maintenance-drill-2026-03-31.md`
   - `governance-maintenance-drill-2026-03-31.md`

这些文档当前之所以保留阶段语义，不是因为“历史残留尚未清掉”，而是因为：

- 它们本身承担计划、模板、候选排序、长期复检或执行演练职责
- 继续强行去历史化，反而会损失它们的使用边界
- 当前已经完成的低风险清理，主要集中在那些“标题像现状真源，但正文仍像旧待办”的文档；这一类高收益目标现在已基本处理完

### 当前收口结论

当前“当前有效文档去历史化整理”这条低风险治理线，可以认为已经达到收口条件：

- 已闭环的历史残留型文档已完成多轮清理
- review / drill / inventory / 设计稿之间的主要双口径已被压下去
- 剩余带阶段语义的文档，当前以“刻意保留”为主，而不是“误写成现状缺口”

因此，后续如继续推进，不应再以“批量去历史化”为默认动作，而应改成：

1. 仅在新增文档再次出现“现状真值 / 历史设计稿混写”时做定向修正
2. 或转向新的治理 / 维护主线
