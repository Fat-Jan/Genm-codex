import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "project_regression_smoke.py"
E2E_NOVEL_ROOT = REPO_ROOT / "e2e-novel"


class RealE2ENovelSmokeTests(unittest.TestCase):
    def test_e2e_novel_regression_smoke_emits_expected_summary(self) -> None:
        self.assertTrue(SCRIPT_PATH.exists(), "scripts/project_regression_smoke.py is missing")
        self.assertTrue(E2E_NOVEL_ROOT.exists(), "e2e-novel sample is missing")

        proc = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(E2E_NOVEL_ROOT), "--batch-count", "3"],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)

        quality_codes = {finding["code"] for finding in payload["quality_audit"]["findings"]}
        structure_codes = {finding["code"] for finding in payload["chapter_structure_audit"]["findings"]}
        batch_issue_codes = {issue["code"] for issue in payload["batch_quality_gate"]["issues"]}

        self.assertEqual(payload["project"], str(E2E_NOVEL_ROOT))
        self.assertEqual(payload["quality_audit"]["status"], "warn")
        self.assertEqual(payload["workflow_health"]["quality_audit_status"], "warn")
        self.assertEqual(payload["workflow_health"]["recommended_next_action"], "repair-review-artifacts")
        self.assertEqual(payload["chapter_structure_audit"]["status"], "warn")
        self.assertEqual(payload["batch_quality_gate"]["status"], "fail")

        self.assertIn("missing-route-decision", quality_codes)
        self.assertIn("missing-anti-flattening-artifacts", quality_codes)
        self.assertIn("repeated-conflict-opponent", structure_codes)
        self.assertIn("repeated-gain-ending", structure_codes)
        self.assertIn("malformed-repeated-token", batch_issue_codes)


if __name__ == "__main__":
    unittest.main()
