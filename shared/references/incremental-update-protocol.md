# 增量更新协议

**版本**: 1.0.0
**创建日期**: 2026-03-18
**适用范围**: Genm 项目真相文件系统

---

## 1. 增量更新原理

### 1.1 全量更新 vs 增量更新

| 维度 | 全量更新 (当前) | 增量更新 (目标) |
|------|----------------|----------------|
| **数据传递** | 传递完整文件内容 | 只传递变更内容 |
| **上下文占用** | 高 (4000字/章 × N章) | 低 (50-200字/变更) |
| **更新效率** | 低 (重复写入相同内容) | 高 (精准定位变更点) |
| **冲突风险** | 低 (覆盖式写入) | 中 (需冲突检测) |
| **回滚复杂度** | 高 (需保存完整快照) | 低 (可逐条回滚) |

### 1.2 核心思想

**只传递变更内容，不传递完整文件。**

```
传统方式:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 完整文件内容    │ ──→ │   Agent 处理    │ ──→ │  覆盖写入文件   │
│  (4000 tokens)  │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘

增量方式:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 变更描述 (diff) │ ──→ │   Hive Bee      │ ──→ │  应用到目标文件 │
│  (100 tokens)   │     │   执行更新      │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 1.3 预期收益

| 指标 | 当前值 | 目标值 | 提升 |
|------|--------|--------|------|
| 单章更新上下文 | ~4000 tokens | ~200 tokens | **-95%** |
| 批量更新 (10章) | ~40000 tokens | ~2000 tokens | **-95%** |
| 真相文件更新 | ~2000 tokens | ~300 tokens | **-85%** |

---

## 2. 变更描述格式

### 2.1 标准格式 (YAML)

```yaml
update_batch:
  # 批次元数据
  batch_id: "uuid-v4"
  chapter: 3
  timestamp: "2026-03-18T10:00:00Z"
  source: "queen-bee"

  # 变更列表
  changes:
    # 变更 1: current_state.md
    - file: "current_state.md"
      file_version: 2  # 乐观锁版本号
      operations:
        - type: "replace"
          path: "protagonist.cultivation"
          old: "炼气期四层"
          new: "炼气期五层"
          reason: "本章突破"

        - type: "append"
          path: "events"
          value: "击败周通，获得外门大比资格"
          chapter_ref: 3

        - type: "replace"
          path: "resources.spirit_stones"
          old: 100
          new: 85
          reason: "购买丹药消耗"

    # 变更 2: pending_hooks.md
    - file: "pending_hooks.md"
      file_version: 5
      operations:
        - type: "resolve"
          hook_id: "hook-001"
          status: "resolved"
          chapter: 3

        - type: "add"
          hook:
            id: "hook-005"
            description: "上界秘密线索"
            target_chapter: 8
            priority: "high"
            status: "pending"

    # 变更 3: character_matrix.md
    - file: "character_matrix.md"
      file_version: 3
      operations:
        - type: "update_relation"
          character_a: "主角"
          character_b: "苏婉儿"
          field: "affection"
          old: 45
          new: 52
          reason: "共同遇险，感情升温"
```

### 2.2 字段说明

#### 批次级别 (update_batch)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `batch_id` | string | 是 | 唯一标识符 (UUID) |
| `chapter` | number | 是 | 触发更新的章节号 |
| `timestamp` | string | 是 | ISO 8601 时间戳 |
| `source` | string | 否 | 变更来源 (queen-bee / hive-bee / manual) |
| `changes` | array | 是 | 变更列表 |

#### 文件级别 (change)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | string | 是 | 目标文件名 |
| `file_version` | number | 是 | 乐观锁版本号 |
| `operations` | array | 是 | 操作列表 |

#### 操作级别 (operation)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | 是 | 操作类型 (replace/append/remove/add/resolve) |
| `path` | string | 条件 | 目标字段路径 (dot notation) |
| `old` | any | 条件 | 旧值 (用于验证) |
| `new` | any | 条件 | 新值 |
| `value` | any | 条件 | 追加/添加的值 |
| `reason` | string | 否 | 变更原因说明 |
| `chapter_ref` | number | 否 | 关联章节 |

---

## 3. 支持的操作类型

### 3.1 replace - 替换字段值

**用途**: 修改现有字段的值

```yaml
operations:
  - type: "replace"
    path: "protagonist.cultivation"      # 字段路径
    old: "炼气期四层"                     # 预期旧值 (用于验证)
    new: "炼气期五层"                     # 新值
    reason: "本章突破"                    # 变更原因
