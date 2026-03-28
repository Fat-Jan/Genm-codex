# Bucket / Profile 命名映射规范

## 目的

解决 bucket、profile、genre 之间的命名漂移，建立统一的 slug 映射规范。

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

## 映射表

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

- `genre_profile.bucket`: 使用 bucket slug
- `genre_profile.loaded`: 使用 profile slug
- `meta.genre`: 使用 display_name

---

## 映射函数

在代码中，需要建立以下映射函数：

```python
# profile slug -> bucket slug
def profile_to_bucket(profile_slug: str) -> str:
    return profile_slug  # 直接映射

# bucket slug -> fanqie-mvp-bucket slug
def bucket_to_fanqie_mvp(bucket_slug: str) -> str:
    mapping = {
        "palace-intrigue": "gongdou_zhai",
        "urban-brainhole": "dushi_naodong",
        "urban-daily": "dushi_changri",
        "sweet-youth": "qingchun_tianchong",
        "ceo-romance": "haomen_zongcai",
        "workplace-romance": "zhichang_hunlian",
        "historical-brainhole": "lishi_naodong",
        "xuanhuan": "xuanhuan_naodong",
        "xiuxian": "xiuxian",
        "urban-superpower": "dushi_yineng",
        "romance": "yanqing",
        "ancient-romance": "gudai_yanqing",
        "historical": "lishi",
        "fantasy-romance": "xuanhuan_yanqing",
        "melodrama": "gouxue",
        "substitute": "tishen",
        "evil-girl": "evil",
        "system": "xitong",
        "infinite-flow": "wuxianliu",
        "apocalypse": "moshi",
        "sci-fi": "kehuan",
        "mystery-horror": "xuanyi_kongbu",
        "rule-horror": "guize_kongbu",
        "rule-mystery": "guize_xuanyi",
        "esports": "dianjing",
        "game-sports": "youxi_saiyou",
        "livestream": "zhibo",
        "farming": "zhongtian",
        "cthulhu": "kelusu",
        "dark": "anhei",
        "dark-theme": "anhei_xilie",
        "spy-war": "jianzhe",
        "war-spy": "zhanzheng",
        "realistic": "xianshi",
        "female-mystery": "nvxing_xuanyi",
        "fertility": "shengyu",
        "multi-offspring": "duotai",
        "sweet-romance": "tianchong",
        "dramatic-romance": "gouxue_yanqing",
        "republic-romance": "minguo_yanqing",
        "modern-brainhole": "xiandai_naodong",
        "modern-creative": "xiandai_chuangyi",
        "historical-creative": "lishi_chuangyi",
        "mystery-creative": "xuanyi_chuangyi",
        "urban-creative": "dushi_chuangyi",
        "urban-life": "dushi_shenghuo",
        "crossover": "chuanhua",
        "era": "shidai",
        "western-fantasy": "xifang_qihuan",
        "supernatural": "chaoran",
        "zhihu-short": "zhihu_duanpian",
    }
    return mapping.get(bucket_slug, bucket_slug)

# fanqie-mvp-bucket slug -> bucket slug
def fanqie_mvp_to_bucket(fanqie_mvp_slug: str) -> str:
    mapping = {
        "gongdou_zhai": "palace-intrigue",
        "dushi_naodong": "urban-brainhole",
        "dushi_changri": "urban-daily",
        "qingchun_tianchong": "sweet-youth",
        "haomen_zongcai": "ceo-romance",
        "zhichang_hunlian": "workplace-romance",
        "lishi_naodong": "historical-brainhole",
        "xuanhuan_naodong": "xuanhuan",
        "xiuxian": "xiuxian",
        "dushi_yineng": "urban-superpower",
        "yanqing": "romance",
        "gudai_yanqing": "ancient-romance",
        "lishi": "historical",
        "xuanhuan_yanqing": "fantasy-romance",
        "gouxue": "melodrama",
        "tishen": "substitute",
        "evil": "evil-girl",
        "xitong": "system",
        "wuxianliu": "infinite-flow",
        "moshi": "apocalypse",
        "kehuan": "sci-fi",
        "xuanyi_kongbu": "mystery-horror",
        "guize_kongbu": "rule-horror",
        "guize_xuanyi": "rule-mystery",
        "dianjing": "esports",
        "youxi_saiyou": "game-sports",
        "zhibo": "livestream",
        "zhongtian": "farming",
        "kelusu": "cthulhu",
        "anhei": "dark",
        "anhei_xilie": "dark-theme",
        "jianzhe": "spy-war",
        "zhanzheng": "war-spy",
        "xianshi": "realistic",
        "nvxing_xuanyi": "female-mystery",
        "shengyu": "fertility",
        "duotai": "multi-offspring",
        "tianchong": "sweet-romance",
        "gouxue_yanqing": "dramatic-romance",
        "minguo_yanqing": "republic-romance",
        "xiandai_naodong": "modern-brainhole",
        "xiandai_chuangyi": "modern-creative",
        "lishi_chuangyi": "historical-creative",
        "xuanyi_chuangyi": "mystery-creative",
        "dushi_chuangyi": "urban-creative",
        "dushi_shenghuo": "urban-life",
        "chuanhua": "crossover",
        "shidai": "era",
        "xifang_qihuan": "western-fantasy",
        "chaoran": "supernatural",
        "zhihu_duanpian": "zhihu-short",
    }
    return mapping.get(fanqie_mvp_slug, fanqie_mvp_slug)

# bucket slug -> display_name
def bucket_to_display_name(bucket_slug: str) -> str:
    mapping = {
        "palace-intrigue": "宫斗宅斗",
        "urban-brainhole": "都市脑洞",
        "urban-daily": "都市日常",
        "sweet-youth": "青春甜宠",
        "ceo-romance": "豪门总裁",
        "workplace-romance": "职场婚恋",
        "historical-brainhole": "历史脑洞",
        "xuanhuan": "玄幻脑洞",
        "xiuxian": "修仙",
        "urban-superpower": "都市异能",
        "romance": "言情",
        "ancient-romance": "古代言情",
        "historical": "历史",
        "fantasy-romance": "玄幻言情",
        "melodrama": "狗血",
        "substitute": "替身",
        "evil-girl": "恶女",
        "system": "系统",
        "infinite-flow": "无限流",
        "apocalypse": "末世",
        "sci-fi": "科幻",
        "mystery-horror": "悬疑恐怖",
        "rule-horror": "规则恐怖",
        "rule-mystery": "规则悬疑",
        "esports": "电竞",
        "game-sports": "游戏赛游",
        "livestream": "直播",
        "farming": "种田",
        "cthulhu": "克苏鲁",
        "dark": "暗黑",
        "dark-theme": "暗黑系列",
        "spy-war": "谍战",
        "war-spy": "战争",
        "realistic": "现实",
        "female-mystery": "女性悬疑",
        "fertility": "生育",
        "multi-offspring": "多胎",
        "sweet-romance": "甜宠",
        "dramatic-romance": "狗血言情",
        "republic-romance": "民国言情",
        "modern-brainhole": "现代脑洞",
        "modern-creative": "现代创意",
        "historical-creative": "历史创意",
        "mystery-creative": "悬疑创意",
        "urban-creative": "都市创意",
        "urban-life": "都市生活",
        "crossover": "穿花",
        "era": "时代",
        "western-fantasy": "西方奇幻",
        "supernatural": "超然",
        "zhihu-short": "知乎短篇",
    }
    return mapping.get(bucket_slug, bucket_slug)
```

---

## 完成标记

- [ ] 有独立设计稿（本文件）
- [ ] 明确字段定义、枚举值和最小用途（本文件）
- [ ] 与 profile 系统对接（待实现）
- [ ] 与 bucket 系统对接（待实现）
- [ ] 与 fanqie-mvp-bucket 系统对接（待实现）
- [ ] 有测试样本能验证字段有效性（待实现）
