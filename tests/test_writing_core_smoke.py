from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "writing_core_smoke.py"


def load_module():
    spec = importlib.util.spec_from_file_location("writing_core_smoke", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class WritingCoreSmokeCliTests(unittest.TestCase):
    def test_parse_args_defaults_to_draft(self) -> None:
        module = load_module()

        args = module.parse_args(
            [
                "--project-root",
                "/tmp/project",
                "--chapters",
                "001-003",
            ]
        )

        self.assertEqual(args.mode, "draft")
        self.assertFalse(args.writeback)
        self.assertFalse(args.save_packaging)

    def test_parse_args_accepts_writeback_and_save_packaging(self) -> None:
        module = load_module()

        args = module.parse_args(
            [
                "--project-root",
                "/tmp/project",
                "--chapters",
                "001-003",
                "--mode",
                "writeback",
                "--writeback",
                "--save-packaging",
            ]
        )

        self.assertEqual(args.mode, "writeback")
        self.assertTrue(args.writeback)
        self.assertTrue(args.save_packaging)


class WritingCoreSmokeDraftTests(unittest.TestCase):
    def test_draft_mode_generates_expected_sections_for_real_project(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/宗门垫底那年，我把废丹卖成了天价",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "玄幻脑洞")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("packaging_judgment:", content)
            self.assertIn("投稿建议:", content)
            self.assertIn("content_standard_summary:", content)
            self.assertIn("writeback_preview:", content)

    def test_draft_mode_can_infer_realistic_bucket_for_second_sample(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/离婚冷静期那天，前夫把董事会席位押给了我",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "豪门总裁")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("离婚当天", content)
            self.assertIn("packaging-needs-update:", content)

    def test_draft_mode_for_city_daily_project_generates_cleaner_packaging_language(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/搬回老小区后，我靠蹭饭认识了整栋楼",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "都市日常")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("老小区", content)
            self.assertIn("换饭", content)
            self.assertNotIn("### 推荐简介\n\n#", content)
            self.assertNotIn("# 总纲", content)
            self.assertNotIn("## 一句话卖点被", content)

    def test_draft_mode_for_historical_project_uses_bucket_specific_packaging_language(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/我在县衙当杂吏，靠翻旧案升了堂",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "历史脑洞")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("卷宗回响", content)
            self.assertIn("旧案", content)
            self.assertIn("制度压力和翻案脑洞", content)

    def test_draft_mode_for_palace_project_uses_bucket_specific_packaging_language(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/庶妹换我婚书那夜，太子先开了口",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "宫斗宅斗")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("继母压制", content)
            self.assertIn("婚书被换", content)
            self.assertIn("东宫", content)

    def test_draft_mode_for_work_romance_project_uses_bucket_specific_packaging_language(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/她升职那天，前上司成了我合租室友",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "职场婚恋")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("升职接锅", content)
            self.assertIn("合租揭面", content)
            self.assertIn("试运行窗口", content)
            self.assertNotIn("书名:", content)

    def test_draft_mode_for_youth_romance_project_uses_bucket_specific_packaging_language(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/转学第一天，我把校草认成了新来的代课老师",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "青春甜宠")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("转学第一天", content)
            self.assertIn("身份错认", content)
            self.assertIn("学习互助", content)

    def test_draft_mode_for_urban_brainhole_project_uses_bucket_specific_packaging_language(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=REPO_ROOT / "projects/我赔光积蓄那天，系统先把违约金打到了账上",
                chapters="001-003",
                mode="draft",
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "draft")
            self.assertEqual(result["bucket"], "都市脑洞")
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("赔光积蓄", content)
            self.assertIn("系统先把违约金打到了账上", content)
            self.assertIn("到账", content)


class WritingCoreSmokeWritebackTests(unittest.TestCase):
    def test_writeback_mode_requires_confirmation(self) -> None:
        module = load_module()

        with self.assertRaises(ValueError):
            module.run_smoke(
                project_root=REPO_ROOT / "projects/宗门垫底那年，我把废丹卖成了天价",
                chapters="001-003",
                mode="writeback",
                writeback=False,
                save_packaging=False,
                output_path=REPO_ROOT / "tmp-smoke.md",
                date_str="2026-03-24",
            )

    def test_writeback_mode_can_update_temp_project_and_save_packaging(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            chapters_dir = project_root / "chapters"
            outline_dir = project_root / "大纲"
            mighty.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            outline_dir.mkdir(parents=True)

            state = {
                "meta": {
                    "title": "测试离婚项目",
                    "genre": "豪门总裁",
                    "platform": "番茄",
                    "updated_at": "2026-03-24T00:00:00Z",
                },
                "genre_profile": {"bucket": "豪门总裁"},
                "chapter_meta": {"003": {}},
            }
            learned = {
                "writing_style_preferences": {
                    "dialogue_style": "冷硬直给",
                    "description_density": "中低",
                    "pacing_preference": "前三章快节奏",
                },
                "high_point_preferences": [],
                "avoid_patterns": [],
                "user_feedback": [],
            }
            market = {
                "adjustments": [
                    {
                        "id": "rich-ceo-second-sample",
                        "scope": "golden-three",
                        "summary": "第一章先落离婚协议与资源差，第二章拉董事会和试运营进场，第三章给出合伙人或席位级小兑现。",
                    }
                ]
            }
            (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "learned-patterns.json").write_text(json.dumps(learned, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "market-adjustments.json").write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
            (outline_dir / "总纲.md").write_text(
                "# 总纲\n\n离婚当天翻项目账，董事会和试运营一起进场，第三章改口合伙人。\n",
                encoding="utf-8",
            )
            sample_text = "离婚协议、董事会、试运营、合伙人、热搜、项目账。" * 80
            for chapter in ("001", "002", "003"):
                (chapters_dir / f"第{chapter}章.md").write_text(sample_text, encoding="utf-8")

            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapters="001-003",
                mode="writeback",
                writeback=True,
                save_packaging=True,
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "writeback")
            self.assertEqual(result["writeback_status"], "written")
            self.assertEqual(result["packaging_status"], "written")

            updated_state = json.loads((mighty / "state.json").read_text(encoding="utf-8"))
            chapter_meta = updated_state["chapter_meta"]["003"]
            self.assertIn("content_standard_flags", chapter_meta)
            self.assertIn("packaging_alignment_note", chapter_meta)

            updated_learned = json.loads((mighty / "learned-patterns.json").read_text(encoding="utf-8"))
            self.assertIn("opening_strategy", updated_learned)
            self.assertIn("multi_line_guardrails", updated_learned)
            self.assertIn("content_standard_alerts", updated_learned)

            packaging_path = project_root / "包装" / "包装方案.md"
            self.assertTrue(packaging_path.exists())
            packaging_content = packaging_path.read_text(encoding="utf-8")
            self.assertIn("推荐书名", packaging_content)
            self.assertIn("推荐简介", packaging_content)

    def test_split_runtime_guidance_preserves_recent_guardrails_sidecar_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)

            state = {
                "meta": {
                    "title": "guardrail-test",
                    "updated_at": "2026-03-25T00:00:00Z",
                },
                "learned_patterns": {
                    "opening_strategy": "先见冲突",
                    "multi_line_guardrails": ["主线先过户，副线轻触旧账。"],
                    "content_standard_alerts": ["避免背景先行"],
                    "recent_guardrails": {
                        "must_avoid": ["不要回滑到解释腔"],
                        "must_preserve": ["代价感"],
                        "next_chapter_watchpoints": ["下一章必须留残账"],
                        "expires_after_chapter": 4,
                    },
                },
                "market_adjustments": {
                    "adjustments": [],
                },
            }
            (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

            proc = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "split-runtime-guidance.py"),
                    str(project_root),
                    "--timestamp",
                    "2026-03-25T00:00:00Z",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertTrue(proc.stdout)

            learned_sidecar = json.loads((mighty / "learned-patterns.json").read_text(encoding="utf-8"))
            self.assertIn("recent_guardrails", learned_sidecar["data"])
            self.assertEqual(
                learned_sidecar["data"]["recent_guardrails"]["expires_after_chapter"],
                4,
            )

            updated_state = json.loads((mighty / "state.json").read_text(encoding="utf-8"))
            learned_summary = updated_state["learned_patterns"]
            self.assertTrue(learned_summary["externalized"])
            self.assertIn("recent_guardrails", learned_summary["available_sections"])
            self.assertTrue(learned_summary["has_recent_guardrails"])
            self.assertEqual(learned_summary["recent_guardrails_expires_after_chapter"], 4)
            self.assertNotIn("must_avoid", learned_summary)

    def test_writeback_mode_for_city_daily_project_writes_clean_packaging_file(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            chapters_dir = project_root / "chapters"
            outline_dir = project_root / "大纲"
            mighty.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            outline_dir.mkdir(parents=True)

            state = {
                "meta": {
                    "title": "搬回老小区后，我靠蹭饭认识了整栋楼",
                    "genre": "都市日常",
                    "platform": "番茄",
                    "updated_at": "2026-03-24T00:00:00Z",
                },
                "genre_profile": {"bucket": "都市日常"},
                "chapter_meta": {"003": {}},
            }
            learned = {
                "writing_style_preferences": {},
                "high_point_preferences": {},
                "avoid_patterns": [],
                "user_feedback": [],
            }
            market = {"adjustments": []}
            (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "learned-patterns.json").write_text(json.dumps(learned, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "market-adjustments.json").write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
            (outline_dir / "总纲.md").write_text(
                "# 总纲\n\n被裁员的苏禾搬回老小区，在停气、父亲康复和存款见底的夹击里，靠换饭和跑腿把自己重新接回整栋楼的人情网。\n",
                encoding="utf-8",
            )
            sample_text = "老小区、停气、换饭、复诊、白板、互助。" * 80
            for chapter in ("001", "002", "003"):
                (chapters_dir / f"第{chapter}章.md").write_text(sample_text, encoding="utf-8")

            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapters="001-003",
                mode="writeback",
                writeback=True,
                save_packaging=True,
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "writeback")
            packaging_path = project_root / "包装" / "包装方案.md"
            packaging_content = packaging_path.read_text(encoding="utf-8")
            self.assertIn("老小区", packaging_content)
            self.assertIn("换饭", packaging_content)
            self.assertNotIn("# 总纲", packaging_content)
            self.assertNotIn("## 一句话卖点被", packaging_content)
            self.assertNotIn("### 推荐简介\n\n#", packaging_content)

    def test_writeback_mode_for_historical_project_writes_specific_packaging_file(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            chapters_dir = project_root / "chapters"
            outline_dir = project_root / "大纲"
            mighty.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            outline_dir.mkdir(parents=True)

            state = {
                "meta": {
                    "title": "我在县衙当杂吏，靠翻旧案升了堂",
                    "genre": "历史脑洞",
                    "platform": "番茄",
                    "updated_at": "2026-03-24T00:00:00Z",
                },
                "genre_profile": {"bucket": "历史脑洞"},
                "chapter_meta": {"003": {}},
            }
            learned = {
                "writing_style_preferences": {},
                "high_point_preferences": [],
                "avoid_patterns": [],
                "user_feedback": [],
            }
            market = {"adjustments": []}
            (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "learned-patterns.json").write_text(json.dumps(learned, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "market-adjustments.json").write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
            (outline_dir / "总纲.md").write_text(
                "# 总纲\n\n永平二十三年，清河县县衙清积案问责压顶，最底层刑房杂吏沈砚靠卷宗回响翻旧案保命、拿权、升堂。\n",
                encoding="utf-8",
            )
            sample_text = "县衙、旧案、卷宗、供词、主簿房、二堂、升堂。" * 80
            for chapter in ("001", "002", "003"):
                (chapters_dir / f"第{chapter}章.md").write_text(sample_text, encoding="utf-8")

            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapters="001-003",
                mode="writeback",
                writeback=True,
                save_packaging=True,
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "writeback")
            packaging_path = project_root / "包装" / "包装方案.md"
            packaging_content = packaging_path.read_text(encoding="utf-8")
            self.assertIn("卷宗回响", packaging_content)
            self.assertIn("旧案", packaging_content)
            self.assertIn("推荐简介", packaging_content)

    def test_writeback_mode_preserves_existing_packaging_by_writing_sidecar(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            chapters_dir = project_root / "chapters"
            outline_dir = project_root / "大纲"
            packaging_dir = project_root / "包装"
            mighty.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            outline_dir.mkdir(parents=True)
            packaging_dir.mkdir(parents=True)

            state = {
                "meta": {
                    "title": "继母换我婚书那夜，太子先开了口",
                    "genre": "宫斗宅斗",
                    "platform": "番茄",
                    "updated_at": "2026-03-24T00:00:00Z",
                },
                "genre_profile": {"bucket": "宫斗宅斗"},
                "chapter_meta": {"003": {}},
            }
            learned = {
                "version": "1.0",
                "data": {
                    "writing_style_preferences": {},
                    "high_point_preferences": [],
                    "avoid_patterns": [],
                    "user_feedback": [],
                },
            }
            market = {"adjustments": []}
            (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "learned-patterns.json").write_text(json.dumps(learned, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "market-adjustments.json").write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
            (outline_dir / "总纲.md").write_text(
                "# 总纲\n\n继母动婚书那夜，庶二姑娘谢云昭把旧账翻上东宫案前。\n",
                encoding="utf-8",
            )
            (packaging_dir / "包装方案.md").write_text("# 旧包装\n\n保留此文件\n", encoding="utf-8")
            sample_text = "继母压制、婚书被换、东宫、伯府旧账、反咬。" * 80
            for chapter in ("001", "002", "003"):
                (chapters_dir / f"第{chapter}章.md").write_text(sample_text, encoding="utf-8")

            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapters="001-003",
                mode="writeback",
                writeback=True,
                save_packaging=True,
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "writeback")
            self.assertEqual(result["packaging_status"], "written-sidecar")
            primary_packaging = (packaging_dir / "包装方案.md").read_text(encoding="utf-8")
            sidecar_packaging = (packaging_dir / "包装方案-writing-core.md").read_text(encoding="utf-8")
            self.assertIn("保留此文件", primary_packaging)
            self.assertIn("继母压制", sidecar_packaging)

    def test_writeback_mode_for_work_romance_project_writes_specific_packaging_file(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            chapters_dir = project_root / "chapters"
            outline_dir = project_root / "大纲"
            mighty.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            outline_dir.mkdir(parents=True)

            state = {
                "meta": {
                    "title": "她升职那天，前上司成了我合租室友",
                    "genre": "职场婚恋",
                    "platform": "番茄",
                    "updated_at": "2026-03-24T00:00:00Z",
                },
                "genre_profile": {"bucket": "职场婚恋"},
                "chapter_meta": {"003": {}},
            }
            learned = {
                "writing_style_preferences": {},
                "high_point_preferences": [],
                "avoid_patterns": [],
                "user_feedback": [],
            }
            market = {"adjustments": []}
            (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "learned-patterns.json").write_text(json.dumps(learned, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "market-adjustments.json").write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
            (outline_dir / "总纲.md").write_text(
                "# 总纲\n\n姜栀升职当天接锅，回家却发现前上司成了新室友，第三章拿下72小时试运行窗口。\n",
                encoding="utf-8",
            )
            sample_text = "升职接锅、合租揭面、试运行、甲方、续约、项目账。" * 80
            for chapter in ("001", "002", "003"):
                (chapters_dir / f"第{chapter}章.md").write_text(sample_text, encoding="utf-8")

            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapters="001-003",
                mode="writeback",
                writeback=True,
                save_packaging=True,
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "writeback")
            packaging_path = project_root / "包装" / "包装方案.md"
            packaging_content = packaging_path.read_text(encoding="utf-8")
            self.assertIn("升职接锅", packaging_content)
            self.assertIn("合租揭面", packaging_content)
            self.assertIn("试运行窗口", packaging_content)
            self.assertNotIn("书名:", packaging_content)

    def test_writeback_mode_for_youth_romance_project_writes_specific_packaging_file(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            chapters_dir = project_root / "chapters"
            outline_dir = project_root / "大纲"
            mighty.mkdir(parents=True)
            chapters_dir.mkdir(parents=True)
            outline_dir.mkdir(parents=True)

            state = {
                "meta": {
                    "title": "转学第一天，我把校草认成了新来的代课老师",
                    "genre": "青春甜宠",
                    "platform": "番茄",
                    "updated_at": "2026-03-24T00:00:00Z",
                },
                "genre_profile": {"bucket": "青春甜宠"},
                "chapter_meta": {"003": {}},
            }
            learned = {
                "writing_style_preferences": {},
                "high_point_preferences": [],
                "avoid_patterns": [],
                "user_feedback": [],
            }
            market = {"adjustments": []}
            (mighty / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "learned-patterns.json").write_text(json.dumps(learned, ensure_ascii=False, indent=2), encoding="utf-8")
            (mighty / "market-adjustments.json").write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
            (outline_dir / "总纲.md").write_text(
                "# 总纲\n\n转学第一天，林栀夏把校草认成代课老师，身份错认把她推入学习互助和校园舆论里。\n",
                encoding="utf-8",
            )
            sample_text = "转学第一天、身份错认、学习互助、广播站、校草、校园舆论。" * 80
            for chapter in ("001", "002", "003"):
                (chapters_dir / f"第{chapter}章.md").write_text(sample_text, encoding="utf-8")

            output_path = Path(tmpdir) / "writing-core-smoke.md"

            result = module.run_smoke(
                project_root=project_root,
                chapters="001-003",
                mode="writeback",
                writeback=True,
                save_packaging=True,
                output_path=output_path,
                date_str="2026-03-24",
            )

            self.assertEqual(result["effective_mode"], "writeback")
            packaging_path = project_root / "包装" / "包装方案.md"
            packaging_content = packaging_path.read_text(encoding="utf-8")
            self.assertIn("身份错认", packaging_content)
            self.assertIn("学习互助", packaging_content)
            self.assertNotIn("书名:", packaging_content)


if __name__ == "__main__":
    unittest.main()
