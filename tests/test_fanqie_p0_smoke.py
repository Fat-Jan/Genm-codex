from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "fanqie_p0_smoke.py"


def load_module():
    spec = importlib.util.spec_from_file_location("fanqie_p0_smoke", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FanqieP0SmokeCliTests(unittest.TestCase):
    def test_parse_args_defaults_to_draft(self) -> None:
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

    def test_parse_args_accepts_explicit_modes(self) -> None:
        module = load_module()

        for mode in ("scaffold", "draft", "writeback"):
            with self.subTest(mode=mode):
                args = module.parse_args(
                    [
                        "--project-root",
                        "/tmp/project",
                        "--chapter",
                        "003",
                        "--chapters",
                        "001-003",
                        "--mode",
                        mode,
                    ]
                )
                self.assertEqual(args.mode, mode)

    def test_infer_bucket_prefers_genre_profile_bucket(self) -> None:
        module = load_module()

        state = {
            "meta": {"genre": "都市脑洞"},
            "genre_profile": {"bucket": "宫斗宅斗"},
        }

        self.assertEqual(module.infer_bucket(state), "宫斗宅斗")

    def test_infer_bucket_falls_back_to_meta_genre(self) -> None:
        module = load_module()

        state = {
            "meta": {"genre": "宫斗宅斗"},
            "genre_profile": {},
        }

        self.assertEqual(module.infer_bucket(state), "宫斗宅斗")

    def test_infer_bucket_returns_none_for_unsupported_bucket(self) -> None:
        module = load_module()

        state = {
            "meta": {"genre": "传统玄幻"},
            "genre_profile": {},
        }

        self.assertIsNone(module.infer_bucket(state))

    def test_infer_bucket_maps_xianyan_tianchong_to_qingchun_tianchong(self) -> None:
        module = load_module()

        state = {
            "meta": {"genre": "言情"},
            "genre_profile": {"bucket": "现言甜宠"},
        }

        self.assertEqual(module.infer_bucket(state), "青春甜宠")

    def test_writeback_is_not_allowed_without_explicit_flag(self) -> None:
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


class FanqieP0SmokeHelperTests(unittest.TestCase):
    def test_load_state_reads_project_state(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            payload = {"meta": {"title": "Demo", "genre": "宫斗宅斗"}}
            (mighty / "state.json").write_text(json.dumps(payload, ensure_ascii=False))

            state = module.load_state(project_root)

            self.assertEqual(state["meta"]["title"], "Demo")

    def test_normalize_chapter_key_zero_pads_numeric_strings(self) -> None:
        module = load_module()

        self.assertEqual(module.normalize_chapter_key("3"), "003")
        self.assertEqual(module.normalize_chapter_key("003"), "003")

    def test_slugify_project_title_keeps_readable_slug(self) -> None:
        module = load_module()

        slug = module.slugify_project_title("继母换我婚书那夜，太子先开了口")

        self.assertEqual(slug, "继母换我婚书那夜-太子先开了口")

    def test_default_output_path_writes_into_framework_docs(self) -> None:
        module = load_module()

        path = module.default_output_path(
            project_root=REPO_ROOT / "projects/庶女谋略",
            title="庶女谋略",
            date_str="2026-03-23",
        )

        self.assertEqual(
            path,
            REPO_ROOT
            / "docs/opening-and-plot-framework/real-project-smoke-庶女谋略-fanqie-p0-2026-03-23.md",
        )


class FanqieP0SmokeScaffoldTests(unittest.TestCase):
    def test_scaffold_mode_writes_markdown_skeleton(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(
                json.dumps(
                    {
                        "meta": {"title": "测试项目", "genre": "宫斗宅斗", "platform": "番茄"},
                        "genre_profile": {"bucket": "宫斗宅斗"},
                    },
                    ensure_ascii=False,
                )
            )
            output_path = Path(tmpdir) / "smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapter="003",
                chapters="001-003",
                mode="scaffold",
                output_path=output_path,
                date_str="2026-03-23",
            )

            self.assertEqual(result["effective_mode"], "scaffold")
            self.assertTrue(output_path.exists())
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("项目：`", content)
            self.assertIn("bucket：`宫斗宅斗`", content)
            self.assertIn("## 手工 `novel-review` 样本", content)
            self.assertIn("## 手工 `novel-precheck` 样本", content)
            self.assertIn("## 结论", content)

    def test_scaffold_mode_for_unsupported_bucket_includes_degrade_note(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(
                json.dumps(
                    {
                        "meta": {"title": "Demo", "genre": "传统玄幻", "platform": "番茄"},
                        "genre_profile": {},
                    },
                    ensure_ascii=False,
                )
            )
            output_path = Path(tmpdir) / "smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapter="003",
                chapters="001-003",
                mode="scaffold",
                output_path=output_path,
                date_str="2026-03-23",
            )

            self.assertEqual(result["effective_mode"], "scaffold")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("scaffold-only", content)


class FanqieP0SmokeDraftTests(unittest.TestCase):
    def test_draft_mode_generates_non_empty_bucket_summaries_for_real_project(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "draft-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/庶女谋略",
                chapter="003",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-23",
            )

            self.assertEqual(result["effective_mode"], "draft")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("draft", content)
            self.assertIn("需人工确认", content)
            self.assertIn("fanqie_bucket_review_summary:", content)
            self.assertIn("fanqie_bucket_precheck_summary:", content)
            self.assertIn("bucket: 宫斗宅斗", content)
            self.assertIn("projects/庶女谋略/chapters/第003章.md", content)
            self.assertIn("projects/庶女谋略/chapters/第001章.md", content)

    def test_draft_mode_degrades_to_scaffold_when_evidence_is_insufficient(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(
                json.dumps(
                    {
                        "meta": {"title": "Demo", "genre": "宫斗宅斗", "platform": "番茄"},
                        "genre_profile": {"bucket": "宫斗宅斗"},
                    },
                    ensure_ascii=False,
                )
            )
            output_path = Path(tmpdir) / "draft-smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapter="003",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-23",
            )

            self.assertEqual(result["effective_mode"], "scaffold")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("证据不足", content)
            self.assertIn("scaffold-only", content)

    def test_draft_mode_adds_confidence_evidence_and_writeback_preview(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "draft-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/庶女谋略",
                chapter="003",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["confidence"], "high")
            self.assertGreaterEqual(result["evidence_count"], 4)
            self.assertIn("market_adjustments", result["signals_used"])
            self.assertIn("learned_patterns", result["signals_used"])
            self.assertIn("writeback_preview", result)

            content = output_path.read_text(encoding="utf-8")
            self.assertIn("confidence: high", content)
            self.assertIn("evidence_count:", content)
            self.assertIn("evidence_sources:", content)
            self.assertIn("writeback_preview:", content)

    def test_non_palace_p0_bucket_gets_conservative_draft_not_fake_strong_judgment(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            chapters_dir = project_root / "chapters"
            mighty.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            (mighty / "state.json").write_text(
                json.dumps(
                    {
                        "meta": {"title": "甜宠样本", "genre": "青春甜宠", "platform": "番茄"},
                        "genre_profile": {"bucket": "青春甜宠"},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            for key in ("001", "002", "003"):
                (chapters_dir / f"第{key}章.md").write_text("校园心动与互动升级。" * 80, encoding="utf-8")
            output_path = Path(tmpdir) / "draft-smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapter="003",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["confidence"], "low")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("bucket: 青春甜宠", content)
            self.assertIn("bucket_grade: draft", content)

    def test_xianyan_tianchong_alias_sample_generates_qingchun_tianchong_draft(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "draft-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "smoke/e2e-tianchong-evil",
                chapter="003",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "青春甜宠")
            self.assertEqual(result["confidence"], "low")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("bucket：`青春甜宠`", content)
            self.assertIn("bucket_grade: draft", content)

    def test_load_sidecars_reads_market_and_learned_patterns(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "market-adjustments.json").write_text(
                json.dumps({"version": "1", "data": {"adjustments": [{"id": "scan-surface-hook"}]}}, ensure_ascii=False),
                encoding="utf-8",
            )
            (mighty / "learned-patterns.json").write_text(
                json.dumps({"version": "1", "data": {"avoid_patterns": ["背景先行"]}}, ensure_ascii=False),
                encoding="utf-8",
            )

            sidecars = module.load_sidecars(project_root)

            self.assertIn("market_adjustments", sidecars)
            self.assertIn("learned_patterns", sidecars)
            self.assertEqual(sidecars["market_adjustments"]["data"]["adjustments"][0]["id"], "scan-surface-hook")
            self.assertEqual(sidecars["learned_patterns"]["data"]["avoid_patterns"][0], "背景先行")


class FanqieP0SmokeWritebackTests(unittest.TestCase):
    def make_project(self, tmpdir: str) -> Path:
        project_root = Path(tmpdir) / "project"
        mighty = project_root / ".mighty"
        chapters_dir = project_root / "chapters"
        mighty.mkdir(parents=True)
        chapters_dir.mkdir(parents=True)
        state = {
            "meta": {"title": "Demo", "genre": "宫斗宅斗", "platform": "番茄", "updated_at": "2026-03-23T00:00:00Z"},
            "genre_profile": {"bucket": "宫斗宅斗"},
            "chapter_meta": {
                "003": {
                    "review_score": 88,
                    "review_grade": "A",
                    "recommended_next_action": "novel-write",
                }
            },
        }
        (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        body = "婚书局压迫与反击。东宫点名回话，礼法与账本一起上桌。" * 40
        for key in ("001", "002", "003"):
            (chapters_dir / f"第{key}章.md").write_text(body, encoding="utf-8")
        return project_root

    def test_writeback_mode_requires_explicit_confirmation_flag(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = self.make_project(tmpdir)
            with self.assertRaises(ValueError):
                module.run_smoke(
                    project_root=project_root,
                    chapter="003",
                    chapters="001-003",
                    mode="writeback",
                    writeback=False,
                    output_path=Path(tmpdir) / "writeback-smoke.md",
                )

    def test_writeback_only_writes_bucket_fields_and_preserves_review_fields(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = self.make_project(tmpdir)
            result = module.run_smoke(
                project_root=project_root,
                chapter="003",
                chapters="001-003",
                mode="writeback",
                writeback=True,
                output_path=Path(tmpdir) / "writeback-smoke.md",
            )

            self.assertEqual(result["effective_mode"], "writeback")
            state = json.loads((project_root / ".mighty/state.json").read_text(encoding="utf-8"))
            chapter = state["chapter_meta"]["003"]
            self.assertEqual(chapter["review_score"], 88)
            self.assertEqual(chapter["review_grade"], "A")
            self.assertEqual(chapter["recommended_next_action"], "novel-write")
            self.assertIn("fanqie_bucket_flags", chapter)
            self.assertIn("fanqie_bucket_summary", chapter)
            self.assertEqual(chapter["fanqie_bucket_summary"]["bucket"], "宫斗宅斗")

    def test_writeback_conflicts_when_bucket_summary_already_exists(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = self.make_project(tmpdir)
            state_path = project_root / ".mighty/state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["chapter_meta"]["003"]["fanqie_bucket_summary"] = {"bucket": "宫斗宅斗", "bucket_grade": "warn"}
            state["chapter_meta"]["003"]["fanqie_bucket_flags"] = ["old-flag"]
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

            result = module.run_smoke(
                project_root=project_root,
                chapter="003",
                chapters="001-003",
                mode="writeback",
                writeback=True,
                output_path=Path(tmpdir) / "writeback-smoke.md",
            )

            self.assertEqual(result["writeback_status"], "conflict")
            updated = json.loads(state_path.read_text(encoding="utf-8"))
            chapter = updated["chapter_meta"]["003"]
            self.assertEqual(chapter["fanqie_bucket_summary"]["bucket_grade"], "warn")
            self.assertEqual(chapter["fanqie_bucket_flags"], ["old-flag"])


if __name__ == "__main__":
    unittest.main()
