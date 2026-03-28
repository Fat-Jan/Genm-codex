import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "audit_project_quality_state.py"


def load_module():
    spec = importlib.util.spec_from_file_location("audit_project_quality_state", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ProjectQualityAuditTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        write_json(
            root / ".mighty" / "state.json",
            {
                "quality_metrics": {
                    "dimension_scores": {
                        "节奏": 0,
                        "代价感": 0,
                        "人物立体度": 0,
                    }
                },
                "chapter_meta": {
                    "001": {
                        "review_score": 88,
                        "issue_clusters": [],
                        "dimension_scores": {},
                        "recommended_next_action": "",
                    },
                    "002": {
                        "review_score": 87,
                        "issue_clusters": [
                            {
                                "type": "language",
                                "summary": "示例",
                            }
                        ],
                        "dimension_scores": {
                            "节奏": 86,
                        },
                        "recommended_next_action": "novel-fix",
                        "needs_fix": True,
                    },
                },
            },
        )
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/audit_project_quality_state.py is missing")

    def test_audit_flags_review_scores_with_empty_issue_clusters(self) -> None:
        module = load_module()
        root = self.make_project_root()

        payload = module.audit_project_quality_state(root)

        finding_codes = {item["code"] for item in payload["findings"]}
        self.assertIn("empty-issue-clusters-with-score", finding_codes)
        self.assertIn("missing-dimension-scores", finding_codes)
        self.assertIn("missing-anti-flattening-artifacts", finding_codes)
        self.assertIn("missing-route-decision", finding_codes)
        self.assertIn("missing-needs-fix-flag", finding_codes)
        self.assertIn("empty-project-dimension-scores", finding_codes)
        self.assertEqual(payload["status"], "fail")

    def test_cli_can_write_quality_audit_sidecar(self) -> None:
        root = self.make_project_root()
        proc = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                str(root),
                "--write",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)
        self.assertIn("quality_audit_file", payload)
        self.assertTrue((root / ".mighty" / "quality-audit.json").exists())


if __name__ == "__main__":
    unittest.main()
