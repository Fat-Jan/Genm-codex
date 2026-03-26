from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


CONSUMER_EXPECTATIONS = {
    "skills/novel-init/SKILL.md": [
        "scripts/profile_contract.py",
        "lightweight projection",
        "state.genre_profile",
    ],
    "skills/novel-genre/SKILL.md": [
        "primary project-facing entrance",
        "state.genre_profile",
        ".mighty/content-positioning.json",
        "core profile",
        "platform overlay",
        "bucket overlay",
        "reference files",
    ],
    "skills/novel-outline/SKILL.md": [
        "state.genre_profile",
        "scripts/profile_contract.py",
        ".mighty/content-positioning.json",
        "platform overlay",
        "bucket overlay",
    ],
    "skills/novel-write/SKILL.md": [
        "state.genre_profile",
        "scripts/profile_contract.py",
        ".mighty/content-positioning.json",
        "platform overlay",
        "bucket overlay",
    ],
    "skills/novel-review/SKILL.md": [
        "state.genre_profile",
        "scripts/profile_contract.py",
        ".mighty/content-positioning.json",
        "platform overlay",
        "bucket overlay",
    ],
    "skills/novel-package/SKILL.md": [
        "state.genre_profile",
        "scripts/profile_contract.py",
        ".mighty/content-positioning.json",
        "platform overlay",
        "bucket overlay",
    ],
}


class ProfileConsumerContractTests(unittest.TestCase):
    def test_consumer_skills_use_profile_contract_entry(self) -> None:
        for relative_path, tokens in CONSUMER_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")


if __name__ == "__main__":
    unittest.main()
