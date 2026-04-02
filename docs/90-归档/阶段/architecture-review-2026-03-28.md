# Genm-codex 架构深度审查与改进方案

**日期**: 2026-03-28
**审查轮次**: 4 轮（静态分析 + 脚本深度 + 真实项目 + 隐蔽盲区）
**状态**: `active` — 待 GPT-5.4 审查后执行
**统计**: 52 个问题（14 HIGH / 23 MEDIUM / 15 LOW）/ 31 个方案（P0×8 / P1×19 / P2×4）

---

## 一、核心发现

### 1.1 上下文经济学：每 1 个创作 token 需要 8-10 个规则 token

典型 write→close 流程：~90K token 被规则读取消耗（其中 ~50K 是重复读取同一文件），仅 ~10K 用于创作。

重复最严重的文件：
| 文件 | 流程中读取次数 | 累计浪费 |
|------|--------------|---------|
| state.json | 3-5 次 | ~12K-20K |
| core-constraints.md | 3-4 次 | ~9K-12K |
| fanqie-writing-techniques.md | 2-3 次 | ~4K-6K |

### 1.2 规则膨胀率：83% 叙事，17% 可执行

三大框架 + fanqie 文档 ~188KB，可执行规则仅 ~33KB。框架文档更适合叫"教程"而非"规则手册"。

### 1.3 Skill 百科全书反模式

novel-write (406行) 中 43% 是参考材料。novel-review 48%。近一半内容在告诉 LLM"参考什么"而非"现在做什么"。

### 1.4 流派/桶系统 70% 是空的

- 54 个 profile 中 38 个没有 platform_positioning
- `summarize_for_state()` 硬编码 `bucket: ""`
- `resolve_platform_positioning()` 存在但从未被调用
- bucket overlay 文件数量为零
- fanqie-mvp-buckets.yaml 只定义 4 个桶
- 桶名无规范 slug 映射（宫斗宅斗 vs palace-intrigue vs gongdou_zhai）

### 1.5 反脸谱化框架：2013 行，5.6% 生产使用率

- 6 个 skill 完整接入，烟测证明能产出有用诊断
- 但 17/18 生产项目无人物立体度评分
- 条件触发模型导致大多数章节走"轻量放行"
- e2e-novel（主反馈样本）零引用
- 流派故障库在生产中触发次数：0

### 1.6 novel-scan：1120 行死代码

18 个项目的 market-adjustments.json 全部为空或空调整。scan→adjustment→write 管道从未对真实创作产生过影响。

### 1.7 learned_patterns 模板复制 + schema 分裂

- opening_strategy / multi_line_guardrails 在 7+ 项目中逐字复制
- v1.0 和 v3.0 两个不兼容 schema 并存
- v3.0（character_voices, vocabulary_preferences, ratios）真正有用
- v1.0（空数组或泛化描述）近乎无用

### 1.8 质量评审只在新项目上生效

最大项目（庶女谋略 35ch）零评审、空 patterns、24 章无 metadata。最小项目之一（搬回老小区 3ch）反而有最丰富的 v3.0 patterns。

### 1.9 工作流合规问题

- e2e-novel Ch2/Ch3 跳过审查，无任何标记
- 庶妹换我婚书 ch15-20 是 260-443 字摘要态伪装为正文
- 庶女谋略 protagonist_knows 仅 2 条（35 章后严重失同步）
- 伏笔逾期检测未运行
- 维护链零容错（一步失败全链停止）

### 1.10 其他结构性问题

- 4 个 skill 步骤编号重复（novel-genre/index/snapshot/retrieve）
- novel-fix/polish 读反脸谱化规则但不写回 state
- novel-sync/skill-usage/INDEX.md 等多处绝对路径
- 5 个模板子目录不在 sync-governance 保护列表
- shared/profiles/README.md 描述已不存在的 v3.0 系统
- thin-state.py 三文件顺序写入无事务保护
- state schema vs template 漂移（跨多轮未解决）
- 无内容质量测试（31 个测试全是结构性）
- hook-ledger / payoff-ledger 在 2 个项目中 100% 空
- 导出管道几乎不存在（全仓库仅 1 个 txt）
- 无平台反馈闭环
- 跨项目模式挖掘完全缺失

---

## 二、改进方案（31 个）

### P0（半天内可完成，零风险）

