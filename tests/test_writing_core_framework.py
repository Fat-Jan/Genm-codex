from pathlib import Path
import json
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]

FRAMEWORK_FILES = [
    "docs/writing-core-framework/README.md",
    "docs/writing-core-framework/01-写作基本功总纲.md",
    "docs/writing-core-framework/02-叙述-镜头-信息投放.md",
    "docs/writing-core-framework/03-对白-动作-情绪-段落节奏.md",
    "docs/writing-core-framework/04-剧情层次与多线编排接口.md",
    "docs/writing-core-framework/05-内容标准与常见失格.md",
    "docs/writing-core-framework/06-精品审核与投稿前判断.md",
    "docs/writing-core-framework/07-memory-压缩信号约定.md",
    "docs/writing-core-framework/08-开篇包装输入接口.md",
    "docs/writing-core-framework/real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md",
    "docs/writing-core-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md",
    "docs/writing-core-framework/real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-2026-03-24.md",
    "docs/writing-core-framework/real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-2026-03-24.md",
    "docs/writing-core-framework/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md",
    "scripts/writing_core_smoke.py",
    "docs/writing-core-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md",
    "docs/writing-core-framework/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md",
    "docs/writing-core-framework/real-project-smoke-继母换我婚书那夜-太子先开了口-2026-03-24.md",
    "scripts/batch_writing_core_smoke.py",
    "docs/writing-core-framework/batch-smoke-manifest.json",
    "docs/writing-core-framework/batch-output/summary-report.json",
    "docs/writing-core-framework/batch-output/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md",
    "docs/writing-core-framework/batch-output/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md",
    "docs/writing-core-framework/batch-output/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md",
]

SKILL_EXPECTATIONS = {
    "skills/novel-outline/SKILL.md": [
        "../../docs/writing-core-framework/README.md",
        "../../docs/writing-core-framework/04-剧情层次与多线编排接口.md",
    ],
    "skills/novel-write/SKILL.md": [
        "../../docs/writing-core-framework/README.md",
        "../../docs/writing-core-framework/01-写作基本功总纲.md",
        "../../docs/writing-core-framework/02-叙述-镜头-信息投放.md",
        "../../docs/writing-core-framework/03-对白-动作-情绪-段落节奏.md",
        "../../docs/writing-core-framework/05-内容标准与常见失格.md",
    ],
    "skills/novel-review/SKILL.md": [
        "../../docs/writing-core-framework/README.md",
        "../../docs/writing-core-framework/01-写作基本功总纲.md",
        "../../docs/writing-core-framework/05-内容标准与常见失格.md",
        "../../docs/writing-core-framework/06-精品审核与投稿前判断.md",
        "../../docs/writing-core-framework/07-memory-压缩信号约定.md",
    ],
    "skills/novel-precheck/SKILL.md": [
        "../../docs/writing-core-framework/README.md",
        "../../docs/writing-core-framework/05-内容标准与常见失格.md",
        "../../docs/writing-core-framework/06-精品审核与投稿前判断.md",
        "../../docs/writing-core-framework/08-开篇包装输入接口.md",
    ],
    "skills/novel-package/SKILL.md": [
        "../../docs/writing-core-framework/README.md",
        "../../docs/writing-core-framework/06-精品审核与投稿前判断.md",
        "../../docs/writing-core-framework/08-开篇包装输入接口.md",
    ],
    "skills/novel-learn/SKILL.md": [
        "../../docs/writing-core-framework/07-memory-压缩信号约定.md",
        "opening_strategy",
        "multi_line_guardrails",
        "content_standard_alerts",
    ],
}

ENTRY_DOCS = {
    "README.md": "writing-core-framework",
    "docs/start-here.md": "writing-core-framework",
    "docs/skill-usage.md": "writing-core-framework",
    "docs/default-workflows.md": "writing-core-framework",
}

FRAMEWORK_README_EXPECTED_TOKENS = [
    "不是课程 dump",
    "opening-and-plot-framework",
    "写作基本功",
    "内容标准",
    "memory",
    "开篇包装输入",
    "宗门垫底那年，我把废丹卖成了天价",
    "离婚冷静期那天，前夫把董事会席位押给了我",
    "搬回老小区后，我靠蹭饭认识了整栋楼",
    "我在县衙当杂吏，靠翻旧案升了堂",
    "她升职那天，前上司成了我合租室友",
    "python3 scripts/writing_core_smoke.py",
    "转学第一天，我把校草认成了新来的代课老师",
    "我赔光积蓄那天，系统先把违约金打到了账上",
    "python3 scripts/batch_writing_core_smoke.py",
    "batch-smoke-manifest.json",
    "继母换我婚书那夜，太子先开了口",
]

STATE_SCHEMA_EXPECTED_TOKENS = [
    "opening_strategy",
    "multi_line_guardrails",
    "content_standard_alerts",
    "content_standard_flags",
    "packaging_alignment_note",
]

STATE_TEMPLATE_EXPECTED_KEYS = [
    "opening_strategy",
    "multi_line_guardrails",
    "content_standard_alerts",
    "content_standard_flags",
    "packaging_alignment_note",
]

