import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "fanqie_launch_stack.py"

FRAMEWORK_FILES = [
    "docs/opening-and-plot-framework/fanqie-launch-stack/README.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/01-premise-layer.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/02-pivot-layer.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/03-launch-grammar-layer.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/04-retention-protocol-layer.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/05-compiler-contract.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/README.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/oppression-breakout.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/bonding-reversal.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/rule-trial.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/resource-climb.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/investigation-reveal.md",
    "docs/opening-and-plot-framework/fanqie-launch-stack/launch-grammars/ensemble-return.md",
]

SCRIPT_FILES = [
    "scripts/fanqie_launch_stack.py",
]

SKILL_EXPECTATIONS = {
    "skills/novel-outline/SKILL.md": [
        "../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md",
        "../../docs/opening-and-plot-framework/fanqie-launch-stack/05-compiler-contract.md",
        ".mighty/launch-stack.json",
    ],
    "skills/novel-write/SKILL.md": [
        "../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md",
        ".mighty/launch-stack.json",
        "chapter_1_3_targets",
    ],
    "skills/novel-review/SKILL.md": [
        "../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md",
        ".mighty/launch-stack.json",
        "launch_alignment",
        "drift_signal",
    ],
    "skills/novel-precheck/SKILL.md": [
        "../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md",
        ".mighty/launch-stack.json",
        "drift_signal",
    ],
    "skills/novel-package/SKILL.md": [
        "../../docs/opening-and-plot-framework/fanqie-launch-stack/README.md",
        ".mighty/launch-stack.json",
        "package_guardrails",
    ],
}

STATE_SCHEMA_EXPECTED_TOKENS = [
    "active_launch_grammar",
    "active_primary_pivot",
    "launch_stack_phase",
    "launch_stack_drift_signal",
]

STATE_TEMPLATE_EXPECTED_TOKENS = [
    "active_launch_grammar",
    "active_primary_pivot",
    "launch_stack_phase",
    "launch_stack_drift_signal",
]

INIT_AND_THINNING_DOCS = {
    "skills/novel-init/SKILL.md": [
        ".mighty/launch-stack.json",
        "active_launch_grammar",
        "active_primary_pivot",
    ],
    "docs/state-thinning-and-setting-sync.md": [
        ".mighty/launch-stack.json",
        "launch_stack",
    ],
}

ENTRY_DOCS = {
    "README.md": "番茄起盘协议栈",
    "docs/start-here.md": "番茄起盘协议栈",
    "docs/skill-usage.md": "番茄起盘协议栈",
    "docs/default-workflows.md": "番茄起盘协议栈",
    "docs/opening-and-plot-framework/README.md": "fanqie-launch-stack",
}

SMOKE_ARTIFACTS = [
    "docs/opening-and-plot-framework/fanqie-launch-stack-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.json",
    "docs/opening-and-plot-framework/fanqie-launch-stack-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.json",
]


