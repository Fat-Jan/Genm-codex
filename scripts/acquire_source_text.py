#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import time
import tomllib
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen


FailureReason = str
FetchProvider = Callable[[str, int], "StageResult"]
HTMLFetcher = Callable[[str, int], str | tuple[str, str | None]]
FetchTextFn = Callable[[str, int], tuple[str, str | None]]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_text(value: str) -> str:
    lines = [re.sub(r"\s+", " ", line).strip() for line in value.splitlines()]
    cleaned = [line for line in lines if line]
    return "\n\n".join(cleaned)


def body_length(value: str | None) -> int:
    if not value:
        return 0
    return len(re.sub(r"\s+", "", value))


def extract_font_face_urls(html: str) -> list[str]:
    return re.findall(r"@font-face\s*\{.*?src:url\((https?://[^)]+)\)", html, flags=re.IGNORECASE | re.DOTALL)


def pick_first(*values: str | None) -> str | None:
    for value in values:
        if value:
            return value
    return None


def canonical_reason(value: str | None, *, default: FailureReason = "unknown") -> FailureReason:
    if not value:
        return default
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    mapping = {
        "blocked_by_robots": "robots",
        "robots_txt": "robots",
        "tool_unavailable": "tool_unavailable",
        "install_error": "install_error",
        "timeout": "timeout",
        "network_error": "network_error",
        "empty_body": "empty_body",
        "extract_failed": "extract_failed",
        "search_only": "search_only",
        "unknown": "unknown",
        "robots": "robots",
    }
    return mapping.get(normalized, default)


@dataclass
class AttemptRecord:
    stage: str
    ok: bool
    duration_ms: int
    reason: str | None = None


@dataclass
class StageResult:
    title: str | None = None
    body: str | None = None
    final_url: str | None = None
    failure_reason: FailureReason | None = None
    notes: list[str] = field(default_factory=list)

    @classmethod
    def ok_result(
        cls,
        *,
        title: str | None = None,
        body: str | None = None,
        final_url: str | None = None,
        notes: list[str] | None = None,
    ) -> "StageResult":
        return cls(
            title=title,
            body=body,
            final_url=final_url,
            failure_reason=None,
            notes=list(notes or []),
        )

    @classmethod
    def failed(
        cls,
        reason: FailureReason,
        *,
        title: str | None = None,
        body: str | None = None,
        final_url: str | None = None,
        notes: list[str] | None = None,
    ) -> "StageResult":
        return cls(
            title=title,
            body=body,
            final_url=final_url,
            failure_reason=canonical_reason(reason),
            notes=list(notes or []),
        )


@dataclass
class AcquireArticleResult:
    status: str
    source_type: str
    title: str | None
    body: str | None
    source_url: str
    final_url: str | None
    failure_reason: FailureReason | None
    attempts: list[AttemptRecord]
    notes: list[str]
    fetched_at: str
    duration_ms: int
    provider_trace: dict | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class DomainPolicyStore:
    def __init__(self, path: Path, robots_skip_threshold: int = 3) -> None:
        self.path = path
        self.robots_skip_threshold = robots_skip_threshold
        self._loaded = False
        self._data: dict[str, dict] = {}

    def _load(self) -> None:
        if self._loaded:
            return
        if self.path.exists():
            self._data = json.loads(self.path.read_text())
        self._loaded = True

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2))

    def get(self, domain: str) -> dict:
        self._load()
        existing = self._data.get(domain)
        if existing:
            return dict(existing)
        return {
            "domain": domain,
            "fetch_mcp_mode": "normal",
            "last_failure_reason": None,
            "last_success_at": None,
            "consecutive_failures": 0,
        }

    def should_skip_fetch(self, domain: str) -> bool:
        return self.get(domain)["fetch_mcp_mode"] == "skip"

    def record_fetch_success(self, domain: str, *, timestamp: str | None = None) -> None:
        self._load()
        payload = self.get(domain)
        payload["fetch_mcp_mode"] = "normal"
        payload["last_failure_reason"] = None
        payload["last_success_at"] = timestamp or now_iso()
        payload["consecutive_failures"] = 0
        self._data[domain] = payload
        self._save()

    def record_fetch_failure(self, domain: str, reason: FailureReason) -> None:
        self._load()
        payload = self.get(domain)
        payload["last_failure_reason"] = reason
        if reason == "robots":
            payload["consecutive_failures"] = int(payload.get("consecutive_failures") or 0) + 1
            if payload["consecutive_failures"] >= self.robots_skip_threshold:
                payload["fetch_mcp_mode"] = "skip"
        else:
            payload["consecutive_failures"] = int(payload.get("consecutive_failures") or 0)
        self._data[domain] = payload
        self._save()


