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
| `projects/转学第一天，我把校草认成了新来的代课老师` | 真实项目 | 番茄 | `校园 / 青春甜宠` | `draft` | `confidence = medium`，`bucket_grade = pass` |
| `projects/公司裁我那天，系统先赔了我一百万` | 真实项目 | 番茄 | `都市 / 都市脑洞` | `draft` | `confidence = medium`，`bucket_grade = warn` |
| `projects/她升职那天，前上司成了我合租室友` | 真实项目 | 番茄 | `现代言情 / 职场婚恋` | `draft` | `confidence = medium`，`bucket_grade = pass` |
| `projects/搬回老小区后，我靠蹭饭认识了整栋楼` | 真实项目 | 番茄 | `都市日常 / 都市日常` | `draft` | `confidence = medium`，`bucket_grade = pass` |
| `projects/宗门垫底那年，我把废丹卖成了天价` | 真实项目 | 番茄 | `玄幻 / 玄幻脑洞` | `draft` | `confidence = medium`，`bucket_grade = pass` |
| `projects/我在县衙当杂吏，靠翻旧案升了堂` | 真实项目 | 番茄 | `历史脑洞 / 历史脑洞` | `draft` | `confidence = medium`，`bucket_grade = pass` |
| `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人` | 真实项目 | 番茄 | `豪门总裁 / 豪门总裁` | `draft` | `confidence = medium`，`bucket_grade = pass` |
| `projects/我在县衙誊旧档，靠半页供词改了判词` | 真实项目 | 番茄 | `历史脑洞 / 历史脑洞` | `draft` | `confidence = medium`，`bucket_grade = pass` |
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

### 1.5. 非宫斗真实 P0 桶

两个真实非宫斗 P0 项目现在都已经能稳定输出结构化 `draft`，并且不再停留在纯低置信草稿：

- `projects/转学第一天，我把校草认成了新来的代课老师`
  - `bucket = 青春甜宠`
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`
- `projects/公司裁我那天，系统先赔了我一百万`
  - `bucket = 都市脑洞`
  - `confidence = medium`
  - `bucket_grade = warn`
  - `submission_fit = fit`

这说明：

- `fanqie_p0_smoke.py` 已经不再只是宫斗主场工具
- `青春甜宠 / 都市脑洞` 两条线都已具备真实项目 smoke 与轻量写回样本
- 非宫斗桶仍比 `宫斗宅斗` 更保守，但已经能给出结构化差异判断

### 1.6. 新增三条非宫斗真实 P0 样本

这三条新增真实项目也已收敛到可复用判断：

- `projects/她升职那天，前上司成了我合租室友`
  - `bucket = 职场婚恋`
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`
- `projects/搬回老小区后，我靠蹭饭认识了整栋楼`
  - `bucket = 都市日常`
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`
- `projects/宗门垫底那年，我把废丹卖成了天价`
  - `bucket = 玄幻脑洞`
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`

这说明：

- `fanqie_p0_smoke.py` 已经从 3 类真实样本扩到 6 类真实样本
- 非宫斗路线不再只靠 `青春甜宠 / 都市脑洞` 两条线支撑
- `职场婚恋 / 都市日常 / 玄幻脑洞` 已经具备真实项目 smoke + 轻量写回样本

### 1.7. P0 收口样本补齐

剩余两个此前缺口桶也已补齐：

- `projects/我在县衙当杂吏，靠翻旧案升了堂`
  - `bucket = 历史脑洞`
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`
- `projects/签下离婚协议那天，冷脸总裁改口叫我合伙人`
  - `bucket = 豪门总裁`
  - `confidence = medium`
  - `bucket_grade = pass`
  - `submission_fit = fit`

这说明：

- 当前 `P0 8 桶` 已全部拿到至少 1 条真实项目样本
- 默认工作流的第一轮平台特化验证已经从“覆盖多数桶”推进到“覆盖全部 P0 桶”

### 1.8. 第二条历史脑洞样本

历史脑洞现在已经不再是单样本：

- `projects/我在县衙当杂吏，靠翻旧案升了堂`
- `projects/我在县衙誊旧档，靠半页供词改了判词`

这两条都已收敛到：

- `confidence = medium`
- `bucket_grade = pass`
- `submission_fit = fit`

这说明：

- `历史脑洞` 当前的强信号门槛已经不只是被单一“盐脚案”样本支撑
- 这条桶的下一步优先级可以下调，转去补更有区分度的第三条样本

### 1.9. 第二批样本继续扩到三个桶

这轮继续补了：

- `projects/离婚冷静期那天，前夫把董事会席位押给了我`
  - `bucket = 豪门总裁`
  - `confidence = medium`
  - `bucket_grade = pass`
- `projects/我赔光积蓄那天，系统先把违约金打到了账上`
  - `bucket = 都市脑洞`
  - `confidence = medium`
  - `bucket_grade = warn`
- `projects/外门药田被夺那天，我靠废丹拍卖赚回了灵石`
  - `bucket = 玄幻脑洞`
  - `confidence = medium`
  - `bucket_grade = pass`

这说明：

- `豪门总裁 / 都市脑洞 / 玄幻脑洞` 也不再是单样本桶
- 当前真正还缺第二条真实样本的，只剩 `青春甜宠 / 职场婚恋 / 都市日常`

### 1.10. 双样本覆盖完成

这轮最后又补了三条：

- `projects/代理续约那天，我和前搭档被公司按进了同一套合租房`
  - `bucket = 职场婚恋`
  - `confidence = medium`
  - `bucket_grade = pass`
- `projects/广播站误放表白信那天，我和学神被迫参加学习互助`
  - `bucket = 青春甜宠`
  - `confidence = medium`
  - `bucket_grade = pass`
- `projects/母亲复健那年，我把楼道白板改成了换饭地图`
  - `bucket = 都市日常`
  - `confidence = medium`
  - `bucket_grade = pass`

这说明：

- `青春甜宠 / 职场婚恋 / 都市日常` 也已经不再是单样本桶
- 到这里，`P0 8 桶` 已全部完成双样本覆盖

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

- 各个 `P0` 桶在第二条、第三条真实样本上的稳定性
- 各个 `P0` 桶在第三条真实样本上的稳定性
- `现实情感` / `系统流` 是否该做 bucket alias 或扩桶
- 非宫斗路线的 `confidence` 是否需要更细化

## 下一步建议

优先级最高的不是继续做大改，而是二选一：

1. 为关键桶补第三条真实项目样本
   - 优先 `都市脑洞`
   - 其次 `豪门总裁 / 玄幻脑洞 / 历史脑洞`
2. 在有更多真实样本后，再决定是否进入 `v1.2`
   - 细化非宫斗路线的 `confidence`
   - 或继续压缩 `writeback_preview` 的冲突提示

一句话：

- 现在工具已经拿到 `P0 8 桶` 的双样本覆盖；下一步不是补空桶，而是补第三条不同路数样本继续压门槛。
