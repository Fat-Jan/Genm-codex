#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tomllib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from trace_log import append_trace


DEFAULT_CONFIG_PATH = Path.home() / ".codex" / "config.toml"
REPORT_PATH = Path(".mighty") / "memory-sync-report.json"
STORE_TOOL_NAME = "openmemory_store"
LOCAL_BRIDGE_PATH = SCRIPT_DIR / "openmemory_store_bridge.js"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_project_config(project_root: Path) -> dict[str, Any]:
    payload = read_json(project_root / ".mighty" / "config.json")
    return payload if isinstance(payload, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync safe project memory context into OpenMemory via MCP.")
    parser.add_argument("project_root", help="Novel project root")
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--mode", choices=["auto", "on", "off"], default=os.environ.get("GENM_OPENMEMORY_SYNC", "auto"))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--user-id", default="")
    parser.add_argument("--config-path", default=str(DEFAULT_CONFIG_PATH))
    return parser.parse_args(argv)


def load_openmemory_client_config(config_path: Path) -> dict[str, Any] | None:
    if not config_path.exists():
        return None
    payload = tomllib.loads(config_path.read_text(encoding="utf-8"))
    mcp_servers = payload.get("mcp_servers", {})
    if not isinstance(mcp_servers, dict):
        return None
    openmemory = mcp_servers.get("openmemory")
    if not isinstance(openmemory, dict):
        return None
    command = openmemory.get("command")
    args = openmemory.get("args", [])
    env = openmemory.get("env", {})
    if not isinstance(command, str) or not command:
        return None
    if not isinstance(args, list) or not all(isinstance(item, str) for item in args):
        return None
    if not isinstance(env, dict):
        return None
    env_payload = {str(key): str(value) for key, value in env.items()}
    return {
        "command": command,
        "args": args,
        "env": env_payload,
        "config_path": str(config_path),
    }


def resolve_openmemory_js_root(client_config: dict[str, Any]) -> str:
    explicit = client_config.get("env", {}).get("OPENMEMORY_JS_ROOT")
    if explicit:
        return explicit
    command = str(client_config.get("command") or "")
    resolved = shutil.which(command) if command else None
    if not resolved:
        raise RuntimeError("Unable to resolve openmemory command path")
    command_path = Path(resolved).resolve()
    if command_path.name == "opm.js":
        return str(command_path.parents[1])
    guessed = command_path.parent.parent / "lib" / "node_modules" / "openmemory-js"
    if guessed.exists():
        return str(guessed)
    raise RuntimeError(f"Unable to resolve OPENMEMORY_JS_ROOT from {command_path}")


def encode_message(payload: dict[str, Any]) -> bytes:
    encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return f"Content-Length: {len(encoded)}\r\n\r\n".encode("utf-8") + encoded


def decode_messages(raw: bytes) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []
    cursor = 0
    total = len(raw)
    while cursor < total:
        header_end = raw.find(b"\r\n\r\n", cursor)
        delimiter_len = 4
        if header_end == -1:
            header_end = raw.find(b"\n\n", cursor)
            delimiter_len = 2
        if header_end == -1:
            break
        header_blob = raw[cursor:header_end].decode("utf-8")
        content_length = None
        for line in header_blob.splitlines():
            key, _, value = line.partition(":")
            if key.lower() == "content-length":
                content_length = int(value.strip())
                break
        if content_length is None:
            raise RuntimeError("MCP response missing Content-Length header")
        body_start = header_end + delimiter_len
        body_end = body_start + content_length
        if body_end > total:
            raise RuntimeError("MCP response body truncated")
        messages.append(json.loads(raw[body_start:body_end].decode("utf-8")))
        cursor = body_end
    return messages


def run_local_store_call(client_config: dict[str, Any], arguments: dict[str, Any]) -> dict[str, Any]:
    env = os.environ.copy()
    env.update(client_config.get("env", {}))
    env["OPENMEMORY_JS_ROOT"] = resolve_openmemory_js_root(client_config)
    proc = subprocess.run(
        ["node", str(LOCAL_BRIDGE_PATH)],
        input=json.dumps(arguments, ensure_ascii=False),
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    payload = json.loads(proc.stdout.strip())
    return {
        "transport": "local-node",
        "result": payload,
    }


def run_mcp_store_call(client_config: dict[str, Any], arguments: dict[str, Any]) -> dict[str, Any]:
    command = [client_config["command"], *client_config.get("args", [])]
    env = os.environ.copy()
    env.update(client_config.get("env", {}))
    stream = b"".join([
        encode_message(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "genm-codex-memory-sync",
                        "version": "0.1.0",
                    },
                },
            }
        ),
        encode_message(
            {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            }
        ),
        encode_message(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": STORE_TOOL_NAME,
                    "arguments": arguments,
                },
            }
        ),
    ])
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    stdout = b""
    stderr = b""
    try:
        stdout, stderr = proc.communicate(input=stream, timeout=10)
    except subprocess.TimeoutExpired as exc:
        proc.kill()
        remaining_stdout, remaining_stderr = proc.communicate()
        stdout = (exc.stdout or b"") + (remaining_stdout or b"")
        stderr = (exc.stderr or b"") + (remaining_stderr or b"")
    if proc.returncode not in (0, None):
        stderr_text = stderr.decode("utf-8", errors="replace").strip()
        if not stdout:
            raise RuntimeError(stderr_text or f"openmemory MCP exited with code {proc.returncode}")
    messages = decode_messages(stdout)
    for message in messages:
        if message.get("id") == 2:
            if "error" in message:
                error = message["error"]
                raise RuntimeError(str(error.get("message", "openmemory_store call failed")))
            return message["result"]
    stderr_text = stderr.decode("utf-8", errors="replace").strip()
    raise RuntimeError(stderr_text or "Missing tools/call response from openmemory MCP server")


