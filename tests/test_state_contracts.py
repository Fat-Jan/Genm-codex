import json
import unittest
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_json(relative_path: str) -> dict:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


class StateContractSchemaTests(unittest.TestCase):
    def test_state_schema_file_exists(self) -> None:
        self.assertTrue((REPO_ROOT / "shared/templates/state-schema-v5.json").exists())

    def test_state_template_validates_against_schema(self) -> None:
        schema = read_json("shared/templates/state-schema-v5.json")
        payload = read_json("shared/templates/state-v5-template.json")
        jsonschema.validate(payload, schema)

    def test_externalized_state_shape_also_validates(self) -> None:
        schema = read_json("shared/templates/state-schema-v5.json")
        payload = read_json("shared/templates/state-v5-template.json")
        payload["learned_patterns"] = {
            "externalized": True,
            "sidecar_file": ".mighty/learned-patterns.json",
            "last_updated": "2026-03-25T00:00:00Z",
            "available_sections": ["opening_strategy", "recent_guardrails"],
            "has_recent_guardrails": True,
            "recent_guardrails_expires_after_chapter": 5,
        }
        payload["market_adjustments"] = {
            "externalized": True,
            "sidecar_file": ".mighty/market-adjustments.json",
            "last_updated": "2026-03-25T00:00:00Z",
            "last_applied": None,
            "source_scan": None,
            "adjustment_count": 1,
        }
        payload["entities"]["items"]["tracked"] = [{"name": "劳动合同电子版"}]
        payload["entities"]["factions"] = {"active": [{"name": "曜石互联"}]}
        jsonschema.validate(payload, schema)

    def test_workflow_template_validates_against_schema(self) -> None:
        schema = read_json("shared/templates/workflow-state-v2.schema.json")
        payload = read_json("shared/templates/workflow-state-v2.json")
        jsonschema.validate(payload, schema)

    def test_learned_patterns_template_validates_against_schema(self) -> None:
        schema = read_json("shared/templates/learned-patterns.schema.json")
        payload = read_json("shared/templates/learned-patterns-template.json")
        jsonschema.validate(payload, schema)

    def test_state_archive_schema_validates_archive_shape(self) -> None:
        schema = read_json("shared/templates/state-archive-v1.json")
        payload = {
            "$schema": "state-archive-v1.json",
            "version": "1.0",
            "archived_at": "2026-03-25T00:00:00Z",
            "retained_recent_chapters": ["004", "005"],
            "chapter_meta": {"001": {"summary": "第一章摘要"}},
            "chapter_snapshots": {},
            "summaries_index": {"001": {"summary": "第一章摘要"}},
        }
        jsonschema.validate(payload, schema)
