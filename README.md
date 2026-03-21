# Genm-codex

Codex 原生网文创作技能工作区。

本目录最初从 `Genm` 仓库拆出，用于承载 Codex 原生网文工作流。当前默认工作流、边界与样本闭环已通过 RC 检查，并已进入正式 `v1.0.0` 阶段。

## 当前范围

第一阶段已完成的核心 Skill：

- `genm-novel-init`
- `genm-novel-outline`
- `genm-novel-write`
- `genm-novel-review`
- `genm-novel-rewrite`
- `genm-novel-export`

第二阶段已完成的扩展 Skill：

- `genm-novel-query`
- `genm-novel-status`
- `genm-novel-character`
- `genm-novel-setting`
- `genm-novel-foreshadowing`
- `genm-novel-batch`

第三阶段已完成的增强 Skill：

- `genm-novel-polish`
- `genm-novel-genre`
- `genm-novel-analyze`
- `genm-novel-resume`
- `genm-novel-index`
- `genm-novel-log`

第四阶段已完成的控制与辅助 Skill：

- `genm-novel-fix`
- `genm-novel-snapshot`
- `genm-novel-precheck`
- `genm-novel-workflow`
- `genm-novel-retrieve`
- `genm-novel-spinoff`

第五阶段已完成的环境与学习 Skill：

- `genm-novel-config`
- `genm-novel-test`
- `genm-novel-learn`

第九阶段已启动的包装层 Skill：

- `genm-novel-package`

第九阶段已完成的整合方向：

- 包装生成层
- 质量闭环第一轮整合

第十阶段已完成的整合方向：

- 包装与市场信号收敛检查点
- 质量路由稳定化检查点

## 目录说明

```text
Genm-codex/
├── skills/      # Codex 原生 Skills
├── shared/      # 从 Genm 同步来的 profiles / references / templates
├── scripts/     # 安装、同步、校验脚本
└── docs/        # 迁移说明、使用说明、阶段总结
```

## 快速开始

### 1. 安装 Skill 链接

```bash
bash scripts/install-skills.sh
```

### 2. 同步共享资产

```bash
bash scripts/sync-shared-from-genm.sh
```

### 3. 校验迁移状态

```bash
bash scripts/validate-migration.sh
```

## 调用名说明

- `scripts/install-skills.sh` 现在会同时创建两套本地链接：
  - `novel-*`
  - `genm-novel-*`
- 但在 Codex 会话里，通常真正被发现和触发的是各个 `SKILL.md` frontmatter 里的 `name`
- 因此实际提示词里，优先使用：
  - `novel-init`
  - `novel-query`
  - `novel-status`
  - `novel-polish`
  - `novel-genre`
- 不要把 `genm-` 前缀默认当成必须的调用名

### 4. 查看使用说明

阅读：

- `docs/skill-usage.md`
- `docs/start-here.md`

### 5. 查看阶段总结

阅读：

- `docs/phase-1-summary.md`
- `docs/phase-2-summary.md`
- `docs/phase-3-summary.md`
- `docs/phase-4-summary.md`
- `docs/phase-5-summary.md`
- `docs/phase-7-summary.md`

## 参考文档

- `docs/migration-map.md`
- `docs/codex-migration-plan.md`
- `docs/v1-maintenance-mode.md`
- `docs/v1.1-roadmap.md`
- `docs/fanqie-short-story-adaptation.md`
- `docs/fanqie-content-buckets.md`
- `docs/fanqie-bucket-constraints.md`
- `docs/fanqie-paid-signal-matrix.md`
- `docs/fanqie-first-execution-plan.md`
- `docs/phase-2-priorities.md`
- `docs/phase-2-smoke-plan.md`
- `docs/phase-2-smoke-results.md`
- `docs/phase-3-scope.md`
- `docs/phase-4-scope.md`
- `docs/phase-5-scope.md`
- `docs/phase-6-scope.md`
- `docs/phase-7-scope.md`
- `docs/phase-7a-scan-contract.md`
- `docs/phase-7b-selective-sync-governance.md`
- `docs/phase-8-scope.md`
- `docs/phase-9-scope.md`
- `docs/phase-9-writing-value-gap-analysis.md`
- `docs/phase-9a-p0-package-smoke-results.md`
- `docs/phase-9b-quality-loop-design.md`
- `docs/phase-9-summary.md`
- `docs/phase-10-scope.md`
- `docs/phase-10-summary.md`
- `docs/phase-11-scope.md`
- `docs/phase-12-scope.md`
- `docs/phase-13-scope.md`
- `docs/phase-14-scope.md`
- `docs/phase-15-scope.md`
- `docs/phase-16-scope.md`
- `docs/phase-11-summary.md`
- `docs/phase-12-summary.md`
- `docs/phase-14-summary.md`
- `docs/phase-15-summary.md`
- `docs/phase-16-summary.md`
- `docs/v1-boundary.md`
- `docs/default-workflows.md`
- `docs/v1-readiness-checklist.md`
- `docs/v1-readiness-assessment.md`
- `docs/v1-rc-plan.md`
- `docs/v1-rc-exit-criteria.md`
- `docs/v1-rc-execution-log.md`
- `docs/v1-final-decision.md`
- `docs/writing-model-strategy.md`
- `docs/start-here.md`
- `docs/phase-5-scope.md`

## 说明

- `Genm` 仍然是源仓库
- `Genm-codex` 负责 Codex 原生 Skill 层
- `shared/` 资产应通过脚本同步，不建议手工维护两份
