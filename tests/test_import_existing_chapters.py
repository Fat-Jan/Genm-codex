import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "import_existing_chapters.py"


def load_module():
    spec = importlib.util.spec_from_file_location("import_existing_chapters", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def scaffold_project(root: Path) -> None:
    write_json(
        root / ".mighty" / "state.json",
        {
            "version": "5.0",
            "meta": {
                "title": "导入测试项目",
                "genre": "都市脑洞",
                "platform": "番茄",
                "updated_at": "2026-03-25T00:00:00Z",
            },
            "progress": {
                "current_chapter": 0,
                "total_words": 0,
            },
        },
    )
    (root / "chapters").mkdir(parents=True, exist_ok=True)


class ImportExistingChaptersContractTests(unittest.TestCase):
    def test_script_exists(self) -> None:
        self.assertTrue(MODULE_PATH.exists(), "scripts/import_existing_chapters.py is missing")


class ImportExistingChaptersBehaviorTests(unittest.TestCase):
    def make_project_root(self) -> Path:
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        root = Path(tmpdir.name) / "project"
        root.mkdir(parents=True)
        scaffold_project(root)
        return root

    def test_import_from_directory_creates_report_and_target_chapters(self) -> None:
        module = load_module()
        project_root = self.make_project_root()
        source_dir = project_root.parent / "source-dir"
        source_dir.mkdir()
        (source_dir / "001_初见.md").write_text("第一章正文", encoding="utf-8")
        (source_dir / "002_对账.md").write_text("第二章正文", encoding="utf-8")

        result = module.main([str(project_root), "--from", str(source_dir)])

        self.assertEqual(result["source_kind"], "directory")
        self.assertEqual(result["chapter_count"], 2)
        self.assertTrue((project_root / "chapters" / "第001章.md").exists())
        self.assertTrue((project_root / "chapters" / "第002章.md").exists())
        report = json.loads((project_root / ".mighty" / "import-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["chapter_count"], 2)
        self.assertIn("novel-index build", " ".join(report["next_actions"]))
        self.assertIn("setting gate", " ".join(report["next_actions"]))
        self.assertIn("novel-resume", " ".join(report["next_actions"]))

    def test_import_from_single_file_splits_chapters(self) -> None:
        module = load_module()
        project_root = self.make_project_root()
        source_file = project_root.parent / "source.txt"
        source_file.write_text(
            "第001章 初见\n第一章正文\n\n第002章 对账\n第二章正文\n",
            encoding="utf-8",
        )

        result = module.main([str(project_root), "--from", str(source_file)])

        self.assertEqual(result["source_kind"], "single-file")
        self.assertEqual(result["chapter_count"], 2)
        first = (project_root / "chapters" / "第001章.md").read_text(encoding="utf-8")
        second = (project_root / "chapters" / "第002章.md").read_text(encoding="utf-8")
        self.assertIn("第001章 初见", first)
        self.assertIn("第002章 对账", second)

    def test_existing_same_content_is_reused(self) -> None:
        module = load_module()
        project_root = self.make_project_root()
        source_dir = project_root.parent / "source-same"
        source_dir.mkdir()
        content = "第一章正文"
        (project_root / "chapters" / "第001章.md").write_text(content, encoding="utf-8")
        (source_dir / "001_初见.md").write_text(content, encoding="utf-8")

        result = module.main([str(project_root), "--from", str(source_dir)])

        self.assertEqual(result["chapter_count"], 1)
        report = json.loads((project_root / ".mighty" / "import-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["chapters"][0]["status"], "reused")

    def test_existing_conflicting_content_is_reported_without_overwrite(self) -> None:
        module = load_module()
        project_root = self.make_project_root()
        source_dir = project_root.parent / "source-conflict"
        source_dir.mkdir()
        target_path = project_root / "chapters" / "第001章.md"
        target_path.write_text("项目内旧稿", encoding="utf-8")
        (source_dir / "001_初见.md").write_text("导入源新稿", encoding="utf-8")

        result = module.main([str(project_root), "--from", str(source_dir)])

        self.assertEqual(result["chapter_count"], 1)
        self.assertEqual(target_path.read_text(encoding="utf-8"), "项目内旧稿")
        report = json.loads((project_root / ".mighty" / "import-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["chapters"][0]["status"], "conflict")


if __name__ == "__main__":
    unittest.main()
