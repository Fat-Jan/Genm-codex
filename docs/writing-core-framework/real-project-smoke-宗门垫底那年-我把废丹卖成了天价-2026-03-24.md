# Writing Core Smoke: 宗门垫底那年，我把废丹卖成了天价

> 当前结果为 `draft`，已完成一轮 `writing-core-framework` 的手工 `package + precheck + memory writeback` 样本。

## 适用范围

- 项目：`projects/宗门垫底那年，我把废丹卖成了天价`
- bucket：`玄幻脑洞`
- package 判断范围：`总纲 + 第001-003章`
- precheck 样本范围：`001-003`
- confidence：`medium`
- evidence_count：`8`

## 证据来源

- `projects/宗门垫底那年，我把废丹卖成了天价/.mighty/state.json`
- `projects/宗门垫底那年，我把废丹卖成了天价/.mighty/learned-patterns.json`
- `projects/宗门垫底那年，我把废丹卖成了天价/.mighty/market-adjustments.json`
- `projects/宗门垫底那年，我把废丹卖成了天价/大纲/总纲.md`
- `projects/宗门垫底那年，我把废丹卖成了天价/chapters/第001章.md`
- `projects/宗门垫底那年，我把废丹卖成了天价/chapters/第002章.md`
- `projects/宗门垫底那年，我把废丹卖成了天价/chapters/第003章.md`
- `docs/writing-core-framework/06-精品审核与投稿前判断.md`

## 手工 `novel-package` 样本

```md
packaging_judgment:
  current_title: keep
  opening_method_cue: 生存困局先落地，废丹重定价机制在第一章点亮，第二章先救急，第三章完成当众卖出天价的小闭环
  genre_difference_cue: 玄幻脑洞应优先让机制改现实账本，而不是先讲世界大设定
  premium_review_cue: 第4-5章要把“更大利益”和“更大反噬”一起抬上来，避免只剩连续赚钱
  overpromise_warning: 不要提前包装成“已经揭开丹院黑幕”或“主角立刻横压全宗”的卖点
  payoff_timing_reminder: 第一轮高价兑现已在第3章完成；下一轮应在第4-5章给出更大交易和更明确追责
  packaging_constraints:
    - 书名主方向可保留当前书名
    - 简介应前置“垫底将逐下山 + 废丹重定价 + 当众卖出天价”
    - 开篇包装提示应落在“卖对了人，废丹能换灵石、换人脉、也换命”
    - 首屏钩子可以落“今夜补不齐三十贡献点就滚下山”
```

## 手工 `novel-precheck` 样本

```md
投稿建议:
  ready-now
packaging-needs-update:
  yes
must_fix_items:
  - none
should_fix_items:
  - 第4章前不要滑回解释性机制说明，继续用具体交易或夺秤动作承接新风险
  - 秦执炉和许观线要尽快落成具体追责单元，避免只停在“被盯上”
strongest_positives:
  - 首屏生存困局清楚
  - 第1-3章兑现链完整
  - 机制卖点直接改现实账本，不是挂名脑洞
content_standard_summary:
  primary_failure_mode: none
  execution_risk: low
  packaging_alignment_note: 当前正文可承接“废丹卖成天价、靠错配残效翻身、被内门盯上”的包装，但不宜提前承诺大黑幕已揭开
```

## memory writeback

本轮已做最小压缩信号写回：

- `.mighty/learned-patterns.json`
  - `opening_strategy`
  - `multi_line_guardrails`
  - `content_standard_alerts`
- `.mighty/state.json`
  - `learned_patterns.available_sections`
  - `chapter_meta["003"].content_standard_flags`
  - `chapter_meta["003"].packaging_alignment_note`
  - `constraints_loaded.includes += docs/writing-core-framework/README.md`

## 结论

- 这条样本证明：`writing-core-framework` 不只停在文档层，已经能被压成 package 约束、precheck 判断和 memory 压缩信号。
- 当前这本书的黄金三章可以支撑“开篇可投”，但外层包装仍建议补齐，因此 `packaging-needs-update = yes`。

## 收口更新

- 已生成：
  - `projects/宗门垫底那年，我把废丹卖成了天价/包装/包装方案.md`
- 这意味着本条样本最初的 `packaging-needs-update = yes` 已转成实际包装产物，不再停在建议层。
