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

    def test_high_frequency_consumers_reference_shared_read_manifest(self) -> None:
        manifest_path = REPO_ROOT / "shared" / "references" / "shared" / "consumer-read-manifest.md"
        self.assertTrue(manifest_path.exists())
        manifest = manifest_path.read_text(encoding="utf-8")
        for token in ("baseline-core", "launch-stack", "content-positioning", "fanqie-bucket", "market-adjustments"):
            self.assertIn(token, manifest)
        for relative_path in (
            "skills/novel-outline/SKILL.md",
            "skills/novel-write/SKILL.md",
            "skills/novel-review/SKILL.md",
            "skills/novel-package/SKILL.md",
            "skills/novel-precheck/SKILL.md",
        ):
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn("../../shared/references/shared/consumer-read-manifest.md", content)


if __name__ == "__main__":
    unittest.main()
