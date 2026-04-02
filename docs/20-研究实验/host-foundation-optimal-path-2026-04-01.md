# 跨宿主基础层最优路径方案（高强度决策稿）

> Status: `research`
>
> 本文不是当前真值，而是站在 `v1.6` 已完成的前提下，对“下一步到底该怎么做才最优”做出的高强度决策稿。

## 结论先行

最优方案**不是**立刻推进完整 `v2` 重构。

最优方案是：

- **先抽离证据层**
- **先做 Trae 能力面审计**
- **设置一个显式决策门**
- **只有当现有 `v1` 结构确实表达不下时，才进入有界 `v2`**

换句话说，最优路径不是“预设要做大重构”，而是：

- **Evidence First, Then Decide**

这比“继续补 `v1`”更稳，也比“直接全面升级 `v2`”更克制、更低风险。

---

## 1. 这份方案试图解决什么问题

当前 `v1.6` 已经有：

- 宿主真值：`host-capability-matrix-v1.json`
- 消费层：`install-skills.sh`
- 投影层：`render_host_capability_projection.py`
- 自检层：`doctor_host_foundation.py`
- 文档层：`skill-usage.md`、`host-support-status-v1.6.md`

因此现在的问题不再是：

- “宿主基础层有没有搭起来”

而是：

- 这套结构**长期是不是最优**
- Trae 这种宿主到底要不要沿当前模型继续做
- 我们现在应不应该为了未来扩展提前重构

这是一个典型的“系统已经能用，但要不要在证据不足时提前架构升级”的问题。

---

## 2. 不可破坏的硬约束

任何被选中的下一步方案，都必须满足下面这些硬约束。

### 2.1 不破坏现有 `v1.6` consumer

以下资产已经进入当前稳定消费面：

- [install-skills.sh](/Users/arm/Desktop/vscode/Genm-codex/scripts/install-skills.sh)
- [render_host_capability_projection.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/render_host_capability_projection.py)
- [doctor_host_foundation.py](/Users/arm/Desktop/vscode/Genm-codex/scripts/doctor_host_foundation.py)
- [skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/skill-usage.md)
- [host-support-status-v1.6.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/host-support-status-v1.6.md)

因此下一步不能要求：

- 所有 consumer 同时迁移
- 当前 doctor 立刻重写
- 当前 matrix 一次性原地变形

### 2.2 不制造第二真值中心

当前项目已经明确拒绝新 runtime / daemon / plugin 真值中心。

因此下一步新增的任何结构都必须满足：

- 要么是**真值**
- 要么是**从真值派生的投影**

不能出现：

- 两份都像真值、但语义略有重叠的数据文件

### 2.3 宿主承诺必须可证据化

后续状态升级不能只靠口头判断。

因此必须支持这类问题：

- 为什么 `Claude` 是 `baseline / partial`
- 为什么 `Trae` 现在仍然不是 installable host
- 为什么某个能力面只到 `doc_verified`

### 2.4 Trae 不能按 Codex/Claude 模型硬套

当前官方文档已经证明 Trae 至少公开了：

- Rules
- Skills
- MCP
- Agent 中使用 MCP
- Auto-run
- Sandbox

因此 Trae 已经不是“完全空白宿主”。

但我们也还没拿到：

- 全局 skill 路径
- 项目 skill 发现机制
- repo-owned 安装可行性

所以最优方案必须允许：

- 某些能力面先 `doc_verified`
- 某些能力面仍 `unknown / unsupported`

### 2.5 当前收益必须大于迁移成本

如果一个方案：

- 架构更漂亮
- 但短期不能提升判断精度
- 还会引入大量兼容代码

那它就不是当前最优。

---

## 3. 备选方案对比

## 方案 A：继续补 `v1`

做法：

- 继续在 `host-capability-matrix-v1.json` 上加字段
- 遇到 Trae 不够表达时再加一两个字段
- doctor / projection / docs 跟着一起补

优点：

- 最省改动
- 最快见效
- 不需要新 projection

缺点：

- 继续混合承诺、证据和观察
- Trae 这种“按能力面部分明确”的宿主会越来越难表达
- 每次升级状态都更容易触发全链修改

结论：

- **短期最省事**
- **长期不是最优**

## 方案 B：立刻做完整 `v2`

做法：

- 立即引入：
  - `host-support-policy-v2`
  - `host-evidence-ledger-v1`
  - 能力面模型
- 再做兼容 projection 回 `v1`

优点：

- 架构最整洁
- 长期扩展性最好
- 对 Trae 表达力最强

缺点：

- 证据还不够时，容易先把模型做复杂
- 现在就做，很可能把猜测写进结构
- 迁移负担高

结论：

- **长期上限高**
- **当前时点过早**

## 方案 C：先证据层，再设决策门，再决定是否上 `v2`

做法：

1. 先新增证据层
2. 先做 Trae capability review
3. 在拿到结果后判断：
   - 现有 `v1` 是否还够表达
   - 如果不够，再做有界 `v2`

优点：

- 先解决真正的信息缺口
- 不预设重构
- 保留向 `v2` 演进的路径
- 最符合“证据优先”的项目风格

缺点：

- 看起来不如“直接重构”痛快
- 需要接受一次显式决策门，而不是一口气干完

结论：

- **当前最优**

## 方案 D：完整能力图谱正规化

做法：

