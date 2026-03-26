import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


SETTING_GATE_MODULE_PATH = REPO_ROOT / "scripts" / "setting_gate.py"
POLICY_PATH = REPO_ROOT / "docs" / "setting-gate-policy.json"


def load_setting_gate_module():
    spec = importlib.util.spec_from_file_location("setting_gate", SETTING_GATE_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {SETTING_GATE_MODULE_PATH}")
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


def scaffold_project(root: Path, *, outline_text: str) -> None:
    write_json(
        root / ".mighty" / "state.json",
        {
            "version": "5.0",
            "meta": {
                "title": "公司裁我那天，系统先赔了我一百万",
                "genre": "都市脑洞",
                "platform": "番茄",
                "target_chapters": 10,
            },
            "progress": {
                "current_chapter": 0,
                "total_words": 0,
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
                            "relationship": "当前直接对手",
                        },
                        {
                            "name": "林乔",
                            "role": "HRBP",
                            "relationship": "执行裁员的人",
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
        },
    )
    write_text(root / "大纲" / "总纲.md", outline_text)
    write_text(root / "大纲" / "章纲" / "第001章.md", outline_text)
    write_text(root / "设定集" / "角色" / "主角.md", "# 周既明\n")
    write_text(root / "设定集" / "力量体系.md", "# 亏损赔付系统\n")


def scaffold_written_project(root: Path) -> None:
    scaffold_project(root, outline_text="韩振和林乔会在曜石互联大厦继续围堵周既明。")
    state = json.loads((root / ".mighty" / "state.json").read_text(encoding="utf-8"))
    state["progress"]["current_chapter"] = 1
    state["chapter_meta"] = {
        "1": {
            "summary": "周既明在裁员会议室中反击。",
        }
    }
    state["chapter_snapshots"] = {"1": {"updated_at": "2026-03-24T00:00:00Z"}}
    state["summaries_index"] = {"1": {"summary": "周既明在裁员会议室中反击。"}}
    write_json(root / ".mighty" / "state.json", state)
    write_text(
        root / "chapters" / "第001章.md",
        (
            "周既明在曜石互联大厦会议室里盯着韩振。"
            "劳动合同电子版摊在桌上，林乔催他签字。"
        )
        * 60
        + "王妈妈在门口只出现一次。",
    )


class SettingGatePolicyTests(unittest.TestCase):
    def test_setting_gate_policy_contains_required_sections(self):
        self.assertTrue(POLICY_PATH.exists(), "setting-gate-policy.json is missing")
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        self.assertEqual(policy.get("policy_name"), "setting-gate-policy")
        self.assertIn("coverage_requirements", policy)
        self.assertIn("mcp_escalation", policy)
        self.assertIn("risk_grades", policy)


class SettingGateCoreTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        return Path(tmpdir.name)

    def test_run_gate_blocks_when_high_risk_gap_remains(self):
        self.assertTrue(SETTING_GATE_MODULE_PATH.exists(), "scripts/setting_gate.py is missing")
        module = load_setting_gate_module()
        root = self.make_project_root()
        scaffold_project(root, outline_text="本书核心冲突依赖世界观真值表与世界规则约束。")
        result = module.run_gate(project_root=root, stage="outline")
        self.assertEqual(result["status"], "blocked")
        self.assertTrue(result["blocking_gaps"])
        self.assertIn("world_rule_support", {gap["key"] for gap in result["blocking_gaps"]})
        self.assertEqual(result["minimal_next_action"]["action"], "novel-setting")
        self.assertIn("python3 scripts/setting_gate.py", result["minimal_next_action"]["suggested_commands"][0])

    def test_run_gate_materializes_local_cards_from_outline_and_state(self):
        self.assertTrue(SETTING_GATE_MODULE_PATH.exists(), "scripts/setting_gate.py is missing")
        module = load_setting_gate_module()
        root = self.make_project_root()
        scaffold_project(root, outline_text="韩振和林乔会在曜石互联大厦继续围堵周既明。")
        result = module.run_gate(project_root=root, stage="outline")
        self.assertIn("设定集/角色/韩振.md", result["auto_created_files"])
        self.assertTrue((root / "设定集" / "角色" / "韩振.md").exists())

    def test_run_gate_outline_auto_compiles_launch_stack_for_fanqie_project(self):
        self.assertTrue(SETTING_GATE_MODULE_PATH.exists(), "scripts/setting_gate.py is missing")
        module = load_setting_gate_module()
        root = self.make_project_root()
        scaffold_project(root, outline_text="韩振和林乔会在曜石互联大厦继续围堵周既明。")

        result = module.run_gate(project_root=root, stage="outline")

        self.assertEqual(result["launch_stack_action"]["status"], "compiled")
        sidecar_path = root / ".mighty" / "launch-stack.json"
        self.assertTrue(sidecar_path.exists())
        state = json.loads((root / ".mighty" / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["launch_stack_phase"], "draft")
        self.assertEqual(state["launch_stack_drift_signal"], "watch")
        self.assertTrue(state["active_launch_grammar"])
        trace_log = root / ".mighty" / "logs" / "trace.jsonl"
        self.assertTrue(trace_log.exists())
        self.assertIn("setting_gate.", trace_log.read_text(encoding="utf-8"))

    def test_mcp_candidate_requires_confirmation_and_blocks(self):
        self.assertTrue(SETTING_GATE_MODULE_PATH.exists(), "scripts/setting_gate.py is missing")
        module = load_setting_gate_module()
        policy = module.load_policy()
        graded = module.grade_candidates(
            [
                {
                    "name": "竞业协议赔偿规则",
                    "kind": "rule",
                    "source": "mcp",
                    "confidence": "medium",
                }
            ],
            policy,
        )
        self.assertEqual(graded["status"], "blocked")
        self.assertEqual(len(graded["review_items"]), 1)
        self.assertTrue(graded["review_items"][0]["requires_user_confirmation"])

    def test_load_candidates_file_reads_candidates_array(self):
        self.assertTrue(SETTING_GATE_MODULE_PATH.exists(), "scripts/setting_gate.py is missing")
        module = load_setting_gate_module()
        root = self.make_project_root()
        candidate_path = root / ".mighty" / "research-candidates.json"
        write_json(
            candidate_path,
            {
                "version": "1.0",
                "candidates": [
                    {
                        "name": "嫡庶婚配真值补证",
                        "kind": "rule",
                        "source": "mcp",
                        "confidence": "medium",
                    }
                ],
            },
        )

        loaded = module.load_candidates_file(candidate_path)

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["name"], "嫡庶婚配真值补证")

    def test_cli_candidates_file_flows_into_gate_state(self):
        root = self.make_project_root()
        scaffold_project(root, outline_text="韩振和林乔会在曜石互联大厦继续围堵周既明。")
        candidate_path = root / ".mighty" / "research-candidates.json"
        write_json(
            candidate_path,
            {
                "version": "1.0",
                "candidates": [
                    {
                        "name": "嫡庶婚配真值补证",
                        "kind": "rule",
                        "source": "mcp",
                        "confidence": "medium",
                    }
                ],
            },
        )

        subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "setting_gate.py"),
                str(root),
                "--stage",
                "outline",
                "--candidates-file",
                str(candidate_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        gate_state = json.loads((root / ".mighty" / "setting-gate.json").read_text(encoding="utf-8"))
        self.assertTrue(gate_state["mcp_used"])
        self.assertEqual(gate_state["status"], "blocked")
        self.assertEqual(gate_state["review_queue_count"], 1)
        self.assertEqual(gate_state["review_items"][0]["name"], "嫡庶婚配真值补证")
        self.assertEqual(gate_state["minimal_next_action"]["action"], "review-sync-queue")
        self.assertIn("python3 scripts/review-sync-queue.py", gate_state["minimal_next_action"]["suggested_commands"][0])

    def test_project_maintenance_runs_setting_gate_before_sync(self):
        root = self.make_project_root()
        scaffold_written_project(root)
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "project-maintenance.py"), str(root)],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)
        self.assertIn("setting_gate.py", payload["steps"])
        self.assertTrue((root / ".mighty" / "setting-gate.json").exists())

    def test_sync_review_contains_stage_confidence_and_confirmation_flags(self):
        root = self.make_project_root()
        scaffold_written_project(root)
        subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "project-maintenance.py"), str(root)],
            capture_output=True,
            text=True,
            check=True,
        )
        review_doc = json.loads((root / ".mighty" / "sync-review.json").read_text(encoding="utf-8"))
        self.assertTrue(review_doc["ambiguous_entities"])
        first = review_doc["ambiguous_entities"][0]
        self.assertIn("source_stage", first)
        self.assertIn("confidence", first)
        self.assertIn("requires_user_confirmation", first)

    def test_skill_contracts_reference_setting_gate_flow(self):
        init_text = (REPO_ROOT / "skills" / "novel-init" / "SKILL.md").read_text(encoding="utf-8")
        outline_text = (REPO_ROOT / "skills" / "novel-outline" / "SKILL.md").read_text(encoding="utf-8")
        write_text = (REPO_ROOT / "skills" / "novel-write" / "SKILL.md").read_text(encoding="utf-8")
        sync_text = (REPO_ROOT / "skills" / "novel-sync" / "SKILL.md").read_text(encoding="utf-8")
        scan_text = (REPO_ROOT / "skills" / "novel-scan" / "SKILL.md").read_text(encoding="utf-8")
        resume_text = (REPO_ROOT / "skills" / "novel-resume" / "SKILL.md").read_text(encoding="utf-8")
        status_text = (REPO_ROOT / "skills" / "novel-status" / "SKILL.md").read_text(encoding="utf-8")
        query_text = (REPO_ROOT / "skills" / "novel-query" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("setting gate(init)", init_text)
        self.assertIn("setting gate(outline)", outline_text)
        self.assertIn(".mighty/setting-gate.json", write_text)
        self.assertIn("setting gate", sync_text)
        self.assertIn("setting gate", scan_text)
        self.assertIn(".mighty/setting-gate.json", resume_text)
        self.assertIn("minimal_next_action", resume_text)
        self.assertIn(".mighty/setting-gate.json", status_text)
        self.assertIn("minimal_next_action", status_text)
        self.assertIn(".mighty/setting-gate.json", query_text)
        self.assertIn("minimal_next_action", query_text)

    def test_workflow_docs_describe_outline_hard_gate_and_write_post_sync(self):
        start_here = (REPO_ROOT / "docs" / "00-当前有效" / "start-here.md").read_text(encoding="utf-8")
        workflows = (REPO_ROOT / "docs" / "00-当前有效" / "default-workflows.md").read_text(encoding="utf-8")
        usage = (REPO_ROOT / "docs" / "00-当前有效" / "skill-usage.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        gate_triage = (REPO_ROOT / "docs" / "00-当前有效" / "gate-triage.md").read_text(encoding="utf-8")
        gate_rollout = (REPO_ROOT / "docs" / "gate-triage-rollout-2026-03-24.md").read_text(encoding="utf-8")
        maintenance = (REPO_ROOT / "docs" / "00-当前有效" / "v1-maintenance-mode.md").read_text(encoding="utf-8")
        self.assertIn("setting gate", start_here)
        self.assertIn("setting gate", workflows)
        self.assertIn("scripts/setting_gate.py", usage)
        self.assertIn("请使用 novel-query skill，告诉我当前 setting gate 的状态、blocking_gaps 和 minimal_next_action。", usage)
        self.assertIn("请使用 novel-status skill，给我一个 full 模式的项目状态面板，并额外带上 gate status、blocking_gaps 和 minimal_next_action。", usage)
        self.assertIn("请使用 novel-resume skill，如果当前项目被 setting gate 卡住，就优先告诉我 minimal_next_action 和最稳的下一步。", usage)
        self.assertIn("请使用 novel-status skill，给我一个 full 模式的项目状态面板，并额外带上 gate status、blocking_gaps 和 minimal_next_action。", start_here)
        self.assertIn("请使用 novel-resume skill，如果当前项目被 setting gate 卡住，就优先告诉我 minimal_next_action 和最稳的下一步。", start_here)
        self.assertIn("Gate Triage", readme)
        self.assertIn("novel-scan -> setting gate -> review-sync-queue", readme)
        self.assertIn("Gate Triage", workflows)
        self.assertIn("novel-status", workflows)
        self.assertIn("novel-resume", workflows)
        self.assertIn("novel-query", workflows)
        self.assertIn("gate-triage.md", readme)
        self.assertIn("gate-triage.md", workflows)
        self.assertIn("gate-triage.md", start_here)
        self.assertIn("gate-triage.md", usage)
        self.assertIn("novel-scan -> setting gate -> review-sync-queue", gate_triage)
        self.assertIn("minimal_next_action", gate_triage)
        self.assertIn("gate-triage-rollout-2026-03-24.md", readme)
        self.assertIn("setting gate", gate_rollout)
        self.assertIn("novel-resume", gate_rollout)
        self.assertIn("gate triage", maintenance)
        self.assertIn("默认工作流", maintenance)


if __name__ == "__main__":
    unittest.main()
