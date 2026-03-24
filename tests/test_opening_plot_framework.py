from pathlib import Path
import unittest
import json


REPO_ROOT = Path(__file__).resolve().parents[1]

FRAMEWORK_FILES = [
    "docs/opening-and-plot-framework/README.md",
    "docs/opening-and-plot-framework/01-开篇目标与成功标准.md",
    "docs/opening-and-plot-framework/02-开篇构件与组合公式.md",
    "docs/opening-and-plot-framework/03-开篇故障与修正.md",
    "docs/opening-and-plot-framework/04-剧情层次模型.md",
    "docs/opening-and-plot-framework/05-推进链与残账设计.md",
    "docs/opening-and-plot-framework/06-题材特化接口.md",
    "docs/opening-and-plot-framework/fanqie-p0-smoke-template.md",
    "docs/opening-and-plot-framework/fanqie-p0-output-contract.md",
    "docs/opening-and-plot-framework/fanqie-p0-gap-tracker-2026-03.md",
    "docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md",
    "docs/opening-and-plot-framework/real-project-smoke-hunshu-taizi-fanqie-p0-2026-03-23.md",
    "docs/opening-and-plot-framework/real-project-smoke-转学第一天-我把校草认成了新来的代课老师-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-公司裁我那天-系统先赔了我一百万-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-她升职那天-前上司成了我合租室友-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-搬回老小区后-我靠蹭饭认识了整栋楼-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-宗门垫底那年-我把废丹卖成了天价-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-我在县衙当杂吏-靠翻旧案升了堂-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-签下离婚协议那天-冷脸总裁改口叫我合伙人-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-我在县衙誊旧档-靠半页供词改了判词-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-外门药田被夺那天-我靠废丹拍卖赚回了灵石-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-外门药田被夺那天-我靠废丹拍卖赚回了灵石-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-离婚冷静期那天-前夫把董事会席位押给了我-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-我赔光积蓄那天-系统先把违约金打到了账上-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/real-project-smoke-外门药田被夺那天-我靠废丹拍卖赚回了灵石-fanqie-p0-2026-03-24.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/README.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/宫斗宅斗.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/职场婚恋.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/青春甜宠.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/豪门总裁.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/都市日常.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/玄幻脑洞.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/都市脑洞.md",
    "docs/opening-and-plot-framework/fanqie-p0-overlays/历史脑洞.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/README.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/宫斗宅斗.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/职场婚恋.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/青春甜宠.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/豪门总裁.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/都市日常.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/玄幻脑洞.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/都市脑洞.md",
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/历史脑洞.md",
]

SKILL_EXPECTATIONS = {
    "skills/novel-outline/SKILL.md": [
        "../../docs/opening-and-plot-framework/README.md",
        "../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md",
        "../../docs/opening-and-plot-framework/04-剧情层次模型.md",
        "../../docs/opening-and-plot-framework/05-推进链与残账设计.md",
        "../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md",
    ],
    "skills/novel-write/SKILL.md": [
        "../../docs/opening-and-plot-framework/README.md",
        "../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md",
        "../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md",
        "../../docs/opening-and-plot-framework/05-推进链与残账设计.md",
        "../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md",
    ],
    "skills/novel-review/SKILL.md": [
        "../../docs/opening-and-plot-framework/README.md",
        "../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md",
        "../../docs/opening-and-plot-framework/03-开篇故障与修正.md",
        "../../docs/opening-and-plot-framework/05-推进链与残账设计.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-output-contract.md",
        "../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-checkcards/<bucket>.md",
        "fanqie_bucket_review_summary",
    ],
    "skills/novel-precheck/SKILL.md": [
        "../../docs/opening-and-plot-framework/README.md",
        "../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md",
        "../../docs/opening-and-plot-framework/05-推进链与残账设计.md",
        "../../docs/opening-and-plot-framework/06-题材特化接口.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-output-contract.md",
        "../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-checkcards/<bucket>.md",
        "fanqie_bucket_precheck_summary",
    ],
    "skills/novel-package/SKILL.md": [
        "../../docs/opening-and-plot-framework/README.md",
        "../../docs/opening-and-plot-framework/01-开篇目标与成功标准.md",
        "../../docs/opening-and-plot-framework/02-开篇构件与组合公式.md",
        "../../docs/opening-and-plot-framework/06-题材特化接口.md",
        "../../docs/opening-and-plot-framework/fanqie-priority-categories-2026-03.md",
        "../../docs/opening-and-plot-framework/fanqie-p0-overlays/<bucket>.md",
    ],
}