def load_module():
    spec = importlib.util.spec_from_file_location("fanqie_launch_stack", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FanqieLaunchStackContractTests(unittest.TestCase):
    def test_framework_files_exist(self):
        for relative_path in FRAMEWORK_FILES:
            path = REPO_ROOT / relative_path
            self.assertTrue(path.exists(), f"Missing framework file: {relative_path}")

    def test_script_exists(self):
        for relative_path in SCRIPT_FILES:
            path = REPO_ROOT / relative_path
            self.assertTrue(path.exists(), f"Missing launch-stack script: {relative_path}")

    def test_skills_reference_launch_stack(self):
        for relative_path, expected_tokens in SKILL_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_state_schema_mentions_light_launch_stack_mirrors(self):
        content = (REPO_ROOT / "shared/references/shared/state-schema.md").read_text(encoding="utf-8")
        for token in STATE_SCHEMA_EXPECTED_TOKENS:
            self.assertIn(token, content)

    def test_state_template_mentions_light_launch_stack_mirrors(self):
        content = (REPO_ROOT / "shared/templates/state-v5-template.json").read_text(encoding="utf-8")
        for token in STATE_TEMPLATE_EXPECTED_TOKENS:
            self.assertIn(token, content)

    def test_init_and_thinning_docs_reference_launch_stack_sidecar(self):
        for relative_path, expected_tokens in INIT_AND_THINNING_DOCS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_entry_docs_expose_launch_stack(self):
        for relative_path, token in ENTRY_DOCS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_smoke_artifacts_exist(self):
        for relative_path in SMOKE_ARTIFACTS:
            self.assertTrue((REPO_ROOT / relative_path).exists(), f"Missing smoke artifact: {relative_path}")

    def test_smoke_artifacts_have_non_empty_core_fields(self):
        for relative_path in SMOKE_ARTIFACTS:
            payload = json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
            self.assertTrue(payload["primary_pivot"], relative_path)
            self.assertTrue(payload["launch_grammar"]["primary"], relative_path)
            self.assertTrue(payload["compiler_output"]["outline_focus"], relative_path)


class FanqieLaunchStackCliTests(unittest.TestCase):
    def test_parse_args_defaults_to_draft(self):
        module = load_module()

        args = module.parse_args(
            [
                "--project-root",
                "/tmp/project",
                "--chapter",
                "003",
                "--chapters",
                "001-003",
            ]
        )

        self.assertEqual(args.mode, "draft")
        self.assertFalse(args.writeback)

    def test_parse_args_accepts_output_path(self):
        module = load_module()

        args = module.parse_args(
            [
                "--project-root",
                "/tmp/project",
                "--chapter",
                "003",
                "--chapters",
                "001-003",
                "--output",
                "/tmp/out.json",
            ]
        )

        self.assertEqual(args.output, "/tmp/out.json")


class FanqieLaunchStackHelperTests(unittest.TestCase):
    def test_load_state_reads_project_state(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            payload = {
                "meta": {"title": "离婚冷静期那天，前夫把董事会席位押给了我", "genre": "职场婚恋", "platform": "番茄"},
                "genre_profile": {"bucket": "职场婚恋"},
            }
            (mighty / "state.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            state = module.load_state(project_root)

            self.assertEqual(state["meta"]["title"], payload["meta"]["title"])

    def test_load_total_outline_reads_outline_text(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            outline_dir = project_root / "大纲"
            outline_dir.mkdir(parents=True)
            outline_text = "# 总纲\n曜衡并购盘与离婚冷静期同时压来。"
            (outline_dir / "总纲.md").write_text(outline_text, encoding="utf-8")

            self.assertEqual(module.load_total_outline(project_root), outline_text)

    def test_load_chapter_texts_reads_requested_chapters(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            chapters_dir = project_root / "chapters"
            chapters_dir.mkdir(parents=True)
            (chapters_dir / "第001章.md").write_text("第001章：离婚冷静期。", encoding="utf-8")
            (chapters_dir / "第002章.md").write_text("第002章：董事会试运营。", encoding="utf-8")

            texts = module.load_chapter_texts(project_root, "001-002")

            self.assertEqual(texts["001"], "第001章：离婚冷静期。")
            self.assertEqual(texts["002"], "第002章：董事会试运营。")

    def test_infer_pivot_candidates_prefers_character_conflict_for_relation_forward_project(self):
        module = load_module()

        state = {
            "meta": {"title": "离婚冷静期那天，前夫把董事会席位押给了我", "genre": "职场婚恋", "platform": "番茄"},
            "genre_profile": {"bucket": "职场婚恋"},
        }
        outline_text = "离婚冷静期、董事会席位、前夫重新绑定她的站位。"
        chapter_texts = {
            "001": "签离婚协议那天，前夫把董事会席位押给了我。",
            "002": "她为了试运营必须继续与他共事。",
        }

        candidates = module.infer_pivot_candidates(state, outline_text, chapter_texts)

        self.assertEqual(candidates[0]["id"], "character-conflict")

    def test_infer_launch_grammar_candidates_prefers_bonding_reversal_for_relation_forward_project(self):
        module = load_module()

        state = {
            "meta": {"title": "离婚冷静期那天，前夫把董事会席位押给了我", "genre": "职场婚恋", "platform": "番茄"},
            "genre_profile": {"bucket": "职场婚恋"},
        }
        pivot_candidates = [
            {"id": "character-conflict", "score": 0.9},
            {"id": "inciting-event", "score": 0.6},
        ]
        outline_text = "离婚冷静期、董事会席位、前夫重新绑定她的站位。"
        chapter_texts = {
            "001": "签离婚协议那天，前夫把董事会席位押给了我。",
            "002": "她为了试运营必须继续与他共事。",
        }

        candidates = module.infer_launch_grammar_candidates(state, pivot_candidates, outline_text, chapter_texts)

        self.assertEqual(candidates[0]["id"], "bonding-reversal")

    def test_compile_launch_stack_returns_compiler_output(self):
        module = load_module()

        state = {
            "meta": {"title": "离婚冷静期那天，前夫把董事会席位押给了我", "genre": "职场婚恋", "platform": "番茄"},
            "genre_profile": {"bucket": "职场婚恋"},
        }
        outline_text = "离婚冷静期、董事会席位、前夫重新绑定她的站位。"
        chapter_texts = {
            "001": "签离婚协议那天，前夫把董事会席位押给了我。",
            "002": "她为了试运营必须继续与他共事。",
            "003": "她拿到了第一轮试运营权限，但也留下了董事会残账。",
        }

        result = module.compile_launch_stack(state, outline_text, chapter_texts, chapter="003", chapters="001-003")

        self.assertIn("premise_line", result)
        self.assertIn("primary_pivot", result)
        self.assertIn("launch_grammar", result)
        self.assertIn("retention_protocol", result)
        self.assertIn("compiler_output", result)
        self.assertIn("chapter_1_3_targets", result["compiler_output"])


class FanqieLaunchStackWritebackTests(unittest.TestCase):
    def test_writeback_requires_explicit_flag(self):
        module = load_module()

        args = module.parse_args(
            [
                "--project-root",
                "/tmp/project",
                "--chapter",
                "003",
                "--chapters",
                "001-003",
                "--mode",
                "writeback",
            ]
        )

        self.assertFalse(module.allow_writeback(args))

    def test_writeback_creates_sidecar_and_light_state_mirrors(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            outline_dir = project_root / "大纲"
            chapters_dir = project_root / "chapters"
            mighty.mkdir(parents=True)
            outline_dir.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            state_payload = {
                "meta": {
                    "title": "离婚冷静期那天，前夫把董事会席位押给了我",
                    "genre": "职场婚恋",
                    "platform": "番茄",
                },
                "genre_profile": {"bucket": "职场婚恋"},
                "chapter_meta": {"003": {"review_score": 88, "fanqie_bucket_summary": {"bucket": "职场婚恋"}}},
            }
            (mighty / "state.json").write_text(json.dumps(state_payload, ensure_ascii=False), encoding="utf-8")
            (outline_dir / "总纲.md").write_text("离婚冷静期与董事会席位绑定在一起。", encoding="utf-8")
            (chapters_dir / "第001章.md").write_text("离婚协议与董事会席位同时压来。", encoding="utf-8")
            (chapters_dir / "第002章.md").write_text("她为了试运营继续与前夫共事。", encoding="utf-8")
            (chapters_dir / "第003章.md").write_text("她拿到第一次硬兑现，也留下董事会残账。", encoding="utf-8")

            result = module.run_launch_stack(
                project_root=project_root,
                chapter="003",
                chapters="001-003",
                mode="writeback",
                writeback=True,
            )

            self.assertEqual(result["effective_mode"], "writeback")
            sidecar = json.loads((mighty / "launch-stack.json").read_text(encoding="utf-8"))
            self.assertEqual(sidecar["primary_pivot"], "character-conflict")
            state = json.loads((mighty / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["active_launch_grammar"], sidecar["launch_grammar"]["primary"])
            self.assertEqual(state["active_primary_pivot"], sidecar["primary_pivot"])
            self.assertIn("launch_stack_phase", state)
            self.assertIn("launch_stack_drift_signal", state)
            self.assertEqual(state["chapter_meta"]["003"]["review_score"], 88)
            self.assertEqual(state["chapter_meta"]["003"]["fanqie_bucket_summary"]["bucket"], "职场婚恋")

    def test_writeback_does_not_overwrite_existing_sidecar_without_force(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            outline_dir = project_root / "大纲"
            chapters_dir = project_root / "chapters"
            mighty.mkdir(parents=True)
            outline_dir.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            (mighty / "state.json").write_text(
                json.dumps(
                    {
                        "meta": {"title": "Demo", "genre": "职场婚恋", "platform": "番茄"},
                        "genre_profile": {"bucket": "职场婚恋"},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (mighty / "launch-stack.json").write_text(json.dumps({"primary_pivot": "old"}, ensure_ascii=False), encoding="utf-8")
            (outline_dir / "总纲.md").write_text("离婚冷静期与董事会席位绑定在一起。", encoding="utf-8")
            (chapters_dir / "第001章.md").write_text("离婚协议与董事会席位同时压来。", encoding="utf-8")
            (chapters_dir / "第002章.md").write_text("她为了试运营继续与前夫共事。", encoding="utf-8")
            (chapters_dir / "第003章.md").write_text("她拿到第一次硬兑现，也留下董事会残账。", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "launch-stack.json already exists"):
                module.run_launch_stack(
                    project_root=project_root,
                    chapter="003",
                    chapters="001-003",
                    mode="writeback",
                    writeback=True,
                )


if __name__ == "__main__":
    unittest.main()
