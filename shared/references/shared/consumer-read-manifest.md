# Consumer Read Manifest

## 目的

这份 manifest 收高频 consumer skill 的共享读档协议。

当前适用对象：

- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-package`
- `novel-precheck`

使用方式：

- 先引用这里的共享 bundle
- 再在各自 `SKILL.md` 里补 `skill-local additions`
- 不要求所有 consumer 完全一样，但共享部分优先以这里为准

## Shared Bundles

### `baseline-core`

默认共享基线：

- `.mighty/state.json`
- `../../shared/references/shared/core-constraints.md`
- `../../docs/anti-flattening-framework/README.md`
- `../../docs/anti-flattening-framework/01-总纲.md`
- `../../docs/opening-and-plot-framework/README.md`
- `../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md`
- `../../docs/writing-core-framework/README.md`

### `launch-stack`

开篇协议栈共享项：

- `../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md`
- `../../docs/opening-and-plot-framework/fanqie-launch-stack/05-compiler-contract.md`
- `.mighty/launch-stack.json`

### `content-positioning`

组合题材 / 结构风味共享项：

- `.mighty/content-positioning.json`

### `active-context`

写作 / 审查窗口共享侧栏：

- `.mighty/active-context.json`

### `market-adjustments`

市场与策略摘要共享项：

- `.mighty/market-adjustments.json`
- `.mighty/market-data.json`

### `fanqie-bucket`

番茄 bucket 共享规则：

- `../../docs/fanqie-content-buckets.md`
- `../../docs/fanqie-bucket-constraints.md`
- `../../docs/fanqie-mvp-buckets.yaml`
- `../../docs/fanqie-mvp-bucket-templates.md`
- `../../docs/fanqie-writing-techniques.md`
- `../../docs/fanqie-rule-priority-matrix.md`
- `../../docs/fanqie-resistance-and-cost-rules.md`

### `fanqie-tagpack`

番茄 tagpack 共享规则：

- `../../docs/fanqie-mvp-tagpacks.yaml`

## Skill-local additions

以下内容通常仍保留在各 skill 本地：

- 目标章节文件
- 目标角色 / 设定文件
- 某个 skill 独有的评估卡 / 输出合同
- 明确只被单一 skill 使用的参考文档
