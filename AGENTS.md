# Genm-codex 项目准则

用途：只定义“在 Genm-codex 里如何更快地做对事”。通用思考方式、模式切换、验证门禁，继承上层全局 `AGENTS.md`。

## 1. 项目定位

- 这是一个 Codex 原生网文创作技能工作区，不是通用应用仓库。
- 当前主战场不是“继续堆技能数量”，而是“包装生成层 + 质量闭环整合”。
- 核心可维护对象有四类：
  - `skills/`：真正的 Skill 定义与流程逻辑
  - `shared/`：从源仓库 `Genm` 同步来的共享资产
  - `docs/`：迁移、阶段、烟测和使用说明
  - `.ops/`：当前任务的 active plan / progress / findings / decisions 默认落点

## 2. 加速原则

- 在这个项目里，加速的定义是：尽快拿到对 Skill 行为、共享资产状态、迁移完整性的可靠反馈。
- 第一优先不是“多改”，而是“先确认你改的是不是正确层”：
  - 改 Skill 行为：看 `skills/`
  - 改共享素材：先看 `shared/` 是否应由 `Genm` 同步
  - 改迁移范围或阶段判断：看 `docs/`
- 默认先跑最便宜的验证，再跑高成本验证：
  - 结构校验
  - 只读报告
  - 定向 smoke
  - 全量人工检查

## 3. 快速入口

第一次进入仓库，按这个顺序理解：

1. [README.md](/Users/arm/Desktop/vscode/Genm-codex/README.md)
2. [project-map.yaml](/Users/arm/Desktop/vscode/Genm-codex/project-map.yaml)
3. [docs/00-当前有效/start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/start-here.md)
4. [docs/00-当前有效/skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/skill-usage.md)
5. [docs/00-当前有效/shared-asset-dependency-map.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/shared-asset-dependency-map.md)
6. 当前目标相关的阶段文档：
   - 包装与质量闭环优先看 [docs/90-归档/阶段/phase-9-summary.md](/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/phase-9-summary.md)
   - 共享资产治理优先看 [docs/90-归档/阶段/phase-7b-selective-sync-governance.md](/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/phase-7b-selective-sync-governance.md)

如果要延续当前任务状态，优先看：

- [.ops/active-plan.md](/Users/arm/Desktop/vscode/Genm-codex/.ops/active-plan.md)
- [.ops/progress.md](/Users/arm/Desktop/vscode/Genm-codex/.ops/progress.md)
- [.ops/findings.md](/Users/arm/Desktop/vscode/Genm-codex/.ops/findings.md)

根目录 `task_plan.md` / `progress.md` / `findings.md` 先作为 legacy 连续性入口保留，不再是新任务默认落点。

如果要看真实样本，不要先翻所有 skill，先看：

- [e2e-novel](/Users/arm/Desktop/vscode/Genm-codex/e2e-novel)
- [e2e-novel/.mighty/state.json](/Users/arm/Desktop/vscode/Genm-codex/e2e-novel/.mighty/state.json)

结构边界：

- `e2e-novel/`：官方最小 E2E 样本
- `smoke/`：专项 smoke 验证资产
- `shared/`：synced boundary，默认不要直接长期手改
- `projects/`：workspace，可变项目数据，不是产品源码真值

## 4. 高频命令

```bash
# 最快结构校验
bash scripts/validate-migration.sh

# 查看共享资产状态，不改文件
bash scripts/sync-shared-from-genm.sh --report

# 查看按域同步状态
bash scripts/sync-shared-from-genm.sh --report --domain profiles
bash scripts/sync-shared-from-genm.sh --report --domain references
bash scripts/sync-shared-from-genm.sh --report --domain templates

# 安装或刷新本地 skill 链接
bash scripts/install-skills.sh

# 真正同步共享资产
bash scripts/sync-shared-from-genm.sh
```

命令优先级：

1. 先 `validate-migration.sh`
2. 涉及 shared 时先 `sync-shared-from-genm.sh --report`
3. 涉及本地 skill 安装或调用名时再跑 `install-skills.sh`
4. 只有明确需要更新共享资产时，才执行真正的 sync

## 5. 模式路由

- 新增或修改某个 skill：
  先读目标 `skills/<skill>/SKILL.md`，再读该 skill 相关阶段文档和 smoke 结果。
