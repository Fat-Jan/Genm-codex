import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "post_write_lint.py"


def load_module():
    spec = importlib.util.spec_from_file_location("post_write_lint", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PostWriteLintContractTests(unittest.TestCase):
    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/post_write_lint.py is missing")


class PostWriteLintBehaviorTests(unittest.TestCase):
    def test_ai_turn_marker_density_warns(self) -> None:
        module = load_module()
        policy = module.load_policy()
        text = "他忽然抬头。她忽然转身。众人忽然沉默。"

        result = module.analyze_text(text, policy)

        self.assertTrue(any(item["code"] == "ai-turn-marker-density" for item in result["warnings"]))

    def test_explanation_first_template_warns(self) -> None:
        module = load_module()
        policy = module.load_policy()
        text = "这一刻，他终于明白了什么叫代价。"

        result = module.analyze_text(text, policy)

        self.assertTrue(any(item["code"] == "explanation-first-template" for item in result["warnings"]))

    def test_long_paragraph_density_warns(self) -> None:
        module = load_module()
        policy = module.load_policy()
        para = "他站在门口看着会议室里的每个人，心里一遍遍过着刚才那场对话留下的裂缝。" * 10
        text = f"{para}\n\n{para}"

        result = module.analyze_text(text, policy)

        self.assertTrue(any(item["code"] == "long-paragraph-density" for item in result["warnings"]))

    def test_collective_shock_template_warns(self) -> None:
        module = load_module()
        policy = module.load_policy()
        text = "全场震惊，所有人都目瞪口呆。"

        result = module.analyze_text(text, policy)

        self.assertTrue(any(item["code"] == "collective-shock-template" for item in result["warnings"]))

    def test_repeated_exact_token_blocks(self) -> None:
        module = load_module()
        policy = module.load_policy()
        text = ("foo " * 3) + ("甲乙丙丁" * 600)

        result = module.analyze_text(text, policy)

        self.assertTrue(any(item["code"] == "malformed-repeated-token" for item in result["issues"]))

    def test_cli_outputs_json_and_leaves_input_unchanged(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            chapter_path = Path(tmpdir) / "第001章.md"
            original = "全场震惊。"
            chapter_path.write_text(original, encoding="utf-8")

            proc = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(chapter_path)],
                capture_output=True,
                text=True,
                check=True,
            )

            payload = json.loads(proc.stdout)
            self.assertEqual(payload["chapter_file"], str(chapter_path))
            self.assertTrue(any(item["code"] == "collective-shock-template" for item in payload["warnings"]))
            self.assertEqual(chapter_path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
