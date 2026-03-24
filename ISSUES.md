# 问题清单（2026-03-24，已归档）

> 基于对仓库整体代码、技能合同、文档结构、脚本、测试和工作流的全量审查生成。
> 归档更新：2026-03-25
> 最新验证：204 passed，0 failed；`bash scripts/validate-migration.sh` passed。
> 当前状态：下列问题均已处理，本文保留为审查记录与归档单，不再作为开放 issue 列表。

---

## P0 — 真实功能缺口（有无声失效风险）

### P0-1 · `novel-write/SKILL.md` 第 10 步编号重复

**状态：** 已处理并归档（2026-03-25）

**位置：** `skills/novel-write/SKILL.md:141` 和 `:153`

两个完全不同的步骤都编号为 `10.`：
- 第一个 `10.`（:141）：处理写作执行基本功（说明/对白/summary-heavy 检查）
- 第二个 `10.`（:153）：处理番茄平台 bucket 写法规则

执行 skill 的 AI 在跑 workflow 时遇到两个 `10.` 会产生理解歧义，且无法确保两条规则都被激活。第二个应改为 `11.`，后续步骤依次顺延。

**归档说明：**
- 已在 `skills/novel-write/SKILL.md` 中改为顺序编号：执行基本功为 `10.`，番茄 bucket 规则为 `11.`，后续步骤整体顺延。

---

### P0-2 · `fanqie_launch_stack.py` 在起盘工作流中没有触发时机

**状态：** 已处理并归档（2026-03-25）

**相关文件：** `docs/default-workflows.md`、`docs/start-here.md`、`scripts/fanqie_launch_stack.py`

默认工作流 1（新书起盘）的步骤链为：
```
novel-init → novel-genre → 家谱/官制 → novel-outline → setting gate → novel-package
```

`fanqie_launch_stack.py --mode draft` 的运行时机完全不在这条主线里。`start-here.md` 第 1 步也没有它。

**结果：** `.mighty/launch-stack.json` 在整个起盘和正文阶段全程为空。`novel-write`/`novel-review`/`novel-precheck`/`novel-package` 都有"当文件存在时消费 `launch-stack` 字段"的合同，但文件空则静默跳过，等于这一层规则对番茄项目完全没生效。

**建议最小修复：**
- 在 `default-workflows.md` 工作流 1 的 `novel-outline` → `setting gate` 之间插入：
  ```
  python3 scripts/fanqie_launch_stack.py --project-root <project_root> --mode draft
  （番茄平台项目必选；非番茄项目可选）
  ```
- `start-here.md` 第 1 步流程同步更新

**归档说明：**
- 已在 `docs/default-workflows.md`、`docs/start-here.md`、`docs/skill-usage.md` 增加显式起盘步骤。
- 实际落地命令采用 writeback 形式：
  ```
  python3 scripts/fanqie_launch_stack.py --project-root <project_root> --chapter 003 --chapters 001-003 --mode writeback --writeback
  ```
- 这样 `.mighty/launch-stack.json` 会被真正编译写回，而不是继续停留在“存在但空/未用”的状态。

---

### P0-3 · `novel-init` 创建的 `.mighty/launch-stack.json` 为空文件，无 placeholder

**状态：** 已处理并归档（2026-03-25）

**位置：** `skills/novel-init/SKILL.md:108-112`

`novel-init` 创建 `.mighty/launch-stack.json` 但未规定初始内容。`novel-outline/SKILL.md:79` 写着：
> "if `.mighty/launch-stack.json` exists, prefer its current launch-side compiler hints"

一个空文件会让这条判断"文件存在"→ "静默通过" → 无任何有效约束进入 outline 步骤。

**建议：** 在 `novel-init` Step 8 增加：初始化时写入最小 `preselect` 阶段 placeholder：
```json
{
  "version": "1.0",
  "phase": "preselect",
  "premise_line": "",
  "primary_pivot": "",
  "compiler_output": {}
}
```
让 consume 端能区分"尚未编译"和"已编译但字段为空"。

