# Genm-codex 第四阶段总结

## 范围

第四阶段聚焦剩余命令中仍有独立价值、且适合 Codex 原生工作流的部分，拆成两个子阶段推进：

### Phase 4A：编辑控制与回溯层

- `novel-fix`
- `novel-snapshot`
- `novel-precheck`
- `novel-workflow`

### Phase 4B：写作辅助与专项创作层

- `novel-retrieve`
- `novel-spinoff`

## 验证结果

### Phase 4A

- `novel-fix`：通过
- `novel-snapshot`：通过
- `novel-precheck`：通过
- `novel-workflow`：通过

其中：

- `novel-fix` 已完成基于 review 结果的定向修复 smoke
- `novel-snapshot` 已完成快照列出与加载 smoke
- `novel-precheck` 已完成番茄平台只读投稿前预检 smoke
- `novel-workflow` 已完成“无活动 workflow / 空闲状态”路径 smoke

### Phase 4B

- `novel-retrieve`：通过
- `novel-spinoff`：通过

其中：

- `novel-retrieve` 已完成写作参考卡 smoke
- `novel-spinoff` 已完成单项目轻量番外写作 smoke

## 本阶段带来的能力变化

到第四阶段结束时，`Genm-codex` 已经补齐：

- 定向修复
- 快照查看与加载
- 投稿前预检
- 轻量 workflow 状态管理
- 写作即时引用层
- 单项目轻量番外写作

这让仓库从“能写 + 能查 + 能增强”继续推进到“能修、能回看、能把关、能做侧写”的层级。

## 关键工程调整

- `install-skills.sh` 与 `validate-migration.sh` 已继续扩展到覆盖第四阶段新增 skill
- 第四阶段所有新增 skill 均保持：
  - `novel-*`
  - `genm-novel-*`
  双别名安装方式

## 当前结论

第四阶段已经完成到一个可验收状态。

这意味着：

- 第一阶段：核心闭环
- 第二阶段：创作中台
- 第三阶段：增强能力
- 第四阶段：编辑控制与写作辅助

这四个阶段构成了 `Genm-codex` 当前的主体迁移成果。

## 还没做的事

- `novel-learn` 和 `novel-scan` 仍然暂缓，尚未迁移
- `novel-config` / `novel-test` / `novel-tutorial` / `novel-help` 仍维持低优先级或文档承担
- 第五阶段范围尚未设计
