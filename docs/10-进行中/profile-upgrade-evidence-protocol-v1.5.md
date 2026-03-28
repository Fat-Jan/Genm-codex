# `v1.5` Profile 全量升级证据协议（超高强度版）

## 目的

这份协议服务于后续“54 个 profile 全量补齐升级强化”任务。

它解决的不是“怎么快速搜到材料”，而是：

1. 哪些来源可以作为 profile 升级的一手证据。
2. 哪些来源必须降权或禁用，避免污染 profile。
3. 每次写回 profile 前，必须记录什么证据和验证结果。

如果没有经过这份协议，后续任何“全量升级”都不应直接写回 `shared/profiles/`。

---

## 一手证据白名单

### A. 平台官方页面（最高优先级）

允许作为核心证据的页面类型：

- 官方分类页
- 官方频道页
- 官方榜单页
- 官方作品详情页
- 官方标签 / 流派页
- 官方征文页
- 官方作者服务 / 编辑规则 / 平台说明页

当前优先平台：

- 起点
- 番茄
- 晋江
- 阅文体系官方页面

这些页面可用于提取：

- 题材标签与分类结构
- 包装层 cue（标题、文案、卖点组织）
- 简介常见模式
- 榜单导向的读者预期
- 平台显式鼓励的叙事模式与避雷点

### B. 平台直接关联的一手运营材料（次高优先级）

允许使用：

- 平台官方活动页
- 官方征稿说明
- 官方写作营 / 训练营说明
- 官方编辑公开规则页

这些材料适合补：

- 平台侧包装偏好
- 标题 / 标签 / 开篇驱动偏好
- 平台显式不鼓励的内容形态

### C. 站内高置信作品样本（受限可用）

允许使用，但只能作为“样本佐证”，不能单独成为 profile 真值来源：

- 同平台头部榜单作品页
- 同分类高热作品页
- 同 bucket 代表性作品页

这类证据只适合回答：

- 当前包装 cue 长什么样
- 标签组合在平台上的常见搭配是什么
- 简介与卖点的真实呈现方式如何

不能单独用来定义：

- profile 的本体规则
- 题材长期本质
- 跨平台通用结论

---

## 降权来源

以下来源不是完全不能看，但只能做辅助交叉参考，不能直接驱动 profile 写回：

- 作者经验贴
- 论坛讨论
- 平台外自媒体长文
- 社区整理的书单 / 榜单解读
- 没有原始链接的流派总结

如果它们和官方页面冲突，默认以官方页面为准。

---

## 禁用来源（黑名单）

以下来源默认禁止进入 profile 升级证据链：

- SEO 聚合站
- 小说镜像站
- 采集站 / 盗链站
- 不可追溯原始 URL 的搬运文
- AI 二次总结页
- “十大题材套路总结”这类无平台原始出处的内容农场

这些来源即便内容“看起来像对的”，也不能进入 profile 写回依据。

---

## 单个 Profile 的最小证据包

后续每升级一个 profile，至少要留以下证据：

1. **平台分类证据**
   - 至少 1 个官方分类/频道/标签页
2. **平台包装证据**
   - 至少 2 个同 bucket 代表性作品页
3. **平台规则证据**
   - 若可得，至少 1 个官方征文/运营/规则页
4. **冲突备注**
   - 如果起点 / 番茄 / 晋江 / 阅文之间出现明显差异，必须写冲突说明，不能直接抹平

没有满足最小证据包，就不能把 profile 标记为“已强化完成”。

---

## 写回字段优先级

在高强度升级中，不允许一次性无边界重写整个 profile。优先只写：

### 第一层：最稳字段

- `platform_positioning.primary_bucket`
- `strong_tags`
- `narrative_modes`
- `tone_guardrails`
- `package_cues`

### 第二层：中风险字段

- `reader_expectations`
- `taboos`
- `constraints`

### 第三层：高风险字段

- `template`
- `pacing`
- `cool_points`
- `strand_weights`

第三层字段只有在证据足够稳定、且跨平台偏差已被显式处理时才允许升级。

---

## 54 个 Profile 的分批升级顺序

后续不按“字母顺序”推进，而按证据成熟度分批：

### Batch 1：已有 positioning / bucket overlay / registry 映射的高成熟对象

- `palace-intrigue`
- `urban-brainhole`
- `urban-daily`
- `sweet-youth`
- `ceo-romance`
- `workplace-romance`
- `historical-brainhole`
- `xuanhuan`
- `xiuxian`
- `realistic`
- `system`

### Batch 2：已有部分 positioning 或 bucket 对应关系，但平台差异尚不稳定的对象

- `romance`
- `historical`
- `apocalypse`
- `melodrama`
- `sweet-romance`
- `urban-superpower`

### Batch 3：长尾题材与组合题材

其余 profile 统一放到后续批次处理，包括：

- 创意 / 脑洞长尾题材
- crossover
- 暗黑 / 克苏鲁 / 规则恐怖等特殊题材
- 知乎短篇等非主流平台型题材

原因不是它们不重要，而是这些 profile 更容易在证据解释上分裂，需要等前两批把协议跑顺后再进入。

---

## 统一验证门

每一批 profile 写回后，至少要过：

- `tests/test_profile_contract.py`
- `tests/test_content_positioning.py`
- `bash scripts/validate-migration.sh`

如果该批改动触达 consumer 假设，还要补对应 consumer 测试。

---

## 写回记录要求

后续每次真正升级 profile 时，都必须留下：

- 变更的 profile 列表
- 每个 profile 的来源 URL 清单
- 提取到的字段摘要
- 平台差异与冲突备注
- 本轮验证结果

没有这份记录，就不能宣称这一批升级“可信完成”。

---

## 非目标

这份协议当前不直接做：

- 配置新的 daemon / runtime
- 直接全量改完 54 个 profile
- 允许二手站点成为主证据
- 用单一平台经验覆盖全部平台

它只负责把后续高强度升级的证据标准和批处理规则写死。
