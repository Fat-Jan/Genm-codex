import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "build_content_positioning.py"
SCHEMA_PATH = REPO_ROOT / "shared" / "templates" / "content-positioning-v1.schema.json"


def load_module():
    spec = importlib.util.spec_from_file_location("build_content_positioning", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ContentPositioningTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name)
        write_json(
            root / ".mighty" / "state.json",
            {
                "meta": {"title": "组合题材测试"},
                "genre_profile": {
                    "loaded": "shared/profiles/urban-brainhole/profile.yaml",
                    "bucket": "科幻末世",
                    "tagpacks": ["穿越生存"],
                    "strong_tags": ["末世", "大佬"],
                    "narrative_modes": ["多主题副本", "多角色群像"],
                    "tone_guardrails": ["搞笑轻松", "非套路"],
                    "positioning_sidecar": ".mighty/content-positioning.json",
                },
            },
        )
        return root

    def test_module_and_schema_exist(self) -> None:
        self.assertTrue(MODULE_PATH.exists())
        self.assertTrue(SCHEMA_PATH.exists())

    def test_build_content_positioning_uses_genre_profile_fields(self) -> None:
        module = load_module()
        root = self.make_project_root()

        payload = module.build_content_positioning(root, timestamp="2026-03-26T00:00:00Z")

        self.assertEqual(payload["primary_profile"], "urban-brainhole")
        self.assertEqual(payload["primary_bucket"], "科幻末世")
        self.assertEqual(payload["tagpacks"], ["穿越生存"])
        self.assertIn("多主题副本", payload["narrative_modes"])
        self.assertIn("tagpack:穿越生存", payload["compiler_output"]["package_cues"])
        self.assertIn("opening_hook_cues", payload)
        self.assertIn("payoff_cadence", payload)
        self.assertIn("reader_motive", payload)
        self.assertEqual(payload["freshness"]["artifact_key"], "content-positioning")
        self.assertEqual(payload["freshness"]["contract"], "sidecar-freshness-v1")
        self.assertIn("state.json", payload["freshness"]["inputs"])

    def test_build_content_positioning_falls_back_to_mapping_defaults(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_json(
                root / ".mighty" / "state.json",
                {
                    "meta": {"title": "宫斗测试", "platform": "番茄"},
                    "genre_profile": {
                        "loaded": "shared/profiles/palace-intrigue/profile.yaml",
                        "bucket": "",
                        "tagpacks": [],
                        "strong_tags": [],
                        "narrative_modes": [],
                        "tone_guardrails": [],
                        "positioning_sidecar": ".mighty/content-positioning.json",
                    },
                },
            )

            payload = module.build_content_positioning(root, timestamp="2026-03-26T00:00:00Z")

            self.assertEqual(payload["primary_bucket"], "宫斗宅斗")
            self.assertIn("高门关系", payload["strong_tags"])
            self.assertIn("多角色群像", payload["narrative_modes"])
            self.assertIn("cue:婚配错位前置", payload["compiler_output"]["package_cues"])

    def test_build_content_positioning_can_consume_bucket_overlay_from_state_bucket(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_json(
                root / ".mighty" / "state.json",
                {
                    "meta": {"title": "宅门测试", "platform": "番茄"},
                    "genre_profile": {
                        "loaded": "shared/profiles/palace-intrigue/profile.yaml",
                        "bucket": "宫斗宅斗",
                        "tagpacks": [],
                        "strong_tags": [],
                        "narrative_modes": [],
                        "tone_guardrails": [],
                        "positioning_sidecar": ".mighty/content-positioning.json",
                    },
                },
            )

            payload = module.build_content_positioning(root, timestamp="2026-03-28T00:00:00Z")

            self.assertIn("宅门账本", payload["narrative_modes"])
            self.assertIn("高门称谓必须闭环", payload["tone_guardrails"])
            self.assertIn("cue:宅门账本前置", payload["compiler_output"]["package_cues"])

    def test_bucket_only_project_can_use_bucket_defaults(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_json(
                root / ".mighty" / "state.json",
                {
                    "meta": {"title": "合租房测试", "platform": "番茄"},
                    "genre_profile": {
                        "loaded": "",
                        "bucket": "职场婚恋",
                        "positioning_initialized": False,
                        "tagpacks": [],
                        "strong_tags": [],
                        "narrative_modes": [],
                        "tone_guardrails": [],
                        "positioning_sidecar": ".mighty/content-positioning.json",
                    },
                },
            )

            payload = module.build_content_positioning(root, timestamp="2026-03-26T00:00:00Z")

            self.assertEqual(payload["primary_bucket"], "职场婚恋")
            self.assertIn("先婚后爱", payload["strong_tags"])
            self.assertIn("双线并进", payload["narrative_modes"])
            self.assertIn("cue:首屏点关系绑定", payload["compiler_output"]["package_cues"])

    def test_empty_lists_can_override_defaults_when_positioning_initialized(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_json(
                root / ".mighty" / "state.json",
                {
                    "meta": {"title": "宫斗测试", "platform": "番茄"},
                    "genre_profile": {
                        "loaded": "shared/profiles/palace-intrigue/profile.yaml",
                        "bucket": "宫斗宅斗",
                        "positioning_initialized": True,
                        "tagpacks": [],
                        "strong_tags": [],
                        "narrative_modes": [],
                        "tone_guardrails": [],
                        "positioning_sidecar": ".mighty/content-positioning.json",
                    },
                },
            )

            payload = module.build_content_positioning(root, timestamp="2026-03-26T00:00:00Z")

            self.assertEqual(payload["primary_bucket"], "宫斗宅斗")
            self.assertEqual(payload["strong_tags"], [])
            self.assertEqual(payload["narrative_modes"], [])
            self.assertEqual(payload["tone_guardrails"], [])

    def test_build_content_positioning_can_use_sibling_platform_overlay_without_map_defaults(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_json(
                root / ".mighty" / "state.json",
                {
                    "meta": {"title": "玄幻测试", "platform": "番茄"},
                    "genre_profile": {
                        "loaded": "shared/profiles/xuanhuan/profile.yaml",
                        "bucket": "",
                        "tagpacks": [],
                        "strong_tags": [],
                        "narrative_modes": [],
                        "tone_guardrails": [],
                        "positioning_sidecar": ".mighty/content-positioning.json",
                    },
                },
            )

            original_loader = module.load_mapping_registry
            module.load_mapping_registry = lambda _project_root: {"profiles": {}, "bucket_defaults": {}}
            try:
                payload = module.build_content_positioning(root, timestamp="2026-03-26T00:00:00Z")
            finally:
                module.load_mapping_registry = original_loader

            self.assertEqual(payload["primary_bucket"], "玄幻脑洞")
            self.assertIn("金手指", payload["strong_tags"])

    def test_system_profile_has_second_round_positioning_defaults(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_json(
                root / ".mighty" / "state.json",
                {
                    "meta": {"title": "系统测试", "platform": "番茄"},
                    "genre_profile": {
                        "loaded": "shared/profiles/system/profile.yaml",
                        "bucket": "",
                        "tagpacks": [],
                        "strong_tags": [],
                        "narrative_modes": [],
                        "tone_guardrails": [],
                        "positioning_sidecar": ".mighty/content-positioning.json",
                    },
                },
            )

            payload = module.build_content_positioning(root, timestamp="2026-03-26T00:00:00Z")

            self.assertEqual(payload["primary_bucket"], "都市脑洞")
            self.assertIn("系统", payload["strong_tags"])
            self.assertIn("cue:前三章要有一次任务兑现", payload["compiler_output"]["package_cues"])
            self.assertTrue(payload["opening_hook_cues"])
            self.assertTrue(payload["payoff_cadence"])
            self.assertTrue(payload["reader_motive"])

    def test_romance_profile_has_second_round_positioning_defaults(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_json(
                root / ".mighty" / "state.json",
                {
                    "meta": {"title": "言情测试", "platform": "番茄"},
                    "genre_profile": {
                        "loaded": "shared/profiles/romance/profile.yaml",
                        "bucket": "",
                        "tagpacks": [],
                        "strong_tags": [],
                        "narrative_modes": [],
                        "tone_guardrails": [],
                        "positioning_sidecar": ".mighty/content-positioning.json",
                    },
                },
            )

            payload = module.build_content_positioning(root, timestamp="2026-03-26T00:00:00Z")

            self.assertEqual(payload["primary_bucket"], "青春甜宠")
            self.assertIn("高甜", payload["strong_tags"])
            self.assertTrue(payload["reader_motive"])

    def test_cli_writes_content_positioning_sidecar(self) -> None:
        module = load_module()
        root = self.make_project_root()

        result = module.main([str(root), "--timestamp", "2026-03-26T00:00:00Z"])

        sidecar_path = root / ".mighty" / "content-positioning.json"
        self.assertTrue(sidecar_path.exists())
        self.assertEqual(result["content_positioning_file"], str(sidecar_path))
        self.assertTrue(Path(result["trace_log_file"]).exists())


if __name__ == "__main__":
    unittest.main()
