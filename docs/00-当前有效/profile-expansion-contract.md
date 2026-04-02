# Profile Expansion Contract

## 目的

为后续 profile 扩面建立统一 contract，避免在没有 guardrail 的情况下批量补文件，重新引入：

- YAML 漂移
- overlay 缺失
- bucket / profile / Fanqie key 不一致

---

## 最低要求

每个新增 `profile.yaml` 至少要有：

- `name`
- `display_name`
- `description`
- `version`

建议同时具备：

- `template`
- `pacing`
- `cool_points`
- `strand_weights`
- `constraints`
- `reader_expectations`
- `taboos`

---

## `platform_positioning` 规则

如果 profile 计划用于 Fanqie-first 路线，或希望 downstream consumer 直接消费平台定位，则必须提供：

- `platform_positioning`

至少要能明确：

- `primary_bucket`
- `strong_tags`
- `narrative_modes`
- `tone_guardrails`
- `package_cues`

---

## `bucket overlay` 规则

如果某个 profile 已声明 `fanqie primary_bucket`，则必须同步提供对应的 `bucket overlay`。

也就是说：

- 只要 profile 对 Fanqie 给出了 `primary_bucket`
- 就必须存在可被 `profile_contract.py` resolve 到的 `bucket overlay`

---

## Fanqie 扩面特别规则

只要新增的是 Fanqie 路线 profile，就必须明确：

- `fanqie primary_bucket`
- 是否需要独立 `bucket overlay`
- 当前 bucket / profile / fanqie key 的映射关系是否已存在

---

## 验证门

扩面工作至少要过：

- `tests/test_profile_contract.py`
- `tests/test_content_positioning.py`
- `bash scripts/validate-migration.sh`

如果新增 profile 会影响 consumer 读取，也应补对应 consumer 测试。

---

## `mimo` 可做范围

在这份 contract 落地后，`mimo` 可以安全做：

- 批量补 profile
- 批量补 `platform_positioning`
- 批量补 `bucket overlay`
- profile inventory / 映射 / 说明文档

但不应直接改：

- `scripts/profile_contract.py`
- `scripts/build_content_positioning.py`
- schema / sidecar contract

这些仍由 `codex` 负责。
