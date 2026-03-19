#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

require_non_empty_dir() {
  local dir="$1"
  if [[ ! -d "${dir}" ]]; then
    echo "Missing directory: ${dir}" >&2
    exit 1
  fi

  if [[ -z "$(find "${dir}" -mindepth 1 -print -quit)" ]]; then
    echo "Directory is empty: ${dir}" >&2
    exit 1
  fi
}

require_file() {
  local file="$1"
  if [[ ! -f "${file}" ]]; then
    echo "Missing file: ${file}" >&2
    exit 1
  fi
}

require_non_empty_dir "${ROOT_DIR}/shared/profiles"
require_non_empty_dir "${ROOT_DIR}/shared/references"
require_non_empty_dir "${ROOT_DIR}/shared/templates"

for skill in novel-init novel-outline novel-write novel-review novel-rewrite novel-export; do
  require_file "${ROOT_DIR}/skills/${skill}/SKILL.md"
done

require_file "${ROOT_DIR}/docs/migration-map.md"
require_file "${ROOT_DIR}/docs/codex-migration-plan.md"

echo "Migration validation passed"
