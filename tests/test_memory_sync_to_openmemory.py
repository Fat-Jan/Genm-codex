import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "sync_memory_context_to_openmemory.py"


def load_module():
    spec = importlib.util.spec_from_file_location("sync_memory_context_to_openmemory", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def openmemory_root() -> str:
    resolved = shutil.which("opm")
    if not resolved:
        raise RuntimeError("opm is required for this test")
    opm = Path(resolved).resolve()
    return str(opm.parents[1])


class MemorySyncToOpenMemoryTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        write_json(
            root / ".mighty" / "memory-context.json",
            {
                "version": "1.0",
                "generated_at": "2026-03-31T00:00:00Z",
                "safe_for_mcp_memory": True,
                "title": "同步测试项目",
                "current_chapter": 7,
                "total_words": 18200,
                "workflow": {
                    "status": "completed",
                    "current_step": None,
                    "last_successful_checkpoint": "snapshot",
                },
                "gate": {
                    "status": "passed",
                    "blocking_gap_keys": [],
                    "minimal_next_action": "novel-write",
                    "minimal_next_reason": "继续下一章",
                },
                "launch_stack": {
                    "phase": "locked",
                    "drift_signal": "none",
                },
                "active_context_summary": {
                    "hook_count": 2,
                    "guardrail_count": 1,
                    "latest_summary_chapter": "007",
                },
                "memory_contract": {
                    "truth_source": "local_files",
                    "allowed_sync": ["workflow_summary"],
                    "forbidden_sync": ["full_state_json", "chapter_prose"],
                },
                "freshness": {
                    "artifact_key": "memory-context",
                    "contract": "sidecar-freshness-v1",
                },
            },
        )
        return root

    def test_build_sync_payload_keeps_safe_summary_only(self) -> None:
        module = load_module()
        root = self.make_project_root()

        payload = module.build_sync_payload(
            json.loads((root / ".mighty" / "memory-context.json").read_text(encoding="utf-8")),
            root,
            user_id="genm-codex",
        )

        self.assertEqual(payload["metadata"]["artifact_key"], "memory-context")
        self.assertEqual(payload["metadata"]["memory_contract"]["truth_source"], "local_files")
        self.assertIn("chapter_prose", payload["metadata"]["memory_contract"]["forbidden_sync"])
        self.assertNotIn("chapter_text", payload["metadata"])
        self.assertIn("workflow=completed/snapshot", payload["content"])

    def test_sync_skips_when_content_hash_is_unchanged(self) -> None:
        module = load_module()
        root = self.make_project_root()
        payload = module.build_sync_payload(
            json.loads((root / ".mighty" / "memory-context.json").read_text(encoding="utf-8")),
            root,
            user_id="genm-codex",
        )
        write_json(
            root / ".mighty" / "memory-sync-report.json",
            {
                "content_hash": payload["content_hash"],
                "memory_id": "mem-existing",
            },
        )

        with mock.patch.object(module, "run_store_call") as mocked_store:
            result = module.sync_memory_context(
                root,
                timestamp="2026-03-31T00:00:00Z",
                mode="on",
                user_id="genm-codex",
                config_path=root / "missing.toml",
            )

        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["reason"], "content-unchanged")
        self.assertEqual(result["memory_id"], "mem-existing")
        mocked_store.assert_not_called()

    def test_sync_stores_memory_when_project_opt_in_and_client_is_configured(self) -> None:
        module = load_module()
        root = self.make_project_root()
        write_json(
            root / ".mighty" / "config.json",
            {
                "memory_sync": {
                    "openmemory": {
                        "enabled": True,
                        "user_id": "project-memory-user",
                    }
                }
            },
        )
        config_path = root / "codex-config.toml"
        config_path.write_text(
            "\n".join(
                [
                    "[mcp_servers.openmemory]",
                    'command = "opm"',
                    'args = ["mcp"]',
                    "[mcp_servers.openmemory.env]",
                    'OM_TIER = "hybrid"',
                ]
            ),
            encoding="utf-8",
        )

        with mock.patch.object(
            module,
            "run_store_call",
            return_value={
                "transport": "local-node",
                "result": {
                    "id": "mem-123",
                    "primary_sector": "semantic",
                    "sectors": ["semantic"],
                },
            },
        ) as mocked_store:
            result = module.sync_memory_context(
                root,
                timestamp="2026-03-31T00:00:00Z",
                mode="auto",
                user_id="project-memory-user",
                config_path=config_path,
            )

        self.assertEqual(result["status"], "stored")
        self.assertEqual(result["memory_id"], "mem-123")
        self.assertEqual(result["command"], ["node", str(module.LOCAL_BRIDGE_PATH)])
        self.assertEqual(result["store_transport"], "local-node")
        mocked_args = mocked_store.call_args[0][1]
        self.assertEqual(mocked_args["user_id"], "project-memory-user")
        self.assertEqual(mocked_args["type"], "contextual")
        self.assertEqual(mocked_args["metadata"]["artifact_key"], "memory-context")

    def test_local_bridge_flattens_metadata_and_replaces_same_project_key(self) -> None:
        root = self.make_project_root()
        bridge = REPO_ROOT / "scripts" / "openmemory_store_bridge.js"
        db_path = root / "openmemory.sqlite"
        env = os.environ.copy()
        env.update(
            {
                "OPENMEMORY_JS_ROOT": openmemory_root(),
                "OM_DB_PATH": str(db_path),
                "OM_EMBEDDINGS": "synthetic",
                "OM_TIER": "hybrid",
            }
        )

        payload_v1 = {
            "content": "project state v1",
            "user_id": "bridge-test-user",
            "tags": ["genm-codex", "memory-context", "project-key:test123"],
            "metadata": {
                "project_key": "test123",
                "content_hash": "hash-v1",
                "title": "Bridge Test",
            },
        }
        payload_v2 = {
            "content": "project state v2",
            "user_id": "bridge-test-user",
            "tags": ["genm-codex", "memory-context", "project-key:test123"],
            "metadata": {
                "project_key": "test123",
                "content_hash": "hash-v2",
                "title": "Bridge Test",
            },
        }

        first = subprocess.run(
            ["node", str(bridge)],
            input=json.dumps(payload_v1, ensure_ascii=False),
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        first_id = json.loads(first.stdout)["id"]

        second = subprocess.run(
            ["node", str(bridge)],
            input=json.dumps(payload_v2, ensure_ascii=False),
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        second_id = json.loads(second.stdout)["id"]
        self.assertEqual(first_id, second_id)

        inspect = subprocess.run(
            [
                "node",
                "-e",
                (
                    "const root=process.env.OPENMEMORY_JS_ROOT;"
                    "const { q } = require(`${root}/dist/core/db.js`);"
                    "(async()=>{"
                    "const rows = await q.all_mem_by_user.all('bridge-test-user', 100, 0);"
                    "console.log(JSON.stringify(rows.map(r=>({id:r.id,tags:JSON.parse(r.tags||'[]'),meta:JSON.parse(r.meta||'{}')}))));"
                    "process.exit(0);"
                    "})().catch(err=>{console.error(err);process.exit(1);});"
                ),
            ],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        rows = json.loads(inspect.stdout)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], first_id)
        self.assertEqual(rows[0]["meta"]["project_key"], "test123")
        self.assertEqual(rows[0]["meta"]["content_hash"], "hash-v2")
        self.assertNotIn("metadata", rows[0]["meta"])


if __name__ == "__main__":
    unittest.main()
