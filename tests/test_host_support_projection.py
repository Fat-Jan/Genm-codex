import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "render_host_capability_projection.py"
SKILL_USAGE_PATH = REPO_ROOT / "docs" / "00-当前有效" / "skill-usage.md"
MATRIX_PATH = REPO_ROOT / "shared" / "templates" / "host-capability-matrix-v1.json"
INSTALL_START = "<!-- host-install-table:start -->"
INSTALL_END = "<!-- host-install-table:end -->"
SUPPORT_START = "<!-- host-support-table:start -->"
SUPPORT_END = "<!-- host-support-table:end -->"


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


class HostSupportProjectionTests(unittest.TestCase):
    def test_projection_helper_exists(self) -> None:
        self.assertTrue(
            MODULE_PATH.exists(),
            "scripts/render_host_capability_projection.py is missing",
        )

    def test_skill_usage_install_table_matches_projection(self) -> None:
        module = load_module()
        projection = module.build_projection()
        content = SKILL_USAGE_PATH.read_text(encoding="utf-8")
        actual = extract_block(content, INSTALL_START, INSTALL_END)
        expected = module.render_install_table(projection)
        self.assertEqual(actual, expected)

    def test_skill_usage_support_table_matches_projection(self) -> None:
        module = load_module()
        projection = module.build_projection()
        content = SKILL_USAGE_PATH.read_text(encoding="utf-8")
        actual = extract_block(content, SUPPORT_START, SUPPORT_END)
        expected = module.render_support_table(projection)
        self.assertEqual(actual, expected)

    def test_skill_usage_projection_excludes_unsupported_install_but_keeps_support_status(
        self,
    ) -> None:
        content = SKILL_USAGE_PATH.read_text(encoding="utf-8")
        install_block = extract_block(content, INSTALL_START, INSTALL_END)
        support_block = extract_block(content, SUPPORT_START, SUPPORT_END)
        self.assertNotIn("| Trae |", install_block)
        self.assertIn("| Trae | experimental | partial | unsupported |", support_block)

    def test_build_projection_respects_allow_env_override_switch(self) -> None:
        module = load_module()
        payload = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        payload["hosts"]["codex"]["skill_install_root"] = "~/.override-codex/skills"

        with tempfile.TemporaryDirectory() as tmpdir:
            matrix_path = Path(tmpdir) / "host-capability-matrix-v1.json"
            matrix_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            old_override = os.environ.get(module.MATRIX_OVERRIDE_ENV)
            os.environ[module.MATRIX_OVERRIDE_ENV] = str(matrix_path)
            try:
                default_projection = module.build_projection(allow_env_override=False)
                override_projection = module.build_projection(allow_env_override=True)
            finally:
                if old_override is None:
                    os.environ.pop(module.MATRIX_OVERRIDE_ENV, None)
                else:
                    os.environ[module.MATRIX_OVERRIDE_ENV] = old_override

        default_codex = next(
            host
            for host in default_projection["hosts"]
            if host["host_id"] == "codex"
        )
        override_codex = next(
            host
            for host in override_projection["hosts"]
            if host["host_id"] == "codex"
        )
        self.assertEqual(default_codex["skill_install_root"], "~/.codex/skills")
        self.assertEqual(
            override_codex["skill_install_root"],
            "~/.override-codex/skills",
        )


if __name__ == "__main__":
    unittest.main()
