import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "install-skills.sh"
MATRIX_PATH = REPO_ROOT / "shared" / "templates" / "host-capability-matrix-v1.json"


def read_matrix() -> dict:
    return json.loads(MATRIX_PATH.read_text(encoding="utf-8"))


def write_matrix(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def resolve_home_path(home: str, raw_path: str) -> Path:
    if not raw_path.startswith("~/"):
        raise ValueError(f"Unsupported home-relative path: {raw_path}")
    return Path(home) / raw_path.removeprefix("~/")


class InstallSkillsMatrixTests(unittest.TestCase):
    def run_script(
        self,
        home: str,
        *args: str,
        matrix_path: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = home
        if matrix_path is not None:
            env["GENM_HOST_CAPABILITY_MATRIX_FILE"] = str(matrix_path)
        return subprocess.run(
            ["bash", str(SCRIPT_PATH), *args],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

    def test_script_exists(self) -> None:
        self.assertTrue(SCRIPT_PATH.exists(), "scripts/install-skills.sh is missing")

    def test_supported_host_installs_into_matrix_root(self) -> None:
        payload = read_matrix()
        host = payload["hosts"]["claude"]
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = self.run_script(tmpdir, "claude")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            target_dir = resolve_home_path(tmpdir, host["skill_install_root"])
            primary = target_dir / "novel-init"
            alias = target_dir / "genm-novel-init"
            self.assertTrue(primary.exists())
            self.assertTrue(alias.exists())
            self.assertTrue(primary.is_symlink())
            self.assertEqual(primary.resolve(), REPO_ROOT / "skills" / "novel-init")

    def test_unsupported_host_is_rejected_by_matrix_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = self.run_script(tmpdir, "trae")
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("unsupported", f"{proc.stdout}\n{proc.stderr}".lower())

    def test_unexpected_install_root_is_rejected_even_with_matrix_override(
        self,
    ) -> None:
        payload = read_matrix()
        payload["hosts"]["codex"]["skill_install_root"] = "~/tmp/skills"
        with tempfile.TemporaryDirectory() as tmpdir:
            matrix_path = Path(tmpdir) / "host-capability-matrix-v1.json"
            write_matrix(matrix_path, payload)
            proc = self.run_script(tmpdir, matrix_path=matrix_path)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn(
                "unexpected install root", f"{proc.stdout}\n{proc.stderr}".lower()
            )

    def test_all_installs_supported_hosts_only(self) -> None:
        payload = read_matrix()
        installable_hosts = {
            host_id: row
            for host_id, row in payload["hosts"].items()
            if row["install_mode"] != "unsupported"
            and row["skill_install_root"] is not None
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = self.run_script(tmpdir, "--all")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            for host_id, row in installable_hosts.items():
                self.assertTrue(
                    resolve_home_path(tmpdir, row["skill_install_root"]).exists(),
                    host_id,
                )
            self.assertNotIn("trae", proc.stdout.lower())

    def test_all_rejects_unexpected_install_root_from_matrix(self) -> None:
        payload = read_matrix()
        payload["hosts"]["openclaw"]["skill_install_root"] = "~/tmp/skills"
        with tempfile.TemporaryDirectory() as tmpdir:
            matrix_path = Path(tmpdir) / "host-capability-matrix-v1.json"
            write_matrix(matrix_path, payload)
            proc = self.run_script(tmpdir, "--all", matrix_path=matrix_path)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn(
                "unexpected install root", f"{proc.stdout}\n{proc.stderr}".lower()
            )

    def test_copy_mode_materializes_directories_instead_of_symlinks(self) -> None:
        payload = read_matrix()
        payload["hosts"]["codex"]["install_mode"] = "copy"
        with tempfile.TemporaryDirectory() as tmpdir:
            matrix_path = Path(tmpdir) / "host-capability-matrix-v1.json"
            write_matrix(matrix_path, payload)
            proc = self.run_script(tmpdir, matrix_path=matrix_path)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            target_dir = resolve_home_path(
                tmpdir, payload["hosts"]["codex"]["skill_install_root"]
            )
            primary = target_dir / "novel-init"
            self.assertTrue(primary.exists())
            self.assertFalse(primary.is_symlink())
            self.assertTrue((primary / "SKILL.md").exists())

    def test_copy_mode_reinstalls_cleanly_over_existing_directory(self) -> None:
        payload = read_matrix()
        payload["hosts"]["codex"]["install_mode"] = "copy"
        with tempfile.TemporaryDirectory() as tmpdir:
            matrix_path = Path(tmpdir) / "host-capability-matrix-v1.json"
            write_matrix(matrix_path, payload)
            first = self.run_script(tmpdir, matrix_path=matrix_path)
            self.assertEqual(first.returncode, 0, first.stderr)
            second = self.run_script(tmpdir, matrix_path=matrix_path)
            self.assertEqual(second.returncode, 0, second.stderr)

    def test_existing_symlink_is_replaced_safely(self) -> None:
        payload = read_matrix()
        host = payload["hosts"]["codex"]
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = resolve_home_path(tmpdir, host["skill_install_root"])
            target_dir.mkdir(parents=True, exist_ok=True)
            primary = target_dir / "novel-init"
            primary.symlink_to(REPO_ROOT / "skills" / "novel-query")
            proc = self.run_script(tmpdir)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(primary.is_symlink())
            self.assertEqual(primary.resolve(), REPO_ROOT / "skills" / "novel-init")

    def test_existing_directory_is_preserved_instead_of_deleted(self) -> None:
        payload = read_matrix()
        host = payload["hosts"]["codex"]
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = resolve_home_path(tmpdir, host["skill_install_root"])
            existing = target_dir / "novel-init"
            existing.mkdir(parents=True, exist_ok=True)
            sentinel = existing / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")
            proc = self.run_script(tmpdir)
            self.assertNotEqual(proc.returncode, 0)
            self.assertTrue(sentinel.exists())
            self.assertIn(
                "refusing to overwrite", f"{proc.stdout}\n{proc.stderr}".lower()
            )


if __name__ == "__main__":
    unittest.main()
