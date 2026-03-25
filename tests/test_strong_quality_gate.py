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

import strong_quality_gate  # noqa: E402


BATCH_GATE_MODULE_PATH = REPO_ROOT / "scripts" / "check-batch-quality-gate.py"
SYNC_SCRIPT_PATH = REPO_ROOT / "scripts" / "sync-setting-assets.py"


def load_batch_gate_module():
    spec = importlib.util.spec_from_file_location("check_batch_quality_gate", BATCH_GATE_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {BATCH_GATE_MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class StrongQualityGatePolicyTests(unittest.TestCase):
    REPO_ROOT = REPO_ROOT
    POLICY_PATH = REPO_ROOT / "docs/strong-quality-gate-policy.json"

    def load_policy(self):
        with self.POLICY_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)

    def test_policy_file_loads(self):
        self.assertTrue(self.POLICY_PATH.exists(), "strong-quality-gate-policy.json is missing")
        policy = self.load_policy()
        self.assertIsInstance(policy, dict)

    def test_metadata_values(self):
        policy = self.load_policy()
        self.assertEqual(policy.get("version"), "1.0")
        self.assertEqual(policy.get("policy_name"), "strong-quality-gate-policy")
        self.assertEqual(policy.get("source_type"), "strong-quality-gate-v1")

    def test_bucket_thresholds_present(self):
        policy = self.load_policy()
        defaults = policy.get("defaults")
        self.assertIsNotNone(defaults)
        for bucket_name in ("longform", "shortform"):
            track = defaults.get(bucket_name)
            self.assertIsNotNone(track, f"{bucket_name} defaults are missing")
            for key in ("hard_min_chars", "soft_min_chars", "preferred_min_chars", "preferred_max_chars"):
                self.assertIn(key, track, f"{bucket_name}.{key} missing")
        buckets = policy.get("buckets")
        self.assertIsInstance(buckets, dict)
        self.assertGreater(len(buckets), 0)
        for bucket_name, bucket in buckets.items():
            self.assertIsNotNone(bucket)
            self.assertIn("track", bucket, f"{bucket_name}.track missing")
            for key in ("hard_min_chars", "soft_min_chars", "preferred_min_chars", "preferred_max_chars"):
                self.assertIn(key, bucket, f"{bucket_name}.{key} missing")

    def test_truth_source_mapping_present(self):
        policy = self.load_policy()
        pre_write = policy.get("pre_write_gate", {})
        truth_sources = pre_write.get("truth_sources")
        self.assertIsNotNone(truth_sources)
        for key in ("kinship_truth", "office_truth", "world_rule_support"):
            self.assertIn(key, truth_sources)
            self.assertTrue(truth_sources[key], f"{key} list must not be empty")

    def test_sync_rejection_patterns_accessible(self):
        policy = self.load_policy()
        sync_gate = policy.get("sync_gate", {})
        characters = sync_gate.get("characters")
        self.assertIsNotNone(characters)
        for key in (
            "min_confidence_mentions",
            "max_person_name_chars",
            "reject_if_contains",
            "reject_exact_names",
            "reject_fullmatch_patterns",
            "reject_role_suffixes",
            "garment_or_object_hints",
            "reject_suffixes",
            "phrase_fragment_reject_min_occurrences",
            "repetitive_noise_reject_min_occurrences",
            "min_phrase_fragment_chars",
        ):
            self.assertIn(key, characters)
        self.assertTrue(characters.get("reject_suffixes"))
        self.assertTrue(characters.get("reject_fullmatch_patterns"))
        self.assertTrue(characters.get("reject_role_suffixes"))

    def test_post_write_gate_sections_present(self):
        policy = self.load_policy()
        post_write = policy.get("post_write_gate", {})
        shrinkage = post_write.get("shrinkage")
        self.assertIsNotNone(shrinkage)
        self.assertIsInstance(shrinkage, dict)
        malformed = post_write.get("malformed_text")
        self.assertIsNotNone(malformed)
        self.assertIsInstance(malformed, dict)

    def test_post_write_lint_sections_present(self):
        policy = self.load_policy()
        post_write_lint = policy.get("post_write_lint", {})
        self.assertIsInstance(post_write_lint, dict)
        for key in ("ai_turn_markers", "explanation_first_patterns", "collective_shock_patterns", "long_paragraphs"):
            self.assertIn(key, post_write_lint)

    def test_defaults_and_shrinkage_values(self):
        policy = self.load_policy()
        defaults = policy.get("defaults", {})
        longform = defaults.get("longform", {})
        self.assertEqual(longform.get("hard_min_chars"), 2000)
        post_write = policy.get("post_write_gate", {})
        shrinkage = post_write.get("shrinkage", {})
        self.assertEqual(shrinkage.get("baseline_drop_ratio"), 0.55)


class StrongQualityGateHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = strong_quality_gate.load_policy()

    def test_load_policy_returns_mapping(self):
        policy = strong_quality_gate.load_policy()
        self.assertIsInstance(policy, dict)
        self.assertEqual(policy.get("policy_name"), "strong-quality-gate-policy")

    def test_resolve_length_policy_prefers_bucket(self):
        state = {"genre_profile": {"bucket": "宫斗宅斗"}}
        resolved = strong_quality_gate.resolve_length_policy(state, self.policy)
        bucket = self.policy["buckets"]["宫斗宅斗"]
        self.assertEqual(resolved["bucket_name"], "宫斗宅斗")
        self.assertEqual(resolved["hard_min_chars"], bucket["hard_min_chars"])
        self.assertEqual(resolved["soft_min_chars"], bucket["soft_min_chars"])

    def test_resolve_length_policy_falls_back_to_shortform_track(self):
        state = {"meta": {"target_chapters": 8}}
        resolved = strong_quality_gate.resolve_length_policy(state, self.policy)
        self.assertEqual(resolved["track"], "shortform")
        self.assertEqual(resolved["bucket_name"], "__default__")
        self.assertEqual(resolved["hard_min_chars"], self.policy["defaults"]["shortform"]["hard_min_chars"])

    def test_detect_missing_truth_sources_returns_missing(self):
        outline = "这是家族宅门相关的章纲"
        route = {"truth_sources": ["kinship_truth", "world_rule_support"]}
        available = ["设定集/家族/宅门真值表.md"]
        result = strong_quality_gate.detect_missing_truth_sources(outline, route, available, self.policy)
        missing_keys = {item["key"] for item in result["missing"]}
        self.assertIn("world_rule_support", missing_keys)
        self.assertNotIn("kinship_truth", missing_keys)

    def test_evaluate_post_write_gate_hard_min_blocks(self):
        state = {"meta": {"target_chapters": 12}}
        result = strong_quality_gate.evaluate_post_write_gate(
            state=state,
            chapter_text="短",
            baseline_avg_chars=None,
            policy=self.policy,
            chapter_number=1,
        )
        self.assertEqual(result["status"], "block")
        self.assertTrue(any(issue["code"] == "chapter-too-short" for issue in result["issues"]))
        self.assertCountEqual(
            result.keys(),
            {
                "status",
                "issues",
                "warnings",
                "length_policy",
                "baseline_avg_chars",
                "metrics",
                "matched_checks",
            },
        )

    def test_evaluate_post_write_gate_soft_min_warns_without_block(self):
        state = {"meta": {"target_chapters": 12}}
        parts = [f"第{i}节推进，因果线索延展，人物动机{i}清晰。" for i in range(1, 120)]
        text = "".join(parts)
        if len(text) > 2300:
            text = text[:2300]
        if len(text) < 2100:
            text = text + ("补充细节" * 80)
        self.assertGreaterEqual(len(text), 2000)
        self.assertLess(len(text), 2400)
        result = strong_quality_gate.evaluate_post_write_gate(
            state=state,
            chapter_text=text,
            baseline_avg_chars=None,
            policy=self.policy,
            chapter_number=2,
        )
        self.assertEqual(result["status"], "pass")
        self.assertTrue(any(warn["code"] == "chapter-below-soft-floor" for warn in result["warnings"]))
        self.assertFalse(any(issue["code"].startswith("malformed") for issue in result["issues"]))
        self.assertNotIn("malformed-repeated-fragment", result["matched_checks"])

    def test_evaluate_post_write_gate_shrinkage_blocks_and_marks_check(self):
        state = {"meta": {"target_chapters": 12}}
        text = "a" * 2100
        result = strong_quality_gate.evaluate_post_write_gate(
            state=state,
            chapter_text=text,
            baseline_avg_chars=4000,
            policy=self.policy,
            chapter_number=3,
        )
        self.assertEqual(result["status"], "block")
        self.assertIn("shrinkage-baseline-drop", result["matched_checks"])

    def test_evaluate_post_write_gate_malformed_block_marks_check(self):
        state = {"meta": {"target_chapters": 12}}
        text = ("foo " * 3) + ("a" * 2100)
        result = strong_quality_gate.evaluate_post_write_gate(
            state=state,
            chapter_text=text,
            baseline_avg_chars=None,
            policy=self.policy,
            chapter_number=4,
        )
        self.assertEqual(result["status"], "block")
        self.assertIn("malformed-repeated-exact-token", result["matched_checks"])

    def test_classify_sync_candidate_rejects_phrase_fragment(self):
        candidate = strong_quality_gate.classify_sync_candidate(
            name="花厅",
            occurrences=3,
            policy=self.policy,
            phrase_fragment_hits=2,
            repetitive_noise_hits=0,
        )
        self.assertFalse(candidate["accepted"])
        self.assertIn("phrase-fragment", candidate["reasons"])

    def test_classify_sync_candidate_rejects_repetitive_noise(self):
        candidate = strong_quality_gate.classify_sync_candidate(
            name="顾承州",
            occurrences=3,
            policy=self.policy,
            phrase_fragment_hits=0,
            repetitive_noise_hits=2,
        )
        self.assertFalse(candidate["accepted"])
        self.assertIn("repetitive-noise", candidate["reasons"])

    def test_classify_sync_candidate_rejects_garment_or_object_hint(self):
        candidate = strong_quality_gate.classify_sync_candidate(
            name="账簿",
            occurrences=3,
            policy=self.policy,
            phrase_fragment_hits=0,
            repetitive_noise_hits=0,
        )
        self.assertFalse(candidate["accepted"])
        self.assertIn("garment-or-object-hint", candidate["reasons"])

    def test_classify_sync_candidate_rejects_noise_token(self):
        candidate = strong_quality_gate.classify_sync_candidate(
            name="席次",
            occurrences=3,
            policy=self.policy,
            phrase_fragment_hits=0,
            repetitive_noise_hits=0,
        )
        self.assertFalse(candidate["accepted"])
        self.assertIn("contains-rejected-token", candidate["reasons"])

    def test_classify_sync_candidate_rejects_school_grade_token(self):
        candidate = strong_quality_gate.classify_sync_candidate(
            name="高二",
            occurrences=3,
            policy=self.policy,
            phrase_fragment_hits=0,
            repetitive_noise_hits=0,
        )
        self.assertFalse(candidate["accepted"])
        self.assertIn("school-grade-token", candidate["reasons"])

    def test_classify_sync_candidate_rejects_role_title_token(self):
        candidate = strong_quality_gate.classify_sync_candidate(
            name="许执事",
            occurrences=3,
            policy=self.policy,
            phrase_fragment_hits=0,
            repetitive_noise_hits=0,
        )
        self.assertFalse(candidate["accepted"])
        self.assertIn("role-title-token", candidate["reasons"])

    def test_classify_sync_candidate_accepts_clean_name(self):
        candidate = strong_quality_gate.classify_sync_candidate(
            name="周全",
            occurrences=3,
            policy=self.policy,
            phrase_fragment_hits=0,
            repetitive_noise_hits=0,
        )
        self.assertTrue(candidate["accepted"])
        self.assertEqual(candidate["reasons"], [])


class BatchQualityGateIntegrationTests(unittest.TestCase):
    def run_gate(self, project_root: Path, *args: str) -> dict:
        cmd = [sys.executable, str(BATCH_GATE_MODULE_PATH), str(project_root), *args]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(proc.stdout)

    def create_project(
        self,
        chapters: dict[int, str],
        *,
        current_chapter: int,
        target_chapters: int = 12,
        bucket: str | None = None,
    ) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        project_root = Path(tmpdir.name) / "project"
        mighty = project_root / ".mighty"
        chapters_dir = project_root / "chapters"
        mighty.mkdir(parents=True)
        chapters_dir.mkdir(parents=True)
        state = {
            "meta": {"target_chapters": target_chapters},
            "progress": {"current_chapter": current_chapter},
            "chapter_meta": {str(num): {} for num in chapters},
        }
        if bucket:
            state["genre_profile"] = {"bucket": bucket}
        (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        for num, text in chapters.items():
            (chapters_dir / f"第{num:03d}章.md").write_text(text, encoding="utf-8")
        return project_root

    def test_batch_gate_blocks_hard_min_short_chapter(self):
        project_root = self.create_project({1: "短"}, current_chapter=1)
        result = self.run_gate(project_root, "--last-n", "1")
        self.assertEqual(result["status"], "fail")
        self.assertTrue(any(item["code"] == "chapter-too-short" for item in result["issues"]))

    def test_batch_gate_blocks_sharp_length_drop(self):
        chapters = {
            1: "甲" * 4000,
            2: "乙" * 4000,
            3: "丙" * 4000,
            4: "丁" * 2100,
        }
        project_root = self.create_project(chapters, current_chapter=4)
        result = self.run_gate(project_root, "--last-n", "1")
        self.assertEqual(result["status"], "fail")
        self.assertTrue(any(item["code"] == "sharp-length-drop" for item in result["issues"]))

    def test_batch_gate_warns_but_passes_valid_shorter_chapter(self):
        base = "".join(f"第{i}节推进，因果线索延展，人物动机{i}清晰。" for i in range(1, 120))
        valid_shorter = base[:2200]
        chapters = {
            1: "甲" * 2800,
            2: "乙" * 2800,
            3: "丙" * 2800,
            4: valid_shorter,
        }
        project_root = self.create_project(chapters, current_chapter=4)
        result = self.run_gate(project_root, "--last-n", "1")
        self.assertEqual(result["status"], "warn")
        self.assertFalse(any(item["code"].startswith("malformed") for item in result["issues"]))
        self.assertTrue(any(item["code"] == "chapter-below-soft-floor" for item in result["warnings"]))

    def test_batch_gate_blocks_malformed_repeated_token(self):
        malformed = ("foo " * 3) + ("甲" * 2100)
        project_root = self.create_project({1: malformed}, current_chapter=1)
        result = self.run_gate(project_root, "--last-n", "1")
        self.assertEqual(result["status"], "fail")
        self.assertTrue(any(item["code"] == "malformed-repeated-token" for item in result["issues"]))


class SyncSettingAssetsIntegrationTests(unittest.TestCase):
    def run_sync(self, project_root: Path, *args: str) -> dict:
        cmd = [sys.executable, str(SYNC_SCRIPT_PATH), str(project_root), *args]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(proc.stdout)

    def create_project(
        self,
        chapters: dict[int, str],
        *,
        current_chapter: int,
        overrides: dict | None = None,
    ) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        project_root = Path(tmpdir.name) / "project"
        mighty = project_root / ".mighty"
        chapters_dir = project_root / "chapters"
        role_dir = project_root / "设定集" / "角色"
        mighty.mkdir(parents=True)
        chapters_dir.mkdir(parents=True)
        role_dir.mkdir(parents=True)
        state = {
            "meta": {"target_chapters": 12},
            "progress": {"current_chapter": current_chapter},
            "chapter_meta": {str(num): {} for num in chapters},
            "entities": {
                "characters": {
                    "protagonist": {
                        "name": "苏照棠",
                        "location": {"current": "西院"},
                        "status": ["清醒"],
                        "current_goals": ["自保"],
                    }
                },
                "locations": {"important": [], "current": None},
                "items": {"tracked": [], "protagonist_inventory": []},
            },
        }
        (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        if overrides is not None:
            (mighty / "sync-overrides.json").write_text(json.dumps(overrides, ensure_ascii=False), encoding="utf-8")
        for num, text in chapters.items():
            (chapters_dir / f"第{num:03d}章.md").write_text(text, encoding="utf-8")
        (role_dir / "主角.md").write_text("# 主角\n", encoding="utf-8")
        return project_root

    def test_sync_rejects_phrase_fragment_to_review_queue(self):
        chapter = "花厅里。花厅里。花厅里。苏照棠看见花厅里人影晃动。"
        project_root = self.create_project({1: chapter}, current_chapter=1)
        result = self.run_sync(project_root, "--mode", "characters", "--recent-chapters", "1")
        queue = json.loads(Path(result["review_queue"]).read_text(encoding="utf-8"))
        queued_names = {item["name"] for item in queue["ambiguous_entities"]}
        self.assertIn("花厅里", queued_names)
        self.assertFalse((project_root / "设定集" / "角色" / "花厅里.md").exists())

    def test_sync_rejects_garment_or_object_name_to_review_queue(self):
        chapter = "白褙子。白褙子。白褙子。苏照棠盯着那件白褙子没有说话。"
        project_root = self.create_project({1: chapter}, current_chapter=1)
        result = self.run_sync(project_root, "--mode", "characters", "--recent-chapters", "1")
        queue = json.loads(Path(result["review_queue"]).read_text(encoding="utf-8"))
        queued_names = {item["name"] for item in queue["ambiguous_entities"]}
        self.assertIn("白褙子", queued_names)
        self.assertFalse((project_root / "设定集" / "角色" / "白褙子.md").exists())

    def test_sync_rejects_school_grade_token_to_review_queue(self):
        chapter = "高二（七）班门口。高二（七）班门口。高二（七）班门口。苏照棠站在高二（七）班门口深呼吸。"
        project_root = self.create_project({1: chapter}, current_chapter=1)
        result = self.run_sync(project_root, "--mode", "characters", "--recent-chapters", "1")
        queue = json.loads(Path(result["review_queue"]).read_text(encoding="utf-8"))
        queued_names = {item["name"] for item in queue["ambiguous_entities"]}
        self.assertIn("高二", queued_names)
        self.assertFalse((project_root / "设定集" / "角色" / "高二.md").exists())

    def test_sync_rejects_role_title_token_to_review_queue(self):
        chapter = "“许执事！”“许执事！”“许执事！”“陆师兄！”“陆师兄！”“陆师兄！”"
        project_root = self.create_project({1: chapter}, current_chapter=1)
        result = self.run_sync(project_root, "--mode", "characters", "--recent-chapters", "1")
        queue = json.loads(Path(result["review_queue"]).read_text(encoding="utf-8"))
        queued_names = {item["name"] for item in queue["ambiguous_entities"]}
        self.assertIn("许执事", queued_names)
        self.assertIn("陆师兄", queued_names)
        self.assertFalse((project_root / "设定集" / "角色" / "许执事.md").exists())
        self.assertFalse((project_root / "设定集" / "角色" / "陆师兄.md").exists())

    def test_sync_overrides_can_ignore_candidate(self):
        chapter = "花厅里花厅里花厅里。"
        overrides = {
            "version": "1.0",
            "updated_at": "",
            "aliases": {"characters": {}, "locations": {}, "factions": {}, "items": {}},
            "ignored": {"characters": ["花厅里"], "locations": [], "factions": [], "items": []},
        }
        project_root = self.create_project({1: chapter}, current_chapter=1, overrides=overrides)
        result = self.run_sync(project_root, "--mode", "characters", "--recent-chapters", "1")
        queue = json.loads(Path(result["review_queue"]).read_text(encoding="utf-8"))
        queued_names = {item["name"] for item in queue["ambiguous_entities"]}
        self.assertNotIn("花厅里", queued_names)
        self.assertFalse((project_root / "设定集" / "角色" / "花厅里.md").exists())

    def test_sync_materializes_repeated_valid_name(self):
        chapter = "周全。周全。周全。苏照棠知道周全还会再来。"
        project_root = self.create_project({1: chapter}, current_chapter=1)
        self.run_sync(project_root, "--mode", "characters", "--recent-chapters", "1")
        self.assertTrue((project_root / "设定集" / "角色" / "周全.md").exists())
