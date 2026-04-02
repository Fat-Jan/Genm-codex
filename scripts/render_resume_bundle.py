#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_memory_context_summary as memory_summary
from trace_log import append_trace


DEFAULT_HANDOFF_PATH = Path('.mighty') / 'resume-handoff.md'
DEFAULT_BUNDLE_PATH = Path('.mighty') / 'resume-bundle.json'
DEFAULT_THREAD_MESSAGE_PATH = Path('.mighty') / 'new-thread-message.txt'
CLIPBOARD_COMMANDS: list[list[str]] = [
    ['pbcopy'],
    ['wl-copy'],
    ['xclip', '-selection', 'clipboard'],
    ['xsel', '--clipboard', '--input'],
    ['clip.exe'],
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Render a resume bundle: handoff + memory summary + new-thread message.')
    parser.add_argument('project_root', help='Novel project root')
    parser.add_argument('--timestamp', default='')
    parser.add_argument('--goal', default='', help='One-line current goal')
    parser.add_argument('--done', action='append', default=[], help='Extra verified completed fact (repeatable)')
    parser.add_argument('--file', dest='files', action='append', default=[], help="Extra key file in 'path: note' form (repeatable)")
    parser.add_argument('--blocker', default='', help='Current blocker')
    parser.add_argument('--next', action='append', default=[], help='Next step (repeatable)')
    parser.add_argument('--verify', action='append', default=[], help='Verification command or path (repeatable)')
    parser.add_argument('--constraint', action='append', default=[], help='Constraint that must be preserved (repeatable)')
    parser.add_argument('--ignore', action='append', default=[], help='Old context that can be ignored (repeatable)')
    parser.add_argument('--sync-openmemory', choices=['auto', 'on', 'off'], default='auto')
    parser.add_argument('--force-sync', action='store_true')
    parser.add_argument('--user-id', default='')
    parser.add_argument('--config-path', default=str(memory_summary.memory_sync.DEFAULT_CONFIG_PATH))
    parser.add_argument('--skip-refresh-memory-context', action='store_true')
    parser.add_argument('--handoff-output', default='')
    parser.add_argument('--bundle-output', default='')
    parser.add_argument('--thread-message-output', default='')
    parser.add_argument('--copy-handoff', action='store_true', help='Best-effort copy generated handoff markdown to system clipboard')
    parser.add_argument('--copy-thread-message', action='store_true', help='Best-effort copy generated new-thread message to system clipboard')
    return parser.parse_args(argv)


def bullet_list(items: list[str], placeholder: str, *, ordered: bool = False) -> str:
    clean = [item.strip() for item in items if item and item.strip()]
    if not clean:
        clean = [placeholder]
    if ordered:
        return '\n'.join(f'{idx}. {item}' for idx, item in enumerate(clean, start=1))
    return '\n'.join(f'- {item}' for item in clean)


def copy_to_clipboard(content: str) -> tuple[str | None, str | None]:
    failures: list[str] = []
    for command in CLIPBOARD_COMMANDS:
        if shutil.which(command[0]) is None:
            continue
        try:
            subprocess.run(command, input=content, text=True, check=True, capture_output=True)
            return command[0], None
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or '').strip()
            failures.append(f"{command[0]}: {stderr or exc.returncode}")
    if failures:
        return None, '; '.join(failures)
    return None, 'No supported clipboard command found'


