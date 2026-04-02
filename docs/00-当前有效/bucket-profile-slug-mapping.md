# Bucket / Profile 命名映射规范

> Status: `active-reference-spec`
>
> 当前 authoritative truth：
> - machine-readable registry：`shared/templates/profile-bucket-registry-v1.json`
> - runtime resolution：`scripts/profile_contract.py`
> - `state.genre_profile.bucket` 当前保存的是 consumer-facing bucket 名称（如 `宫斗宅斗`），不是 slug

## 目的

解决 bucket、profile、genre 之间的命名漂移，并说明当前已经落地的 slug 映射真值、运行时入口与状态投影口径。

---

## 当前命名漂移

| 类型 | 当前值 | 问题 |
|------|--------|------|
| bucket | 宫斗宅斗 | 中文，不便于代码处理 |
| profile | palace-intrigue | 英文，与 bucket 不一致 |
| fanqie-mvp-bucket | gongdou_zhai | 英文，与 profile 不一致 |
| genre | 宫斗宅斗 | 中文，与 bucket 相同 |

---

## 命名规范

### 1. Slug 格式

- **profile slug**: 小写英文，连字符分隔（如 `palace-intrigue`）
- **bucket slug**: 小写英文，连字符分隔（如 `palace-intrigue`）
- **fanqie-mvp-bucket slug**: 小写英文，下划线分隔（如 `gongdou_zhai`）

### 2. 映射规则

- **profile slug = bucket slug**: 保持一致
- **fanqie-mvp-bucket slug**: 保持原有格式（下划线），但建立映射关系
- **display_name**: 中文显示名，用于 UI 和文档

---

## 示意映射表

下表用于说明三类命名之间的关系与命名意图，不作为 machine-readable 当前真值。完整当前映射请以 `shared/templates/profile-bucket-registry-v1.json` 为准。

| profile slug | bucket slug | fanqie-mvp-bucket slug | display_name | description |
|--------------|-------------|------------------------|--------------|-------------|
| palace-intrigue | palace-intrigue | gongdou_zhai | 宫斗宅斗 | 后宫争斗、宅门内斗、权谋复仇 |
| urban-brainhole | urban-brainhole | dushi_naodong | 都市脑洞 | 都市背景的脑洞、系统、异能 |
| urban-daily | urban-daily | dushi_changri | 都市日常 | 都市背景的日常生活、治愈 |
| sweet-youth | sweet-youth | qingchun_tianchong | 青春甜宠 | 青春校园甜宠 |
| ceo-romance | ceo-romance | haomen_zongcai | 豪门总裁 | 豪门总裁、先婚后爱 |
| workplace-romance | workplace-romance | zhichang_hunlian | 职场婚恋 | 职场背景的婚恋 |
| historical-brainhole | historical-brainhole | lishi_naodong | 历史脑洞 | 历史背景的脑洞、穿越 |
| xuanhuan | xuanhuan | xuanhuan_naodong | 玄幻脑洞 | 玄幻背景的脑洞、系统 |
| xiuxian | xiuxian | xiuxian | 修仙 | 修仙题材 |
| urban-superpower | urban-superpower | dushi_yineng | 都市异能 | 都市背景的异能 |
| romance | romance | yanqing | 言情 | 通用言情 |
| ancient-romance | ancient-romance | gudai_yanqing | 古代言情 | 古代背景的言情 |
| historical | historical | lishi | 历史 | 历史题材 |
| fantasy-romance | fantasy-romance | xuanhuan_yanqing | 玄幻言情 | 玄幻背景的言情 |
| melodrama | melodrama | gouxue | 狗血 | 狗血剧情 |
| substitute | substitute | tishen | 替身 | 替身题材 |
| evil-girl | evil-girl | evil | 恶女 | 恶女题材 |
| system | system | xitong | 系统 | 系统流 |
| infinite-flow | infinite-flow | wuxianliu | 无限流 | 无限流题材 |
| apocalypse | apocalypse | moshi | 末世 | 末世题材 |
| sci-fi | sci-fi | kehuan | 科幻 | 科幻题材 |
| mystery-horror | mystery-horror | xuanyi_kongbu | 悬疑恐怖 | 悬疑恐怖题材 |
| rule-horror | rule-horror | guize_kongbu | 规则恐怖 | 规则恐怖题材 |
| rule-mystery | rule-mystery | guize_xuanyi | 规则悬疑 | 规则悬疑题材 |
| esports | esports | dianjing | 电竞 | 电竞题材 |
| game-sports | game-sports | youxi_saiyou | 游戏赛游 | 游戏赛游题材 |
| livestream | livestream | zhibo | 直播 | 直播题材 |
| farming | farming | zhongtian | 种田 | 种田题材 |
| cthulhu | cthulhu | kelusu | 克苏鲁 | 克苏鲁题材 |
| dark | dark | anhei | 暗黑 | 暗黑题材 |
| dark-theme | dark-theme | anhei_xilie | 暗黑系列 | 暗黑系列题材 |
| spy-war | spy-war | jianzhe | 谍战 | 谍战题材 |
| war-spy | war-spy | zhanzheng | 战争 | 战争题材 |
| realistic | realistic | xianshi | 现实 | 现实题材 |
| female-mystery | female-mystery | nvxing_xuanyi | 女性悬疑 | 女性悬疑题材 |
| fertility | fertility | shengyu | 生育 | 生育题材 |
| multi-offspring | multi-offspring | duotai | 多胎 | 多胎题材 |
| sweet-romance | sweet-romance | tianchong | 甜宠 | 甜宠题材 |
| dramatic-romance | dramatic-romance | gouxue_yanqing | 狗血言情 | 狗血言情题材 |
| republic-romance | republic-romance | minguo_yanqing | 民国言情 | 民国言情题材 |
| modern-brainhole | modern-brainhole | xiandai_naodong | 现代脑洞 | 现代脑洞题材 |
| modern-creative | modern-creative | xiandai_chuangyi | 现代创意 | 现代创意题材 |
| historical-creative | historical-creative | lishi_chuangyi | 历史创意 | 历史创意题材 |
| mystery-creative | mystery-creative | xuanyi_chuangyi | 悬疑创意 | 悬疑创意题材 |
| urban-creative | urban-creative | dushi_chuangyi | 都市创意 | 都市创意题材 |
| urban-life | urban-life | dushi_shenghuo | 都市生活 | 都市生活题材 |
| crossover | crossover | chuanhua | 穿花 | 穿花题材 |
| era | era | shidai | 时代 | 时代题材 |
| western-fantasy | western-fantasy | xifang_qihuan | 西方奇幻 | 西方奇幻题材 |
| supernatural | supernatural | chaoran | 超然 | 超然题材 |
| zhihu-short | zhihu-short | zhihu_duanpian | 知乎短篇 | 知乎短篇题材 |

