# Sample / Regression 维护实战演练 2026-03-31

> 执行模板来源：
> [maintenance-specialized-template-pack-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/maintenance-specialized-template-pack-v1.md) 中的“模板 B：Sample / Regression 维护执行模板”。
>
> 目的：用已经落地的专项执行模板，真实跑一轮样本体系维护检查，验证模板是否足够可执行、结果是否足够可复检。

---

## 一、输入材料

**思考强度：L1 + L2**

本轮按模板实际读取：

- [sample-manifest-v1.json](file:///Users/arm/Desktop/vscode/Genm-codex/shared/templates/sample-manifest-v1.json)
- [sample-library-index.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/sample-library-index.md)
- [sample-library-matrix-v1.5.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/sample-library-matrix-v1.5.md)
- [test_real_regression_samples.py](file:///Users/arm/Desktop/vscode/Genm-codex/tests/test_real_regression_samples.py)
- [test_real_e2e_novel_smoke.py](file:///Users/arm/Desktop/vscode/Genm-codex/tests/test_real_e2e_novel_smoke.py)
- [sample-regression-maintenance-checklist-v1.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/sample-regression-maintenance-checklist-v1.md)

---

## 二、执行摘要

**思考强度：L3**

本轮使用“Sample / Regression 维护执行模板”做了一次真实专项演练，结论如下：

1. 样本体系当前仍遵循 **manifest-first**
2. regression 样本仍遵循 **regression-target-first**
3. bucket sample 当前没有被误当 regression 样本
4. index / matrix 仍保持浏览层定位
5. 发现 1 项低风险人读文档语义滞后：
   - `sample-library-index.md` 的“样本维护”段仍偏旧式“只更新索引页”口径，且完成标记未现状化
6. 该问题已在本轮直接修正
7. 本轮不需要升级为结构问题或专项治理

---

## 三、检查结果表

**思考强度：L3 + L4**

| 项目 | 当前状态 | 证据 | 结论 | 风险 | 建议动作 |
|---|---|---|---|---|---|
| manifest 是否为 machine-readable 真值入口 | 稳定 | `sample-manifest-v1.json`、`sample-library-index.md`、`sample-library-matrix-v1.5.md` | 是 | 低 | 无需动作 |
| regression 样本是否写清退化目标 | 稳定 | `jiazhuangdan-regression` 的 `verification_targets`，以及 `test_real_regression_samples.py` | 是 | 低 | 无需动作 |
| bucket sample 是否仍承担题材覆盖而非 regression 责任 | 稳定 | manifest 中 `trust_tier = bucket_sample` 的多条项目样本 | 是 | 低 | 无需动作 |
| smoke / regression 样本是否有真实测试入口 | 稳定 | `test_real_regression_samples.py`、`test_real_e2e_novel_smoke.py` | 是 | 低 | 无需动作 |
| 索引页是否存在“只更新索引、不更新 manifest”的旧语义 | 存在轻微滞后表述 | `sample-library-index.md` 的“样本维护”段和完成标记 | 属于低风险历史残留 | 低 | 本轮已直接修正 |

---

## 四、已处理项

**思考强度：L2**

本轮已直接处理：

1. 更新 [sample-library-index.md](file:///Users/arm/Desktop/vscode/Genm-codex/docs/00-当前有效/sample-library-index.md)
   - 将“样本维护”改为 manifest-first 口径：
     - 先改 manifest
     - 再改索引页
     - 再按需改矩阵页和治理文档
   - 补充 regression 样本更新时需确认退化目标
   - 将“清理样本”更新为先确认引用，再先改 manifest
   - 将完成标记改为与当前现状一致的已完成状态

---

## 五、保留项

**思考强度：L4**

本轮未发现需要继续保留的中高风险项。

仍需长期持续复检、但本轮不构成问题的边界包括：

1. 新增样本时不得只改 index，不改 manifest
2. 新增 regression 样本时必须继续写清退化目标
3. bucket sample 仍只承担题材覆盖，不默认承担 regression 责任

这些属于长期维护规则，不属于本轮未闭环问题。

---

## 六、是否需要升级

**思考强度：L4**

**结论：不需要。**

原因：

- 本轮仅发现 1 项低风险文档语义滞后
- 已在本轮直接修正
- 未发现 manifest / tests / matrix / index 之间的结构性失配

---

## 七、模板实战结果评价

**思考强度：L3**

本次实战说明：

1. “模板 B：Sample / Regression 维护执行模板”可以直接驱动真实检查
2. 模板要求的输入、步骤、边界和输出结构足够完整
3. 主 agent 可直接复检本轮交付，无需额外重建检查框架

因此，这份专项执行模板已经通过了一次真实维护任务验证。
