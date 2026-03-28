import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "profile_contract.py"
SCHEMA_PATH = REPO_ROOT / "shared" / "templates" / "profile-contract-v1.schema.json"
PROFILE_ROOT = REPO_ROOT / "shared" / "profiles"


def load_module():
    spec = importlib.util.spec_from_file_location("profile_contract", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProfileContractTests(unittest.TestCase):
    def test_contract_module_and_schema_exist(self) -> None:
        self.assertTrue(MODULE_PATH.exists())
        self.assertTrue(SCHEMA_PATH.exists())

    def test_normalize_profile_handles_known_variants(self) -> None:
        module = load_module()

        palace = module.normalize_profile(
            module.load_profile(PROFILE_ROOT / "palace-intrigue" / "profile.yaml"),
            source_path="shared/profiles/palace-intrigue/profile.yaml",
        )
        urban = module.normalize_profile(
            module.load_profile(PROFILE_ROOT / "urban-brainhole" / "profile.yaml"),
            source_path="shared/profiles/urban-brainhole/profile.yaml",
        )

        self.assertEqual(palace["cool_points"]["density"], 0.8)
        self.assertEqual(palace["reader_expectations"]["must_not"][0], "对手全是蠢货")
        self.assertEqual(urban["cool_points"]["density"], "1.3/千字")
        self.assertEqual(urban["taboos"][0]["id"], "TABOO-001")
        self.assertEqual(urban["taboos"][0]["checkpoint"], "设定设计")
        self.assertFalse(urban["notes"]["has_dialogue_templates"])
        self.assertFalse(urban["notes"]["has_scene_description"])

    def test_state_summary_projection_matches_current_state_shape(self) -> None:
        module = load_module()
        normalized = module.normalize_profile(
            module.load_profile(PROFILE_ROOT / "xuanhuan" / "profile.yaml"),
            source_path="shared/profiles/xuanhuan/profile.yaml",
        )
        summary = module.summarize_for_state(normalized)

        self.assertEqual(summary["loaded"], "shared/profiles/xuanhuan/profile.yaml")
        self.assertEqual(summary["positioning_sidecar"], ".mighty/content-positioning.json")
        self.assertEqual(summary["tagpacks"], [])
        self.assertIn("type", summary["节奏"])
        self.assertIn("density", normalized["cool_points"])
        self.assertIn("quest", summary["strand权重"])
        self.assertIsInstance(summary["特殊约束"], list)

    def test_state_summary_can_project_platform_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "xuanhuan" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/xuanhuan/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "玄幻脑洞")
        self.assertTrue(summary["positioning_initialized"])
        self.assertIn("金手指", summary["strong_tags"])
        self.assertIn("多主题副本", summary["narrative_modes"])
        self.assertIn("升级必须有代价", summary["tone_guardrails"])

    def test_state_summary_can_apply_bucket_overlay(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "palace-intrigue" / "profile.yaml",
            platform="fanqie",
            bucket="宫斗宅斗",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/palace-intrigue/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertIn("宅门账本", summary["narrative_modes"])
        self.assertIn("高门称谓必须闭环", summary["tone_guardrails"])

    def test_layer_descriptor_uses_core_overlay_reference_split(self) -> None:
        module = load_module()
        descriptor = module.resolve_profile_layers(PROFILE_ROOT / "xuanhuan", platform="tomato")

        self.assertTrue(descriptor["core_profile"].endswith("shared/profiles/xuanhuan/profile.yaml"))
        self.assertTrue(descriptor["platform_overlay"].endswith("shared/profiles/xuanhuan/profile-tomato.yaml"))
        self.assertIsNone(descriptor["bucket_overlay"])
        self.assertIn("cool-points.md", descriptor["reference_files"])

    def test_layer_descriptor_can_resolve_bucket_overlay_from_bucket_name(self) -> None:
        module = load_module()
        descriptor = module.resolve_profile_layers(PROFILE_ROOT / "palace-intrigue", platform="fanqie", bucket="宫斗宅斗")

        self.assertTrue(descriptor["bucket_overlay"].endswith("shared/profiles/palace-intrigue/bucket-palace-intrigue.yaml"))

    def test_layer_descriptor_can_resolve_bucket_overlay_from_fanqie_bucket_key(self) -> None:
        module = load_module()
        descriptor = module.resolve_profile_layers(PROFILE_ROOT / "palace-intrigue", platform="fanqie", bucket="gongdou_zhai")

        self.assertTrue(descriptor["bucket_overlay"].endswith("shared/profiles/palace-intrigue/bucket-palace-intrigue.yaml"))

    def test_layer_descriptor_can_resolve_bucket_overlay_from_platform_overlay_bucket_name(self) -> None:
        module = load_module()
        descriptor = module.resolve_profile_layers(PROFILE_ROOT / "xuanhuan", platform="fanqie", bucket="玄幻脑洞")

        self.assertTrue(descriptor["bucket_overlay"].endswith("shared/profiles/xuanhuan/bucket-xuanhuan.yaml"))

    def test_all_profiles_normalize_to_contract_shape(self) -> None:
        module = load_module()
        required_keys = set(json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["required"])

        profile_paths = sorted(PROFILE_ROOT.glob("*/profile.yaml"))
        self.assertGreater(len(profile_paths), 0)

        for path in profile_paths:
            normalized = module.normalize_profile(module.load_profile(path), source_path=str(path.relative_to(REPO_ROOT)))
            self.assertEqual(required_keys, set(normalized.keys()), path.name)
            self.assertTrue(normalized["name"], path.name)
            self.assertTrue(normalized["display_name"], path.name)
            self.assertIn("word_count", normalized["pacing"], path.name)
            self.assertIn("density", normalized["cool_points"], path.name)
            self.assertIn("must_not", normalized["reader_expectations"], path.name)

    def test_docs_describe_profile_contract_layers(self) -> None:
        readme = (REPO_ROOT / "shared" / "profiles" / "README.md").read_text(encoding="utf-8")
        schema_doc = (REPO_ROOT / "shared" / "references" / "shared" / "state-schema.md").read_text(encoding="utf-8")
        for token in ("core profile", "platform overlay", "bucket overlay", "reference files"):
            self.assertIn(token, readme)
        for token in ("genre_profile", "投影层", "raw profile dump", "content-positioning"):
            self.assertIn(token, schema_doc)

    def test_first_batch_profiles_moved_legacy_reference_out_of_yaml(self) -> None:
        expectations = {
            "shared/profiles/urban-brainhole/profile.yaml": "shared/profiles/urban-brainhole/reference-notes.md",
            "shared/profiles/workplace-romance/profile.yaml": "shared/profiles/workplace-romance/reference-notes.md",
            "shared/profiles/palace-intrigue/profile.yaml": "shared/profiles/palace-intrigue/reference-notes.md",
        }
        for yaml_path, notes_path in expectations.items():
            content = (REPO_ROOT / yaml_path).read_text(encoding="utf-8")
            self.assertIn("reference_files:", content)
            self.assertTrue((REPO_ROOT / notes_path).exists())

    def test_second_round_profiles_move_legacy_reference_out_of_yaml(self) -> None:
        expectations = {
            "shared/profiles/apocalypse/profile.yaml": "shared/profiles/apocalypse/reference-notes.md",
            "shared/profiles/historical/profile.yaml": "shared/profiles/historical/reference-notes.md",
            "shared/profiles/romance/profile.yaml": "shared/profiles/romance/reference-notes.md",
        }
        for yaml_path, notes_path in expectations.items():
            content = (REPO_ROOT / yaml_path).read_text(encoding="utf-8")
            self.assertIn("reference_files:", content)
            self.assertTrue((REPO_ROOT / notes_path).exists())

    def test_first_batch_bucket_overlay_files_exist(self) -> None:
        expected = [
            "shared/profiles/palace-intrigue/bucket-palace-intrigue.yaml",
            "shared/profiles/urban-brainhole/bucket-urban-brainhole.yaml",
            "shared/profiles/urban-daily/bucket-urban-daily.yaml",
            "shared/profiles/sweet-youth/bucket-sweet-youth.yaml",
            "shared/profiles/ceo-romance/bucket-ceo-romance.yaml",
            "shared/profiles/workplace-romance/bucket-workplace-romance.yaml",
            "shared/profiles/historical-brainhole/bucket-historical-brainhole.yaml",
            "shared/profiles/xuanhuan/bucket-xuanhuan.yaml",
        ]
        for relative_path in expected:
            self.assertTrue((REPO_ROOT / relative_path).exists(), relative_path)

    def test_all_profiles_with_fanqie_primary_bucket_resolve_bucket_overlay(self) -> None:
        module = load_module()
        profile_paths = sorted(PROFILE_ROOT.glob("*/profile.yaml"))
        for path in profile_paths:
            profile_dir = path.parent
            raw = module.load_profile(path)
            platform_overlay = module.resolve_platform_overlay_path(profile_dir, "fanqie")
            if platform_overlay is not None:
                raw = module.merge_profile_layers(raw, module.load_profile(platform_overlay))
            positioning = module.resolve_platform_positioning(raw, platform="fanqie")
            if not isinstance(positioning, dict):
                continue
            bucket_name = positioning.get("primary_bucket")
            if not isinstance(bucket_name, str) or not bucket_name:
                continue
            bucket_overlay = module.resolve_bucket_overlay_path(profile_dir, bucket_name, raw_profile=raw)
            self.assertIsNotNone(bucket_overlay, f"{profile_dir.name} missing bucket overlay for {bucket_name}")

    def test_batch_one_profiles_expose_platform_positioning_with_package_cues(self) -> None:
        module = load_module()
        expectations = {
            "palace-intrigue": "宫斗宅斗",
            "urban-brainhole": "都市脑洞",
            "urban-daily": "都市日常",
            "ceo-romance": "豪门总裁",
            "sweet-youth": "青春甜宠",
            "workplace-romance": "职场婚恋",
            "historical-brainhole": "历史脑洞",
            "xuanhuan": "玄幻脑洞",
            "xiuxian": "传统玄幻",
            "realistic": "现实情感",
            "system": "都市脑洞",
        }

        for slug, expected_bucket in expectations.items():
            raw = module.load_profile_with_overlays(
                PROFILE_ROOT / slug / "profile.yaml",
                platform="fanqie",
            )
            normalized = module.normalize_profile(
                raw,
                source_path=f"shared/profiles/{slug}/profile.yaml",
            )
            summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

            self.assertEqual(summary["bucket"], expected_bucket)
            self.assertTrue(summary["strong_tags"], slug)
            self.assertTrue(summary["narrative_modes"], slug)
            self.assertTrue(summary["tone_guardrails"], slug)

    def test_next_batch_profiles_can_surface_overlay_strengthened_positioning(self) -> None:
        module = load_module()
        expectations = {
            "urban-brainhole": {
                "bucket": "都市脑洞",
                "mode": "反差连锁",
                "guardrail": "反差设定必须尽快兑现",
            },
            "workplace-romance": {
                "bucket": "职场婚恋",
                "mode": "关系工作同场换账",
                "guardrail": "办公室权力关系要具体",
            },
            "urban-daily": {
                "bucket": "都市日常",
                "mode": "日常账本",
                "guardrail": "关系升温必须伴随现实牵连",
            },
        }

        for slug, expected in expectations.items():
            raw = module.load_profile_with_overlays(
                PROFILE_ROOT / slug / "profile.yaml",
                platform="fanqie",
                bucket=expected["bucket"],
            )
            normalized = module.normalize_profile(
                raw,
                source_path=f"shared/profiles/{slug}/profile.yaml",
            )
            summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

            self.assertIn(expected["mode"], summary["narrative_modes"], slug)
            self.assertIn(expected["guardrail"], summary["tone_guardrails"], slug)

    def test_batch_two_profiles_fill_basic_narrative_modes(self) -> None:
        module = load_module()
        expectations = {
            "melodrama": {
                "bucket": "豪门总裁",
                "mode": "误会追妻双线",
            },
            "sweet-romance": {
                "bucket": "青春甜宠",
                "mode": "高甜日常推进",
            },
        }

        for slug, expected in expectations.items():
            raw = module.load_profile_with_overlays(
                PROFILE_ROOT / slug / "profile.yaml",
                platform="fanqie",
            )
            normalized = module.normalize_profile(
                raw,
                source_path=f"shared/profiles/{slug}/profile.yaml",
            )
            summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

            self.assertEqual(summary["bucket"], expected["bucket"])
            self.assertIn(expected["mode"], summary["narrative_modes"], slug)

    def test_urban_superpower_can_expose_fanqie_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "urban-superpower" / "profile.yaml",
            platform="fanqie",
            bucket="都市脑洞",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/urban-superpower/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "都市脑洞")
        self.assertIn("异能", summary["strong_tags"])
        self.assertIn("多主题副本", summary["narrative_modes"])
        self.assertIn("异能展示要伴随现实后果", summary["tone_guardrails"])

    def test_realistic_profile_already_matches_cross_platform_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "realistic" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/realistic/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "现实情感")
        self.assertIn("现实困局", summary["strong_tags"])
        self.assertIn("成长", summary["strong_tags"])
        self.assertIn("现实代价不能消失", summary["tone_guardrails"])
        self.assertIn("治愈不等于无后果", summary["tone_guardrails"])

    def test_historical_brainhole_profile_matches_cross_platform_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "historical-brainhole" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/historical-brainhole/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "历史脑洞")
        self.assertIn("穿越", summary["strong_tags"])
        self.assertIn("权谋", summary["strong_tags"])
        self.assertIn("历史感不能被现代腔冲掉", summary["tone_guardrails"])
        self.assertIn("创意设定必须自洽", summary["tone_guardrails"])

    def test_palace_intrigue_profile_can_surface_cross_platform_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "palace-intrigue" / "profile.yaml",
            platform="fanqie",
            bucket="宫斗宅斗",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/palace-intrigue/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "宫斗宅斗")
        self.assertIn("高门关系", summary["strong_tags"])
        self.assertIn("婚配错位", summary["strong_tags"])
        self.assertIn("强压后必须换账", summary["tone_guardrails"])
        self.assertIn("高门称谓必须闭环", summary["tone_guardrails"])

    def test_system_profile_can_surface_cross_platform_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "system" / "profile.yaml",
            platform="fanqie",
            bucket="都市脑洞",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/system/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "都市脑洞")
        self.assertIn("系统", summary["strong_tags"])
        self.assertIn("逆袭", summary["strong_tags"])
        self.assertIn("系统奖励不能替代成长", summary["tone_guardrails"])
        self.assertIn("任务推进要和主线冲突绑定", summary["tone_guardrails"])

    def test_xuanhuan_profile_can_surface_cross_platform_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "xuanhuan" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/xuanhuan/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "玄幻脑洞")
        self.assertIn("金手指", summary["strong_tags"])
        self.assertIn("成长", summary["strong_tags"])
        self.assertIn("升级必须有代价", summary["tone_guardrails"])
        self.assertIn("爽点不能替代世界规则", summary["tone_guardrails"])

    def test_xiuxian_profile_matches_cross_platform_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "xiuxian" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/xiuxian/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "传统玄幻")
        self.assertIn("宗门", summary["strong_tags"])
        self.assertIn("成长", summary["strong_tags"])
        self.assertIn("升级必须有代价", summary["tone_guardrails"])
        self.assertIn("机缘不能白拿", summary["tone_guardrails"])

    def test_romance_profile_matches_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "romance" / "profile.yaml",
            platform="fanqie",
            bucket="青春甜宠",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/romance/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "青春甜宠")
        self.assertIn("高甜", summary["strong_tags"])
        self.assertIn("情感拉扯", summary["strong_tags"])
        self.assertIn("甜感不能空转", summary["tone_guardrails"])
        self.assertIn("误会不能纯靠不沟通", summary["tone_guardrails"])

    def test_historical_profile_matches_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "historical" / "profile.yaml",
            platform="fanqie",
            bucket="历史脑洞",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/historical/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "历史脑洞")
        self.assertIn("权谋", summary["strong_tags"])
        self.assertIn("家国", summary["strong_tags"])
        self.assertIn("历史感不能散", summary["tone_guardrails"])
        self.assertIn("权力线必须讲层级", summary["tone_guardrails"])

    def test_apocalypse_profile_matches_candidate_fields(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "apocalypse" / "profile.yaml",
            platform="fanqie",
            bucket="科幻末世",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/apocalypse/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "科幻末世")
        self.assertIn("末世", summary["strong_tags"])
        self.assertIn("生存", summary["strong_tags"])
        self.assertIn("危险感不能消失", summary["tone_guardrails"])
        self.assertIn("资源不能白给", summary["tone_guardrails"])

    def test_era_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "era" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/era/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "年代")
        self.assertIn("时代变迁", summary["strong_tags"])
        self.assertIn("奋斗成长", summary["strong_tags"])
        self.assertIn("时代细节不能失真", summary["tone_guardrails"])

    def test_farming_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "farming" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/farming/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "种田")
        self.assertIn("丰收致富", summary["strong_tags"])
        self.assertIn("温馨治愈", summary["strong_tags"])
        self.assertIn("发展速度要合理", summary["tone_guardrails"])

    def test_republic_romance_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "republic-romance" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/republic-romance/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "民国言情")
        self.assertIn("乱世情缘", summary["strong_tags"])
        self.assertIn("时代悲歌", summary["strong_tags"])
        self.assertIn("时代感不能悬浮", summary["tone_guardrails"])

    def test_ancient_romance_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "ancient-romance" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/ancient-romance/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "古言")
        self.assertIn("高门婚配", summary["strong_tags"])
        self.assertIn("权谋情感", summary["strong_tags"])
        self.assertIn("礼法关系不能悬浮", summary["tone_guardrails"])

    def test_fantasy_romance_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "fantasy-romance" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/fantasy-romance/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "幻想言情")
        self.assertIn("奇幻恋爱", summary["strong_tags"])
        self.assertIn("跨种族情缘", summary["strong_tags"])
        self.assertIn("奇幻设定必须服务情感主线", summary["tone_guardrails"])

    def test_war_spy_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "war-spy" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/war-spy/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "抗战谍战")
        self.assertIn("潜伏智斗", summary["strong_tags"])
        self.assertIn("家国信仰", summary["strong_tags"])
        self.assertIn("历史背景不能失真", summary["tone_guardrails"])

    def test_urban_life_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "urban-life" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/urban-life/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "都市日常")
        self.assertIn("温馨日常", summary["strong_tags"])
        self.assertIn("生活改善", summary["strong_tags"])
        self.assertIn("生活细节必须真实可感", summary["tone_guardrails"])

    def test_livestream_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "livestream" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/livestream/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "直播文")
        self.assertIn("粉丝增长", summary["strong_tags"])
        self.assertIn("打赏互动", summary["strong_tags"])
        self.assertIn("直播反馈必须及时可见", summary["tone_guardrails"])

    def test_game_sports_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "game-sports" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/game-sports/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "游戏体育")
        self.assertIn("竞技成长", summary["strong_tags"])
        self.assertIn("逆境翻盘", summary["strong_tags"])
        self.assertIn("比赛规则不能出硬伤", summary["tone_guardrails"])

    def test_mystery_brainhole_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "mystery-brainhole" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/mystery-brainhole/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "悬疑脑洞")
        self.assertIn("脑洞解谜", summary["strong_tags"])
        self.assertIn("惊喜反转", summary["strong_tags"])
        self.assertIn("创意设定要自洽", summary["tone_guardrails"])

    def test_mystery_creative_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "mystery-creative" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/mystery-creative/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "悬疑脑洞")
        self.assertIn("脑洞解谜", summary["strong_tags"])
        self.assertIn("规则反转", summary["strong_tags"])
        self.assertIn("反转必须有伏笔", summary["tone_guardrails"])

    def test_female_mystery_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "female-mystery" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/female-mystery/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "女频悬疑")
        self.assertIn("悬疑言情", summary["strong_tags"])
        self.assertIn("女性主体", summary["strong_tags"])
        self.assertIn("悬疑线与感情线要平衡", summary["tone_guardrails"])

    def test_supernatural_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "supernatural" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/supernatural/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "悬疑灵异")
        self.assertIn("诡异求生", summary["strong_tags"])
        self.assertIn("规则驱鬼", summary["strong_tags"])
        self.assertIn("鬼怪规则必须自洽", summary["tone_guardrails"])

    def test_rule_mystery_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "rule-mystery" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/rule-mystery/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "规则怪谈")
        self.assertIn("规则压迫", summary["strong_tags"])
        self.assertIn("漏洞求生", summary["strong_tags"])
        self.assertIn("规则设计必须有内在逻辑", summary["tone_guardrails"])

    def test_infinite_flow_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "infinite-flow" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/infinite-flow/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "无限流")
        self.assertIn("副本通关", summary["strong_tags"])
        self.assertIn("绝境翻盘", summary["strong_tags"])
        self.assertIn("副本规则必须自洽", summary["tone_guardrails"])

    def test_scifi_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "sci-fi" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/sci-fi/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "科幻")
        self.assertIn("科技突破", summary["strong_tags"])
        self.assertIn("文明碰撞", summary["strong_tags"])
        self.assertIn("科技设定必须自洽", summary["tone_guardrails"])

    def test_gaowu_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "gaowu" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/gaowu/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "高武")
        self.assertIn("越级挑战", summary["strong_tags"])
        self.assertIn("武道成长", summary["strong_tags"])
        self.assertIn("突破必须有积累", summary["tone_guardrails"])

    def test_western_fantasy_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "western-fantasy" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/western-fantasy/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "西幻")
        self.assertIn("魔法冒险", summary["strong_tags"])
        self.assertIn("领地成长", summary["strong_tags"])
        self.assertIn("魔法规则必须有代价", summary["tone_guardrails"])

    def test_urban_creative_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "urban-creative" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/urban-creative/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "都市脑洞")
        self.assertIn("设定反转", summary["strong_tags"])
        self.assertIn("能力展开", summary["strong_tags"])
        self.assertIn("设定不能只靠解释成立", summary["tone_guardrails"])

    def test_modern_brainhole_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "modern-brainhole" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/modern-brainhole/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "现言脑洞")
        self.assertIn("创意恋爱", summary["strong_tags"])
        self.assertIn("命运改写", summary["strong_tags"])
        self.assertIn("创意设定必须服务情感推进", summary["tone_guardrails"])

    def test_historical_creative_profile_exposes_minimum_positioning(self) -> None:
        module = load_module()
        raw = module.load_profile_with_overlays(
            PROFILE_ROOT / "historical-creative" / "profile.yaml",
            platform="fanqie",
        )
        normalized = module.normalize_profile(
            raw,
            source_path="shared/profiles/historical-creative/profile.yaml",
        )
        summary = module.summarize_for_state(normalized, raw_profile=raw, platform="fanqie")

        self.assertEqual(summary["bucket"], "历史脑洞")
        self.assertIn("历史改写", summary["strong_tags"])
        self.assertIn("现代知识入局", summary["strong_tags"])
        self.assertIn("历史改写必须保留时代逻辑", summary["tone_guardrails"])


if __name__ == "__main__":
    unittest.main()
