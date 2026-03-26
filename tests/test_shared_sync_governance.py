import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "sync-shared-from-genm.sh"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class SharedSyncGovernanceTests(unittest.TestCase):
    def make_roots(self) -> tuple[Path, Path]:
        tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(tempdir.cleanup)
        base = Path(tempdir.name)
        source_root = base / "Genm"
        target_root = base / "Genm-codex"
        for domain in ("profiles", "references", "templates"):
            (source_root / "build" / domain).mkdir(parents=True, exist_ok=True)
            (target_root / "shared" / domain).mkdir(parents=True, exist_ok=True)
        return source_root, target_root

    def write_governance(self, target_root: Path, protected_paths: list[str]) -> Path:
        governance_path = target_root / "shared" / "sync-governance.json"
        write_json(
            governance_path,
            {
                "version": "1.0",
                "policy": {
                    "protected_local_paths_are_restored": True,
                    "same_path_drift_requires_explicit_override": True,
                },
                "domains": {
                    "profiles": {"protected_local_paths": []},
                    "references": {"protected_local_paths": protected_paths},
                    "templates": {"protected_local_paths": []},
                },
            },
        )
        return governance_path

    def run_script(self, source_root: Path, target_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["GENM_SHARED_SOURCE_ROOT"] = str(source_root)
        env["GENM_CODEX_SHARED_TARGET_ROOT"] = str(target_root)
        env["GENM_SHARED_GOVERNANCE_FILE"] = str(target_root / "shared" / "sync-governance.json")
        return subprocess.run(
            ["bash", str(SCRIPT_PATH), *args],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

    def test_report_json_includes_local_only_drift_and_source_only(self) -> None:
        source_root, target_root = self.make_roots()
        self.write_governance(target_root, ["protected.md"])
        write_text(source_root / "build" / "references" / "common.md", "source-version")
        write_text(source_root / "build" / "references" / "source-only.md", "source-only")
        write_text(target_root / "shared" / "references" / "common.md", "target-version")
        write_text(target_root / "shared" / "references" / "protected.md", "keep-me")

        proc = self.run_script(source_root, target_root, "--report-json", "--domain", "references")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        domain = payload["domains"][0]
        self.assertEqual(domain["protected_local_paths"], ["protected.md"])
        self.assertEqual(domain["local_only_paths"], ["protected.md"])
        self.assertEqual(domain["unexpected_local_only_paths"], [])
        self.assertEqual(domain["drift_paths"], ["common.md"])
        self.assertEqual(domain["source_only_paths"], ["source-only.md"])

    def test_sync_blocks_unexpected_local_only_paths(self) -> None:
        source_root, target_root = self.make_roots()
        self.write_governance(target_root, [])
        write_text(source_root / "build" / "references" / "common.md", "source-version")
        write_text(target_root / "shared" / "references" / "common.md", "source-version")
        write_text(target_root / "shared" / "references" / "rogue.md", "unexpected")

        proc = self.run_script(source_root, target_root, "--domain", "references")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unexpected local-only paths", proc.stderr)
        self.assertTrue((target_root / "shared" / "references" / "rogue.md").exists())

    def test_sync_blocks_same_path_drift_without_override(self) -> None:
        source_root, target_root = self.make_roots()
        self.write_governance(target_root, [])
        write_text(source_root / "build" / "references" / "common.md", "source-version")
        write_text(target_root / "shared" / "references" / "common.md", "target-version")

        proc = self.run_script(source_root, target_root, "--domain", "references")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("same-path drift would be overwritten", proc.stderr)
        self.assertEqual(
            (target_root / "shared" / "references" / "common.md").read_text(encoding="utf-8"),
            "target-version",
        )

    def test_sync_with_override_restores_protected_local_paths(self) -> None:
        source_root, target_root = self.make_roots()
        self.write_governance(target_root, ["protected.md"])
        write_text(source_root / "build" / "references" / "common.md", "source-version")
        write_text(source_root / "build" / "references" / "source-only.md", "source-only")
        write_text(target_root / "shared" / "references" / "common.md", "target-version")
        write_text(target_root / "shared" / "references" / "protected.md", "keep-me")

        proc = self.run_script(
            source_root,
            target_root,
            "--allow-drift-overwrite",
            "--domain",
            "references",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(
            (target_root / "shared" / "references" / "common.md").read_text(encoding="utf-8"),
            "source-version",
        )
        self.assertEqual(
            (target_root / "shared" / "references" / "source-only.md").read_text(encoding="utf-8"),
            "source-only",
        )
        self.assertEqual(
            (target_root / "shared" / "references" / "protected.md").read_text(encoding="utf-8"),
            "keep-me",
        )

    def test_report_text_mode_surfaces_counts_and_lists(self) -> None:
        source_root, target_root = self.make_roots()
        self.write_governance(target_root, ["protected.md"])
        write_text(source_root / "build" / "references" / "common.md", "source-version")
        write_text(target_root / "shared" / "references" / "common.md", "target-version")
        write_text(target_root / "shared" / "references" / "protected.md", "keep-me")

        proc = self.run_script(source_root, target_root, "--report", "--domain", "references")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("# Shared Sync Report", proc.stdout)
        self.assertIn("protected local paths: 1", proc.stdout)
        self.assertIn("same-path drift paths: 1", proc.stdout)
        self.assertIn("local-only list: protected.md", proc.stdout)
        self.assertIn("drift list: common.md", proc.stdout)

    def test_report_json_supports_multiple_domains(self) -> None:
        source_root, target_root = self.make_roots()
        self.write_governance(target_root, ["protected.md"])
        write_text(source_root / "build" / "references" / "common.md", "source-version")
        write_text(target_root / "shared" / "references" / "protected.md", "keep-me")
        write_text(source_root / "build" / "templates" / "outline.md", "template")

        proc = self.run_script(
            source_root,
            target_root,
            "--report-json",
            "--domain",
            "references",
            "--domain",
            "templates",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual([item["domain"] for item in payload["domains"]], ["references", "templates"])


class SharedSyncGovernanceDocsTests(unittest.TestCase):
    def test_user_entry_docs_describe_governance_aware_sync(self) -> None:
        expectations = {
            "README.md": [
                "shared/sync-governance.json",
                "protected_local_paths",
                "drift_paths",
                "--allow-drift-overwrite",
            ],
            "docs/00-当前有效/v1-boundary.md": [
                "shared/sync-governance.json",
                "same-path drift overwrite",
                "--allow-drift-overwrite",
                "protected local paths",
            ],
            "docs/00-当前有效/skill-usage.md": [
                "protected_local_paths",
                "unexpected_local_only_paths",
                "drift_paths",
                "--allow-drift-overwrite",
            ],
        }
        for relative_path, tokens in expectations.items():
            content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for token in tokens:
                self.assertIn(token, content, f"{relative_path} missing token: {token}")

    def test_open_issues_reflect_resolved_shared_and_validation_items(self) -> None:
        content = (REPO_ROOT / "docs" / "10-进行中" / "architecture-open-issues.md").read_text(encoding="utf-8")
        self.assertIn("### AOI-002", content)
        self.assertIn("Status: `resolved`", content)
        self.assertIn("shared/sync-governance.json", content)
        self.assertIn("tests/test_shared_sync_governance.py", content)


if __name__ == "__main__":
    unittest.main()
