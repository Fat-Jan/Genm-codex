# Genm-codex 第十五阶段范围设计

## 设计结论

第十四阶段已经把 RC 计划、RC 退出条件、RC 执行记录和写作模型策略都准备好了。

因此第十五阶段不再讨论“要不要发起 RC”，而是直接进入：

- **`v1.0.0-rc1` 发起层**

---

## 核心目标

把当前项目从：

- RC 准备期

推进到：

- RC 已发起

并把这一状态同步到：

- 执行记录
- release 文稿
- 项目入口文档

---

## 第一版产物

- `docs/releases/v1.0.0-rc1.md`
- `docs/phase-15-summary.md`

并同步更新：

- `docs/v1-rc-execution-log.md`
- `docs/codex-migration-plan.md`
- `README.md`

---

## 不做什么

第十五阶段暂不做：

- 新能力迁移
- `novel-scan` 正式化
- shared 策略切换
- 直接发布正式 `v1.0.0`

---

## 当前推荐下一步

如果继续自动推进，第十五阶段最自然的动作是：

1. 更新 RC 执行记录状态为“已发起”
2. 创建 `v1.0.0-rc1` prerelease
3. 把后续工作切换成：
   - 仅修 blocker
   - 不再扩默认能力范围