```

**约束**:

- `old` 值必须匹配当前值，否则触发版本冲突
- `path` 使用点号表示法 (e.g., `protagonist.stats.hp`)
- 支持嵌套对象访问

### 3.2 append - 追加到列表

**用途**: 向列表末尾添加元素

```yaml
operations:
  - type: "append"
    path: "events"                       # 列表字段路径
    value: "击败周通"                     # 追加的元素
    chapter_ref: 3                        # 关联章节
```

**约束**:

- 目标字段必须是数组类型
- 自动去重 (如果配置 `unique: true`)
- 支持追加对象或简单值

### 3.3 remove - 从列表移除

**用途**: 从列表中移除指定元素

```yaml
operations:
  - type: "remove"
    path: "active_effects"
    value: "中毒效果"                     # 要移除的元素值
    # 或使用索引
    index: 2                              # 要移除的索引
```

**约束**:

- 通过 `value` 匹配移除 (适合简单值)
- 或通过 `index` 指定位置 (适合复杂对象)
- 元素不存在时不报错

### 3.4 add - 新增条目

**用途**: 向映射/字典添加新条目

```yaml
operations:
  - type: "add"
    path: "characters"                   # 父路径
    key: "zhou_tong"                     # 新键名
    value:                               # 新值 (对象)
      name: "周通"
      status: "defeated"
      first_appearance: 3
```

**约束**:

- `key` 在当前层级必须唯一
- 如果 `key` 已存在，触发冲突

### 3.5 resolve - 标记解决

**用途**: 标记钩子/任务/伏笔为已解决

```yaml
operations:
  - type: "resolve"
    hook_id: "hook-001"                  # 钩子ID
    status: "resolved"                   # 新状态
    chapter: 3                           # 解决章节
    resolution_summary: "主角发现玉佩秘密"
```

**约束**:

- 专用于 `pending_hooks.md` 文件
- 必须提供 `hook_id` 定位目标
- 支持状态: `pending` / `resolved` / `abandoned`

### 3.6 update_relation - 更新关系值

**用途**: 更新人物关系矩阵

```yaml
operations:
  - type: "update_relation"
    character_a: "主角"                   # 人物A
    character_b: "苏婉儿"                  # 人物B
    field: "affection"                    # 关系字段
    old: 45                               # 旧值
    new: 52                               # 新值
    reason: "共同遇险"
```

**约束**:

- 专用于 `character_matrix.md` 文件
- `character_a` 和 `character_b` 顺序无关
- 支持字段: `affection` / `trust` / `conflict` / `familiarity`

---

## 4. 增量更新执行流程

### 4.1 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                     Phase 1: 生成变更描述                        │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Queen Bee 完成章节生成                                        │
│ 2. 对比新旧状态，识别变更点                                       │
│ 3. 生成 update_batch YAML                                        │
│ 4. 附加到章节输出                                                │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Phase 2: 应用变更                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Hive Bee 接收 update_batch                                    │
│ 2. 验证批次格式和完整性                                          │
│ 3. 按文件分组操作                                                │
│ 4. 逐个文件执行操作                                              │
│ 5. 验证文件版本号 (乐观锁)                                       │
│ 6. 执行具体操作 (replace/append/...)                            │
│ 7. 递增文件版本号                                                │
│ 8. 写入更新后的文件                                              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Phase 3: 验证结果                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. 读取更新后的文件                                              │
│ 2. 验证所有变更已正确应用                                        │
│ 3. 生成更新报告                                                  │
│ 4. 标记批次状态 (success / partial / failed)                    │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Phase 4: 错误处理                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. 检测到冲突/错误                                               │
│ 2. 停止当前批次剩余操作                                          │
│ 3. 触发回滚机制 (如配置)                                         │
│ 4. 报告错误详情                                                  │
│ 5. 标记批次状态为 failed                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 伪代码实现

```typescript
// Hive Bee 执行更新
async function applyIncrementalUpdate(batch: UpdateBatch): Promise<UpdateResult> {
  const result: UpdateResult = {
    batchId: batch.batch_id,
    status: 'success',
    appliedFiles: [],
    failedOperations: []
  };

  for (const change of batch.changes) {
    try {
      // 1. 读取目标文件
      const file = await readFile(change.file);

      // 2. 验证版本号 (乐观锁)
      if (file.version !== change.file_version) {
        throw new VersionConflictError(
          `Expected version ${change.file_version}, got ${file.version}`
        );
      }

      // 3. 执行所有操作
      for (const op of change.operations) {
        applyOperation(file.content, op);
      }

      // 4. 递增版本号
      file.version++;

      // 5. 写入文件
      await writeFile(change.file, file);

      result.appliedFiles.push(change.file);

    } catch (error) {
      result.failedOperations.push({
        file: change.file,
        error: error.message
      });
      result.status = 'partial';

      // 如果配置为严格模式，停止后续操作
      if (config.strictMode) {
        result.status = 'failed';
        break;
      }
    }
  }

  return result;
}