**归档说明：**
- 已在 `skills/novel-init/SKILL.md` Step 8 写明 `preselect` placeholder 合同。
- 已在 `scripts/fanqie_launch_stack.py` 增加 placeholder 检测：正式 writeback 可覆盖 `preselect` 占位文件，不再被 init 阶段的占位 sidecar 反向阻断。

---

## P1 — 接线缺口（技能合同不一致）

### P1-1 · `novel-learn` 缺少对 `writing-core-framework/README.md` 的 required read

**状态：** 已处理并归档（2026-03-25）

**位置：** `skills/novel-learn/SKILL.md` 第 46-65 行

所有其他 consumer skill（write / review / precheck / package / outline）的 Required reads 都包含 `../../docs/writing-core-framework/README.md`。`novel-learn` 只在条件读取中有 `07-memory-压缩信号约定.md`，缺 README 入口。

`writing-core-framework/README.md` 的"技能读取包"章节明确列出了 `novel-learn` 应读 `07-memory-压缩信号约定.md`，但 skill 合同没有将这条关系锁定为 required read。

**归档说明：**
- 已在 `skills/novel-learn/SKILL.md` 的 Always read 中加入 `../../docs/writing-core-framework/README.md`。

---

### P1-2 · `novel-learn` 完全未接入 launch-stack

**状态：** 已处理并归档（2026-03-25）

`novel-learn` 无任何 launch-stack 读取路径。整条主链（outline → write → review → precheck → package）都在 required reads 里挂了 `fanqie-launch-stack/README.md`。

用户跑完 `novel-learn` 后，如果发现起盘判断需要更新（如语法偏移、pivot 调整），没有任何路径触发 `drift_signal` 更新。learn 结果与 launch-stack 处于孤立状态。