class _ReadableHTMLParser(HTMLParser):
    BLOCK_TAGS = {"p", "article", "main", "section", "div", "li", "blockquote", "h1", "h2", "h3", "h4", "pre"}
    SKIP_TAGS = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.title_parts: list[str] = []
        self.meta_description: str | None = None
        self.article_chunks: list[str] = []
        self.body_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self.stack.append(tag)
        if tag != "meta":
            return
        attr_map = {key.lower(): value for key, value in attrs}
        name = (attr_map.get("name") or attr_map.get("property") or "").lower()
        if name not in {"description", "og:description", "twitter:description"}:
            return
        content = normalize_text(attr_map.get("content") or "")
        if content and not self.meta_description:
            self.meta_description = content

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index] == tag:
                del self.stack[index]
                break

    def handle_data(self, data: str) -> None:
        if any(tag in self.SKIP_TAGS for tag in self.stack):
            return
        text = normalize_text(data)
        if not text:
            return
        if self.stack and self.stack[-1] == "title":
            self.title_parts.append(text)
            return
        target = self.article_chunks if any(tag in {"article", "main"} for tag in self.stack) else self.body_chunks
        if any(tag in self.BLOCK_TAGS for tag in self.stack):
            target.append(text)

    def best_title(self) -> str | None:
        title = normalize_text(" ".join(self.title_parts))
        return title or None

    def best_body(self) -> str:
        article = normalize_text("\n".join(self.article_chunks))
        if article:
            return article
        return normalize_text("\n".join(self.body_chunks))


def extract_html_stage(html: str, *, final_url: str | None, min_body_chars: int) -> StageResult:
    parser = _ReadableHTMLParser()
    parser.feed(html)
    body = parser.best_body()
    title = parser.best_title()
    notes: list[str] = []
    if parser.meta_description:
        notes.append("html metadata description captured")
    final_host = urlparse(final_url or "").netloc.lower()
    if final_host.endswith("fanqienovel.com"):
        for font_url in extract_font_face_urls(html)[:1]:
            notes.append(f"font_url:{font_url}")
    if body_length(body) >= min_body_chars:
        return StageResult.ok_result(title=title, body=body, final_url=final_url, notes=notes)
    if body:
        notes.append(f"html body too short ({body_length(body)} < {min_body_chars})")
        return StageResult.failed("extract_failed", title=title, body=body, final_url=final_url, notes=notes)
    return StageResult.failed("empty_body", title=title, body=None, final_url=final_url, notes=notes)


