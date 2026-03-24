from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "batch_writing_core_smoke.py"


def load_module():
    spec = importlib.util.spec_from_file_location("batch_writing_core_smoke", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class BatchWritingCoreSmokeTests(unittest.TestCase):
    def test_parse_args_accepts_manifest_and_output_dir(self) -> None:
        module = load_module()

        args = module.parse_args(
            [
                "--manifest",
                "/tmp/manifest.json",
                "--output-dir",
                "/tmp/out",
                "--mode",
                "draft",
            ]
        )

        self.assertEqual(args.manifest, "/tmp/manifest.json")
        self.assertEqual(args.output_dir, "/tmp/out")
        self.assertEqual(args.mode, "draft")

    def test_batch_run_generates_outputs_for_multiple_projects(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            manifest = Path(tmpdir) / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "projects": [
                            {
                                "project_root": str(REPO_ROOT / "projects/宗门垫底那年，我把废丹卖成了天价"),
                                "chapters": "001-003",
                            },
                            {
                                "project_root": str(REPO_ROOT / "projects/她升职那天，前上司成了我合租室友"),
                                "chapters": "001-003",
                            },
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = module.run_batch(
                manifest_path=manifest,
                output_dir=output_dir,
                mode="draft",
                writeback=False,
                save_packaging=False,
            )

            self.assertEqual(result["count"], 2)
            self.assertEqual(len(result["outputs"]), 2)
            for item in result["outputs"]:
                self.assertTrue(Path(item["output_path"]).exists())

    def test_batch_run_can_writeback_save_packaging_and_emit_summary_report(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            summary_path = Path(tmpdir) / "summary.json"
            manifest = Path(tmpdir) / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "projects": [
                            {
                                "project_root": str(REPO_ROOT / "projects/转学第一天，我把校草认成了新来的代课老师"),
                                "chapters": "001-003",
                            },
                            {
                                "project_root": str(REPO_ROOT / "projects/我赔光积蓄那天，系统先把违约金打到了账上"),
                                "chapters": "001-003",
                            },
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = module.run_batch(
                manifest_path=manifest,
                output_dir=output_dir,
                mode="writeback",
                writeback=True,
                save_packaging=True,
                summary_report=summary_path,
            )

            self.assertEqual(result["count"], 2)
            self.assertTrue(summary_path.exists())
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["count"], 2)
            self.assertEqual(summary["mode"], "writeback")
            self.assertEqual(summary["success_count"], 2)
            self.assertEqual(summary["failure_count"], 0)
            self.assertIn("bucket_counts", summary)
            self.assertIn("packaging_status_counts", summary)
            self.assertIn("writeback_status_counts", summary)
            self.assertEqual(summary["bucket_counts"]["青春甜宠"], 1)
            self.assertEqual(summary["bucket_counts"]["都市脑洞"], 1)
            for item in summary["outputs"]:
                self.assertEqual(item["effective_mode"], "writeback")
                self.assertIn(item["packaging_status"], {"written", "written-sidecar"})

    def test_batch_run_collects_failures_without_aborting_whole_batch(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            summary_path = Path(tmpdir) / "summary.json"
            manifest = Path(tmpdir) / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "projects": [
                            {
                                "project_root": str(REPO_ROOT / "projects/宗门垫底那年，我把废丹卖成了天价"),
                                "chapters": "001-003",
                            },
                            {
                                "project_root": str(REPO_ROOT / "does-not-exist"),
                                "chapters": "001-003",
                            },
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = module.run_batch(
                manifest_path=manifest,
                output_dir=output_dir,
                mode="draft",
                writeback=False,
                save_packaging=False,
                summary_report=summary_path,
            )

            self.assertEqual(result["count"], 2)
            self.assertEqual(result["success_count"], 1)
            self.assertEqual(result["failure_count"], 1)
            self.assertEqual(len(result["failed_projects"]), 1)
            failure = result["failed_projects"][0]
            self.assertIn("does-not-exist", failure["project_root"])
            self.assertIn("error", failure)


if __name__ == "__main__":
    unittest.main()
