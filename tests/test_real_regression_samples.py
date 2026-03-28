import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "project_regression_smoke.py"
JIAZHUANGDAN_ROOT = REPO_ROOT / "projects" / "成婚前三日，我先改了侯府嫁妆单"


class RealRegressionSampleTests(unittest.TestCase):
    def test_jiazhuangdan_regression_sample_emits_expected_risks(self) -> None:
        self.assertTrue(SCRIPT_PATH.exists(), "scripts/project_regression_smoke.py is missing")
        self.assertTrue(JIAZHUANGDAN_ROOT.exists(), "regression sample project is missing")

        proc = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(JIAZHUANGDAN_ROOT), "--batch-count", "3"],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)

        quality_codes = {finding["code"] for finding in payload["quality_audit"]["findings"]}
        structure_codes = {finding["code"] for finding in payload["chapter_structure_audit"]["findings"]}
        batch_warning_codes = {warning["code"] for warning in payload["batch_quality_gate"]["warnings"]}

        self.assertEqual(payload["quality_audit"]["status"], "fail")
        self.assertEqual(payload["knowledge_projection"]["workflow_truth"]["status"], "pass")
        self.assertEqual(payload["knowledge_projection"]["workflow_contract"]["current_command"], "novel-batch")
        self.assertEqual(payload["chapter_structure_audit"]["status"], "warn")
        self.assertEqual(payload["batch_quality_gate"]["status"], "warn")

        for code in (
            "empty-issue-clusters-with-score",
            "missing-needs-fix-flag",
            "missing-dimension-scores",
            "missing-anti-flattening-artifacts",
            "empty-project-dimension-scores",
        ):
            self.assertIn(code, quality_codes)

        self.assertIn("repeated-conflict-opponent", structure_codes)
        self.assertIn("repeated-gain-ending", structure_codes)
        self.assertIn("near-floor-cluster", batch_warning_codes)


if __name__ == "__main__":
    unittest.main()