ENTRY_DOCS = {
    "README.md": "opening-and-plot-framework",
    "docs/start-here.md": "opening-and-plot-framework",
    "docs/skill-usage.md": "opening-and-plot-framework",
    "docs/default-workflows.md": "opening-and-plot-framework",
    "docs/opening-and-plot-framework/README.md": "fanqie-p0-smoke-template.md",
}

README_EXPECTED_TOKENS = [
    "转学第一天，我把校草认成了新来的代课老师",
    "公司裁我那天，系统先赔了我一百万",
    "她升职那天，前上司成了我合租室友",
    "搬回老小区后，我靠蹭饭认识了整栋楼",
    "宗门垫底那年，我把废丹卖成了天价",
    "我在县衙当杂吏，靠翻旧案升了堂",
    "签下离婚协议那天，冷脸总裁改口叫我合伙人",
    "我在县衙誊旧档，靠半页供词改了判词",
    "离婚冷静期那天，前夫把董事会席位押给了我",
    "我赔光积蓄那天，系统先把违约金打到了账上",
    "外门药田被夺那天，我靠废丹拍卖赚回了灵石",
    "离婚冷静期那天，前夫把董事会席位押给了我",
    "我赔光积蓄那天，系统先把违约金打到了账上",
    "外门药田被夺那天，我靠废丹拍卖赚回了灵石",
    "fanqie-p0-gap-tracker-2026-03.md",
]

GAP_TRACKER_EXPECTED_TOKENS = [
    "## 已覆盖桶",
    "## 仍缺真实项目的桶",
    "## 下一批推荐顺序",
    "## 可直接开工的项目提示词",
]

STATE_SCHEMA_EXPECTED_TOKENS = [
    "开篇抓力",
    "层次清晰度",
    "推进有效性",
    "fanqie_bucket_flags",
    "fanqie_bucket_summary",
]

OVERLAY_STRUCTURE_EXPECTATIONS = {
    "docs/opening-and-plot-framework/fanqie-p0-overlays/宫斗宅斗.md": [
        "## 开篇公式",
        "## 黄金三章最低要求",
        "## 高频故障清单",
        "## precheck 专项检查点",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-overlays/职场婚恋.md": [
        "## 开篇公式",
        "## 黄金三章最低要求",
        "## 高频故障清单",
        "## precheck 专项检查点",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-overlays/青春甜宠.md": [
        "## 开篇公式",
        "## 黄金三章最低要求",
        "## 高频故障清单",
        "## precheck 专项检查点",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-overlays/豪门总裁.md": [
        "## 开篇公式",
        "## 黄金三章最低要求",
        "## 高频故障清单",
        "## precheck 专项检查点",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-overlays/都市日常.md": [
        "## 开篇公式",
        "## 黄金三章最低要求",
        "## 高频故障清单",
        "## precheck 专项检查点",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-overlays/玄幻脑洞.md": [
        "## 开篇公式",
        "## 黄金三章最低要求",
        "## 高频故障清单",
        "## precheck 专项检查点",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-overlays/都市脑洞.md": [
        "## 开篇公式",
        "## 黄金三章最低要求",
        "## 高频故障清单",
        "## precheck 专项检查点",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-overlays/历史脑洞.md": [
        "## 开篇公式",
        "## 黄金三章最低要求",
        "## 高频故障清单",
        "## precheck 专项检查点",
    ],
}

