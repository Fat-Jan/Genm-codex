import json
import unittest
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "shared" / "templates" / "sample-manifest-v1.schema.json"
DOC_PATH = REPO_ROOT / "docs" / "00-当前有效" / "sample-manifest-contract.md"


class SampleManifestContractTests(unittest.TestCase):
    def test_schema_and_doc_exist(self) -> None:
        self.assertTrue(SCHEMA_PATH.exists(), "sample-manifest schema is missing")
        self.assertTrue(DOC_PATH.exists(), "sample-manifest contract doc is missing")

    def test_schema_accepts_minimal_manifest_shape(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        payload = {
            "version": "1.0",
            "generated_at": "2026-03-28T00:00:00Z",
            "samples": [
                {
                    "sample_id": "e2e-novel",
                    "path": "e2e-novel",
                    "sample_type": "smoke",
                    "trust_tier": "baseline",
                    "platform": "番茄",
                    "bucket": "传统玄幻",
                    "status": "active",
                    "notes": "基础 smoke 样本",
                },
                {
                    "sample_id": "jiazhuangdan-regression",
                    "path": "projects/成婚前三日，我先改了侯府嫁妆单",
                    "sample_type": "project",
                    "trust_tier": "regression",
                    "platform": "番茄",
                    "bucket": "宫斗宅斗",
                    "status": "active",
                    "notes": "结构重复 regression 样本",
                },
            ],
        }
        jsonschema.validate(payload, schema)

    def test_doc_mentions_core_layers_and_admission_rules(self) -> None:
        content = DOC_PATH.read_text(encoding="utf-8")
        for token in (
            "`smoke`",
            "`regression`",
            "`high_confidence`",
            "`sample_id`",
            "`sample_type`",
            "`trust_tier`",
            "`path`",
            "`platform`",
            "`bucket`",
            "`status`",
        ):
            self.assertIn(token, content)


if __name__ == "__main__":
    unittest.main()
