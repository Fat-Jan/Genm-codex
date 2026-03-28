import json
import unittest
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKET_DATA_SCHEMA = REPO_ROOT / "shared" / "templates" / "market-data-v1.schema.json"
MARKET_ADJUSTMENTS_SCHEMA = REPO_ROOT / "shared" / "templates" / "market-adjustments-v1.schema.json"
RESEARCH_CANDIDATES_SCHEMA = REPO_ROOT / "shared" / "templates" / "research-candidates-v1.schema.json"
DOC_PATH = REPO_ROOT / "docs" / "00-当前有效" / "scan-result-contract.md"


class ScanResultContractTests(unittest.TestCase):
    def test_scan_contract_files_exist(self) -> None:
        self.assertTrue(MARKET_DATA_SCHEMA.exists(), "market-data schema is missing")
        self.assertTrue(MARKET_ADJUSTMENTS_SCHEMA.exists(), "market-adjustments schema is missing")
        self.assertTrue(RESEARCH_CANDIDATES_SCHEMA.exists(), "research-candidates schema is missing")
        self.assertTrue(DOC_PATH.exists(), "scan-result contract doc is missing")

    def test_market_data_schema_accepts_minimal_report_only_payload(self) -> None:
        schema = json.loads(MARKET_DATA_SCHEMA.read_text(encoding="utf-8"))
        payload = {
            "version": "1.0",
            "scan_time": "2026-03-28T00:00:00Z",
            "mode": "report-only",
            "report_kind": "skeleton",
            "targets": {"platforms": ["番茄"], "genre": "玄幻", "depth": "quick"},
            "source_plan": {"requested_scope": {"platform": "番茄"}},
            "sources": [],
            "findings": {
                "hot_genres": [],
                "recommended_content_buckets": [],
                "hot_tags": [],
                "opening_patterns": [],
                "cool_point_patterns": [],
                "platform_notes": [],
            },
            "confidence": {"overall": "low", "reason": "insufficient evidence"},
            "gaps": [],
            "apply_recommendations": [],
        }
        jsonschema.validate(payload, schema)

    def test_market_adjustments_schema_accepts_project_annotate_payload(self) -> None:
        schema = json.loads(MARKET_ADJUSTMENTS_SCHEMA.read_text(encoding="utf-8"))
        payload = {
            "version": "1.0",
            "last_applied": "2026-03-28T00:00:00Z",
            "source_scan": {
                "tool": "novel-scan",
                "mode": "project-annotate",
                "confidence": {
                    "overall": "medium",
                    "reason": "test"
                },
            },
            "adjustments": [
                {
                    "id": "scan-manual-review-first",
                    "type": "manual_review",
                    "suggestion": "先人工审查再决定是否采纳。",
                    "confidence": "medium",
                }
            ],
        }
        jsonschema.validate(payload, schema)

    def test_research_candidates_schema_accepts_candidate_payload(self) -> None:
        schema = json.loads(RESEARCH_CANDIDATES_SCHEMA.read_text(encoding="utf-8"))
        payload = {
            "version": "1.0",
            "generated_at": "2026-03-28T00:00:00Z",
            "source_scan": {
                "tool": "novel-scan",
                "mode": "project-annotate",
                "platform": "番茄",
                "genre": "宫斗宅斗",
                "depth": "quick",
                "report_kind": "real_report",
            },
            "candidates": [
                {
                    "name": "嫡庶婚配真值补证",
                    "kind": "rule",
                    "source": "mcp",
                    "confidence": "medium",
                    "candidate_files": ["设定集/家族/宅门真值表.md"],
                    "evidence_urls": ["https://fanqienovel.com/rank/0_2_246"],
                    "notes": ["candidate only, not canon"],
                }
            ],
        }
        jsonschema.validate(payload, schema)

    def test_scan_contract_doc_mentions_mode_boundaries_and_consumers(self) -> None:
        content = DOC_PATH.read_text(encoding="utf-8")
        for token in (
            "`report-only`",
            "`project-annotate`",
            "`confidence`",
            "`.mighty/market-data.json`",
            "`.mighty/market-adjustments.json`",
            "`.mighty/research-candidates.json`",
            "`novel-package`",
            "`novel-query`",
            "`setting gate`",
            "不能覆盖 canon",
        ):
            self.assertIn(token, content)


if __name__ == "__main__":
    unittest.main()
