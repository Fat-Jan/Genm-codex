# Shared 资产治理阶段报告 v1

> 治理周期：2026-03-31
>
> 本报告覆盖：profiles 域、references 域的系统性巡检，以及对应的治理动作。
>
> 前序阶段：[phase-9-summary.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/phase-9-summary.md)、[phase-7b-selective-sync-governance.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/phase-7b-selective-sync-governance.md)

---

## 一、执行摘要

本轮治理完成了三项核心工作：

1. **Profiles 域系统性巡检**：验证了 50 个 complete profiles 的稳定保留门槛达成情况
2. **References 域系统性巡检**：验证了 10 个保护项的保护合理性
3. **Profiles 稳定保留门槛清单**：将从试点经验中归纳的判断框架固化为可复用文档

**核心结论**：Profiles 域和 References 域整体处于高质量状态，无需大规模保护名单收缩。

---

## 二、本轮实际执行的治理动作

### 2.1 维持保护名单版本升级

- `sync-governance.json` 版本：`1.1` → `1.2`

### 2.2 Orphan 文件归档

已归档 3 个确定 orphan 文件，不再受治理保护：

| 文件 | 归档原因 |
|---|---|
| `shared/references/commands/novel-review.md` | 无任何消费，governance 保护意图残留 |
| `shared/templates/chapter-structure/template-validation-rules.md` | Validator 概念已迁移至脚本和 gate policy |
| `shared/validators/post-write-validator.md` | Validator 概念已迁移至脚本和 gate policy |

对应归档文档：[orphan-asset-archive-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/orphan-asset-archive-v1.md)

### 2.3 SKILL.md 依赖声明降级

将 5 个 SKILL 中对 `consumer-read-manifest.md` 的声明从 `Read ... first` 降级为 `Reference`：

- `skills/novel-review/SKILL.md`
- `skills/novel-outline/SKILL.md`
- `skills/novel-package/SKILL.md`
- `skills/novel-precheck/SKILL.md`
- `skills/novel-write/SKILL.md`

原因：该文件属于典型 declared-only 幻觉——被多处声明引用，但无任何程序消费者。

### 2.4 Genre 保护名单收缩（三批试点）

从 `templates.protected_local_paths` 中移出 16 个弱证据 genre 文件：

**第一批（4 个）**：`克苏鲁`、`直播文`、`知乎短篇`、`黑暗题材`

**第二批（6 个）**：`女频悬疑`、`年代`、`悬疑脑洞`、`现实题材`、`规则怪谈`、`都市异能`

**第三批（6 个）**：`抗战谍战`、`无限流`、`末世`、`电竞`、`种田`、`高武`

当前保留的 genre 保护项（9 个）均为强联动组或 creative-brief 默认映射主入口。

### 2.5 References 边缘项保护移出

将 2 个弱证据 reference 从 `references.protected_local_paths` 移出：

- `chapter-index-schema.md`
- `serial-generation-mode.md`

原因：经复核，这两个文件仅在治理名单和互相引用中存在，无 skills/scripts/tests 直接消费证据，属于历史方案文档而非当前主流程核心 reference。

---

## 三、Profiles 域巡检结论

### 3.1 核心数据

