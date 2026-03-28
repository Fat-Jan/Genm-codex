import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "render_project_scan_summary.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_project_scan_summary", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ProjectScanSummaryTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        mighty = root / ".mighty"
        mighty.mkdir(parents=True)

        write_json(
            mighty / "market-data.json",
            {
                "version": "1.0",
                "scan_time": "2026-03-28T00:00:00Z",
                "mode": "report-only",
                "report_kind": "real_report",
                "targets": {"platforms": ["番茄"], "genre": "宫斗宅斗", "depth": "quick"},
                "source_plan": {"requested_scope": {"platform": "番茄"}},
                "sources": [{"url": "https://fanqienovel.com/rank/0_2_246", "status": "success"}],
                "findings": {
                    "hot_genres": [],
                    "recommended_content_buckets": [
                        {"bucket_name": "宫斗宅斗", "config_key": "gongdou_zhai", "confidence": "medium", "reason": "test"}
                    ],
                    "hot_tags": [{"tag": "高门婚配/权臣拉扯"}],
                    "opening_patterns": [{"pattern": "婚配冲突先落地"}],
                    "cool_point_patterns": [],
                    "platform_notes": [],
                },
                "confidence": {"overall": "medium", "reason": "test"},
                "gaps": [],
                "apply_recommendations": [{"type": "hook_design", "suggestion": "前置婚配冲突"}],
            },
        )
        write_json(
            mighty / "market-adjustments.json",
            {
                "last_applied": "2026-03-28T00:00:00Z",
                "source_scan": {
                    "tool": "novel-scan",
                    "mode": "project-annotate",
                    "confidence": {"overall": "medium", "reason": "test"},
                },
                "adjustments": [
                    {"id": "scan-surface-hook", "suggestion": "把婚配错位前置到首屏。"},
                    {"id": "scan-frontload-conflict", "suggestion": "压迫和反击同轮闭合。"},
                ],
            },
        )
        write_json(
            mighty / "research-candidates.json",
            {
                "version": "1.0",
                "generated_at": "2026-03-28T00:00:00Z",
                "source_scan": {
                    "tool": "novel-scan",
                    "mode": "project-annotate",
                    "platform": "番茄",
                    "genre": "宫斗宅斗",
                    "depth": "quick",
                    "report_kind": "real_report",
                },
                "candidates": [
                    {
                        "name": "嫡庶婚配真值补证",
                        "kind": "rule",
                        "source": "mcp",
                        "confidence": "medium",
                        "candidate_files": ["设定集/家族/宅门真值表.md"],
                        "evidence_urls": ["https://fanqienovel.com/rank/0_2_246"],
                        "notes": ["candidate only, not canon"],
                    }
                ],
            },
        )
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/render_project_scan_summary.py is missing")

    def test_render_scan_summary_markdown_contains_key_sections(self) -> None:
        module = load_module()
        root = self.make_project_root()

        markdown = module.render_project_scan_summary_markdown(root)

        self.assertIn("## Project Scan Summary", markdown)
        self.assertIn("scan-mode: `report-only`", markdown)
        self.assertIn("confidence: `medium`", markdown)
        self.assertIn("宫斗宅斗", markdown)
        self.assertIn("scan-surface-hook", markdown)
        self.assertIn("嫡庶婚配真值补证", markdown)

    def test_render_query_answer_contains_compact_scan_status(self) -> None:
        module = load_module()
        root = self.make_project_root()

        answer = module.render_project_scan_query_answer(root)

        self.assertIn("scan-summary", answer)
        self.assertIn("mode=`report-only`", answer)
        self.assertIn("confidence=`medium`", answer)
        self.assertIn("top-bucket=`宫斗宅斗`", answer)


if __name__ == "__main__":
    unittest.main()
