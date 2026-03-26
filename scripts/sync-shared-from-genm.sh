#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ROOT="${GENM_CODEX_SHARED_TARGET_ROOT:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
SOURCE_ROOT="${GENM_SHARED_SOURCE_ROOT:-$(cd "${SCRIPT_DIR}/../../Genm" && pwd)}"
GOVERNANCE_FILE="${GENM_SHARED_GOVERNANCE_FILE:-${TARGET_ROOT}/shared/sync-governance.json}"
export GENM_SYNC_TARGET_ROOT="${TARGET_ROOT}"
export GENM_SYNC_SOURCE_ROOT="${SOURCE_ROOT}"
export GENM_SYNC_GOVERNANCE_FILE="${GOVERNANCE_FILE}"

exec python3 - "$@" <<'PY'
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path


TARGET_ROOT = Path(os.environ["GENM_SYNC_TARGET_ROOT"]).resolve()
SOURCE_ROOT = Path(os.environ["GENM_SYNC_SOURCE_ROOT"]).resolve()
GOVERNANCE_FILE = Path(os.environ["GENM_SYNC_GOVERNANCE_FILE"]).resolve()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sync-shared-from-genm.sh",
        description="Sync shared assets from Genm with governance-aware drift reporting.",
    )
    parser.add_argument("--report", action="store_true", help="Show text report only")
    parser.add_argument("--report-json", action="store_true", help="Show JSON report only")
    parser.add_argument(
        "--allow-drift-overwrite",
        action="store_true",
        help="Allow same-path drift files to be overwritten after explicit review",
    )
    parser.add_argument(
        "--domain",
        action="append",
        choices=("profiles", "references", "templates"),
        help="Limit to one or more domains",
    )
    return parser.parse_args(argv)


def resolve_source_dir(domain: str) -> Path:
    mapping = {
        "profiles": SOURCE_ROOT / "build" / "profiles",
        "references": SOURCE_ROOT / "build" / "references",
        "templates": SOURCE_ROOT / "build" / "templates",
    }
    return mapping[domain]


def resolve_target_dir(domain: str) -> Path:
    mapping = {
        "profiles": TARGET_ROOT / "shared" / "profiles",
        "references": TARGET_ROOT / "shared" / "references",
        "templates": TARGET_ROOT / "shared" / "templates",
    }
    return mapping[domain]


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def count_dirs(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_dir())


def list_relative_files(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        str(item.relative_to(path)).replace("\\", "/")
        for item in path.rglob("*")
        if item.is_file()
    }


def read_governance() -> dict:
    if not GOVERNANCE_FILE.exists():
        raise SystemExit(f"Missing governance file: {GOVERNANCE_FILE}")
    return json.loads(GOVERNANCE_FILE.read_text(encoding="utf-8"))


def snapshot_domain(domain: str, governance: dict) -> dict:
    source_dir = resolve_source_dir(domain)
    target_dir = resolve_target_dir(domain)
    if not source_dir.exists():
        raise SystemExit(f"Missing source directory: {source_dir}")

    protected = governance.get("domains", {}).get(domain, {}).get("protected_local_paths", [])
    protected_set = set(protected)
    source_files = list_relative_files(source_dir)
    target_files = list_relative_files(target_dir)
    local_only = sorted(target_files - source_files)
    source_only = sorted(source_files - target_files)
    shared_paths = sorted(source_files & target_files)
    drift = sorted(
        rel
        for rel in shared_paths
        if (target_dir / rel).read_bytes() != (source_dir / rel).read_bytes()
    )
    unexpected_local_only = sorted(rel for rel in local_only if rel not in protected_set)

    return {
        "domain": domain,
        "source": str(source_dir),
        "target": str(target_dir),
        "source_files": count_files(source_dir),
        "source_subdirs": count_dirs(source_dir),
        "target_status": "present" if target_dir.exists() else "missing",
        "target_files": count_files(target_dir),
        "target_subdirs": count_dirs(target_dir),
        "protected_local_paths": protected,
        "local_only_paths": local_only,
        "unexpected_local_only_paths": unexpected_local_only,
        "drift_paths": drift,
        "source_only_paths": source_only,
    }


