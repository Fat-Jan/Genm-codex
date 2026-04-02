# Post-Write Validator Compatibility Note

**归档日期**：2026-03-30
**归档依据**：orphan-asset-archive-v1.md
**原位置**：shared/validators/post-write-validator.md

---

这份文档用于承接旧的 shared 引用。

当前 `Genm-codex` 里，写后验证相关的权威入口主要是：

- [strong-quality-gate-policy.json](file:///Users/arm/Desktop/vscode/Genm-codex/docs/strong-quality-gate-policy.json)
- [skills/novel-close/SKILL.md](file:///Users/arm/Desktop/vscode/Genm-codex/skills/novel-close/SKILL.md)
- [gate-triage.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/gate-triage.md)

如果你需要判断"本章写完后是否仍有客观 blocker"，优先看这些入口，而不是继续寻找已不存在的旧 validator 文档。

---

**归档原因**：无任何脚本/测试/技能实际消费，仅为兼容重定向说明页。Validator 概念已迁移至 `scripts/post_write_lint.py` 及 gate policy json。
