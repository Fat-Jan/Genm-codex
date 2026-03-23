# Genm-codex Phase 7A Scan Contract

## 目标

为未来的 `novel-scan` 建立一个**最小稳定契约**，让它在真正实现前就先明确：

- 可以依赖什么外部来源
- 结果可信度如何分层
- 无网络时如何退化
- 哪些结果只报告，哪些结果允许回写

## 当前定位

`novel-scan` 不属于普通本地 skill。

它更接近一个“外部趋势采集 + 本地分析 + 可选 profile 调整建议”的复合能力。

因此必须先约定契约，而不是直接写一个默认可用实现。

## 数据源分层

### Level A：官方或平台公开页面

示例：

- 官方排行榜
- 官方热榜
- 官方月票榜 / 金榜

特点：

- 可信度最高
- 但 HTML/结构可能常变

### Level B：稳定的中间提取层

示例：

- Jina Reader
- 已验证的外部内容抽取代理

特点：

- 适合把网页内容转成可分析文本
- 可信度次于原站

### Level C：搜索层 / 聚合层

示例：

- Exa
- GitHub/论坛讨论检索
- 社交媒体趋势线索

特点：

- 适合发现候选样本
- 不适合直接作为最终结论依据

### Level D：用户提供材料

示例：

- 用户粘贴榜单
- 用户提供章节文本
- 用户提供导出的热门作品样本

特点：

- 可用性最高
- 可信度取决于来源说明

## 最小结果结构

未来 `novel-scan` 无论通过哪条路径获得数据，输出都应该统一成一个本地结果文件，例如：

- `.mighty/market-data.json`

最小结构建议：

```json
{
  "version": "1.0",
  "scan_time": "<timestamp>",
  "mode": "report-only",
  "sources": [
    {
      "type": "official-ranking",
      "platform": "番茄",
      "url": "...",
      "trust_level": "A"
    }
  ],
  "findings": {
    "hot_genres": [],
    "hot_tags": [],
    "opening_patterns": [],
    "cool_point_patterns": [],
    "platform_notes": []
  },
  "confidence": {
    "overall": "medium",
    "reason": "A/B sources present, sample size limited"
  },
  "apply_recommendations": []
}
```

## 模式边界

### 模式 1：report-only

默认模式。只做：

- 外部数据整理
- 趋势摘要
- 对 Profile 的建议

不直接修改任何项目状态或 shared 配置。

### 模式 2：project-annotate

只允许在项目内增加“市场观察结果”与低风险项目内建议，例如：

- `.mighty/market-data.json`
- `.mighty/market-adjustments.json`
- `.mighty/state.json -> market_adjustments` 轻量摘要 / 指针

约束：

- 只有当前运行拿到中高可信证据时，才允许写入 `market-adjustments`
- low confidence 或 skeleton 结果只保留 `market-data.json`
- 仍不直接改 shared profile

### 模式 3：apply-suggestion

只允许在显式确认下，把扫描结果转换为：

- 一份待应用建议
- 或一个局部 project-level override
- 或更强的 bucket / profile 级决策

不直接改 shared 源资产。

### 明确禁止

- 默认改写 `shared/profiles/`
- 没有可信来源分层时直接回写权重
- 低可信结果直接写入 `market-adjustments`
- 把搜索层线索当成确定结论

## 退化路径

### 无网络

退化为：

- 请求用户提供榜单/章节样本/文本材料
- 只做本地分析

### 有网络但无可用抓取层

退化为：

- 收集 URL 与来源清单
- 输出“待人工抓取/待用户提供内容”

### 有网络但抓取层不稳定

当前仓库已补一个 report-only 获取辅助脚本：

- `scripts/acquire_source_text.py`

它的定位不是保证“任意站点都能拿到正文”，而是保证“任意输入都能稳定返回结构化结果”：

- 先尝试 `fetch MCP`
- 当前如果没有显式配置外部 `fetch MCP` 命令，会先退到 `r.jina.ai` reader proxy
- 再退到直抓 HTML + 内建正文提取
- 最后退到搜索回退 provider；当前默认可用的是 `Bing RSS`
- 始终返回统一状态、来源类型、失败原因和尝试记录

因此后续 scan/report-only 流程如果要接抓取层，应该优先复用这类稳定结果结构，而不是把单一抓取工具当作唯一入口。

### 数据不足

明确返回：

- 结论不足
- 原因
- 还缺什么数据

## 可信度规则

### High

- 至少 2 个 A/B 级来源
- 样本量充足
- 各来源结论大体一致

### Medium

- 只有 1 个 A/B 级来源
- 或 A/B + C 级混合

### Low

- 主要依赖 C/D 级来源
- 或样本量太小

## 与现有 skill 的关系

- `novel-scan` 负责外部趋势输入
- `novel-genre` 负责 profile 显式管理
- `novel-analyze` 负责本地章节分析
- `novel-learn` 负责本地/用户提供内容学习

也就是说，未来 `novel-scan` 不应替代这些已有 skill，而应补它们拿不到的外部趋势信号。

## 当前结论

在真正实现 `novel-scan` 前，至少需要先满足：

1. 数据源分层清楚
2. 结果结构固定
3. 退化路径明确
4. 回写边界明确

做到这四点，才值得进入实现阶段。

补充：

- 如果只是先把不稳定抓取层包成可消费结果，当前可直接复用：
  - `python3 scripts/acquire_source_text.py <url> --pretty`
- 但它仍然是 report-only helper，不代表 `novel-scan` 已进入默认工作流。
