import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "profile_contract.py"
SCHEMA_PATH = REPO_ROOT / "shared" / "templates" / "profile-contract-v1.schema.json"
PROFILE_ROOT = REPO_ROOT / "shared" / "profiles"


def load_module():
    spec = importlib.util.spec_from_file_location("profile_contract", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProfileContractTests(unittest.TestCase):
    def test_contract_module_and_schema_exist(self) -> None:
        self.assertTrue(MODULE_PATH.exists())
        self.assertTrue(SCHEMA_PATH.exists())

    def test_normalize_profile_handles_known_variants(self) -> None:
        module = load_module()

        palace = module.normalize_profile(
            module.load_profile(PROFILE_ROOT / "palace-intrigue" / "profile.yaml"),
            source_path="shared/profiles/palace-intrigue/profile.yaml",
        )
        urban = module.normalize_profile(
            module.load_profile(PROFILE_ROOT / "urban-brainhole" / "profile.yaml"),
            source_path="shared/profiles/urban-brainhole/profile.yaml",
        )

        self.assertEqual(palace["cool_points"]["density"], 0.8)
        self.assertEqual(palace["reader_expectations"]["must_not"][0], "对手全是蠢货")
        self.assertEqual(urban["cool_points"]["density"], "1.3/千字")
        self.assertEqual(urban["taboos"][0]["id"], "TABOO-001")
        self.assertEqual(urban["taboos"][0]["checkpoint"], "设定设计")
        self.assertTrue(urban["notes"]["has_dialogue_templates"])
        self.assertTrue(urban["notes"]["has_scene_description"])

    def test_state_summary_projection_matches_current_state_shape(self) -> None:
        module = load_module()
        normalized = module.normalize_profile(
            module.load_profile(PROFILE_ROOT / "xuanhuan" / "profile.yaml"),
            source_path="shared/profiles/xuanhuan/profile.yaml",
        )
        summary = module.summarize_for_state(normalized)

        self.assertEqual(summary["loaded"], "shared/profiles/xuanhuan/profile.yaml")
        self.assertEqual(summary["positioning_sidecar"], ".mighty/content-positioning.json")
        self.assertEqual(summary["tagpacks"], [])
        self.assertIn("type", summary["节奏"])
        self.assertIn("density", normalized["cool_points"])
        self.assertIn("quest", summary["strand权重"])
        self.assertIsInstance(summary["特殊约束"], list)

    def test_layer_descriptor_uses_core_overlay_reference_split(self) -> None:
        module = load_module()
        descriptor = module.resolve_profile_layers(PROFILE_ROOT / "xuanhuan", platform="tomato")

        self.assertTrue(descriptor["core_profile"].endswith("shared/profiles/xuanhuan/profile.yaml"))
        self.assertTrue(descriptor["platform_overlay"].endswith("shared/profiles/xuanhuan/profile-tomato.yaml"))
        self.assertIsNone(descriptor["bucket_overlay"])
        self.assertIn("cool-points.md", descriptor["reference_files"])

    def test_all_profiles_normalize_to_contract_shape(self) -> None:
        module = load_module()
        required_keys = set(json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["required"])

        profile_paths = sorted(PROFILE_ROOT.glob("*/profile.yaml"))
        self.assertGreater(len(profile_paths), 0)

        for path in profile_paths:
            normalized = module.normalize_profile(module.load_profile(path), source_path=str(path.relative_to(REPO_ROOT)))
            self.assertEqual(required_keys, set(normalized.keys()), path.name)
            self.assertTrue(normalized["name"], path.name)
            self.assertTrue(normalized["display_name"], path.name)
            self.assertIn("word_count", normalized["pacing"], path.name)
            self.assertIn("density", normalized["cool_points"], path.name)
            self.assertIn("must_not", normalized["reader_expectations"], path.name)

    def test_docs_describe_profile_contract_layers(self) -> None:
        readme = (REPO_ROOT / "shared" / "profiles" / "README.md").read_text(encoding="utf-8")
        schema_doc = (REPO_ROOT / "shared" / "references" / "shared" / "state-schema.md").read_text(encoding="utf-8")
        for token in ("core profile", "platform overlay", "bucket overlay", "reference files"):
            self.assertIn(token, readme)
        for token in ("genre_profile", "投影层", "raw profile dump", "content-positioning"):
            self.assertIn(token, schema_doc)


if __name__ == "__main__":
    unittest.main()