// 应用单个操作
function applyOperation(content: any, op: Operation): void {
  switch (op.type) {
    case 'replace':
      validateOldValue(content, op.path, op.old);
      setValue(content, op.path, op.new);
      break;

    case 'append':
      const list = getValue(content, op.path);
      if (!Array.isArray(list)) {
        throw new Error(`Path ${op.path} is not an array`);
      }
      list.push(op.value);
      break;

    case 'remove':
      removeFromList(content, op.path, op.value || op.index);
      break;

    case 'add':
      addToMap(content, op.path, op.key, op.value);
      break;

    case 'resolve':
      resolveHook(content, op.hook_id, op.status, op.chapter);
      break;

    case 'update_relation':
      updateRelation(content, op.character_a, op.character_b, op.field, op.new);
      break;

    default:
      throw new Error(`Unknown operation type: ${op.type}`);
  }
}
```

### 4.3 回滚机制

#### 自动回滚 (单次操作失败)

```yaml
# 配置示例
rollback:
  enabled: true
  scope: "file"        # file / batch / none
  strategy: "immediate" # immediate / on_batch_fail / manual
```

- `scope: "file"`: 单个文件操作失败时，回滚该文件的所有操作
- `scope: "batch"`: 任意文件失败时，回滚整个批次
- `strategy`: 回滚时机 (立即 / 批次结束时 / 手动)

#### 手动回滚

```bash
# 通过 CLI 回滚到指定批次
hive-bee rollback --batch-id <uuid> --to-version <n>

# 回滚整个章节的所有变更
hive-bee rollback --chapter 3 --all
```

---

## 5. 与 Queen Bee 集成

### 5.1 生成阶段输出

Queen Bee 在完成章节生成后，需要同时输出:

1. **章节内容** (Markdown)
2. **变更描述** (YAML)

```yaml
# Queen Bee 输出格式
chapter_output:
  content: |
    # 第三章 突破

    林凡盘膝而坐...

  incremental_update:
    batch_id: "550e8400-e29b-41d4-a716-446655440000"
    chapter: 3
    timestamp: "2026-03-18T10:00:00Z"
    changes:
      - file: "current_state.md"
        file_version: 2
        operations:
          - type: "replace"
            path: "protagonist.cultivation"
            old: "炼气期四层"
            new: "炼气期五层"
