# Batch 1 Profile Upgrade Evidence Log (`v1.5`)

## 目的

记录 Batch 1 首轮升级中实际采用的一手来源入口、当前已修复的 profile，以及后续仍待补的对象。

这份记录当前只覆盖首轮最小修复批次，不假装代表 Batch 1 已全部完成。

---

## 已完成的首轮最小修复

### 1. `ceo-romance`

- 变更：补齐 `platform_positioning.fanqie.narrative_modes`
- 当前值：`["双线并进"]`
- 备注：本次还顺手修复了文件内已有 YAML 结构错误，使其重新可被 contract 测试链消费

### 2. `sweet-youth`

- 变更：补齐 `platform_positioning.fanqie`
- 当前补齐字段：
  - `primary_bucket`
  - `strong_tags`
  - `narrative_modes`
  - `tone_guardrails`
  - `package_cues`

---

## 当前一手来源入口（首轮）

### 番茄

- `https://fanqienovel.com/page/7509329103988739097`
  - `青春甜宠`
  - 作品页样本
- `https://fanqienovel.com/page/7512007315621432382`
  - `青春甜宠` + `校园甜宠`
  - 作品页样本
- `https://fanqienovel.com/page/7462572101195549721`
  - `青春甜宠` + `天作之合` + `学霸` + `一见钟情`
  - 作品页样本

### 起点

- `https://m.qidian.com/book/1044474526/`
  - `浪漫青春` / `青春校园`
  - 作品页样本
- `https://m.qidian.com/bookrecommend/e88a823d7f8d634f/`
  - `轻小说` / `恋爱日常`
  - 作品页样本

### 晋江

- `https://www.jjwxc.net/onebook.php?novelid=9768186`
  - 校园题材作品页
- `http://www.jjwxc.net/onebook.php?novelid=9593621`
  - 校园爱情作品页
- `http://static.jjwxc.net/onebook.php?novelid=10612020`
  - 校园暗恋作品页

这些入口当前只作为首轮包装与标签佐证，不单独定义 profile 本体。

### 番茄（第二轮补充）

- `https://fanqienovel.com/page/7525800272312945689`
  - `都市脑洞` + `都市异能` + `发家致富` + `重生`
  - 作品页样本
- `https://fanqienovel.com/page/7493362220613501464`
  - `职场婚恋` + `现代言情` + `先婚后爱`
  - 作品页样本
- `https://fanqienovel.com/page/7530130425956535321`
  - `职场婚恋` + `天作之合`
  - 作品页样本
- `https://fanqienovel.com/page/7470788135014648857`
  - `都市日常` + `单女主` + `1v1`
  - 作品页样本
- `https://fanqienovel.com/page/7516125781441907774`
  - `职场婚恋` + `女强` + `职场`
  - 作品页样本

---

## 当前结论

1. Batch 1 的“高成熟对象”里，仍然存在实际未补齐 contract 字段的 profile。
2. 因此 Batch 1 不能按口头假设一口气推进，必须走：
   - 先测出缺口
   - 再做最小修复
   - 再补证据
3. 当前首轮最小修复批次已经证明：
   - 测试基线有效
   - profile 资产确实仍有可修复缺口
   - 一手来源入口可获得
4. 第二轮补充来源说明：
   - `urban-brainhole` / `workplace-romance` / `urban-daily` 已拿到更贴近番茄 bucket 标签的一手作品页入口
   - 当前 bucket overlay 中的 `narrative_modes` 与 `tone_guardrails` 比 core profile 更细，可作为后续回写候选
5. 当前最小验证结论：
   - 对 `urban-brainhole` / `workplace-romance` / `urban-daily` 而言，现有 bucket overlay 已可稳定投影更强的 positioning
   - 因此这一小批当前不需要强行回写 core profile，维持 overlay-first 更符合最小变更原则

6. Batch 2 首轮最小缺口结论：
   - `melodrama` 与 `sweet-romance` 都已声明 `platform_positioning`，但此前 `narrative_modes` 为空
   - 这类对象不需要先做大范围升级，只需补齐最小可消费字段即可进入下一轮交叉平台校正

---

## Batch 2 首轮最小修复

### 1. `melodrama`

- 变更：补齐 `platform_positioning.fanqie.narrative_modes`
- 当前值：`["误会追妻双线"]`

### 2. `sweet-romance`

- 变更：补齐 `platform_positioning.fanqie.narrative_modes`
- 当前值：`["高甜日常推进"]`

---

## Batch 2 第二轮最小验证

### `urban-superpower`

- 结论：当前不需要强行回写 core profile
- 原因：现有 `bucket-urban-superpower.yaml` 已经可以稳定暴露：
  - `primary_bucket = 都市脑洞`
  - `strong_tags` 含 `异能`
  - `narrative_modes` 含 `多主题副本`
  - `tone_guardrails` 含 `异能展示要伴随现实后果`
- 跨平台参考入口已补：
  - 番茄：`都市异能 / 都市脑洞 / 灵气复苏` 相关作品页与关键词页
  - 起点：`都市异能` 分类页与作品页
  - 晋江：当前只拿到弱相关幻想/异能入口，暂不作为强写回依据

---

## 后续待补对象

Batch 1 后续仍待继续核实/强化的包括：

- `palace-intrigue`
- `urban-brainhole`
- `urban-daily`
- `workplace-romance`
- `historical-brainhole`
- `xuanhuan`
- `xiuxian`
- `realistic`
- `system`

后续每推进一个 profile，都应继续按证据协议追加来源记录与验证结果。
