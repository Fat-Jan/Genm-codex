# Fanqie 内容数据层

## 目的

这份文档回答：

- 当前项目里，什么才算“内容数据层”
- 这些数据怎么分层
- 它们最终应该怎么喂给：
  - 书名自动生成
  - 大纲推荐生成
  - 角色名字风格
  - 包装 / 写作 / 预检 / 扫描

这份文档不是市场报告，也不是写作技巧合集。  
它的作用是把现有分散的 Fanqie 信号收成一个**统一可消费的数据层**。

---

## 一、内容数据层是什么

这里的“内容数据层”不是单纯指榜单数据。

它应该至少包含 4 层：

### 1. 热度层

回答：

- 平台现在在推什么
- 哪些分类桶有明显曝光

来源：

- 榜单
- 分类榜
- 新书榜

### 2. 收益层

回答：

- 哪些内容桶更接近收益
- 哪些方向更像长期扶持方向

来源：

- 征文
- 保障计划
- 激励计划
- 互补付费信号

### 3. 写法层

回答：

- 这个桶通常怎样开篇
- 标题和简介该怎么写
- 前几章该怎么兑现

来源：

- 作者专区教程中心
- 写作技巧图文

### 4. 设定一致性层

回答：

- 这个桶里哪些身份关系必须先闭合
- 嫡庶、继室、齿序、尊卑这些词能不能直接写进标题
- 项目当前有没有“标题好看但设定不成立”的风险

来源：

- `shared/templates/genres/宫斗宅斗.md`
- `shared/profiles/palace-intrigue/profile.yaml`
- `shared/references/writing/ancient-household-kinship-guide.md`
- 项目自己的总纲 / 角色卡 / state

### 5. 样本层

回答：

- 当前项目自己已经跑通了哪些桶
- 哪些桶只是候选
- 哪些桶还只是实验线

来源：

- 本地 smoke / e2e 项目
- review / precheck / submission assessment

---

## 二、当前项目里已有的内容数据层工件

### 热度 / 收益层

- [fanqie-paid-signal-matrix.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-paid-signal-matrix.md)
- [fanqie-content-buckets.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-content-buckets.md)
- [fanqie-bucket-constraints.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-bucket-constraints.md)

### 写法层

- [fanqie-writing-techniques.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-writing-techniques.md)
- [fanqie-writer-zone-lessons.md](/Users/arm/Desktop/vscode/Genm-codex/docs/research/fanqie/fanqie-writer-zone-lessons.md)
- [fanqie-rule-priority-matrix.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-rule-priority-matrix.md)
- [fanqie-resistance-and-cost-rules.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-resistance-and-cost-rules.md)

### 样本层

- [fanqie-mvp-bucket-templates.md](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-mvp-bucket-templates.md)
- [fanqie-evil-gongdou-production-template.md](/Users/arm/Desktop/vscode/Genm-codex/docs/research/fanqie/fanqie-evil-gongdou-production-template.md)
- [fanqie-evil-gongdou-submission-assessment.md](/Users/arm/Desktop/vscode/Genm-codex/docs/research/fanqie/fanqie-evil-gongdou-submission-assessment.md)
- [fanqie-evil-qinggan-production-candidate.md](/Users/arm/Desktop/vscode/Genm-codex/docs/research/fanqie/fanqie-evil-qinggan-production-candidate.md)
- [fanqie-evil-tianchong-experiment-status.md](/Users/arm/Desktop/vscode/Genm-codex/docs/research/fanqie/fanqie-evil-tianchong-experiment-status.md)

### 机器可消费层

- [fanqie-mvp-buckets.yaml](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-mvp-buckets.yaml)
- [fanqie-mvp-tagpacks.yaml](/Users/arm/Desktop/vscode/Genm-codex/docs/fanqie-mvp-tagpacks.yaml)
- `.mighty/market-data.json`
- `.mighty/market-adjustments.json`
- `.mighty/state.json -> market_adjustments` 轻量摘要 / 指针

---

## 三、内容数据层应该输出什么字段

### A. 对 `novel-package`

最关键的不是“这个书名好不好听”，而是：

- `recommended_content_bucket`
- `recommended_tagpack`
- `title_patterns`
- `title_cues`
- `synopsis_patterns`
- `click_through_risk`
- `overpromise_risk`

#### `title_patterns`

应该回答：

