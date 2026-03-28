import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from unittest import mock
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "project-maintenance.py"


def load_module():
    spec = importlib.util.spec_from_file_location("project_maintenance", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
                "title": "maintenance-tolerance-test",
                "genre": "都市脑洞",
                "platform": "番茄",
                "target_chapters": 5,
                "updated_at": "2026-03-28T00:00:00Z",
            },
            "progress": {
                "current_chapter": 1,
                "total_words": 3200,
                "last_write_chapter": 1,
            },
            "genre_profile": {"bucket": "都市脑洞"},
            "entities": {
                "characters": {"protagonist": {"name": "周既明"}},
                "items": {"tracked": []},
                "locations": {"current": "曜石互联大厦"},
            },
            "plot_threads": {"foreshadowing": {"active": []}},
            "knowledge_base": {"reader_knows": [], "protagonist_knows": [], "protagonist_doesnt_know": []},
            "chapter_meta": {"1": {"summary": "第一章摘要"}},
        },
    )
    write_json(
        root / ".mighty" / "workflow_state.json",
        {
            "version": "2.0",
            "transaction_contract": "chapter-transaction-v1",
            "current_task": {
                "command": "novel-write",
                "args": {"chapter": 1},
                "status": "running",
                "current_step": "maintenance",
                "completed_steps": ["gate-check", "draft", "close"],
                "failed_steps": [],
                "pending_steps": ["maintenance", "snapshot"],
                "last_successful_checkpoint": "close",
                "started_at": "2026-03-28T00:00:00Z",
                "last_heartbeat": "2026-03-28T00:00:00Z",
                "error_message": None,
            },
            "history": [],
        },
    )
    write_json(root / ".mighty" / "setting-gate.json", {"status": "passed"})
    write_text(root / "chapters" / "第001章.md", "主角反击。" * 200)


class ProjectMaintenanceToleranceTests(unittest.TestCase):
    def test_post_snapshot_failure_does_not_rollback_snapshot_completion(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)

            def fake_run(cmd):
                script_name = Path(cmd[1]).name
                if script_name == "generate_snapshot.py":
                    return {
                        "cmd": cmd,
                        "stdout": json.dumps(
                            {
                                "filesystem_snapshot_file": str(root / ".mighty" / "snapshots" / "chapter-001" / "snapshot.json"),
                            },
                            ensure_ascii=False,
                        ),
                    }
                if script_name == "build_content_positioning.py":
                    raise RuntimeError("simulated content-positioning failure")
                return {"cmd": cmd, "stdout": json.dumps({"ok": True}, ensure_ascii=False)}

            with mock.patch.object(module, "run", side_effect=fake_run), \
                 mock.patch.object(module, "append_trace", return_value=root / ".mighty" / "logs" / "trace.jsonl"), \
                 mock.patch.object(sys, "argv", ["project-maintenance.py", str(root)]), \
                 mock.patch("builtins.print") as mocked_print:
                module.main()

            workflow_state = json.loads((root / ".mighty" / "workflow_state.json").read_text(encoding="utf-8"))
            current_task = workflow_state["current_task"]
            self.assertEqual(current_task["status"], "completed")
            self.assertEqual(current_task["last_successful_checkpoint"], "snapshot")

            report = json.loads((root / ".mighty" / "maintenance-report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["result"], "partial")
            self.assertTrue(any(step.get("status") == "failed" for step in report["steps"]))

            printed = json.loads(mocked_print.call_args[0][0])
            self.assertEqual(printed["workflow_status"], "completed")
            self.assertEqual(printed["result"], "partial")


if __name__ == "__main__":
    unittest.main()
