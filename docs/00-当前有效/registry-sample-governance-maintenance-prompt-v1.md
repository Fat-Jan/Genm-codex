# Registry / Sample / Governance 维护执行提示词 v1

> 目的：把当前已经稳定下来的三条维护线——registry、sample / regression、governance——整理成一份可以直接交给其他 agent 执行的统一提示词 / 检查清单。
>
> 适用对象：协作 agent、执行 agent、复检 agent。
>
> 使用方式：执行 agent 直接按本文步骤推进；主 agent 再按本文末复检要点审查结果。

---

## 一、适用范围

本提示词适用于以下 3 类维护任务：

1. **Registry / Consumer 边界维护**
   - bucket / strong_tags / tagpacks / narrative_modes / tone_guardrails
   - bucket overlay
   - consumer 读取边界
   - `novel-scan` sidecar 边界

2. **Sample / Regression 维护**
   - `sample-manifest-v1.json`
   - sample library index / matrix
   - regression 样本
   - bucket sample
   - smoke / baseline / derived / high_confidence 分层

3. **Governance 常态维护**
   - weekly snapshot
   - biweekly review
   - monthly phase close
   - shared 三域治理状态
   - 文档与现状一致性

---

## 二、统一执行原则

### 2.1 思考强度规则

| 任务类型 | 默认思考强度 | 说明 |
|---|---|---|
| 整理、抄录、状态核对 | L1 / L2 | 快速完成，不做过度推理 |
| 常规对比、归类、交叉核对 | L2 | 做必要上下文比对 |
| 异常定性、边界判断、风险分析 | L3 | 做多源证据综合 |
| 是否升级、是否裁决、是否改边界 | L4 | 保守判断，避免越权 |

### 2.2 默认边界

执行时默认遵循：

1. **现状优先**
   - 先看仓库当前文件与测试状态
   - 再看旧文档与历史说明

2. **manifest / contract / sidecar-first**
   - machine-readable 真值优先于人读索引
   - 当前 contract 优先于旧草案
   - sidecar 是辅助输入，不是 canon

3. **不把历史计划误判成当前缺口**
   - 若文档本身是计划 / 模板 / 候选排序文档，不强行现状化
   - 若文档标题像现状盘点，但正文像历史待办，才优先整理

4. **不越权升级结构**
   - 不因维护任务顺手扩大 `novel-scan` 权限
   - 不把 registry 层改成第二真值系统
   - 不把 bucket sample 默认升级成 regression 样本

---

## 三、执行前输入材料

执行 agent 开始前，至少准备：

### 3.1 Registry / Consumer 维护所需
- `docs/00-当前有效/profile-calibration-and-bucket-mapping.md`
- `docs/00-当前有效/bucket-overlay-inventory.md`
- `docs/00-当前有效/scan-result-contract.md`
- `docs/00-当前有效/novel-scan-usage-and-source-matrix-v1.5.md`
- `docs/00-当前有效/skill-usage.md`
- 相关 skill 文档（如 `skills/novel-query/SKILL.md`）

### 3.2 Sample / Regression 维护所需
- `shared/templates/sample-manifest-v1.json`
- `docs/00-当前有效/sample-library-governance-v1.5.md`
- `docs/00-当前有效/sample-library-index.md`
- `docs/00-当前有效/sample-library-matrix-v1.5.md`
- `docs/00-当前有效/sample-regression-maintenance-checklist-v1.md`
- 相关测试文件

### 3.3 Governance 维护所需
- `docs/00-当前有效/steady-governance-rhythm-v1.md`
- `docs/00-当前有效/monthly-governance-phase-close-template-v1.md`
- 最近一轮 weekly / biweekly / monthly 文档
- `docs/00-当前有效/current-effective-docs-hygiene-log-2026-03-31.md`

---

## 四、统一执行步骤

### Step 1：先确认任务属于哪一类
**思考强度：L2**

执行前先判断当前任务主要属于：

- Registry / Consumer 维护
- Sample / Regression 维护
- Governance 常态维护
- 文档一致性整理

如果同时跨多类，先拆成子块，不要混做。

---

### Step 2：读取当前 machine-readable 或 contract 真值
**思考强度：L2**

优先读取：

- manifest
- contract
- sidecar
- 当前有效规则文档
- 当前测试 / 验证入口

不要先从旧阶段说明反推现状。

---

### Step 3：判断是“现状缺口”还是“历史语义残留”
**思考强度：L3**

判断规则：

