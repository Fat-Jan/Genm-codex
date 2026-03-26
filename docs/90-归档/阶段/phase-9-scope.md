# Genm-codex 第九阶段范围设计

## 设计结论

第九阶段不再优先追求“再补多少命令”，而是直接围绕项目本质推进：

- 提高正文生成质量
- 提高平台适配度
- 提高作品包装完成度

基于旧项目资产和当前迁移状态，第九阶段拆成两条并行线：

- **Phase 9A：包装生成层**
- **Phase 9B：质量闭环整合**

这两条不再做二选一，而是并行推进，但共享写点统一收口。

---

## Phase 9A：包装生成层

### 目标

补齐当前最明显的写作价值缺口：

- 书名建议
- 简介生成与平台适配
- 角色命名建议
- 开篇钩子包装

### 实现策略

第一版不拆成多个命令，而是统一收进：

- `novel-package`

这样做的原因是：

- 包装相关能力共享同一套项目输入
- 都会依赖题材、平台、总纲、市场扫描结果
- 拆成多个命令会让边界变碎，后续更难维护

### 第一版边界

支持：

- `title`
- `synopsis`
- `naming`
- `opening-hook`
- `full`

支持的保存目标：

- `包装/书名方案.md`
- `包装/简介方案.md`
- `包装/命名方案.md`
- `包装/开篇包装.md`
- `包装/包装方案.md`

不做：

- 自动改 `.mighty/state.json`
- 自动改 shared profile
- 自动替换总纲里的书名或简介
- 平台上传自动化

---

## Phase 9B：质量闭环整合

### 目标

把已经迁过来的高价值命令真正整合成统一质量系统：

- `novel-write`
- `novel-review`
- `novel-fix`
- `novel-polish`
- `novel-rewrite`
- `novel-precheck`
- `novel-learn`

### 要解决的问题

- AI 味口径仍然分散
- 平台适配、节奏、爽点、追读力的指标没有完全统一
- `learn` 对写作链的反哺还不够明确
- `review -> fix/polish/rewrite -> precheck` 的协同规则还不够稳定

### 第一阶段产物

先不急着大改 skill，而是先落：

- 一份质量闭环整合设计文档
- 一组统一指标与衔接建议

---

## 并行策略

第九阶段开始显式采用“小颗粒并行”：

1. 主线：实现 `novel-package`
2. 并行线：完成质量闭环整合设计
3. 收口线：统一更新：
   - `docs/90-归档/迁移与RC/codex-migration-plan.md`
   - `docs/90-归档/迁移与RC/migration-map.md`
   - `README.md`
   - `scripts/install-skills.sh`
   - `scripts/validate-migration.sh`

---

## 推荐实施顺序

1. `Phase 9A / P0`
   - 创建 `novel-package`
   - 跑首轮 smoke
2. `Phase 9B / P0`
   - 落质量闭环整合设计
3. `Phase 9A / P1`
   - 把 `novel-scan` 的市场信号更明确地喂给包装层
4. `Phase 9B / P1`
   - 选择性增强 `write/review/precheck/learn` 的统一质量口径

---

## 版本边界建议

- **`v0.13.0`**：
  - `novel-package` 第一版稳定
  - 第九阶段设计文档落地

- **`v0.14.0`**：
  - 如果质量闭环整合进入第一轮实现

---

## 当前推荐下一步

第九阶段的第一步，不是继续补低价值命令，而是：

1. 先做 `novel-package`
2. 同时写完质量闭环整合设计

这是当前最贴近“提高小说写作生成效果”的高回报推进方向。
