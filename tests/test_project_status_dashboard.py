import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "render_project_status_dashboard.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_project_status_dashboard", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ProjectStatusDashboardTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        mighty = root / ".mighty"
        mighty.mkdir(parents=True)

        write_json(
            mighty / "state.json",
            {
                "meta": {"title": "状态面板测试", "platform": "番茄"},
                "progress": {"current_chapter": 12, "total_words": 42000},
                "active_context": {
                    "sidecar_file": ".mighty/active-context.json",
                    "last_built": "2026-03-28T00:00:00Z",
                    "summary_window": {"latest_chapter": 12},
                    "hook_count": 2,
                    "guardrail_count": 1,
                },
            },
        )
        write_json(
            mighty / "workflow-health.json",
            {
                "project_title": "状态面板测试",
                "quality_audit_status": "warn",
                "top_finding_codes": ["missing-anti-flattening-artifacts"],
                "workflow_truth_status": "pass",
                "workflow_truth_missing_artifacts": [],
                "repo_owned_tail_steps": ["maintenance", "snapshot"],
                "setting_gate_status": "blocked",
                "has_recent_guardrails": True,
                "recommended_next_action": "repair-review-artifacts",
                "recommended_reason": "先修 review artifact。",
            },
        )
        write_json(
            mighty / "setting-gate.json",
            {
                "status": "blocked",
                "blocking_gaps": ["补齐宅门真值表"],
                "review_items": ["确认排行称谓"],
                "minimal_next_action": {
                    "summary": "先补真值表再重跑 gate",
                    "suggested_commands": ["python3 scripts/setting_gate.py . --stage outline"],
                },
            },
        )
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/render_project_status_dashboard.py is missing")

    def test_render_dashboard_markdown_contains_status_sections(self) -> None:
        module = load_module()
        root = self.make_project_root()

        markdown = module.render_project_status_dashboard_markdown(root)

        self.assertIn("## Project Status Dashboard", markdown)
        self.assertIn("### Workflow 健康", markdown)
        self.assertIn("### Setting Gate", markdown)
        self.assertIn("### Current Writing Slice", markdown)
        self.assertIn("状态面板测试", markdown)
        self.assertIn("repair-review-artifacts", markdown)
        self.assertIn("补齐宅门真值表", markdown)

    def test_render_query_answer_contains_compact_operational_summary(self) -> None:
        module = load_module()
        root = self.make_project_root()

        answer = module.render_project_status_query_answer(root)

        self.assertIn("project-status", answer)
        self.assertIn("chapter=`12`", answer)
        self.assertIn("workflow-action=`repair-review-artifacts`", answer)
        self.assertIn("gate=`blocked`", answer)


if __name__ == "__main__":
    unittest.main()