STATE_THINNING_EXPECTED_TOKENS = [
    ".mighty/learned-patterns.json",
    "轻量摘要 / 指针",
    "learned_patterns",
]

FIXED_BATCH_BUCKETS = {
    "宫斗宅斗",
    "职场婚恋",
    "青春甜宠",
    "豪门总裁",
    "都市日常",
    "玄幻脑洞",
    "都市脑洞",
    "历史脑洞",
}

SAMPLE_PROJECTS = {
    "projects/宗门垫底那年，我把废丹卖成了天价": {
        "learned_patterns_path": "projects/宗门垫底那年，我把废丹卖成了天价/.mighty/learned-patterns.json",
        "state_path": "projects/宗门垫底那年，我把废丹卖成了天价/.mighty/state.json",
        "packaging_path": "projects/宗门垫底那年，我把废丹卖成了天价/包装/包装方案.md",
        "smoke_path": "docs/writing-core-framework/real-project-smoke-宗门垫底那年-我把废丹卖成了天价-2026-03-24.md",
        "state_chapter": "003",
        "packaging_title": "宗门垫底那年，我把废丹卖成了天价",
    },
    "projects/离婚冷静期那天，前夫把董事会席位押给了我": {
        "learned_patterns_path": "projects/离婚冷静期那天，前夫把董事会席位押给了我/.mighty/learned-patterns.json",
        "state_path": "projects/离婚冷静期那天，前夫把董事会席位押给了我/.mighty/state.json",
        "packaging_path": "projects/离婚冷静期那天，前夫把董事会席位押给了我/包装/包装方案.md",
        "smoke_path": "docs/writing-core-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-2026-03-24.md",
        "state_chapter": "003",
        "packaging_title": "离婚冷静期那天，前夫把董事会席位押给了我",
    },
    "projects/搬回老小区后，我靠蹭饭认识了整栋楼": {
        "learned_patterns_path": "projects/搬回老小区后，我靠蹭饭认识了整栋楼/.mighty/learned-patterns.json",
        "state_path": "projects/搬回老小区后，我靠蹭饭认识了整栋楼/.mighty/state.json",
        "packaging_path": "projects/搬回老小区后，我靠蹭饭认识了整栋楼/包装/包装方案.md",
        "smoke_path": "docs/writing-core-framework/real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-2026-03-24.md",
        "state_chapter": "003",
        "packaging_title": "搬回老小区后，我靠蹭饭认识了整栋楼",
    },
    "projects/我在县衙当杂吏，靠翻旧案升了堂": {
        "learned_patterns_path": "projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/learned-patterns.json",
        "state_path": "projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/state.json",
        "packaging_path": "projects/我在县衙当杂吏，靠翻旧案升了堂/包装/包装方案.md",
        "smoke_path": "docs/writing-core-framework/real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-2026-03-24.md",
        "state_chapter": "003",
        "packaging_title": "我在县衙当杂吏，靠翻旧案升了堂",
    },
    "projects/她升职那天，前上司成了我合租室友": {
        "learned_patterns_path": "projects/她升职那天，前上司成了我合租室友/.mighty/learned-patterns.json",
        "state_path": "projects/她升职那天，前上司成了我合租室友/.mighty/state.json",
        "packaging_path": "projects/她升职那天，前上司成了我合租室友/包装/包装方案.md",
        "smoke_path": "docs/writing-core-framework/real-project-smoke-她升职那天-前上司成了我合租室友-2026-03-24.md",
        "state_chapter": "003",
        "packaging_title": "她升职那天，前上司成了我合租室友",
    },
    "projects/转学第一天，我把校草认成了新来的代课老师": {
        "learned_patterns_path": "projects/转学第一天，我把校草认成了新来的代课老师/.mighty/learned-patterns.json",
        "state_path": "projects/转学第一天，我把校草认成了新来的代课老师/.mighty/state.json",
        "packaging_path": "projects/转学第一天，我把校草认成了新来的代课老师/包装/包装方案.md",
        "smoke_path": "docs/writing-core-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-2026-03-24.md",
        "state_chapter": "003",
        "packaging_title": "转学第一天，我把校草认成了新来的代课老师",
    },
    "projects/我赔光积蓄那天，系统先把违约金打到了账上": {
        "learned_patterns_path": "projects/我赔光积蓄那天，系统先把违约金打到了账上/.mighty/learned-patterns.json",
        "state_path": "projects/我赔光积蓄那天，系统先把违约金打到了账上/.mighty/state.json",
        "packaging_path": "projects/我赔光积蓄那天，系统先把违约金打到了账上/包装/包装方案.md",
        "smoke_path": "docs/writing-core-framework/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-2026-03-24.md",
        "state_chapter": "003",
        "packaging_title": "我赔光积蓄那天，系统先把违约金打到了账上",
    },
    "projects/庶妹换我婚书那夜，太子先开了口": {
        "learned_patterns_path": "projects/庶妹换我婚书那夜，太子先开了口/.mighty/learned-patterns.json",
        "state_path": "projects/庶妹换我婚书那夜，太子先开了口/.mighty/state.json",
        "packaging_path": "projects/庶妹换我婚书那夜，太子先开了口/包装/包装方案-writing-core.md",
        "smoke_path": "docs/writing-core-framework/real-project-smoke-继母换我婚书那夜-太子先开了口-2026-03-24.md",
        "state_chapter": "003",
        "packaging_title": "继母换我婚书那夜，太子先开了口",
    },
}