| # | 方案 | 操作 |
|---|------|------|
| 5 | 工作流合规检测器 | 新增 workflow_compliance.py |
| 8 | state.json 孤儿字段清理 | schema 移除 5 个字段 |
| G10 | novel-sync 绝对路径修复 | 1 行改相对路径 |
| N9 | 所有绝对路径修复 | ~5 文件各 1-2 行 |
| N1 | 重写 shared/profiles/README.md | 匹配当前 53-genre 分层 |
| N3 | sync-governance 保护目录补全 | +5 条路径 |
| N5 | 步骤编号重复修复 | 4 个 SKILL.md 各 1 行 |
| 18 | bucket 分配系统打通 | wire up resolve_platform_positioning |

### P1（1-2 周）

| # | 方案 | 核心操作 |
|---|------|---------|
| 0 | 框架速查卡（QUICK.md） | token 节省 83% |
| 1 | 规则预加载（rule-cache.json） | 4 文件代替 60 个 |
| 2 | 规则注册表（registry.yaml） | bundle + trigger |
| 3 | 声明式质量门（gates.yaml） | 消除 ~12 处重复 |
| 4 | 声明式事务状态机（fsm.yaml） | 阻止非法跳步 |
| 6 | state.json 分层 | canon + state + chapter-ledger |
| 7 | 合同缺口修复 | G2-G10 + 代码重复 |
| 11 | e2e-novel 自动化 smoke | 新增 e2e_smoke.sh |
| 14 | thin-state.py 原子写入 | write-tmp → rename |
| 17 | state schema/template 一致性 | 统一字段定义 |
| 19 | 跨流派规则继承 | _base/profile.yaml |
| 20 | 流派故障库扩面 | 8→20+ 流派 |
| 21 | 维护链容错改造 | check=False + continue |
| 22 | 伏笔逾期检测 | 超出 expected_range 标记 |
| 25 | 反脸谱化默认激活 | review 时默认打人物立体度 |
| 26 | novel-scan 降级为实验 | 从默认工作流移除引用 |
| 27 | learned_patterns 修复 | 统一 v3.0 + 修复模板 |

### P2（可选）

| # | 方案 | 说明 |
|---|------|------|
| 9 | Lazy Skill 试点 | novel-fix 25 行版验证 |
| 10 | Skill 精简合并 31→25 | analyze+query / retrieve+setting 等 |
| 23 | learned_patterns 回填 | 对空 patterns 项目运行 |
| 28 | 跨项目模式库 | shared/patterns/ 汇编通用模式 |

### 作废

| # | 原因 |
|---|------|
| 24 | "83% 停在第 3 章"是误读——测试样本，非用户流失 |

---

## 三、质量保障

token 降低 ≠ 质量降低。当前 100K 中 ~90K 规则读取、~10K 创作判断；改进后 ~35K 规则、~65K 创作。速查卡保留 100% 可执行规则。释放的 55K token 给推理，一致性判断反而需要更多推理空间。

---

## 四、执行路径

Phase 0（半天）：方案 5/8 + G10/N9 + N1/N3/N5 + 标记词校准 + 方案 18

Phase 1（1 周）：方案 0/1/2/7 + 方案 25/26/27

Phase 2（1-2 周）：方案 3/4/6/11/14/17 + 方案 19/20/21/22

Phase 3（可选）：方案 9/10/23/28

---

## 五、预期收益

| 指标 | 当前 | Phase 1 后 | Phase 2 后 |
|------|------|-----------|-----------|
| chapter close token 消耗 | ~100K | ~35-45K | ~30-40K |
| 创作可用上下文空间 | ~15-20K | ~55-65K | ~60-70K |
| SKILL.md 平均长度 | ~375 行 | ~200 行 | ~150 行 |
| 质量规则重复维护点 | ~12 处 | ~12 处 | 1 处 |
| 反脸谱化生产使用率 | 5.6% | ~80% | ~95% |
| bucket 空分配率 | 70% | 30% | 10% |

---

## 六、审查指引

### 审查焦点

1. 方案 0（速查卡）：压缩后 LLM 能否准确执行？
2. 方案 18（bucket 打通）：影响整个规则加载链路
3. 方案 25（反脸谱化激活）：默认激活是否引入噪声？
4. 方案 19（跨流派继承）：_base profile + overlay 是否最优？
5. 整体：四层分离架构方向是否正确？

### 参考文件

README.md / docs/00-当前有效/start-here.md / default-workflows.md / skill-usage.md / v1.3-roadmap.md / e2e-novel/.mighty/state.json / projects/成婚前三日/ / projects/被推去顶罪/ / shared/references/shared/consumer-read-manifest.md / scripts/profile_contract.py / docs/anti-flattening-framework/README.md