从 [batch-evidence-sidecar.json](file:///Users/arm/Desktop/vscode/Genm-codex/docs/10-进行中/batch-evidence-sidecar.json)：

| 指标 | 数值 |
|---|---|
| complete | 50 |
| partial | 1（zhihu-short） |
| exception | 1（zhihu-short） |

### 3.2 关键发现

**全部 50 个 complete profiles，ontology_ready = true**

这意味着：
- 这 50 个 profiles 全部满足五维框架的"题材本体可上升"要求
- 历史上曾经 partial 或被降级的 profiles（如 cthulhu、livestream、gaowu）均已在本次周期内补证完成
- 唯一 partial 的 zhihu-short 是明确特殊例外（zhihu-primary-source），不适用默认三平台对齐标准

### 3.3 Profiles 稳定保留门槛清单

通过 gaowu / cthulhu / livestream / realistic / workplace-romance 五个试点样本，归纳出一套五维检查框架：

| 维度 | 检查内容 | 关键判断 |
|---|---|---|
| 结构完整性 | 三件套是否齐全 | core + bucket overlay + platform overlay |
| 运行投影可读 | 测试能否读出 bucket / strong_tags / tone_guardrails | profile contract 测试断言 |
| 测试兜底覆盖 | 是否有 profile contract 测试用例 | 测试用例存在且断言明确 |
| 跨平台证据状态 | sidecar 是否为 complete / ontology_ready / exception=false | batch-evidence-sidecar.json |
| 题材本体可上升 | 是否在 ontology 决策文档中有"可上升"标注 | genre-ontology-field-decisions-v1.5.md |

详细清单：[profile-stability-threshold-checklist-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/profile-stability-threshold-checklist-v1.md)

### 3.4 三种污染/补证路径

| 类型 | 代表样本 | 补证路径 |
|---|---|---|
| 正常补证完成 | gaowu | 补入晋江 A 级实体页 |
| 污染修复完成 | cthulhu | 替换被污染的 URL（晋江 novelid=10267899 → 9455935） |
| 官方分类页补证完成 | livestream | 用平台官方分类/培训页补证（不等同于具体作品页） |

### 3.5 结论

**Profiles 域整体高质量，无需大规模保护名单收缩。**

存在问题不是"保护过多"，而是历史上部分 profile 曾有 evidence 污染或不足，但这些问题已被系统性补正。当前 profiles 域适合建立**持续巡检机制**，而不是集中收缩。

---

## 四、References 域巡检结论

### 4.1 当前保护状态

| 指标 | 数值 |
|---|---|
| protected local paths | 10 |
| local-only paths | 7 |
| same-path drift paths | 5 |

### 4.2 全部 10 个保护项分类

| 分类 | 文件数 | 包含项 |
|---|---|---|
| Skill 软消费保留 | 4 | `core-constraints.md`、`state-schema.md`、`character-naming-guide.md`、`worldview-motif-catalog.md` |
| 典型 declared-only 幻觉（已处理） | 1 | `consumer-read-manifest.md`（已降级为 Reference） |
| Local-only 核心保留 | 5 | `chapter-transaction-schema.md`、`truth-files-guide.md`、`truth-files-spec.md`、`ancient-household-kinship-guide.md`、`ancient-office-hierarchy-guide.md` |

### 4.3 关键发现

- `consumer-read-manifest.md` 属于典型 declared-only 幻觉：被 5 个 skill 声明引用，但无任何 scripts/tests 程序消费者。已在 SKILL.md 降级中处理。
- `state-schema.md` 在 tests 中被多次读取，但这是正常的 schema 验证测试，不影响其作为 reference 文档的性质。
- `chapter-index-schema.md` 和 `serial-generation-mode.md` 已在本轮移出保护名单。

### 4.4 结论

**References 域保护名单基本健康，无明显"保护过当"项。**

已处理的 declared-only 幻觉（consumer-read-manifest）和边缘 drift 项（chapter-index-schema、serial-generation-mode）已在前序治理动作中处理。当前保护名单其余项均有合理保留理由。

---

## 五、Templates 域（基于前序工作）

### 5.1 本轮Templates 域治理动作

**Genre 保护名单收缩（16 个文件）**

已完成三批试点，共移出 16 个弱证据 genre 文件。当前保留的 genre 保护项均为强联动组或 creative-brief 默认映射主入口。

### 5.2 Templates 保护名单现状

`templates.protected_local_paths` 从 53 下降到 37。

### 5.3 Templates 域结论

Templates 域的 genre 类别已从"整组保护"转变为"证据驱动保护"。核心 schema/template 文件（如 state-schema-v5.json、state-v5-template.json、learned-patterns-template.json、profile-bucket-registry-v1.json 等）均已确认具有 scripts/tests 消费证据，继续保护合理。

---

## 六、治理方法论总结

### 6.1 从本轮工作中归纳的核心原则

1. **不能只靠单一证据判定**：一个维度达标不等于整体达标
2. **历史记录不等于当前状态**：曾经的 partial 或污染，不代表现在仍有问题
3. **exception ≠ 无效**：带例外说明的对象，需单独评估例外原因
4. **补证路径多元**：具体作品页、平台官方分类页、培训页等均可作为有效 evidence
5. **drift 不等于该删**：drift 只说明本地与上游不同步，不等于无价值或应删除

### 6.2 域适配的治理策略

| 域 | 消费类型 | 治理策略 |
|---|---|---|
| profiles | 运行时消费者明确（测试/.mighty/state.json） | 建立稳定保留门槛清单，持续巡检 |
| references | 消费链最隐性（多为 skill 声明引用） | 关注 declared-only 幻觉，区分软消费与硬消费 |
| templates | 多为数据模板（被脚本读取） | 以 scripts/tests 消费证据为主要判断依据 |

### 6.3 本轮建立的可复用资产

- [profile-stability-threshold-checklist-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/profile-stability-threshold-checklist-v1.md)：Profiles 稳定保留门槛检查清单
- [orphan-asset-archive-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/orphan-asset-archive-v1.md)：Orphan 资产归档记录

---

## 七、当前状态快照

### 7.1 sync-governance.json 关键指标

| 域 | 初始值 | 当前值 | 变化 |
|---|---|---|---|
| templates protected | 53 | 37 | -16 |
| references protected | 12 | 10 | -2 |
| version | 1.1 | 1.2 | +0.1 |

### 7.2 已归档文件

3 个 orphan 文件已归档，不再受治理保护。

### 7.3 SKILL.md 声明降级

5 个 SKILL 中对 `consumer-read-manifest.md` 的声明已从 `Read ... first` 降级为 `Reference`。

---

## 八、待处理事项

| 优先级 | 事项 | 说明 |
|---|---|---|
| 低 | Profiles 持续巡检机制建立 | 以 checklist 为基准定期巡检新 profile 准入和现有 profile 状态 |
| 低 | Templates 域 schema/template 进一步巡检 | 用 scripts/tests 消费证据巡检核心模板资产 |
| 低 | Governance schema 升级 | 考虑引入 repo-owned/local-owned/overlay-owned 三态或 evidence 等级元数据 |
| 已处理 | Orphan 清理 | 本轮已完成 |
| 已处理 | consumer-read-manifest 幻觉降级 | 本轮已完成 |
| 已处理 | genre 保护名单收缩 | 本轮已完成 |
| 已处理 | references 边缘项移出 | 本轮已完成 |

---

## 九、验证结果

本轮所有治理动作后均运行了验证脚本：

```bash
bash scripts/validate-migration.sh      # 结果：通过
bash scripts/sync-shared-from-genm.sh --report  # 结果：成功输出
```

---

## 十、版本记录

| 版本 | 日期 | 更新内容 |
|---|---|---|
| v1 | 2026-03-31 | 初始版本，覆盖本轮 profiles + references 域系统性巡检与治理动作 |