```

### 5.2 Hive Bee 执行文件更新

Hive Bee 接收 Queen Bee 的输出后:

1. 解析 `incremental_update` 部分
2. 调用 `applyIncrementalUpdate()` 执行更新
3. 返回执行结果

```typescript
// Hive Bee 集成点
async function processChapterOutput(output: ChapterOutput) {
  // 1. 保存章节内容
  await saveChapter(output.content);

  // 2. 执行增量更新
  const updateResult = await applyIncrementalUpdate(output.incremental_update);

  // 3. 处理结果
  if (updateResult.status === 'success') {
    await createSnapshot(output.chapter);
    await updateStateJson(output.chapter);
  } else {
    await handleUpdateFailure(updateResult);
  }

  return updateResult;
}
```

### 5.3 批量更新 vs 单文件更新

#### 单文件更新 (推荐)

每生成一章，立即更新相关真相文件。

```
Chapter 3 → Update truth files → Chapter 4 → Update truth files → ...
```

**优点**:

- 即时生效，后续章节基于最新状态
- 冲突早发现早解决
- 粒度细，回滚影响小

#### 批量更新 (可选)

生成多章后，统一批量更新。

```
Chapters 3-5 → Batch update all truth files
```

**适用场景**:

- 并行生成多章时
- 离线批处理

**批量格式**:

```yaml
update_batch:
  batch_id: "..."
  type: "bulk"           # 标记为批量更新
  chapters: [3, 4, 5]    # 涉及的章节
  changes:
    # 合并多个章节的变更
    - file: "current_state.md"
      operations:
        - type: "replace"  # 来自第3章
          path: "..."
          new: "..."
        - type: "replace"  # 来自第5章
          path: "..."
          new: "..."
```

---

## 6. 冲突处理策略

### 6.1 乐观锁机制

每个真相文件维护一个版本号，更新时验证:

```yaml
# current_state.md
metadata:
  version: 5           # 当前版本号
  last_updated: "..."
  last_chapter: 4

# 变更描述
changes:
  - file: "current_state.md"
    file_version: 5    # 预期版本号
    operations: [...]
```

**验证逻辑**:

- 如果 `file_version == actual_version`: 允许更新，版本号+1
- 如果 `file_version < actual_version`: 触发冲突 (文件已被其他更新修改)
- 如果 `file_version > actual_version`: 异常状态 (不应发生)

### 6.2 版本号控制

```typescript
interface TruthFile {
  metadata: {
    version: number;        // 递增版本号
    last_updated: string;   // ISO 时间戳
    last_chapter: number;   // 最后更新章节
    update_history: Array<{
      batch_id: string;
      chapter: number;
      timestamp: string;
      operations_count: number;
    }>;
  };
  content: any;
}
```

### 6.3 手动合并流程

当自动冲突发生时，进入手动合并流程:

```
┌─────────────────┐
│  检测到版本冲突  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 暂停自动更新    │
│ 保存变更描述    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 提示用户冲突    │
│ 显示差异对比    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 用户选择:       │
│ A. 强制覆盖     │
│ B. 手动合并     │
│ C. 放弃当前变更 │
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│ 强制   │ │ 打开   │ │ 删除   │
│ 更新   │ │ 合并   │ │ 批次   │
│ 版本+1 │ │ 工具   │ │ 记录   │
└────────┘ └────────┘ └────────┘
```

**CLI 命令**:

```bash
# 查看冲突详情
hive-bee conflicts show --batch-id <uuid>

# 强制应用 (覆盖)
hive-bee conflicts resolve --batch-id <uuid> --strategy overwrite

# 手动编辑合并
hive-bee conflicts resolve --batch-id <uuid> --strategy manual

