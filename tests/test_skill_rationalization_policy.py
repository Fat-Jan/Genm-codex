import json
import unittest
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_DOC = REPO_ROOT / "docs" / "00-当前有效" / "skill-rationalization-policy.md"
MERGE_MAP_SCHEMA = REPO_ROOT / "shared" / "templates" / "skill-merge-map-v1.schema.json"


class SkillRationalizationPolicyTests(unittest.TestCase):
    def test_policy_doc_and_schema_exist(self) -> None:
        self.assertTrue(POLICY_DOC.exists(), "skill rationalization policy doc is missing")
        self.assertTrue(MERGE_MAP_SCHEMA.exists(), "skill merge map schema is missing")

    def test_policy_doc_mentions_merge_alias_and_protected_boundaries(self) -> None:
        content = POLICY_DOC.read_text(encoding="utf-8")
        for token in (
            "`merge`",
            "`alias`",
            "`protected`",
            "`novel-scan`",
            "`install-skills.sh`",
            "`novel-status`",
            "`novel-query`",
            "`novel-write`",
        ):
            self.assertIn(token, content)

    def test_merge_map_schema_accepts_minimal_payload(self) -> None:
        schema = json.loads(MERGE_MAP_SCHEMA.read_text(encoding="utf-8"))
        payload = {
            "version": "1.0",
            "generated_at": "2026-03-28T00:00:00Z",
            "entries": [
                {
                    "skill": "novel-status",
                    "decision": "protected",
                    "reason": "高频主链 consumer，不在 v1.5 合并",
                },
                {
                    "skill": "novel-config",
                    "decision": "alias",
                    "target": "novel-test",
                    "reason": "可先做弱合并入口",
                },
                {
                    "skill": "novel-scan",
                    "decision": "protected",
                    "reason": "实验能力，不进入 skill merge",
                },
            ],
        }
        jsonschema.validate(payload, schema)


if __name__ == "__main__":
    unittest.main()