def build_project_key(project_root: Path) -> str:
    return hashlib.sha1(str(project_root).encode("utf-8")).hexdigest()[:12]


def build_sync_payload(memory_context: dict[str, Any], project_root: Path, *, user_id: str) -> dict[str, Any]:
    project_key = build_project_key(project_root)
    normalized = {
        "schema": "genm-memory-sync-v1",
        "project_root": str(project_root),
        "project_key": project_key,
        "generated_at": memory_context.get("generated_at", ""),
        "title": memory_context.get("title", ""),
        "current_chapter": memory_context.get("current_chapter", 0),
        "total_words": memory_context.get("total_words", 0),
        "workflow": memory_context.get("workflow", {}),
        "gate": memory_context.get("gate", {}),
        "launch_stack": memory_context.get("launch_stack", {}),
        "active_context_summary": memory_context.get("active_context_summary", {}),
        "memory_contract": memory_context.get("memory_contract", {}),
        "freshness": memory_context.get("freshness", {}),
    }
    content_hash = hashlib.sha256(
        json.dumps(normalized, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    summary = (
        f"Project {normalized['title'] or project_root.name} "
        f"(key={project_key}) at {normalized['project_root']}: "
        f"chapter={normalized['current_chapter']}, words={normalized['total_words']}, "
        f"workflow={normalized['workflow'].get('status')}/{normalized['workflow'].get('last_successful_checkpoint')}, "
        f"gate={normalized['gate'].get('status')}, "
        f"next_action={normalized['gate'].get('minimal_next_action')}, "
        f"launch_stack={normalized['launch_stack'].get('phase')}/{normalized['launch_stack'].get('drift_signal')}, "
        f"hooks={normalized['active_context_summary'].get('hook_count')}, "
        f"guardrails={normalized['active_context_summary'].get('guardrail_count')}, "
        f"latest_summary_chapter={normalized['active_context_summary'].get('latest_summary_chapter')}, "
        f"generated_at={normalized['generated_at']}."
    )
    return {
        "content": summary,
        "content_hash": content_hash,
        "metadata": {
            **normalized,
            "source": "genm-codex",
            "artifact_key": "memory-context",
            "content_hash": content_hash,
        },
        "tags": [
            "genm-codex",
            "memory-context",
            f"project-key:{project_key}",
        ],
        "user_id": user_id,
    }


def extract_memory_id(store_result: dict[str, Any]) -> str | None:
    if isinstance(store_result.get("result"), dict) and isinstance(store_result["result"].get("id"), str):
        return store_result["result"]["id"]
    content = store_result.get("content", [])
    if not isinstance(content, list):
        return None
    for item in content:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if not isinstance(text, str):
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        hsg = payload.get("hsg")
        if isinstance(hsg, dict) and isinstance(hsg.get("id"), str):
            return hsg["id"]
    return None


def write_report(project_root: Path, payload: dict[str, Any]) -> Path:
    report_path = project_root / REPORT_PATH
    write_json(report_path, payload)
    return report_path


def run_store_call(client_config: dict[str, Any], arguments: dict[str, Any]) -> dict[str, Any]:
    local_error: Exception | None = None
    if LOCAL_BRIDGE_PATH.exists():
        try:
            return run_local_store_call(client_config, arguments)
        except Exception as exc:
            local_error = exc
    try:
        result = run_mcp_store_call(client_config, arguments)
        result["transport"] = "mcp-stdio"
        return result
    except Exception as exc:
        if local_error is not None:
            raise RuntimeError(f"local bridge failed: {local_error}; mcp fallback failed: {exc}") from exc
        raise


def sync_memory_context(
    project_root: Path,
    *,
    timestamp: str,
    mode: str,
    user_id: str,
    config_path: Path,
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    memory_context_path = project_root / ".mighty" / "memory-context.json"
    report_path = project_root / REPORT_PATH
    project_config_path = project_root / ".mighty" / "config.json"
    project_config = read_project_config(project_root)
    memory_sync = project_config.get("memory_sync", {})
    openmemory_sync = memory_sync.get("openmemory", {}) if isinstance(memory_sync, dict) else {}
    base_report = {
        "version": "1.0",
        "run_at": timestamp,
        "project_root": str(project_root),
        "source_file": str(memory_context_path),
        "report_file": str(report_path),
        "project_config_file": str(project_config_path),
        "mode": mode,
        "target": "openmemory-mcp",
        "user_id": user_id,
    }
    if mode == "off":
        return {**base_report, "status": "skipped", "reason": "sync-disabled"}
    if mode == "auto" and not bool(openmemory_sync.get("enabled")):
        return {**base_report, "status": "skipped", "reason": "project-sync-disabled"}
    if not memory_context_path.exists():
        return {**base_report, "status": "skipped", "reason": "memory-context-missing"}

    memory_context = read_json(memory_context_path)
    if not memory_context.get("safe_for_mcp_memory"):
        return {**base_report, "status": "skipped", "reason": "unsafe-memory-context"}

    sync_payload = build_sync_payload(memory_context, project_root, user_id=user_id)
    previous_report = read_json(report_path)
    if not force and previous_report.get("content_hash") == sync_payload["content_hash"]:
        return {
            **base_report,
            "status": "skipped",
            "reason": "content-unchanged",
            "content_hash": sync_payload["content_hash"],
            "memory_id": previous_report.get("memory_id"),
        }

    client_config = load_openmemory_client_config(config_path)
    if client_config is None:
        if mode == "auto":
            return {
                **base_report,
                "status": "skipped",
                "reason": "openmemory-not-configured",
                "content_hash": sync_payload["content_hash"],
                "config_path": str(config_path),
            }
        client_config = {
            "command": "opm",
            "args": ["mcp"],
            "env": {},
            "config_path": str(config_path),
        }

    if dry_run:
        return {
            **base_report,
            "status": "dry-run",
            "content_hash": sync_payload["content_hash"],
            "summary_preview": sync_payload["content"],
            "config_path": client_config["config_path"],
        }

    store_result = run_store_call(
        client_config,
        {
            "content": sync_payload["content"],
            "metadata": sync_payload["metadata"],
            "tags": sync_payload["tags"],
            "type": "contextual",
            "user_id": user_id,
        },
    )
    return {
        **base_report,
        "status": "stored",
        "content_hash": sync_payload["content_hash"],
        "memory_id": extract_memory_id(store_result),
        "config_path": client_config["config_path"],
        "command": [client_config["command"], *client_config.get("args", [])] if store_result.get("transport") == "mcp-stdio" else ["node", str(LOCAL_BRIDGE_PATH)],
        "store_transport": store_result.get("transport"),
        "store_result": store_result,
    }


def main(argv: list[str] | None = None) -> dict[str, Any]:
    args = parse_args(argv)
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    project_config = read_project_config(root)
    memory_sync = project_config.get("memory_sync", {})
    openmemory_sync = memory_sync.get("openmemory", {}) if isinstance(memory_sync, dict) else {}
    resolved_user_id = (
        args.user_id
        or str(openmemory_sync.get("user_id") or "")
        or os.environ.get("GENM_OPENMEMORY_USER_ID", "genm-codex")
    )
    try:
        result = sync_memory_context(
            root,
            timestamp=ts,
            mode=args.mode,
            user_id=resolved_user_id,
            config_path=Path(args.config_path).expanduser(),
            force=args.force,
            dry_run=args.dry_run,
        )
        report_path = write_report(root, result)
        append_trace(
            root,
            event="memory_sync.completed",
            skill="sync_memory_context_to_openmemory",
            result=result["status"],
            details={
                "report_file": str(report_path),
                "reason": result.get("reason"),
                "memory_id": result.get("memory_id"),
            },
            timestamp=ts,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    except Exception as exc:
        failure = {
            "version": "1.0",
            "run_at": ts,
            "project_root": str(root),
            "source_file": str(root / ".mighty" / "memory-context.json"),
            "report_file": str(root / REPORT_PATH),
            "project_config_file": str(root / ".mighty" / "config.json"),
            "mode": args.mode,
            "target": "openmemory-mcp",
            "user_id": resolved_user_id,
            "status": "failed",
            "error": str(exc),
        }
        report_path = write_report(root, failure)
        append_trace(
            root,
            event="memory_sync.completed",
            skill="sync_memory_context_to_openmemory",
            result="failed",
            details={"report_file": str(report_path)},
            error=str(exc),
            timestamp=ts,
        )
        print(json.dumps(failure, ensure_ascii=False, indent=2))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