CHECKCARD_STRUCTURE_EXPECTATIONS = {
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/宫斗宅斗.md": [
        "## 自动触发范围",
        "## 对 `novel-review`",
        "## 对 `novel-precheck`",
        "## 核心检查问题",
        "## 红灯判定",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/职场婚恋.md": [
        "## 自动触发范围",
        "## 对 `novel-review`",
        "## 对 `novel-precheck`",
        "## 核心检查问题",
        "## 红灯判定",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/青春甜宠.md": [
        "## 自动触发范围",
        "## 对 `novel-review`",
        "## 对 `novel-precheck`",
        "## 核心检查问题",
        "## 红灯判定",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/豪门总裁.md": [
        "## 自动触发范围",
        "## 对 `novel-review`",
        "## 对 `novel-precheck`",
        "## 核心检查问题",
        "## 红灯判定",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/都市日常.md": [
        "## 自动触发范围",
        "## 对 `novel-review`",
        "## 对 `novel-precheck`",
        "## 核心检查问题",
        "## 红灯判定",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/玄幻脑洞.md": [
        "## 自动触发范围",
        "## 对 `novel-review`",
        "## 对 `novel-precheck`",
        "## 核心检查问题",
        "## 红灯判定",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/都市脑洞.md": [
        "## 自动触发范围",
        "## 对 `novel-review`",
        "## 对 `novel-precheck`",
        "## 核心检查问题",
        "## 红灯判定",
    ],
    "docs/opening-and-plot-framework/fanqie-p0-checkcards/历史脑洞.md": [
        "## 自动触发范围",
        "## 对 `novel-review`",
        "## 对 `novel-precheck`",
        "## 核心检查问题",
        "## 红灯判定",
    ],
}

SMOKE_TEMPLATE_EXPECTED_TOKENS = [
    "## 适用场景",
    "## 使用步骤",
    "## `novel-review` 样本模板",
    "## `novel-precheck` 样本模板",
    "## 可选写回记录",
]


