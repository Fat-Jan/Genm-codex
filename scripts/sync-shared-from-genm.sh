#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_ROOT="$(cd "${SCRIPT_DIR}/../../Genm" && pwd)"

copy_tree() {
  local source_dir="$1"
  local target_dir="$2"

  if [[ ! -d "${source_dir}" ]]; then
    echo "Missing source directory: ${source_dir}" >&2
    exit 1
  fi

  rm -rf "${target_dir}"
  mkdir -p "$(dirname "${target_dir}")"
  cp -R "${source_dir}" "${target_dir}"
}

copy_tree "${SOURCE_ROOT}/build/profiles" "${TARGET_ROOT}/shared/profiles"
copy_tree "${SOURCE_ROOT}/build/references" "${TARGET_ROOT}/shared/references"
copy_tree "${SOURCE_ROOT}/build/templates" "${TARGET_ROOT}/shared/templates"

echo "Synced shared assets from ${SOURCE_ROOT} to ${TARGET_ROOT}/shared"
