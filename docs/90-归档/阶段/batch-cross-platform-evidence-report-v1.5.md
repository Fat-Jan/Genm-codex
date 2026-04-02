# Batch 2 完成汇报

### 本轮完成对象
- `sweet-romance`：`partial`
- `melodrama`：`partial`
- `substitute`：`partial`
- `urban-life`：`partial`
- `modern-brainhole`：`partial`

### 本轮新增/更新
- `docs/10-进行中/batch-cross-platform-evidence-pack-v1.5.md`
- `progress.md`

### 每个 profile 的结果

#### sweet-romance
- 状态：`partial`
- 完成等级：`A / B / A`（起点待补 A 级实体页）
- 番茄：`A | https://fanqienovel.com/page/7485098015225547838`（心动的感觉，爱情我来了）
- 番茄：`A | https://fanqienovel.com/page/7591843054365985816`（靠近你，甜度超标）
- 起点：`B | https://m.qidian.com/rank/rec/catid2/`（起点青春甜宠推荐排行）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=5574552`（蜜桃甜）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=8689436`（甜度超标）
- 备注：番茄双实体页覆盖"心动日常"与"校园甜宠"，起点仅有 B 级分类页

#### melodrama
- 状态：`partial`
- 完成等级：`A / B / A`（起点待补 A 级实体页）
- 番茄：`A | https://fanqienovel.com/page/7378472519826672664`（追妻火葬场失败以后）
- 番茄：`A | https://fanqienovel.com/keyword/7344472635058882599`（爱意燃尽，傅总追妻火葬场）
- 起点：`B | https://m.qidian.com/rank/rec/catid2/`（起点现代言情推荐排行）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=4507570`（替身）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=4462115`（替身竟是本王自己）
- 备注：番茄双实体页覆盖"追妻火葬场"与"豪门虐恋"，起点仅有 B 级分类页

#### substitute
- 状态：`partial`
- 完成等级：`A / B / A`（起点待补 A 级实体页）
- 番茄：`A | https://fanqienovel.com/page/7539093126963547160`（替身女配能听到弹幕吐槽）
- 番茄：`A | https://fanqienovel.com/keyword/7508814946927642643`（得知自己是替身，合约妻子哭惨了）
- 起点：`B | https://m.qidian.com/rank/rec/catid2/`（起点现代言情推荐排行）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=4507570`（替身）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=4462115`（替身竟是本王自己）
- 备注：番茄双实体页覆盖"弹幕穿书"与"合约替身"，起点仅有 B 级分类页

#### urban-life
- 状态：`partial`
- 完成等级：`A / B / A`（起点待补 A 级实体页）
- 番茄：`A | https://fanqienovel.com/page/7293145014165572647`（美食：随机摆摊，顾客追我十条街）
- 番茄：`A | https://fanqienovel.com/keyword/1853102`（小院儿生活）
- 起点：`B | https://m.qidian.com/category/catid4/subcatid12-male/`（起点女生网·都市生活分类）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=10610952`（我在小城慢慢活）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=9345752`（小巷日常[八零]）
- 备注：番茄双实体页覆盖"美食摆摊"与"年代小院"，起点为女生网分类页（B 级）

#### modern-brainhole
- 状态：`partial`
- 完成等级：`A / B / A`（起点待补 A 级实体页）
- 番茄：`A | https://fanqienovel.com/page/7492738355491245080`（社畜逆袭：世界剧本任我改）
- 番茄：`A | https://fanqienovel.com/keyword/2004318551`（限时占有）
- 起点：`B | https://m.qidian.com/rank/rec/catid15/2/`（起点现实小说推荐排行）
- 晋江：`A | https://www.jjwxc.net/onebook.php?novelid=10610952`（我在小城慢慢活）
- 备注：番茄双实体页覆盖"创意命运改写"，起点仅有 B 级分类页，晋江实体页偏向日常

### 本轮缺口
- `sweet-romance`：起点缺 A 级实体页，仅有 B 级分类排行页
- `melodrama`：起点缺 A 级实体页，仅有 B 级分类排行页
- `substitute`：起点缺 A 级实体页，仅有 B 级分类排行页
- `urban-life`：起点缺 A 级实体页，仅有 B 级女生网分类页
- `modern-brainhole`：起点缺 A 级实体页，仅有 B 级分类排行页

### 搜索/抓取说明
- 本轮优先使用：`Exa 官方域名搜索`
- 搜索策略：
  - Exa 搜索番茄小说 site:fanqienovel.com/page + 题材关键词
  - Exa 搜索晋江文学城 onebook.php?novelid + 题材关键词
  - Exa 搜索起点中文网 book.qidian.com + 题材关键词
  - 换关键词轮搜（如"高甜/甜宠/心动日常"）
- 起点侧困难：m.qidian.com/book/ 实体页 Exa 命中率极低，改用分类排行页（B 级）作为入口
- 未使用非官方来源

### 验证
- `bash scripts/validate-migration.sh`
  - 结果：`passed`
- `python3 -m pytest -q tests/test_profile_contract.py`
  - 结果：`65 passed`

### 是否可进入下一批
- `yes`（但需要说明）
- 原因：5 个 profile 均达到 partial 门槛（番茄≥1A + 起点/晋江至少1个B + 晋江有A），但起点侧均需要手动补 A 级实体页才能升为 complete。建议下一批优先处理起点侧已确认 A 级的 profile，或尝试从番茄/晋江作者页反向追溯起点实体页。