class WritingCoreFrameworkContractTests(unittest.TestCase):
    def test_framework_files_exist(self):
        for relative_path in FRAMEWORK_FILES:
            path = REPO_ROOT / relative_path
            self.assertTrue(path.exists(), f"Missing framework file: {relative_path}")

    def test_framework_readme_exposes_boundary(self):
        content = (REPO_ROOT / "docs/writing-core-framework/README.md").read_text(encoding="utf-8")
        for token in FRAMEWORK_README_EXPECTED_TOKENS:
            self.assertIn(token, content)

    def test_skills_reference_framework(self):
        for relative_path, expected_tokens in SKILL_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_entry_docs_expose_framework(self):
        for relative_path, token in ENTRY_DOCS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_state_schema_mentions_compressed_signal_contract(self):
        content = (REPO_ROOT / "shared/references/shared/state-schema.md").read_text(encoding="utf-8")
        for token in STATE_SCHEMA_EXPECTED_TOKENS:
            self.assertIn(token, content)

    def test_state_thinning_doc_mentions_pointer_style_storage(self):
        content = (REPO_ROOT / "docs/state-thinning-and-setting-sync.md").read_text(encoding="utf-8")
        for token in STATE_THINNING_EXPECTED_TOKENS:
            self.assertIn(token, content)

    def test_state_template_contains_lightweight_fields(self):
        state = json.loads((REPO_ROOT / "shared/templates/state-v5-template.json").read_text(encoding="utf-8"))
        learned_patterns = state["learned_patterns"]
        chapter_meta = state["chapter_meta"]["<chapter_number>"]
        self.assertIn("opening_strategy", learned_patterns)
        self.assertIn("multi_line_guardrails", learned_patterns)
        self.assertIn("content_standard_alerts", learned_patterns)
        self.assertIn("content_standard_flags", chapter_meta)
        self.assertIn("packaging_alignment_note", chapter_meta)

    def test_real_project_smokes_reference_packaging_closure(self):
        for _, sample in SAMPLE_PROJECTS.items():
            content = (REPO_ROOT / sample["smoke_path"]).read_text(encoding="utf-8")
            self.assertIn("packaging-needs-update", content)
            self.assertIn("收口更新", content)
            self.assertIn("包装/包装方案.md", content)

    def test_real_project_learned_patterns_contain_compressed_signals(self):
        for _, sample in SAMPLE_PROJECTS.items():
            learned = json.loads((REPO_ROOT / sample["learned_patterns_path"]).read_text(encoding="utf-8"))
            data = learned.get("data", learned)
            self.assertIn("opening_strategy", data)
            self.assertIn("multi_line_guardrails", data)
            self.assertIn("content_standard_alerts", data)

    def test_real_project_state_contains_chapter_level_contract_fields(self):
        for _, sample in SAMPLE_PROJECTS.items():
            state = json.loads((REPO_ROOT / sample["state_path"]).read_text(encoding="utf-8"))
            chapter_map = state["chapter_meta"]
            chapter_key = sample["state_chapter"]
            chapter_meta = chapter_map.get(chapter_key) or chapter_map.get(str(int(chapter_key)))
            self.assertIsNotNone(chapter_meta, f"Missing chapter_meta for {sample['state_path']} chapter {chapter_key}")
            self.assertIn("content_standard_flags", chapter_meta)
            self.assertIn("packaging_alignment_note", chapter_meta)
            learned_patterns = state.get("learned_patterns", {})
            if learned_patterns:
                available_sections = learned_patterns.get("available_sections", [])
                self.assertIn("opening_strategy", available_sections)
                self.assertIn("multi_line_guardrails", available_sections)
                self.assertIn("content_standard_alerts", available_sections)

    def test_real_project_packaging_outputs_exist_and_match_title(self):
        for _, sample in SAMPLE_PROJECTS.items():
            path = REPO_ROOT / sample["packaging_path"]
            self.assertTrue(path.exists(), f"Missing packaging output: {sample['packaging_path']}")
            content = path.read_text(encoding="utf-8")
            self.assertIn(sample["packaging_title"], content)
            self.assertIn("推荐书名", content)
            self.assertIn("推荐简介", content)

    def test_fixed_batch_baseline_covers_representative_buckets(self):
        summary = json.loads((REPO_ROOT / "docs/writing-core-framework/batch-output/summary-report.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["count"], len(FIXED_BATCH_BUCKETS))
        self.assertEqual(summary["success_count"], len(FIXED_BATCH_BUCKETS))
        self.assertEqual(summary["failure_count"], 0)
        self.assertEqual(set(summary["bucket_counts"].keys()), FIXED_BATCH_BUCKETS)


if __name__ == "__main__":
    unittest.main()