- 这个桶当前最适合哪种标题结构
- 关系词应该放在哪
- 爆点词要不要前置
- 该不该带“太子 / 婚书 / 离婚 / 闪婚 / 京圈”这类点击词

### B. 对 `novel-outline`

最关键的不是“章节会不会接”，而是：

- `opening_patterns`
- `golden_three_expectation`
- `payoff_timing`
- `handoff_patterns`
- `map_shift_risk`
- `kinship_schema`
- `relation_consistency_checks`
- `resistance_patterns`
- `cost_patterns`
- `partial_payoff_patterns`
- `trust_curve_patterns`

#### `opening_patterns`

应该回答：

- 第一屏要给什么
- 第 1 章里先抛压制、异常还是关系绑定
- 第 3 章前必须兑现什么
- 第 2 章必须在哪卡一下

### C. 对 `character naming`

最关键的不是“名字美不美”，而是：

- `naming_style`
- `surname_pool`
- `given_name_style`
- `forbidden_name_patterns`
- `male_lead_style`
- `female_lead_style`
- `supporting_role_style`
- `external_name_collision_risk`
- `title_similarity_risk`
- `search_scope`

#### `naming_style`

应该回答：

- 这个桶里角色名该偏：
  - 日常现实
  - 京圈精致
  - 宫廷权谋
  - 玄幻识别度
- 名字是不是要更短、更直白、更可记

---

## 四、三个最需要优先打磨的消费点

### 1. 书名自动生成

当前问题：

- 规则已经有了，但还偏“会生成”
- 还不够“更像番茄点击模型”

打磨方向：

- 增加 `title_patterns`
- 区分：
  - 长篇稳收型书名
  - 起量型书名
  - 女频付费型书名
- 对每个桶给：
  - 主标题格式
  - 次级格式
  - 不推荐格式

### 2. 大纲推荐生成

当前问题：

- 现在能按 bucket 写大纲
- 但还不够显式地吃“平台前几章兑现模式”

打磨方向：

- 增加：
  - `opening_patterns`
  - `golden_three_expectation`
  - `handoff_patterns`
  - `resistance_patterns`
  - `cost_patterns`
  - `partial_payoff_patterns`
- 让大纲不是只会写：
  - goal / conflict / reveal / hook
- 还会明确：
  - 第 1 章为什么能点进去
  - 第 2 章为什么不掉速
  - 第 3 章为什么必须硬兑现
  - 第 3 章为什么不能赢得太满

### 3. 角色名字风格

当前问题：

- 现有命名指南过于平台泛化
- 还不够 Fanqie-first
- 也还没围绕当前最重要的桶来写
- 还缺一层投前检索，不足以拦住撞名 / 高相似度风险

打磨方向：

- 先收缩到当前优先桶：
  - `宫斗宅斗`
  - `现实情感`
  - `现言甜宠`
  - `传统玄幻`
- 每个桶给：
  - 女主命名风格
  - 男主命名风格
  - 配角命名风格
  - 禁忌
  - 投稿前的最小检索门

---

## 五、当前推荐的优先级

如果只从“现在最该打磨什么”排序：

1. **书名自动生成**
2. **大纲推荐生成**
3. **角色名字风格**
4. **关系谱系闭环**

原因：

- 书名直接影响点击
- 大纲直接影响前三章
- 命名影响辨识度和风格统一
- 宫斗宅斗这类桶如果关系谱系不闭合，会直接把包装、总纲、正文一起带偏

这三层都比继续补更多外围文档更值钱。

---

## 六、和现有规则的关系

这个内容数据层不是新的一套硬规则。

它应服从：

1. canon / state / outline
2. bucket
3. content data layer 的写法建议
4. tagpack

也就是说：

- 它是第二、第三层之间的桥
- 不该推翻 canon
- 不该推翻 bucket
- 但它应该让 `package / outline / naming` 变得更聪明

---

## 七、当前结论

现在项目里已经有不少 Fanqie 相关工件了，但它们仍然偏分散：

- 有市场信号
- 有内容桶
- 有写法规则
- 有样本线

而 `fanqie-content-data-layer.md` 的作用就是把它们统一成：

- **可以直接喂给技能的上游数据层**

如果后续继续增强，最优先的三个落地点应该是：

1. `novel-package`
2. `novel-outline`
3. `character-naming-guide`
