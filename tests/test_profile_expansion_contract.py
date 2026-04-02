from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "00-当前有效" / "profile-expansion-contract.md"
README_PATH = REPO_ROOT / "shared" / "profiles" / "README.md"


class ProfileExpansionContractTests(unittest.TestCase):
    def test_profile_expansion_contract_doc_exists(self) -> None:
        self.assertTrue(DOC_PATH.exists(), "profile expansion contract doc is missing")

    def test_contract_doc_mentions_minimum_profile_rules(self) -> None:
        content = DOC_PATH.read_text(encoding="utf-8")
        for token in (
            "`profile.yaml`",
            "`name`",
            "`display_name`",
            "`description`",
            "`version`",
            "`platform_positioning`",
            "`bucket overlay`",
            "`fanqie primary_bucket`",
            "`tests/test_profile_contract.py`",
            "`tests/test_content_positioning.py`",
            "`bash scripts/validate-migration.sh`",
        ):
            self.assertIn(token, content)

    def test_profiles_readme_points_to_expansion_contract(self) -> None:
        content = README_PATH.read_text(encoding="utf-8")
        self.assertIn("profile-expansion-contract.md", content)


if __name__ == "__main__":
    unittest.main()
