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
        for relative_path in ("docs/00-当前有效/default-workflows.md", "docs/00-当前有效/start-here.md", "docs/00-当前有效/skill-usage.md"):
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
        self.assertIn("../../docs/00-当前有效/default-workflows.md", content)
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

    def test_p2_2b_root_roadmap_exists_and_tracks_status(self):
        content = (REPO_ROOT / "docs/90-归档/阶段/v1.1-roadmap.md").read_text(encoding="utf-8")
        for token in ("Status:", "[planned]", "[deferred]", "主线 A", "主线 B"):
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

    def test_p2_5_boundary_doc_locks_memory_and_runtime_limits(self):
        content = (REPO_ROOT / "docs/00-当前有效/v1-boundary.md").read_text(encoding="utf-8")
        for token in ("MCP memory", "协调记忆", "plugin framework", "orchestration runtime"):
            self.assertIn(token, content)

    def test_p2_6_docs_roadmap_path_is_only_a_pointer(self):
        content = (REPO_ROOT / "docs/00-当前有效/v1.1-roadmap.md").read_text(encoding="utf-8")
        self.assertIn("主 roadmap", content)
        self.assertIn("/Users/arm/Desktop/vscode/Genm-codex/docs/90-归档/阶段/v1.1-roadmap.md", content)

    def test_p2_7_docs_reflect_phase2_fetch_snapshot_log_updates(self):
        usage = (REPO_ROOT / "docs/00-当前有效/skill-usage.md").read_text(encoding="utf-8")
        workflows = (REPO_ROOT / "docs/00-当前有效/default-workflows.md").read_text(encoding="utf-8")
        start_here = (REPO_ROOT / "docs/00-当前有效/start-here.md").read_text(encoding="utf-8")
        state_doc = (REPO_ROOT / "docs/00-当前有效/state-thinning-and-setting-sync.md").read_text(encoding="utf-8")
        for token in ("--show-provider-config", "memory-context", "trace log", "snapshot artifact", "content-positioning"):
            self.assertIn(token, usage + start_here + state_doc)
        self.assertIn("auto-compile `launch-stack`", workflows)

    def test_p3_1_sidecar_freshness_registry_is_exposed(self):
        registry = REPO_ROOT / "shared" / "templates" / "sidecar-freshness-registry-v1.json"
        self.assertTrue(registry.exists())
        state_doc = (REPO_ROOT / "docs/00-当前有效/state-thinning-and-setting-sync.md").read_text(encoding="utf-8")
        self.assertIn("sidecar-freshness-registry-v1.json", state_doc)
        self.assertIn("freshness", state_doc)

    def test_p3_2_upstream_structure_contract_is_exposed(self):
        contract = REPO_ROOT / "docs/00-当前有效/upstream-structure-contract.md"
        self.assertTrue(contract.exists())
        contract_text = contract.read_text(encoding="utf-8")
        for token in ("creative-brief", "content-positioning", "launch-stack", "总纲"):
            self.assertIn(token, contract_text)
        docs = "".join(
            (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for relative_path in (
                "docs/00-当前有效/default-workflows.md",
                "docs/00-当前有效/start-here.md",
                "docs/00-当前有效/skill-usage.md",
            )
        )
        self.assertIn("upstream-structure-contract.md", docs)
        self.assertIn("creative-brief", docs)

    def test_p3_3_quality_route_contract_is_shared_by_review_precheck_package(self):
        contract = REPO_ROOT / "docs/00-当前有效/quality-route-contract.md"
        self.assertTrue(contract.exists())
        contract_text = contract.read_text(encoding="utf-8")
        for token in ("route_signal", "hard_blocker", "revise_before_submit", "packaging_hold"):
            self.assertIn(token, contract_text)
        for relative_path in (
            "skills/novel-review/SKILL.md",
            "skills/novel-precheck/SKILL.md",
            "skills/novel-package/SKILL.md",
        ):
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn("../../docs/00-当前有效/quality-route-contract.md", content)

    def test_p3_4_upstream_contract_reaches_init_outline_package(self):
        for relative_path in (
            "skills/novel-init/SKILL.md",
            "skills/novel-outline/SKILL.md",
            "skills/novel-package/SKILL.md",
        ):
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn("creative-brief", content)
            self.assertIn("../../docs/00-当前有效/upstream-structure-contract.md", content)

    def test_p3_5_fanqie_first_freeze_is_declared(self):
        freeze_doc = REPO_ROOT / "docs/20-研究实验/fanqie-first-frozen-template-2026-03-26.md"
        route_doc = REPO_ROOT / "docs/20-研究实验/quality-route-smoke-2026-03-26.md"
        self.assertTrue(freeze_doc.exists())
        self.assertTrue(route_doc.exists())
        workflows = (REPO_ROOT / "docs/00-当前有效/default-workflows.md").read_text(encoding="utf-8")
        self.assertIn("她升职那天，前上司成了我合租室友", workflows)
        self.assertIn("恶女 x 宫斗宅斗", workflows)
        self.assertNotIn("暂无已冻结样本", workflows)
        self.assertNotIn("首个可投样本：\n  - 暂无", workflows)

    def test_p3_6_total_outline_contract_is_exposed(self):
        contract = REPO_ROOT / "docs/00-当前有效/total-outline-structure-contract.md"
        self.assertTrue(contract.exists())
        contract_text = contract.read_text(encoding="utf-8")
        for token in ("开端", "发展", "转折", "高潮", "卷末钩子", "主副线迁移", "关键兑现"):
            self.assertIn(token, contract_text)
        docs = "".join(
            (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for relative_path in (
                "docs/00-当前有效/default-workflows.md",
                "docs/00-当前有效/start-here.md",
                "docs/00-当前有效/skill-usage.md",
            )
        )
        self.assertIn("total-outline-structure-contract.md", docs)

    def test_p2_8_profile_calibration_doc_is_currently_exposed(self):
        calibration = (REPO_ROOT / "docs/00-当前有效/profile-calibration-and-bucket-mapping.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        index_doc = (REPO_ROOT / "docs/INDEX.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "docs/90-归档/阶段/v1.1-roadmap.md").read_text(encoding="utf-8")
        for token in ("主 profile", "主 bucket", "strong_tags", "narrative_modes", "tone_guardrails"):
            self.assertIn(token, calibration)
        self.assertIn("profile-calibration-and-bucket-mapping.md", readme)
        self.assertIn("profile-calibration-and-bucket-mapping.md", index_doc)
        self.assertIn("Status: `[done]`", roadmap)

    def test_v15_novel_analyze_has_current_workflow_entry(self):
        workflows = (REPO_ROOT / "docs/00-当前有效/default-workflows.md").read_text(encoding="utf-8")
        start_here = (REPO_ROOT / "docs/00-当前有效/start-here.md").read_text(encoding="utf-8")
        boundary = (REPO_ROOT / "docs/00-当前有效/v1-boundary.md").read_text(encoding="utf-8")
        self.assertIn("novel-analyze", workflows)
        self.assertIn("novel-analyze", start_here)
        self.assertIn("novel-analyze", boundary)

    def test_v15_novel_spinoff_is_explicitly_non_default_but_accessible(self):
        workflows = (REPO_ROOT / "docs/00-当前有效/default-workflows.md").read_text(encoding="utf-8")
        start_here = (REPO_ROOT / "docs/00-当前有效/start-here.md").read_text(encoding="utf-8")
        boundary = (REPO_ROOT / "docs/00-当前有效/v1-boundary.md").read_text(encoding="utf-8")
        self.assertIn("novel-spinoff", workflows)
        self.assertIn("novel-spinoff", start_here)
        self.assertIn("novel-spinoff", boundary)
        self.assertIn("不属于默认工作流", workflows)


    def test_v16_mainline_entry_pointers_are_consistent(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        index_doc = (REPO_ROOT / "docs/INDEX.md").read_text(encoding="utf-8")
        start_here = (REPO_ROOT / "docs/00-当前有效/start-here.md").read_text(encoding="utf-8")
        usage = (REPO_ROOT / "docs/00-当前有效/skill-usage.md").read_text(encoding="utf-8")
        retention = (REPO_ROOT / "docs/00-当前有效/root-retention-policy.md").read_text(encoding="utf-8")
        trae_context = (REPO_ROOT / ".trae/rules/project-context.md").read_text(encoding="utf-8")

        self.assertIn("当前主线版本：`v1.6`", readme)
        self.assertIn("[v1.6-roadmap.md](/Users/arm/Desktop/vscode/Genm-codex/v1.6-roadmap.md) — `active`", index_doc)
        self.assertIn("[v1.5-roadmap.md](/Users/arm/Desktop/vscode/Genm-codex/v1.5-roadmap.md) — `archived(mainline-upstream-reference)`", index_doc)
        self.assertIn("**`v1.6` 宿主支持 / 跨宿主基础层**", start_here)
        self.assertIn("**历史 `v1.5` 治理 / contract / registry / consumer 接线**", start_here)
        self.assertIn("当前主线已切到 `v1.6`", usage)
        self.assertIn("`v1.6-roadmap.md` → 当前主线", retention)
        self.assertIn("`v1.5-roadmap.md` → 紧邻当前主线的上游参考", retention)
        self.assertIn("| `v1.6-roadmap.md` | 当前主线路线图 |", trae_context)
        self.assertIn("| `v1.5-roadmap.md` | 直接上游参考 roadmap |", trae_context)
        self.assertNotIn("| `v1.5-roadmap.md` | 当前主线路线图 |", trae_context)


if __name__ == "__main__":
    unittest.main()