- 调整 skill 调用名、安装方式或本地发现问题：
  先看 [scripts/install-skills.sh](/Users/arm/Desktop/vscode/Genm-codex/scripts/install-skills.sh) 和 [docs/00-当前有效/skill-usage.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/skill-usage.md)。
- 调整 `shared/` 下任何内容：
  先进入调研模式，确认它是否应该从 `Genm` 同步；默认不要直接手改 `shared/`。
- 延续或接手一个已有任务：
  先看 `.ops/`，只有在追历史链路或旧链接时才回读根目录 legacy ops 文件。
- 调整 profiles / references / templates 的依赖关系：
  先看 [docs/00-当前有效/shared-asset-dependency-map.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/shared-asset-dependency-map.md)。
- 处理包装层或质量闭环相关任务：
  先看 [docs/90-归档/阶段/phase-9-summary.md](/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/phase-9-summary.md)。
- 不知道从哪个 skill 开始：
  先看 [docs/00-当前有效/start-here.md](/Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/start-here.md)，不要凭记忆猜。

## 6. 复用优先级

- 第一优先复用现有 `skills/*/SKILL.md` 的模式和措辞，不新造平行 skill。
- 第二优先复用 `shared/` 里的 profile / reference / template，不把同样规则重写进 skill 文档。
- 第三优先复用 `docs/` 里的阶段结论、烟测结果、迁移边界，不重复发明项目历史。
- 第四优先复用 `e2e-novel` 作为最短反馈样本，不要每次从零造测试项目。
- 第五优先复用 `project-map.yaml` 与 `.ops/` 的结构边界，不要再把新的 active 状态文件散落到根目录。

## 7. 高风险区域

- `shared/` 是同步资产，不是首选手改区域。
- `.ops/` 承担 active ops，不要把它误当 durable docs；稳定规则应回写到 `docs/00-当前有效/`。
- `scripts/sync-shared-from-genm.sh` 会直接覆盖目标目录；执行真实同步前，先确认需求和来源。
- `skills/<name>/SKILL.md` 中的 frontmatter `name` 会影响实际触发方式，不要只改目录名或安装别名。
- `docs/` 不是纯装饰；阶段判断、边界和 smoke 结论如果失真，会误导后续所有实现。
- `novel-scan` 目前不属于默认工作流，涉及它时先确认任务是不是已经超出当前默认范围。

## 8. 最短反馈回路

- 改安装脚本或技能链接：
  先跑 `bash scripts/install-skills.sh`
- 改共享资产同步逻辑：
  先跑 `bash scripts/sync-shared-from-genm.sh --report`
- 改共享资产域划分或依赖判断：
  先读依赖图，再做按域 report
- 改 skill 文案或结构约束：
  先检查目标 `SKILL.md`，再用 `e2e-novel` 做最小人工 smoke
- 改迁移完整性：
  先跑 `bash scripts/validate-migration.sh`

原则：

- 先选择最快发现方向错了的验证方式
- 再补充最终确认的说明、烟测记录或文档同步

## 9. 这个项目里不要做的事

- 不要把 `shared/` 当作普通源码目录直接长期维护
- 不要继续把新的 `task_plan.md` / `progress.md` / `findings.md` 直接落在仓库根目录
- 不要把 `projects/` 当成产品源码真值，也不要把 `smoke/` 当成官方最小 E2E 样本的替代
- 不要只改 `~/.codex/skills` 里的链接结果，而不改仓库里的 `skills/`
- 不要只更新 README，不同步更新真正承载约束的阶段文档或使用文档
- 不要在不知道默认工作流边界的情况下，把实验能力写成默认推荐路径

## 10. 完成定义

- 能运行：
  对应脚本可执行，或对应 skill 文档与目录结构保持可发现、可使用状态
- 能验证：
  至少有脚本验证、只读报告、`e2e-novel` 样本检查、或文档化 smoke 证据之一
- 能接手：
  README / `project-map.yaml` / `.ops/` / start-here / skill-usage / 阶段文档中至少有一个位置承载新的事实
- 能复用：
  没有把 shared 规则复制进多个 skill，没有制造新的平行安装或平行调用体系

## 11. 第一条工作回复模板

- 建议模式：调研 / 规划 / 执行 / 调试 / 评审
- 第一动作：先读哪个文件或先跑哪条命令
- 第一份反馈：预计通过什么命令、报告或样本拿到
- 主要风险：shared 覆盖、skill 调用名漂移、阶段边界误判
- 如果被阻塞：退回依赖图、阶段文档或 `e2e-novel` 样本
