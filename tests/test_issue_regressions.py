from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class IssueRegressionTests(unittest.TestCase):
    def test_p0_1_novel_write_numbering_is_sequential(self):
        content = (REPO_ROOT / "skills/novel-write/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("10. When the chapter needs stronger execution craft", content)
        self.assertIn("11. If the platform is 番茄", content)
        self.assertIn("12. If Fanqie writing is active", content)
        self.assertNotIn("\n10. If the platform is 番茄", content)

    def test_p0_2_launch_stack_has_default_workflow_trigger(self):
        expected = "python3 scripts/fanqie_launch_stack.py --project-root <project_root> --chapter 003 --chapters 001-003 --mode writeback --writeback"
        for relative_path in ("docs/default-workflows.md", "docs/start-here.md", "docs/skill-usage.md"):
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn(expected, content, relative_path)

    def test_p0_3_novel_init_declares_preselect_placeholder(self):
        content = (REPO_ROOT / "skills/novel-init/SKILL.md").read_text(encoding="utf-8")
        for token in (
            '"phase": "preselect"',
            '"premise_line": ""',
            '"primary_pivot": ""',
            '"compiler_output"',
            "launch_stack_phase",
            "launch_stack_drift_signal",
        ):
            self.assertIn(token, content)

    def test_p1_1_and_p1_2_novel_learn_reads_framework_and_launch_stack(self):
        content = (REPO_ROOT / "skills/novel-learn/SKILL.md").read_text(encoding="utf-8")
        for token in (
            "../../docs/writing-core-framework/README.md",
            "../../docs/writing-core-framework/07-memory-压缩信号约定.md",
            "../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md",
            ".mighty/launch-stack.json",
            "drift_signal",
        ):
            self.assertIn(token, content)

    def test_p1_3_novel_close_no_longer_reads_child_skill_contracts(self):
        content = (REPO_ROOT / "skills/novel-close/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("../../docs/default-workflows.md", content)
        for token in (
            "../novel-review/SKILL.md",
            "../novel-fix/SKILL.md",
            "../novel-polish/SKILL.md",
            "../novel-rewrite/SKILL.md",
        ):
            self.assertNotIn(token, content)

    def test_p2_1_task_plan_archived_and_single_active(self):
        self.assertTrue((REPO_ROOT / "task_plan_archive.md").exists())
        content = (REPO_ROOT / "task_plan.md").read_text(encoding="utf-8")
        self.assertEqual(content.count("# Task Plan:"), 1)

    def test_p2_2_docs_index_exists(self):
        content = (REPO_ROOT / "docs/INDEX.md").read_text(encoding="utf-8")
        for token in ("文档索引", "start-here.md", "default-workflows.md", "research/fanqie"):
            self.assertIn(token, content)

    def test_p2_3_experiment_docs_moved_under_research(self):
        moved = {
            "docs/fanqie-evil-dual-female-substitute-candidate.md": "docs/research/fanqie/fanqie-evil-dual-female-substitute-candidate.md",
            "docs/fanqie-evil-gongdou-production-deep-dive.md": "docs/research/fanqie/fanqie-evil-gongdou-production-deep-dive.md",
            "docs/fanqie-evil-gongdou-production-template.md": "docs/research/fanqie/fanqie-evil-gongdou-production-template.md",
            "docs/fanqie-evil-gongdou-submission-assessment.md": "docs/research/fanqie/fanqie-evil-gongdou-submission-assessment.md",
            "docs/fanqie-evil-qinggan-production-candidate.md": "docs/research/fanqie/fanqie-evil-qinggan-production-candidate.md",
            "docs/fanqie-evil-tianchong-experiment-status.md": "docs/research/fanqie/fanqie-evil-tianchong-experiment-status.md",
            "docs/fanqie-evil-variant-comparison.md": "docs/research/fanqie/fanqie-evil-variant-comparison.md",
            "docs/fanqie-writer-zone-lessons.md": "docs/research/fanqie/fanqie-writer-zone-lessons.md",
        }
        for old_path, new_path in moved.items():
            self.assertFalse((REPO_ROOT / old_path).exists(), old_path)
            self.assertTrue((REPO_ROOT / new_path).exists(), new_path)

    def test_p2_4_smoke_readme_declares_retention_policy(self):
        content = (REPO_ROOT / "smoke/README.md").read_text(encoding="utf-8")
        for token in ("保留策略", "基线样本", "派生副本", "清理"):
            self.assertIn(token, content)


if __name__ == "__main__":
    unittest.main()
