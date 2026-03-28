import importlib.util
import json
import sys
from pathlib import Path
import unittest

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "shared" / "templates" / "sample-manifest-v1.json"
SCHEMA_PATH = REPO_ROOT / "shared" / "templates" / "sample-manifest-v1.schema.json"
MODULE_PATH = REPO_ROOT / "scripts" / "render_sample_manifest_summary.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_sample_manifest_summary", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SampleManifestRuntimeTests(unittest.TestCase):
    def test_manifest_exists_and_validates(self) -> None:
        self.assertTrue(MANIFEST_PATH.exists(), "sample manifest json is missing")
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        jsonschema.validate(payload, schema)

    def test_manifest_contains_key_samples(self) -> None:
        payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        ids = {item["sample_id"] for item in payload["samples"]}
        self.assertIn("e2e-novel", ids)
        self.assertIn("jiazhuangdan-regression", ids)
        self.assertIn("shunvmoulue-high-confidence", ids)

    def test_summary_helper_exists_and_renders_counts(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "render_sample_manifest_summary.py is missing")
        module = load_module()
        markdown = module.render_sample_manifest_summary_markdown(MANIFEST_PATH)
        self.assertIn("## Sample Manifest Summary", markdown)
        self.assertIn("baseline", markdown)
        self.assertIn("regression", markdown)
        self.assertIn("high_confidence", markdown)


if __name__ == "__main__":
    unittest.main()
