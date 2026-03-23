# Fanqie P0 Smoke 压力测试结果（2026-03-24）

## 目标

验证 `scripts/fanqie_p0_smoke.py v1.1` 在当前仓库已有的真实项目与 smoke 样本上是否表现稳定，重点看：

1. 命中 `P0` bucket 的项目是否能稳定输出 `draft`
2. 未命中 `P0` bucket 或证据不足的样本是否会保守降级成 `scaffold-only`
3. `confidence / evidence_count / sidecar signals / writeback_preview` 是否在支持桶路径上正常出现

## 测试矩阵

| 样本 | 来源类型 | 平台 | 原始 genre/bucket | 结果 | 备注 |
|------|----------|------|-------------------|------|------|
| `projects/庶女谋略` | 真实项目 | 番茄 | `宫斗宅斗 / 宫斗宅斗` | `draft` | `confidence = high` |
| `projects/庶妹换我婚书那夜，太子先开了口` | 真实项目 | 番茄 | `宫斗宅斗 / 宫斗宅斗` | `draft` | `confidence = high` |
| `smoke/e2e-tianchong` | smoke 样本 | 番茄 | `言情 / 现言甜宠` | `scaffold-only` | alias 到 `青春甜宠`，但当前证据不足 |
| `smoke/e2e-tianchong-evil` | smoke 样本 | 番茄 | `言情 / 现言甜宠` | `draft` | alias 到 `青春甜宠`，`confidence = low` |
| `smoke/e2e-dual-substitute-evil-antiflattening-20260322` | smoke 样本 | 番茄 | `言情 / 现言甜宠` | `draft` | alias 到 `青春甜宠`，`confidence = low` |
| `smoke/e2e-qinggan-evil-antiflattening-20260322` | smoke 样本 | 番茄 | `现实题材 / 现实情感` | `scaffold-only` | 当前不在 P0 列表 |
| `smoke/e2e-system-antiflattening-20260322` | smoke 样本 | 番茄 | `系统流 / none` | `scaffold-only` | 当前不在 P0 列表 |

## 代表性结果

### 1. `宫斗宅斗` 支持桶

两个真实项目都成功输出：

- `fanqie_bucket_review_summary`
- `fanqie_bucket_precheck_summary`
- `confidence`
- `evidence_count`
- `signals_used`
- `writeback_preview`

并且当前都判为：

- `bucket = 宫斗宅斗`
- `confidence = high`

这说明：

- `v1.1` 对当前最成熟的 P0 桶已经可用
- sidecar 信号读取没有把主判断搞乱

### 2. 未命中或证据不足样本

三个样本当前都自动降级成：

- `scaffold-only`

并在文档里保留：

- `smoke/e2e-tianchong`：
  - 已经 alias 到 `青春甜宠`
  - 但当前章节证据不足，所以仍降级
- `smoke/e2e-qinggan-evil-antiflattening-20260322` / `smoke/e2e-system-antiflattening-20260322`：
  - 当前原始 `genre`
  - 当前 bucket 无法稳定命中 P0 的说明

### 3. alias 样本

`现言甜宠 -> 青春甜宠` alias 已跑通：

- `smoke/e2e-tianchong`
- `smoke/e2e-tianchong-evil`
- `smoke/e2e-dual-substitute-evil-antiflattening-20260322`

当前结果是：

- `smoke/e2e-tianchong-evil` / `smoke/e2e-dual-substitute-evil-antiflattening-20260322`
  - `effective_mode = draft`
  - `bucket = 青春甜宠`
  - `confidence = low`
- `smoke/e2e-tianchong`
  - `bucket = 青春甜宠`
  - 但因证据不足仍是 `scaffold-only`

这说明：

- alias 现在已经能把接近 `P0` 的历史样本拉进可分析范围
- alias 只负责桶归一，不会绕过证据门槛
- 工具仍然保持保守，不会把它们伪装成高置信判断

这说明：

- 当前工具的保守边界是稳定的
- 不会因为看见“番茄项目”就胡乱产出高置信草稿

## 当前结论

### 已证明的

- `fanqie_p0_smoke.py v1.1` 对 `宫斗宅斗` 已具备可用性
- `draft` 路径的证据来源、辅助信号、preview 都能正常输出
- unsupported 或证据不足样本会稳定降级
- `现言甜宠 -> 青春甜宠` alias 已生效，其中两个甜宠代理样本能产出低置信 `draft`

### 尚未证明的

- 其它 `P0` 桶在真实项目上的稳定性
- `青春甜宠` 当前证据门槛是否合适，还是要补更贴近真实项目的样本
- `现实情感` / `系统流` 是否该做 bucket alias 或扩桶
- 非宫斗路线的 `confidence` 是否需要更细化
- `青春甜宠` 当前仍只有代理样本，没有真实项目样本

## 下一步建议

优先级最高的不是继续做大改，而是二选一：

1. 找到一个真实或接近真实的 `P0` 非宫斗样本
   - 例如 `青春甜宠` / `都市脑洞`
   - 继续压测工具边界
2. 如果仓库短期内拿不到这样的样本，再考虑：
   - 为 `现实情感`
   - 或其它常见近邻桶
   建 alias / 扩桶策略

一句话：

- 现在工具在“最强样本桶”上已经站住了，甜宠 alias 路径也跑通了，但它仍然受证据门槛约束，而且还没有拿到真正的非宫斗 P0 真实项目。
