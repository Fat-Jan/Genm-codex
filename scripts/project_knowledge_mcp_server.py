#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_project_quality_state
import build_project_knowledge_projection
import build_workflow_health_bundle
import render_project_status_dashboard
import render_project_scan_summary
import render_workflow_health_summary


SERVER_INFO = {
    "name": "genm-project-knowledge",
    "version": "0.1.0",
}


def tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": "get_project_knowledge_projection",
            "description": "Read the compact repo-owned knowledge projection for a project.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
                "required": ["project_root"],
            },
        },
        {
            "name": "get_project_quality_audit",
            "description": "Audit review/close artifacts for false-positive quality signals.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
                "required": ["project_root"],
            },
        },
        {
            "name": "get_project_workflow_bundle",
            "description": "Read one compact bundle containing knowledge projection and quality audit for a project.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
                "required": ["project_root"],
            },
        },
        {
            "name": "get_project_workflow_health_summary",
            "description": "Render a compact Markdown workflow-health summary for direct display.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
                "required": ["project_root"],
            },
        },
        {
            "name": "get_project_status_dashboard",
            "description": "Render a compact project status dashboard for direct display.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
                "required": ["project_root"],
            },
        },
        {
            "name": "get_project_scan_summary",
            "description": "Render a compact project scan summary for direct display.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_root": {"type": "string"},
                },
                "required": ["project_root"],
            },
        },
    ]


def _success_response(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result,
    }


def _error_response(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message,
        },
    }


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    project_root = arguments.get("project_root")
    if not isinstance(project_root, str) or not project_root:
        raise ValueError("project_root is required")

    root = Path(project_root)
    if name == "get_project_knowledge_projection":
        payload = build_project_knowledge_projection.build_project_knowledge_projection(
            root,
            timestamp=build_project_knowledge_projection.now_iso(),
        )
    elif name == "get_project_quality_audit":
        payload = audit_project_quality_state.audit_project_quality_state(root)
    elif name == "get_project_workflow_bundle":
        projection = build_project_knowledge_projection.build_project_knowledge_projection(
            root,
            timestamp=build_project_knowledge_projection.now_iso(),
        )
        audit = audit_project_quality_state.audit_project_quality_state(root)
        workflow_health = build_workflow_health_bundle.build_workflow_health_bundle(
            root,
            timestamp=build_workflow_health_bundle.now_iso(),
        )
        payload = {
            "project_root": str(root),
            "knowledge_projection": projection,
            "quality_audit": audit,
            "workflow_health": workflow_health,
            "bundle_contract": {
                "read_only": True,
                "truth_source": "local_files",
            },
        }
    elif name == "get_project_workflow_health_summary":
        payload = render_workflow_health_summary.render_workflow_health_markdown(root)
    elif name == "get_project_status_dashboard":
        payload = render_project_status_dashboard.render_project_status_dashboard_markdown(root)
    elif name == "get_project_scan_summary":
        payload = render_project_scan_summary.render_project_scan_summary_markdown(root)
    else:
        raise ValueError(f"unknown tool: {name}")

    return {
        "content": [
            {
                "type": "text",
                "text": payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=2),
            }
        ],
        "isError": False,
    }


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    request_id = request.get("id")

    if method == "initialize":
        return _success_response(
            request_id,
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                },
                "serverInfo": SERVER_INFO,
            },
        )

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return _success_response(request_id, {"tools": tool_definitions()})

    if method == "tools/call":
        params = request.get("params", {})
        try:
            result = call_tool(params.get("name", ""), params.get("arguments", {}))
        except Exception as exc:  # pragma: no cover - exercised through error response path
            return _error_response(request_id, -32000, str(exc))
        return _success_response(request_id, result)

    return _error_response(request_id, -32601, f"Method not found: {method}")


def _read_message() -> dict[str, Any] | None:
    content_length = None
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, _, value = line.decode("utf-8").partition(":")
        if key.lower() == "content-length":
            content_length = int(value.strip())

    if content_length is None:
        return None

    body = sys.stdin.buffer.read(content_length)
    if not body:
        return None
    return json.loads(body.decode("utf-8"))


def _write_message(payload: dict[str, Any]) -> None:
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(encoded)}\r\n\r\n".encode("utf-8"))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def main() -> None:
    while True:
        request = _read_message()
        if request is None:
            break
        response = handle_request(request)
        if response is not None:
            _write_message(response)


if __name__ == "__main__":
    main()
