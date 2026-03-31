# Profiles 稳定保留门槛检查清单 v1

> 用于判断一个 profile 是否已达到"稳定保留"标准。
>
> 来源：本清单通过 gaowu / cthulhu / livestream / realistic / workplace-romance 五个试点样本的经验归纳得出。

---

## 一、核心判断原则

1. **不能只靠单一证据**：一个维度达标不等于整体达标
2. **历史记录不等于当前状态**：曾经的 partial 或污染，不代表现在仍有问题
3. **exception ≠ 无效**：带例外说明的对象，需看例外原因是否已解决
4. **补证路径多元**：可用具体作品页、平台官方分类页、培训页等多种方式补证

---

## 二、五维检查框架

检查一个 profile 是否"稳定保留"，必须同时满足以下**全部五个维度**。

### 维度 1：结构完整性

**要求**：profile 目录下至少包含三件套

| 必需文件 | 说明 |
|---|---|
| `profile.yaml` | core profile |
| `bucket-{slug}.yaml` | bucket overlay（番茄定位） |
| `profile-{platform}.yaml` | platform overlay（如番茄、起点等） |

**判定规则**：
- 三件套齐全 → 通过
- 仅有 core profile → 不通过
- 两件套 → 不通过

---

### 维度 2：运行投影可读性

**要求**：profile 能在运行时被正确加载和投影，产出最小摘要。

**检查方式**：
1. 确认 `profile contract` 测试能正常读取该 profile
2. 确认摘要输出包含以下三个最小字段：
   - `bucket`：平台主 bucket 名
   - `strong_tags`：强标签列表
   - `tone_guardrails`：调性约束列表

**判定规则**：
- 测试能断言三个字段 → 通过
- 仅有文档描述，但无测试读取 → 不通过

---

### 维度 3：测试兜底覆盖

**要求**：存在 profile contract 测试用例，对该 profile 进行最小投影验证。

**检查方式**：
- 查找 `tests/test_profile_contract.py` 中是否有 `test_{slug}_profile_exposes_minimum_positioning`
- 确认测试内部对 bucket / strong_tags / tone_guardrails 有明确断言

**判定规则**：
- 有测试且断言明确 → 通过
- 有测试但断言模糊（如仅检查不抛异常） → 降级通过
- 无测试 → 不通过

---

### 维度 4：跨平台证据状态

**要求**：`batch-evidence-sidecar.json` 中该 profile 的 evidence 状态为 complete。

**检查方式**：
1. 查找 `docs/10-进行中/batch-evidence-sidecar.json`
2. 找到对应 profile 条目
3. 确认三项字段：
   - `status = "complete"`
   - `ontology_ready = true`
   - `exception = false`

**判定规则**：
- 三项全部满足 → 通过
- `status = complete` 但 `exception = true` → 需单独评估例外原因
- `status = partial` → 不通过
- `ontology_ready = false` → 不通过

**补证路径说明**：
补齐 cross-platform evidence 不一定只能靠具体作品页，还包括：
- 平台官方分类页（如起点"游戏主播"子分类）
- 平台培训/帮助页（如番茄作家课堂直播培训页）
- 以上均属于有效平台级证据

---

### 维度 5：题材本体可上升性

**要求**：该 profile 在 `genre-ontology-field-decisions-v1.5.md` 中有明确记录，且具备跨平台证据支撑。

**检查方式**：
1. 查找 `docs/00-当前有效/genre-ontology-field-decisions-v1.5.md`
2. 找到对应 profile 条目
3. 确认是否标注"可上升为题材本体"

**判定规则**：
- 有记录且标注"可上升" → 通过
- 有记录但标注"暂不直接上升"（如 package_cues 尚缺）→ 降级通过
- 无记录 → 不通过

---

## 三、综合判定矩阵

| 结构 | 运行投影 | 测试兜底 | Evidence | Ontology | 综合结论 |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | **稳定保留** |
| ✅ | ✅ | ✅ | ✅ | 降级 | **稳定保留（建议补足 ontology）** |
| ✅ | ✅ | 降级 | ✅ | ✅ | **稳定保留（建议补测试）** |
| ❌ | - | - | - | - | **不达标（缺结构件）** |
| - | ❌ | - | - | - | **不达标（无法运行）** |
| - | - | ❌ | - | - | **不达标（无测试兜底）** |
| - | - | - | ❌ | - | **不达标（证据不全）** |
| - | - | - | - | ❌ | **不达标（无本体支撑）** |

