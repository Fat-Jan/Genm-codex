import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "audit_chapter_structure_repetition.py"


def load_module():
    spec = importlib.util.spec_from_file_location("audit_chapter_structure_repetition", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ChapterStructureRepetitionTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        write_json(
            root / ".mighty" / "state.json",
            {
                "chapter_meta": {
                    "1": {
                        "chapter_structure": {
                            "conflict_type": "resource",
                            "protagonist_arc": "suppress",
                            "opponent_mode": "direct",
                            "gain_type": "information",
                            "cost_visibility": "explicit",
                            "chapter_end_style": "hook",
                        }
                    },
                    "2": {
                        "chapter_structure": {
                            "conflict_type": "resource",
                            "protagonist_arc": "test",
                            "opponent_mode": "direct",
                            "gain_type": "information",
                            "cost_visibility": "implicit",
                            "chapter_end_style": "hook",
                        }
                    },
                    "3": {
                        "chapter_structure": {
                            "conflict_type": "resource",
                            "protagonist_arc": "breakthrough",
                            "opponent_mode": "direct",
                            "gain_type": "information",
                            "cost_visibility": "none",
                            "chapter_end_style": "hook",
                        }
                    },
                }
            },
        )
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/audit_chapter_structure_repetition.py is missing")

    def test_audit_detects_repeated_conflict_and_gain_end_shapes(self) -> None:
        module = load_module()
        root = self.make_project_root()

        payload = module.audit_chapter_structure_repetition(root)

        finding_codes = {item["code"] for item in payload["findings"]}
        self.assertIn("repeated-conflict-opponent", finding_codes)
        self.assertIn("repeated-gain-ending", finding_codes)
        self.assertEqual(payload["status"], "warn")


if __name__ == "__main__":
    unittest.main()
