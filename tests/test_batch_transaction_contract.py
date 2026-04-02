import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


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
                "title": "batch-transaction-test",
                "genre": "都市脑洞",
                "platform": "番茄",
                "target_chapters": 6,
                "updated_at": "2026-03-25T00:00:00Z",
            },
            "progress": {
                "current_chapter": 3,
                "total_words": 9600,
                "last_write_chapter": 3,
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
                    },
                    "active": [
                        {"name": "韩振", "role": "对手"},
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
                "1": {"summary": "第一章摘要"},
                "2": {"summary": "第二章摘要"},
                "3": {"summary": "第三章摘要"},
            },
            "summaries_index": {
                "1": {"summary": "第一章摘要"},
                "2": {"summary": "第二章摘要"},
                "3": {"summary": "第三章摘要"},
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
                "suggested_commands": [],
            },
        },
    )
    write_json(
        root / ".mighty" / "launch-stack.json",
        {
            "version": "1.0",
            "phase": "draft",
        },
    )
    write_text(root / "chapters" / "第001章.md", "主角反击。" * 400)
    write_text(root / "chapters" / "第002章.md", "主角推进。" * 400)
    write_text(root / "chapters" / "第003章.md", "主角承压。" * 400)


class BatchTransactionContractTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        scaffold_project(root)
        return root

    def test_post_task_maintenance_exposes_repo_owned_tail_for_batch(self) -> None:
        root = self.make_project_root()
        proc = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "post-task-maintenance.py"),
                str(root),
                "--trigger",
                "batch",
                "--batch-count",
                "3",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["trigger"], "batch")
        self.assertEqual(payload["repo_owned_tail_steps"], ["maintenance", "snapshot"])
        self.assertIn("quality_audit", payload)
        self.assertIn("status", payload["quality_audit"])
        self.assertIn("memory_sync", payload)
        self.assertEqual(payload["memory_sync"]["status"], "skipped")

    def test_batch_docs_define_repo_owned_tail_as_maintenance_and_snapshot(self) -> None:
        novel_batch = (REPO_ROOT / "skills" / "novel-batch" / "SKILL.md").read_text(encoding="utf-8")
        default_workflows = (REPO_ROOT / "docs" / "00-当前有效" / "default-workflows.md").read_text(encoding="utf-8")

        self.assertIn("`maintenance + snapshot`", novel_batch)
        self.assertIn("`maintenance + snapshot`", default_workflows)


if __name__ == "__main__":
    unittest.main()
