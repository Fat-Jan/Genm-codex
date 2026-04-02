# 维护专项执行模板包 v1

> 目的：把当前已经稳定的维护体系拆成 4 份更细的执行模板，方便直接交给不同 agent 分工执行，再由主 agent 统一复检。
>
> 组成：
>
> 1. Registry / Consumer 维护执行模板
> 2. Sample / Regression 维护执行模板
> 3. Governance 常态巡检执行模板
> 4. 主 agent 复检模板

---

## 一、使用说明

**思考强度：L2 标准**

使用方法：

1. 先确定本轮任务属于哪类专项
2. 直接复制对应模板给执行 agent
3. 执行 agent 按模板输出结果
4. 主 agent 再按本文最后的复检模板进行复检

默认规则：

- 低风险维护动作可直接执行
- 涉及边界升级、真值改写、结构扩权时必须保守
- 所有模板都要求标注思考强度（L1 / L2 / L3 / L4）
- 所有执行完成后，若有改动，默认运行：
  - `bash scripts/validate-migration.sh`

---

## 二、模板 A：Registry / Consumer 维护执行模板

### 适用场景

- bucket / tagpacks / strong_tags / narrative_modes / tone_guardrails 读面维护
- bucket overlay 现状整理
- consumer 边界复检
- `novel-scan` sidecar 使用边界检查

### 可直接复制给 agent 的提示词

```md
请执行一轮 Genm-codex 的 Registry / Consumer 维护检查。

目标：
1. 确认 registry 层当前是否仍保持单主桶与多 overlay 分工
2. 确认 consumer 是否把 registry 当成约束层而不是真值重写入口
3. 确认 novel-scan 是否仍保持“可消费但不主链化、可参考但不改 canon”的边界
4. 若发现低风险文档语义残留，可直接整理

输入材料至少包括：
- docs/00-当前有效/profile-calibration-and-bucket-mapping.md
- docs/00-当前有效/bucket-overlay-inventory.md
- docs/00-当前有效/scan-result-contract.md
- docs/00-当前有效/novel-scan-usage-and-source-matrix-v1.5.md
- docs/00-当前有效/skill-usage.md
- 相关 skill 文档（如 skills/novel-query/SKILL.md）

执行要求：
1. 先判断当前差异属于“现状缺口”还是“历史语义残留”
2. 至少检查：
   - bucket 是否仍是单主桶
   - strong_tags / tagpacks / narrative_modes / tone_guardrails 是否各司其职
   - bucket overlay 是否被错误写成待实现
   - novel-scan 是否仍为 soft guidance / candidate 输入，而不是真值入口
3. 低风险文档问题可直接处理
4. 不得顺手扩大 novel-scan 权限，不得把 registry 层升级成第二真值系统
5. 标注每个主要步骤的思考强度
6. 如有改动，最后运行：bash scripts/validate-migration.sh

输出结构至少包括：
- 输入材料
- 执行摘要
- 检查结果表
- 已处理项
- 保留项
- 是否需要升级
```

---

## 三、模板 B：Sample / Regression 维护执行模板

### 适用场景

- sample manifest 维护
- sample index / matrix 同步
- regression 样本维护
- bucket sample / smoke / baseline 分层检查

### 可直接复制给 agent 的提示词

```md
请执行一轮 Genm-codex 的 Sample / Regression 维护检查。

目标：
1. 确认样本体系仍然遵循 manifest-first
2. 确认 regression 样本仍然遵循 regression-target-first
3. 确认 bucket sample 没有被误当 regression 样本
4. 确认 index / matrix 仍是浏览层，而不是 machine-readable 真值入口

输入材料至少包括：
- shared/templates/sample-manifest-v1.json
- docs/00-当前有效/sample-library-governance-v1.5.md
- docs/00-当前有效/sample-library-index.md
- docs/00-当前有效/sample-library-matrix-v1.5.md
- docs/00-当前有效/sample-regression-maintenance-checklist-v1.md
- 相关测试文件

执行要求：
1. 先从 manifest 与测试入口确认现状，再看 index / matrix
2. 至少检查：
   - manifest 条目是否与索引页一致
   - regression 样本是否写清 verification_targets 或等价退化目标
   - bucket sample 是否仍承担题材覆盖而不是 regression 责任
   - 是否存在只更新索引、不更新 manifest 的情况
3. 低风险同步问题可直接处理
4. 不得把 bucket sample 默认升级成 regression 样本
5. 标注每个主要步骤的思考强度
6. 如有改动，最后运行：bash scripts/validate-migration.sh

输出结构至少包括：
- 输入材料
- 执行摘要
- 检查结果表
- 已处理项
- 保留项
- 是否需要升级
```