**归档说明：**
- 已在 `skills/novel-learn/SKILL.md` 增加：
  - `.mighty/launch-stack.json`
  - `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
  - `drift_signal` 对齐与轻量 state mirror 更新说明
- `novel-learn` 现在能把 early-phase 偏移回流成 `launch_stack_drift_signal`，但不会越权重写完整 sidecar。

---

### P1-3 · `novel-close` 直接读取子技能 SKILL.md 文件

**状态：** 已处理并归档（2026-03-25）

**位置：** `skills/novel-close/SKILL.md` Required reads

`novel-close` 把 `../novel-review/SKILL.md`、`../novel-fix/SKILL.md`、`../novel-polish/SKILL.md`、`../novel-rewrite/SKILL.md` 列为 required reads。

这意味着 `novel-close` 的执行模式依赖完整读取 4 个子技能的全文合同（4 × ~300 行）。当任意子技能 SKILL.md 更新时，`novel-close` 的行为可能意外变化；而且 AI 需要在执行前消耗大量上下文来加载子技能定义。

建议 `novel-close` 改为只读 `docs/default-workflows.md`（已有路由规则）和 `state.json` 中的 routing 字段，子技能执行时再由子技能自行读取自身合同。

**归档说明：**
- 已从 `skills/novel-close/SKILL.md` 的 Required reads 中移除：
  - `../novel-review/SKILL.md`
  - `../novel-fix/SKILL.md`
  - `../novel-polish/SKILL.md`
  - `../novel-rewrite/SKILL.md`
- 保留 `docs/default-workflows.md` 和状态路由说明，子技能边界改为在被选中时自行加载。

---

## P2 — 可读性与维护问题

### P2-1 · `task_plan.md` 多个计划堆叠，番茄起盘协议栈出现两次

**状态：** 已处理并归档（2026-03-25）

`task_plan.md` 包含 3 个 Task Plan 的全文：
1. 反脸谱化体系（Phase 1-13，全部完成）
2. 开篇方法与剧情层次（Phase 1-26，全部完成）
3. 番茄起盘协议栈 **出现两次**：
   - 第一次：Phase 1-2 完成，Phase 3-8 pending
   - 第二次：Phase 1-8 全部完成

读者无法快速判断当前状态。建议把已完成的历史计划归档到 `task_plan_archive.md`，`task_plan.md` 只保留当前活跃计划。

**归档说明：**
- 已将历史内容保留到 `task_plan_archive.md`。
- `task_plan.md` 现只保留当前活跃任务计划。

---

### P2-2 · `docs/` 目录 131 个文件，缺少分类入口

**状态：** 已处理并归档（2026-03-25）

`docs/` 目前混放：
- 阶段历史（`phase-*-summary.md`）
- 框架文档（`anti-flattening-framework/`、`opening-and-plot-framework/` 等）
- 平台研究（`fanqie-evil-*.md`、`fanqie-writer-zone-lessons.md`）
- 系统配置（`strong-quality-gate-policy.json`、`setting-gate-policy.json`）
- v1 治理文档（`v1-*.md`）

没有 `docs/INDEX.md` 或分类导航。新用户需要依赖 `README.md` 里的线性列表（已达 40+ 条目）才能找到所需文档。

**归档说明：**
- 已新增 `docs/INDEX.md`，按“上手入口 / 框架与规则层 / 治理与策略 / 阶段历史 / 研究与实验”分类。

---

### P2-3 · 番茄生产实验文档与框架文档混放

**状态：** 已处理并归档（2026-03-25）

`docs/` 根目录下的 `fanqie-evil-gongdou-production-template.md`、`fanqie-evil-variant-comparison.md`、`fanqie-writer-zone-lessons.md` 等是生产实验记录或作者经验笔记，与 `default-workflows.md`、`start-here.md` 等权威框架文档混放，容易让读者误以为这些实验记录是规范性文档。

**归档说明：**
- 上述实验/经验文档已移入 `docs/research/fanqie/`。
- 已补 `docs/research/fanqie/README.md` 作为研究区入口，并更新主要引用路径。

---

### P2-4 · `smoke/` 目录无清理策略

**状态：** 已处理并归档（2026-03-25）

当前 `smoke/` 目录下有多个 e2e 隔离副本（`e2e-gongdou-evil-antiflattening-20260322`、`e2e-dual-substitute-evil-*` 等）。随着每次新框架验证都产生新副本，该目录将无限增长。建议明确 smoke 副本的保留策略（如只保留最近 N 个，或按框架保留最终版本）。

**归档说明：**
- 已新增 `smoke/README.md`。
- 文档中明确了 `基线样本 / 派生副本 / 清理` 三类规则，用来约束后续副本增长。

---

## 汇总优先级

| 优先级 | 编号 | 问题 | 当前状态 |
|--------|------|------|---------|
| P0 | P0-1 | `novel-write` 步骤 10 重复 | 已处理并归档 |
| P0 | P0-2 | launch-stack CLI 无触发时机 | 已处理并归档 |
| P0 | P0-3 | `launch-stack.json` 空文件无 placeholder | 已处理并归档 |
| P1 | P1-1 | `novel-learn` 缺 writing-core README | 已处理并归档 |
| P1 | P1-2 | `novel-learn` 未接 launch-stack | 已处理并归档 |
| P1 | P1-3 | `novel-close` 读子技能 SKILL.md | 已处理并归档 |
| P2 | P2-1 | `task_plan.md` 堆叠 + 重复 | 已处理并归档 |
| P2 | P2-2 | `docs/` 无分类入口 | 已处理并归档 |
| P2 | P2-3 | 实验文档与框架文档混放 | 已处理并归档 |
| P2 | P2-4 | `smoke/` 无清理策略 | 已处理并归档 |

---

*由 2026-03-24 全量审查生成，2026-03-25 完成修复并归档。验证：204 passed，0 failed。*
