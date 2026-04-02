import json
import os
import unittest
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]
HOST_MATRIX_RELATIVE_PATH = "shared/templates/host-capability-matrix-v1.json"
HOST_EVIDENCE_LEDGER_RELATIVE_PATH = "shared/templates/host-evidence-ledger-v1.json"


def resolve_json_path(relative_path: str) -> Path:
    if relative_path == HOST_MATRIX_RELATIVE_PATH:
        override = os.environ.get("GENM_HOST_CAPABILITY_MATRIX_FILE")
        if override:
            return Path(override)
    return REPO_ROOT / relative_path


def read_json(relative_path: str) -> dict:
    return json.loads(resolve_json_path(relative_path).read_text(encoding="utf-8"))


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
        content = (REPO_ROOT / "shared/references/shared/state-schema.md").read_text(
            encoding="utf-8"
        )
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

    def test_host_capability_matrix_files_exist(self) -> None:
        self.assertTrue(
            (
                REPO_ROOT / "shared/templates/host-capability-matrix-v1.schema.json"
            ).exists()
        )
        self.assertTrue(
            (REPO_ROOT / "shared/templates/host-capability-matrix-v1.json").exists()
        )

    def test_host_evidence_ledger_files_exist(self) -> None:
        self.assertTrue(
            (
                REPO_ROOT / "shared/templates/host-evidence-ledger-v1.schema.json"
            ).exists()
        )
        self.assertTrue(
            (REPO_ROOT / "shared/templates/host-evidence-ledger-v1.json").exists()
        )

    def test_host_capability_matrix_validates_against_schema(self) -> None:
        schema = read_json("shared/templates/host-capability-matrix-v1.schema.json")
        payload = read_json("shared/templates/host-capability-matrix-v1.json")
        jsonschema.validate(payload, schema)

    def test_host_capability_matrix_rejects_unsupported_host_with_install_root(
        self,
    ) -> None:
        schema = read_json("shared/templates/host-capability-matrix-v1.schema.json")
        payload = json.loads(
            json.dumps(read_json("shared/templates/host-capability-matrix-v1.json"))
        )
        payload["hosts"]["trae"]["skill_install_root"] = "~/.trae/skills"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(payload, schema)

    def test_host_capability_matrix_rejects_installable_host_without_install_root(
        self,
    ) -> None:
        schema = read_json("shared/templates/host-capability-matrix-v1.schema.json")
        payload = json.loads(
            json.dumps(read_json("shared/templates/host-capability-matrix-v1.json"))
        )
        payload["hosts"]["codex"]["skill_install_root"] = None
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(payload, schema)

    def test_host_capability_matrix_rejects_empty_install_root_for_copy_mode(
        self,
    ) -> None:
        schema = read_json("shared/templates/host-capability-matrix-v1.schema.json")
        payload = json.loads(
            json.dumps(read_json("shared/templates/host-capability-matrix-v1.json"))
        )
        payload["hosts"]["codex"]["install_mode"] = "copy"
        payload["hosts"]["codex"]["skill_install_root"] = ""
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(payload, schema)

    def test_host_capability_matrix_rejects_unexpected_install_root_for_known_host(
        self,
    ) -> None:
        schema = read_json("shared/templates/host-capability-matrix-v1.schema.json")
        payload = json.loads(
            json.dumps(read_json("shared/templates/host-capability-matrix-v1.json"))
        )
        payload["hosts"]["codex"]["skill_install_root"] = "~/tmp/skills"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(payload, schema)

    def test_host_capability_matrix_declares_expected_hosts(self) -> None:
        payload = read_json("shared/templates/host-capability-matrix-v1.json")
        self.assertEqual(
            sorted(payload["hosts"].keys()),
            ["claude", "codex", "openclaw", "opencode", "trae"],
        )

    def test_host_capability_matrix_preserves_status_and_verification_levels(
        self,
    ) -> None:
        payload = read_json("shared/templates/host-capability-matrix-v1.json")
        actual = {
            host_id: (row["status"], row["verification_level"])
            for host_id, row in payload["hosts"].items()
        }
        self.assertEqual(
            actual,
            {
                "claude": ("baseline", "partial"),
                "codex": ("legacy", "verified"),
                "opencode": ("experimental", "partial"),
                "openclaw": ("experimental", "partial"),
                "trae": ("experimental", "partial"),
            },
        )

    def test_host_capability_matrix_install_fields_match_current_contract(self) -> None:
        payload = read_json("shared/templates/host-capability-matrix-v1.json")
        actual = {
            host_id: (row["skill_install_root"], row["install_mode"])
            for host_id, row in payload["hosts"].items()
        }
        self.assertEqual(
            actual,
            {
                "claude": ("~/.claude/skills", "symlink"),
                "codex": ("~/.codex/skills", "symlink"),
                "opencode": ("~/.config/opencode/skills", "symlink"),
                "openclaw": ("~/.openclaw/skills", "symlink"),
                "trae": (None, "unsupported"),
            },
        )

    def test_host_capability_matrix_captures_capability_boundaries(self) -> None:
        payload = read_json("shared/templates/host-capability-matrix-v1.json")
        capability_keys = (
            "supports_skill_discovery",
            "supports_alias",
            "supports_rules_context",
            "supports_hooks",
            "supports_mcp",
            "supports_native_invocation",
        )
        actual = {
            host_id: {key: row[key] for key in capability_keys}
            for host_id, row in payload["hosts"].items()
        }

        self.assertEqual(
            actual,
            {
                "claude": {
                    "supports_skill_discovery": "partial",
                    "supports_alias": "partial",
                    "supports_rules_context": "verified",
                    "supports_hooks": "verified",
                    "supports_mcp": "verified",
                    "supports_native_invocation": "partial",
                },
                "codex": {
                    "supports_skill_discovery": "verified",
                    "supports_alias": "verified",
                    "supports_rules_context": "assumed",
                    "supports_hooks": "assumed",
                    "supports_mcp": "assumed",
                    "supports_native_invocation": "verified",
                },
                "opencode": {
                    "supports_skill_discovery": "partial",
                    "supports_alias": "partial",
                    "supports_rules_context": "assumed",
                    "supports_hooks": "assumed",
                    "supports_mcp": "assumed",
                    "supports_native_invocation": "assumed",
                },
                "openclaw": {
                    "supports_skill_discovery": "partial",
                    "supports_alias": "partial",
                    "supports_rules_context": "assumed",
                    "supports_hooks": "assumed",
                    "supports_mcp": "assumed",
                    "supports_native_invocation": "assumed",
                },
                "trae": {
                    "supports_skill_discovery": "partial",
                    "supports_alias": "assumed",
                    "supports_rules_context": "verified",
                    "supports_hooks": "assumed",
                    "supports_mcp": "partial",
                    "supports_native_invocation": "assumed",
                },
            },
        )

    def test_host_capability_matrix_evidence_refs_exist(self) -> None:
        payload = read_json("shared/templates/host-capability-matrix-v1.json")
        for host_id, host in payload["hosts"].items():
            self.assertGreaterEqual(len(host["evidence"]), 1, host_id)
            for evidence in host["evidence"]:
                self.assertIn(evidence["kind"], {"repo_file", "runtime_observation"})
                self.assertTrue(evidence["ref"].strip())
                self.assertTrue(evidence["summary"].strip())
                if evidence["kind"] == "repo_file":
                    self.assertTrue(
                        (REPO_ROOT / evidence["ref"]).exists(), evidence["ref"]
                    )

    def test_host_capability_matrix_evidence_covers_install_and_context_surfaces(
        self,
    ) -> None:
        payload = read_json("shared/templates/host-capability-matrix-v1.json")
        for host_id in ("claude", "codex", "opencode", "openclaw"):
            repo_refs = {
                item["ref"]
                for item in payload["hosts"][host_id]["evidence"]
                if item["kind"] == "repo_file"
            }
            self.assertIn("scripts/install-skills.sh", repo_refs)

        trae_refs = {
            item["ref"]
            for item in payload["hosts"]["trae"]["evidence"]
            if item["kind"] == "repo_file"
        }
        self.assertTrue(any(ref.startswith(".trae/rules/") for ref in trae_refs))

    def test_host_evidence_ledger_validates_against_schema(self) -> None:
        schema = read_json("shared/templates/host-evidence-ledger-v1.schema.json")
        payload = read_json("shared/templates/host-evidence-ledger-v1.json")
        jsonschema.validate(payload, schema)

    def test_host_evidence_ledger_covers_current_matrix_evidence(self) -> None:
        matrix = read_json("shared/templates/host-capability-matrix-v1.json")
        ledger = read_json("shared/templates/host-evidence-ledger-v1.json")
        ledger_refs = {
            (entry["host_id"], entry["kind"], entry["ref"])
            for entry in ledger["entries"]
        }
        for host_id, row in matrix["hosts"].items():
            for evidence in row["evidence"]:
                self.assertIn(
                    (host_id, evidence["kind"], evidence["ref"]),
                    ledger_refs,
                )

    def test_host_evidence_ledger_repo_file_refs_exist(self) -> None:
        payload = read_json("shared/templates/host-evidence-ledger-v1.json")
        for entry in payload["entries"]:
            if entry["kind"] == "repo_file":
                self.assertTrue((REPO_ROOT / entry["ref"]).exists(), entry["ref"])

    def test_host_evidence_ledger_tracks_trae_official_doc_surfaces(self) -> None:
        payload = read_json("shared/templates/host-evidence-ledger-v1.json")
        trae_doc_surfaces = {
            entry["surface"]
            for entry in payload["entries"]
            if entry["host_id"] == "trae" and entry["kind"] == "official_doc"
        }
        self.assertTrue(
            {
                "project_rules",
                "user_or_global_rules",
                "project_skills",
                "global_skills",
                "mcp_registration",
                "mcp_agent_binding",
                "auto_run_mcp",
                "auto_run_commands",
                "sandbox",
            }.issubset(trae_doc_surfaces)
        )

    def test_host_evidence_ledger_tracks_trae_manual_verification_surfaces(
        self,
    ) -> None:
        payload = read_json("shared/templates/host-evidence-ledger-v1.json")
        trae_manual_surfaces = {
            entry["surface"]
            for entry in payload["entries"]
            if entry["host_id"] == "trae" and entry["kind"] == "manual_verification"
        }
        self.assertTrue(
            {
                "global_skills",
                "skill_discovery",
                "mcp",
                "sandbox",
                "skill_invocation",
            }.issubset(trae_manual_surfaces)
        )
