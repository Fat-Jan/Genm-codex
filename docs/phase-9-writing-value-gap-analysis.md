# Genm-codex 写作价值功能对比分析

## 目的

这份文档不再按“还剩多少命令没迁”来判断进度，而是按更贴近项目本质的标准判断：

- 哪些旧项目能力，真的直接帮助小说写作生成与质量提升
- 这些能力在 `Genm-codex` 里是否已经迁移
- 如果还没完全迁移，缺的到底是“命令”，还是“整合与收口”

---

## 评估标准

本分析把“高价值写作功能”定义为：

1. 能直接提高正文生成质量
2. 能直接提高平台适配度和投稿可用性
3. 能直接降低 AI 痕迹、解释腔、节奏掉速等常见问题
4. 能直接提高续写稳定性、设定一致性和伏笔管理质量

以下能力不算高优先级写作能力：

- 单纯帮助/教程入口
- 配置和连接引导
- 纯日志、纯统计、纯历史归档
- 已被现有 skill 吸收的旧草案命令

---

## 旧项目里真正有写作价值的能力

### A. 核心创作闭环

- `novel-init`
- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-fix`
- `novel-polish`
- `novel-rewrite`
- `novel-batch`
- `novel-export`
- `novel-precheck`

### B. 上下文与一致性支撑层

- `novel-character`
- `novel-setting`
- `novel-foreshadowing`
- `novel-query`
- `novel-retrieve`
- `novel-index`
- `novel-snapshot`
- `novel-resume`
- `novel-workflow`
- `novel-status`

### C. 平台与题材适配层

- `novel-genre`
- `novel-scan`
- 平台专用写作命令：
  - `platform/novel-write-fanqie.md`
  - `platform/novel-write-qidian.md`
  - `platform/novel-write-qimao.md`
  - `platform/novel-write-jinjiang.md`
- 平台简介适配：
  - `platform/novel-synopsis-platform-adapt.md`
- 角色命名参考：
  - `build/references/writing/character-naming-guide.md`

### D. 写作质量学习层

- `novel-learn`
- 反 AI 腔、平台风格、核心约束等共享参考资产

---

## 已迁移覆盖情况

### 已经迁移且已验证可用

以下能力已经在 `Genm-codex` 中存在，并且在前几阶段里拿到过 smoke 或 E2E 证据：

- `novel-init`
- `novel-outline`
- `novel-write`
- `novel-review`
- `novel-fix`
- `novel-polish`
- `novel-rewrite`
- `novel-batch`
- `novel-export`
- `novel-precheck`
- `novel-character`
- `novel-setting`
- `novel-foreshadowing`
- `novel-query`
- `novel-retrieve`
- `novel-index`
- `novel-snapshot`
- `novel-resume`
- `novel-workflow`
- `novel-status`
- `novel-genre`
- `novel-learn`

结论：

**从“正文生成与质量控制”的主链看，核心能力已经基本迁完。**

---

## 部分迁移或已被吸收的能力

### 1. 平台专用写作命令

旧项目有独立的：

- `novel-write-fanqie`
- `novel-write-qidian`
- `novel-write-qimao`
- `novel-write-jinjiang`

但从当前 `Genm-codex` 的结构看，这部分已经被以下组合吸收：

- `novel-genre`
- `novel-write`
- `novel-precheck`
- shared profiles / platform references

所以这里的缺口不是“没有平台适配”，而是：

- 还没有把“平台差异”做成足够强的统一质量闭环
- 平台特定写法还没有被更强地注入到 `write -> review -> fix/polish/rewrite -> precheck`

### 2. `novel-scan`

这项已经迁移，但目前还处于实验深化阶段：

- `report-only`：有
- `project-annotate`：有
- `apply-suggestion`：还没完全做成稳定边界

所以它不是“没迁”，而是：

- **已经迁了第一阶段**
- **但还没走到高价值完成态**

### 3. `novel-content-generate-polish`

这份旧命令本身已经被定性为历史方案文档。

它承诺的能力，实际已被拆进：

- `novel-write`
- `novel-polish`
- `novel-fix`
- `novel-rewrite`

因此它不构成单独迁移缺口。

### 4. `novel-outline-intelligent`

这份也更像历史草案。

它的有效部分已经主要被吸收到：

- `novel-outline`
- `novel-genre`
- `novel-scan`

它不是优先缺口。

---

## 真正还缺的高价值能力

从“提升小说写作生成效果”角度看，真正还值得优先补的缺口，不多，主要只有三类。

### 1. 包装生成层

这是我现在判断的**最大真实缺口**。

旧项目里明确有：

- 平台适配简介生成
- 角色命名指南

但 `Genm-codex` 目前还没有一个统一的、写作收益很高的“包装层”能力，去做：

- 书名方向建议
- 角色命名建议
- 简介/卖点文案生成
- 平台化包装调整
- 开篇钩子包装

这类能力虽然不是正文主体，但对：

- 选题表达
- 平台适配
- 投稿点击率
- 作品包装完整度

的回报很高。

### 2. 质量闭环整合

这不是缺一个命令，而是缺一轮整合。

现在这些命令都已经在了：

- `write`
- `review`
- `fix`
- `polish`
- `rewrite`
- `precheck`
- `learn`

但它们还没有彻底形成统一的“质量系统”。

当前仍缺：

- AI 味风险的统一口径
- 平台适配、追读力、节奏、爽点的一致指标
- `learn` 对写作链的真正反哺
- `review -> fix/polish/rewrite -> precheck` 的更稳定协同

这类工作不增加命令数量，但会直接提升正文质量。

### 3. `novel-scan` 的高价值完成态

`scan` 已经不是空白，但还没到真正高回报的终点。

现在仍缺：

- 更稳定的建议应用边界
- 更结构化的项目级市场建议
- 对标题、简介、开篇包装的更直接反馈

也就是说，`novel-scan` 现在的价值已经开始显现，但还没完全吃到。

---

## 低优先级或不值得单独迁的部分

以下旧项目内容不建议继续按“核心功能缺口”计算：

- `novel-help`
- `novel-tutorial`
- `novel-config`
- `novel-test`
- `novel-stats`
- `novel-inheritance`
- `novel-content-generate-polish`
- `novel-outline-intelligent`

原因分别是：

- 已经 docs-first 化
- 已经被更底层能力吸收
- 写作收益不够高
- 或本身只是历史文档/参考草案

---

## 对比结论

如果从“旧项目里真正有助于小说写作的能力”来算，而不是按命令数量来算：

### 已经迁完的大头

- 核心创作链：基本迁完
- 质量审查与修复链：基本迁完
- 上下文与一致性管理链：基本迁完
- 题材与平台基础适配：基本迁完

### 仍然值得优先投入的部分

1. 包装生成层
2. 质量闭环整合
3. `novel-scan` 深化到更高价值完成态

---

## 我现在的判断

如果只问：

**“旧项目里对小说写作最有用的功能，还差多少没迁？”**

答案不是“还差很多命令”，而是：

**命令层面已经差不多了，真正还差的是 1 个缺失能力层 + 2 个整合层。**

更具体说：

- **缺失能力层**：包装生成层
- **整合层 1**：质量闭环整合
- **整合层 2**：`novel-scan` 高价值完成态

---

## 建议的下一步

如果后续继续按“提高小说写作生成效果”优先级推进，建议顺序改成：

1. **先做包装生成层**
   - 书名
   - 简介
   - 命名
   - 开篇包装

2. **再做质量闭环整合**
   - `write/review/fix/polish/rewrite/precheck/learn`

3. **最后深化 `novel-scan`**
   - 让市场信息真正反哺包装与写作，而不是停留在报告

这条路线，比继续补低价值命令，更符合项目本质。
