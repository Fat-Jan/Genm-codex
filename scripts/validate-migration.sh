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

for skill in \
  novel-init \
  novel-analyze \
  novel-close \
  novel-outline \
  novel-package \
  novel-write \
  novel-review \
  novel-resume \
  novel-retrieve \
  novel-rewrite \
  novel-export \
  novel-sync \
  novel-query \
  novel-scan \
  novel-status \
  novel-config \
  novel-test \
  novel-character \
  novel-setting \
  novel-foreshadowing \
  novel-batch \
  novel-index \
  novel-log \
  novel-learn \
  novel-fix \
  novel-polish \
  novel-precheck \
  novel-genre \
  novel-snapshot \
  novel-workflow \
  novel-retrieve \
  novel-spinoff
do
  require_file "${ROOT_DIR}/skills/${skill}/SKILL.md"
done

require_file "${ROOT_DIR}/docs/90-归档/迁移与RC/migration-map.md"
require_file "${ROOT_DIR}/docs/90-归档/迁移与RC/codex-migration-plan.md"
require_file "${ROOT_DIR}/docs/00-当前有效/project-knowledge-mcp.md"
require_file "${ROOT_DIR}/docs/00-当前有效/chapter-structure-fields-design.md"
require_file "${ROOT_DIR}/docs/00-当前有效/bucket-profile-slug-mapping.md"
require_file "${ROOT_DIR}/docs/00-当前有效/bucket-overlay-inventory.md"
require_file "${ROOT_DIR}/docs/00-当前有效/sample-library-index.md"
require_file "${ROOT_DIR}/docs/anti-flattening-framework/QUICK.md"
require_file "${ROOT_DIR}/docs/anti-flattening-framework/rule-cache.json"
require_file "${ROOT_DIR}/docs/opening-and-plot-framework/QUICK.md"
require_file "${ROOT_DIR}/docs/opening-and-plot-framework/rule-cache.json"
require_file "${ROOT_DIR}/docs/writing-core-framework/QUICK.md"
require_file "${ROOT_DIR}/docs/writing-core-framework/rule-cache.json"
require_file "${ROOT_DIR}/v1.1-roadmap.md"
require_file "${ROOT_DIR}/v1.3-roadmap.md"
require_file "${ROOT_DIR}/docs/fanqie-chapter-length-policy.json"
require_file "${ROOT_DIR}/shared/templates/state-schema-v5.json"
require_file "${ROOT_DIR}/shared/templates/learned-patterns.schema.json"
require_file "${ROOT_DIR}/shared/templates/workflow-state-v2.schema.json"
require_file "${ROOT_DIR}/shared/templates/state-archive-v1.json"
require_file "${ROOT_DIR}/shared/templates/profile-contract-v1.schema.json"
require_file "${ROOT_DIR}/shared/templates/acquire-provider-registry-v1.json"
require_file "${ROOT_DIR}/shared/templates/memory-context-v1.schema.json"
require_file "${ROOT_DIR}/shared/templates/content-positioning-v1.schema.json"
require_file "${ROOT_DIR}/shared/templates/content-positioning-map-v1.json"
require_file "${ROOT_DIR}/shared/templates/sidecar-freshness-registry-v1.json"
require_file "${ROOT_DIR}/shared/sync-governance.json"
require_file "${ROOT_DIR}/scripts/review-sync-queue.py"
require_file "${ROOT_DIR}/scripts/profile_contract.py"
require_file "${ROOT_DIR}/scripts/build_memory_context.py"
require_file "${ROOT_DIR}/scripts/build_content_positioning.py"
require_file "${ROOT_DIR}/scripts/build_project_knowledge_projection.py"
require_file "${ROOT_DIR}/scripts/build_workflow_health_bundle.py"
require_file "${ROOT_DIR}/scripts/render_workflow_health_summary.py"
require_file "${ROOT_DIR}/scripts/project_knowledge_mcp_server.py"
require_file "${ROOT_DIR}/scripts/audit_chapter_structure_repetition.py"
require_file "${ROOT_DIR}/scripts/project_regression_smoke.py"
require_file "${ROOT_DIR}/scripts/workflow_health_smoke.py"
require_file "${ROOT_DIR}/scripts/generate_snapshot.py"
require_file "${ROOT_DIR}/scripts/trace_log.py"
require_file "${ROOT_DIR}/scripts/post-task-maintenance.py"
require_file "${ROOT_DIR}/scripts/check-batch-quality-gate.py"
require_file "${ROOT_DIR}/scripts/thin-state.py"
require_file "${ROOT_DIR}/scripts/split-runtime-guidance.py"
require_file "${ROOT_DIR}/scripts/project-maintenance.py"

echo "Migration validation passed"
