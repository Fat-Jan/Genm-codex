# Genm-codex 第二阶段 Smoke Plan

## 目的

验证第二阶段已迁入的 Skill 是否能在现有 `e2e-novel` 样本项目上完成最小可用操作。

当前待 smoke 的能力：

- `genm-novel-query`
- `genm-novel-status`
- `genm-novel-character`
- `genm-novel-setting`
- `genm-novel-foreshadowing`
- `genm-novel-batch`

---

## 推荐顺序

建议先跑只读能力，再跑会改状态的能力：

1. `genm-novel-query`
2. `genm-novel-status`
3. `genm-novel-character`
4. `genm-novel-setting`
5. `genm-novel-foreshadowing`
6. `genm-novel-batch`

---

## Smoke 场景

### 1. Query

#### 提示词

```text
请使用 genm-novel-query skill，回答：
主角现在什么境界？有哪些活跃伏笔？请给我一个简洁结果。
```

#### 成功判据

- 能正确读取 `.mighty/state.json`
- 返回主角当前境界
- 返回活跃伏笔列表
- 不需要改动任何文件

---

### 2. Status

#### 提示词

```text
请使用 genm-novel-status skill，总结当前项目状态，给我一个简明 dashboard，并指出下一步建议。
```

#### 成功判据

- 能读取 `.mighty/state.json`
- 能汇总当前章节、总字数、质量状态、活跃伏笔
- 能给出下一步建议
- 不需要改动任何文件

---

### 3. Character

#### 提示词

```text
请使用 genm-novel-character skill，在当前项目中创建一个新角色：
姓名=林晚照
定位=外门药庐女弟子
与主角关系=潜在盟友
```

#### 成功判据

- 在 `设定集/角色/` 下生成新角色文件
- 内容包含最小角色卡信息
- 不破坏现有主角卡

---

### 4. Setting

#### 提示词

```text
请使用 genm-novel-setting skill，为当前项目新增一个地点设定：
名称=后山东壁石门
类型=location
action=create
```

#### 成功判据

- 在 `设定集/地点/` 下生成目标设定文件
- 至少包含地点用途和故事相关性
- 不破坏现有力量体系文件

---

### 5. Foreshadowing

#### 提示词

```text
请使用 genm-novel-foreshadowing skill，列出当前项目的活跃伏笔，并指出最该优先回收的一项。
```

#### 成功判据

- 能正确读取 `plot_threads.foreshadowing`
- 能给出按状态分组或按优先级排序的结果
- 不需要改动文件

---

### 6. Batch

#### 提示词

```text
请使用 genm-novel-batch skill，评估当前项目是否适合从第002章开始顺序批量写 2 章；如果前置条件不足，请明确指出阻塞项，不要强行写作。
```

#### 成功判据

- 能检查 `.mighty/state.json`
- 能检查 `大纲/章纲/第002章.md` 等前置条件
- 若前置不足，能明确阻塞项
- 若前置足够，能给出批量写作建议

---

## 记录建议

每跑一个 skill，记录：

- 提示词
- 实际输出摘要
- 是否改文件
- 是否通过
- 失败原因

推荐追加到：

- `docs/90-归档/迁移与RC/codex-migration-plan.md`
- 或单独新建 `docs/90-归档/阶段/phase-2-smoke-results.md`
