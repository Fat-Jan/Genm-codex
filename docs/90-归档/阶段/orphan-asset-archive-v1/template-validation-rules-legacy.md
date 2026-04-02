# 十章结构模板验证规则

**归档日期**：2026-03-30
**归档依据**：orphan-asset-archive-v1.md
**原位置**：shared/templates/chapter-structure/template-validation-rules.md

---

## 归档说明

本文件已归档。模板验证逻辑的实际落地已迁移至：

- `scripts/post_write_lint.py`
- `docs/strong-quality-gate-policy.json`
- `docs/setting-gate-policy.json`
- `skills/novel-close/SKILL.md`

本文件保留作为历史参考，不参与任何活跃工作流。

---

## 原文件内容

### 验证目标

确保十章结构模板符合番茄平台要求，满足快节奏、高密度爽点、强钩子等核心标准。

### 平台适配性验证

番茄平台核心指标：

```yaml
required_metrics:
  - cool_point_density: "≥1.5/千字"
  - hook_strength: "≥80分"
  - chapter_length: "2500-3200字"
  - golden_finger_appearance: "<800字"
  - opening_conflict: "<1000字"
```

### 综合评分体系

| 维度 | 权重 | 满分 | 合格线 |
|------|------|------|--------|
| 平台适配度 | 30% | 100 | ≥80 |
| 结构完整性 | 25% | 100 | ≥85 |
| 爽点密度 | 20% | 100 | ≥90 |
| 钩子质量 | 15% | 100 | ≥80 |
| 内容创新 | 10% | 100 | ≥70 |

---

**最后更新**: 2026-03-18
**维护者**: Claude Code
**状态**: 已归档（2026-03-30）
