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

    def test_state_template_chapter_meta_mentions_review_artifact_fields(self) -> None:
        payload = read_json("shared/templates/state-v5-template.json")
        chapter_meta = payload["chapter_meta"]["<chapter_number>"]
        self.assertIn("needs_fix", chapter_meta)
        self.assertIn("issue_clusters", chapter_meta)
        self.assertIn("dimension_scores", chapter_meta)
        self.assertIn("chapter_structure", chapter_meta)
        self.assertIn("anti_flattening_flags", chapter_meta)
        self.assertIn("anti_flattening_summary", chapter_meta)

    def test_state_schema_declares_all_template_top_level_keys(self) -> None:
        schema = read_json("shared/templates/state-schema-v5.json")
        payload = read_json("shared/templates/state-v5-template.json")
        schema_keys = set(schema["properties"].keys())
        template_keys = set(payload.keys())
        self.assertEqual(sorted(template_keys - schema_keys), [])

    def test_state_template_chapter_structure_uses_expected_fields(self) -> None:
        payload = read_json("shared/templates/state-v5-template.json")
        structure = payload["chapter_meta"]["<chapter_number>"]["chapter_structure"]
        self.assertEqual(
            sorted(structure.keys()),
            [
                "chapter_end_style",
                "conflict_type",
                "cost_visibility",
                "gain_type",
                "opponent_mode",
                "protagonist_arc",
            ],
        )

    def test_state_schema_accepts_chapter_structure_projection(self) -> None:
        schema = read_json("shared/templates/state-schema-v5.json")
        payload = read_json("shared/templates/state-v5-template.json")
        payload["chapter_meta"] = {
            "7": {
                "review_score": 88,
                "review_grade": "B+",
                "review_time": "2026-03-28T00:00:00Z",
                "needs_fix": False,
                "recommended_next_action": "novel-write",
                "issue_clusters": [],
                "dimension_scores": {"节奏": 8},
                "chapter_structure": {
                    "conflict_type": "resource",
                    "protagonist_arc": "test",
                    "opponent_mode": "trap",
                    "gain_type": "information",
                    "cost_visibility": "implicit",
                    "chapter_end_style": "residue",
                },
                "anti_flattening_flags": [],
                "anti_flattening_summary": {},
                "fanqie_bucket_flags": [],
                "fanqie_bucket_summary": {},
                "content_standard_flags": [],
                "packaging_alignment_note": "",
                "last_close_time": "2026-03-28T00:00:00Z",
                "last_close_route": "pass",
                "last_close_review_score_before": 86,
                "last_close_review_score_after": 88,
            }
        }
        jsonschema.validate(payload, schema)

    def test_state_schema_doc_mentions_current_top_level_runtime_blocks(self) -> None:
        content = (REPO_ROOT / "shared/references/shared/state-schema.md").read_text(encoding="utf-8")
        for token in (
            "`meta`",
            "`progress`",
            "`quality_metrics`",
            "`auto_learn_config`",
            "`platform_config`",
            "`genre_profile`",
            "`active_launch_grammar`",
            "`active_primary_pivot`",
            "`launch_stack_phase`",
            "`launch_stack_drift_signal`",
            "`active_context`",
            "`chapter_meta`",
            "`character_states`",
            "`setting_versions`",
            "`dungeons`",
            "`teammates`",
            "`constraints_loaded`",
        ):
            self.assertIn(token, content)
