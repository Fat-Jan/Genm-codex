# Batch Cross-Platform Evidence Pack (`v1.5`)

## 目的

这份文档把当前已进入“跨平台交叉压”阶段的 profile 收成一份证据包骨架。

当前只做三件事：

1. 给每个目标 profile 记录番茄一手入口。
2. 给每个目标 profile 记录起点或晋江的一手入口。
3. 标明当前这些证据能支撑“平台特化”还是“题材本体”判断。

当前不在这份文档里直接改 profile 真值。

---

## 1. `palace-intrigue`

### 番茄入口

- `https://fanqienovel.com/page/7483754097208724505`
  - 《双玉谋·盛唐劫》
  - 关键词：穿越、权谋、盛唐、命运之网

### 晋江入口

- `http://static.jjwxc.net/onebook.php?novelid=9749457`
  - 《进宫后，咸鱼炮灰靠弹幕宫斗》
- `http://www.jjwxc.net/onebook.php?novelid=1949950`
  - 《明月宅斗纪事》
- `http://static.jjwxc.net/onebook.php?novelid=8374763`
  - 《二嫁高门》

### 当前判断

- `高门关系 / 婚配错位` 更像可以继续保留的题材本体线索
- `宫斗宅斗` 的表达方式在晋江和番茄上都成立，但具体包装 cue 仍应优先保留在平台特化层

### 当前可上升字段

- 可上升为题材本体：
  - `strong_tags` 中的 `高门关系`
  - `strong_tags` 中的 `婚配错位`
  - `tone_guardrails` 中“强压后必须换账”的高层冲突约束
- 暂不直接上升：
  - `package_cues`
  - 番茄式首屏推进节奏要求

---

## 2. `historical-brainhole`

### 番茄入口

- `https://fanqienovel.com/page/7575061959293275198`
  - 《顶级权谋：重生之同治皇帝》
  - 关键词：重生、权谋、同治皇帝、步步为营
- `https://fanqienovel.com/page/7482629278010444824`
  - 《穿越之我在大秦当女帝》
  - 关键词：历史系、穿越、大秦、女帝

### 起点入口

- 现阶段 Exa 额度受限，起点这一类后续补抓官方分类 / 作品页

### 晋江入口

- `https://www.jjwxc.net/onebook.php?novelid=8099748`
  - 《吉祥如意》
- `https://my.jjwxc.net/onebook.php?novelid=10266934`
  - 《斗秾华》

### 当前判断

- `穿越 / 权谋` 目前仍可视为较稳的题材本体线索
- “历史感不能散 / 创意设定必须自洽” 这类 guardrail 看起来也具有跨平台共识潜力
- 但具体 package cue 仍不应直接抬成本体

### 当前可上升字段

- 可上升为题材本体：
  - `strong_tags` 中的 `穿越`
  - `strong_tags` 中的 `权谋`
  - `tone_guardrails` 中“历史感不能散”
  - `tone_guardrails` 中“创意设定必须自洽`
- 暂不直接上升：
  - `package_cues`
  - 番茄偏好的“一句话讲清主设定”式包装要求

---

## 3. `realistic`

### 番茄入口

- `https://fanqienovel.com/page/7470788135014648857`
  - 《向和平星许愿，听你呼吸里的伤》
  - 关键词：都市、单女主、1v1、纯爱校园文、不狗血

### 起点入口

- 现阶段 Exa 额度受限，起点现实情感 / 婚恋 / 现实成长类入口待后续补抓

### 晋江入口

- `https://www.jjwxc.net/onebook.php?novelid=5623891`
  - 《情不忍释》

### 当前判断

- `现实困局 / 成长` 具有继续保留为题材本体字段的可能性
- `治愈不等于无后果` 这类 guardrail 有较强跨平台一致性潜力
- 但“首行点困局 / 300字内点主线”仍明显属于番茄包装约束

### 当前可上升字段

- 可上升为题材本体：
  - `strong_tags` 中的 `现实困局`
  - `strong_tags` 中的 `成长`
  - `tone_guardrails` 中“现实代价不能消失”
  - `tone_guardrails` 中“治愈不等于无后果”
- 暂不直接上升：
  - `package_cues`
  - 开篇 300 字内必须交代主线这类平台包装约束

---

## 当前共识

1. 这三类对象已经具备“番茄 + 晋江/起点”的最小证据包骨架。
2. 当前更适合上升为题材本体的，主要是：
   - 高层题材标签
   - 基本关系/冲突类型
   - 高层 tone guardrail