- 额外引入：
  - capability surface catalog
  - host surface map
  - evidence ledger
  - policy layer
  - multi-step compatibility projection

优点：

- 理论上最规范
- 宿主和能力面完全解耦

缺点：

- 明显过度设计
- 对 5 个宿主来说成本太高
- 当前收益远低于维护负担

结论：

- **现在不是最优**

---

## 4. 选型结论

当前最优路线是：

- **方案 C：Evidence First + Decision Gate**

原因不是它最“炫”，而是它同时满足：

1. 不破坏 `v1.6`
2. 不预设过度重构
3. 能先解决 Trae 这种真正的未知数
4. 给未来 `v2` 留出了正确入口

最重要的是：

- 它能把“不知道的东西”先变成“知道”

而不是把“不知道的东西”先编码成结构。

---

## 5. 最优执行方案

### Phase A：证据层抽离

目标：

- 把“为什么敢做这个承诺”从 `v1` 主真值中拆出来

新增：

- `shared/templates/host-evidence-ledger-v1.json`
- `shared/templates/host-evidence-ledger-v1.schema.json`

最低支持的证据类型：

- `official_doc`
- `repo_file`
- `runtime_observation`
- `manual_verification`
- `doctor_result`

Acceptance Criteria：

- 能记录每条证据的：
  - `host_id`
  - `surface`
  - `kind`
  - `ref`
  - `summary`
  - `verified_at`
  - `confidence`
- 当前 `v1.6` consumer 不依赖它才能工作

### Phase B：Trae Capability Review

目标：

- 用官方文档和最小手工验证，给 Trae 做逐能力面判级

新增研究文档：

- `docs/20-研究实验/trae-capability-review-2026-04-01.md`

必须回答的 5 个问题：

1. `Global skills` 的本地路径是什么
2. `Project skills` 的发现方式是什么
3. 是否支持 repo-owned 目录直接落盘后发现
4. MCP 配置是 UI-only 还是支持文件源
5. `Auto-run + sandbox` 是否足够承担 hooks-like automation

Acceptance Criteria：

- 每个结论都至少有：
  - `official_doc`
  - 或 `manual_verification`
- 不再把 Trae 笼统视为“只有 rules/context”

### Gate 1：是否真的需要 `v2`

在完成 Phase A + B 后，做一次明确判断：

#### 如果满足以下任一条件，则继续维持 `v1.x`

- Trae 的新增事实只需要提升证据等级，不需要新表达结构
- 当前 `supports_* + install_mode + degrade_policy` 仍能清晰表达承诺
- 新增 consumer 仍能直接吃 `v1`

那么最优做法是：

- **不做 `v2`**
- 只做 `v1.6.1` 级别增强

#### 只有在以下条件成立时，才进入 `v2`

- 至少一个宿主出现“当前 `v1` 无法清楚表达”的能力面状态
- 证据与承诺分离已经成为真实维护负担
- Trae 或未来宿主确实需要“按能力面承诺”而不是“按宿主承诺”

### Phase C：有界 `v2`

如果进入 `v2`，建议采用**有界分层**，不是全量图谱重构。

新增：

- `host-support-policy-v2`

但**不新增**单独的 capability catalog 真值文件。

理由：

- 当前还没多到需要独立 catalog
- 直接把能力面 enum 收进 `policy-v2` schema 就够了
- 可以避免设计复杂度过早膨胀

### Phase D：兼容投影

目标：

- 新结构不直接替换 `v1`
- 先投影回兼容视图

投影目标：

- `host-capability-matrix-v1` compat
- `host-support-status` 文档
- `doctor` summary

Acceptance Criteria：

- 老 consumer 无需同时迁移
- `install-skills.sh` 可继续稳定工作
- doctor 能同时解释承诺和证据

---

## 6. 为什么这是“真的更优”

这条路线比“直接上 `v2`”更优，原因在于：

### 6.1 它先解决信息不对称，而不是先解决结构焦虑

Trae 当前真正缺的是信息，不是 schema。

如果先重构 schema，很可能只是把不确定性编码成了更复杂的数据结构。

### 6.2 它保留了真正的回头空间

如果 Trae 审计后发现：

- `v1` 其实够用

那么这条路线允许我们：

- 停在 `v1.6.1`

而不是为了已经开始的 `v2` 重构继续硬做。

### 6.3 它把“必要复杂度”和“过度设计”分开了

引入证据层是必要复杂度。

立刻引入完整能力图谱不是。

### 6.4 它更符合这个仓库当前的治理哲学

这个仓库的成熟路径一直是：

- 先 contract
- 再 projection
- 再 consumer
- 最后才提升默认真值

因此最优方案必须延续这个节奏，而不是因为 Trae 有新信号就直接重做底层。

---

## 7. 非目标

这份方案明确不建议：

- 直接把 Trae 从 `unsupported` 提升成 installable host
- 直接把 `host-capability-matrix-v1` 改成复杂嵌套结构
- 立即做 capability graph normalization
- 为每个宿主单独写一套新的 adapter 脚本
- 在没有决策门的情况下直接发起 `v2`

---

## 8. 最终建议

如果要我以“超高强度思考”只给一个结论，那就是：

- **先做证据层和 Trae 审计，再决定要不要重构。**

这比“继续修补 `v1`”更进化，也比“立刻做 `v2`”更克制。

一句话说：

- **当前真正的最优解，不是更快重构，而是更晚承诺。**
