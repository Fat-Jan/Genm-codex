# Genm-codex 第三阶段范围设计

## 设计结论

第三阶段采用 `A + B` 组合，但拆成两个子阶段推进：

- **Phase 3A：创作增强层**
- **Phase 3B：查询与状态增强层**

这样做的目标不是放慢迁移，而是避免把“直接创作能力”和“中台增强能力”混成一个难验收的大阶段。

## 为什么不是只选 A 或只选 B

### 只做 A 的问题

- 用户面感知强，但项目检索、统计、状态深化仍然偏薄
- 到后期仍要回来补查询与索引层

### 只做 B 的问题

- 技术层更完整，但用户在日常创作里的直接收益不够集中
- 容易继续向“中台工程”膨胀

### 采用 A + B 的原因

- 当前仓库已经具备核心创作闭环和第二阶段中台基础
- 继续迁移最有用的能力，比单独偏一侧更符合现阶段目标
- 但必须拆子阶段，否则范围和验收会再次变糊

## 候选命令评估

| 命令 | 迁移价值 | 依赖复杂度 | 验证成本 | 第三阶段定位 |
|------|----------|------------|----------|--------------|
| `novel-polish` | 高 | 中 | 中 | Phase 3A P0 |
| `novel-genre` | 高 | 中 | 低 | Phase 3A P0 |
| `novel-analyze` | 高 | 中 | 中 | Phase 3A P1 |
| `novel-resume` | 中 | 高 | 高 | Phase 3A P2 |
| `novel-index` | 高 | 中 | 中 | Phase 3B P0 |
| `novel-query` 扩展模式 | 高 | 中 | 中 | Phase 3B P1 |
| `novel-status` 高级统计 | 高 | 中 | 中 | Phase 3B P1 |
| `novel-log` | 中 | 中 | 低 | Phase 3B P2 |

## Phase 3A：创作增强层

### 目标

把当前“能写、能审、能改、能导”的主闭环，扩成更接近日常使用的创作工作台。

### 范围

#### P0

- `novel-polish`
- `novel-genre`

#### P1

- `novel-analyze`

#### P2

- `novel-resume`

### 迁移顺序

1. `novel-polish`
2. `novel-genre`
3. `novel-analyze`
4. `novel-resume`

### 这样排的原因

- `polish` 直接补强 `write → review → rewrite` 之后的精修能力
- `genre` 能把 profile 应用和题材切换显式化，提升初始化后的长期可维护性
- `analyze` 依赖前面已有章节、state 和 profile，放在前两项之后更自然
- `resume` 最有用，但最依赖工作流中断点和恢复约定，应放在 3A 尾部

### 3A 迁移约束

- `novel-polish` 第一版不追求旧命令里的“交互式对比 UI”，先做可靠的最小润色闭环
- `novel-genre` 第一版优先支持：
  - 列出可用题材
  - 读取当前题材
  - 应用指定题材 profile
- `novel-analyze` 第一版优先做基于现有章节和 state 的文本/节奏分析，不引入复杂图表依赖
- `novel-resume` 只有在恢复契约足够清晰时才纳入实际实现；若工作流状态结构仍不稳定，不阻塞 3A 其他项

### 3A 验收标准

- 每个 skill 都能在独立 Codex 会话中被发现
- 每个 skill 至少有 1 条 smoke 用例通过
- `novel-polish` 至少能对单章完成最小可用润色
- `novel-genre` 至少能完成一次真实 profile 应用
- `novel-analyze` 至少能输出一份可读的区间分析结果
- `novel-resume` 如进入实现，必须基于明确的中断状态恢复，不允许伪恢复

## Phase 3B：查询与状态增强层

### 目标

在第二阶段“查 / 看 / 管”的基础上，把项目检索、状态聚合和索引能力做成更强的工作台层。

### 范围

#### P0

- `novel-index`

#### P1

- `novel-query` 扩展模式
- `novel-status` 高级统计

#### P2

- `novel-log`

### 迁移顺序

1. `novel-index`
2. `novel-query` 扩展模式
3. `novel-status` 高级统计
4. `novel-log`

### 这样排的原因

- `index` 是 `query/status` 深化的最佳底座
- 扩展版 `query` 和高级 `status` 都适合在索引存在后再增强
- `log` 有用，但对用户主工作流的直接增益弱于前三项

### 3B 迁移约束

- `novel-index` 第一版先支持：
  - build
  - update
  - query
  - stats
- `novel-query` 扩展模式只补强已存在的自然语言和模板能力，不急于完整复制旧 Dataview 语法
- `novel-status` 高级统计先做：
  - timeline / foreshadowing 视图
  - stats 聚合
  - 关键预警摘要
- `novel-log` 只有在 `.mighty/logs/trace.jsonl` 约定明确后再落地，不主动引入重型日志系统

### 3B 验收标准

- `novel-index` 能真实构建并查询一次项目索引
- 扩展版 `novel-query` 能在索引存在时给出更强的结构化回答
- 高级版 `novel-status` 能输出比第二阶段更丰富的统计视图
- `novel-log` 如进入实现，必须能在无日志和有日志两种情况下都稳定返回

## 版本边界建议

- **`v0.3.0`**：以 `Phase 3A` 为主要封版目标
- **`v0.4.0`**：以 `Phase 3B` 为主要封版目标

如果 `novel-resume` 因恢复契约不稳定而延期，不阻塞 `v0.3.0`，可顺延到后续小版本。

## 本阶段明确不做

- 不迁移已定性为历史/参考文档的旧命令
- 不在第三阶段同时推进 shared 资产 selective-sync 改造
- 不在第三阶段一并重做版本体系或仓库结构
- 不把 Phase 3 做成“大一统增强包”

## 下一步建议

第三阶段正式实施时，先从 **Phase 3A / P0** 开始：

1. `novel-polish`
2. `novel-genre`

原因：

- 用户收益最直接
- 对现有主闭环补强最大
- 风险低于 `resume`
- 验证也比 3B 更便于快速收证
