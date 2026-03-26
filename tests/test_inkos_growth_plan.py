import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]

TRANSACTION_SCHEMA_PATH = REPO_ROOT / "shared" / "references" / "shared" / "chapter-transaction-schema.md"
WORKFLOW_TEMPLATE_PATH = REPO_ROOT / "shared" / "templates" / "workflow-state-v2.json"
ACTIVE_CONTEXT_SCRIPT_PATH = REPO_ROOT / "scripts" / "build_active_context.py"
POST_WRITE_LINT_SCRIPT_PATH = REPO_ROOT / "scripts" / "post_write_lint.py"
IMPORT_EXISTING_SCRIPT_PATH = REPO_ROOT / "scripts" / "import_existing_chapters.py"
VOLUME_SUMMARIES_SCRIPT_PATH = REPO_ROOT / "scripts" / "build_volume_summaries.py"
GUARDRAIL_EXPECTATIONS = {
    "docs/writing-core-framework/07-memory-压缩信号约定.md": [
        "recent_guardrails",
        "must_avoid",
        "must_preserve",
        "next_chapter_watchpoints",
        "expires_after_chapter",
    ],
    "skills/novel-review/SKILL.md": [
        "recent_guardrails",
        "must_avoid",
        "must_preserve",
        "next_chapter_watchpoints",
        "expires_after_chapter",
    ],
    "skills/novel-write/SKILL.md": [
        "recent_guardrails",
        "must_avoid",
        "must_preserve",
        "next_chapter_watchpoints",
    ],
    "skills/novel-learn/SKILL.md": [
        "recent_guardrails",
    ],
    "skills/novel-status/SKILL.md": [
        "recent_guardrails",
    ],
}
REFERENCE_LEARN_EXPECTATIONS = {
    "skills/novel-learn/SKILL.md": [
        "chapter range",
        "local file",
        "retrievable URL",
        "../../scripts/acquire_source_text.py",
        ".mighty/learned-patterns.json",
    ],
    "docs/90-归档/阶段/phase-5b-p0-learn-smoke-plan.md": [
        "本地文件",
        "retrievable URL",
        ".mighty/learned-patterns.json",
        "style_profile.json",
    ],
    "docs/90-归档/阶段/phase-5b-p0-learn-smoke-results.md": [
        "本地文件",
        "retrievable URL",
        ".mighty/learned-patterns.json",
        "style_profile.json",
    ],
}
IMPORT_BRIDGE_EXPECTATIONS = {
    "skills/novel-resume/SKILL.md": [
        ".mighty/import-report.json",
        "novel-index build",
    ],
    "skills/novel-index/SKILL.md": [
        ".mighty/import-report.json",
    ],
    "skills/novel-sync/SKILL.md": [
        ".mighty/import-report.json",
        "sync-review",
    ],
    "skills/novel-query/SKILL.md": [
        ".mighty/import-report.json",
    ],
    "docs/00-当前有效/default-workflows.md": [
        "已有稿接入",
        "import-report",
    ],
    "docs/00-当前有效/start-here.md": [
        "已有稿接入",
        "import-report",
    ],
    "docs/00-当前有效/skill-usage.md": [
        "已有稿接入",
        "import-report",
    ],
}
VOLUME_SUMMARY_EXPECTATIONS = {
    "skills/novel-status/SKILL.md": [
        ".mighty/volume-summaries.json",
        "volume summaries",
    ],
    "skills/novel-query/SKILL.md": [
        ".mighty/volume-summaries.json",
        "volume summaries",
    ],
    "docs/00-当前有效/state-thinning-and-setting-sync.md": [
        ".mighty/volume-summaries.json",
    ],
}

TRANSACTION_EXPECTED_STEPS = [
    "gate-check",
    "draft",
    "close",
    "maintenance",
    "snapshot",
]

SKILL_EXPECTATIONS = {
    "skills/novel-write/SKILL.md": [
        "chapter transaction",
        "gate-check",
        "draft",
        "close",
        "maintenance",
        "snapshot",
    ],
    "skills/novel-close/SKILL.md": [
        "chapter transaction",
        "transaction contract",
        "close",
    ],
    "skills/novel-workflow/SKILL.md": [
        "gate-check",
        "draft",
        "close",
        "maintenance",
        "snapshot",
        "workflow-state-v2.json",
    ],
    "skills/novel-resume/SKILL.md": [
        "gate-check",
        "draft",
        "close",
        "maintenance",
        "snapshot",
        "safest recovery point",
    ],
}

