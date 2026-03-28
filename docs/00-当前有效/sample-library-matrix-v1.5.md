# `v1.5` 样本库矩阵

## 目的

这份矩阵把 `sample-manifest-v1.json` 的主要样本层级收成一份当前有效的人读说明，方便在 `P2-B` 完成后快速确认 manifest 已覆盖哪些样本面。

机器真值仍以：

- `shared/templates/sample-manifest-v1.json`

为准。

---

## 当前分层覆盖

### `smoke / baseline`

- `e2e-novel`
- `e2e-gongdou`
- `e2e-gongdou-evil`
- `e2e-qinggan`
- `e2e-qinggan-evil`
- `e2e-tianchong`
- `e2e-tianchong-evil`
- `e2e-dual-substitute-evil`

### `smoke / derived`

- `gongdou-antiflattening-derived`
- `qinggan-antiflattening-derived`
- `system-antiflattening-derived`
- `dual-substitute-antiflattening-derived`

### `project / high_confidence`

- `shunvmoulue-high-confidence`
- `hunshu-high-confidence`

### `project / regression`

- `jiazhuangdan-regression`

### `project / bucket_sample`

- 修仙
- 豪门总裁
- 青春甜宠
- 都市脑洞
- 都市日常
- 历史脑洞
- 职场婚恋

其中都市日常、历史脑洞、豪门总裁、都市脑洞、修仙、青春甜宠都已补到多样本覆盖，不再只剩单点示例。

---

## 使用口径

- 默认 smoke / regression / sample library consumer 应优先读 manifest。
- 索引页继续保留给人读，但不再作为样本真值中心。
- 后续若新增样本，应先补 manifest，再补索引页和说明页。
