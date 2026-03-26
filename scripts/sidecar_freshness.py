from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def registry_path(repo_root: Path) -> Path:
    return repo_root / "shared" / "templates" / "sidecar-freshness-registry-v1.json"


def load_registry(repo_root: Path) -> dict[str, Any]:
    return json.loads(registry_path(repo_root).read_text(encoding="utf-8"))


def build_freshness(
    *,
    repo_root: Path,
    artifact_key: str,
    timestamp: str,
    inputs: dict[str, Any],
    project_root: Path | None = None,
) -> dict[str, Any]:
    registry = load_registry(repo_root)
    artifact = registry.get("artifacts", {}).get(artifact_key, {})
    return {
        "contract": registry.get("contract", "sidecar-freshness-v1"),
        "artifact_key": artifact_key,
        "generated_at": timestamp,
        "generated_by": artifact.get("produced_by", ""),
        "registry_file": str(registry_path(repo_root)),
        "project_root": str(project_root) if project_root is not None else None,
        "depends_on": artifact.get("depends_on", []),
        "inputs": inputs,
    }
