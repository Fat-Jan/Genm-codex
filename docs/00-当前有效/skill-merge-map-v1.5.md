# `v1.5` Skill Merge Map

## 目的

这份文档把 `P2-D` 需要的 merge / alias / protected 结果收成一份可落地映射，供后续迁移说明、弃用说明和入口兼容层使用。

当前它是文档化结论，不直接触发破坏性合并。

---

## `protected`

当前继续视为 `protected` 的包括：

- `novel-init`
- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-close`
- `novel-status`
- `novel-query`
- `novel-precheck`
- `novel-package`
- `novel-scan`

这些入口不在 `v1.5` 做破坏性改名或删除。

---

## `alias-now`

### 安装层 alias

继续保留：

- `novel-*`
- `genm-novel-*`

### 调用面 alias 候选

- `novel-retrieve` → 解释为 `novel-query` 的快速检索面
- `novel-batch` → 解释为 `novel-write` 的批量推进面

当前只做说明，不做删除旧入口。

---

## `boundary-only`

这类当前不进入真合并，只做边界说明：

- `novel-workflow` / `novel-resume`
- `novel-fix` / `novel-polish` / `novel-rewrite`

说明口径：

- 恢复 / 状态类保持双入口
- 修章类按局部问题、语言层问题、结构层问题做职责分流

---

## `deferred-merge`

`v1.5` 当前明确不做：

- 真正的 `31 -> 25` skill 大合并
- skill 删除
- frontmatter 名称直接改写
- 安装脚本入口裁撤

这些都留到 `v1.5` 之后再决定。