def render_memory_summary(root: Path, args: argparse.Namespace, *, timestamp: str) -> tuple[dict[str, Any], dict[str, Any], Path, Path]:
    markdown_path = root / memory_summary.DEFAULT_MARKDOWN_PATH
    json_path = root / memory_summary.DEFAULT_JSON_PATH
    if args.skip_refresh_memory_context:
        memory_context_payload = memory_summary.read_json(root / '.mighty' / 'memory-context.json')
        if not memory_context_payload:
            memory_context_payload = memory_summary.refresh_memory_context(root, timestamp=timestamp)
    else:
        memory_context_payload = memory_summary.refresh_memory_context(root, timestamp=timestamp)

    sync_result = memory_summary.maybe_sync_openmemory(
        root,
        timestamp=timestamp,
        mode=args.sync_openmemory,
        user_id=memory_summary.resolve_user_id(root, args.user_id),
        config_path=Path(args.config_path).expanduser(),
        force_sync=args.force_sync,
    )
    summary = memory_summary.build_summary_payload(root, memory_context_payload, sync_result)
    memory_summary.write_json(json_path, summary)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(memory_summary.render_markdown(summary), encoding='utf-8')
    append_trace(
        root,
        event='memory_summary.rendered',
        skill='render_memory_context_summary',
        result=sync_result.get('status') or 'success',
        details={
            'markdown_file': str(markdown_path),
            'json_file': str(json_path),
            'sync_status': sync_result.get('status'),
        },
        timestamp=timestamp,
    )
    result = {
        'project': str(root),
        'memory_context_file': str(root / '.mighty' / 'memory-context.json'),
        'markdown_file': str(markdown_path),
        'json_file': str(json_path),
        'openmemory_sync_status': sync_result.get('status'),
        'resume_hint': summary['resume_hint'],
    }
    return result, summary, markdown_path, json_path


def default_done_facts(summary: dict[str, Any], memory_markdown_path: Path, sync_status: str | None) -> list[str]:
    workflow = summary.get('workflow', {})
    gate = summary.get('gate', {})
    return [
        f'已生成 memory summary：{memory_markdown_path}',
        f"当前进度：chapter={summary.get('current_chapter')}, words={summary.get('total_words')}",
        f"当前状态：workflow={workflow.get('status')}/{workflow.get('last_successful_checkpoint')}, gate={gate.get('status')}, openmemory_sync={sync_status}",
    ]


def default_key_files(root: Path, memory_markdown_path: Path, memory_json_path: Path) -> list[str]:
    files = [
        f'{memory_markdown_path}: 当前 memory summary（给人看）',
        f'{memory_json_path}: 当前 memory summary（给脚本/agent 读）',
        f'{root / ".mighty" / "memory-context.json"}: 安全 memory context 原文',
    ]
    sync_report = root / '.mighty' / 'memory-sync-report.json'
    if sync_report.exists():
        files.append(f'{sync_report}: 最近一次 OpenMemory sync 结果')
    return files


def default_blocker(summary: dict[str, Any], explicit: str) -> str:
    if explicit.strip():
        return explicit.strip()
    gate = summary.get('gate', {})
    sync_state = summary.get('openmemory_sync', {})
    if gate.get('status') not in (None, 'passed'):
        return str(gate.get('minimal_next_reason') or f"gate={gate.get('status')}")
    if sync_state.get('status') == 'failed':
        return str(sync_state.get('reason') or 'OpenMemory sync failed')
    return '无明确 blocker；按 next_action 继续即可。'


def default_next_steps(summary: dict[str, Any], explicit: list[str]) -> list[str]:
    clean = [item.strip() for item in explicit if item and item.strip()]
    if clean:
        return clean
    gate = summary.get('gate', {})
    next_action = gate.get('minimal_next_action')
    if next_action:
        return [f'执行 {next_action}', '根据 memory-summary.md 的 resume hint 在新线程继续']
    return ['阅读 memory-summary.md 后继续当前阶段任务']


def default_verification(memory_markdown_path: Path, memory_json_path: Path, explicit: list[str]) -> list[str]:
    clean = [item.strip() for item in explicit if item and item.strip()]
    if clean:
        return clean
    return [f'检查 {memory_markdown_path} 与 {memory_json_path} 已更新']


def default_constraints(summary: dict[str, Any], explicit: list[str]) -> list[str]:
    clean = [item.strip() for item in explicit if item and item.strip()]
    forbidden = summary.get('memory_contract', {}).get('forbidden_sync', [])
    if forbidden:
        clean.insert(0, f"不要把 {', '.join(forbidden)} 重新塞回上下文或记忆库")
    if not clean:
        clean = ['不要回放旧长历史']
    return clean


