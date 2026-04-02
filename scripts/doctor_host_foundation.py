#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import jsonschema

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_host_capability_projection

MATRIX_SCHEMA_PATH = (
    REPO_ROOT / "shared" / "templates" / "host-capability-matrix-v1.schema.json"
)
LEDGER_SCHEMA_PATH = (
    REPO_ROOT / "shared" / "templates" / "host-evidence-ledger-v1.schema.json"
)
LEDGER_PATH = REPO_ROOT / "shared" / "templates" / "host-evidence-ledger-v1.json"
SKILL_USAGE_PATH = REPO_ROOT / "docs" / "00-当前有效" / "skill-usage.md"
HOST_SUPPORT_DOC_PATH = (
    REPO_ROOT / "docs" / "00-当前有效" / "host-support-status-v1.6.md"
)
INSTALL_START = "<!-- host-install-table:start -->"
INSTALL_END = "<!-- host-install-table:end -->"
SUPPORT_START = "<!-- host-support-table:start -->"
SUPPORT_END = "<!-- host-support-table:end -->"
DOC_SUMMARY_START = "<!-- host-support-summary:start -->"
DOC_SUMMARY_END = "<!-- host-support-summary:end -->"
DOC_DETAILS_START = "<!-- host-support-details:start -->"
DOC_DETAILS_END = "<!-- host-support-details:end -->"
CONTRACT_TEST_PATH = REPO_ROOT / "tests" / "test_state_contracts.py"
INSTALL_TEST_PATH = REPO_ROOT / "tests" / "test_install_skills_matrix.py"
SKILL_ALIAS_PLAN_TEST_PATH = REPO_ROOT / "tests" / "test_skill_alias_plan.py"
PROJECTION_TEST_PATH = REPO_ROOT / "tests" / "test_host_support_projection.py"
HOST_SUPPORT_DOC_TEST_PATH = REPO_ROOT / "tests" / "test_host_support_status_doc.py"
TRAE_REVIEW_DOC_TEST_PATH = REPO_ROOT / "tests" / "test_trae_capability_review_doc.py"


def get_matrix_path(*, respect_override: bool) -> Path:
    return render_host_capability_projection.get_matrix_path(
        allow_env_override=respect_override,
    )


def build_check_env(*, respect_override: bool) -> dict[str, str]:
    env = os.environ.copy()
    if not respect_override:
        env.pop(render_host_capability_projection.MATRIX_OVERRIDE_ENV, None)
    return env


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check repo-owned host foundation contracts."
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--respect-matrix-override",
        action="store_true",
        help="Use GENM_HOST_CAPABILITY_MATRIX_FILE for all checks instead of the repo matrix.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_block(content: str, start_marker: str, end_marker: str) -> str:
    start = content.index(start_marker) + len(start_marker)
    end = content.index(end_marker)
    return content[start:end].strip()


def run_pytest(
    test_path: Path,
    *pytest_args: str,
    env: dict[str, str] | None = None,
) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_path), *pytest_args, "-q"],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    detail = (proc.stdout or proc.stderr).strip()
    return proc.returncode == 0, detail


def check_matrix_schema(*, respect_override: bool) -> tuple[bool, str]:
    schema = read_json(MATRIX_SCHEMA_PATH)
    payload = read_json(get_matrix_path(respect_override=respect_override))
    jsonschema.validate(payload, schema)
    return True, "host capability matrix validates against schema"


def check_host_evidence_ledger(*, respect_override: bool) -> tuple[bool, str]:
    del respect_override
    schema = read_json(LEDGER_SCHEMA_PATH)
    payload = read_json(LEDGER_PATH)
    matrix = read_json(MATRIX_SCHEMA_PATH.parent / "host-capability-matrix-v1.json")
    jsonschema.validate(payload, schema)

    ledger_refs = {
        (entry["host_id"], entry["kind"], entry["ref"]) for entry in payload["entries"]
    }
    for host_id, row in matrix["hosts"].items():
        for evidence in row["evidence"]:
            key = (host_id, evidence["kind"], evidence["ref"])
            if key not in ledger_refs:
                return False, f"host evidence ledger missing matrix evidence {key}"
    for entry in payload["entries"]:
        if entry["kind"] == "repo_file" and not (REPO_ROOT / entry["ref"]).exists():
            return False, f"host evidence ledger repo file missing: {entry['ref']}"
    ok, detail = run_pytest(TRAE_REVIEW_DOC_TEST_PATH)
    return ok, detail or "host evidence ledger and Trae review doc tests passed"


