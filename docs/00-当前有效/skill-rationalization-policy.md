# Skill Rationalization Policy

## 目的

为 `31 -> 25` 这类 skill 收敛工作先定政策边界，避免在 `v1.5` 里直接做破坏性大合并。

这份政策只回答三件事：

1. 哪些 skill 可以考虑 `merge`
2. 哪些只能先做 `alias`
3. 哪些必须保持 `protected`

---

## 当前结论

`v1.5` 不做真正的 skill 大合并，只做：

- overlap inventory
- merge map
- alias / deprecation policy

不做：

- 直接删除 skill
- 直接改 frontmatter `name`
- 直接移除 `install-skills.sh` 中的安装名

---

## 三种决策

### `merge`

只适用于：

- 语义边界高度重叠
- 下游调用面可控
- 已有稳定替代路径

### `alias`

适用于：

- 旧入口仍有历史调用价值
- 但主入口已经清晰
- 可以先保留兼容名，再慢慢去文档化

### `protected`

适用于：

- 高频主链 skill
- 实验边界敏感 skill
- 直接牵动 install / discoverability / workflow contract 的 skill

---

## 当前 `protected` 范围

至少包括：

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

原因：

- 这些 skill 直接处在默认工作流、高频 consumer 或实验边界上
- 尤其 `novel-scan` 当前仍是实验能力，不进入 skill merge

---

## 当前 `alias` 范围

`install-skills.sh` 继续保留两套安装名：

- `novel-*`
- `genm-novel-*`

在 `v1.5` 里，这两套入口继续视为 alias 层，不做删除。

也就是说：

- `install-skills.sh` 先不减名
- 先做 merge map
- 后续再决定哪些 alias 可以进入弃用周期

---

## 与安装脚本的关系

`install-skills.sh` 当前仍是稳定入口，因此：

- 任何 skill rationalization 不能先改安装脚本，再补政策
- 必须先有 merge / alias / protected 结论
- 再决定是否改 `install-skills.sh`

---

## `mimo` 可做范围

在这份政策落地后，`mimo` 可以做：

- 31 个 skill 的 overlap inventory
- merge map 文档化
- alias / deprecation 说明稿

但不应直接做：

- skill 删除
- frontmatter 改名
- `install-skills.sh` 入口移除

这些仍由 `codex` 执行。