ENTRY_DOC_EXPECTATIONS = {
    "docs/00-当前有效/default-workflows.md": "chapter transaction",
    "docs/00-当前有效/start-here.md": "chapter transaction",
    "docs/00-当前有效/skill-usage.md": "chapter transaction",
}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def scaffold_project(root: Path) -> None:
    write_json(
        root / ".mighty" / "state.json",
        {
            "version": "5.0",
            "meta": {
                "title": "事务化测试项目",
                "genre": "都市脑洞",
                "platform": "番茄",
                "target_chapters": 5,
                "updated_at": "2026-03-25T00:00:00Z",
            },
            "progress": {
                "current_chapter": 1,
                "total_words": 3200,
                "last_write_chapter": 1,
            },
            "genre_profile": {
                "bucket": "都市脑洞",
            },
            "entities": {
                "characters": {
                    "protagonist": {
                        "name": "周既明",
                        "location": {
                            "current": "曜石互联大厦",
                        },
                        "inventory": [
                            "劳动合同电子版",
                        ],
                    },
                    "active": [
                        {
                            "name": "韩振",
                            "role": "产品总监",
                        },
                        {
                            "name": "林乔",
                            "role": "HRBP",
                        },
                    ],
                },
                "locations": {
                    "current": "曜石互联大厦",
                    "important": ["曜石互联大厦"],
                },
                "factions": {
                    "active": ["曜石互联"],
                },
                "items": {
                    "tracked": ["劳动合同电子版"],
                    "protagonist_inventory": ["劳动合同电子版"],
                },
            },
            "chapter_meta": {
                "1": {
                    "summary": "主角完成第一轮反击。",
                    "last_close_route": "novel-fix",
                }
            },
        },
    )
    write_json(
        root / ".mighty" / "setting-gate.json",
        {
            "version": "1.0",
            "status": "passed",
            "checked_after": "write-post",
            "blocking_gaps": [],
            "review_items": [],
            "minimal_next_action": {
                "action": "novel-write",
                "suggested_commands": ["请使用 novel-write skill 继续下一章。"],
            },
        },
    )
    write_text(root / "大纲" / "总纲.md", "主角进入事务化写作链。")
    write_text(root / "大纲" / "章纲" / "第001章.md", "主角先过 gate，再写，再收口。")
    write_text(root / "设定集" / "角色" / "主角.md", "# 主角\n")
    write_text(root / "设定集" / "力量体系.md", "# 世界规则\n")
    write_text(root / "chapters" / "第001章.md", "主角先过 gate，再写，再收口。" * 80)


class InkosGrowthContractTests(unittest.TestCase):
    def test_transaction_schema_exists_and_mentions_fixed_steps(self):
        self.assertTrue(TRANSACTION_SCHEMA_PATH.exists(), "Missing chapter transaction schema")
        content = TRANSACTION_SCHEMA_PATH.read_text(encoding="utf-8")
        for token in TRANSACTION_EXPECTED_STEPS:
            self.assertIn(token, content)

    def test_workflow_state_v2_template_exists_and_mentions_fixed_steps(self):
        self.assertTrue(WORKFLOW_TEMPLATE_PATH.exists(), "Missing workflow-state-v2 template")
        content = WORKFLOW_TEMPLATE_PATH.read_text(encoding="utf-8")
        for token in TRANSACTION_EXPECTED_STEPS:
            self.assertIn(token, content)

    def test_active_context_script_exists(self):
        self.assertTrue(ACTIVE_CONTEXT_SCRIPT_PATH.exists(), "Missing active-context builder script")

    def test_post_write_lint_script_exists(self):
        self.assertTrue(POST_WRITE_LINT_SCRIPT_PATH.exists(), "Missing post-write lint script")

    def test_guardrail_contract_tokens_exist(self):
        for relative_path, expected_tokens in GUARDRAIL_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_reference_learning_contract_tokens_exist(self):
        for relative_path, expected_tokens in REFERENCE_LEARN_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_import_existing_script_exists(self):
        self.assertTrue(IMPORT_EXISTING_SCRIPT_PATH.exists(), "Missing import existing chapters script")

    def test_import_bridge_contract_tokens_exist(self):
        for relative_path, expected_tokens in IMPORT_BRIDGE_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_volume_summaries_script_exists(self):
        self.assertTrue(VOLUME_SUMMARIES_SCRIPT_PATH.exists(), "Missing volume summaries script")

    def test_volume_summary_contract_tokens_exist(self):
        for relative_path, expected_tokens in VOLUME_SUMMARY_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_skills_reference_transaction_contract(self):
        for relative_path, expected_tokens in SKILL_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_entry_docs_expose_transaction_as_default_unit(self):
        for relative_path, token in ENTRY_DOC_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn(token, content, f"{relative_path} missing token: {token}")


class InkosGrowthScriptOutputTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        scaffold_project(root)
        return root

    def test_project_maintenance_reports_transaction_phase(self):
        root = self.make_project_root()
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "project-maintenance.py"), str(root)],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["transaction_phase"], "snapshot")
        self.assertIsNone(payload["next_transaction_step"])
        self.assertIsNone(payload["workflow_current_step"])
        self.assertEqual(payload["last_successful_checkpoint"], "snapshot")
        self.assertEqual(payload["workflow_status"], "completed")
        self.assertTrue((root / ".mighty" / "active-context.json").exists())
        self.assertTrue((root / ".mighty" / "memory-context.json").exists())
        self.assertTrue((root / ".mighty" / "logs" / "trace.jsonl").exists())
        workflow_state = json.loads((root / ".mighty" / "workflow_state.json").read_text(encoding="utf-8"))
        self.assertIsNone(workflow_state["current_task"]["current_step"])
        self.assertEqual(workflow_state["current_task"]["last_successful_checkpoint"], "snapshot")
        self.assertEqual(workflow_state["current_task"]["status"], "completed")
        self.assertIn("maintenance", workflow_state["current_task"]["completed_steps"])
        self.assertIn("snapshot", workflow_state["current_task"]["completed_steps"])
        self.assertFalse(workflow_state["current_task"]["pending_steps"])
        snapshots = json.loads((root / ".mighty" / "state.json").read_text(encoding="utf-8"))["chapter_snapshots"]
        self.assertIn("001", snapshots)

    def test_post_task_maintenance_reports_transaction_tail(self):
        root = self.make_project_root()
        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "post-task-maintenance.py"),
                str(root),
                "--trigger",
                "write",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["transaction_phase"], "snapshot")
        self.assertIsNone(payload["next_transaction_step"])

    def test_project_maintenance_updates_existing_workflow_state(self):
        root = self.make_project_root()
        write_json(
            root / ".mighty" / "workflow_state.json",
            {
                "version": "2.0",
                "transaction_contract": "chapter-transaction-v1",
                "current_task": {
                    "command": "novel-write",
                    "args": {"chapter": 2},
                    "status": "running",
                    "current_step": "maintenance",
                    "completed_steps": ["gate-check", "draft", "close"],
                    "failed_steps": [],
                    "pending_steps": ["maintenance", "snapshot"],
                    "last_successful_checkpoint": "close",
                    "started_at": "2026-03-25T00:00:00Z",
                    "last_heartbeat": "2026-03-25T00:00:00Z",
                    "error_message": None,
                },
                "history": [],
            },
        )
        subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "project-maintenance.py"), str(root)],
            capture_output=True,
            text=True,
            check=True,
        )
        workflow_state = json.loads((root / ".mighty" / "workflow_state.json").read_text(encoding="utf-8"))
        current_task = workflow_state["current_task"]
        self.assertEqual(current_task["command"], "novel-write")
        self.assertIsNone(current_task["current_step"])
        self.assertEqual(current_task["last_successful_checkpoint"], "snapshot")
        self.assertEqual(current_task["args"]["trigger"], "maintenance")
        self.assertIn("maintenance", current_task["completed_steps"])
        self.assertIn("snapshot", current_task["completed_steps"])
        self.assertFalse(current_task["pending_steps"])


if __name__ == "__main__":
    unittest.main()
