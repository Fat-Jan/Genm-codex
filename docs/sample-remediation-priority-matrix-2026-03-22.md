# 存量项目 / 样本回收优先级矩阵（2026-03-22）

## 目的

把当前仓库里的真实项目与 smoke 样本分成三档：

1. **优先按新章纲模板重生**
2. **只需 review 提醒**
3. **应重写，不应继续修补**

判断依据不是“我更喜欢哪条线”，而是：

- 是否命中了新规则识别出的“推进过顺”问题
- 是否已经有足够样本长度值得继续投资源
- 是否仍是当前默认路线里的有效资产
- 是否存在更高优先级的设定 / 真值问题，导致修补已经不划算

## 后续注记

本矩阵形成于样本回收启动时。

其中：

- [smoke/e2e-dual-substitute-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-dual-substitute-evil)

已在同日完成：

- 章纲重生
- 第 `004-009` 章正文验证
- 第 `007-009` 章集中 review

当前应视为：

- **已完成验证样本闭环**

不再属于“待回收对象”。

---

## 分流原则

### A. 优先按新章纲模板重生

适用于：

- 样本仍有高价值
- 核心方向成立
- 但章纲里存在明显顺推、白拿、全赢过满的问题

优先动作：

- 先重生章纲
- 再决定正文是 fix 还是 rewrite

### B. 只需 review 提醒

适用于：

- 当前样本整体成立
- 新规则没有强命中结构性问题
- 暂时只需要在继续写之前提醒作者不要回滑

优先动作：

- 继续写前跑 review
- 不先动模板回收

### C. 应重写，不应继续修补

适用于：

- 当前资产过旧、过薄、或已被更新样本替代
- 存在更高层级真值问题
- 继续 patch 的收益低于直接重开 / 重写

优先动作：

- 停止局部修补
- 直接重开或整段统改

---

## 优先级矩阵

| 对象 | 当前定位 | 建议路线 | 优先级 | 原因 |
|------|----------|----------|--------|------|
| [projects/庶妹换我婚书那夜，太子先开了口](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口) 的章纲层 | 真实项目 / 已锁真值 / 章纲已开始重生 | **优先按新章纲模板重生** | S | 真实项目、当前主战场、且已被证明旧章纲顺推感明显 |
| [smoke/e2e-gongdou-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-gongdou-evil) | 待重验样本 / 6章 | **优先按新章纲模板重生** | S | 长篇女频核心样本，回归已命中“权力兑现偏快” |
| [smoke/e2e-dual-substitute-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-dual-substitute-evil) | 第四条候选实验线 / `golden three` | **优先按新章纲模板重生** | S | 新线价值高，回归已强命中“同盟太快 / 证据太顺 / 第3章赢太满” |
| [smoke/e2e-qinggan-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-qinggan-evil) | 第二条生产模板候选 / 3章 | **只需 review 提醒** | A | 回归显示“快但不白拿”，当前主要缺更长样本，不缺章纲重生 |
| [e2e-novel](/Users/arm/Desktop/vscode/Genm-codex/e2e-novel) | 传统玄幻主样本 / 5章 | **只需 review 提醒** | A | 回归未误伤，说明旧章纲至少在前3章没有明显顺推病 |
| [smoke/e2e-tianchong-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-tianchong-evil) | 第三条实验线 / 3章 | **只需 review 提醒** | B | 目前主要问题是长期承载未验证，不是已经明确命中的顺推病 |
| [smoke/e2e-gongdou](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-gongdou) | 旧版基础样本 / 1章 | **应重写，不应继续修补** | A | 旧标题与旧设定仍绑定错误关系词，且已被 `e2e-gongdou-evil` 替代 |
| [smoke/e2e-qinggan](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-qinggan) | 旧版基础样本 / 1章 | **应重写，不应继续修补** | B | 样本太薄，继续 patch 不如按新模板重开 |
| [smoke/e2e-tianchong](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-tianchong) | 旧版基础样本 / 1章 | **应重写，不应继续修补** | B | 样本太薄，且关系型线更依赖新模板分层，不值得修补旧稿 |

---

## 细化说明

### 1. `projects/庶妹换我婚书那夜，太子先开了口`

要分层看：

- `总纲 / 包装 / 真值表`
  - 已收口
- `章纲`
  - 应继续重生
- `正文 001-020`
  - 不建议再靠零碎 patch 继续补洞
  - 需要按章纲新口径分段统改

也就是说：

- **这个项目的章纲层 = 重生优先**
- **这个项目的正文层 = 分段重写优先**

### 2. `smoke/e2e-gongdou-evil`

这条线还值得投资源，因为：

- 它仍是长篇女频的核心样本
- 问题不是方向错，而是章纲和推进习惯太顺

最合理做法：

- 先按新模板重生第2-6章章纲
- 再决定正文是局部 fix 还是整段 rewrite

### 3. `smoke/e2e-dual-substitute-evil`

这条线现在最不该直接补第4-5章。

更合理的是：

- 先重生第2-3章章纲
- 再重写第2-3章正文
- 再继续第4-5章

因为它的病不在“后续没写”，而在“前3章赢得太顺”。

### 4. `smoke/e2e-qinggan-evil`

这条线目前更像：

- 不缺章纲
- 缺更长样本

所以：

- 先继续写
- 继续前跑 review

比先回头重生章纲更划算。

### 5. `e2e-novel`

玄幻主样本说明了一件重要事：

- 新规则不是无脑反快

所以这条线当前最合适的不是回收，而是作为“没被误伤”的对照样本继续保留。

### 6. 三个旧版基础样本

- [smoke/e2e-gongdou](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-gongdou)
- [smoke/e2e-qinggan](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-qinggan)
- [smoke/e2e-tianchong](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-tianchong)

这三条共同问题是：

- 样本太薄
- 已被更成熟的 evil 变体替代
- 继续 patch 的收益很低

结论：

- **要么保留为历史样本**
- **要么以后直接用新模板重开**

不建议继续修修补补。

---

## 推荐执行顺序

1. [projects/庶妹换我婚书那夜，太子先开了口](/Users/arm/Desktop/vscode/Genm-codex/projects/庶妹换我婚书那夜，太子先开了口)
   - 继续章纲重生
   - 再分段统改正文
2. [smoke/e2e-gongdou-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-gongdou-evil)
   - 重生第2-6章章纲
3. [smoke/e2e-dual-substitute-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-dual-substitute-evil)
   - 先重生第2-3章章纲，再重写正文
4. [smoke/e2e-qinggan-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-qinggan-evil)
   - 继续写前先 review 提醒
5. [smoke/e2e-tianchong-evil](/Users/arm/Desktop/vscode/Genm-codex/smoke/e2e-tianchong-evil)
   - 继续写前先 review 提醒

---

## 一句话结论

最值得按新章纲模板重生的，不是所有样本，而是：

- **高价值、已命中“顺推病”的样本**

最不值得继续 patch 的，是：

- **过旧、过薄、已被替代的基础样本。**
