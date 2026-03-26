import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_MODULE_PATH = REPO_ROOT / "scripts" / "generate_snapshot.py"
MEMORY_MODULE_PATH = REPO_ROOT / "scripts" / "build_memory_context.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
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


class Phase2HelperTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        write_json(
            root / ".mighty" / "state.json",
            {
                "meta": {
                    "title": "Phase2 Helper Test",
                    "updated_at": "2026-03-26T00:00:00Z",
                },
                "progress": {
                    "current_chapter": 1,
                    "last_write_chapter": 1,
                    "total_words": 3200,
                },
                "entities": {
                    "characters": {
                        "protagonist": {"name": "周既明", "location": {"current": "曜石互联大厦"}},
                        "active": [{"name": "韩振", "role": "对手"}],
                    }
                },
                "plot_threads": {"foreshadowing": {"active": [{"id": "F1", "name": "赔付来源"}]}},
                "knowledge_base": {"reader_knows": ["系统赔付机制曝光"]},
                "chapter_meta": {"001": {"summary": "主角完成第一轮反击。", "key_events": ["签离职协议"]}},
                "active_context": {"hook_count": 1, "guardrail_count": 2},
                "launch_stack_phase": "locked",
                "launch_stack_drift_signal": "none",
            },
        )
        write_json(
            root / ".mighty" / "workflow_state.json",
            {
                "version": "2.0",
                "transaction_contract": "chapter-transaction-v1",
                "current_task": {
                    "command": "novel-write",
                    "args": {},
                    "status": "running",
                    "current_step": "snapshot",
                    "completed_steps": ["gate-check", "draft", "close", "maintenance"],
                    "failed_steps": [],
                    "pending_steps": ["snapshot"],
                    "last_successful_checkpoint": "maintenance",
                },
                "history": [],
            },
        )
        write_json(
            root / ".mighty" / "setting-gate.json",
            {
                "status": "passed",
                "blocking_gaps": [],
                "minimal_next_action": {"action": "novel-write", "reason": "gate passed"},
            },
        )
        write_json(
            root / ".mighty" / "active-context.json",
            {"summary_window": {"latest_chapter": "001"}},
        )
        write_text(root / "chapters" / "第001章.md", "主角反击。" * 200)
        return root

    def test_generate_snapshot_writes_state_and_filesystem_artifact(self) -> None:
        module = load_module(SNAPSHOT_MODULE_PATH, "generate_snapshot")
        root = self.make_project_root()

        result = module.generate_snapshot(root, chapter="001", timestamp="2026-03-26T00:00:00Z")

        self.assertTrue(result["state_snapshot_written"])
        state = json.loads((root / ".mighty" / "state.json").read_text(encoding="utf-8"))
        self.assertIn("001", state["chapter_snapshots"])
        self.assertTrue(Path(result["filesystem_snapshot_file"]).exists())
        self.assertTrue(Path(result["trace_log_file"]).exists())

    def test_build_memory_context_keeps_only_safe_summary_fields(self) -> None:
        module = load_module(MEMORY_MODULE_PATH, "build_memory_context")
        root = self.make_project_root()

        payload = module.build_memory_context(root, timestamp="2026-03-26T00:00:00Z")

        self.assertTrue(payload["safe_for_mcp_memory"])
        self.assertEqual(payload["workflow"]["current_step"], "snapshot")
        self.assertEqual(payload["gate"]["minimal_next_action"], "novel-write")
        self.assertEqual(payload["memory_contract"]["truth_source"], "local_files")
        self.assertIn("full_state_json", payload["memory_contract"]["forbidden_sync"])
        self.assertNotIn("chapter_meta", payload)
        self.assertNotIn("chapter_text", payload)


if __name__ == "__main__":
    unittest.main()
