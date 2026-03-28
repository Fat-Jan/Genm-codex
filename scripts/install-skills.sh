#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_DIR="${HOME}/.codex/skills"

mkdir -p "${TARGET_DIR}"

link_skill() {
  local source_name="$1"
  local target_name="$2"
  ln -sfn "${ROOT_DIR}/skills/${source_name}" "${TARGET_DIR}/${target_name}"
}

while IFS=$'\t' read -r source_name target_name; do
  [[ -n "${source_name}" ]] || continue
  link_skill "${source_name}" "${target_name}"
done < <(python3 "${ROOT_DIR}/scripts/render_skill_alias_plan.py" --format tsv)

echo "Installed Genm-codex skills into ${TARGET_DIR}"
