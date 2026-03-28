import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "build_active_context.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_active_context", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ActiveContextContractTests(unittest.TestCase):
    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/build_active_context.py is missing")

    def test_state_schema_mentions_active_context_as_sidecar_pointer(self) -> None:
        content = (REPO_ROOT / "shared" / "references" / "shared" / "state-schema.md").read_text(encoding="utf-8")
        self.assertIn("active_context", content)
        self.assertIn(".mighty/active-context.json", content)
        self.assertIn("sidecar", content)

    def test_state_template_mentions_active_context_pointer(self) -> None:
        content = (REPO_ROOT / "shared" / "templates" / "state-v5-template.json").read_text(encoding="utf-8")
        self.assertIn('"active_context"', content)
        self.assertIn(".mighty/active-context.json", content)

    def test_skill_contracts_reference_active_context(self) -> None:
        expectations = {
            "skills/novel-write/SKILL.md": ".mighty/active-context.json",
            "skills/novel-review/SKILL.md": ".mighty/active-context.json",
            "skills/novel-status/SKILL.md": ".mighty/active-context.json",
            "skills/novel-query/SKILL.md": ".mighty/active-context.json",
            "docs/00-当前有效/state-thinning-and-setting-sync.md": ".mighty/active-context.json",
        }
        for relative_path, token in expectations.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn(token, content, f"{relative_path} missing token: {token}")


class ActiveContextHelperTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        mighty = root / ".mighty"
        mighty.mkdir(parents=True)
        write_json(
            mighty / "state.json",
            {
                "meta": {
                    "title": "测试书",
                    "updated_at": "2026-03-25T00:00:00Z",
                },
                "progress": {
                    "current_chapter": 4,
                    "total_words": 12000,
                },
                "entities": {
                    "characters": {
                        "protagonist": {
                            "name": "周既明",
                            "aliases": ["既明"],
                            "location": {
                                "current": "曜石互联大厦",
                            },
                            "status": ["刚完成反击"],
                            "current_goals": ["下一章继续追账"],
                        },
                        "active": [
                            {"name": "韩振", "role": "对手"},
                            {"name": "林乔", "role": "HRBP"},
                        ],
                    },
                    "locations": {
                        "current": "曜石互联大厦",
                        "important": ["曜石互联大厦", "会议室"],
                    },
                    "factions": {
                        "active": [{"name": "曜石互联"}],
                    },
                    "items": {
                        "tracked": [{"name": "劳动合同电子版"}],
                        "protagonist_inventory": ["劳动合同电子版"],
                    },
                },
                "plot_threads": {
                    "foreshadowing": {
                        "active": [
                            {"id": "f1", "name": "赔付系统来源", "status": "active"},
                        ],
                        "pending": [
                            {"id": "f2", "name": "董事会旧账", "status": "pending"},
                        ],
                        "warning": [],
                        "overdue": [],
                        "resolved": [
                            {"id": "f0", "name": "已回收伏笔", "status": "resolved"},
                        ],
                    }
                },
                "reading_power_state": {
                    "active_hooks": [
                        {"id": "h1", "content": "下一章先看谁翻桌"},
                    ]
                },
                "summaries_index": {
                    "2": {"summary": "第二章摘要"},
                    "3": {"summary": "第三章摘要"},
                    "4": {"summary": "第四章摘要"},
                },
                "active_launch_grammar": "resource-climb",
                "active_primary_pivot": "赔付到账",
                "launch_stack_phase": "locked",
                "launch_stack_drift_signal": "watch",
            },
        )
        write_json(
            mighty / "state-archive.json",
            {
                "chapter_meta": {},
                "chapter_snapshots": {},
                "summaries_index": {
                    "1": {"summary": "第一章摘要"},
                },
            },
        )
        write_json(
            mighty / "setting-gate.json",
            {
                "status": "review_required",
                "blocking_gaps": [{"key": "world_rule_support"}],
                "minimal_next_action": {
                    "action": "novel-setting",
                    "suggested_commands": ["请先补世界规则卡。"],
                },
            },
        )
        write_json(
            mighty / "learned-patterns.json",
            {
                "version": "1.0",
                "data": {
                    "recent_guardrails": {
                        "must_avoid": ["解释腔"],
                        "must_preserve": ["赔付到账后的代价感"],
                        "next_chapter_watchpoints": ["不要让韩振变成功能位"],
                        "expires_after_chapter": 5,
                    }
                },
            },
        )
        write_json(
            mighty / "market-adjustments.json",
            {
                "version": "1.0",
                "data": {
                    "adjustments": [{"id": "scan-frontload-conflict"}],
                },
            },
        )
        write_json(
            mighty / "launch-stack.json",
            {
                "launch_grammar": {"primary": "resource-climb"},
                "primary_pivot": "赔付到账",
            },
        )
        return root

    def test_load_state_and_sidecars_reads_expected_files(self) -> None:
        module = load_module()
        root = self.make_project_root()

        loaded = module.load_state_and_sidecars(root)

        self.assertEqual(loaded["state"]["meta"]["title"], "测试书")
        self.assertEqual(loaded["gate"]["status"], "review_required")
        self.assertIn("recent_guardrails", loaded["learned"])
        self.assertEqual(loaded["launch_stack"]["primary_pivot"], "赔付到账")

    def test_select_recent_summaries_prefers_recent_live_rows_then_archive(self) -> None:
        module = load_module()
        root = self.make_project_root()
        loaded = module.load_state_and_sidecars(root)

        summaries = module.select_recent_summaries(loaded["state"], loaded["state_archive"], limit=3)

        self.assertEqual([row["chapter"] for row in summaries], ["2", "3", "4"])
        self.assertEqual(summaries[-1]["summary"], "第四章摘要")

    def test_select_active_hooks_excludes_resolved_and_keeps_active_signal(self) -> None:
        module = load_module()
        root = self.make_project_root()
        loaded = module.load_state_and_sidecars(root)

        hooks = module.select_active_hooks(loaded["state"])

        names = {hook["name"] for hook in hooks if "name" in hook}
        self.assertIn("赔付系统来源", names)
        self.assertIn("董事会旧账", names)
        self.assertNotIn("已回收伏笔", names)

    def test_select_relevant_entities_keeps_current_writing_slice(self) -> None:
        module = load_module()
        root = self.make_project_root()
        loaded = module.load_state_and_sidecars(root)

        entities = module.select_relevant_entities(loaded["state"])

        self.assertEqual(entities["protagonist"]["name"], "周既明")
        self.assertEqual(len(entities["active_characters"]), 2)
        self.assertIn("曜石互联", entities["active_factions"])
        self.assertIn("劳动合同电子版", entities["tracked_items"])

    def test_build_active_context_returns_narrow_sidecar_shape(self) -> None:
        module = load_module()
        root = self.make_project_root()
        loaded = module.load_state_and_sidecars(root)

        context = module.build_active_context(
            state=loaded["state"],
            state_archive=loaded["state_archive"],
            learned=loaded["learned"],
            market=loaded["market"],
            gate=loaded["gate"],
            launch_stack=loaded["launch_stack"],
            generated_at="2026-03-25T00:00:00Z",
        )

        self.assertEqual(context["version"], "1.0")
        self.assertEqual(context["title"], "测试书")
        self.assertEqual(context["summary_window"]["count"], 4)
        self.assertIn("recent_summaries", context)
        self.assertIn("active_hooks", context)
        self.assertIn("relevant_entities", context)
        self.assertEqual(context["write_readiness"]["gate_status"], "review_required")
        self.assertEqual(context["launch_stack"]["active_launch_grammar"], "resource-climb")
        self.assertIn("guardrail_summary", context)
        self.assertTrue(context["guardrail_summary"]["has_recent_guardrails"])
        self.assertEqual(context["guardrail_summary"]["must_avoid_count"], 1)
        self.assertEqual(context["guardrail_summary"]["must_preserve_count"], 1)
        self.assertEqual(context["guardrail_summary"]["watchpoint_count"], 1)
        self.assertEqual(context["guardrail_summary"]["expires_after_chapter"], 5)
        self.assertEqual(context["guardrail_summary"]["source_sidecar"], ".mighty/learned-patterns.json")
        self.assertNotIn("recent_guardrails", context)
        self.assertNotIn("chapter_meta", context)
        self.assertNotIn("knowledge_base", context)
        self.assertEqual(context["relevant_entities"]["protagonist"]["name"], "周既明")
        self.assertEqual(context["relevant_entities"]["protagonist"]["aliases"], ["既明"])
        self.assertNotIn("status", context["relevant_entities"]["protagonist"])
        self.assertNotIn("current_goals", context["relevant_entities"]["protagonist"])

    def test_cli_writes_active_context_sidecar(self) -> None:
        module = load_module()
        root = self.make_project_root()

        payload = module.main([str(root), "--timestamp", "2026-03-25T00:00:00Z"])

        sidecar_path = root / ".mighty" / "active-context.json"
        self.assertTrue(sidecar_path.exists())
        written = json.loads(sidecar_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["active_context_file"], str(sidecar_path))
        self.assertEqual(written["generated_at"], "2026-03-25T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