# 放弃批次
hive-bee conflicts resolve --batch-id <uuid> --strategy abort
```

### 6.4 冲突预防策略

| 策略 | 说明 |
|------|------|
| **串行生成** | 小说章节串行生成，避免并行冲突 |
| **细粒度锁** | 按文件锁定，不同文件可同时更新 |
| **预检机制** | 更新前读取最新版本，提前发现冲突 |
| **队列机制** | 变更请求入队，顺序执行 |

---

## 7. 文件示例

### 7.1 完整变更描述示例

```yaml
update_batch:
  batch_id: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  chapter: 3
  timestamp: "2026-03-18T14:30:00Z"
  source: "queen-bee"

  changes:
    # current_state.md 更新
    - file: "current_state.md"
      file_version: 2
      operations:
        - type: "replace"
          path: "protagonist.cultivation"
          old: "炼气期四层"
          new: "炼气期五层"
          reason: "突破"

        - type: "replace"
          path: "protagonist.stats.hp"
          old: 100
          new: 120

        - type: "append"
          path: "completed_events"
          value: "击败周通"
          chapter_ref: 3

        - type: "append"
          path: "completed_events"
          value: "获得外门大比资格"
          chapter_ref: 3

        - type: "replace"
          path: "resources.spirit_stones"
          old: 100
          new: 85
          reason: "购买回气丹"

    # pending_hooks.md 更新
    - file: "pending_hooks.md"
      file_version: 5
      operations:
        - type: "resolve"
          hook_id: "hook-001"
          status: "resolved"
          chapter: 3
          resolution_summary: "在战斗中主角发现玉佩异常发热"

        - type: "add"
          hook:
            id: "hook-005"
            description: "玉佩与上界存在神秘联系"
            target_chapter: 8
            priority: "high"
            status: "pending"
            created_in_chapter: 3

    # character_matrix.md 更新
    - file: "character_matrix.md"
      file_version: 3
      operations:
        - type: "update_relation"
          character_a: "主角"
          character_b: "周通"
          field: "conflict"
          old: 30
          new: 80
          reason: "本章击败周通，结下深仇"

        - type: "update_relation"
          character_a: "主角"
          character_b: "苏婉儿"
          field: "affection"
          old: 45
          new: 52
          reason: "共同遇险，感情升温"

    # chapter_summaries.md 更新
    - file: "chapter_summaries.md"
      file_version: 2
      operations:
        - type: "add"
          path: "chapters"
          key: "chapter-003"
          value:
            title: "突破"
            word_count: 4123
            summary: "林凡在修炼中突破到炼气期五层，随后在外门比试中击败周通，获得外门大比资格。战斗中玉佩异常发热，暗示其不凡来历。"
            key_events:
              - "突破炼气期五层"
              - "击败周通"
              - "获得外门大比资格"
            hooks_introduced:
              - "hook-005"
            hooks_resolved:
              - "hook-001"

    # particle_ledger.md 更新
    - file: "particle_ledger.md"
      file_version: 1
      operations:
        - type: "append"
          path: "transactions"
          value:
            id: "txn-003-001"
            chapter: 3
            type: "expense"
            item: "回气丹"
            quantity: 1
            cost: 15
            balance_after: 85
```

---

## 8. 集成检查清单

### 8.1 Queen Bee 侧

- [ ] 生成章节后自动对比状态变更
- [ ] 生成符合规范的 update_batch YAML
- [ ] 包含正确的 file_version
- [ ] 提供变更原因说明

### 8.2 Hive Bee 侧

- [ ] 实现 applyIncrementalUpdate() 函数
- [ ] 支持所有 6 种操作类型
- [ ] 实现乐观锁验证
- [ ] 实现回滚机制
- [ ] 生成更新报告

### 8.3 真相文件侧

- [ ] 添加 metadata.version 字段
- [ ] 添加 update_history 追踪
- [ ] 初始化所有文件版本号为 1

### 8.4 CLI 工具侧

- [ ] 实现冲突查看命令
- [ ] 实现冲突解决命令
- [ ] 实现手动合并工具
- [ ] 实现批量更新支持

---

## 9. 迁移指南

### 9.1 从全量更新迁移

1. **为所有真相文件添加版本号**

   ```bash
   hive-bee migrate --add-version
   ```

2. **更新 Queen Bee 提示词**
   - 添加增量更新格式说明
   - 提供变更识别指引

3. **测试单个章节**
   - 生成测试章节
   - 验证更新流程
   - 检查版本号递增

4. **全面启用**
   - 更新配置 `incremental_update: true`
   - 监控冲突率

---

## 10. 附录

### 10.1 术语表

| 术语 | 说明 |
|------|------|
| Update Batch | 一次更新操作批次，包含多个文件的变更 |
| Operation | 单个变更操作 (replace/append/...) |
| Optimistic Lock | 乐观锁，通过版本号检测并发冲突 |
| File Version | 文件版本号，每次成功更新后递增 |
| Path | 字段路径，使用点号表示法 |

### 10.2 相关文档

- `build/commands/novel-write.md` - 写作命令
- `build/bees/orchestrator/queen-bee.md` - Queen Bee
- `build/bees/orchestrator/hive-bee.md` - Hive Bee
- `findings.md` (根目录) - 问题分析
- `task_plan.md` (根目录) - Phase 2.5 规划

---

**文档版本历史**:

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-18 | 初始版本 |
