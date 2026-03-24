# Compiler Contract

## 目标

把 `premise / pivot / launch grammar / retention protocol` 编译成下游 skill 可以直接消费的最小输入。

## 运行时对象

统一对象名：

- `launch_stack`

建议形态：

```json
{
  "version": "1.0",
  "phase": "preselect|locked|drift-monitor|reselected",
  "premise_line": "",
  "primary_pivot": "",
  "secondary_pivot": "",
  "launch_grammar": {
    "primary": "",
    "candidates": [],
    "confidence": "medium"
  },
  "retention_protocol": {
    "enabled_rules": [],
    "priority_rules": [],
    "violations": []
  },
  "compiler_output": {
    "outline_focus": [],
    "chapter_1_3_targets": [],
    "review_watchpoints": [],
    "precheck_risks": [],
    "package_guardrails": []
  },
  "confidence": "medium",
  "drift_signal": "none",
  "reselect_note": ""
}
```

## 固定 compiler 输出

第一版固定产出：

- `outline_focus`
- `chapter_1_3_targets`
- `review_watchpoints`
- `precheck_risks`
- `package_guardrails`

## sidecar 与 state

详细结果：

- `.mighty/launch-stack.json`

预留账本：

- `.mighty/hook-ledger.json`
- `.mighty/payoff-ledger.json`

`state.json` 只镜像：

- `active_launch_grammar`
- `active_primary_pivot`
- `launch_stack_phase`
- `launch_stack_drift_signal`

## 第一版原则

- compiler 只做保守编译，不做黑盒 orchestrator
- 低置信度时允许保留候选，不硬装高确定性
- 不把长推理写进 state
