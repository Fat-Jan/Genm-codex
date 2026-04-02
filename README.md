# Genm-codex

Codex 原生网文创作技能工作区。

这个仓库的当前主线不是“继续堆更多 skill”，而是把已有 `skills + docs + scripts + sidecars` 工作流做稳、做可恢复、做可治理。

当前主线版本：`v1.6`

## 当前定位

- `v1.5` 已完成，并作为当前稳定基线保留
- `v1.6` 当前重点：
  - host capability matrix 真值层
  - install / projection / doctor 对宿主真值的消费
  - host support status、verification level 与 degrade policy 收口
  - 主线 roadmap / `.ops` / README / 文档索引的一致化
- `v1.6` 当前明确不做：
  - 新 plugin / runtime / daemon 实装
  - 未经证据支撑的完整宿主支持承诺
  - 将 Trae 提前写成已支持的 skill install host

历史基线与备份：

- `v1.0.0`：首个 `v1` 正式发布基线
- `v1.5-roadmap.md`：上一轮主线 roadmap，作为 `v1.6` 直接上游参考保留
- `v1.4-roadmap.md`：上一轮稳定主线 roadmap，作为高可见上游参考保留
- `backup/main-pre-v1.3-20260327`：主线切换到 `v1.3` 前的 `main` 备份分支
- `v1.3-roadmap.md`：上一阶段主线

## 默认覆盖范围

- `opening-and-plot-framework`
- `writing-core-framework`
- `番茄起盘协议栈`
- `Gate Triage`

## 最短入口

如果你是第一次回到这个仓库，优先看：

- `project-map.yaml`
- `docs/INDEX.md`
- `docs/00-当前有效/start-here.md`
- `docs/00-当前有效/default-workflows.md`
- `docs/00-当前有效/skill-usage.md`
- `.ops/README.md`

如果遇到 `profile / genre` 边界争议，先回看：

- `docs/10-进行中/batch-evidence-sidecar.json`
- `docs/00-当前有效/genre-ontology-field-decisions-v1.5.md`

不要只凭项目局部文本硬猜。

## 快速开始

### 1. 安装 Skill 链接

```bash
bash scripts/install-skills.sh
```

### 2. 查看 shared 同步差异

先跑文本报告：

```bash
bash scripts/sync-shared-from-genm.sh --report
```

需要机器可读差异时，再看：

```bash
bash scripts/sync-shared-from-genm.sh --report-json
```

当前 `--report-json` 会输出：

- `protected_local_paths`
- `local_only_paths`
- `unexpected_local_only_paths`
- `drift_paths`
- `source_only_paths`

### 3. 真正同步 shared

默认策略：

- 会恢复 `shared/sync-governance.json` 中声明的 repo-local protected files
- 会阻断同路径内容漂移覆盖（`same-path drift overwrite`）

只有在你确认确实要覆盖漂移文件时，才显式传：

```bash
bash scripts/sync-shared-from-genm.sh --allow-drift-overwrite --domain references
```

### 4. 校验迁移状态

```bash
bash scripts/validate-migration.sh
```

## 调用名

- 本地安装链接会同时保留：
  - `novel-*`
  - `genm-novel-*`
- 实际在 Codex 会话里，优先使用各个 `SKILL.md` frontmatter 中的 `name`
- 因此通常优先写：
  - `novel-init`
  - `novel-close`
  - `novel-query`
  - `novel-status`
  - `novel-polish`
  - `novel-genre`
  - `novel-scan`（实验态，非默认主线）

## 关键导航

