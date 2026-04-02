import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / 'scripts' / 'render_memory_context_summary.py'


def load_module():
    spec = importlib.util.spec_from_file_location('render_memory_context_summary', MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Unable to load module from {MODULE_PATH}')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def scaffold_project(root: Path) -> None:
    write_json(
        root / '.mighty' / 'state.json',
        {
            'meta': {
                'title': 'Memory Summary Test',
                'updated_at': '2026-04-02T00:00:00Z',
            },
            'progress': {
                'current_chapter': 12,
                'last_write_chapter': 12,
                'total_words': 36343,
            },
            'active_context': {'hook_count': 2, 'guardrail_count': 0},
            'launch_stack_phase': 'draft',
            'launch_stack_drift_signal': 'watch',
        },
    )
    write_json(
        root / '.mighty' / 'workflow_state.json',
        {
            'current_task': {
                'status': 'completed',
                'current_step': None,
                'last_successful_checkpoint': 'snapshot',
            }
        },
    )
    write_json(
        root / '.mighty' / 'setting-gate.json',
        {
            'status': 'passed',
            'blocking_gaps': [],
            'minimal_next_action': {'action': 'novel-write', 'reason': '继续下一章'},
        },
    )
    write_json(root / '.mighty' / 'active-context.json', {'summary_window': {'latest_chapter': '12'}})
    write_text(root / 'chapters' / '第012章.md', '已完成章节。' * 100)


class MemoryContextSummaryTests(unittest.TestCase):
    def test_build_summary_payload_keeps_resume_facts_compact(self) -> None:
        module = load_module()
        root = Path('/tmp/demo-project')
        payload = {
            'title': '测试项目',
            'generated_at': '2026-04-02T00:00:00Z',
            'safe_for_mcp_memory': True,
            'current_chapter': 12,
            'total_words': 36343,
            'workflow': {'status': 'completed', 'current_step': None, 'last_successful_checkpoint': 'snapshot'},
            'gate': {'status': 'passed', 'minimal_next_action': 'novel-write', 'minimal_next_reason': '继续下一章'},
            'launch_stack': {'phase': 'draft', 'drift_signal': 'watch'},
            'active_context_summary': {'hook_count': 2, 'guardrail_count': 0, 'latest_summary_chapter': '12'},
            'memory_contract': {
                'truth_source': 'local_files',
                'allowed_sync': ['workflow_summary', 'next_action_hint'],
                'forbidden_sync': ['full_state_json', 'chapter_prose'],
            },
        }
        sync_result = {'status': 'stored', 'memory_id': 'mem-123', 'reason': None}

        summary = module.build_summary_payload(root, payload, sync_result)

        self.assertEqual(summary['openmemory_sync']['status'], 'stored')
        self.assertEqual(summary['memory_contract']['truth_source'], 'local_files')
        self.assertIn('chapter 12', summary['resume_hint'])
        self.assertIn('next_action=novel-write', summary['resume_hint'])

    def test_main_writes_markdown_and_json_outputs(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)
            write_json(
                root / '.mighty' / 'memory-sync-report.json',
                {'status': 'stored', 'memory_id': 'mem-123', 'reason': None},
            )

            with mock.patch.object(module, 'append_trace', return_value=root / '.mighty' / 'logs' / 'trace.jsonl'):
                result = module.main([str(root), '--sync-openmemory', 'off'])

            markdown = (root / '.mighty' / 'memory-summary.md').read_text(encoding='utf-8')
            payload = json.loads((root / '.mighty' / 'memory-summary.json').read_text(encoding='utf-8'))

            self.assertEqual(result['openmemory_sync_status'], 'stored')
            self.assertIn('Memory Summary Test', markdown)
            self.assertIn('openmemory_sync: status=stored', markdown)
            self.assertEqual(payload['openmemory_sync']['memory_id'], 'mem-123')
            self.assertEqual(payload['gate']['minimal_next_action'], 'novel-write')


if __name__ == '__main__':
    unittest.main()
