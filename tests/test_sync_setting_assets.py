import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "sync-setting-assets.py"


def load_module():
    spec = importlib.util.spec_from_file_location("sync_setting_assets", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SyncSettingAssetsTests(unittest.TestCase):
    def test_recent_chapter_numbers_ignores_non_numeric_keys(self) -> None:
        module = load_module()
        state = {
            "chapter_meta": {
                "001": {},
                "002": {},
                "spinoff:番外1": {},
                "note": {},
                "010": {},
            }
        }

        result = module.recent_chapter_numbers(state, 2)

        self.assertEqual(result, [2, 10])


if __name__ == "__main__":
    unittest.main()
