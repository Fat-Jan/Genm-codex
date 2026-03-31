# Historical Brainhole County Yamen Sample Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `projects/我在县衙当杂吏，靠翻旧案升了堂` 中落一个可直接用于番茄 `历史脑洞` smoke 的最小真实样本，覆盖 `init -> outline -> write(1-3)`。

**Architecture:** 先用 `novel-init` 约定创建项目骨架和最小 truth files，再以 `历史脑洞` overlay 锁总纲与前三章章纲，最后写出前三章正文并更新 `state`。样本只验证黄金三章链路，不扩到第四章以后。

**Tech Stack:** Markdown, JSON, 项目内 novel workflow 约定, `scripts/setting_gate.py`

---

### Task 1: Initialize Project Skeleton

**Files:**
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/state.json`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/learned-patterns.json`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/market-adjustments.json`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/setting-gate.json`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/设定集/角色/主角.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/设定集/力量体系.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/设定集/世界观/时代与制度口径.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/设定集/官制/官职真值表.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/设定集/官制/权力层级图.md`

- [ ] Step 1: 写最小初始化文件
- [ ] Step 2: 校对 `historical-brainhole` bucket 与 state 结构一致
- [ ] Step 3: 尝试运行 `python3 scripts/setting_gate.py <project_root> --stage init`

### Task 2: Lock Outline

**Files:**
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/大纲/总纲.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/大纲/章纲/第001章.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/大纲/章纲/第002章.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/大纲/章纲/第003章.md`

- [ ] Step 1: 锁开篇 promise、机制边界、制度压力
- [ ] Step 2: 锁前三章兑现链与残账
- [ ] Step 3: 尝试运行 `python3 scripts/setting_gate.py <project_root> --stage outline`

### Task 3: Write Chapters 1-3

**Files:**
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/chapters/第001章.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/chapters/第002章.md`
- Create: `projects/我在县衙当杂吏，靠翻旧案升了堂/chapters/第003章.md`
- Modify: `projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/state.json`

- [ ] Step 1: 写第一章，先砸身份困局和制度压力
- [ ] Step 2: 写第二章，让机制第一次现实见效
- [ ] Step 3: 写第三章，完成小闭环但不打穿主线
- [ ] Step 4: 回写 progress、chapter_meta、threads、knowledge_base

### Task 4: Verify and Close

**Files:**
- Modify: `task_plan.md`
- Modify: `progress.md`

- [ ] Step 1: 校验 JSON 与目录结构
- [ ] Step 2: 总结适合 `fanqie_p0_smoke.py` 的章节范围
- [ ] Step 3: 说明该样本为何能验证 `历史脑洞` bucket
