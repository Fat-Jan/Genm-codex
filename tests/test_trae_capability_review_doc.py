import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    REPO_ROOT / "docs" / "20-研究实验" / "trae-capability-review-2026-04-02.md"
)


class TraeCapabilityReviewDocTests(unittest.TestCase):
    def test_doc_exists(self) -> None:
        self.assertTrue(DOC_PATH.exists(), "Trae capability review doc is missing")

    def test_doc_mentions_official_doc_surfaces_and_unknowns(self) -> None:
        content = DOC_PATH.read_text(encoding="utf-8")
        for token in (
            "Rules",
            "Skills",
            "Add MCP servers",
            "Use MCP servers in agents",
            "Auto-run & security",
            "Sandbox",
            "doc_verified",
            "unknown",
            "install_mode = unsupported",
        ):
            self.assertIn(token, content)

    def test_doc_mentions_manual_verification_and_gate1_result(self) -> None:
        content = DOC_PATH.read_text(encoding="utf-8")
        for token in (
            "manual_verified",
            "using remote definition",
            "Gate 1",
            "v1.6.1",
            "不正式进入有界 `v2`",
        ):
            self.assertIn(token, content)


if __name__ == "__main__":
    unittest.main()
