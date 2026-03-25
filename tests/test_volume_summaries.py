import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "build_volume_summaries.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_volume_summaries", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class VolumeSummariesContractTests(unittest.TestCase):
    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/build_volume_summaries.py is missing")

    def test_status_and_query_docs_reference_volume_summaries(self) -> None:
        expectations = {
            "skills/novel-status/SKILL.md": ".mighty/volume-summaries.json",
            "skills/novel-query/SKILL.md": ".mighty/volume-summaries.json",
            "docs/state-thinning-and-setting-sync.md": ".mighty/volume-summaries.json",
        }
        for relative_path, token in expectations.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn(token, content, f"{relative_path} missing token: {token}")


class VolumeSummariesBehaviorTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        mighty = root / ".mighty"
        mighty.mkdir(parents=True)
        write_json(
            mighty / "state.json",
            {
                "meta": {"title": "长篇压缩测试"},
                "summaries_index": {
                    "4": {"summary": "第四章摘要"},
                    "5": {"summary": "第五章摘要"},
                },
                "chapter_meta": {
                    "4": {"summary": "第四章摘要"},
                    "5": {"summary": "第五章摘要"},
                },
            },
        )
        write_json(
            mighty / "state-archive.json",
            {
                "summaries_index": {
                    "1": {"summary": "第一章摘要"},
                    "2": {"summary": "第二章摘要"},
                    "3": {"summary": "第三章摘要"},
                },
                "chapter_meta": {
                    "1": {"summary": "第一章摘要"},
                    "2": {"summary": "第二章摘要"},
                    "3": {"summary": "第三章摘要"},
                },
            },
        )
        return root

    def test_build_volume_summaries_creates_archive_only_summary_ranges(self) -> None:
        module = load_module()
        root = self.make_project_root()

        result = module.main([str(root), "--timestamp", "2026-03-25T00:00:00Z"])

        sidecar = root / ".mighty" / "volume-summaries.json"
        self.assertTrue(sidecar.exists())
        payload = json.loads(sidecar.read_text(encoding="utf-8"))
        self.assertEqual(result["volume_summaries_file"], str(sidecar))
        self.assertEqual(payload["archived_summary_count"], 3)
        self.assertEqual(payload["live_summary_count"], 2)
        self.assertEqual(len(payload["ranges"]), 1)
        first_range = payload["ranges"][0]
        self.assertEqual(first_range["start_chapter"], "1")
        self.assertEqual(first_range["end_chapter"], "3")
        self.assertEqual(first_range["chapter_count"], 3)
        self.assertIn("第一章摘要", first_range["summary"])
        self.assertNotIn("第四章摘要", first_range["summary"])

    def test_thin_state_refreshes_volume_summaries(self) -> None:
        root = self.make_project_root()
        mighty = root / ".mighty"
        state = json.loads((mighty / "state.json").read_text(encoding="utf-8"))
        state["summaries_index"] = {
            "1": {"summary": "第一章摘要"},
            "2": {"summary": "第二章摘要"},
            "3": {"summary": "第三章摘要"},
            "4": {"summary": "第四章摘要"},
            "5": {"summary": "第五章摘要"},
        }
        state["chapter_meta"] = {
            "1": {"summary": "第一章摘要"},
            "2": {"summary": "第二章摘要"},
            "3": {"summary": "第三章摘要"},
            "4": {"summary": "第四章摘要"},
            "5": {"summary": "第五章摘要"},
        }
        (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        (mighty / "state-archive.json").unlink(missing_ok=True)

        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "thin-state.py"),
                str(root),
                "--retain-recent-chapters",
                "2",
                "--timestamp",
                "2026-03-25T00:00:00Z",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertTrue(proc.stdout)
        sidecar = json.loads((mighty / "volume-summaries.json").read_text(encoding="utf-8"))
        self.assertEqual(sidecar["archived_summary_count"], 3)
        self.assertEqual(sidecar["ranges"][0]["end_chapter"], "3")


if __name__ == "__main__":
    unittest.main()
