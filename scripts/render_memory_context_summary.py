#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_memory_context as memory_context_builder
import sync_memory_context_to_openmemory as memory_sync
from trace_log import append_trace


DEFAULT_MARKDOWN_PATH = Path('.mighty') / 'memory-summary.md'
DEFAULT_JSON_PATH = Path('.mighty') / 'memory-summary.json'


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Render a compact memory summary and optionally sync OpenMemory.')
    parser.add_argument('project_root', help='Novel project root')
    parser.add_argument('--timestamp', default='')
    parser.add_argument('--sync-openmemory', choices=['auto', 'on', 'off'], default='auto')
    parser.add_argument('--force-sync', action='store_true')
    parser.add_argument('--user-id', default='')
    parser.add_argument('--config-path', default=str(memory_sync.DEFAULT_CONFIG_PATH))
    parser.add_argument('--skip-refresh-memory-context', action='store_true')
    parser.add_argument('--output-markdown', default='')
    parser.add_argument('--output-json', default='')
    return parser.parse_args(argv)


def resolve_user_id(project_root: Path, explicit_user_id: str) -> str:
    project_config = memory_sync.read_project_config(project_root)
    memory_sync_cfg = project_config.get('memory_sync', {})
    openmemory_cfg = memory_sync_cfg.get('openmemory', {}) if isinstance(memory_sync_cfg, dict) else {}
    return (
        explicit_user_id
        or str(openmemory_cfg.get('user_id') or '')
        or os.environ.get('GENM_OPENMEMORY_USER_ID', 'genm-codex')
    )


def refresh_memory_context(project_root: Path, *, timestamp: str) -> dict[str, Any]:
    payload = memory_context_builder.build_memory_context(project_root, timestamp=timestamp)
    output_path = project_root / '.mighty' / 'memory-context.json'
    write_json(output_path, payload)
    return payload


def maybe_sync_openmemory(
    project_root: Path,
    *,
    timestamp: str,
    mode: str,
    user_id: str,
    config_path: Path,
    force_sync: bool,
) -> dict[str, Any]:
    if mode == 'off':
        existing = read_json(project_root / memory_sync.REPORT_PATH)
        return existing or {
            'status': 'skipped',
            'reason': 'sync-disabled-for-summary',
        }
    result = memory_sync.sync_memory_context(
        project_root,
        timestamp=timestamp,
        mode=mode,
        user_id=user_id,
        config_path=config_path,
        force=force_sync,
        dry_run=False,
    )
    memory_sync.write_report(project_root, result)
    return result


def build_summary_payload(project_root: Path, memory_context_payload: dict[str, Any], sync_result: dict[str, Any]) -> dict[str, Any]:
    workflow = memory_context_payload.get('workflow', {}) if isinstance(memory_context_payload.get('workflow'), dict) else {}
    gate = memory_context_payload.get('gate', {}) if isinstance(memory_context_payload.get('gate'), dict) else {}
    launch_stack = memory_context_payload.get('launch_stack', {}) if isinstance(memory_context_payload.get('launch_stack'), dict) else {}
    active = memory_context_payload.get('active_context_summary', {}) if isinstance(memory_context_payload.get('active_context_summary'), dict) else {}
    contract = memory_context_payload.get('memory_contract', {}) if isinstance(memory_context_payload.get('memory_contract'), dict) else {}

    return {
        'version': '1.0',
        'project_root': str(project_root),
        'title': memory_context_payload.get('title', ''),
        'generated_at': memory_context_payload.get('generated_at', ''),
        'safe_for_mcp_memory': bool(memory_context_payload.get('safe_for_mcp_memory')),
        'current_chapter': memory_context_payload.get('current_chapter', 0),
        'total_words': memory_context_payload.get('total_words', 0),
        'workflow': {
            'status': workflow.get('status'),
            'current_step': workflow.get('current_step'),
            'last_successful_checkpoint': workflow.get('last_successful_checkpoint'),
        },
        'gate': {
            'status': gate.get('status'),
            'blocking_gap_keys': gate.get('blocking_gap_keys', []),
            'minimal_next_action': gate.get('minimal_next_action'),
            'minimal_next_reason': gate.get('minimal_next_reason'),
        },
        'launch_stack': {
            'phase': launch_stack.get('phase'),
            'drift_signal': launch_stack.get('drift_signal'),
        },
        'active_context_summary': {
            'hook_count': active.get('hook_count', 0),
            'guardrail_count': active.get('guardrail_count', 0),
            'latest_summary_chapter': active.get('latest_summary_chapter'),
        },
        'memory_contract': {
            'truth_source': contract.get('truth_source'),
            'allowed_sync': contract.get('allowed_sync', []),
            'forbidden_sync': contract.get('forbidden_sync', []),
        },
        'openmemory_sync': {
            'status': sync_result.get('status'),
            'reason': sync_result.get('reason'),
            'memory_id': sync_result.get('memory_id'),
        },
        'resume_hint': (
            f"Continue from chapter {memory_context_payload.get('current_chapter', 0)}; "
            f"workflow={workflow.get('status')}/{workflow.get('last_successful_checkpoint')}; "
            f"gate={gate.get('status')}; next_action={gate.get('minimal_next_action')}."
        ),
    }