def default_html_fetcher(url: str, timeout_ms: int) -> tuple[str, str | None]:
    try:
        return curl_fetch_text(url, timeout_ms, accept="text/html,application/xhtml+xml")
    except RuntimeError:
        pass
    request = Request(
        url,
        headers={
            "User-Agent": "Genm-codex/1.0 (+report-only acquisition helper)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=max(1.0, timeout_ms / 1000.0)) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        text = raw.decode(charset, errors="replace")
        return text, response.geturl()


def classify_subprocess_failure(stderr: str, stdout: str) -> FailureReason:
    haystack = f"{stderr}\n{stdout}".lower()
    if "robots" in haystack:
        return "robots"
    if "npm err" in haystack or "enoent" in haystack or "cannot find module" in haystack:
        return "install_error"
    return "tool_unavailable"


def build_reader_proxy_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme or "https"
    normalized = f"{scheme}://{parsed.netloc}{parsed.path}"
    if parsed.query:
        normalized = f"{normalized}?{parsed.query}"
    if parsed.fragment:
        normalized = f"{normalized}#{parsed.fragment}"
    return f"https://r.jina.ai/http://{normalized.removeprefix('http://').removeprefix('https://')}"


def curl_fetch_text(url: str, timeout_ms: int, *, accept: str) -> tuple[str, str | None]:
    marker = "__GENM_FINAL_URL__:"
    cmd = [
        "curl",
        "-L",
        "--max-time",
        str(max(1, int(timeout_ms / 1000))),
        "-A",
        "Genm-codex/1.0",
        "-H",
        f"Accept: {accept}",
        "-w",
        f"\\n{marker}%{{url_effective}}",
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        stderr = (proc.stderr or proc.stdout).strip()
        if proc.returncode == 28:
            raise RuntimeError("timeout")
        raise RuntimeError(stderr or f"curl_exit_{proc.returncode}")

    stdout = proc.stdout
    final_url = None
    if marker in stdout:
        stdout, final_url = stdout.rsplit(marker, 1)
        final_url = final_url.strip() or None
    return stdout.strip(), final_url


def parse_reader_proxy_response(text: str) -> StageResult:
    cleaned = text.replace("\r\n", "\n")
    title_match = re.search(r"^Title:\s*(.+)$", cleaned, re.MULTILINE)
    source_match = re.search(r"^URL Source:\s*(.+)$", cleaned, re.MULTILINE)
    body = cleaned
    marker = "Markdown Content:"
    if marker in cleaned:
        body = cleaned.split(marker, 1)[1]
    body = normalize_text(body)
    title = normalize_text(title_match.group(1)) if title_match else None
    final_url = normalize_text(source_match.group(1)) if source_match else None
    if body_length(body) == 0:
        return StageResult.failed("empty_body", title=title, final_url=final_url)
    return StageResult.ok_result(title=title, body=body, final_url=final_url, notes=["reader proxy"])


def bing_rss_search_provider(fetch_text_fn: FetchTextFn | None = None) -> FetchProvider:
    generic_tokens = {"article", "post", "page", "question", "p", "www", "m", "amp"}

    def meaningful_path_tokens(value: str) -> set[str]:
        parsed = urlparse(value)
        tokens = re.findall(r"[A-Za-z0-9]+", parsed.path.lower())
        result = set()
        for token in tokens:
            if token in generic_tokens:
                continue
            if token.isdigit() and len(token) >= 4:
                result.add(token)
                continue
            if len(token) >= 4:
                result.add(token)
        return result

    def run(url: str, timeout_ms: int) -> StageResult:
        query_url = f"https://www.bing.com/search?format=rss&q={quote_plus(url)}"
        source_host = urlparse(url).netloc.lower()
        source_tokens = meaningful_path_tokens(url)
        try:
            if fetch_text_fn is not None:
                text, _ = fetch_text_fn(query_url, timeout_ms, accept="application/rss+xml,text/xml")
            else:
                text, _ = curl_fetch_text(query_url, timeout_ms, accept="application/rss+xml,text/xml")
        except RuntimeError as exc:
            reason = "timeout" if str(exc) == "timeout" else "network_error"
            return StageResult.failed(reason, notes=[str(exc)])

        try:
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            return StageResult.failed("extract_failed", notes=[f"bing rss parse error: {exc}"])

        items = root.findall("./channel/item")
        if not items:
            return StageResult.failed("empty_body", notes=["bing rss returned no items"])

        chosen = None
        for item in items:
            link = normalize_text(item.findtext("link") or "")
            host = urlparse(link).netloc.lower()
            if source_host and host == source_host:
                if source_tokens:
                    candidate_tokens = meaningful_path_tokens(link)
                    if not (candidate_tokens & source_tokens):
                        continue
                chosen = item
                break
        if chosen is None:
            return StageResult.failed("extract_failed", notes=["bing rss returned no same-host items"])

        title = normalize_text(chosen.findtext("title") or "")
        link = normalize_text(chosen.findtext("link") or "")
        description = normalize_text(chosen.findtext("description") or "")
        body = description or title
        if body_length(body) == 0:
            return StageResult.failed("empty_body", title=title or None, final_url=link or None)
        return StageResult.ok_result(
            title=title or None,
            body=body,
            final_url=link or None,
            notes=["bing rss search fallback"],
        )

    return run


def reader_proxy_provider(
    urlopen_fn: Callable = urlopen,
    fetch_text_fn: FetchTextFn | None = None,
) -> FetchProvider:
    def run(url: str, timeout_ms: int) -> StageResult:
        proxy_url = build_reader_proxy_url(url)
        try:
            if fetch_text_fn is not None:
                text, _ = fetch_text_fn(proxy_url, timeout_ms, accept="text/plain,text/markdown")
            else:
                try:
                    text, _ = curl_fetch_text(proxy_url, timeout_ms, accept="text/plain,text/markdown")
                except RuntimeError:
                    request = Request(
                        proxy_url,
                        headers={
                            "User-Agent": "Genm-codex/1.0 (+reader proxy fetch)",
                            "Accept": "text/plain,text/markdown",
                        },
                    )
                    with urlopen_fn(request, timeout=max(1.0, timeout_ms / 1000.0)) as response:
                        text = response.read().decode("utf-8", errors="replace")
        except HTTPError as exc:
            if exc.code in {451, 403}:
                return StageResult.failed("robots", notes=[f"reader proxy http {exc.code}"])
            if exc.code == 422:
                return StageResult.failed("extract_failed", notes=[f"reader proxy http {exc.code}"])
            return StageResult.failed("network_error", notes=[f"reader proxy http {exc.code}"])
        except URLError as exc:
            return StageResult.failed("network_error", notes=[str(exc.reason)])
        except TimeoutError:
            return StageResult.failed("timeout")
        except RuntimeError as exc:
            reason = "timeout" if str(exc) == "timeout" else "network_error"
            return StageResult.failed(reason, notes=[str(exc)])

        return parse_reader_proxy_response(text)

    return run


def command_provider(command: str | None) -> FetchProvider | None:
    if not command:
        return None
    template = shlex.split(command)
    if not template:
        return None

    def run(url: str, timeout_ms: int) -> StageResult:
        argv = [part.replace("{url}", url) for part in template]
        if not any("{url}" in part for part in template):
            argv.append(url)
        try:
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=max(1.0, timeout_ms / 1000.0),
                check=False,
            )
        except FileNotFoundError as exc:
            return StageResult.failed("tool_unavailable", notes=[str(exc)])
        except subprocess.TimeoutExpired:
            return StageResult.failed("timeout")

        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        if proc.returncode != 0:
            return StageResult.failed(classify_subprocess_failure(stderr, stdout), notes=[stderr or stdout])

        if not stdout:
            return StageResult.failed("empty_body", notes=["provider returned empty stdout"])

        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as exc:
            return StageResult.failed("unknown", notes=[f"provider returned non-json output: {exc}"])

        status = str(payload.get("status") or "").strip().lower()
        if status in {"blocked_by_robots", "robots"}:
            return StageResult.failed("robots", notes=list(payload.get("notes") or []))

        failure_reason = payload.get("failure_reason")
        if failure_reason:
            return StageResult.failed(
                canonical_reason(str(failure_reason)),
                title=payload.get("title"),
                body=pick_first(payload.get("body"), payload.get("content"), payload.get("text")),
                final_url=payload.get("final_url") or payload.get("source_url"),
                notes=list(payload.get("notes") or []),
            )

        return StageResult.ok_result(
            title=payload.get("title"),
            body=pick_first(payload.get("body"), payload.get("content"), payload.get("text")),
            final_url=payload.get("final_url") or payload.get("source_url"),
            notes=list(payload.get("notes") or []),
        )

    return run


def empty_stage_result(
    *,
    source_url: str,
    attempts: list[AttemptRecord],
    notes: list[str],
    fetched_at: str,
    duration_ms: int,
    failure_reason: FailureReason,
) -> AcquireArticleResult:
    return AcquireArticleResult(
        status="failed",
        source_type="none",
        title=None,
        body=None,
        source_url=source_url,
        final_url=None,
        failure_reason=failure_reason,
        attempts=attempts,
        notes=notes,
        fetched_at=fetched_at,
        duration_ms=duration_ms,
    )


def acquire_article(
    url: str,
    *,
    prefer_source: str = "auto",
    timeout_ms: int = 30000,
    min_body_chars: int = 300,
    fetch_provider: FetchProvider | None = None,
    html_fetcher: HTMLFetcher | None = None,
    search_provider: FetchProvider | None = None,
    policy_store: DomainPolicyStore | None = None,
    fetched_at: str | None = None,
) -> AcquireArticleResult:
    started = time.monotonic()
    fetched_at = fetched_at or now_iso()
    attempts: list[AttemptRecord] = []
    notes: list[str] = []
    domain = urlparse(url).netloc.lower()
    html_fetcher = html_fetcher or default_html_fetcher
    fetch_provider = fetch_provider or reader_proxy_provider()
    search_provider = search_provider or bing_rss_search_provider()

    order_map = {
        "auto": ["fetch_mcp", "direct_html", "search_fallback"],
        "fetch_mcp": ["fetch_mcp", "direct_html", "search_fallback"],
        "direct_html": ["direct_html", "search_fallback"],
        "search_fallback": ["search_fallback"],
    }
    stages = order_map.get(prefer_source, order_map["auto"])

    def record_attempt(stage: str, ok: bool, started_at: float, reason: str | None = None) -> None:
        attempts.append(
            AttemptRecord(
                stage=stage,
                ok=ok,
                duration_ms=int((time.monotonic() - started_at) * 1000),
                reason=reason,
            )
        )

    def finalize(stage: str, stage_result: StageResult, *, status: str, failure_reason: FailureReason | None) -> AcquireArticleResult:
        all_notes = notes + list(stage_result.notes)
        return AcquireArticleResult(
            status=status,
            source_type=stage,
            title=stage_result.title,
            body=stage_result.body,
            source_url=url,
            final_url=stage_result.final_url,
            failure_reason=failure_reason,
            attempts=attempts,
            notes=all_notes,
            fetched_at=fetched_at,
            duration_ms=int((time.monotonic() - started) * 1000),
        )

    for stage in stages:
        if stage == "fetch_mcp":
            if policy_store and domain and policy_store.should_skip_fetch(domain):
                notes.append(f"fetch_mcp skipped due to domain policy for {domain}")
                continue
            if fetch_provider is None:
                attempts.append(AttemptRecord(stage="fetch_mcp", ok=False, duration_ms=0, reason="tool_unavailable"))
                notes.append("fetch_mcp provider not configured")
                continue
            stage_started = time.monotonic()
            result = fetch_provider(url, timeout_ms)
            reason = result.failure_reason
            ok = reason is None and body_length(result.body) >= min_body_chars
            if not ok and reason is None:
                reason = "empty_body"
                result = StageResult.failed(reason, title=result.title, body=result.body, final_url=result.final_url, notes=result.notes)
            record_attempt("fetch_mcp", ok, stage_started, reason)
            if ok:
                if policy_store and domain:
                    policy_store.record_fetch_success(domain, timestamp=fetched_at)
                return finalize("fetch_mcp", result, status="success", failure_reason=None)
            if policy_store and domain and reason:
                policy_store.record_fetch_failure(domain, reason)
            continue

        if stage == "direct_html":
            stage_started = time.monotonic()
            try:
                html_payload = html_fetcher(url, timeout_ms)
            except HTTPError as exc:
                result = StageResult.failed("network_error", notes=[f"http error {exc.code}"])
                record_attempt("direct_html", False, stage_started, result.failure_reason)
                continue
            except URLError as exc:
                result = StageResult.failed("network_error", notes=[str(exc.reason)])
                record_attempt("direct_html", False, stage_started, result.failure_reason)
                continue
            except TimeoutError:
                result = StageResult.failed("timeout")
                record_attempt("direct_html", False, stage_started, result.failure_reason)
                continue

            if isinstance(html_payload, tuple):
                html, final_url = html_payload
            else:
                html, final_url = html_payload, url
            result = extract_html_stage(html, final_url=final_url, min_body_chars=min_body_chars)
            ok = result.failure_reason is None
            record_attempt("direct_html", ok, stage_started, result.failure_reason)
            if ok:
                return finalize("html_extract", result, status="success", failure_reason=None)
            continue

        if stage == "search_fallback":
            if search_provider is None:
                attempts.append(AttemptRecord(stage="search_fallback", ok=False, duration_ms=0, reason="tool_unavailable"))
                notes.append("search_fallback provider not configured")
                continue
            stage_started = time.monotonic()
            result = search_provider(url, timeout_ms)
            ok = result.failure_reason is None and body_length(result.body) > 0
            reason = result.failure_reason
            if not ok and reason is None:
                reason = "empty_body"
                result = StageResult.failed(reason, title=result.title, body=result.body, final_url=result.final_url, notes=result.notes)
            record_attempt("search_fallback", ok, stage_started, reason)
            if ok:
                return finalize("search_fallback", result, status="partial", failure_reason="search_only")
            continue

    last_reason = next((attempt.reason for attempt in reversed(attempts) if attempt.reason), "unknown")
    return empty_stage_result(
        source_url=url,
        attempts=attempts,
        notes=notes,
        fetched_at=fetched_at,
        duration_ms=int((time.monotonic() - started) * 1000),
        failure_reason=last_reason,
    )


def default_policy_path() -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root / ".tmp" / "acquire-source-policy.json"


def default_provider_registry_path() -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root / "shared" / "templates" / "acquire-provider-registry-v1.json"


def load_json_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_toml_if_exists(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_project_config(project_root: str | None) -> dict:
    if not project_root:
        return {}
    return load_json_if_exists(Path(project_root) / ".mighty" / "config.json")


def read_codex_config() -> dict:
    config_path = Path.home() / ".codex" / "config.toml"
    return load_toml_if_exists(config_path)


def load_provider_registry(path: str | Path | None) -> dict:
    registry_path = Path(path) if path else default_provider_registry_path()
    payload = load_json_if_exists(registry_path)
    return payload if isinstance(payload, dict) else {}


def nested_get(payload: dict, path: list[str]) -> dict | str | None:
    current: object = payload
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current if isinstance(current, (dict, str)) else None


def resolve_provider_settings(
    *,
    role: str,
    cli_command: str,
    env_command: str,
    project_root: str | None,
    registry: dict,
) -> tuple[FetchProvider, dict]:
    builtin_defaults = registry.get("defaults", {})
    project_config = read_project_config(project_root)
    codex_config = read_codex_config()

    if cli_command:
        provider = command_provider(cli_command)
        if provider is not None:
            return provider, {
                "role": role,
                "source": "cli",
                "kind": "external_command",
                "name": "external_command",
                "command": cli_command,
            }

    if env_command:
        provider = command_provider(env_command)
        if provider is not None:
            return provider, {
                "role": role,
                "source": "env",
                "kind": "external_command",
                "name": "external_command",
                "command": env_command,
            }

    project_spec = nested_get(project_config, ["acquire_source_text", f"{role}_provider"])
    if isinstance(project_spec, dict):
        preset = str(project_spec.get("preset") or "")
        command = str(project_spec.get("command") or "")
        if command:
            provider = command_provider(command)
            if provider is not None:
                return provider, {
                    "role": role,
                    "source": "project_config",
                    "kind": "external_command",
                    "name": preset or "external_command",
                    "command": command,
                }
        if preset:
            provider = builtin_provider(role, preset)
            if provider is not None:
                return provider, {
                    "role": role,
                    "source": "project_config",
                    "kind": "builtin",
                    "name": preset,
                    "command": None,
                }

    codex_spec = nested_get(codex_config, ["genm", "acquire_source_text", f"{role}_provider"])
    if isinstance(codex_spec, dict):
        preset = str(codex_spec.get("preset") or "")
        command = str(codex_spec.get("command") or "")
        if command:
            provider = command_provider(command)
            if provider is not None:
                return provider, {
                    "role": role,
                    "source": "codex_config",
                    "kind": "external_command",
                    "name": preset or "external_command",
                    "command": command,
                }
        if preset:
            provider = builtin_provider(role, preset)
            if provider is not None:
                return provider, {
                    "role": role,
                    "source": "codex_config",
                    "kind": "builtin",
                    "name": preset,
                    "command": None,
                }

    default_name = str(builtin_defaults.get(role) or ("reader_proxy" if role == "fetch" else "bing_rss"))
    provider = builtin_provider(role, default_name)
    if provider is None:
        raise RuntimeError(f"Unsupported default provider preset: {default_name}")
    return provider, {
        "role": role,
        "source": "registry_default",
        "kind": "builtin",
        "name": default_name,
        "command": None,
    }


def builtin_provider(role: str, preset: str) -> FetchProvider | None:
    if role == "fetch" and preset == "reader_proxy":
        return reader_proxy_provider()
    if role == "search" and preset == "bing_rss":
        return bing_rss_search_provider()
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Acquire article text with fetch MCP -> direct HTML -> search fallback stages.")
    parser.add_argument("url", help="Article URL to acquire")
    parser.add_argument("--project-root", default="")
    parser.add_argument("--prefer-source", choices=["auto", "fetch_mcp", "direct_html", "search_fallback"], default="auto")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    parser.add_argument("--min-body-chars", type=int, default=300)
    parser.add_argument("--fetch-cmd", default="")
    parser.add_argument("--search-cmd", default="")
    parser.add_argument("--policy-file", default=os.getenv("GENM_ACQUIRE_POLICY_FILE", str(default_policy_path())))
    parser.add_argument("--provider-registry", default=str(default_provider_registry_path()))
    parser.add_argument("--show-provider-config", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    registry = load_provider_registry(args.provider_registry)
    fetch_provider, fetch_trace = resolve_provider_settings(
        role="fetch",
        cli_command=args.fetch_cmd,
        env_command=os.getenv("GENM_FETCH_MCP_CMD", ""),
        project_root=args.project_root or None,
        registry=registry,
    )
    search_provider, search_trace = resolve_provider_settings(
        role="search",
        cli_command=args.search_cmd,
        env_command=os.getenv("GENM_SEARCH_FALLBACK_CMD", ""),
        project_root=args.project_root or None,
        registry=registry,
    )
    if args.show_provider_config:
        print(
            json.dumps(
                {
                    "fetch_provider": fetch_trace,
                    "search_provider": search_trace,
                    "project_root": args.project_root or None,
                    "provider_registry": args.provider_registry,
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return
    policy_store = DomainPolicyStore(Path(args.policy_file)) if args.policy_file else None
    result = acquire_article(
        args.url,
        prefer_source=args.prefer_source,
        timeout_ms=args.timeout_ms,
        min_body_chars=args.min_body_chars,
        fetch_provider=fetch_provider,
        search_provider=search_provider,
        policy_store=policy_store,
    )
    result.provider_trace = {"fetch": fetch_trace, "search": search_trace}
    payload = result.to_dict()
    if args.pretty:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
