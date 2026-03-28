import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "render_workflow_health_summary.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_workflow_health_summary", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class WorkflowHealthRenderTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        write_json(
            root / ".mighty" / "workflow-health.json",
            {
                "project_title": "渲染测试书",
                "quality_audit_status": "fail",
                "top_finding_codes": [
                    "empty-issue-clusters-with-score",
                    "empty-project-dimension-scores",
                ],
                "workflow_truth_status": "warn",
                "workflow_truth_missing_artifacts": ["snapshot_file_exists"],
                "repo_owned_tail_steps": ["maintenance", "snapshot"],
                "setting_gate_status": "passed",
                "has_recent_guardrails": False,
            },
        )
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/render_workflow_health_summary.py is missing")

    def test_render_markdown_summary_contains_key_fields(self) -> None:
        module = load_module()
        root = self.make_project_root()

        markdown = module.render_workflow_health_markdown(root)

        self.assertIn("## Workflow Health", markdown)
        self.assertIn("quality-audit: `fail`", markdown)
        self.assertIn("workflow-truth: `warn`", markdown)
        self.assertIn("snapshot_file_exists", markdown)
        self.assertIn("maintenance -> snapshot", markdown)
        self.assertIn("setting-gate: `passed`", markdown)
        self.assertIn("empty-issue-clusters-with-score", markdown)
        self.assertIn("next-action:", markdown)

    def test_render_status_block_contains_dashboard_sections(self) -> None:
        module = load_module()
        root = self.make_project_root()

        markdown = module.render_workflow_health_status_block(root)

        self.assertIn("### Workflow 健康", markdown)
        self.assertIn("- workflow-truth: `warn`", markdown)
        self.assertIn("- quality-audit: `fail`", markdown)
        self.assertIn("- repo-owned tail: `maintenance -> snapshot`", markdown)
        self.assertIn("- next-action:", markdown)

    def test_render_query_answer_returns_concise_risk_summary(self) -> None:
        module = load_module()
        root = self.make_project_root()

        markdown = module.render_workflow_health_query_answer(root)

        self.assertIn("workflow-health", markdown)
        self.assertIn("workflow-truth=`warn`", markdown)
        self.assertIn("quality-audit=`fail`", markdown)
        self.assertIn("snapshot_file_exists", markdown)
        self.assertIn("next-action=`", markdown)


if __name__ == "__main__":
    unittest.main()
