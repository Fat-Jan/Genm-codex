import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "build_workflow_health_bundle.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_workflow_health_bundle", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class WorkflowHealthBundleTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        mighty = root / ".mighty"
        mighty.mkdir(parents=True)

        write_json(
            mighty / "quality-audit.json",
            {
                "project": str(root),
                "status": "fail",
                "findings": [
                    {"code": "empty-issue-clusters-with-score", "chapter": "11", "severity": "warn"},
                    {"code": "empty-project-dimension-scores", "severity": "fail"},
                ],
            },
        )
        write_json(
            mighty / "knowledge-projection.json",
            {
                "project_title": "workflow-health-test",
                "workflow_contract": {
                    "transaction_contract": "chapter-transaction-v1",
                    "current_command": "novel-batch",
                    "current_status": "completed",
                    "repo_owned_tail_steps": ["maintenance", "snapshot"],
                },
                "workflow_truth": {
                    "status": "fail",
                    "missing_artifacts": ["snapshot_file_exists"],
                },
                "sidecar_health": {
                    "setting_gate_status": "passed",
                    "has_recent_guardrails": False,
                },
            },
        )
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/build_workflow_health_bundle.py is missing")

    def test_build_bundle_returns_compact_workflow_health_summary(self) -> None:
        module = load_module()
        root = self.make_project_root()

        payload = module.build_workflow_health_bundle(root, timestamp="2026-03-28T00:00:00Z")

        self.assertEqual(payload["project_title"], "workflow-health-test")
        self.assertEqual(payload["quality_audit_status"], "fail")
        self.assertEqual(payload["top_finding_codes"], ["empty-issue-clusters-with-score", "empty-project-dimension-scores"])
        self.assertEqual(payload["workflow_truth_status"], "fail")
        self.assertEqual(payload["workflow_truth_missing_artifacts"], ["snapshot_file_exists"])
        self.assertEqual(payload["repo_owned_tail_steps"], ["maintenance", "snapshot"])
        self.assertEqual(payload["setting_gate_status"], "passed")


if __name__ == "__main__":
    unittest.main()