- 默认创作主线：`docs/00-当前有效/default-workflows.md`
- 首次上手入口：`docs/00-当前有效/start-here.md`
- Skill 触发与调用说明：`docs/00-当前有效/skill-usage.md`
- 项目结构边界：`project-map.yaml`
- Active ops 入口：`.ops/README.md`
- Active ops 接手顺序：先看 `.ops/active-plan.md` → `.ops/progress.md` → `.ops/findings.md`
- 根目录保留原则：`docs/00-当前有效/root-retention-policy.md`
- 文档状态头约定：`docs/00-当前有效/document-status-convention.md`
- Active / legacy 状态导航：`.ops/` 优先；根目录 `progress.md` / `findings.md` / `task_plan.md` 仅保留为 legacy 连续性入口
- 当前边界：`docs/00-当前有效/v1-boundary.md`
- `v1.5` 运行时边界：`docs/00-当前有效/runtime-boundary-adr.md`
- 当前宿主支持状态：`docs/00-当前有效/host-support-status-v1.6.md`
- 当前 profile / bucket 校准口径：`docs/00-当前有效/profile-calibration-and-bucket-mapping.md`
- 样本库入口：`docs/00-当前有效/sample-library-index.md`
- `v1.6` contract / governance 入口：`docs/INDEX.md`
- `v1.6` 分工 roadmap：`v1.6-roadmap.md`

### 当前高频文档

- 三大框架 QUICK 速查卡：
  - `docs/anti-flattening-framework/QUICK.md`
  - `docs/opening-and-plot-framework/QUICK.md`
  - `docs/writing-core-framework/QUICK.md`
- 运行时执行卡压缩稿：
  - `docs/anti-flattening-framework/rule-cache.json`
  - `docs/opening-and-plot-framework/rule-cache.json`
  - `docs/writing-core-framework/rule-cache.json`
- 章纲结构字段设计：`docs/00-当前有效/chapter-structure-fields-design.md`
- Bucket / Profile 映射规范：`docs/00-当前有效/bucket-profile-slug-mapping.md`

## Gate Triage

当项目被 `setting gate` 卡住时，优先按这条最小链路处理：

- `novel-scan -> setting gate -> review-sync-queue`
- 然后用 `novel-status` / `novel-resume` / `novel-query` 看：
  - `gate status`
  - `blocking_gaps`
  - `review_items`
  - `minimal_next_action`

进一步说明见：

- `docs/00-当前有效/gate-triage.md`
- `docs/gate-triage-rollout-2026-03-24.md`

## 已落地能力

主仓 `main` 已经落地：

- `quality-audit`：质量审计，产出 `quality_audit.json`
- `knowledge-projection`：知识投影，产出 `knowledge_projection.json`
- `workflow-truth`：工作流真相
- `workflow-health`：工作流健康度，包含 bundle 和 renderer
- 最小只读 MCP server：`project_knowledge_mcp_server.py`
- `novel-status` / `novel-query` sidecar 消费合同

维护链入口：

```bash
# 完整维护链
python3 scripts/project-maintenance.py <project_root>

# 任务后维护
python3 scripts/post-task-maintenance.py <project_root> --trigger write
```

## 边界提醒

- `Genm` 仍是 shared 源仓库
- `Genm-codex` 负责 Codex 原生 skill/workflow 承载层
- `project-map.yaml` 是结构边界的单一入口
- `.ops/` 是当前任务运行态默认落点
- `shared/` 不再被视为"可无脑整包覆盖"的纯镜像目录
- `e2e-novel/` 是官方最小 E2E 样本；`smoke/` 是专项验证资产；`projects/` 是 workspace
- `active-context` 现在只应作为当前 prompt 装配侧栏，不应复制长期 guidance 全文
- `workflow_state` 已开始由维护链真实写回，但当前默认骨架仍然是 `docs + skills + scripts + sidecars`，不引入 monolithic runtime / plugin system

README 只保留最短启动说明和关键边界；更细的 contract、治理和历史入口统一从 `docs/INDEX.md` 进入。

根目录是否应该继续保留某份文档，优先按 `docs/00-当前有效/root-retention-policy.md` 判断。
新的 active 计划、进度、结论默认写入 `.ops/`，根目录 legacy ops 文件只为旧链接和历史连续性保留。
