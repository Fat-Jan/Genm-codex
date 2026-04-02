# Genm-codex 跨平台支持规划

## 目标

让 Genm-codex 项目不仅仅局限于 Codex 使用，也能被 Claude Code、OpenCode、OpenCLAW 等其他 AI 工具使用。

---

## 背景

### 当前状态

Genm-codex 是一个 Codex 原生网文创作技能工作区，包含：
- 31 个 skill（SKILL.md 格式）
- 54 个 profile（题材配置）
- 40+ 个脚本（Python/Shell）
- 通用的 shared 资产（references/templates/validators）

### 核心发现

**三大工具都使用相同的 AgentSkills 标准格式**（SKILL.md），Genm-codex 的 skill 格式具有良好的跨平台兼容性。

| 工具 | Skill 格式 | 存储位置 | 兼容性 |
|------|-----------|---------|--------|
| Codex | AgentSkills | `~/.codex/skills/` | 当前 |
| Claude Code | AgentSkills | `~/.claude/skills/` 或 `.claude/skills/` | ✅ 已兼容 |
| OpenCode | AgentSkills 兼容 | `~/.config/opencode/skills/` 或 `.opencode/skills/` | ✅ 兼容 |
| OpenCLAW | AgentSkills + Pi | `~/.openclaw/skills/` 或 `./skills/` | ✅ 兼容 |

---

## 依赖分析

### Codex 特有依赖（需要修改）

| 组件 | 依赖 | 迁移难度 |
|------|------|---------|
| 安装路径 | `install-skills.sh` 硬编码 `~/.codex/skills/` | 低 |
| 配置文件 | `novel-config`、`novel-test` 读取 `~/.codex/config.toml` | 中 |
| 配置读取 | `acquire_source_text.py` 的 `read_codex_config()` | 中 |
| Skill 描述 | SKILL.md 的 description 包含 "Codex-managed" | 低 |

### 通用组件（无需修改）

| 组件 | 说明 |
|------|------|
| SKILL.md 内容 | 工作流程、规则、约束都是通用的网文创作逻辑 |
| Scripts（大部分） | `thin-state.py`、`project-maintenance.py` 等通用脚本 |
| Shared 资产 | profiles、references、templates 都是通用配置 |
| 数据格式 | JSON schema、YAML 配置都是标准格式 |

---

## 实现方案

### 方案 1：最小改动（推荐）

修改 `install-skills.sh`，支持多平台安装：

```bash
#!/bin/bash
# 支持多平台安装

PLATFORM="${1:-codex}"  # 默认 codex

case "$PLATFORM" in
  codex)     TARGET_DIR="$HOME/.codex/skills" ;;
  claude)    TARGET_DIR="$HOME/.claude/skills" ;;
  opencode)  TARGET_DIR="$HOME/.config/opencode/skills" ;;
  openclaw)  TARGET_DIR="$HOME/.openclaw/skills" ;;
  *)         echo "Unknown platform: $PLATFORM"; exit 1 ;;
esac

# 安装逻辑...
```

**使用方式**：
```bash
bash scripts/install-skills.sh            # 默认安装到 Codex
bash scripts/install-skills.sh claude     # 安装到 Claude Code
bash scripts/install-skills.sh opencode   # 安装到 OpenCode
bash scripts/install-skills.sh openclaw   # 安装到 OpenCLAW
```

---

### 方案 2：一键全平台安装

新增 `scripts/install-skills-all.sh`：

```bash
#!/bin/bash
# 安装到所有平台

PLATFORMS=("codex" "claude" "opencode" "openclaw")

for platform in "${PLATFORMS[@]}"; do
  echo "Installing to $platform..."
  bash scripts/install-skills.sh "$platform"
done

echo "Done! Skills installed to all platforms."
```

---

### 方案 3：配置系统适配

修改 `acquire_source_text.py`，支持多平台配置：

```python
def read_platform_config(platform: str = "codex") -> dict:
    """读取指定平台的配置文件"""
    config_paths = {
        "codex": "~/.codex/config.toml",
        "claude": "~/.claude/settings.json",
        "opencode": "~/.config/opencode/config.json",
        "openclaw": "~/.openclaw/config.toml",
    }
    
    path = Path(config_paths.get(platform, config_paths["codex"])).expanduser()
    if not path.exists():
        return {}
    
    # 根据平台解析配置...
```

---

## 需要修改的文件

