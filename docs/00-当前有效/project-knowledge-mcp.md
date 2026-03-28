# Project Knowledge MCP

## 目的

这份文档说明如何把项目本地的知识投影与质量审计，以 **read-only** 的方式挂接成 MCP server，供 agent 稳定读取。

它解决的问题不是“把 repo 再复制一份到外部知识库”，而是：

- 让 agent 有统一入口读取：
  - `.mighty/workflow-health.json`
  - `.mighty/knowledge-projection.json`
  - `.mighty/quality-audit.json`
- 让 workflow contract / sidecar health / quality artifact health 变成可调工具

## 边界

- 本 server 是 **read-only**
- 不直接写 `state.json`
- 不直接写 `设定集/`
- 不直接写任何 canon
- 不引入新的 runtime / scheduler / plugin framework

项目真值仍然是本地文件。

## 当前工具

当前 `project_knowledge_mcp_server.py` 暴露：

- `get_project_knowledge_projection`
- `get_project_quality_audit`
- `get_project_workflow_bundle`

其中：

- `get_project_knowledge_projection`
  - 返回 workflow contract、workflow_truth、sidecar health、story index 的紧凑投影
- `get_project_quality_audit`
  - 返回 review/close artifact 的假阳性审计结果
- `get_project_workflow_bundle`
  - 一次返回 workflow-health + projection + audit，适合 agent 少调一次

## 启动方式

本 server 走 stdio。

直接启动命令：

```bash
python3 /ABS/PATH/TO/Genm-codex/scripts/project_knowledge_mcp_server.py
```

如果你已经在仓库根目录：

```bash
python3 scripts/project_knowledge_mcp_server.py
```

## MCP 客户端挂接示例

可用一个标准 `mcpServers` 配置挂接：

```json
{
  "mcpServers": {
    "genm-project-knowledge": {
      "command": "python3",
      "args": [
        "/ABS/PATH/TO/Genm-codex/scripts/project_knowledge_mcp_server.py"
      ]
    }
  }
}
```

说明：

- 这里不要求 server 自己知道具体 project root
- `project_root` 作为 tool 参数传入
- 这样同一个 server 可以读多个项目，但仍保持本地文件是真值

## 推荐调用顺序

对 agent 来说，推荐优先级：

1. `get_project_workflow_bundle`
2. `get_project_knowledge_projection`
3. `get_project_quality_audit`

原因：

- bundle 先给最小全景
- projection 再给 workflow / sidecar 健康细节
- audit 再给 review artifact 假阳性细节

## 与 workflow 的关系

维护链已经会生成：

- `.mighty/workflow-health.json`
- `.mighty/quality-audit.json`
- `.mighty/knowledge-projection.json`

也就是说，这个 MCP server 不是现算真值，而是优先暴露 repo-owned sidecar。

这保证了：

- workflow 自己先能消费
- MCP 再暴露给 agent
- 不会出现“MCP 看到的东西”和 repo 里的 sidecar 不是同一层语义

## 后续增强方向

后续如果继续扩展，优先做：

- 更好的 bundle 字段裁剪
- 资源列表 / resources/read 兼容
- 针对 `novel-status` / `novel-query` 的标准 bundle 字段约定

不优先做：

- 直接暴露全文正文
- 直接暴露全量 `state.json`
- 让 MCP 变成写回真值层