3. 当前不适合直接上升为题材本体的，主要是：
   - package cue
   - 首屏/前三章这类平台包装约束
4. 由于起点抓取受额度限制，当前三类对象的“跨平台骨架”已成立，但仍应在后续补齐更稳定的起点分类页/作品页后再做更激进写回。

---

## 当前阶段字段边界结论

在这三类对象上，当前最稳妥的做法是：

- 允许把高层题材标签与高层 tone guardrail 视为“可上升候选”
- 暂不把 `package_cues`、首屏要求、前三章兑现节奏这类内容上升为题材本体

也就是说，当前这轮跨平台交叉压更像是在给“哪些字段未来值得写回 core profile”做筛选，而不是立刻重写 profile。

---

## 首次本体写回候选顺序

基于当前证据密度与冲突程度，首次本体写回更适合按下面顺序推进：

1. `realistic`
   - 候选字段：`现实困局`、`成长`、`现实代价不能消失`、`治愈不等于无后果`
   - 原因：平台差异相对最小，题材边界清晰，番茄与晋江都支持“现实困局 + 成长 + 非悬浮治愈”这组高层判断
   - 当前状态：已通过定向测试验证，当前 core profile 已满足这组高层候选字段，不需要额外本体写回

2. `historical-brainhole`
   - 候选字段：`穿越`、`权谋`、`历史感不能散`、`创意设定必须自洽`
   - 原因：高层题材判断较稳，但仍待更稳定的起点侧分类证据补强
   - 当前状态：已通过定向测试验证，当前 core profile 已满足这组高层候选字段，不需要额外本体写回

3. `palace-intrigue`
   - 候选字段：`高门关系`、`婚配错位`、`强压后必须换账`
   - 原因：番茄与晋江都支持宫斗/宅斗/高门婚配线，但包装层与叙事推进节奏差异仍更明显，适合放在前两者之后
   - 当前状态：已通过定向测试验证，当前 core profile + bucket overlay 已能稳定暴露这组候选字段，不需要额外 core profile 写回

当前不建议作为首次本体写回候选的内容：

- `package_cues`
- 首屏/前三章兑现节奏
- 任何明显绑定番茄消费链的包装约束

---

## 已验证但当前无需额外本体写回的对象

### `system`

- 当前结论：`system / 逆袭 / 系统奖励不能替代成长 / 任务推进要和主线冲突绑定` 已可稳定暴露
- 当前状态：依赖 core profile + `bucket-system.yaml` 即可，不需要额外 core profile 写回

### `xuanhuan`

- 当前结论：`金手指 / 成长 / 升级必须有代价 / 爽点不能替代世界规则` 已可稳定暴露
- 当前状态：依赖 `profile-tomato.yaml` 即可满足番茄侧高层候选，不需要额外 core profile 写回

### `xiuxian`

- 当前结论：`宗门 / 成长 / 升级必须有代价 / 机缘不能白拿` 已可稳定暴露
- 当前状态：当前 core profile 已满足这组高层候选字段，不需要额外本体写回

### `romance`

- 当前结论：`高甜 / 情感拉扯 / 甜感不能空转 / 误会不能纯靠不沟通` 已可稳定暴露
- 当前状态：依赖 core profile + `bucket-romance.yaml` 即可，不需要额外 core profile 写回

### `historical`

- 当前结论：`权谋 / 家国 / 历史感不能散 / 权力线必须讲层级` 已可稳定暴露
- 当前状态：依赖 core profile + `bucket-historical.yaml` 即可，不需要额外 core profile 写回

### `apocalypse`

- 当前结论：`末世 / 生存 / 危险感不能消失 / 资源不能白给` 已可稳定暴露
- 当前状态：依赖 core profile + `bucket-apocalypse.yaml` 即可，不需要额外 core profile 写回

### `ceo-romance`

- 当前结论：`先婚后爱 / 追妻 / 双线并进 / 总裁设定不能悬浮 / 关系冲突必须有现实后果` 已可稳定暴露
- 当前状态：当前 core profile 已满足这组高层候选字段，不需要额外本体写回

### `sweet-youth`

- 当前结论：`高甜 / 校园心动 / 双线并进 / 高甜不等于低幼 / 误会不能长时间拖延` 已可稳定暴露
- 当前状态：当前 core profile 已满足这组高层候选字段，不需要额外本体写回

