#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
MATRIX_FILE="${GENM_HOST_CAPABILITY_MATRIX_FILE:-${ROOT_DIR}/shared/templates/host-capability-matrix-v1.json}"
PLATFORM="${1:-codex}"

read_host_spec() {
  local platform="$1"
  python3 - "$MATRIX_FILE" "$platform" <<'PY'
import json
import os
import sys
from pathlib import Path

ALLOWED_INSTALL_ROOTS = {
    "claude": "~/.claude/skills",
    "codex": "~/.codex/skills",
    "opencode": "~/.config/opencode/skills",
    "openclaw": "~/.openclaw/skills",
}

matrix_path = Path(sys.argv[1])
platform = sys.argv[2]
payload = json.loads(matrix_path.read_text(encoding="utf-8"))
row = payload["hosts"].get(platform)
if row is None:
    sys.stderr.write(f"Unknown platform: {platform}\n")
    sys.exit(2)
install_mode = row["install_mode"]
install_root = row["skill_install_root"]
if install_mode == "unsupported":
    sys.stderr.write(f"Unsupported platform: {platform}\n")
    sys.exit(3)
if not isinstance(install_root, str) or not install_root:
    sys.stderr.write(f"Platform {platform} has no install root\n")
    sys.exit(4)
expected_root = ALLOWED_INSTALL_ROOTS.get(platform)
if expected_root is None:
    sys.stderr.write(f"Platform {platform} has no allowed install root\n")
    sys.exit(5)
if install_root != expected_root:
    sys.stderr.write(f"Platform {platform} declares unexpected install root\n")
    sys.exit(6)
resolved = str(Path(os.environ["HOME"]) / install_root.removeprefix("~/"))
print(f"{platform}\t{install_mode}\t{resolved}")
PY
}

list_installable_specs() {
  python3 - "$MATRIX_FILE" <<'PY'
import json
import os
import sys
from pathlib import Path

ALLOWED_INSTALL_ROOTS = {
    "claude": "~/.claude/skills",
    "codex": "~/.codex/skills",
    "opencode": "~/.config/opencode/skills",
    "openclaw": "~/.openclaw/skills",
}

matrix_path = Path(sys.argv[1])
payload = json.loads(matrix_path.read_text(encoding="utf-8"))
for platform, row in payload["hosts"].items():
    install_mode = row["install_mode"]
    install_root = row["skill_install_root"]
    if install_mode == "unsupported":
        continue
    if not isinstance(install_root, str) or not install_root:
        sys.stderr.write(f"Platform {platform} has no install root\n")
        sys.exit(4)
    expected_root = ALLOWED_INSTALL_ROOTS.get(platform)
    if expected_root is None:
        sys.stderr.write(f"Platform {platform} has no allowed install root\n")
        sys.exit(5)
    if install_root != expected_root:
        sys.stderr.write(f"Platform {platform} declares unexpected install root\n")
        sys.exit(6)
    resolved = str(Path(os.environ["HOME"]) / install_root.removeprefix("~/"))
    print(f"{platform}\t{install_mode}\t{resolved}")
PY
}

validate_install_name() {
  local install_name="$1"

  if [[ ! "${install_name}" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]; then
    echo "Unsafe install name: ${install_name}" >&2
    return 1
  fi
}

prepare_target_path() {
  local target_path="$1"
  local install_mode="$2"

  if [[ -L "${target_path}" ]]; then
    rm -f "${target_path}"
    return 0
  fi

  if [[ "${install_mode}" == "copy" && -e "${target_path}" ]]; then
    rm -rf "${target_path}"
    return 0
  fi

  if [[ -e "${target_path}" ]]; then
    echo "Refusing to overwrite existing non-symlink path: ${target_path}" >&2
    return 1
  fi
}

materialize_pair() {
  local source_name="$1"
  local target_name="$2"
  local install_mode="$3"
  local target_dir="$4"
  validate_install_name "${source_name}"
  validate_install_name "${target_name}"
  local source_path="${ROOT_DIR}/skills/${source_name}"
  local target_path="${target_dir}/${target_name}"

  prepare_target_path "${target_path}" "${install_mode}"
  case "${install_mode}" in
    symlink)
      ln -s "${source_path}" "${target_path}"
      ;;
    copy)
      cp -R "${source_path}" "${target_path}"
      ;;
    *)
      echo "Unsupported install mode: ${install_mode}" >&2
      exit 1
      ;;
  esac
}

install_to() {
  local platform="$1"
  local install_mode="$2"
  local target_dir="$3"
  mkdir -p "${target_dir}"
  while IFS=$'\t' read -r source_name target_name; do
    [[ -n "${source_name}" ]] || continue
    materialize_pair "${source_name}" "${target_name}" "${install_mode}" "${target_dir}"
  done < <(python3 "${ROOT_DIR}/scripts/render_skill_alias_plan.py" --format tsv)
  echo "Installed Genm-codex skills into ${target_dir} (${platform}, ${install_mode})"
}

if [[ "${PLATFORM}" == "--all" ]]; then
  install_specs="$(list_installable_specs)"
  while IFS=$'\t' read -r platform install_mode target_dir; do
    [[ -n "${platform}" ]] || continue
    install_to "${platform}" "${install_mode}" "${target_dir}"
  done <<<"${install_specs}"
  exit 0
fi

IFS=$'\t' read -r resolved_platform install_mode target_dir <<<"$(read_host_spec "${PLATFORM}")"
install_to "${resolved_platform}" "${install_mode}" "${target_dir}"
