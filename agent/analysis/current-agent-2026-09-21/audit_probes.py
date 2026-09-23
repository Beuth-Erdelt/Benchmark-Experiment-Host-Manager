"""Reproduce review findings offline using temporary files and a scripted model.

Run from the repository root. No model API or Kubernetes call is made.
The sole process-launch path exercised is replaced with unittest.mock.
These probes document current behavior; they are not a corrected test suite.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
from unittest import mock

from agent.harness import agent, tools
from agent.harness.model_client import ChatModel, ToolCall
from tests.test_agent_harness import (
    WorkspaceTest, _Model, _SPEC, _REPORT_PATH, _RESULT_CONTRACT_PATH,
    _tool_reply, _text_reply, _record_arguments, _evidence_record_reply,
)


def main() -> None:
    """Print observable results without contacting external services."""
    findings = {}
    fixture = WorkspaceTest()
    fixture.setUp()
    try:
        workspace = fixture.workspace
        # The default design workspace permits an already existing result.
        findings['design_can_read_existing_result'] = 'text' in workspace.read_file(_REPORT_PATH)

        # A valid existing draft can be validated/submitted without contract reads.
        workspace.write_file(fixture.path, _SPEC)
        model = _Model([
            _tool_reply(ToolCall('v', 'validate', {'path': fixture.path})),
            _tool_reply(ToolCall('s', 'submit', {'path': fixture.path})),
            _text_reply('Done.'),
        ])
        with (
            mock.patch('agent.harness.tools.subprocess.Popen') as launch,
            mock.patch.object(workspace, '_await_result_folder', return_value='timeout'),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            launch.return_value = mock.Mock(pid=os.getpid(), returncode=None)
            outcome = agent.run_design(
                task='Offline audit', workspace=workspace, model=model,
                trajectory=agent.Trajectory(fixture.run),
                catalog_path='contracts/contract_catalog.yml', catalog_sha256='audit',
                environment_path='environment.yml', dry_run=True,
            )
        findings['dry_run_dispatched_submit_with_mocked_process'] = bool(outcome['code']) and launch.called
        findings['submit_was_absent_from_advertised_tools'] = all('submit' not in names for names in model.tool_sets)
        findings['submission_without_contract_reads'] = bool(outcome['code'])
        command = launch.call_args.args[0]
        launch_catalog = command[command.index('--catalog') + 1]
        findings['initial_launch_uses_live_catalog'] = launch_catalog == workspace.catalog_path
        findings['initial_launch_catalog_is_staged_snapshot'] = Path(launch_catalog).name == 'submitted-contract_catalog.yml'

        # Evidence interpretation dispatches a write it never advertises.
        record = _record_arguments(
            [{'question': 'Is performance proved?', 'status': 'settled',
              'conclusion': 'The metric is 999.', 'evidence': 'Invented number.', 'missing': ''}],
            hypothesis_verdict={'status': 'supported', 'conclusion': 'The metric is 999.',
                                'evidence_paths': [_REPORT_PATH]},
        )
        model = _Model([
            _tool_reply(ToolCall('w', 'write_file', {'path': 'inbox/unadvertised.yml', 'text': _SPEC})),
            _evidence_record_reply('r', record),
            _text_reply('Contradictory closing prose: the hypothesis was refuted.'),
        ])
        with contextlib.redirect_stdout(io.StringIO()):
            result = agent._interpret_evidence(
                [], workspace, model, agent.Trajectory(fixture.run),
                _REPORT_PATH, _RESULT_CONTRACT_PATH,
            )
        findings['interpretation_dispatched_unadvertised_write'] = (workspace.inbox / 'unadvertised.yml').exists()
        findings['write_was_absent_from_interpretation_tools'] = all('write_file' not in names for names in model.tool_sets)
        findings['unsupported_numeric_conclusion_recorded'] = result[1].get('status') == 'supported'
        findings['contradictory_closing_prose_accepted'] = result[0].startswith('Contradictory')

        broken = fixture.root / 'broken-trajectory'
        broken.mkdir()
        (broken / 'trajectory.jsonl').write_text('{"type":"task","text":"Question"}\n{"type":')
        try:
            agent._carry_forward(broken, fixture.root)
        except json.JSONDecodeError:
            findings['carry_forward_rejects_partial_tail'] = True
        else:
            findings['carry_forward_rejects_partial_tail'] = False

        adapter = ChatModel.__new__(ChatModel)
        adapter._counted_messages = 2
        adapter._counted_prompt_tokens = 5000
        fresh_messages = [{'role': 'system', 'content': 'New context'}, {'role': 'user', 'content': 'New question'}]
        inherited = adapter._prompt_tokens(fresh_messages)
        adapter._counted_messages = 0
        fresh = adapter._prompt_tokens(fresh_messages)
        findings['token_estimate_reuses_old_context_anchor'] = {'inherited_estimate': inherited, 'fresh_estimate': fresh}
        print(json.dumps(findings, indent=2))
    finally:
        fixture.tearDown()


if __name__ == '__main__':
    main()
