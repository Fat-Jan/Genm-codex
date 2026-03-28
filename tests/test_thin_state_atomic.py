import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from unittest import mock
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "thin-state.py"


def load_module():
    spec = importlib.util.spec_from_file_location("thin_state", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ThinStateAtomicTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        mighty = root / ".mighty"
        mighty.mkdir(parents=True)
        write_json(
            mighty / "state.json",
            {
                "meta": {"title": "thin-state-test"},
                "active_context": {"sidecar_file": ".mighty/active-context.json"},
                "chapter_meta": {
                    "1": {"summary": "第一章摘要"},
                    "2": {"summary": "第二章摘要"},
                    "3": {"summary": "第三章摘要"},
                },
                "chapter_snapshots": {
                    "1": {"updated_at": "2026-03-28T00:00:00Z"},
                    "2": {"updated_at": "2026-03-28T00:00:00Z"},
                    "3": {"updated_at": "2026-03-28T00:00:00Z"},
                },
                "summaries_index": {
                    "1": {"summary": "第一章摘要"},
                    "2": {"summary": "第二章摘要"},
                    "3": {"summary": "第三章摘要"},
                },
            },
        )
        return root

    def test_atomic_write_json_replaces_file_without_leaving_tmp(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "payload.json"
            module.atomic_write_json(path, {"ok": True})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"ok": True})
            self.assertEqual(list(path.parent.glob("*.tmp")), [])

    def test_main_uses_atomic_write_for_all_output_files(self) -> None:
        module = load_module()
        root = self.make_project_root()
        calls: list[Path] = []
        real_atomic = module.atomic_write_json

        def spy(path: Path, payload: dict) -> None:
            calls.append(path)
            real_atomic(path, payload)

        with mock.patch.object(module, "atomic_write_json", side_effect=spy):
            module.main([str(root), "--retain-recent-chapters", "1", "--timestamp", "2026-03-28T00:00:00Z"])

        mighty = root / ".mighty"
        self.assertIn(mighty / "state.json", calls)
        self.assertIn(mighty / "state-archive.json", calls)
        self.assertIn(mighty / "volume-summaries.json", calls)


if __name__ == "__main__":
    unittest.main()
