# 样本库 / Regression 维护清单 v1

> 目的：把 `v1.5` 已确认稳定的样本库 / regression 维护规则整理成一份可直接执行的清单，避免后续只改索引、不改 manifest，或增加 regression 样本却不写清楚它在防什么退化。
>
> 适用对象：主 agent、协作 agent、后续维护者。

---

## 一、默认维护原则

**思考强度：L3 + L4**

后续维护样本库时，默认遵循以下原则：

1. **manifest-first**
   - 样本的 machine-readable 真值入口始终是 `shared/templates/sample-manifest-v1.json`
   - 新增、变更、归档样本时，先改 manifest，再改索引页 / 矩阵页 / 治理文档

2. **regression-target-first**
   - 只要样本被归类为 `regression`，必须明确它要防什么退化
   - 如果说不清“防什么”，就不应直接进入 regression 层

3. **bucket coverage 不等于 regression coverage**
   - bucket sample 的核心职责是题材落点覆盖
   - 不自动承担 regression 样本职责

4. **索引页是浏览层，不是真值入口**
   - `sample-library-index.md` 与 `sample-library-matrix-v1.5.md` 用于浏览与说明
   - 不应用来替代 manifest 的真值角色

---

## 二、执行清单

### 1. 新增样本
**思考强度：L2 标准**

新增样本前，先回答：

- 它是 `smoke` 还是 `project`
- 它的 `trust_tier` 是什么
- 它是题材覆盖样本、质量基准样本，还是 regression 样本
- 如果是 regression，它防什么退化
- 它是否需要 `verification_targets`

执行顺序：

1. 更新 `shared/templates/sample-manifest-v1.json`
2. 如需要，更新 `sample-library-index.md`
3. 如需要，更新 `sample-library-matrix-v1.5.md`
4. 如需要，更新治理说明文档

最小通过标准：

- manifest 中有对应条目
- `sample_type / trust_tier / status` 明确
- 若为 regression，`verification_targets` 或等价说明明确

---

### 2. 更新样本
**思考强度：L2 标准**

更新已有样本时，至少检查：

- 路径是否仍然有效
- `status` 是否仍是 `active`
- 当前分层是否仍合理
- regression 样本的退化目标是否仍准确
- bucket sample 是否仍代表该题材落点

执行顺序：

1. 先更新 manifest 中的状态 / 标签 / target
2. 再更新索引页、矩阵页中的人读说明
3. 如涉及治理口径变化，再更新治理文档

---

### 3. 归档或移除样本
**思考强度：L3 深度**

样本归档前，至少确认：

- 不再被 smoke / regression / docs / tests 引用
- 已有更稳定替代项，或该样本本身已无维护价值
- manifest、索引页、矩阵页可同步更新

执行顺序：

1. 先处理 manifest：改 `status` 或移除条目
2. 再处理索引页 / 矩阵页
3. 如有必要，补归档说明

---

### 4. 新增 regression 样本
**思考强度：L3 深度**

只有同时满足以下条件，才建议把样本纳入 `regression`：

- 存在明确退化风险
- 样本能稳定复现该风险或覆盖该风险面
- 后续测试 / consumer 确实会读取或受益
- 能写出最小 `verification_targets`

建议至少写清：

- 防的是什么退化
- 对应哪类测试或 consumer
- 为什么现有 baseline / high_confidence / bucket sample 不足以覆盖

---

## 三、推荐字段检查表

**思考强度：L1 轻量**

维护 manifest 时，优先检查：

| 字段 | 是否必看 | 说明 |
|---|---|---|
| `sample_id` | 是 | 唯一标识 |
| `path` | 是 | 路径是否仍有效 |
| `sample_type` | 是 | `smoke` / `project` |
| `trust_tier` | 是 | `baseline` / `derived` / `regression` / `high_confidence` / `bucket_sample` |
| `status` | 是 | `active` / `archived` / `draft` |
| `verification_targets` | 建议 | regression 样本优先保留 |
| `notes` | 建议 | 用一句话解释样本用途 |

---

## 四、不建议的做法

**思考强度：L4 审慎**

后续维护时，不建议：

1. 只更新 `sample-library-index.md`，不更新 manifest
2. 把 bucket sample 直接写成 regression 样本而不解释退化目标
3. 增加 regression 样本，但不说明其测试 / consumer 关联
4. 把索引页重新当成真值入口
5. 在没有明确用途时持续膨胀样本数量

---

## 五、最小维护闭环

**思考强度：L2 标准**

后续每次样本维护，最小闭环建议为：

1. 改 manifest
2. 对齐索引页 / 矩阵页
3. 如涉及 regression，确认目标清晰
4. 跑一次项目验证：
   - `bash scripts/validate-migration.sh`

---

## 六、结论

**思考强度：L3 深度**

样本库 / regression 体系当前已经具备长期维护基础。后续最重要的不是继续扩文档，而是把“manifest-first + regression-target-first”真正执行成日常维护动作。只要守住这条线，样本体系就不容易再退回到“人读索引驱动、机器真值漂移”的旧状态。