| 文件 | 修改内容 | 优先级 | 工作量 |
|------|---------|--------|--------|
| `scripts/install-skills.sh` | 支持多平台参数 | 高 | 1-2 小时 |
| `scripts/install-skills-all.sh` | 新增全平台安装脚本 | 中 | 1 小时 |
| `scripts/acquire_source_text.py` | 支持多平台配置读取 | 中 | 4-8 小时 |
| 所有 SKILL.md 的 description | 移除 "Codex-managed" 前缀 | 低 | 1-2 小时 |
| `docs/00-当前有效/skill-usage.md` | 添加多平台使用说明 | 低 | 2-4 小时 |

**总工作量**：1-2 天

---

## 实施步骤

### 阶段 1：最小可用（1-2 小时）

1. 修改 `install-skills.sh` 支持 `PLATFORM` 参数
2. 测试 `bash scripts/install-skills.sh claude`
3. 验证 Claude Code 能否正确加载 skill

### 阶段 2：完善支持（1 天）

1. 创建 `install-skills-all.sh` 一键安装脚本
2. 适配配置系统（`acquire_source_text.py`）
3. 更新 SKILL.md 的 description（移除 Codex 特定引用）

### 阶段 3：文档完善（1 天）

1. 创建 `docs/00-当前有效/cross-platform-support.md`
2. 更新 `skill-usage.md` 添加多平台使用说明
3. 更新 `README.md` 说明跨平台支持

---

## 验证方法

### 功能验证

```bash
# 1. 安装到 Claude Code
bash scripts/install-skills.sh claude

# 2. 在 Claude Code 中测试
# 打开 Claude Code，输入 /novel-init
# 验证 skill 能否正确加载和执行

# 3. 安装到 OpenCode
bash scripts/install-skills.sh opencode

# 4. 在 OpenCode 中测试
# 打开 OpenCode，使用 skill 工具调用 novel-init
```

### 回归验证

```bash
# 确保 Codex 功能不受影响
bash scripts/install-skills.sh codex
bash scripts/validate-migration.sh
pytest -q
```

---

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 配置格式不兼容 | 中 | 设计适配层，支持多种格式 |
| Skill 触发机制不同 | 低 | 各平台都支持 AgentSkills 标准 |
| 路径引用错误 | 低 | 使用相对路径或环境变量 |

---

## 结论

Genm-codex 的架构设计良好，核心逻辑与平台解耦充分。跨平台支持的主要工作是：
1. 修改安装脚本支持多平台路径（低风险）
2. 适配配置系统（可选，中等复杂度）
3. 更新文档（低风险）

这是一个低风险、高收益的改进，能显著扩大项目的适用范围。

---

## 最佳方案（待 codex 评判）

### 核心思路

**先做"能用"，再做"好用"，最后做"智能"**

### 推荐方案：方案 1 + 方案 2 组合

| 阶段 | 做什么 | 工作量 | 优先级 |
|------|--------|--------|--------|
| 1 | 修改 `install-skills.sh` 支持 PLATFORM 参数 | 30 分钟 | 必须 |
| 2 | 添加 `--all` 选项一键全平台安装 | 10 分钟 | 推荐 |
| 3 | 配置系统适配 | 4-8 小时 | 等有需求再做 |

### 最终形态

```bash
# 单平台安装
bash scripts/install-skills.sh claude
bash scripts/install-skills.sh opencode
bash scripts/install-skills.sh openclaw

# 全平台安装
bash scripts/install-skills.sh --all
```

### 具体改动

**`scripts/install-skills.sh`**（改 10 行）：
```bash
PLATFORM="${1:-codex}"

case "$PLATFORM" in
  codex)     TARGET_DIR="$HOME/.codex/skills" ;;
  claude)    TARGET_DIR="$HOME/.claude/skills" ;;
  opencode)  TARGET_DIR="$HOME/.config/opencode/skills" ;;
  openclaw)  TARGET_DIR="$HOME/.openclaw/skills" ;;
  --all)     # 遍历所有平台执行安装 ;;
  *)         echo "Unknown platform: $PLATFORM"; exit 1 ;;
esac
```

### 不做的事

- ❌ 不做配置格式转换（等有实际用户反馈）
- ❌ 不做 SKILL.md 内容适配（AgentSkills 格式已通用）
- ❌ 不做新平台检测（先支持已知 4 个平台）

### 做的事

- ✅ 改 install-skills.sh 加 PLATFORM 参数
- ✅ 加 --all 选项
- ✅ 改文档（skill-usage.md 加多平台说明）

### 总工作量

> 改 20 行 bash，支持 4 个平台，30 分钟搞定。

---

## 状态

- **当前状态**：`[planned]`
- **优先级**：中
- **预计工作量**：30 分钟（最佳方案）
- **前置依赖**：无

## 待 codex 评判

1. 方案是否合理？
2. 有没有遗漏的平台依赖？
3. `--all` 选项的实现方式是否最优？
