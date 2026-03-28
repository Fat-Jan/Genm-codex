import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


QUICK_DOCS = [
    "docs/anti-flattening-framework/QUICK.md",
    "docs/opening-and-plot-framework/QUICK.md",
    "docs/writing-core-framework/QUICK.md",
]

RULE_CACHES = [
    "docs/anti-flattening-framework/rule-cache.json",
    "docs/opening-and-plot-framework/rule-cache.json",
    "docs/writing-core-framework/rule-cache.json",
]


class V14DocAssetTests(unittest.TestCase):
    def test_quick_docs_exist_and_explain_runtime_role(self) -> None:
        for relative_path in QUICK_DOCS:
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn("速查卡", content, relative_path)
            self.assertIn("不是新的规则源", content, relative_path)

    def test_rule_caches_parse_and_share_contract_shape(self) -> None:
        required_keys = {
            "version",
            "framework",
            "core_guardrails",
            "conditional_guardrails",
            "diagnostic_signals",
            "minimal_fixes",
            "root_cause_categories",
        }
        for relative_path in RULE_CACHES:
            payload = json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
            self.assertEqual(required_keys - set(payload.keys()), set(), relative_path)
            self.assertIsInstance(payload["core_guardrails"], list, relative_path)
            self.assertIsInstance(payload["conditional_guardrails"], dict, relative_path)

    def test_entry_docs_surface_v14_assets(self) -> None:
        expectations = {
            "README.md": [
                "v1.4-roadmap.md",
                "docs/anti-flattening-framework/QUICK.md",
                "docs/00-当前有效/chapter-structure-fields-design.md",
                "docs/00-当前有效/sample-library-index.md",
            ],
            "docs/00-当前有效/start-here.md": [
                "docs/anti-flattening-framework/QUICK.md",
                "docs/opening-and-plot-framework/rule-cache.json",
                "docs/00-当前有效/bucket-profile-slug-mapping.md",
                "docs/00-当前有效/chapter-structure-fields-design.md",
            ],
            "docs/00-当前有效/skill-usage.md": [
                "docs/anti-flattening-framework/rule-cache.json",
                "docs/opening-and-plot-framework/QUICK.md",
                "docs/writing-core-framework/rule-cache.json",
            ],
            "docs/00-当前有效/default-workflows.md": [
                "docs/anti-flattening-framework/QUICK.md",
                "docs/opening-and-plot-framework/rule-cache.json",
                "docs/writing-core-framework/QUICK.md",
            ],
        }
        for relative_path, tokens in expectations.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_structure_and_sample_docs_capture_v14_contracts(self) -> None:
        structure_doc = (REPO_ROOT / "docs/00-当前有效/chapter-structure-fields-design.md").read_text(encoding="utf-8")
        for token in (
            "conflict_type",
            "protagonist_arc",
            "opponent_mode",
            "gain_type",
            "cost_visibility",
            "chapter_end_style",
            "novel-precheck",
        ):
            self.assertIn(token, structure_doc)

        sample_index = (REPO_ROOT / "docs/00-当前有效/sample-library-index.md").read_text(encoding="utf-8")
        self.assertIn("成婚前三日，我先改了侯府嫁妆单", sample_index)
        self.assertIn("Regression", sample_index)

        mapping_doc = (REPO_ROOT / "docs/00-当前有效/bucket-profile-slug-mapping.md").read_text(encoding="utf-8")
        self.assertIn("profile slug", mapping_doc)
        self.assertIn("bucket slug", mapping_doc)

        inventory_doc = (REPO_ROOT / "docs/00-当前有效/bucket-overlay-inventory.md").read_text(encoding="utf-8")
        self.assertIn("P0", inventory_doc)
        self.assertIn("bucket overlay", inventory_doc)