class OpeningAndPlotFrameworkTests(unittest.TestCase):
    def test_framework_files_exist(self) -> None:
        for relative_path in FRAMEWORK_FILES:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).exists(), f"{relative_path} is missing")

    def test_skill_contracts_reference_framework(self) -> None:
        for relative_path, expected_tokens in SKILL_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                with self.subTest(file=relative_path, token=token):
                    self.assertIn(token, content)

    def test_entry_docs_expose_framework(self) -> None:
        for relative_path, token in ENTRY_DOCS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            with self.subTest(file=relative_path):
                self.assertIn(token, content)

    def test_state_schema_mentions_optional_review_dimensions(self) -> None:
        content = (REPO_ROOT / "shared/references/shared/state-schema.md").read_text(encoding="utf-8")
        for token in STATE_SCHEMA_EXPECTED_TOKENS:
            with self.subTest(token=token):
                self.assertIn(token, content)

    def test_fanqie_p0_overlay_files_have_medium_depth_sections(self) -> None:
        for relative_path, expected_tokens in OVERLAY_STRUCTURE_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                with self.subTest(file=relative_path, token=token):
                    self.assertIn(token, content)

    def test_fanqie_p0_checkcards_have_review_and_precheck_sections(self) -> None:
        for relative_path, expected_tokens in CHECKCARD_STRUCTURE_EXPECTATIONS.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in expected_tokens:
                with self.subTest(file=relative_path, token=token):
                    self.assertIn(token, content)

    def test_real_project_sample_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/庶女谋略/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter_meta = state.get("chapter_meta", {})
        self.assertIn("003", chapter_meta)
        chapter = chapter_meta["003"]
        self.assertIn("fanqie_bucket_flags", chapter)
        self.assertIn("fanqie_bucket_summary", chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "宫斗宅斗")

    def test_qingchun_tianchong_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/转学第一天，我把校草认成了新来的代课老师/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter_meta = state.get("chapter_meta", {})
        self.assertIn("003", chapter_meta)
        chapter = chapter_meta["003"]
        self.assertIn("fanqie_bucket_flags", chapter)
        self.assertIn("fanqie_bucket_summary", chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "青春甜宠")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "pass")

    def test_dushi_naodong_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/公司裁我那天，系统先赔了我一百万/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter_meta = state.get("chapter_meta", {})
        self.assertIn("003", chapter_meta)
        chapter = chapter_meta["003"]
        self.assertIn("fanqie_bucket_flags", chapter)
        self.assertIn("fanqie_bucket_summary", chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "都市脑洞")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "warn")

    def test_zhichang_hunlian_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/她升职那天，前上司成了我合租室友/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter_meta = state.get("chapter_meta", {})
        self.assertIn("003", chapter_meta)
        chapter = chapter_meta["003"]
        self.assertIn("fanqie_bucket_flags", chapter)
        self.assertIn("fanqie_bucket_summary", chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "职场婚恋")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "pass")

    def test_dushi_richang_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/搬回老小区后，我靠蹭饭认识了整栋楼/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter_meta = state.get("chapter_meta", {})
        self.assertIn("003", chapter_meta)
        chapter = chapter_meta["003"]
        self.assertIn("fanqie_bucket_flags", chapter)
        self.assertIn("fanqie_bucket_summary", chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "都市日常")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "pass")

    def test_xuanhuan_naodong_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/宗门垫底那年，我把废丹卖成了天价/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter_meta = state.get("chapter_meta", {})
        self.assertIn("003", chapter_meta)
        chapter = chapter_meta["003"]
        self.assertIn("fanqie_bucket_flags", chapter)
        self.assertIn("fanqie_bucket_summary", chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "玄幻脑洞")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "pass")

    def test_lishi_naodong_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/我在县衙当杂吏，靠翻旧案升了堂/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter_meta = state.get("chapter_meta", {})
        chapter = chapter_meta.get("003") or chapter_meta.get("3")
        self.assertIsNotNone(chapter)
        self.assertIn("fanqie_bucket_flags", chapter)
        self.assertIn("fanqie_bucket_summary", chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "历史脑洞")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "pass")

    def test_haomen_zongcai_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/签下离婚协议那天，冷脸总裁改口叫我合伙人/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter_meta = state.get("chapter_meta", {})
        chapter = chapter_meta.get("003") or chapter_meta.get("3")
        self.assertIsNotNone(chapter)
        self.assertIn("fanqie_bucket_flags", chapter)
        self.assertIn("fanqie_bucket_summary", chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "豪门总裁")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "pass")

    def test_third_urban_brainhole_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/我赔光积蓄那天，系统先把违约金打到了账上/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter = (state.get("chapter_meta", {}) or {}).get("003")
        self.assertIsNotNone(chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "都市脑洞")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "warn")

    def test_third_rich_ceo_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/离婚冷静期那天，前夫把董事会席位押给了我/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter = (state.get("chapter_meta", {}) or {}).get("003")
        self.assertIsNotNone(chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "豪门总裁")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "pass")

    def test_third_historical_brainhole_real_project_state_contains_bucket_writeback(self) -> None:
        state_path = REPO_ROOT / "projects/我在县衙誊旧档，靠半页供词改了判词/.mighty/state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        chapter = (state.get("chapter_meta", {}) or {}).get("003")
        self.assertIsNotNone(chapter)
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket"), "历史脑洞")
        self.assertEqual(chapter["fanqie_bucket_summary"].get("bucket_grade"), "pass")

    def test_fanqie_p0_smoke_template_has_reusable_sections(self) -> None:
        content = (REPO_ROOT / "docs/opening-and-plot-framework/fanqie-p0-smoke-template.md").read_text(
            encoding="utf-8"
        )
        for token in SMOKE_TEMPLATE_EXPECTED_TOKENS:
            with self.subTest(token=token):
                self.assertIn(token, content)

    def test_framework_readme_exposes_real_project_smoke_samples(self) -> None:
        content = (REPO_ROOT / "docs/opening-and-plot-framework/README.md").read_text(encoding="utf-8")
        for token in README_EXPECTED_TOKENS:
            with self.subTest(token=token):
                self.assertIn(token, content)

    def test_gap_tracker_doc_has_remaining_bucket_sections(self) -> None:
        content = (REPO_ROOT / "docs/opening-and-plot-framework/fanqie-p0-gap-tracker-2026-03.md").read_text(
            encoding="utf-8"
        )
        for token in GAP_TRACKER_EXPECTED_TOKENS:
            with self.subTest(token=token):
                self.assertIn(token, content)


if __name__ == "__main__":
    unittest.main()
