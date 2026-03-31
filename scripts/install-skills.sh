#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

PLATFORM="${1:-codex}"

install_to() {
  local target_dir="$1"
  mkdir -p "${target_dir}"
  while IFS=$'\t' read -r source_name target_name; do
    [[ -n "${source_name}" ]] || continue
    ln -sfn "${ROOT_DIR}/skills/${source_name}" "${target_dir}/${target_name}"
  done < <(python3 "${ROOT_DIR}/scripts/render_skill_alias_plan.py" --format tsv)
  echo "Installed Genm-codex skills into ${target_dir}"
}

case "${PLATFORM}" in
  codex)    install_to "${HOME}/.codex/skills" ;;
  claude)   install_to "${HOME}/.claude/skills" ;;
  opencode) install_to "${HOME}/.config/opencode/skills" ;;
  openclaw) install_to "${HOME}/.openclaw/skills" ;;
  --all)
    install_to "${HOME}/.codex/skills"
    install_to "${HOME}/.claude/skills"
    install_to "${HOME}/.config/opencode/skills"
    install_to "${HOME}/.openclaw/skills"
    ;;
  *)
    echo "Unknown platform: ${PLATFORM}" >&2
    echo "Usage: $0 [codex|claude|opencode|openclaw|--all]" >&2
    exit 1
    ;;
esac
