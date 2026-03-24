from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]

SKILL_FILES = [
    "skills/novel-genre/SKILL.md",
    "skills/novel-analyze/SKILL.md",
    "skills/novel-precheck/SKILL.md",
]

DOC_FILES = [
    "docs/opening-and-plot-framework/README.md",
    "docs/anti-flattening-framework/README.md",
    "docs/writing-core-framework/README.md",
    "docs/writing-core-framework/04-剧情层次与多线编排接口.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/README.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/README.md",
]


class RepoPathIntegrityTests(unittest.TestCase):
    def test_selected_skill_relative_repo_paths_exist(self):
        pattern = re.compile(r"`((?:\.\./|\.\/)[^`]+)`")
        for relative_path in SKILL_FILES:
            full_path = REPO_ROOT / relative_path
            text = full_path.read_text(encoding="utf-8")
            for match in pattern.finditer(text):
                rel = match.group(1)
                if any(ch in rel for ch in ("<", ">", "*", "{", "}")):
                    continue
                target = (full_path.parent / rel).resolve()
                self.assertTrue(target.exists(), f"{relative_path} missing relative target: {rel}")

    def test_selected_doc_local_links_resolve(self):
        pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
        for relative_path in DOC_FILES:
            full_path = REPO_ROOT / relative_path
            text = full_path.read_text(encoding="utf-8")
            for match in pattern.finditer(text):
                target = match.group(1).strip()
                if not target or target.startswith("http://") or target.startswith("https://") or target.startswith("/"):
                    continue
                resolved = (full_path.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"{relative_path} broken local link: {target}")


if __name__ == "__main__":
    unittest.main()
