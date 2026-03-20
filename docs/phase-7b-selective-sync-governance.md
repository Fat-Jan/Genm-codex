# Genm-codex Phase 7B Selective-Sync Governance

## 目标

为 `shared` 资产从当前的 full-copy 模式，演进到更可控的 selective-sync 模式建立治理方案。

## 当前现状

当前同步策略：

- `scripts/sync-shared-from-genm.sh`
- 每次直接整包复制：
  - `build/profiles`
  - `build/references`
  - `build/templates`

优点：

- 简单
- 稳定
- 前几阶段迁移速度快

问题：

- 同步粒度太粗
- `shared` 体量持续增长
- 很多 skill 只需要其中一小部分
- 路径解析负担分散在多个 skill 中

## 当前风险点

### 1. 引用路径耦合广

当前多个 skill 直接引用：

- `shared/profiles/`
- `../shared/profiles/`
- `../../shared/profiles/`

受影响明显的包括：

- `novel-init`
- `novel-write`
- `novel-outline`
- `novel-review`
- `novel-genre`
- `novel-analyze`
- `novel-precheck`

### 2. 资产更新不可见

整包复制的模式下，用户很难快速知道：

- 哪些 shared 文件变化了
- 哪些 skill 真会受影响
- 哪些同步只是噪音

### 3. selective-sync 不能直接切

如果现在直接切 selective-sync，风险很高：

- 现有 skill 的相对路径假设会被冲击
- 某些 profile / template / reference 可能被漏掉
- smoke 结果可能从“稳定”变成“到处缺文件”

## selective-sync 的建议边界

### 不按单 skill 同步

不建议做到：

- “每个 skill 只拉自己用到的 3 个文件”

原因：

- 维护成本太高
- 路径矩阵会爆炸

### 建议按资产域同步

更合理的是按资产域划分：

#### Domain A：profiles

- 同步策略按 genre / platform 分组
- 示例：
  - `shared/profiles/xuanhuan/`
  - `shared/profiles/xiuxian/`
  - `shared/profiles/urban-superpower/`

#### Domain B：references

- 按子目录分组：
  - `shared/references/shared/`
  - `shared/references/writing/`
  - `shared/references/platforms/`
  - `shared/references/creativity/`

#### Domain C：templates

- 按模板簇分组：
  - `shared/templates/outline/`
  - `shared/templates/characters/`
  - `shared/templates/world/`
  - `shared/templates/chapter-structure/`

## 推荐演进路径

### Step 1：先做“可观测同步”

在不改变 full-copy 逻辑前，先补：

- 同步报告
- 资产变更摘要
- 哪些目录发生变化

先提高可见性，而不是先改策略。

**当前进展**：

- `scripts/sync-shared-from-genm.sh` 已补 `--report`
- 也已补 `--domain <profiles|references|templates>`
- 已补 `--report-json`
- 当前仍不切换 full-copy，只先提供可观测性

### Step 2：引入“按域同步”模式

例如未来支持：

- `sync-shared-from-genm.sh --domain profiles`
- `sync-shared-from-genm.sh --domain references`
- `sync-shared-from-genm.sh --domain templates`

这一步仍然不做细粒度 selective-sync。

### Step 3：引入“按子域同步”

例如：

- `--profile xuanhuan`
- `--references shared,writing`
- `--templates outline,characters`

只有到这一步，才算真正进入 selective-sync。

## 前置检查要求

在任何 selective-sync 实施前，至少先具备：

1. **引用清单**
   - 哪些 skill 依赖哪些 shared 子域

2. **缺失探测**
   - 启动或校验时能明确提示缺了哪类 shared 资产

3. **同步报告**
   - 每次同步后能看到：
     - 同步了什么
     - 跳过了什么
     - 目标目录变了什么

4. **回退路径**
   - 仍然保留 full-copy 回退模式

## 当前建议

第七阶段 B 段先只做治理，不切策略。

最合理的下一步是：

1. 给 `sync-shared-from-genm.sh` 增加“报告模式”
2. 生成一份 shared 依赖映射
3. 再评估是否值得上“按域同步”

**当前进展补充**：

- `docs/shared-asset-dependency-map.md` 已建立，用于说明各 skill 对 shared 资产的依赖面

## 当前结论

selective-sync 值得做，但不适合直接开干。

当前最稳的推进顺序是：

- 先治理
- 再可观测
- 最后才是策略切换
