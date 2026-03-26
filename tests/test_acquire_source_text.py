from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "acquire_source_text.py"


def load_module():
    spec = importlib.util.spec_from_file_location("acquire_source_text", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def long_html(title: str, phrase: str = "正文") -> str:
    body = phrase * 220
    return f"<html><head><title>{title}</title></head><body><main><p>{body}</p></main></body></html>"


class AcquireSourceTextTests(unittest.TestCase):
    def test_retrievable_url_result_is_usable_for_learning(self) -> None:
        module = load_module()

        result = module.acquire_article(
            "https://example.com/post",
            fetch_provider=lambda url, timeout_ms: module.StageResult.ok_result(
                title="Example Source",
                body="正文学习样本" * 120,
                final_url=url,
            ),
            min_body_chars=300,
        )

        self.assertEqual(result.status, "success")
        self.assertEqual(result.source_type, "fetch_mcp")
        self.assertEqual(result.title, "Example Source")
        self.assertGreater(len(result.body or ""), 300)
        self.assertEqual(result.source_url, "https://example.com/post")
        self.assertEqual(result.final_url, "https://example.com/post")

    def test_reader_proxy_provider_parses_markdown_response(self) -> None:
        module = load_module()

        captured_urls: list[str] = []

        def fake_fetch_text(url: str, timeout_ms: int, *, accept: str):
            captured_urls.append(url)
            return (
                "Title: Proxy Title\n\nURL Source: https://example.com/post\n\nMarkdown Content:\n正文内容" + ("甲" * 400),
                "https://r.jina.ai/http://example.com/post",
            )

        provider = module.reader_proxy_provider(fetch_text_fn=fake_fetch_text)
        result = provider("https://example.com/post", 12000)

        self.assertIsNone(result.failure_reason)
        self.assertEqual(result.title, "Proxy Title")
        self.assertIn("正文内容", result.body)
        self.assertEqual(result.final_url, "https://example.com/post")
        self.assertEqual(captured_urls, ["https://r.jina.ai/http://example.com/post"])

    def test_bing_rss_provider_parses_first_item(self) -> None:
        module = load_module()
        captured_urls: list[str] = []

        def fake_fetch_text(url: str, timeout_ms: int, *, accept: str):
            captured_urls.append(url)
            return (
                """<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0">
  <channel>
    <title>必应：example.com</title>
    <item>
      <title>Example Domain</title>
      <link>https://example.com/</link>
      <description>Example Domain summary body</description>
    </item>
  </channel>
</rss>""",
                url,
            )

        provider = module.bing_rss_search_provider(fetch_text_fn=fake_fetch_text)
        result = provider("https://example.com/post", 12000)

        self.assertIsNone(result.failure_reason)
        self.assertEqual(result.title, "Example Domain")
        self.assertEqual(result.final_url, "https://example.com/")
        self.assertIn("summary body", result.body)
        self.assertEqual(
            captured_urls,
            ["https://www.bing.com/search?format=rss&q=https%3A%2F%2Fexample.com%2Fpost"],
        )

    def test_bing_rss_provider_prefers_same_host_result(self) -> None:
        module = load_module()

        def fake_fetch_text(url: str, timeout_ms: int, *, accept: str):
            return (
                """<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0">
  <channel>
    <item>
      <title>Unrelated Result</title>
      <link>https://www.zhihu.com/question/1</link>
      <description>Not the same host.</description>
    </item>
    <item>
      <title>Example Domain Real</title>
      <link>https://example.com/article</link>
      <description>Same host summary.</description>
    </item>
  </channel>
</rss>""",
                url,
            )

        provider = module.bing_rss_search_provider(fetch_text_fn=fake_fetch_text)
        result = provider("https://example.com/post", 12000)

        self.assertIsNone(result.failure_reason)
        self.assertEqual(result.title, "Example Domain Real")
        self.assertEqual(result.final_url, "https://example.com/article")

    def test_bing_rss_provider_rejects_irrelevant_host_results(self) -> None:
        module = load_module()

        def fake_fetch_text(url: str, timeout_ms: int, *, accept: str):
            return (
                """<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0">
  <channel>
    <item>
      <title>Unrelated Result</title>
      <link>https://www.zhihu.com/question/1</link>
      <description>Not the same host.</description>
    </item>
  </channel>
</rss>""",
                url,
            )

        provider = module.bing_rss_search_provider(fetch_text_fn=fake_fetch_text)
        result = provider("https://example.com/post", 12000)

        self.assertEqual(result.failure_reason, "extract_failed")

    def test_bing_rss_provider_rejects_same_host_but_wrong_path(self) -> None:
        module = load_module()

        def fake_fetch_text(url: str, timeout_ms: int, *, accept: str):
            return (
                """<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0">
  <channel>
    <item>
      <title>Wrong Zhihu Question</title>
      <link>https://www.zhihu.com/question/19577317</link>
      <description>Same host but wrong question id.</description>
    </item>
  </channel>
</rss>""",
                url,
            )

        provider = module.bing_rss_search_provider(fetch_text_fn=fake_fetch_text)
        result = provider("https://www.zhihu.com/question/29998374", 12000)

        self.assertEqual(result.failure_reason, "extract_failed")

    def test_fetch_mcp_success_short_circuits_fallbacks(self) -> None:
        module = load_module()
        html_calls: list[str] = []
        search_calls: list[str] = []

        def fetch_provider(url: str, timeout_ms: int):
            return module.StageResult.ok_result(
                title="Fetch Title",
                body="A" * 400,
                final_url=url,
                notes=["fetch hit"],
            )

        def html_fetcher(url: str, timeout_ms: int):
            html_calls.append(url)
            return ""

        def search_provider(url: str, timeout_ms: int):
            search_calls.append(url)
            return module.StageResult.failed("search_only")

        result = module.acquire_article(
            "https://allowed.example/post",
            fetch_provider=fetch_provider,
            html_fetcher=html_fetcher,
            search_provider=search_provider,
            min_body_chars=300,
        )

        self.assertEqual(result.status, "success")
        self.assertEqual(result.source_type, "fetch_mcp")
        self.assertEqual(result.title, "Fetch Title")
        self.assertEqual(result.failure_reason, None)
        self.assertEqual(len(result.attempts), 1)
        self.assertFalse(html_calls)
        self.assertFalse(search_calls)

    def test_robots_block_falls_back_to_html_extract(self) -> None:
        module = load_module()

        def fetch_provider(url: str, timeout_ms: int):
            return module.StageResult.failed("robots", notes=["robots denied"])

        result = module.acquire_article(
            "https://blocked.example/article",
            fetch_provider=fetch_provider,
            html_fetcher=lambda url, timeout_ms: long_html("HTML Title", "段落"),
            min_body_chars=300,
        )

        self.assertEqual(result.status, "success")
        self.assertEqual(result.source_type, "html_extract")
        self.assertEqual(result.title, "HTML Title")
        self.assertEqual(result.failure_reason, None)
        self.assertEqual([attempt.stage for attempt in result.attempts], ["fetch_mcp", "direct_html"])
        self.assertFalse(result.attempts[0].ok)
        self.assertEqual(result.attempts[0].reason, "robots")
        self.assertTrue(result.attempts[1].ok)

    def test_extract_html_stage_captures_fanqie_font_url_note(self) -> None:
        module = load_module()
        html = """
<html>
  <head>
    <style>
      @font-face{
        font-family:DNMrHsV173Pd4pgy;
        src:url(https://lf6-awef.bytetos.com/obj/awesome-font/c/demo-font.woff2) format("woff2");
      }
    </style>
    <title>番茄榜单</title>
  </head>
  <body>
    <main><p>渊 沐潇 系统</p></main>
  </body>
</html>
"""

        result = module.extract_html_stage(
            html,
            final_url="https://fanqienovel.com/rank/1_2_258",
            min_body_chars=3,
        )

        self.assertIsNone(result.failure_reason)
        self.assertIn("font_url:https://lf6-awef.bytetos.com/obj/awesome-font/c/demo-font.woff2", result.notes)

    def test_search_fallback_returns_partial_result(self) -> None:
        module = load_module()

        def fetch_provider(url: str, timeout_ms: int):
            return module.StageResult.failed("tool_unavailable")

        def search_provider(url: str, timeout_ms: int):
            return module.StageResult.ok_result(
                title="Search Snippet",
                body="摘要内容" * 20,
                final_url=url,
                notes=["search fallback"],
            )

        result = module.acquire_article(
            "https://unknown.example/article",
            fetch_provider=fetch_provider,
            html_fetcher=lambda url, timeout_ms: "<html><head><title>Thin</title></head><body><p>太短</p></body></html>",
            search_provider=search_provider,
            min_body_chars=200,
        )

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.source_type, "search_fallback")
        self.assertEqual(result.title, "Search Snippet")
        self.assertEqual(result.failure_reason, "search_only")
        self.assertEqual([attempt.stage for attempt in result.attempts], ["fetch_mcp", "direct_html", "search_fallback"])
        self.assertTrue(result.attempts[2].ok)

    def test_domain_policy_skips_fetch_after_repeated_robots_failures(self) -> None:
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            policy_file = Path(tmpdir) / "policy.json"
            store = module.DomainPolicyStore(policy_file, robots_skip_threshold=3)

            for _ in range(3):
                result = module.acquire_article(
                    "https://robots.example/post",
                    fetch_provider=lambda url, timeout_ms: module.StageResult.failed("robots"),
                    html_fetcher=lambda url, timeout_ms: "<html><body><p>短</p></body></html>",
                    policy_store=store,
                    min_body_chars=50,
                )
                self.assertEqual(result.attempts[0].stage, "fetch_mcp")

            policy = store.get("robots.example")
            self.assertEqual(policy["fetch_mcp_mode"], "skip")
            self.assertEqual(policy["consecutive_failures"], 3)

            fetch_calls: list[str] = []

            def fetch_provider(url: str, timeout_ms: int):
                fetch_calls.append(url)
                return module.StageResult.failed("robots")

            result = module.acquire_article(
                "https://robots.example/post",
                fetch_provider=fetch_provider,
                html_fetcher=lambda url, timeout_ms: long_html("Skipped Fetch HTML"),
                policy_store=store,
                min_body_chars=300,
            )

            self.assertFalse(fetch_calls)
            self.assertEqual(result.status, "success")
            self.assertEqual(result.source_type, "html_extract")
            self.assertEqual([attempt.stage for attempt in result.attempts], ["direct_html"])
            self.assertTrue(any("skip" in note for note in result.notes))

    def test_partial_search_result_still_returns_body_for_learning_fallback(self) -> None:
        module = load_module()

        result = module.acquire_article(
            "https://unknown.example/article",
            fetch_provider=lambda url, timeout_ms: module.StageResult.failed("tool_unavailable"),
            html_fetcher=lambda url, timeout_ms: "<html><body><p>太短</p></body></html>",
            search_provider=lambda url, timeout_ms: module.StageResult.ok_result(
                title="Search Learning Fallback",
                body="摘要学习样本" * 120,
                final_url=url,
            ),
            min_body_chars=300,
        )

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.failure_reason, "search_only")
        self.assertEqual(result.title, "Search Learning Fallback")
        self.assertGreater(len(result.body or ""), 300)

    def test_provider_registry_defaults_are_reported_in_result(self) -> None:
        module = load_module()

        result = module.acquire_article(
            "https://example.com/post",
            fetch_provider=lambda url, timeout_ms: module.StageResult.ok_result(
                title="Example Source",
                body="正文学习样本" * 120,
                final_url=url,
            ),
            min_body_chars=300,
        )
        result.provider_trace = {
            "fetch": {"name": "reader_proxy", "source": "registry_default"},
            "search": {"name": "bing_rss", "source": "registry_default"},
        }

        payload = result.to_dict()
        self.assertEqual(payload["provider_trace"]["fetch"]["name"], "reader_proxy")
        self.assertEqual(payload["provider_trace"]["search"]["name"], "bing_rss")

    def test_project_config_can_resolve_provider_presets(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            config_path = project_root / ".mighty" / "config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                json.dumps(
                    {
                        "acquire_source_text": {
                            "fetch_provider": {"preset": "reader_proxy"},
                            "search_provider": {"preset": "bing_rss"},
                        }
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            registry = module.load_provider_registry(module.default_provider_registry_path())
            fetch_provider, fetch_trace = module.resolve_provider_settings(
                role="fetch",
                cli_command="",
                env_command="",
                project_root=str(project_root),
                registry=registry,
            )
            search_provider, search_trace = module.resolve_provider_settings(
                role="search",
                cli_command="",
                env_command="",
                project_root=str(project_root),
                registry=registry,
            )

            self.assertIsNotNone(fetch_provider)
            self.assertIsNotNone(search_provider)
            self.assertEqual(fetch_trace["source"], "project_config")
            self.assertEqual(fetch_trace["name"], "reader_proxy")
            self.assertEqual(search_trace["source"], "project_config")
            self.assertEqual(search_trace["name"], "bing_rss")

    def test_cli_fetch_command_overrides_project_config(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            config_path = project_root / ".mighty" / "config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                json.dumps(
                    {
                        "acquire_source_text": {
                            "fetch_provider": {"preset": "reader_proxy"},
                        }
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            registry = module.load_provider_registry(module.default_provider_registry_path())
            provider, trace = module.resolve_provider_settings(
                role="fetch",
                cli_command="python3 -c \"import json; print(json.dumps({'status':'success','title':'T','body':'B'*400}))\"",
                env_command="",
                project_root=str(project_root),
                registry=registry,
            )

            self.assertIsNotNone(provider)
            self.assertEqual(trace["source"], "cli")
            self.assertEqual(trace["kind"], "external_command")


if __name__ == "__main__":
    unittest.main()
