# Orphan Asset Archive v1

**归档日期**：2026-03-30
**归档依据**：空挂 / 依赖现实盘点 v1 + 复检 v1
**归档决策**：Orphan Lane（vacuum orphan）确认文件，从 sync-governance.json v1.1 移除保护并归档

---

## 归档文件清单

| 文件路径 | sync-governance v1.1 保护状态 | 消费证据 | 归档原因 |
|---|---|---|---|
| `shared/references/commands/novel-review.md` | references 域 protected | E1，无任何消费 | Governance 保护意图残留，无消费者 |
| `shared/templates/chapter-structure/template-validation-rules.md` | templates 域 protected | E0，无任何消费 | Governance 保护意图残留，无消费者 |
| `shared/validators/post-write-validator.md` | 不在保护名单 | E1，无任何消费 | Validator 概念已迁移至 post_write_lint.py 和 gate policy json |

---

## 归档理由详述

### shared/references/commands/novel-review.md

- sync-governance v1.1 第 188 行被列为 protected_local_paths
- 仓库内无任何 scripts/tests/skills 引用
- 命令参考文档，但无命令真正调用它
- **归档结论**：vacuum orphan，移除保护，物理文件归档

### shared/templates/chapter-structure/template-validation-rules.md

- sync-governance v1.1 第 205 行被列为 protected_local_paths
- 仓库内无任何 scripts/tests/skills 引用
- 模板验证规则文档，但无任何校验逻辑接入
- **归档结论**：vacuum orphan，移除保护，物理文件归档

### shared/validators/post-write-validator.md

- 不在 sync-governance v1.1 保护名单中
- 仓库内无任何 scripts/tests/skills 引用
- Validator 概念的实际落地已迁移至：
  - `scripts/post_write_lint.py`
  - `docs/strong-quality-gate-policy.json`
  - `docs/setting-gate-policy.json`
- **归档结论**：不在 governance 保护名单，物理文件归档

---

## 相关治理动作

- sync-governance.json 版本从 v1.1 升级至 v1.2
- 移除：`commands/novel-review.md`（references 域）
- 移除：`chapter-structure/template-validation-rules.md`（templates 域）
- shared/validators/ 目录清空后已无其他文件，可考虑删除目录

---

## 后续建议

Review Lane 的 `shared/references/shared/consumer-read-manifest.md` 属于 dependency illusion，建议：
- 将 6 个 SKILL.md 中的声明从 required-like 降为 reference-like
- 不从 sync-governance 移除（文件本身有价值）
- 在 docs 中补充说明其"声明密度高但程序消费弱"的特性
