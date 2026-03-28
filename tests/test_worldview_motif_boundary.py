from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class WorldviewMotifBoundaryTests(unittest.TestCase):
    def test_creative_brief_keeps_motif_selection_input(self):
        content = (REPO_ROOT / "shared/templates/project/creative-brief.md").read_text(encoding="utf-8")
        for token in (
            "### 母题选择",
            "shared/references/writing/worldview-motif-catalog.md",
            "建议不要在立项阶段一次叠超过 `3` 个母题。",
            "| **世界观母题** |",
            "| **机制母题** |",
            "| **包装 / 关系母题** |",
        ):
            self.assertIn(token, content)

    def test_novel_init_locks_motif_boundary_as_upstream_input(self):
        content = (REPO_ROOT / "skills/novel-init/SKILL.md").read_text(encoding="utf-8")
        for token in (
            "../../shared/references/writing/worldview-motif-catalog.md",
            "`1` worldview motif",
            "optional `1` mechanism motif",
            "optional `1` packaging / relationship motif",
            "do not turn the motif catalog into a full-world encyclopedia during initialization",
            "write a lightweight note under `设定集/世界观/` instead of a long-form world bible",
            "keep them as high-level premise inputs; do not pretend all motif implications are already canon.",
        ):
            self.assertIn(token, content)

    def test_novel_outline_limits_motif_use_and_prevents_outline_pollution(self):
        content = (REPO_ROOT / "skills/novel-outline/SKILL.md").read_text(encoding="utf-8")
        for token in (
            "../../shared/references/writing/worldview-motif-catalog.md",
            "`1` worldview motif",
            "optional `1` mechanism motif",
            "optional `1` packaging motif",
            "do not dump unused motif cards into the outline text",
        ):
            self.assertIn(token, content)

    def test_novel_package_keeps_motif_use_as_sharpening_layer(self):
        content = (REPO_ROOT / "skills/novel-package/SKILL.md").read_text(encoding="utf-8")
        for token in (
            "../../shared/references/writing/worldview-motif-catalog.md",
            "use selected motif cues only to sharpen:",
            "world hook legibility",
            "do not stack multiple motif names into the outward package copy",
        ):
            self.assertIn(token, content)

    def test_entry_docs_continue_pointing_to_brief_and_motif_catalog(self):
        for relative_path in (
            "docs/00-当前有效/start-here.md",
            "docs/00-当前有效/skill-usage.md",
        ):
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn("creative-brief", content, relative_path)
            self.assertIn("worldview-motif-catalog.md", content, relative_path)


if __name__ == "__main__":
    unittest.main()
