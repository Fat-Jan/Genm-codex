# Quality Route Smoke 2026-03-26

## 目的

验证 `review / precheck / package` 现在是否能对同一批样本给出一致的方向性判断。

## 样本 1：`她升职那天，前上司成了我合租室友`

- 证据：
  - `docs/writing-core-framework/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md`
- 当前一致结论：
  - `review` 方向：无明显结构 blocker，可继续
  - `precheck`：`ready-now`
  - `package`：`packaging-needs-update: no`
- 路由判断：
  - `route_signal = pass`

## 样本 2：`恶女 x 宫斗宅斗`

- 证据：
  - `docs/research/fanqie/fanqie-evil-gongdou-production-template.md`
  - `docs/research/fanqie/fanqie-evil-gongdou-submission-assessment.md`
- 当前一致结论：
  - `review`：需要回到真值与关系词一致性
  - `precheck`：`do-not-submit`
  - `package`：`packaging-needs-update: yes`
- 路由判断：
  - `route_signal = hard_blocker`

## 当前结论

- 当前质量路由至少已经能稳定区分：
  - `pass`
  - `hard_blocker`
- 后续还应继续补：
  - `revise_before_submit`
  - `packaging_hold`
  的真实项目样本
