from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def trace_log_path(project_root: Path) -> Path:
    return project_root / ".mighty" / "logs" / "trace.jsonl"


def append_trace(
    project_root: Path,
    *,
    event: str,
    skill: str,
    result: str,
    details: dict[str, Any] | None = None,
    error: str | None = None,
    timestamp: str | None = None,
) -> Path:
    path = trace_log_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ts": timestamp or now_iso(),
        "event": event,
        "skill": skill,
        "result": result,
    }
    if details:
        payload["details"] = details
    if error:
        payload["error"] = error
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return path
