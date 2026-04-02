import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "render_host_capability_projection.py"
DOC_PATH = REPO_ROOT / "docs" / "00-当前有效" / "host-support-status-v1.6.md"
SUMMARY_START = "<!-- host-support-summary:start -->"
SUMMARY_END = "<!-- host-support-summary:end -->"
DETAILS_START = "<!-- host-support-details:start -->"
DETAILS_END = "<!-- host-support-details:end -->"


def load_module() -> object:
    spec = importlib.util.spec_from_file_location(
        "render_host_capability_projection", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def extract_block(content: str, start_marker: str, end_marker: str) -> str:
    start = content.index(start_marker) + len(start_marker)
    end = content.index(end_marker)
    return content[start:end].strip()


class HostSupportStatusDocTests(unittest.TestCase):
    def test_doc_exists(self) -> None:
        self.assertTrue(DOC_PATH.exists(), "host support status doc is missing")

    def test_summary_table_matches_projection(self) -> None:
        module = load_module()
        projection = module.build_projection()
        content = DOC_PATH.read_text(encoding="utf-8")
        actual = extract_block(content, SUMMARY_START, SUMMARY_END)
        expected = module.render_support_table(projection)
        self.assertEqual(actual, expected)

    def test_detail_sections_match_projection(self) -> None:
        module = load_module()
        projection = module.build_projection()
        content = DOC_PATH.read_text(encoding="utf-8")
        actual = extract_block(content, DETAILS_START, DETAILS_END)
        expected = module.render_support_details(projection)
        self.assertEqual(actual, expected)

    def test_trae_detail_keeps_unsupported_boundary(self) -> None:
        content = DOC_PATH.read_text(encoding="utf-8")
        detail_block = extract_block(content, DETAILS_START, DETAILS_END)
        self.assertIn("### Trae", detail_block)
        self.assertIn("- 安装支持：`unsupported`", detail_block)


if __name__ == "__main__":
    unittest.main()
