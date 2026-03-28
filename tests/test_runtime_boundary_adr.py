import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ADR_PATH = REPO_ROOT / "docs" / "00-当前有效" / "runtime-boundary-adr.md"


class RuntimeBoundaryAdrTests(unittest.TestCase):
    def test_runtime_boundary_adr_exists(self) -> None:
        self.assertTrue(ADR_PATH.exists(), "runtime boundary ADR is missing")

    def test_runtime_boundary_adr_mentions_core_non_goals(self) -> None:
        content = ADR_PATH.read_text(encoding="utf-8")
        for token in (
            "`repo truth + sidecar + MCP`",
            "第二真值中心",
            "daemon",
            "scheduler",
            "plugin framework",
            "orchestration runtime",
            "`novel-scan`",
            "研究可以做，但不进 v1.5 实装",
        ):
            self.assertIn(token, content)


if __name__ == "__main__":
    unittest.main()
