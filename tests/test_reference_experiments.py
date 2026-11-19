"""
The reference experiments (scripts/test-reference-experiments.sh / .ps1) copy their
commands from the test-docs-* scripts, so that their logs are those of the
documentation. This checks that every copied command is still identical to its source.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import os
import re
import unittest

_SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
#: Comment line naming a run and its source: "#### 3. TPC-H refresh stream (test-docs-tpch.sh)".
_RUN = re.compile(r'^#### \d+\. .* \((test-docs-[a-z]+)\.(sh|ps1)\)$')
_LOG = {'sh': re.compile(r'\$LOG_DIR/(\w+)\.log'), 'ps1': re.compile(r'\$LOG_DIR\\(\w+)\.log')}


def _command(lines, log, kind):
    """The bexhoma command writing <log>.log, from its first line to the log line."""
    end = next(i for i, line in enumerate(lines) if (m := _LOG[kind].search(line)) and m.group(1) == log)
    start = end
    while not lines[start].lstrip().startswith('bexhoma '):
        start -= 1
    return [line.strip() for line in lines[start:end + 1]]


class ReferenceExperimentsTest(unittest.TestCase):

    def check(self, kind):
        with open(os.path.join(_SCRIPTS, f'test-reference-experiments.{kind}'), encoding='utf-8') as f:
            lines = f.read().splitlines()
        runs = [(i, m.group(1)) for i, line in enumerate(lines) if (m := _RUN.match(line))]
        self.assertGreaterEqual(len(runs), 10)
        for index, source in runs:
            log = next(m.group(1) for line in lines[index:] if (m := _LOG[kind].search(line)))
            with self.subTest(log=log):
                with open(os.path.join(_SCRIPTS, f'{source}.{kind}'), encoding='utf-8') as f:
                    source_lines = f.read().splitlines()
                self.assertEqual(_command(lines, log, kind), _command(source_lines, log, kind),
                                 f'{log}: command differs from {source}.{kind}')

    def test_sh(self):
        self.check('sh')

    def test_ps1(self):
        self.check('ps1')


if __name__ == '__main__':
    unittest.main()
