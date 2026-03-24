from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "novel_scan.py"


def load_module():
    spec = importlib.util.spec_from_file_location("novel_scan", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class NovelScanTests(unittest.TestCase):
    def test_default_source_plan_supports_fanqie_palace_intrigue_quick(self) -> None:
        module = load_module()

        plan = module.default_source_plan("番茄", "宫斗宅斗", "quick")

        urls = [item["url"] for item in plan["targets"]]
        self.assertIn("https://fanqienovel.com/rank/0", urls)
        self.assertIn("https://fanqienovel.com/rank/0_2_246", urls)
        self.assertIn("https://fanqienovel.com/rank/0_1_246", urls)
        self.assertIn("https://fanqienovel.com/rank/0_2_1139", urls)
        self.assertIn("https://fanqienovel.com/rank/0_1_1139", urls)

    def test_parse_fanqie_ranking_entries_extracts_ranked_items(self) -> None:
        module = load_module()
        body = (
            "统计时间截止至 03-22 24:00 榜单说明 "
            "01 - 天渊 沐潇三生 主角腹黑 无系统 幽默 传统玄幻 在读：106.2万 最近更新：第2619章 "
            "02 - 惊鸿 一夕烟雨 传统玄幻 非后宫 布局天下 在读：103.5万 最近更新：第3945章 "
            "03 - 开局长生万古，苟到天荒地老 紫灵风雪 长生 系统 苟王 玄幻脑洞 在读：117.3万 最近更新：第1888章"
        )

        entries = module.parse_fanqie_ranking_entries(body)

        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0]["rank"], 1)
        self.assertEqual(entries[0]["title"], "天渊")
        self.assertIn("无系统", entries[0]["summary"])
        self.assertEqual(entries[1]["rank"], 2)
        self.assertEqual(entries[1]["author"], "一夕烟雨")
        self.assertEqual(entries[2]["rank"], 3)
        self.assertIn("长生", entries[2]["summary"])

    def test_parse_fanqie_ranking_entries_skips_date_noise(self) -> None:
        module = load_module()
        body = (
            "统计时间截止至 03-22 24:00 榜单说明 "
            "01 - 天渊 沐潇三生 无系统 传统玄幻 在读：106.2万 最近更新：2026-03-22 22:18 "
            "02 - 惊鸿 一夕烟雨 非后宫 布局天下 在读：103.5万 最近更新：2026-03-22 23:59 "
        )

        entries = module.parse_fanqie_ranking_entries(body)

        self.assertEqual(len(entries), 2)
        self.assertEqual([entry["rank"] for entry in entries], [1, 2])

    def test_parse_fanqie_ranking_entries_skips_obfuscated_items(self) -> None:
        module = load_module()
        body = (
            "统计时间截止至 03-22 24:00 榜单说明 "
            "01 - 渊 沐潇 系统 传统玄幻 在读：106.2万 最近更新：第2619章 "
            "02 - 惊鸿 一夕烟雨 传统玄幻 非后宫 布局天下 在读：103.5万 最近更新：第3945章 "
        )

        entries = module.parse_fanqie_ranking_entries(body)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["rank"], 2)
        self.assertEqual(entries[0]["title"], "惊鸿")

    def test_parse_fanqie_ranking_entries_keeps_partially_obfuscated_but_readable_item(self) -> None:
        module = load_module()
        body = (
            "统计时间截止至 03-22 24:00 榜单说明 "
            "01 - 惹枝 空留 权谋 高门 在读：55.6万 最近更新：第550章 "
        )

        entries = module.parse_fanqie_ranking_entries(body, allow_partial_sanitization=True)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["title"], "惹枝")
        self.assertEqual(entries[0]["author"], "空留")

    def test_report_only_writes_skeleton_when_no_sources_succeed(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(json.dumps({"meta": {"title": "Demo"}}))

            result = module.run_scan(
                project_root=project_root,
                platform="番茄",
                genre="玄幻",
                depth="quick",
                mode="report-only",
                acquire_fn=lambda url, **kwargs: {
                    "status": "failed",
                    "source_type": "none",
                    "title": None,
                    "body": None,
                    "source_url": url,
                    "final_url": None,
                    "failure_reason": "network_error",
                    "attempts": [],
                    "notes": [],
                    "fetched_at": "2026-03-23T00:00:00Z",
                    "duration_ms": 10,
                },
                timestamp="2026-03-23T00:00:00Z",
            )

            self.assertEqual(result["mode"], "report-only")
            self.assertEqual(result["report_kind"], "skeleton")
            self.assertEqual(result["confidence"]["overall"], "low")
            self.assertTrue((mighty / "market-data.json").exists())
            self.assertFalse((mighty / "market-adjustments.json").exists())

    def test_project_annotate_writes_sidecar_and_state_summary(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(json.dumps({"meta": {"title": "Demo"}}))

            def fake_acquire(url: str, **kwargs):
                if url.endswith("1_2_258"):
                    body = (
                        "统计时间截止至 03-22 24:00 榜单说明 "
                        "01 - 天渊 沐潇三生 主角腹黑 无系统 幽默 传统玄幻 在读：106.2万 最近更新：第2619章 "
                        "02 - 惊鸿 一夕烟雨 传统玄幻 非后宫 布局天下 在读：103.5万 最近更新：第3945章 "
                    )
                elif url.endswith("1_1_258"):
                    body = (
                        "统计时间截止至 03-22 24:00 榜单说明 "
                        "01 - 无耻老登，强当岳父 半壶墨 退婚 高概念 传统玄幻 在读：22.5万 最近更新：第88章 "
                        "02 - 命格坐享其成，开局弟弟被退婚 作者乙 命格 开局 规则收益 传统玄幻 在读：12.7万 最近更新：第21章 "
                    )
                elif url.endswith("1_2_257"):
                    body = (
                        "统计时间截止至 03-22 24:00 榜单说明 "
                        "01 - 开局长生万古，苟到天荒地老 紫灵风雪 长生 系统 苟王 玄幻脑洞 在读：117.3万 最近更新：第1888章 "
                        "02 - 系统赋我长生，我熬死了所有人 作者丙 长生 系统 玄幻脑洞 在读：108.3万 最近更新：第1666章 "
                    )
                elif url.endswith("1_1_257"):
                    body = (
                        "统计时间截止至 03-22 24:00 榜单说明 "
                        "01 - 无敌镖人，开局护送灭世帝女！ 乌鸦不喝水水 开局 词条 无敌 玄幻脑洞 在读：111.9万 最近更新：第77章 "
                        "02 - 莫欺老年穷：一天涨一年功力！ 作者丁 老年穷 高概念 玄幻脑洞 在读：58.4万 最近更新：第36章 "
                    )
                else:
                    body = "番茄 官方 榜单 传统玄幻 玄幻脑洞 新书榜 阅读榜"
                return {
                    "status": "success",
                    "source_type": "fetch_mcp",
                    "title": "官方榜单页",
                    "body": body + (" 样本" * 40),
                    "source_url": url,
                    "final_url": url,
                    "failure_reason": None,
                    "attempts": [],
                    "notes": ["fake"],
                    "fetched_at": "2026-03-23T00:00:00Z",
                    "duration_ms": 10,
                }

            result = module.run_scan(
                project_root=project_root,
                platform="番茄",
                genre="玄幻",
                depth="quick",
                mode="project-annotate",
                acquire_fn=fake_acquire,
                timestamp="2026-03-23T00:00:00Z",
            )

            self.assertEqual(result["report_kind"], "real_report")
            self.assertEqual(result["confidence"]["overall"], "medium")
            self.assertGreaterEqual(len(result["findings"]["hot_genres"]), 2)
            self.assertGreaterEqual(len(result["findings"]["hot_tags"]), 2)
            self.assertGreaterEqual(len(result["findings"]["opening_patterns"]), 1)
            self.assertGreaterEqual(len(result["findings"]["cool_point_patterns"]), 1)
            self.assertGreaterEqual(len(result["findings"]["recommended_content_buckets"]), 1)
            recommendation_types = {item["type"] for item in result["apply_recommendations"]}
            self.assertIn("manual_review", recommendation_types)
            self.assertIn("hook_design", recommendation_types)
            self.assertIn("payoff_design", recommendation_types)
            sidecar = json.loads((mighty / "market-adjustments.json").read_text())
            self.assertIn("source_scan", sidecar)
            self.assertIn("adjustments", sidecar)
            adjustment_ids = {item["id"] for item in sidecar["adjustments"]}
            self.assertIn("scan-manual-review-first", adjustment_ids)
            self.assertIn("scan-surface-hook", adjustment_ids)
            self.assertIn("scan-frontload-payoff", adjustment_ids)

            state = json.loads((mighty / "state.json").read_text())
            self.assertIn("market_adjustments", state)
            self.assertEqual(state["market_adjustments"]["source_scan"]["mode"], "project-annotate")

    def test_project_annotate_does_not_write_adjustments_for_low_confidence_sources(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(json.dumps({"meta": {"title": "Demo"}}))

            result = module.run_scan(
                project_root=project_root,
                platform="",
                genre="",
                depth="quick",
                mode="project-annotate",
                source_urls=["https://example.com/source"],
                acquire_fn=lambda url, **kwargs: {
                    "status": "success",
                    "source_type": "direct_html",
                    "title": "Example",
                    "body": "正文样本 " * 80,
                    "source_url": url,
                    "final_url": url,
                    "failure_reason": None,
                    "attempts": [],
                    "notes": [],
                    "fetched_at": "2026-03-23T00:00:00Z",
                    "duration_ms": 10,
                },
                timestamp="2026-03-23T00:00:00Z",
            )

            self.assertEqual(result["report_kind"], "real_report")
            self.assertEqual(result["confidence"]["overall"], "low")
            self.assertFalse((mighty / "market-adjustments.json").exists())
            state = json.loads((mighty / "state.json").read_text())
            self.assertNotIn("market_adjustments", state)

    def test_report_only_clears_stale_market_adjustments(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(json.dumps({"meta": {"title": "Demo"}}))

            def official_success(url: str, **kwargs):
                return {
                    "status": "success",
                    "source_type": "fetch_mcp",
                    "title": "官方榜单页",
                    "body": "统计时间截止至 03-22 24:00 榜单说明 01 - 天渊 沐潇三生 无系统 传统玄幻 " + ("样本 " * 80),
                    "source_url": url,
                    "final_url": url,
                    "failure_reason": None,
                    "attempts": [],
                    "notes": [],
                    "fetched_at": "2026-03-23T00:00:00Z",
                    "duration_ms": 10,
                }

            module.run_scan(
                project_root=project_root,
                platform="番茄",
                genre="玄幻",
                depth="quick",
                mode="project-annotate",
                acquire_fn=official_success,
                timestamp="2026-03-23T00:00:00Z",
            )

            module.run_scan(
                project_root=project_root,
                platform="番茄",
                genre="玄幻",
                depth="quick",
                mode="report-only",
                acquire_fn=lambda url, **kwargs: {
                    "status": "failed",
                    "source_type": "none",
                    "title": None,
                    "body": None,
                    "source_url": url,
                    "final_url": None,
                    "failure_reason": "network_error",
                    "attempts": [],
                    "notes": [],
                    "fetched_at": "2026-03-23T00:00:01Z",
                    "duration_ms": 10,
                },
                timestamp="2026-03-23T00:00:01Z",
            )

            self.assertFalse((mighty / "market-adjustments.json").exists())
            state = json.loads((mighty / "state.json").read_text())
            self.assertNotIn("market_adjustments", state)

    def test_fanqie_sources_prefer_direct_html_acquisition(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(json.dumps({"meta": {"title": "Demo"}}))
            calls: list[tuple[str, str | None]] = []

            def fake_acquire(url: str, **kwargs):
                calls.append((url, kwargs.get("prefer_source")))
                return {
                    "status": "failed",
                    "source_type": "none",
                    "title": None,
                    "body": None,
                    "source_url": url,
                    "final_url": None,
                    "failure_reason": "network_error",
                    "attempts": [],
                    "notes": [],
                    "fetched_at": "2026-03-23T00:00:00Z",
                    "duration_ms": 10,
                }

            module.run_scan(
                project_root=project_root,
                platform="番茄",
                genre="玄幻",
                depth="quick",
                mode="report-only",
                acquire_fn=fake_acquire,
                timestamp="2026-03-23T00:00:00Z",
            )

            self.assertTrue(calls)
            self.assertTrue(all(prefer == "direct_html" for _, prefer in calls))

    def test_focus_excerpt_prefers_fanqie_ranking_content(self) -> None:
        module = load_module()
        body = (
            "番茄小说 帮助中心 作家助手 男频阅读榜 传统玄幻 玄幻脑洞 统计时间截止至 03-22 24:00 "
            "榜单说明 01 - 天渊 无系统 幽默 传统玄幻 在读：106.2万 "
            "02 - 惊鸿 非后宫 布局天下 "
        )
        excerpt = module.focus_excerpt(
            "https://fanqienovel.com/rank/1_2_258",
            body,
            limit=120,
        )

        self.assertIn("天渊", excerpt)
        self.assertNotIn("帮助中心", excerpt)

    def test_focus_excerpt_hides_obfuscated_fanqie_ranking_content(self) -> None:
        module = load_module()
        body = (
            "番茄小说 帮助中心 作家助手 男频阅读榜 传统玄幻 统计时间截止至 03-22 24:00 "
            "榜单说明 01 - 渊 沐潇 系统 传统玄幻 在读：106.2万 "
        )

        excerpt = module.focus_excerpt(
            "https://fanqienovel.com/rank/1_2_258",
            body,
            limit=120,
        )

        self.assertEqual(excerpt, "")

    def test_focus_excerpt_keeps_sanitized_readable_content(self) -> None:
        module = load_module()
        body = (
            "番茄小说 帮助中心 作家助手 女频阅读榜 统计时间截止至 03-22 24:00 "
            "榜单说明 01 - 惹枝 空留 权谋 高门 在读：55.6万 "
        )

        excerpt = module.focus_excerpt(
            "https://fanqienovel.com/rank/0_2_1139",
            body,
            limit=120,
            allow_partial_sanitization=True,
        )

        self.assertIn("惹枝", excerpt)
        self.assertNotIn("帮助中心", excerpt)

    def test_total_rank_page_does_not_pollute_tag_inference(self) -> None:
        module = load_module()
        sources = [
            {
                "name": "番茄小说排行榜总页",
                "title": "小说排行榜_番茄小说官网",
                "excerpt": "01 - 早知道不这么玩了 无系统 修罗场 龙与史诗",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "早知道不这么玩了", "author": "作者甲", "summary": "无系统 修罗场 龙与史诗"}
                ],
            },
            {
                "name": "番茄传统玄幻阅读榜",
                "title": "小说排行榜_番茄小说官网",
                "excerpt": "01 - 天渊 沐潇三生 无系统 传统玄幻",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "天渊", "author": "沐潇三生", "summary": "无系统 传统玄幻"}
                ],
            },
        ]

        hot_tags = module.infer_hot_tags(sources)
        self.assertEqual(len(hot_tags), 1)
        self.assertEqual(hot_tags[0]["tag"], "苟道/无系统")
        self.assertEqual(hot_tags[0]["evidence_titles"], ["番茄传统玄幻阅读榜"])

    def test_total_rank_page_query_variant_does_not_pollute_tag_inference(self) -> None:
        module = load_module()
        sources = [
            {
                "name": "显式总榜 URL",
                "url": "https://fanqienovel.com/rank/1?foo=bar",
                "title": "小说排行榜_番茄小说官网",
                "excerpt": "01 - 早知道不这么玩了 无系统 修罗场 龙与史诗",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "早知道不这么玩了", "author": "作者甲", "summary": "无系统 修罗场 龙与史诗"}
                ],
            },
            {
                "name": "番茄传统玄幻阅读榜",
                "url": "https://fanqienovel.com/rank/1_2_258",
                "title": "小说排行榜_番茄小说官网",
                "excerpt": "01 - 天渊 沐潇三生 无系统 传统玄幻",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "天渊", "author": "沐潇三生", "summary": "无系统 传统玄幻"}
                ],
            },
        ]

        hot_tags = module.infer_hot_tags(sources)
        self.assertEqual(len(hot_tags), 1)
        self.assertEqual(hot_tags[0]["tag"], "苟道/无系统")
        self.assertEqual(hot_tags[0]["evidence_titles"], ["番茄传统玄幻阅读榜"])

    def test_decode_fanqie_obfuscated_body_uses_reference_font_when_available(self) -> None:
        module = load_module()

        decoded = module.decode_fanqie_obfuscated_body(
            body="渊 沐潇 系统",
            notes=["font_url:https://example.com/demo-font.woff2"],
            reference_font_path=Path("/tmp/SourceHanSansSC-Regular.otf"),
            download_font_fn=lambda url: Path("/tmp/demo-font.woff2"),
            suggest_mapping_fn=lambda subset_font_path, reference_font_path, sample_text, reference_font_number=None: {
                "": "天",
                "": "三",
                "": "生",
                "": "无",
            },
        )

        self.assertEqual(decoded, "天渊 沐潇三生 无系统")

    def test_decode_fanqie_obfuscated_body_skips_without_font_url_note(self) -> None:
        module = load_module()

        decoded = module.decode_fanqie_obfuscated_body(
            body="渊 沐潇 系统",
            notes=[],
            reference_font_path=Path("/tmp/SourceHanSansSC-Regular.otf"),
        )

        self.assertEqual(decoded, "渊 沐潇 系统")

    def test_keyword_frequency_uses_top_entries_window(self) -> None:
        module = load_module()
        source = {
            "name": "番茄玄幻脑洞阅读榜",
            "url": "https://fanqienovel.com/rank/1_2_257",
            "status": "success",
            "trust_level": "A",
            "ranking_entries": [
                {"rank": 1, "title": "开局长生万古", "author": "作者甲", "summary": "长生 系统 苟王"},
                {"rank": 2, "title": "系统赋我长生", "author": "作者乙", "summary": "长生 系统"},
                {"rank": 3, "title": "误认大帝", "author": "作者丙", "summary": "误认 高概念"},
                {"rank": 4, "title": "后排样本", "author": "作者丁", "summary": "退婚 词条"},
            ],
        }

        freq = module.collect_keyword_frequency([source], top_n=3)

        self.assertEqual(freq["长生"], 2)
        self.assertEqual(freq["系统"], 2)
        self.assertEqual(freq["误认"], 1)
        self.assertNotIn("退婚", freq)

    def test_hot_tags_use_frequency_thresholds(self) -> None:
        module = load_module()
        sources = [
            {
                "name": "番茄传统玄幻新书榜",
                "url": "https://fanqienovel.com/rank/1_1_258",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "命格坐享其成", "author": "作者甲", "summary": "命格 开局 规则收益"},
                    {"rank": 2, "title": "弟弟被退婚", "author": "作者乙", "summary": "退婚 高概念"},
                    {"rank": 3, "title": "长生大帝", "author": "作者丙", "summary": "长生 误认大帝"},
                ],
                "excerpt": "",
                "title": "小说排行榜_番茄小说官网",
            },
            {
                "name": "番茄玄幻脑洞阅读榜",
                "url": "https://fanqienovel.com/rank/1_2_257",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "开局长生万古", "author": "作者丁", "summary": "长生 系统 苟王"},
                    {"rank": 2, "title": "系统赋我长生", "author": "作者戊", "summary": "长生 系统"},
                    {"rank": 3, "title": "无敌镖人", "author": "作者己", "summary": "开局 词条 无敌"},
                ],
                "excerpt": "",
                "title": "小说排行榜_番茄小说官网",
            },
        ]

        hot_tags = module.infer_hot_tags(sources)
        tags = {item["tag"] for item in hot_tags}

        self.assertIn("长生", tags)
        self.assertIn("系统/命格/词条", tags)
        self.assertIn("身份反差/退婚", tags)

    def test_new_book_list_uses_more_sensitive_thresholds(self) -> None:
        module = load_module()
        sources = [
            {
                "name": "番茄传统玄幻新书榜",
                "url": "https://fanqienovel.com/rank/1_1_258",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "无耻老登，强当岳父", "author": "作者甲", "summary": "老登 高概念"},
                    {"rank": 2, "title": "普通条目", "author": "作者乙", "summary": "传统玄幻"},
                ],
                "excerpt": "",
                "title": "小说排行榜_番茄小说官网",
            }
        ]

        hot_tags = module.infer_hot_tags(sources)
        tags = {item["tag"] for item in hot_tags}

        self.assertIn("身份反差/退婚", tags)

    def test_palace_intrigue_tags_and_patterns_can_be_inferred(self) -> None:
        module = load_module()
        sources = [
            {
                "name": "番茄宫斗宅斗阅读榜",
                "url": "https://fanqienovel.com/rank/0_2_246",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "掌家", "author": "作者甲", "summary": "嫡女 家权 反击陷害"},
                    {"rank": 2, "title": "后宅风云", "author": "作者乙", "summary": "掌家 对手试探 嫡庶"},
                    {"rank": 3, "title": "权门", "author": "作者丙", "summary": "家权 族谱 对手反制"},
                ],
                "excerpt": "",
                "title": "小说排行榜_番茄小说官网",
            },
            {
                "name": "番茄宫斗宅斗新书榜",
                "url": "https://fanqienovel.com/rank/0_1_246",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "重生归来", "author": "作者丁", "summary": "重生复仇 当场反击"},
                    {"rank": 2, "title": "嫡女改命", "author": "作者戊", "summary": "嫡女 继母陷害 打脸"},
                ],
                "excerpt": "",
                "title": "小说排行榜_番茄小说官网",
            },
            {
                "name": "番茄古风世情新书榜",
                "url": "https://fanqienovel.com/rank/0_1_1139",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "和嫡姐进错婚房", "author": "作者己", "summary": "错婚房 权臣 先婚后爱"},
                    {"rank": 2, "title": "侯府和离", "author": "作者庚", "summary": "和离 高门婚配 赐婚"},
                ],
                "excerpt": "",
                "title": "小说排行榜_番茄小说官网",
            },
        ]

        hot_tags = module.infer_hot_tags(sources)
        tags = {item["tag"] for item in hot_tags}
        self.assertIn("嫡庶/家权", tags)
        self.assertIn("反击陷害", tags)
        self.assertIn("重生复仇", tags)
        self.assertIn("高门婚配/权臣拉扯", tags)

        patterns = {item["pattern"] for item in module.infer_opening_patterns(sources)}
        self.assertIn("开篇先立压迫位阶", patterns)
        self.assertIn("婚配冲突先落地", patterns)

        cool_points = {item["pattern"] for item in module.infer_cool_point_patterns(sources)}
        self.assertIn("反击陷害当场兑现", cool_points)
        self.assertIn("高门婚配制造拉扯", cool_points)

    def test_palace_findings_generate_market_adjustments(self) -> None:
        module = load_module()
        payload = {
            "scan_time": "2026-03-23T00:00:00Z",
            "mode": "project-annotate",
            "report_kind": "real_report",
            "targets": {"platforms": ["番茄"], "genre": "宫斗宅斗", "depth": "quick"},
            "confidence": {"overall": "medium", "reason": "test"},
            "sources": [{"url": "https://fanqienovel.com/rank/0_2_246", "status": "success"}],
            "findings": {
                "hot_tags": [
                    {"tag": "高门婚配/权臣拉扯", "signal": "", "evidence_titles": ["番茄古风世情新书榜"]},
                    {"tag": "反击陷害", "signal": "", "evidence_titles": ["番茄宫斗宅斗阅读榜"]},
                ],
                "opening_patterns": [
                    {"pattern": "婚配冲突先落地", "detail": "", "confidence": "medium"},
                    {"pattern": "先压后反击", "detail": "", "confidence": "medium"},
                ],
                "cool_point_patterns": [],
            },
        }

        rec_types = {item["type"] for item in module.build_apply_recommendations_from_findings(payload)}
        self.assertIn("hook_design", rec_types)
        self.assertIn("conflict_design", rec_types)
        self.assertIn("truth_consistency", rec_types)

        adjustment_ids = {item["id"] for item in module.build_adjustments(payload)["adjustments"]}
        self.assertIn("scan-surface-hook", adjustment_ids)
        self.assertIn("scan-frontload-conflict", adjustment_ids)
        self.assertIn("scan-kinship-truth-check", adjustment_ids)

    def test_build_research_candidates_extracts_truth_gap_candidate(self) -> None:
        module = load_module()
        payload = {
            "scan_time": "2026-03-23T00:00:00Z",
            "mode": "project-annotate",
            "report_kind": "real_report",
            "targets": {"platforms": ["番茄"], "genre": "宫斗宅斗", "depth": "quick"},
            "confidence": {"overall": "medium", "reason": "test"},
            "sources": [
                {
                    "url": "https://fanqienovel.com/rank/0_2_246",
                    "status": "success",
                    "source_type": "fetch_mcp",
                }
            ],
            "findings": {
                "hot_tags": [
                    {"tag": "高门婚配/权臣拉扯", "signal": "", "evidence_titles": ["番茄古风世情新书榜"]},
                ],
                "opening_patterns": [
                    {"pattern": "婚配冲突先落地", "detail": "", "confidence": "medium"},
                ],
                "cool_point_patterns": [],
            },
            "apply_recommendations": [
                {
                    "type": "truth_consistency",
                    "suggestion": "先补齐嫡庶、齿序、婚配与家权真值。",
                    "confidence": "medium",
                    "note": "test",
                }
            ],
        }

        candidates_doc = module.build_research_candidates(payload)

        self.assertEqual(candidates_doc["source_scan"]["tool"], "novel-scan")
        self.assertEqual(len(candidates_doc["candidates"]), 1)
        self.assertEqual(candidates_doc["candidates"][0]["kind"], "rule")
        self.assertEqual(candidates_doc["candidates"][0]["source"], "mcp")

    def test_run_scan_can_emit_research_candidates_file(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "project"
            mighty = project_root / ".mighty"
            mighty.mkdir(parents=True)
            (mighty / "state.json").write_text(json.dumps({"meta": {"title": "Demo"}}))

            def fake_acquire(url: str, **kwargs):
                if url.endswith("0_2_246"):
                    body = (
                        "统计时间截止至 03-22 24:00 榜单说明 "
                        "01 - 掌家 作者甲 嫡女 家权 反击陷害 "
                        "02 - 后宅风云 作者乙 掌家 对手试探 嫡庶 "
                    )
                elif url.endswith("0_1_246"):
                    body = (
                        "统计时间截止至 03-22 24:00 榜单说明 "
                        "01 - 重生归来 作者丁 重生复仇 当场反击 "
                        "02 - 嫡女改命 作者戊 嫡女 继母陷害 打脸 "
                    )
                else:
                    body = (
                        "统计时间截止至 03-22 24:00 榜单说明 "
                        "01 - 和嫡姐进错婚房 作者己 错婚房 权臣 先婚后爱 "
                        "02 - 侯府和离 作者庚 和离 高门婚配 赐婚 "
                    )
                return {
                    "status": "success",
                    "source_type": "fetch_mcp",
                    "title": "官方榜单页",
                    "body": body + (" 样本" * 40),
                    "source_url": url,
                    "final_url": url,
                    "failure_reason": None,
                    "attempts": [],
                    "notes": [],
                    "fetched_at": "2026-03-23T00:00:00Z",
                    "duration_ms": 10,
                }

            module.run_scan(
                project_root=project_root,
                platform="番茄",
                genre="宫斗宅斗",
                depth="quick",
                mode="project-annotate",
                acquire_fn=fake_acquire,
                timestamp="2026-03-23T00:00:00Z",
                emit_research_candidates=True,
            )

            candidates_doc = json.loads((mighty / "research-candidates.json").read_text(encoding="utf-8"))
            self.assertEqual(candidates_doc["source_scan"]["tool"], "novel-scan")
            self.assertEqual(len(candidates_doc["candidates"]), 1)
            self.assertEqual(candidates_doc["candidates"][0]["name"], "嫡庶婚配真值补证")

    def test_reading_list_keeps_stricter_thresholds(self) -> None:
        module = load_module()
        sources = [
            {
                "name": "番茄传统玄幻阅读榜",
                "url": "https://fanqienovel.com/rank/1_2_258",
                "status": "success",
                "trust_level": "A",
                "ranking_entries": [
                    {"rank": 1, "title": "单条误认样本", "author": "作者甲", "summary": "误认大帝"},
                    {"rank": 2, "title": "普通条目", "author": "作者乙", "summary": "传统玄幻"},
                    {"rank": 3, "title": "另一个普通条目", "author": "作者丙", "summary": "宗门修炼"},
                ],
                "excerpt": "",
                "title": "小说排行榜_番茄小说官网",
            }
        ]

        hot_tags = module.infer_hot_tags(sources)
        tags = {item["tag"] for item in hot_tags}

        self.assertNotIn("身份反差/退婚", tags)


if __name__ == "__main__":
    unittest.main()