---

## 四、污染/补证类型说明

不同历史问题的 profile 达到"稳定保留"的路径不同。

### 类型 A：正常补证完成

**特征**：原本 evidence 不足，但后续补齐。

**代表样本**：`gaowu`

**补证路径**：
- 补入晋江 A 级实体页
- `status` 从 partial → complete
- `ontology_ready` 升为 true

**达到稳定保留的标志**：
- sidecar 五项全绿
- ontology 有"可上升"标注
- 测试可正常读取

---

### 类型 B：污染修复完成

**特征**：曾因 URL 存疑或证据污染被降级，后续通过替换 URL 补正。

**代表样本**：`cthulhu`

**污染原因**：
- 原晋江 novelid=10267899 为"穿到虫族文"，被错误塞入不相关题材

**修复方式**：
- 替换为正确的晋江 URL（novelid=9455935）
- 补入番茄、起点 A 级实体页

**达到稳定保留的标志**：
- sidecar 五项全绿
- exception = false
- ontology 有"可上升"标注

---

### 类型 C：官方分类/培训页补证完成

**特征**：曾被彻底删除（无可用 URL），后续通过平台官方分类页或培训页重建 evidence。

**代表样本**：`livestream`

**污染原因**：
- 原所有 URL 为批量虚构，被彻底删除

**修复方式**：
- 番茄：平台官方"直播培训"页
- 起点：官方"游戏主播"子分类页
- 晋江：具体作品页

**达到稳定保留的标志**：
- sidecar 五项全绿
- 补证路径为平台级官方页面（不等同于具体作品页）
- ontology 有"可上升"标注

---

## 五、例外对象处理规则

以下情况为例外对象，判定时需单独审查。

### 规则 1：exception = true 的对象

**不等于"无效"**，而是说明该对象有合理的特殊原因不适用默认标准。

**典型代表**：`zhihu-short`

- `status = partial`
- `exception = true`
- `exception_type = "zhihu-primary-source"`

**处理方式**：
- 不适用三平台默认对齐要求
- 改为以知乎原生证据为主要判断依据
- 单独追踪其 evidence 完成路径

---

### 规则 2：ontology_ready = false 的对象

**可能原因**：
- 跨平台证据已齐，但 package_cues 或首屏/前三章节奏尚未定义
- 题材本体定位仍有争议

**处理方式**：
- 不阻断 stable 保留
- 但需记录"待补足 ontology"项
- 后续以单独 ticket 追踪

---

## 六、使用方式

### 场景 1：新 profile 准入审查

新 profile 进入 `shared/profiles/` 前，需通过本清单全部五维检查。

### 场景 2：已有 profile 定期巡检

每隔一个治理周期，对现有 profiles 按本清单重新走一遍五维检查。

### 场景 3：partial profile 升级评估

当一个 profile 声称已补证完毕可升级时，需按本清单逐项举证。

### 场景 4：保护名单收缩决策

在考虑将某 profile 移出 `sync-governance.json` 保护名单前，需确认该 profile 在本清单下已达"稳定保留"状态。

---

## 七、相关文件索引

| 文件 | 用途 |
|---|---|
| `shared/profiles/{slug}/profile.yaml` | core profile |
| `shared/profiles/{slug}/bucket-{slug}.yaml` | bucket overlay |
| `shared/profiles/{slug}/profile-{platform}.yaml` | platform overlay |
| `tests/test_profile_contract.py` | profile contract 测试 |
| `docs/10-进行中/batch-evidence-sidecar.json` | evidence 状态追踪 |
| `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md` | 跨平台证据包 |
| `docs/00-当前有效/genre-ontology-field-decisions-v1.5.md` | 题材本体决策记录 |
| `shared/templates/profile-bucket-registry-v1.json` | bucket registry |
| `shared/sync-governance.json` | 治理保护名单 |

---

## 八、版本记录

| 版本 | 日期 | 更新内容 |
|---|---|---|
| v1 | 2026-03-31 | 初始版本：通过 gaowu/cthulhu/livestream/realistic/workplace-romance 五个试点样本归纳 |
