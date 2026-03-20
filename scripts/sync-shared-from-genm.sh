#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_ROOT="$(cd "${SCRIPT_DIR}/../../Genm" && pwd)"
REPORT_ONLY=false
DOMAINS=()

usage() {
  cat <<'EOF'
Usage:
  sync-shared-from-genm.sh [--report] [--domain <profiles|references|templates>]

Examples:
  sync-shared-from-genm.sh
  sync-shared-from-genm.sh --report
  sync-shared-from-genm.sh --domain profiles
  sync-shared-from-genm.sh --report --domain references
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --report)
      REPORT_ONLY=true
      shift
      ;;
    --domain)
      [[ $# -ge 2 ]] || { echo "Missing value for --domain" >&2; exit 1; }
      DOMAINS+=("$2")
      shift 2
      ;;
    --domain=*)
      DOMAINS+=("${1#*=}")
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ ${#DOMAINS[@]} -eq 0 ]]; then
  DOMAINS=(profiles references templates)
fi

resolve_source_dir() {
  local domain="$1"
  case "${domain}" in
    profiles) echo "${SOURCE_ROOT}/build/profiles" ;;
    references) echo "${SOURCE_ROOT}/build/references" ;;
    templates) echo "${SOURCE_ROOT}/build/templates" ;;
    *)
      echo "Unsupported domain: ${domain}" >&2
      exit 1
      ;;
  esac
}

resolve_target_dir() {
  local domain="$1"
  case "${domain}" in
    profiles) echo "${TARGET_ROOT}/shared/profiles" ;;
    references) echo "${TARGET_ROOT}/shared/references" ;;
    templates) echo "${TARGET_ROOT}/shared/templates" ;;
    *)
      echo "Unsupported domain: ${domain}" >&2
      exit 1
      ;;
  esac
}

count_files() {
  local dir="$1"
  if [[ ! -d "${dir}" ]]; then
    echo 0
    return
  fi
  find "${dir}" -type f | wc -l | awk '{print $1}'
}

count_dirs() {
  local dir="$1"
  if [[ ! -d "${dir}" ]]; then
    echo 0
    return
  fi
  find "${dir}" -mindepth 1 -type d | wc -l | awk '{print $1}'
}

report_domain() {
  local domain="$1"
  local source_dir
  local target_dir
  source_dir="$(resolve_source_dir "${domain}")"
  target_dir="$(resolve_target_dir "${domain}")"

  if [[ ! -d "${source_dir}" ]]; then
    echo "Missing source directory: ${source_dir}" >&2
    exit 1
  fi

  echo "## ${domain}"
  echo "- source: ${source_dir}"
  echo "- target: ${target_dir}"
  echo "- source files: $(count_files "${source_dir}")"
  echo "- source subdirs: $(count_dirs "${source_dir}")"
  if [[ -d "${target_dir}" ]]; then
    echo "- target status: present"
    echo "- target files: $(count_files "${target_dir}")"
    echo "- target subdirs: $(count_dirs "${target_dir}")"
  else
    echo "- target status: missing"
  fi
}

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

if [[ "${REPORT_ONLY}" == true ]]; then
  echo "# Shared Sync Report"
  echo "- source root: ${SOURCE_ROOT}"
  echo "- target root: ${TARGET_ROOT}/shared"
  for domain in "${DOMAINS[@]}"; do
    report_domain "${domain}"
  done
  exit 0
fi

for domain in "${DOMAINS[@]}"; do
  copy_tree "$(resolve_source_dir "${domain}")" "$(resolve_target_dir "${domain}")"
done

echo "Synced shared assets from ${SOURCE_ROOT} to ${TARGET_ROOT}/shared"
