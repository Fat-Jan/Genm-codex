# Genm-codex

Codex 原生网文创作技能工作区。

这个仓库的当前主线不是“继续堆更多 skill”，而是把已有 `skills + docs + scripts + sidecars` 工作流做稳、做可恢复、做可治理。

当前主线版本：`v1.4`

历史基线与备份：

- `v1.0.0`：首个 `v1` 正式发布基线
- `backup/main-pre-v1.3-20260327`：主线切换到 `v1.3` 前的 `main` 备份分支
- `v1.3-roadmap.md`：上一阶段主线

当前默认范围里仍然包含：

- `opening-and-plot-framework`
- `writing-core-framework`
- `番茄起盘协议栈`
- `Gate Triage`

## 先看哪里

如果你是第一次回到这个仓库，优先看：

- `docs/INDEX.md`
- `docs/00-当前有效/start-here.md`
- `docs/00-当前有效/default-workflows.md`
- `docs/00-当前有效/skill-usage.md`

README 现在只保留最短启动说明和关键治理边界。

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

## 调用名说明

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

## 默认工作流入口

- 默认创作主线：`docs/00-当前有效/default-workflows.md`
- 首次上手入口：`docs/00-当前有效/start-here.md`
- Skill 触发与调用说明：`docs/00-当前有效/skill-usage.md`
- 当前边界：`docs/00-当前有效/v1-boundary.md`
- 当前 profile / bucket 校准口径：`docs/00-当前有效/profile-calibration-and-bucket-mapping.md`
- 当前主线 roadmap：`v1.4-roadmap.md`
- 上一阶段 roadmap：`v1.3-roadmap.md`
- 已归档阶段 roadmap：`v1.1-roadmap.md`

### v1.4 新增文档

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
- Bucket Overlay 缺口清单：`docs/00-当前有效/bucket-overlay-inventory.md`
- 样本库索引：`docs/00-当前有效/sample-library-index.md`

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
- `shared/` 不再被视为"可无脑整包覆盖"的纯镜像目录
- `active-context` 现在只应作为当前 prompt 装配侧栏，不应复制长期 guidance 全文
- `workflow_state` 已开始由维护链真实写回，但当前默认骨架仍然是 `docs + skills + scripts + sidecars`，不引入 monolithic runtime / plugin system
