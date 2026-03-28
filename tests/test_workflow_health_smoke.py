import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "workflow_health_smoke.py"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class WorkflowHealthSmokeTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        mighty = root / ".mighty"
        mighty.mkdir(parents=True)
        write_json(
            mighty / "state.json",
            {
                "meta": {"title": "workflow-health-smoke"},
                "progress": {"current_chapter": 3},
                "plot_threads": {"foreshadowing": {"active": []}},
                "active_context": {"last_built": "2026-03-28T00:00:00Z", "hook_count": 0, "guardrail_count": 0},
                "chapter_meta": {"1": {"review_score": 87, "issue_clusters": [], "dimension_scores": {}}},
                "quality_metrics": {"dimension_scores": {"节奏": 0}},
            },
        )
        write_json(mighty / "state-archive.json", {"chapter_meta": {}})
        write_json(mighty / "workflow_state.json", {"transaction_contract": "chapter-transaction-v1", "current_task": {"status": "completed"}})
        write_json(mighty / "setting-gate.json", {"status": "passed"})
        write_json(mighty / "content-positioning.json", {"version": "1.0"})
        write_json(mighty / "learned-patterns.json", {"data": {}})
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(SCRIPT_PATH.exists(), "scripts/workflow_health_smoke.py is missing")

    def test_cli_reports_three_layer_health_summary(self) -> None:
        root = self.make_project_root()
        proc = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), str(root)],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["project"], str(root))
        self.assertIn("quality_audit", payload)
        self.assertIn("knowledge_projection", payload)
        self.assertIn("workflow_health", payload)
        self.assertEqual(payload["workflow_health"]["quality_audit_status"], "fail")


if __name__ == "__main__":
    unittest.main()
