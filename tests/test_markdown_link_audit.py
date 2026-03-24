from pathlib import Path
import importlib.util
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "audit_local_links.py"


def load_module():
    spec = importlib.util.spec_from_file_location("audit_local_links", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MarkdownLinkAuditTests(unittest.TestCase):
    def test_repo_has_no_broken_local_markdown_links_outside_code_fences(self):
        module = load_module()
        broken = module.find_broken_links(REPO_ROOT)
        self.assertEqual(broken, [], broken)


if __name__ == "__main__":
    unittest.main()