def print_text_report(domains: list[str], governance: dict, allow_drift_overwrite: bool) -> None:
    print("# Shared Sync Report")
    print(f"- source root: {SOURCE_ROOT}")
    print(f"- target root: {TARGET_ROOT / 'shared'}")
    print(f"- governance file: {GOVERNANCE_FILE}")
    print(f"- same-path drift policy: {'allow overwrite by explicit flag' if allow_drift_overwrite else 'block unless --allow-drift-overwrite'}")
    for domain in domains:
        data = snapshot_domain(domain, governance)
        print(f"## {domain}")
        print(f"- source: {data['source']}")
        print(f"- target: {data['target']}")
        print(f"- source files: {data['source_files']}")
        print(f"- source subdirs: {data['source_subdirs']}")
        print(f"- target status: {data['target_status']}")
        print(f"- target files: {data['target_files']}")
        print(f"- target subdirs: {data['target_subdirs']}")
        print(f"- protected local paths: {len(data['protected_local_paths'])}")
        print(f"- local-only paths: {len(data['local_only_paths'])}")
        print(f"- same-path drift paths: {len(data['drift_paths'])}")
        print(f"- source-only paths: {len(data['source_only_paths'])}")
        if data["unexpected_local_only_paths"]:
            print(f"- unexpected local-only paths: {len(data['unexpected_local_only_paths'])}")
        if data["local_only_paths"]:
            print(f"- local-only list: {' '.join(data['local_only_paths'])}")
        if data["drift_paths"]:
            print(f"- drift list: {' '.join(data['drift_paths'])}")


def print_json_report(domains: list[str], governance: dict, allow_drift_overwrite: bool) -> None:
    payload = {
        "source_root": str(SOURCE_ROOT),
        "target_root": str(TARGET_ROOT / "shared"),
        "governance_file": str(GOVERNANCE_FILE),
        "allow_drift_overwrite": allow_drift_overwrite,
        "domains": [snapshot_domain(domain, governance) for domain in domains],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def sync_domain(domain: str, governance: dict, allow_drift_overwrite: bool) -> None:
    snapshot = snapshot_domain(domain, governance)
    if snapshot["unexpected_local_only_paths"]:
        paths = "\n".join(f"  - {path}" for path in snapshot["unexpected_local_only_paths"])
        raise SystemExit(
            f"Refusing sync for {domain}: found unexpected local-only paths not declared in {GOVERNANCE_FILE}\n{paths}"
        )
    if snapshot["drift_paths"] and not allow_drift_overwrite:
        paths = "\n".join(f"  - {path}" for path in snapshot["drift_paths"])
        raise SystemExit(
            f"Refusing sync for {domain}: same-path drift would be overwritten. Re-run with --allow-drift-overwrite only after review.\n{paths}"
        )

    source_dir = Path(snapshot["source"])
    target_dir = Path(snapshot["target"])
    protected_paths = snapshot["protected_local_paths"]

    with tempfile.TemporaryDirectory() as tempdir:
        staged_target = Path(tempdir) / domain
        shutil.copytree(source_dir, staged_target)
        for rel in protected_paths:
            original = target_dir / rel
            if original.exists():
                destination = staged_target / rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original, destination)

        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(staged_target), str(target_dir))


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    domains = args.domain or ["profiles", "references", "templates"]
    governance = read_governance()

    if args.report_json:
        print_json_report(domains, governance, args.allow_drift_overwrite)
        return 0

    if args.report:
        print_text_report(domains, governance, args.allow_drift_overwrite)
        return 0

    for domain in domains:
        sync_domain(domain, governance, args.allow_drift_overwrite)

    print(
        f"Synced shared assets from {SOURCE_ROOT} to {TARGET_ROOT / 'shared'} using governance {GOVERNANCE_FILE}"
    )
    return 0


raise SystemExit(main(sys.argv[1:]))
PY
