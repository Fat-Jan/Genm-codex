# 十章结构模板验证规则

## 🎯 验证目标

确保十章结构模板符合番茄平台要求，满足快节奏、高密度爽点、强钩子等核心标准。

## 📋 验证维度

### 1. 平台适配性验证

#### 番茄平台核心指标

```yaml
required_metrics:
  - cool_point_density: "≥1.5/千字"
  - hook_strength: "≥80分"
  - chapter_length: "2500-3200字"
  - golden_finger_appearance: "<800字"
  - opening_conflict: "<1000字"
```

#### 验证函数

```python
def validate_tomato_compliance(template):
    """验证模板是否符合番茄平台要求"""
    checks = {
        "cool_point_density": check_cool_points(template),
        "hook_strength": check_hook_quality(template),
        "pacing_consistency": check_pacing(template),
        "golden_three_rules": check_golden_three(template)
    }
    return all(checks.values())
```

### 2. 结构完整性验证

#### 章节结构检查

- ✅ 每章必须有明确的目标和目的
- ✅ 段落划分合理，字数分配均衡
- ✅ 包含必需的爽点类型
- ✅ 有合适的钩子结尾

#### 元素完整性检查

```yaml
required_elements_per_chapter:
  - section_purpose: "明确"
  - word_count_range: "200-1000字"
  - required_elements: "至少2个"
  - forbidden_elements: "无违规"
  - cool_points: "至少1个"
  - hook_type: "必须指定"
  - resistance_or_cost: "关键推进至少出现其一"
```

### 3. 内容质量验证

#### 爽点密度验证

```python
def calculate_cool_point_density(template):
    total_weight = 0
    total_words = 0

    for chapter in template.chapters:
        chapter_weight = sum(point.weight for point in chapter.cool_points)
        chapter_words = chapter.word_count
        total_weight += chapter_weight
        total_words += chapter_words

    density = total_weight / (total_words / 1000)
    return density >= 1.5  # 番茄标准要求
```

#### 钩子强度验证

- ✅ 每章必须有钩子
- ✅ 钩子强度≥80分
- ✅ 钩子类型正确（危机钩、悬念钩等）
- ✅ 钩子位置在章末

### 4. 平台约束验证

#### 番茄特有约束

```yaml
tomato_constraints:
  - golden_finger_visibility: "high/moderate"
  - combat_clarity: "extreme"
  - reward_immediacy: "required"
  - pacing_consistency: "strict"
  - hook_frequency: "每章必强钩子"
```

#### 违规检测

- ❌ 冗长世界观铺垫 >500字
- ❌ 无意义对话
- ❌ 主角软弱（连续2章无主动行为）
- ❌ 节奏拖沓（>800字无爽点）
- ❌ 慢热开局（>1000字无金手指）
- ❌ 关键证据自动上门
- ❌ 关键同盟一句话立刻成立
- ❌ 第三章结尾全赢无残留

## 🔧 验证工具

### 自动化验证脚本

```bash
# 验证模板文件
./validate-template.py tomato-xiuxian-vol1.yaml

# 批量验证所有模板
./validate-all-templates.sh

# 生成验证报告
./generate-validation-report.py --format=markdown
```

### 验证命令集成

```bash
# 集成到现有命令系统
/novel-template-validate --template=tomato-xiuxian-vol1

# 查看详细验证结果
/novel-template-check --chapter=1 --verbose
```

## 📊 评分标准

### 综合评分体系

| 维度 | 权重 | 满分 | 合格线 |
|------|------|------|--------|
| 平台适配度 | 30% | 100 | ≥80 |
| 结构完整性 | 25% | 100 | ≥85 |
| 爽点密度 | 20% | 100 | ≥90 |
| 钩子质量 | 15% | 100 | ≥80 |
| 内容创新 | 10% | 100 | ≥70 |

### 等级评定

- **A级** (90-100分): 优秀模板，可直接使用
- **B级** (80-89分): 良好模板，需微调
- **C级** (70-79分): 一般模板，需要重大修改
- **D级** (<70分): 不合格模板，重新设计

## 🛠️ 问题修复指南

### 常见问题及解决方案

#### 爽点密度不足

**问题**: 密度 < 1.5/千字
**解决方案**:

1. 增加爽点数量
2. 提高单个爽点权重
3. 调整章节长度分布

#### 钩子强度不够

**问题**: 钩子强度 < 80分
**解决方案**:

1. 增强悬念设置
2. 增加危机预告
3. 使用更强烈的钩子类型

#### 节奏拖沓

**问题**: 单场景 > 800字无变化
**解决方案**:

1. 拆分过长段落
2. 增加小高潮或转折点
3. 调整内容优先级

## 📈 持续优化

### 数据驱动改进

```python
# 收集用户反馈数据
feedback_data = {
    "completion_rate": "读者追读完成率",
    "hook_effectiveness": "钩子吸引力评分",
    "cool_point_satisfaction": "爽点满意度",
    "pacing_feedback": "节奏感受评价"
}

# 基于数据优化模板
def optimize_template_based_on_feedback(template, feedback):
    if feedback.completion_rate < 0.7:
        increase_hook_intensity(template)
    if feedback.cool_point_satisfaction < 0.8:
        add_more_cool_points(template)
```

### A/B测试框架

- 测试不同章节结构效果
- 对比各种爽点组合
- 评估钩子类型偏好
- 收集读者反馈迭代

## 🔄 版本控制

### 模板版本管理

```yaml
version_control:
  major_version: "v1.x"  # 重大结构调整
  minor_version: "v1.x-tomato"  # 平台特化
  patch_version: "v1.x-tomato.YYYYMMDD"  # 小更新
```

### 变更记录

- v1.0-tomato: 初始版本
- v1.1-tomato: 优化节奏控制
- v1.2-tomato: 增加爽点类型
- v1.3-tomato: 完善验证规则

## 📚 参考资源

### 相关文档

- `build/references/writing/anti-ai-style.md` - 去AI味道指南
- `build/bees/worker/platform-forbidden-bee.md` - 平台禁用规则
- `build/profiles/tomato.profile-tomato.yaml` - 番茄平台配置

### 外部标准

- 番茄平台用户偏好调研数据
- 网文市场趋势分析报告
- 读者阅读习惯研究

---

**最后更新**: 2026-03-18
**维护者**: Claude Code
**状态**: ✅ **验证规则文档完成**