def default_ignore(explicit: list[str]) -> list[str]:
    clean = [item.strip() for item in explicit if item and item.strip()]
    if clean:
        return clean
    return ['旧长聊天历史', '整份工具输出', '完整章节正文', '全量日志']


def build_handoff_markdown(
    root: Path,
    args: argparse.Namespace,
    *,
    timestamp: str,
    summary: dict[str, Any],
    memory_markdown_path: Path,
    memory_json_path: Path,
) -> str:
    goal = args.goal.strip() or summary.get('resume_hint') or '<一句话目标>'
    done = default_done_facts(summary, memory_markdown_path, summary.get('openmemory_sync', {}).get('status')) + list(args.done)
    key_files = default_key_files(root, memory_markdown_path, memory_json_path) + list(args.files)
    blocker = default_blocker(summary, args.blocker)
    next_steps = default_next_steps(summary, args.next)
    verification = default_verification(memory_markdown_path, memory_json_path, args.verify)
    constraints = default_constraints(summary, args.constraint)
    ignore = default_ignore(args.ignore)
    return f"""继续这个任务，但不要回放旧长历史；把下面内容当作新的起点。

> generated_by: render_resume_bundle.py
> generated_at: {timestamp}

# 目标
- {goal}

# 当前工作区
- cwd: {root}
- 相关仓库/项目: {root}

# 已完成（仅保留已验证事实）
{bullet_list(done, '<事实 1>')}

# 关键文件
{bullet_list(key_files, '<path/a>: <一句话说明>')}

# 当前阻塞
- {blocker}

# 下一步
{bullet_list(next_steps, '<下一步 1>', ordered=True)}

# 验证方式
{bullet_list(verification, '<命令 / 测试 / 手工验证路径>')}

# 必须保留的约束
{bullet_list(constraints, '<约束 1>')}

# 可忽略的旧上下文
{bullet_list(ignore, '<哪些旧讨论不用再带>')}
"""


def build_thread_message(
    root: Path,
    *,
    summary: dict[str, Any],
    handoff_path: Path,
    memory_markdown_path: Path,
    memory_json_path: Path,
    goal: str,
) -> str:
    gate = summary.get('gate', {}) if isinstance(summary.get('gate'), dict) else {}
    workflow = summary.get('workflow', {}) if isinstance(summary.get('workflow'), dict) else {}
    contract = summary.get('memory_contract', {}) if isinstance(summary.get('memory_contract'), dict) else {}
    forbidden = contract.get('forbidden_sync', []) if isinstance(contract.get('forbidden_sync'), list) else []
    forbidden_text = ', '.join(forbidden) if forbidden else '长日志和完整正文'
    return f"""继续这个任务，但不要回放旧长历史。\n\n当前目标：{goal}\n项目根目录：{root}\n\n我已经准备好了恢复材料，请先把下面文件当作当前任务起点：\n- {handoff_path}\n- {memory_markdown_path}\n- {memory_json_path}\n\n请按这个顺序继续：\n1. 先用以上恢复材料理解当前状态，不要重扫整个项目。\n2. 以 handoff 为主，以 memory-summary.json 为结构化事实源。\n3. 仅在需要时再读取 handoff 中列出的关键文件。\n\n当前恢复摘要：\n- chapter={summary.get('current_chapter')}\n- words={summary.get('total_words')}\n- workflow={workflow.get('status')}/{workflow.get('last_successful_checkpoint')}\n- gate={gate.get('status')}\n- next_action={gate.get('minimal_next_action')}\n- resume_hint={summary.get('resume_hint')}\n\n约束：\n- 不要回放旧长历史。\n- 不要把 {forbidden_text} 重新塞回上下文。\n- 如果需要更多细节，只按需读取恢复材料提到的文件。\n"""


