# `v1.5` Profile 扩面候选与优先级

## 目的

这份文档收口 `P1-C`，只做 candidate inventory 和优先级排序，不直接批量建文件。

排序标准只看三件事：

1. 当前样本是否已经有真实承载。
2. 当前 bucket / profile / positioning 的**质量与消费读面**是否仍存在明显缺口。
3. 补它之后，是否能立刻提升 `v1.5` 的 registry / consumer 可用性。

补充说明：

- 当前 `52/52` 个标准 profile 已具备 `platform_positioning`
- 当前 `52/52` 个标准 profile 已具备 `profile-tomato.yaml`
- 当前 `52/52` 个标准 profile 已具备首层 `bucket-*.yaml`

因此，这份优先级文档当前关注的已不再是“先把基础文件补齐”，而是：

- 哪些题材最值得优先做更深一层的 consumer/readiness 收口
- 哪些对象更适合作为下一批扩面与质量校准的主样本线

---

## 第一优先级

这一组已经有真实样本承载，且最适合优先做下一批 consumer/readiness 收口。

### 1. 宫斗宅斗

原因：

- 当前高置信项目样本最集中
- regression 样本也在这条线上
- gate / scan / package / review 的联动价值最高
- 最适合作为“样本 -> profile -> registry -> consumer”全链复检主线

### 2. 历史脑洞

原因：

- 已有多个真实项目样本
- 与 truth source、地方官场、旧案、结构推进关系紧密
- 很适合验证 profile → bucket → positioning 读取链
- 很适合作为下一批 profile 深化校准对象

### 3. 都市日常

原因：

- 已有多个 bucket 样本
- 与关系、日常推进、现实秩序承载有关
- 可以补足“非强冲突题材”的 profile 面
- 适合继续验证弱冲突题材的 consumer 读取与 quality gate 表现

### 4. 豪门总裁

原因：

- 已有多个真实样本
- 包装层和平台 cue 明显
- 很适合验证 `package_cues` 与 positioning 的消费者读取
- 适合继续强化 package / precheck 侧的定位消费

### 5. 修仙

原因：

- 有稳定 bucket 样本
- 与设定、规则、升级路径强相关
- 对 profile contract 的结构字段有较高测试价值
- 适合作为设定 / 规则型题材的深化校准对象

---

## 第二优先级

### 6. 青春甜宠

原因：

- 已有稳定样本
- 平台 cue 较清晰
- 但当前紧迫性低于上面几类主样本线

### 7. 都市脑洞

原因：

- 已有样本承载
- 与系统流、脑洞流、爽点组织有关
- 可以补，但不应早于宫斗宅斗 / 历史脑洞 / 豪门总裁

### 8. 职场婚恋

原因：

- 已有样本，但数量少于上面几类
- 适合在前一批 profile 收口后再补

---

## 第三优先级

这一组不是不能补，而是应等前两批把 consumer/readiness 收口跑顺后再动。

- 恶女 x 宫斗宅斗
- 恶女 x 情感
- 恶女 x 甜宠
- 双女主替身
- 系统

原因：

- 这类更像组合题材、派生题材或专项验证题材
- 它们很适合做下一阶段扩面，但不适合作为当前第一批 consumer/readiness 收口对象

---

## 当前推荐顺序

建议后续如果继续做下一批 profile 扩面，按这个顺序推进：

1. 宫斗宅斗
2. 历史脑洞
3. 都市日常
4. 豪门总裁
5. 修仙
6. 青春甜宠
7. 都市脑洞
8. 职场婚恋

组合题材和派生题材放到后面。

---

## 当前不做的事

这份文档当前不做：

- 直接新增 profile 文件
- 直接新增 overlay 文件
- 直接改 `profile_contract.py`
- 直接发明新的 bucket 名称体系
- 也不再把“基础 platform_positioning / overlay 文件是否存在”当成当前首要判断标准

它只负责把后续扩面顺序排清楚。
