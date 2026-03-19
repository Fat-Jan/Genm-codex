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

link_skill "novel-init" "genm-novel-init"
link_skill "novel-batch" "genm-novel-batch"
link_skill "novel-character" "genm-novel-character"
link_skill "novel-foreshadowing" "genm-novel-foreshadowing"
link_skill "novel-query" "genm-novel-query"
link_skill "novel-setting" "genm-novel-setting"
link_skill "novel-status" "genm-novel-status"
link_skill "novel-outline" "genm-novel-outline"
link_skill "novel-write" "genm-novel-write"
link_skill "novel-review" "genm-novel-review"
link_skill "novel-rewrite" "genm-novel-rewrite"
link_skill "novel-export" "genm-novel-export"

echo "Installed Genm-codex skills into ${TARGET_DIR}"
