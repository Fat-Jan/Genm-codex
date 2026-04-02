import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "doctor_host_foundation.py"
MATRIX_PATH = REPO_ROOT / "shared" / "templates" / "host-capability-matrix-v1.json"


def read_matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def write_matrix(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class HostFoundationDoctorTests(unittest.TestCase):
    def run_script(
        self,
        *args: str,
        matrix_path: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        if matrix_path is not None:
            env["GENM_HOST_CAPABILITY_MATRIX_FILE"] = str(matrix_path)
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

    def test_script_exists(self) -> None:
        self.assertTrue(
            SCRIPT_PATH.exists(), "scripts/doctor_host_foundation.py is missing"
        )

    def test_doctor_reports_host_foundation_status(self) -> None:
        proc = self.run_script("--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(
            [item["name"] for item in payload["checks"]],
            [
                "matrix_schema",
                "host_evidence_ledger",
                "host_contract_semantics",
                "install_script_behavior",
                "skill_alias_plan",
                "skill_usage_projection",
                "host_support_document",
            ],
        )
        self.assertTrue(all(item["ok"] for item in payload["checks"]))

    def test_doctor_ignores_invalid_matrix_override_by_default(self) -> None:
        payload = read_matrix()
        payload["hosts"]["codex"]["skill_install_root"] = None
        with tempfile.TemporaryDirectory() as tmpdir:
            matrix_path = Path(tmpdir) / "host-capability-matrix-v1.json"
            write_matrix(matrix_path, payload)
            proc = self.run_script("--json", matrix_path=matrix_path)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            self.assertTrue(report["ok"])
            self.assertTrue(all(item["ok"] for item in report["checks"]))

    def test_doctor_respects_invalid_matrix_override_when_flag_is_set(self) -> None:
        payload = read_matrix()
        payload["hosts"]["codex"]["skill_install_root"] = None
        with tempfile.TemporaryDirectory() as tmpdir:
            matrix_path = Path(tmpdir) / "host-capability-matrix-v1.json"
            write_matrix(matrix_path, payload)
            proc = self.run_script(
                "--json",
                "--respect-matrix-override",
                matrix_path=matrix_path,
            )
            self.assertNotEqual(proc.returncode, 0)
            report = json.loads(proc.stdout)
            checks = {item["name"]: item for item in report["checks"]}
            self.assertFalse(report["ok"])
            self.assertFalse(checks["matrix_schema"]["ok"])
            self.assertFalse(checks["install_script_behavior"]["ok"])

    def test_doctor_contract_checks_only_consume_override_with_explicit_flag(
        self,
    ) -> None:
        payload = read_matrix()
        payload["hosts"]["trae"]["supports_mcp"] = "verified"
        with tempfile.TemporaryDirectory() as tmpdir:
            matrix_path = Path(tmpdir) / "host-capability-matrix-v1.json"
            write_matrix(matrix_path, payload)

            default_proc = self.run_script("--json", matrix_path=matrix_path)
            self.assertEqual(default_proc.returncode, 0, default_proc.stderr)
            default_report = json.loads(default_proc.stdout)
            default_checks = {item["name"]: item for item in default_report["checks"]}
            self.assertTrue(default_report["ok"])
            self.assertTrue(default_checks["host_contract_semantics"]["ok"])
            self.assertTrue(default_checks["skill_usage_projection"]["ok"])

            override_proc = self.run_script(
                "--json",
                "--respect-matrix-override",
                matrix_path=matrix_path,
            )
            self.assertNotEqual(override_proc.returncode, 0)
            override_report = json.loads(override_proc.stdout)
            override_checks = {
                item["name"]: item for item in override_report["checks"]
            }
            self.assertFalse(override_report["ok"])
            self.assertTrue(override_checks["host_evidence_ledger"]["ok"])
            self.assertFalse(override_checks["host_contract_semantics"]["ok"])
            self.assertTrue(override_checks["skill_usage_projection"]["ok"])
            self.assertFalse(override_checks["host_support_document"]["ok"])
            self.assertEqual(read_matrix()["hosts"]["trae"]["supports_mcp"], "partial")


if __name__ == "__main__":
    unittest.main()