---

## 使用规范

### 1. 在代码中

- **profile slug**: 用于目录路径、文件名、配置键
- **bucket slug**: 用于 bucket 分配、条件判断
- **fanqie-mvp-bucket slug**: 用于番茄 MVP bucket 标识

### 2. 在文档中

- **display_name**: 用于 UI 显示、文档标题
- **profile slug**: 用于内部引用、链接
- **bucket slug**: 用于 bucket 相关说明

### 3. 在状态中

- `genre_profile.bucket`: 使用当前 bucket 名称 / display_name（如 `宫斗宅斗`）
- `genre_profile.loaded`: 使用当前生效 profile 路径
- `meta.genre`: 使用 display_name
- 如需在运行时把 fanqie bucket key、bucket 名称和 profile slug 互相转换，应走 registry + `profile_contract.py`，而不是在 state 中直接存 slug

---

## 当前运行时入口

当前不再建议把映射关系维护成散落在文档里的硬编码函数。实际运行时应以以下入口为准：

1. `shared/templates/profile-bucket-registry-v1.json`
   - machine-readable 真值
   - 当前承载 fanqie bucket key -> `bucket_name` -> `profile_slug` 的映射

2. `scripts/profile_contract.py`
   - `_load_fanqie_bucket_name_map()` 会从 registry 读取 fanqie key 与 bucket 名称映射
   - `resolve_bucket_overlay_path()` 同时支持：
     - bucket 名称（如 `宫斗宅斗`）
     - fanqie bucket key（如 `gongdou_zhai`）
   - `resolve_profile_layers()` / `load_profile_with_overlays()` 会把 profile、platform overlay 和 bucket overlay 串起来

3. `state.genre_profile`
   - 当前保存 consumer-facing 轻量投影
   - `bucket` 字段保存当前 bucket 名称，而不是 slug
   - 更完整的组合定位信息继续放在 `.mighty/content-positioning.json`

## 当前验证证据

- `tests/test_profile_bucket_registry.py`
  - 验证 registry 存在，并覆盖关键 fanqie key 映射
- `tests/test_profile_contract.py`
  - 验证 bucket overlay 可由 bucket 名称和 fanqie bucket key 解析
  - 验证所有声明了 `fanqie primary_bucket` 的 profile 都能解析到对应 overlay
- `tests/test_fanqie_p0_smoke.py`
  - 验证 `state.genre_profile.bucket` 当前以 bucket 名称参与实际推断
- `scripts/validate-migration.sh`
  - 已把 `bucket-profile-slug-mapping.md`、`profile-bucket-registry-v1.json` 和首批 bucket overlay 一并纳入结构校验

---

## 完成标记

- [x] 有独立设计稿（本文件）
- [x] 明确字段定义、枚举值和最小用途（本文件）
- [x] 与 profile 系统对接（`scripts/profile_contract.py`、`tests/test_profile_contract.py`）
- [x] 与 bucket 系统对接（`shared/templates/profile-bucket-registry-v1.json`、`scripts/profile_contract.py`）
- [x] 与 fanqie-mvp-bucket 系统对接（`shared/templates/profile-bucket-registry-v1.json`、`tests/test_profile_bucket_registry.py`）
- [x] 有测试样本能验证字段有效性（`tests/test_profile_bucket_registry.py`、`tests/test_profile_contract.py`、`tests/test_fanqie_p0_smoke.py`）