def main(argv: list[str] | None = None) -> dict[str, Any]:
    args = parse_args(argv)
    root = Path(args.project_root)
    ts = args.timestamp or now_iso()
    handoff_path = root / Path(args.handoff_output) if args.handoff_output else root / DEFAULT_HANDOFF_PATH
    bundle_path = root / Path(args.bundle_output) if args.bundle_output else root / DEFAULT_BUNDLE_PATH
    thread_message_path = root / Path(args.thread_message_output) if args.thread_message_output else root / DEFAULT_THREAD_MESSAGE_PATH

    memory_result, summary, memory_markdown_path, memory_json_path = render_memory_summary(root, args, timestamp=ts)
    goal = args.goal.strip() or summary.get('resume_hint') or '<一句话目标>'
    handoff = build_handoff_markdown(
        root,
        args,
        timestamp=ts,
        summary=summary,
        memory_markdown_path=memory_markdown_path,
        memory_json_path=memory_json_path,
    )
    handoff_path.parent.mkdir(parents=True, exist_ok=True)
    handoff_path.write_text(handoff, encoding='utf-8')

    thread_message = build_thread_message(
        root,
        summary=summary,
        handoff_path=handoff_path,
        memory_markdown_path=memory_markdown_path,
        memory_json_path=memory_json_path,
        goal=goal,
    )
    thread_message_path.parent.mkdir(parents=True, exist_ok=True)
    thread_message_path.write_text(thread_message, encoding='utf-8')

    handoff_copy_status = None
    handoff_copy_error = None
    if args.copy_handoff:
        handoff_copy_status, handoff_copy_error = copy_to_clipboard(handoff)

    thread_message_copy_status = None
    thread_message_copy_error = None
    if args.copy_thread_message:
        thread_message_copy_status, thread_message_copy_error = copy_to_clipboard(thread_message)

    bundle = {
        'version': '1.0',
        'project_root': str(root),
        'generated_at': ts,
        'handoff_file': str(handoff_path),
        'new_thread_message_file': str(thread_message_path),
        'memory_summary_markdown_file': str(memory_markdown_path),
        'memory_summary_json_file': str(memory_json_path),
        'memory_context_file': memory_result['memory_context_file'],
        'openmemory_sync_status': memory_result['openmemory_sync_status'],
        'resume_hint': memory_result['resume_hint'],
        'copy_handoff': {
            'requested': bool(args.copy_handoff),
            'clipboard_command': handoff_copy_status,
            'error': handoff_copy_error,
        },
        'copy_thread_message': {
            'requested': bool(args.copy_thread_message),
            'clipboard_command': thread_message_copy_status,
            'error': thread_message_copy_error,
        },
    }
    memory_summary.write_json(bundle_path, bundle)
    trace_log_path = append_trace(
        root,
        event='resume_bundle.rendered',
        skill='render_resume_bundle',
        result='success',
        details={
            'handoff_file': str(handoff_path),
            'thread_message_file': str(thread_message_path),
            'bundle_file': str(bundle_path),
            'memory_summary_markdown_file': str(memory_markdown_path),
            'copy_handoff': bool(args.copy_handoff),
            'copy_handoff_error': handoff_copy_error,
            'copy_thread_message': bool(args.copy_thread_message),
            'copy_thread_message_error': thread_message_copy_error,
        },
        timestamp=ts,
    )
    result = {
        'project': str(root),
        'handoff_file': str(handoff_path),
        'new_thread_message_file': str(thread_message_path),
        'bundle_file': str(bundle_path),
        'memory_summary_markdown_file': str(memory_markdown_path),
        'memory_summary_json_file': str(memory_json_path),
        'trace_log_file': str(trace_log_path),
        'openmemory_sync_status': memory_result['openmemory_sync_status'],
        'resume_hint': memory_result['resume_hint'],
        'copy_handoff_clipboard_command': handoff_copy_status,
        'copy_handoff_error': handoff_copy_error,
        'copy_thread_message_clipboard_command': thread_message_copy_status,
        'copy_thread_message_error': thread_message_copy_error,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    main()