def render_markdown(summary: dict[str, Any]) -> str:
    workflow = summary['workflow']
    gate = summary['gate']
    launch_stack = summary['launch_stack']
    active = summary['active_context_summary']
    sync_state = summary['openmemory_sync']
    contract = summary['memory_contract']
    allowed = ', '.join(contract.get('allowed_sync') or []) or 'none'
    forbidden = ', '.join(contract.get('forbidden_sync') or []) or 'none'
    return f"""# Memory Summary

- project: {summary['title'] or Path(summary['project_root']).name}
- project_root: {summary['project_root']}
- generated_at: {summary['generated_at']}
- safe_for_mcp_memory: {str(summary['safe_for_mcp_memory']).lower()}
- current_chapter: {summary['current_chapter']}
- total_words: {summary['total_words']}
- workflow: {workflow.get('status')}/{workflow.get('last_successful_checkpoint')} (current_step={workflow.get('current_step')})
- gate: {gate.get('status')}
- next_action: {gate.get('minimal_next_action')} ({gate.get('minimal_next_reason')})
- launch_stack: {launch_stack.get('phase')}/{launch_stack.get('drift_signal')}
- active_context: hooks={active.get('hook_count')}, guardrails={active.get('guardrail_count')}, latest_summary_chapter={active.get('latest_summary_chapter')}
- openmemory_sync: status={sync_state.get('status')}, reason={sync_state.get('reason')}, memory_id={sync_state.get('memory_id')}
- truth_source: {contract.get('truth_source')}
- allowed_sync: {allowed}
- forbidden_sync: {forbidden}

## Resume Hint

{summary['resume_hint']}
"""


def main(argv: list[str] | None = None) -> dict[str, Any]:
    args = parse_args(argv)
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    markdown_path = root / Path(args.output_markdown) if args.output_markdown else root / DEFAULT_MARKDOWN_PATH
    json_path = root / Path(args.output_json) if args.output_json else root / DEFAULT_JSON_PATH

    if args.skip_refresh_memory_context:
        memory_context_payload = read_json(root / '.mighty' / 'memory-context.json')
        if not memory_context_payload:
            memory_context_payload = refresh_memory_context(root, timestamp=ts)
    else:
        memory_context_payload = refresh_memory_context(root, timestamp=ts)

    sync_result = maybe_sync_openmemory(
        root,
        timestamp=ts,
        mode=args.sync_openmemory,
        user_id=resolve_user_id(root, args.user_id),
        config_path=Path(args.config_path).expanduser(),
        force_sync=args.force_sync,
    )
    summary = build_summary_payload(root, memory_context_payload, sync_result)
    write_json(json_path, summary)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(render_markdown(summary), encoding='utf-8')
    trace_log_path = append_trace(
        root,
        event='memory_summary.rendered',
        skill='render_memory_context_summary',
        result=sync_result.get('status') or 'success',
        details={
            'markdown_file': str(markdown_path),
            'json_file': str(json_path),
            'sync_status': sync_result.get('status'),
        },
        timestamp=ts,
    )
    result = {
        'project': str(root),
        'memory_context_file': str(root / '.mighty' / 'memory-context.json'),
        'markdown_file': str(markdown_path),
        'json_file': str(json_path),
        'trace_log_file': str(trace_log_path),
        'openmemory_sync_status': sync_result.get('status'),
        'resume_hint': summary['resume_hint'],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    main()
