import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "project_knowledge_mcp_server.py"


def load_module():
    spec = importlib.util.spec_from_file_location("project_knowledge_mcp_server", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ProjectKnowledgeMcpServerTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        mighty = root / ".mighty"
        mighty.mkdir(parents=True)
        write_json(
            mighty / "state.json",
            {
                "meta": {"title": "MCP 测试书"},
                "progress": {"current_chapter": 3},
                "plot_threads": {"foreshadowing": {"active": [{"id": "f1", "name": "旧账"}]}},
                "active_context": {
                    "last_built": "2026-03-28T00:00:00Z",
                    "hook_count": 1,
                    "guardrail_count": 0,
                },
                "chapter_meta": {"1": {"review_score": 87}},
            },
        )
        write_json(mighty / "state-archive.json", {"chapter_meta": {"0": {"review_score": 80}}})
        write_json(mighty / "workflow_state.json", {"transaction_contract": "chapter-transaction-v1", "current_task": {"status": "completed"}})
        write_json(mighty / "setting-gate.json", {"status": "passed"})
        write_json(mighty / "content-positioning.json", {"version": "1.0"})
        write_json(mighty / "learned-patterns.json", {"data": {}})
        return root

    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/project_knowledge_mcp_server.py is missing")

    def test_tools_list_exposes_projection_and_quality_audit(self) -> None:
        module = load_module()
        response = module.handle_request(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
            }
        )
        tool_names = [item["name"] for item in response["result"]["tools"]]
        self.assertIn("get_project_knowledge_projection", tool_names)
        self.assertIn("get_project_quality_audit", tool_names)
        self.assertIn("get_project_workflow_bundle", tool_names)
        self.assertIn("get_project_workflow_health_summary", tool_names)
        self.assertIn("get_project_status_dashboard", tool_names)

    def test_tools_call_returns_projection_payload(self) -> None:
        module = load_module()
        root = self.make_project_root()
        response = module.handle_request(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_project_knowledge_projection",
                    "arguments": {"project_root": str(root)},
                },
            }
        )
        self.assertFalse(response["result"]["isError"])
        content = json.loads(response["result"]["content"][0]["text"])
        self.assertEqual(content["project_title"], "MCP 测试书")
        self.assertEqual(content["workflow_contract"]["repo_owned_tail_steps"], ["maintenance", "snapshot"])

    def test_tools_call_returns_workflow_bundle_payload(self) -> None:
        module = load_module()
        root = self.make_project_root()
        response = module.handle_request(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "get_project_workflow_bundle",
                    "arguments": {"project_root": str(root)},
                },
            }
        )
        self.assertFalse(response["result"]["isError"])
        content = json.loads(response["result"]["content"][0]["text"])
        self.assertIn("knowledge_projection", content)
        self.assertIn("quality_audit", content)
        self.assertIn("workflow_health", content)
        self.assertEqual(content["knowledge_projection"]["project_title"], "MCP 测试书")

    def test_tools_call_returns_workflow_health_summary_text(self) -> None:
        module = load_module()
        root = self.make_project_root()
        write_json(
            root / ".mighty" / "workflow-health.json",
            {
                "project_title": "MCP 测试书",
                "quality_audit_status": "warn",
                "top_finding_codes": ["empty-issue-clusters-with-score"],
                "workflow_truth_status": "pass",
                "workflow_truth_missing_artifacts": [],
                "repo_owned_tail_steps": ["maintenance", "snapshot"],
                "setting_gate_status": "passed",
                "has_recent_guardrails": False,
            },
        )
        response = module.handle_request(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "get_project_workflow_health_summary",
                    "arguments": {"project_root": str(root)},
                },
            }
        )
        self.assertFalse(response["result"]["isError"])
        text = response["result"]["content"][0]["text"]
        self.assertIn("## Workflow Health", text)
        self.assertIn("quality-audit: `warn`", text)

    def test_tools_call_returns_project_status_dashboard(self) -> None:
        module = load_module()
        root = self.make_project_root()
        write_json(
            root / ".mighty" / "workflow-health.json",
            {
                "project_title": "MCP 测试书",
                "quality_audit_status": "warn",
                "top_finding_codes": ["empty-issue-clusters-with-score"],
                "workflow_truth_status": "pass",
                "workflow_truth_missing_artifacts": [],
                "repo_owned_tail_steps": ["maintenance", "snapshot"],
                "setting_gate_status": "passed",
                "has_recent_guardrails": False,
                "recommended_next_action": "repair-review-artifacts",
                "recommended_reason": "先修 review artifact。",
            },
        )
        write_json(
            root / ".mighty" / "setting-gate.json",
            {
                "status": "passed",
                "blocking_gaps": [],
                "review_items": [],
                "minimal_next_action": {"summary": "继续写下一章", "suggested_commands": []},
            },
        )
        response = module.handle_request(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "get_project_status_dashboard",
                    "arguments": {"project_root": str(root)},
                },
            }
        )
        self.assertFalse(response["result"]["isError"])
        text = response["result"]["content"][0]["text"]
        self.assertIn("## Project Status Dashboard", text)
        self.assertIn("MCP 测试书", text)


if __name__ == "__main__":
    unittest.main()
