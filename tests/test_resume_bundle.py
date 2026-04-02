import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / 'scripts' / 'render_resume_bundle.py'


def load_module():
    spec = importlib.util.spec_from_file_location('render_resume_bundle', MODULE_PATH)
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
                'title': 'Resume Bundle Test',
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
    write_json(root / '.mighty' / 'memory-sync-report.json', {'status': 'stored', 'memory_id': 'mem-123', 'reason': None})
    write_text(root / 'chapters' / '第012章.md', '已完成章节。' * 100)


class ResumeBundleTests(unittest.TestCase):
    def test_main_writes_handoff_bundle_and_new_thread_message(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)

            with mock.patch.object(module, 'append_trace', return_value=root / '.mighty' / 'logs' / 'trace.jsonl'):
                result = module.main([str(root), '--sync-openmemory', 'off', '--goal', '继续推进项目'])

            handoff = (root / '.mighty' / 'resume-handoff.md').read_text(encoding='utf-8')
            bundle = json.loads((root / '.mighty' / 'resume-bundle.json').read_text(encoding='utf-8'))
            thread_message = (root / '.mighty' / 'new-thread-message.txt').read_text(encoding='utf-8')

            self.assertEqual(result['openmemory_sync_status'], 'stored')
            self.assertIn('继续推进项目', handoff)
            self.assertIn('执行 novel-write', handoff)
            self.assertIn('memory-summary.md', handoff)
            self.assertIn('继续这个任务，但不要回放旧长历史。', thread_message)
            self.assertIn('resume-handoff.md', thread_message)
            self.assertIn('memory-summary.json', thread_message)
            self.assertEqual(bundle['openmemory_sync_status'], 'stored')
            self.assertTrue(bundle['handoff_file'].endswith('.mighty/resume-handoff.md'))
            self.assertTrue(bundle['new_thread_message_file'].endswith('.mighty/new-thread-message.txt'))

    def test_copy_failures_recorded_without_failing_bundle(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            scaffold_project(root)

            with mock.patch.object(module, 'append_trace', return_value=root / '.mighty' / 'logs' / 'trace.jsonl'), \
                 mock.patch.object(module, 'copy_to_clipboard', side_effect=[(None, 'pbcopy: 1'), (None, 'pbcopy: 1')]):
                result = module.main([str(root), '--sync-openmemory', 'off', '--copy-handoff', '--copy-thread-message'])

            bundle = json.loads((root / '.mighty' / 'resume-bundle.json').read_text(encoding='utf-8'))
            self.assertIsNone(result['copy_handoff_clipboard_command'])
            self.assertEqual(result['copy_handoff_error'], 'pbcopy: 1')
            self.assertIsNone(result['copy_thread_message_clipboard_command'])
            self.assertEqual(result['copy_thread_message_error'], 'pbcopy: 1')
            self.assertEqual(bundle['copy_handoff']['error'], 'pbcopy: 1')
            self.assertEqual(bundle['copy_thread_message']['error'], 'pbcopy: 1')


if __name__ == '__main__':
    unittest.main()
