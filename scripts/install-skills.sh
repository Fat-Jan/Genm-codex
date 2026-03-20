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

install_skill_aliases() {
  local source_name="$1"
  link_skill "${source_name}" "${source_name}"
  link_skill "${source_name}" "genm-${source_name}"
}

install_skill_aliases "novel-init"
install_skill_aliases "novel-analyze"
install_skill_aliases "novel-batch"
install_skill_aliases "novel-character"
install_skill_aliases "novel-foreshadowing"
install_skill_aliases "novel-fix"
install_skill_aliases "novel-genre"
install_skill_aliases "novel-index"
install_skill_aliases "novel-log"
install_skill_aliases "novel-polish"
install_skill_aliases "novel-precheck"
install_skill_aliases "novel-query"
install_skill_aliases "novel-setting"
install_skill_aliases "novel-snapshot"
install_skill_aliases "novel-spinoff"
install_skill_aliases "novel-status"
install_skill_aliases "novel-outline"
install_skill_aliases "novel-workflow"
install_skill_aliases "novel-write"
install_skill_aliases "novel-review"
install_skill_aliases "novel-resume"
install_skill_aliases "novel-retrieve"
install_skill_aliases "novel-rewrite"
install_skill_aliases "novel-export"

echo "Installed Genm-codex skills into ${TARGET_DIR}"
