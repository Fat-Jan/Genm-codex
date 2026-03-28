import importlib.util
import json
import sys
import unittest
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "render_skill_alias_plan.py"
MERGE_MAP_PATH = REPO_ROOT / "shared" / "templates" / "skill-merge-map-v1.json"
SCHEMA_PATH = REPO_ROOT / "shared" / "templates" / "skill-merge-map-v1.schema.json"
INSTALL_SCRIPT_PATH = REPO_ROOT / "scripts" / "install-skills.sh"


def load_module():
    spec = importlib.util.spec_from_file_location("render_skill_alias_plan", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SkillAliasPlanTests(unittest.TestCase):
    def test_helper_and_merge_map_exist(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "render_skill_alias_plan.py is missing")
        self.assertTrue(MERGE_MAP_PATH.exists(), "skill merge map json is missing")

    def test_merge_map_validates_against_schema(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        payload = json.loads(MERGE_MAP_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(payload, schema)

    def test_helper_emits_install_pairs_for_current_skills(self) -> None:
        module = load_module()
        payload = module.build_install_pairs()
        pair_set = {(item["source"], item["target"]) for item in payload["pairs"]}

        self.assertIn(("novel-init", "novel-init"), pair_set)
        self.assertIn(("novel-init", "genm-novel-init"), pair_set)
        self.assertIn(("novel-scan", "genm-novel-scan"), pair_set)

    def test_install_script_uses_helper(self) -> None:
        content = INSTALL_SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn("render_skill_alias_plan.py", content)


if __name__ == "__main__":
    unittest.main()
