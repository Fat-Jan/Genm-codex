import importlib.util
import json
import subprocess
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


def scaffold_project(
    root: Path,
    *,
    current_step: str = "maintenance",
    completed_steps: list[str] | None = None,
    checkpoint: str | None = "close",
) -> None:
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
            "knowledge_base": {
                "reader_knows": [],
                "protagonist_knows": [],
                "protagonist_doesnt_know": [],
            },
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
                "current_step": current_step,
                "completed_steps": (
                    completed_steps
                    if completed_steps is not None
                    else ["gate-check", "draft", "close"]
                ),
                "failed_steps": [],
                "pending_steps": (
                    ["maintenance", "snapshot"]
                    if current_step == "maintenance"
                    else [
                        "gate-check",
                        "draft",
                        "close",
                        "maintenance",
                        "snapshot",
                    ]
                ),
                "last_successful_checkpoint": checkpoint,
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

            executed_scripts: list[str] = []

            def fake_run(cmd):
                script_name = Path(cmd[1]).name
                executed_scripts.append(script_name)
                if script_name == "generate_snapshot.py":
                    snapshot_path = (
                        root / ".mighty" / "snapshots" / "chapter-001" / "snapshot.json"
                    )
                    write_json(snapshot_path, {"ok": True})
                    return {
                        "cmd": cmd,
                        "stdout": json.dumps(
                            {
                                "filesystem_snapshot_file": str(snapshot_path),
                            },
                            ensure_ascii=False,
                        ),
                    }
                if script_name == "build_content_positioning.py":
                    raise RuntimeError("simulated content-positioning failure")
                if script_name == "build_project_knowledge_projection.py":
                    write_json(
                        root / ".mighty" / "knowledge-projection.json",
                        {
                            "workflow_truth": {
                                "status": "pass",
                                "missing_artifacts": [],
                            }
                        },
                    )
                    payload = json.loads(
                        (root / ".mighty" / "knowledge-projection.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    self.assertEqual(payload["workflow_truth"]["status"], "pass")
                    self.assertFalse(payload["workflow_truth"]["missing_artifacts"])
                    return {
                        "cmd": cmd,
                        "stdout": json.dumps({"ok": True}, ensure_ascii=False),
                    }
                if script_name == "build_workflow_health_bundle.py":
                    report = json.loads(
                        (root / ".mighty" / "maintenance-report.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    failed_steps = [
                        Path(step["cmd"][1]).name
                        for step in report.get("steps", [])
                        if step.get("status") == "failed"
                    ]
                    write_json(
                        root / ".mighty" / "workflow-health.json",
                        {
                            "maintenance_result": report.get("result"),
                            "failed_maintenance_steps": failed_steps,
                            "recommended_next_action": "repair-maintenance-tail",
                        },
                    )
                return {
                    "cmd": cmd,
                    "stdout": json.dumps({"ok": True}, ensure_ascii=False),
                }

            with (
                mock.patch.object(module, "run", side_effect=fake_run),
                mock.patch.object(
                    module,
                    "append_trace",
                    return_value=root / ".mighty" / "logs" / "trace.jsonl",
                ),
                mock.patch.object(
                    sys, "argv", ["project-maintenance.py", str(root)]
                ),
                mock.patch("builtins.print") as mocked_print,
            ):
                module.main()

            workflow_state = json.loads(
                (root / ".mighty" / "workflow_state.json").read_text(
                    encoding="utf-8"
                )
            )
            current_task = workflow_state["current_task"]
            self.assertEqual(current_task["status"], "completed")
            self.assertEqual(current_task["last_successful_checkpoint"], "snapshot")
            self.assertEqual(
                current_task["args"]["maintenance_report_file"],
                ".mighty/maintenance-report.json",
            )
            self.assertEqual(
                current_task["args"]["snapshot_file"],
                ".mighty/snapshots/chapter-001/snapshot.json",
            )
            self.assertFalse(
                Path(current_task["args"]["maintenance_report_file"]).is_absolute()
            )
            self.assertFalse(Path(current_task["args"]["snapshot_file"]).is_absolute())

            report = json.loads(
                (root / ".mighty" / "maintenance-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["result"], "partial")
            self.assertTrue(
                any(step.get("status") == "failed" for step in report["steps"])
            )

            workflow_health = json.loads(
                (root / ".mighty" / "workflow-health.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(workflow_health["maintenance_result"], "partial")
            self.assertEqual(
                workflow_health["failed_maintenance_steps"],
                ["build_content_positioning.py"],
            )
            self.assertEqual(
                workflow_health["recommended_next_action"],
                "repair-maintenance-tail",
            )

            self.assertIn("build_workflow_health_bundle.py", executed_scripts)

            printed = json.loads(mocked_print.call_args[0][0])
            self.assertEqual(printed["workflow_status"], "completed")
            self.assertEqual(printed["result"], "partial")

    def test_maintenance_rejects_tasks_before_repo_owned_tail(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(
                root,
                current_step="gate-check",
                completed_steps=[],
                checkpoint=None,
            )

            with (
                mock.patch.object(
                    module,
                    "run",
                    side_effect=RuntimeError("should not run steps"),
                ),
                mock.patch.object(
                    module,
                    "append_trace",
                    return_value=root / ".mighty" / "logs" / "trace.jsonl",
                ),
                mock.patch.object(
                    sys, "argv", ["project-maintenance.py", str(root)]
                ),
            ):
                with self.assertRaisesRegex(
                    ValueError, "has not reached repo-owned tail"
                ):
                    module.main()

            workflow_state = json.loads(
                (root / ".mighty" / "workflow_state.json").read_text(
                    encoding="utf-8"
                )
            )
            current_task = workflow_state["current_task"]
            self.assertEqual(current_task["current_step"], "gate-check")
            self.assertEqual(current_task["completed_steps"], [])
            self.assertIsNone(current_task["last_successful_checkpoint"])
            self.assertFalse((root / ".mighty" / "maintenance-report.json").exists())

    def test_maintenance_rejects_snapshot_path_outside_repo_owned_sidecar(self) -> None:
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
                                "filesystem_snapshot_file": (
                                    "/tmp/external-snapshot.json"
                                ),
                            },
                            ensure_ascii=False,
                        ),
                    }
                return {
                    "cmd": cmd,
                    "stdout": json.dumps({"ok": True}, ensure_ascii=False),
                }

            with (
                mock.patch.object(module, "run", side_effect=fake_run),
                mock.patch.object(
                    module,
                    "append_trace",
                    return_value=root / ".mighty" / "logs" / "trace.jsonl",
                ),
                mock.patch.object(
                    sys, "argv", ["project-maintenance.py", str(root)]
                ),
            ):
                with self.assertRaisesRegex(
                    ValueError, "project root|repo-owned sidecar"
                ):
                    module.main()

    def test_maintenance_rejects_missing_snapshot_file_in_repo_owned_sidecar(
        self,
    ) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)
            legacy_snapshot_path = (
                f"/tmp/old-checkout/projects/{root.name}/.mighty/snapshots/"
                "chapter-001/snapshot.json"
            )

            def fake_run(cmd):
                script_name = Path(cmd[1]).name
                if script_name == "generate_snapshot.py":
                    return {
                        "cmd": cmd,
                        "stdout": json.dumps(
                            {
                                "filesystem_snapshot_file": legacy_snapshot_path,
                            },
                            ensure_ascii=False,
                        ),
                    }
                return {
                    "cmd": cmd,
                    "stdout": json.dumps({"ok": True}, ensure_ascii=False),
                }

            with (
                mock.patch.object(module, "run", side_effect=fake_run),
                mock.patch.object(
                    module,
                    "append_trace",
                    return_value=root / ".mighty" / "logs" / "trace.jsonl",
                ),
                mock.patch.object(
                    sys, "argv", ["project-maintenance.py", str(root)]
                ),
            ):
                with self.assertRaisesRegex(
                    ValueError, "snapshot artifact does not exist"
                ):
                    module.main()

            workflow_state = json.loads(
                (root / ".mighty" / "workflow_state.json").read_text(
                    encoding="utf-8"
                )
            )
            current_task = workflow_state["current_task"]
            self.assertEqual(current_task["status"], "running")
            self.assertEqual(current_task["current_step"], "maintenance")
            self.assertEqual(
                current_task["completed_steps"],
                ["gate-check", "draft", "close"],
            )
            self.assertEqual(current_task["last_successful_checkpoint"], "close")
            self.assertNotIn("snapshot_file", current_task["args"])

            report = json.loads(
                (root / ".mighty" / "maintenance-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["result"], "failed")
            self.assertEqual(report["transaction_phase"], "snapshot")
            self.assertIn("snapshot artifact does not exist", report["error"])

    def test_maintenance_runs_memory_summary_step(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)
            called_scripts: list[str] = []

            def fake_run(cmd):
                script_name = Path(cmd[1]).name
                called_scripts.append(script_name)
                if script_name == "generate_snapshot.py":
                    snapshot_path = (
                        root / ".mighty" / "snapshots" / "chapter-001" / "snapshot.json"
                    )
                    write_json(snapshot_path, {"ok": True})
                    return {
                        "cmd": cmd,
                        "stdout": json.dumps(
                            {
                                "filesystem_snapshot_file": str(snapshot_path),
                            },
                            ensure_ascii=False,
                        ),
                    }
                return {
                    "cmd": cmd,
                    "stdout": json.dumps({"ok": True}, ensure_ascii=False),
                }

            with (
                mock.patch.object(module, "run", side_effect=fake_run),
                mock.patch.object(
                    module,
                    "append_trace",
                    return_value=root / ".mighty" / "logs" / "trace.jsonl",
                ),
                mock.patch.object(
                    sys, "argv", ["project-maintenance.py", str(root)]
                ),
                mock.patch("builtins.print") as mocked_print,
            ):
                module.main()

            self.assertIn("render_memory_context_summary.py", called_scripts)
            printed = json.loads(mocked_print.call_args[0][0])
            self.assertIn("render_memory_context_summary.py", printed["steps"])

    def test_maintenance_writes_final_report_before_projection_and_health(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)
            observed_report_results: dict[str, str | None] = {
                "knowledge_projection": None,
                "workflow_health": None,
            }

            def fake_run(cmd):
                script_name = Path(cmd[1]).name
                if script_name == "generate_snapshot.py":
                    snapshot_path = (
                        root / ".mighty" / "snapshots" / "chapter-001" / "snapshot.json"
                    )
                    write_json(snapshot_path, {"ok": True})
                    return {
                        "cmd": cmd,
                        "stdout": json.dumps(
                            {
                                "filesystem_snapshot_file": str(snapshot_path),
                            },
                            ensure_ascii=False,
                        ),
                    }
                if script_name == "build_content_positioning.py":
                    raise subprocess.CalledProcessError(
                        1,
                        cmd,
                        stderr="simulated content-positioning failure",
                    )
                if script_name == "build_project_knowledge_projection.py":
                    report_path = root / ".mighty" / "maintenance-report.json"
                    report = json.loads(report_path.read_text(encoding="utf-8"))
                    observed_report_results["knowledge_projection"] = report.get(
                        "result"
                    )
                    write_json(
                        root / ".mighty" / "knowledge-projection.json",
                        {
                            "workflow_truth": {
                                "status": "pass",
                                "missing_artifacts": [],
                            }
                        },
                    )
                if script_name == "build_workflow_health_bundle.py":
                    report_path = root / ".mighty" / "maintenance-report.json"
                    report = json.loads(report_path.read_text(encoding="utf-8"))
                    observed_report_results["workflow_health"] = report.get(
                        "result"
                    )
                    failed_steps = [
                        Path(step["cmd"][1]).name
                        for step in report.get("steps", [])
                        if step.get("status") == "failed"
                    ]
                    write_json(
                        root / ".mighty" / "workflow-health.json",
                        {
                            "maintenance_result": report.get("result"),
                            "failed_maintenance_steps": failed_steps,
                            "recommended_next_action": "repair-maintenance-tail",
                        },
                    )
                return {
                    "cmd": cmd,
                    "stdout": json.dumps({"ok": True}, ensure_ascii=False),
                }

            with (
                mock.patch.object(module, "run", side_effect=fake_run),
                mock.patch.object(
                    module,
                    "append_trace",
                    return_value=root / ".mighty" / "logs" / "trace.jsonl",
                ),
                mock.patch.object(
                    sys, "argv", ["project-maintenance.py", str(root)]
                ),
            ):
                module.main()

            self.assertEqual(observed_report_results["knowledge_projection"], "partial")
            self.assertEqual(observed_report_results["workflow_health"], "partial")

            report = json.loads(
                (root / ".mighty" / "maintenance-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["result"], "partial")

            workflow_health = json.loads(
                (root / ".mighty" / "workflow-health.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(workflow_health["maintenance_result"], "partial")
            self.assertEqual(
                workflow_health["failed_maintenance_steps"],
                ["build_content_positioning.py"],
            )

    def test_maintenance_rewrites_report_after_projection_failure(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)
            observed_workflow_health_result: str | None = None

            def fake_run(cmd):
                nonlocal observed_workflow_health_result
                script_name = Path(cmd[1]).name
                if script_name == "generate_snapshot.py":
                    snapshot_path = (
                        root / ".mighty" / "snapshots" / "chapter-001" / "snapshot.json"
                    )
                    write_json(snapshot_path, {"ok": True})
                    return {
                        "cmd": cmd,
                        "stdout": json.dumps(
                            {
                                "filesystem_snapshot_file": str(snapshot_path),
                            },
                            ensure_ascii=False,
                        ),
                    }
                if script_name == "build_project_knowledge_projection.py":
                    raise subprocess.CalledProcessError(
                        1,
                        cmd,
                        stderr="simulated knowledge-projection failure",
                    )
                if script_name == "build_workflow_health_bundle.py":
                    report = json.loads(
                        (root / ".mighty" / "maintenance-report.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    observed_workflow_health_result = report.get("result")
                    failed_steps = [
                        Path(step["cmd"][1]).name
                        for step in report.get("steps", [])
                        if step.get("status") == "failed"
                    ]
                    write_json(
                        root / ".mighty" / "workflow-health.json",
                        {
                            "maintenance_result": report.get("result"),
                            "failed_maintenance_steps": failed_steps,
                            "recommended_next_action": "repair-maintenance-tail",
                        },
                    )
                return {
                    "cmd": cmd,
                    "stdout": json.dumps({"ok": True}, ensure_ascii=False),
                }

            with (
                mock.patch.object(module, "run", side_effect=fake_run),
                mock.patch.object(
                    module,
                    "append_trace",
                    return_value=root / ".mighty" / "logs" / "trace.jsonl",
                ),
                mock.patch.object(
                    sys, "argv", ["project-maintenance.py", str(root)]
                ),
            ):
                module.main()

            self.assertEqual(observed_workflow_health_result, "partial")

            report = json.loads(
                (root / ".mighty" / "maintenance-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["result"], "partial")
            self.assertEqual(
                [
                    Path(step["cmd"][1]).name
                    for step in report["steps"]
                    if step.get("status") == "failed"
                ],
                ["build_project_knowledge_projection.py"],
            )

            workflow_health = json.loads(
                (root / ".mighty" / "workflow-health.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(workflow_health["maintenance_result"], "partial")
            self.assertEqual(
                workflow_health["failed_maintenance_steps"],
                ["build_project_knowledge_projection.py"],
            )

    def test_maintenance_rewrites_final_report_after_workflow_health_failure(
        self,
    ) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)

            def fake_run(cmd):
                script_name = Path(cmd[1]).name
                if script_name == "generate_snapshot.py":
                    snapshot_path = (
                        root / ".mighty" / "snapshots" / "chapter-001" / "snapshot.json"
                    )
                    write_json(snapshot_path, {"ok": True})
                    return {
                        "cmd": cmd,
                        "stdout": json.dumps(
                            {
                                "filesystem_snapshot_file": str(snapshot_path),
                            },
                            ensure_ascii=False,
                        ),
                    }
                if script_name == "build_workflow_health_bundle.py":
                    raise subprocess.CalledProcessError(
                        1,
                        cmd,
                        stderr="simulated workflow-health failure",
                    )
                return {
                    "cmd": cmd,
                    "stdout": json.dumps({"ok": True}, ensure_ascii=False),
                }

            with (
                mock.patch.object(module, "run", side_effect=fake_run),
                mock.patch.object(
                    module,
                    "append_trace",
                    return_value=root / ".mighty" / "logs" / "trace.jsonl",
                ),
                mock.patch.object(
                    sys, "argv", ["project-maintenance.py", str(root)]
                ),
            ):
                module.main()

            report = json.loads(
                (root / ".mighty" / "maintenance-report.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(report["result"], "partial")
            self.assertEqual(
                [
                    Path(step["cmd"][1]).name
                    for step in report["steps"]
                    if step.get("status") == "failed"
                ],
                ["build_workflow_health_bundle.py"],
            )


if __name__ == "__main__":
    unittest.main()
