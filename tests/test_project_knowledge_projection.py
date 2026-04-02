import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "build_project_knowledge_projection.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_project_knowledge_projection", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ProjectKnowledgeProjectionTests(unittest.TestCase):
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
                    "title": "知识投影测试书",
                },
                "progress": {
                    "current_chapter": 18,
                },
                "plot_threads": {
                    "foreshadowing": {
                        "active": [
                            {"id": "f1", "name": "旧井案"},
                            {"id": "f2", "name": "外室子线"},
                        ]
                    }
                },
                "active_context": {
                    "sidecar_file": ".mighty/active-context.json",
                    "last_built": "2026-03-28T00:00:00Z",
                    "hook_count": 2,
                    "guardrail_count": 0,
                },
                "learned_patterns": {
                    "externalized": True,
                    "sidecar_file": ".mighty/learned-patterns.json",
                    "has_recent_guardrails": True,
                    "recent_guardrails_expires_after_chapter": 19,
                },
                "chapter_meta": {
                    "11": {"review_score": 87},
                    "12": {"review_score": 86},
                },
            },
        )
        write_json(
            mighty / "state-archive.json",
            {
                "chapter_meta": {
                    "1": {"review_score": 87},
                    "2": {"review_score": 88},
                }
            },
        )
        write_json(
            mighty / "workflow_state.json",
            {
                "transaction_contract": "chapter-transaction-v1",
                "current_task": {
                    "command": "novel-batch",
                    "status": "completed",
                    "last_successful_checkpoint": "snapshot",
                    "args": {
                        "snapshot_file": ".mighty/snapshots/chapter-018/snapshot.json",
                        "maintenance_report_file": ".mighty/maintenance-report.json",
                    },
                },
            },
        )
        write_json(
            mighty / "setting-gate.json",
            {
                "status": "passed",
            },
        )
        write_json(
            mighty / "content-positioning.json",
            {
                "version": "1.0",
            },
        )
        write_json(mighty / "active-context.json", {"version": "1.0"})
        write_json(mighty / "memory-context.json", {"version": "1.0"})
        write_json(mighty / "quality-audit.json", {"status": "warn"})
        write_json(mighty / "maintenance-report.json", {"run_at": "2026-03-28T00:00:00Z"})
        write_json(mighty / "snapshots" / "chapter-018" / "snapshot.json", {"ok": True})
        write_json(
            mighty / "learned-patterns.json",
            {
                "version": "1.0",
                "data": {
                    "recent_guardrails": {
                        "must_avoid": ["不要总结句"],
                        "must_preserve": ["代价感"],
                        "next_chapter_watchpoints": ["保留残账"],
                        "expires_after_chapter": 19,
                    }
                },
            },
        )
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/build_project_knowledge_projection.py is missing")

    def test_build_projection_returns_compact_sections(self) -> None:
        module = load_module()
        root = self.make_project_root()

        payload = module.build_project_knowledge_projection(root, timestamp="2026-03-28T00:00:00Z")

        self.assertEqual(payload["project_title"], "知识投影测试书")
        self.assertEqual(payload["workflow_contract"]["transaction_contract"], "chapter-transaction-v1")
        self.assertEqual(payload["workflow_contract"]["repo_owned_tail_steps"], ["maintenance", "snapshot"])
        self.assertEqual(payload["sidecar_health"]["setting_gate_status"], "passed")
        self.assertTrue(payload["sidecar_health"]["has_content_positioning"])
        self.assertTrue(payload["sidecar_health"]["has_recent_guardrails"])
        self.assertEqual(payload["story_index"]["current_chapter"], 18)
        self.assertEqual(payload["story_index"]["active_hook_count"], 2)
        self.assertEqual(payload["story_index"]["live_reviewed_chapters"], 2)
        self.assertEqual(payload["story_index"]["archived_reviewed_chapters"], 2)
        self.assertEqual(payload["workflow_truth"]["status"], "pass")
        self.assertFalse(payload["workflow_truth"]["missing_artifacts"])
        self.assertTrue(payload["workflow_truth"]["checks"]["maintenance_report_exists"])
        self.assertTrue(payload["workflow_truth"]["checks"]["snapshot_file_exists"])
        self.assertEqual(payload["freshness"]["artifact_key"], "knowledge-projection")
        self.assertEqual(payload["freshness"]["contract"], "sidecar-freshness-v1")

    def test_build_projection_accepts_legacy_root_prefixed_relative_paths(self) -> None:
        module = load_module()
        root = self.make_project_root()
        mighty = root / ".mighty"
        workflow_state_path = mighty / "workflow_state.json"
        workflow_state = json.loads(workflow_state_path.read_text(encoding="utf-8"))
        workflow_state["current_task"]["args"] = {
            "maintenance_report_file": f"projects/{root.name}/.mighty/maintenance-report.json",
            "snapshot_file": f"projects/{root.name}/.mighty/snapshots/chapter-018/snapshot.json",
        }
        workflow_state_path.write_text(json.dumps(workflow_state, ensure_ascii=False, indent=2), encoding="utf-8")

        payload = module.build_project_knowledge_projection(root, timestamp="2026-03-28T00:00:00Z")

        self.assertEqual(payload["workflow_truth"]["status"], "pass")
        self.assertFalse(payload["workflow_truth"]["missing_artifacts"])


    def test_build_projection_accepts_legacy_absolute_paths_from_other_checkout(self) -> None:
        module = load_module()
        root = self.make_project_root()
        mighty = root / ".mighty"
        workflow_state_path = mighty / "workflow_state.json"
        workflow_state = json.loads(workflow_state_path.read_text(encoding="utf-8"))
        workflow_state["current_task"]["args"] = {
            "maintenance_report_file": f"/tmp/old-checkout/projects/{root.name}/.mighty/maintenance-report.json",
            "snapshot_file": f"/tmp/old-checkout/projects/{root.name}/.mighty/snapshots/chapter-018/snapshot.json",
        }
        workflow_state_path.write_text(json.dumps(workflow_state, ensure_ascii=False, indent=2), encoding="utf-8")

        payload = module.build_project_knowledge_projection(root, timestamp="2026-03-28T00:00:00Z")

        self.assertEqual(payload["workflow_truth"]["status"], "pass")
        self.assertFalse(payload["workflow_truth"]["missing_artifacts"])
    def test_build_projection_rejects_external_absolute_artifact_paths(self) -> None:
        module = load_module()
        root = self.make_project_root()
        mighty = root / ".mighty"
        external_root = Path(tempfile.mkdtemp())
        self.addCleanup(
            lambda: __import__("shutil").rmtree(external_root, ignore_errors=True)
        )
        external_report = external_root / "maintenance-report.json"
        external_snapshot = external_root / "snapshot.json"
        write_json(external_report, {"run_at": "2026-03-28T00:00:00Z"})
        write_json(external_snapshot, {"ok": True})
        workflow_state_path = mighty / "workflow_state.json"
        workflow_state = json.loads(workflow_state_path.read_text(encoding="utf-8"))
        workflow_state["current_task"]["args"] = {
            "maintenance_report_file": str(external_report),
            "snapshot_file": str(external_snapshot),
        }
        workflow_state_path.write_text(
            json.dumps(workflow_state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        payload = module.build_project_knowledge_projection(
            root,
            timestamp="2026-03-28T00:00:00Z",
        )

        self.assertEqual(payload["workflow_truth"]["status"], "fail")
        self.assertEqual(
            payload["workflow_truth"]["missing_artifacts"],
            ["maintenance_report_exists", "snapshot_file_exists"],
        )

    def test_build_projection_rejects_snapshot_path_traversal(self) -> None:
        module = load_module()
        root = self.make_project_root()
        mighty = root / ".mighty"
        workflow_state_path = mighty / "workflow_state.json"
        workflow_state = json.loads(workflow_state_path.read_text(encoding="utf-8"))
        workflow_state["current_task"]["args"] = {
            "maintenance_report_file": ".mighty/maintenance-report.json",
            "snapshot_file": ".mighty/snapshots/../../../../etc/passwd",
        }
        workflow_state_path.write_text(
            json.dumps(workflow_state, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        payload = module.build_project_knowledge_projection(
            root,
            timestamp="2026-03-28T00:00:00Z",
        )

        self.assertEqual(payload["workflow_truth"]["status"], "fail")
        self.assertEqual(
            payload["workflow_truth"]["missing_artifacts"],
            ["snapshot_file_exists"],
        )


if __name__ == "__main__":
    unittest.main()
