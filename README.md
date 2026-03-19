# Genm-codex

Codex 原生网文创作技能工作区。

本目录是从 `Genm` 仓库拆出的第一阶段迁移产物，目标是让 Codex 直接使用核心网文工作流，而不再依赖 Claude 插件清单和旧命令壳。

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

### 4. 查看使用说明

阅读：

- `docs/skill-usage.md`

### 5. 查看阶段总结

阅读：

- `docs/phase-1-summary.md`
- `docs/phase-2-summary.md`

## 参考文档

- `docs/migration-map.md`
- `docs/codex-migration-plan.md`
- `docs/phase-2-priorities.md`
- `docs/phase-2-smoke-plan.md`
- `docs/phase-2-smoke-results.md`

## 说明

- `Genm` 仍然是源仓库
- `Genm-codex` 负责 Codex 原生 Skill 层
- `shared/` 资产应通过脚本同步，不建议手工维护两份
