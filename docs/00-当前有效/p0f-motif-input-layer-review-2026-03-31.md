# P0-F 母题输入层持续复检 2026-03-31

> 目的：对 `v1.5` 下一阶段主线中的首个持续复检项进行一次正式检查，确认“世界观母题层”仍然只是上游输入，而没有膨胀成第二真值中心。
>
> 复检范围：`creative-brief`、`novel-init`、`novel-outline`、`novel-package`、`worldview-motif-catalog`、runtime boundary。

---

## 一、复检结论

**思考强度：L4 审慎**

本轮结论：**通过，当前母题输入层边界稳定，无需修正实现。**

当前仓库中的“世界观母题层”仍满足以下约束：

1. `worldview-motif-catalog.md` 明确定位为上游灵感 / 母题输入目录，而非项目真值库
2. `creative-brief.md` 保留了母题选择段，且明确限制立项阶段最多只选 `1 + 0-1 + 0-1` 的母题组合
3. `novel-init / novel-outline / novel-package` 均只把母题目录作为“概念尚不稳定时的输入源”，未把它提升为 canon
4. 代码与状态侧当前未出现 `state.meta.motifs` 的落地使用，不存在第二真值中心膨胀迹象
5. `runtime-boundary-adr.md` 仍明确禁止形成第二真值中心，边界与当前母题输入层设计一致

因此，P0-F 当前适合继续作为**持续复检项**存在，而不是重新进入实施或修正阶段。

---

## 二、检查项与结果

### 2.1 `worldview-motif-catalog.md` 的定位是否仍是上游输入
**思考强度：L3 深度**

结论：**是。**

证据：

- [worldview-motif-catalog.md](file:///Users/arm/Desktop/vscode/Genm-codex/shared/references/writing/worldview-motif-catalog.md) 开头明确写明：
  - 用途是给 `creative-brief`、`novel-init`、`novel-outline`、`novel-package` 提供开书灵感与世界观丰富时的标准化母题输入
  - “母题是上游输入，不是项目真值；只有被项目真正选中的部分，才应进入 `总纲` 或 `设定集/世界观/`”

判断：

- 这份目录的边界定义仍然清晰
- 没有被文档层升级为“项目永久真值”

---

### 2.2 `creative-brief.md` 是否仍保留母题输入段，且没有过度膨胀
**思考强度：L3 深度**

结论：**是。**

证据：

- [creative-brief.md](file:///Users/arm/Desktop/vscode/Genm-codex/shared/templates/project/creative-brief.md) 中明确保留“母题选择”段
- 明确要求：
  - `1` 个世界观母题
  - `0-1` 个机制母题
  - `0-1` 个包装 / 关系母题
- 明确提示：
  - 不要在立项阶段一次叠超过 `3` 个母题
  - 如果这里填不顺，不要急着锁 `总纲`

判断：

- `creative-brief` 仍然是“轻量立项输入层”
- 没有把母题目录扩展成庞大世界观百科导入流程

---

### 2.3 `novel-init / novel-outline / novel-package` 是否仍只把母题目录当作条件性输入
**思考强度：L3 深度**

结论：**是。**

证据：

- [novel-init](file:///Users/arm/Desktop/vscode/Genm-codex/skills/novel-init/SKILL.md)
  - 仅在“项目想法还模糊 / 用户明确要开书灵感或世界观方向 / 脑洞组合”时读取母题目录
  - 明确限制 init 时只优先锁 `1 + 0-1 + 0-1`
  - 明确写明“不把母题目录变成完整世界观百科”

- [novel-outline](file:///Users/arm/Desktop/vscode/Genm-codex/skills/novel-outline/SKILL.md)
  - 仅在 premise 仍松散、用户要 worldbuilding enrichment、路线明显依赖脑洞混搭时读取母题目录
  - 明确要求最多解析：
    - `1` 个 worldview motif
    - optional `1` mechanism motif
    - optional `1` packaging motif
  - 且要求只把其转为 premise / conflict engine / visible cost / hidden truth direction

- [novel-package](file:///Users/arm/Desktop/vscode/Genm-codex/skills/novel-package/SKILL.md)
  - 仅在 package 需要更强世界观钩子、或项目仍是 concept-first 时读取母题目录
  - 明确要求只用选中的 motif cue 强化一句话 premise、世界观钩子与开篇包装，不得把多个母题名称直接堆进对外包装

判断：

- 3 个 consumer 都在“条件触发 + 限量使用 + 不外溢”边界内
- 当前没有任何一个 consumer 把 motif 目录当成默认全量加载真值库

---

### 2.4 `state.meta.motifs` 是否已膨胀为项目状态真值中心
**思考强度：L4 审慎**

结论：**当前未发现落地使用。**

证据：

- 全仓库范围内未检索到 Python 代码对 `state.meta.motifs` 的读写使用
- 全仓库范围内未检索到 JSON 状态中已经落地的 `"motifs"` 字段实例

判断：

- 这意味着当前仓库并没有把 motif 选择固化成另一个与 `总纲 / 设定集 / sidecar` 并列的状态真值中心
- 从边界控制上，这是好现象
- 但也说明：若未来真的引入 `state.meta.motifs`，必须继续维持“高层 premise 输入”而不能升级成运行时 canon

---

### 2.5 Runtime Boundary 是否仍与 P0-F 边界一致
**思考强度：L3 深度**

结论：**一致。**

证据：

- [runtime-boundary-adr.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/runtime-boundary-adr.md) 明确要求：
  - 继续维持 `repo truth + sidecar + MCP`
  - 不进入 daemon / scheduler / plugin framework / orchestration runtime
  - 不允许形成第二真值中心

判断：

- P0-F 当前的母题输入层设计与 runtime boundary 没有冲突
- 母题目录仍然是 repo-owned 的只读参考输入，而不是 runtime truth

---

## 三、风险判断

**思考强度：L4 审慎**

当前没有发现需要立即修正的实现风险，但存在 2 个后续应持续盯住的漂移风险：

1. **consumer 未来可能把 motif 目录从条件性输入变成默认重输入**
   - 风险：outline / package 过度依赖脑洞目录，而弱化项目真值

2. **未来若引入 `state.meta.motifs` 字段，可能被误用为持久真值**
   - 风险：项目状态层出现“第二套世界观真值”

当前这两个风险都尚未发生，只需保留在持续复检清单中。

---

## 四、建议动作

**思考强度：L3 + L4**

### 当前不需要做的
- 不需要修改 `creative-brief`
- 不需要修改 `worldview-motif-catalog`
- 不需要修改 `novel-init / novel-outline / novel-package`
- 不需要为 `state.meta.motifs` 新增实现

### 建议保留的后续复检点
1. 后续若改 `novel-init / novel-outline / novel-package`，优先复检它们是否仍保持“条件读取 + 限量选择 + 不上升为 canon”
2. 后续若引入 `state.meta.motifs`，必须先补一条明确规则：
   - 仅可作为高层 premise 输入摘要
   - 不得替代 `总纲 / 设定集 / 世界观规则说明`
3. 后续若新增 `设定集/世界观/*.md` 模板，应保持“规则说明 / 关键异常 / 代价 / 真相方向”的轻量定位，不应膨胀成大而空的百科库

---

## 五、本轮结论摘要

**思考强度：L3 深度**

P0-F 母题输入层当前状态良好，边界清楚，consumer 接线合理，未发现第二真值中心膨胀，也未发现 runtime boundary 被突破。该项当前不需要进入修正实施，更适合作为 v1.5 下一阶段中的**持续复检项**继续保留。