---

## 四、模板 C：Governance 常态巡检执行模板

### 适用场景

- weekly snapshot
- biweekly review
- monthly phase close
- shared 三域治理稳定性检查
- 低风险文档残留整理

### 可直接复制给 agent 的提示词

```md
请执行一轮 Genm-codex 的 Governance 常态巡检。

目标：
1. 结合当前节奏（weekly / biweekly / monthly）完成对应治理检查
2. 确认 shared 三域当前是否稳定
3. 区分报表信号、低风险文档残留和真实异常
4. 对低风险已确认项可直接整理，对高风险项保守升级

输入材料至少包括：
- docs/00-当前有效/steady-governance-rhythm-v1.md
- docs/00-当前有效/monthly-governance-phase-close-template-v1.md
- 最近一轮 weekly / biweekly / monthly 文档
- docs/00-当前有效/current-effective-docs-hygiene-log-2026-03-31.md

执行要求：
1. 先确认当前任务属于 weekly / biweekly / monthly 哪一种
2. 运行并核对：
   - bash scripts/validate-migration.sh
   - bash scripts/sync-shared-from-genm.sh --report （若任务需要）
3. 至少检查：
   - protected / local-only / drift / source-only 是否稳定
   - 是否有 orphan / declared-only / 残留引用 / 文档失真
   - 当前文档是否把历史计划误写成现状缺口
4. 报表信号不得直接写成确认事实
5. 标注每个主要步骤的思考强度
6. 若处理了低风险项，保留变更说明

输出结构至少包括：
- 输入材料
- 执行摘要
- 指标或异常表
- 已处理项
- 保留项
- 是否需要升级专项治理
```

---

## 五、模板 D：主 agent 复检模板

### 适用场景

- 对其他 agent 已交付的 registry / sample / governance 结果做统一复检

### 可直接复制给主 agent / 复检 agent 的提示词

```md
请对本轮执行 agent 的交付物做复检，重点检查：

1. 是否优先读取了 manifest / contract / sidecar / 当前测试，而不是只看旧文档
2. 是否区分了：
   - 现状已稳定
   - 低风险历史语义残留
   - 真实未闭环项
3. 是否把 registry / sidecar / novel-scan / sample 层误判成真值或主链
4. 是否把计划型文档错误当成失真文档强行改写
5. 是否对高风险项保持了保守边界
6. 如果有改动，验证是否通过

复检输出至少包括：
- 复检范围
- 通过项
- 发现的问题
- 是否需要回改
- 最终结论（通过 / 基本通过 / 部分通过 / 不通过）
```

---

## 六、主 agent 复检要点表

**思考强度：L3 + L4**

| 检查项 | 通过标准 |
|---|---|
| 是否先看真值入口 | 优先看 manifest / contract / sidecar / 当前测试 |
| 是否区分现状缺口与历史残留 | 未混写 |
| 是否保守处理边界项 | 未扩大 scan / registry 权限 |
| 是否保持样本分层正确 | bucket sample 未被误当 regression |
| 是否保持治理节奏正确 | weekly / biweekly / monthly 未混做 |
| 是否运行验证 | 改动后已跑 `validate-migration.sh` |

---

## 七、结论

**思考强度：L3 深度**

这份模板包的定位，是把统一维护提示词继续拆细，变成 4 份可直接分发的专项执行模板。这样后续如果需要多人协作，不必每次重新拼装提示词，直接按任务类型分发即可。
