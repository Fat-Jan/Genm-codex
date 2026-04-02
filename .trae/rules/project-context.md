# Genm-codex 项目上下文

## 项目定位

Genm-codex 是网文创作技能工作区，核心是 `skills/` 下的 `novel-*` skill 链。

## 进入项目后第一步

1. 检查项目目录下是否有 `.mighty/state.json`
   - **存在**：先调用 `novel-status`，了解当前写作进度
   - **不存在**：从 `novel-init` 开始
2. 不确定读哪份文档时，先看 `docs/INDEX.md`
3. 当前正在进行的任务，看 `.ops/active-plan.md`

## Skill 调用约定

- 优先用 `novel-*` 前缀调用：`novel-init`、`novel-outline`、`novel-write`、`novel-status` 等
- `genm-novel-*` 是兼容别名，不要当唯一调用假设
- skill 安装路径：`~/.claude/skills/`（Claude Code）或 `~/.openclaw/skills/`（OpenCLAW）等

## 标准创作主线顺序

```
novel-init → novel-genre → novel-outline → novel-package → novel-write → novel-review → novel-close
```

## 关键文件位置

| 文件 | 用途 |
|------|------|
| `project-map.yaml` | 项目全局地图，最高层入口 |
| `docs/INDEX.md` | 文档索引 |
| `docs/00-当前有效/start-here.md` | 快速入口 |
| `docs/00-当前有效/default-workflows.md` | 默认工作流 |
| `v1.6-roadmap.md` | 当前主线路线图 |
| `v1.5-roadmap.md` | 直接上游参考 roadmap |
| `shared/profiles/` | 题材配置，**不要直接手改** |
| `shared/` | 上游同步资产，**不要直接手改** |

## 高风险操作（需要先确认）

- 执行 `scripts/sync-shared-from-genm.sh`（会覆盖 shared/ 资产）
- 修改 `skills/*/SKILL.md` 的 frontmatter name 字段
- 任何破坏性删除或重命名

## 任务强度参考（配合 rule.md）

- 普通创作调用 skill → L1/L2
- 治理/contract 决策 → L3
- 路线图方向裁决、是否升级专项 → L4