### `melodrama`

- 当前结论：`误会 / 追妻 / 误会追妻双线 / 狗血要讲逻辑 / 误会不能纯靠不长嘴` 已可稳定暴露
- 当前状态：当前 core profile 已满足这组高层候选字段，不需要额外本体写回

### `sweet-romance`

- 当前结论：`高甜 / 心动日常 / 高甜日常推进 / 不能转虐 / 男主必须专一` 已可稳定暴露
- 当前状态：当前 core profile 已满足这组高层候选字段，不需要额外本体写回

### `urban-brainhole`

- 当前结论：`系统 / 逆袭 / 反差连锁 / 反差设定必须尽快兑现` 可由现有 bucket overlay 稳定暴露
- 当前状态：依赖 core profile + `bucket-urban-brainhole.yaml` 即可，不需要额外 core profile 写回

### `workplace-romance`

- 当前结论：`先婚后爱 / 办公室暧昧 / 关系工作同场换账 / 办公室权力关系要具体` 可由现有 bucket overlay 稳定暴露
- 当前状态：依赖 core profile + `bucket-workplace-romance.yaml` 即可，不需要额外 core profile 写回

### `urban-daily`

- 当前结论：`日常治愈 / 群像 / 日常账本 / 关系升温必须伴随现实牵连` 可由现有 bucket overlay 稳定暴露
- 当前状态：依赖 core profile + `bucket-urban-daily.yaml` 即可，不需要额外 core profile 写回

### `era`

- 当前结论：`时代变迁 / 奋斗成长 / 时代细节不能失真 / 奋斗不能脱离时代土壤` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `farming`

- 当前结论：`丰收致富 / 温馨治愈 / 发展速度要合理 / 治愈感不能被狗血冲突破坏` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `republic-romance`

- 当前结论：`乱世情缘 / 时代悲歌 / 时代感不能悬浮 / 爱情线必须扎根乱世处境` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `ancient-romance`

- 当前结论：`高门婚配 / 权谋情感 / 礼法关系不能悬浮 / 情感推进必须服从古代身份秩序` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `fantasy-romance`

- 当前结论：`奇幻恋爱 / 跨种族情缘 / 奇幻设定必须服务情感主线 / 跨种族恋爱必须讲清代价与阻力` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `war-spy`

- 当前结论：`潜伏智斗 / 家国信仰 / 历史背景不能失真 / 身份处理必须长期保持高压谨慎` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `urban-life`

- 当前结论：`温馨日常 / 生活改善 / 生活细节必须真实可感 / 人物关系要有烟火气` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `livestream`

- 当前结论：`粉丝增长 / 打赏互动 / 直播反馈必须及时可见 / 互动爽点不能替代真实成长` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `game-sports`

- 当前结论：`竞技成长 / 逆境翻盘 / 比赛规则不能出硬伤 / 成长突破必须来自训练与对抗` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `mystery-brainhole`

- 当前结论：`脑洞解谜 / 惊喜反转 / 创意设定要自洽 / 反转要有伏笔` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `mystery-creative`

- 当前结论：`脑洞解谜 / 规则反转 / 反转必须有伏笔 / 设定解释不能糊弄过关` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `female-mystery`

- 当前结论：`悬疑言情 / 女性主体 / 悬疑线与感情线要平衡 / 女性角色必须保有主体性` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `supernatural`

- 当前结论：`诡异求生 / 规则驱鬼 / 鬼怪规则必须自洽 / 危险感不能被爽点完全冲掉` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `rule-mystery`

- 当前结论：`规则压迫 / 漏洞求生 / 规则设计必须有内在逻辑 / 违反规则的代价必须够重` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `infinite-flow`

- 当前结论：`副本通关 / 绝境翻盘 / 副本规则必须自洽 / 队友不能全是工具人` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `sci-fi`

- 当前结论：`科技突破 / 文明碰撞 / 科技设定必须自洽 / 术语解释不能压垮阅读节奏` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `gaowu`

- 当前结论：`越级挑战 / 武道成长 / 突破必须有积累 / 越级不能无代价发生` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段

### `western-fantasy`

- 当前结论：`魔法冒险 / 领地成长 / 魔法规则必须有代价 / 世界观体系不能自相矛盾` 已可稳定暴露
- 当前状态：本轮已补齐最小 `platform_positioning.fanqie`，当前可进入后续跨平台校正阶段