def check_host_contract_semantics(*, respect_override: bool) -> tuple[bool, str]:
    ok, detail = run_pytest(
        CONTRACT_TEST_PATH,
        "-k",
        "host_capability_matrix",
        env=build_check_env(respect_override=respect_override),
    )
    return ok, detail or "host contract semantics tests passed"


def check_install_script_behavior(*, respect_override: bool) -> tuple[bool, str]:
    ok, detail = run_pytest(
        INSTALL_TEST_PATH,
        env=build_check_env(respect_override=respect_override),
    )
    return ok, detail or "install script behavior tests passed"


def check_skill_alias_plan(*, respect_override: bool) -> tuple[bool, str]:
    ok, detail = run_pytest(
        SKILL_ALIAS_PLAN_TEST_PATH,
        env=build_check_env(respect_override=respect_override),
    )
    return ok, detail or "skill alias/registry projection tests passed"


def check_skill_usage_projection(*, respect_override: bool) -> tuple[bool, str]:
    projection = render_host_capability_projection.build_projection(
        allow_env_override=respect_override,
    )
    content = SKILL_USAGE_PATH.read_text(encoding="utf-8")
    install_block = extract_block(content, INSTALL_START, INSTALL_END)
    support_block = extract_block(content, SUPPORT_START, SUPPORT_END)
    expected_install = render_host_capability_projection.render_install_table(
        projection
    )
    expected_support = render_host_capability_projection.render_support_table(
        projection
    )
    if install_block != expected_install:
        return False, "skill usage install table drift detected"
    if support_block != expected_support:
        return False, "skill usage support table drift detected"
    ok, detail = run_pytest(
        PROJECTION_TEST_PATH,
        env=build_check_env(respect_override=respect_override),
    )
    return ok, detail or "skill usage projection tests passed"


def check_host_support_document(*, respect_override: bool) -> tuple[bool, str]:
    projection = render_host_capability_projection.build_projection(
        allow_env_override=respect_override,
    )
    content = HOST_SUPPORT_DOC_PATH.read_text(encoding="utf-8")
    summary_block = extract_block(content, DOC_SUMMARY_START, DOC_SUMMARY_END)
    detail_block = extract_block(content, DOC_DETAILS_START, DOC_DETAILS_END)
    expected_summary = render_host_capability_projection.render_support_table(
        projection
    )
    expected_details = render_host_capability_projection.render_support_details(
        projection
    )
    if summary_block != expected_summary:
        return False, "host support status summary drift detected"
    if detail_block != expected_details:
        return False, "host support status detail drift detected"
    ok, detail = run_pytest(
        HOST_SUPPORT_DOC_TEST_PATH,
        env=build_check_env(respect_override=respect_override),
    )
    return ok, detail or "host support status doc tests passed"


def build_payload(*, respect_override: bool) -> dict:
    checks: list[dict[str, object]] = []
    for name, func in (
        ("matrix_schema", check_matrix_schema),
        ("host_evidence_ledger", check_host_evidence_ledger),
        ("host_contract_semantics", check_host_contract_semantics),
        ("install_script_behavior", check_install_script_behavior),
        ("skill_alias_plan", check_skill_alias_plan),
        ("skill_usage_projection", check_skill_usage_projection),
        ("host_support_document", check_host_support_document),
    ):
        try:
            ok, detail = func(respect_override=respect_override)
        except Exception as exc:  # noqa: BLE001
            ok = False
            detail = str(exc)
        checks.append({"name": name, "ok": ok, "detail": detail})
    return {
        "ok": all(item["ok"] for item in checks),
        "checks": checks,
    }


def main() -> None:
    args = parse_args()
    payload = build_payload(respect_override=args.respect_matrix_override)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if not payload["ok"]:
            raise SystemExit(1)
        return
    for item in payload["checks"]:
        status = "PASS" if item["ok"] else "FAIL"
        print(f"[{status}] {item['name']}: {item['detail']}")
    if not payload["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