- 如果文件 / 测试 / contract 真实缺失，算现状缺口
- 如果实现已存在，只是文档仍写成“待实现”，算历史语义残留
- 如果文档本来就是计划 / 模板 / 候选排序，默认不算残留问题

---

### Step 4：按任务类型执行

#### A. Registry / Consumer
**思考强度：L3 + L4**

至少检查：

- `bucket` 是否仍是单主桶
- `strong_tags / tagpacks / narrative_modes / tone_guardrails` 是否仍各司其职
- `bucket overlay` 是否被写成当前已落地还是历史计划
- `novel-scan` 是否仍保持：
  - 可消费
  - 不主链化
  - 不改 canon
- consumer 是否把 sidecar 当 soft guidance，而不是真值入口

可执行动作：

- 修正文档中把已完成事项写成待办的表述
- 补充边界说明
- 记录低风险文档一致性问题

不要做：

- 顺手扩大 `novel-scan` 权限
- 把 registry 层升级为第二真值系统

#### B. Sample / Regression
**思考强度：L2 + L3 + L4**

至少检查：

- 是否 manifest-first
- regression 样本是否写清退化目标
- bucket sample 是否被误当 regression
- index / matrix 是否仍只是浏览层
- 测试入口是否与样本层级一致

可执行动作：

- 先改 manifest，再改索引 / 矩阵 / 治理文档
- 补 `verification_targets`
- 对样本做状态修正

不要做：

- 只改 index，不改 manifest
- 增加 regression 样本却不说明它防什么

#### C. Governance
**思考强度：L2 + L3 + L4**

至少检查：

- 当前属于 weekly / biweekly / monthly 哪种节奏
- shared 三域是否稳定
- 是否有 orphan / declared-only / drift / protected 异常波动
- 当前文档是否与验证结果一致

可执行动作：

- 周快照记录
- 双周异常定性
- 月度阶段收口
- 低风险文档残留整理

不要做：

- 在 weekly 阶段顺手发起大规模专项
- 把报表信号直接写成确认事实

---

### Step 5：输出结果时必须区分三类状态
**思考强度：L3**

每项发现都要归入：

1. **现状已稳定**
2. **低风险历史残留 / 文档语义问题**
3. **真实未闭环项 / 需升级项**

不要把这三类混写。

---

## 五、标准输出结构

执行 agent 输出时，至少包含：

### 1. 输入材料
- 本轮读取的 manifest / contract / 文档 / 测试

### 2. 执行摘要
- 本轮检查对象
- 总体结论
- 是否有中高风险问题

### 3. 检查结果
建议表：

| 项目 | 当前状态 | 证据 | 结论 | 风险 | 建议动作 |
|---|---|---|---|---|---|

### 4. 已处理项
- 本轮已实际修正的文档 / 配置 / 状态

### 5. 保留项
- 哪些项虽然有历史语义，但当前不应强改

### 6. 是否需要升级
- 不需要
- 需要低风险后续整理
- 需要主 agent 裁决

---

## 六、主 agent 复检要点

主 agent 复检时，优先看：

1. 是否先看了 manifest / contract / 当前测试，而不是只看旧文档
2. 是否区分了“现状缺口”与“历史语义残留”
3. 是否把 sidecar / market guidance / registry 数据误判成真值
4. 是否把计划型文档错误地当成待修文档
5. 是否在低风险范围内做了保守整理，而没有顺手扩大结构改动

---

## 七、可直接复制给 agent 的提示词

```md
请对 Genm-codex 执行一轮维护检查，范围覆盖 registry / sample / governance 三条维护线中的当前目标项。

执行要求：
1. 先判断当前任务属于 registry、sample、governance 还是文档一致性整理
2. 优先读取 machine-readable 真值、contract、sidecar、当前有效规则文档与测试入口
3. 区分“真实现状缺口”与“历史语义残留”
4. 低风险项可直接整理，涉及边界升级或结构变化时必须保守
5. 输出结果时必须区分：
   - 现状已稳定
   - 低风险历史残留
   - 真实未闭环项
6. 每个步骤标注思考强度：L1 / L2 / L3 / L4
7. 若有改动，最后运行：
   - `bash scripts/validate-migration.sh`

输出结构至少包括：
- 输入材料
- 执行摘要
- 检查结果表
- 已处理项
- 保留项
- 是否需要升级
```

---

## 八、结论

**思考强度：L3 深度**

这份文档的定位不是新的治理计划，而是把当前已经收口的 registry / sample / governance 维护动作，下沉成一个 agent 可以直接执行的统一入口。后续如果继续协作，执行 agent 不需要再自己重新发明检查结构，只要按本文走即可。
