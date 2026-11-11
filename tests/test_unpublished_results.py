"""
Guard for DBMS whose benchmark results must not be published.

SQL Server: the license terms of the Developer edition (section "Benchmark
testing") require Microsoft's prior written approval to disclose benchmark
results (issue #834). CedarDB: its results are kept internal as well.
For these DBMS the repository may describe how to deploy and run them, but
holds no results:

* no committed file under ``logs_tests/`` (outside ``logs_tests/local/``,
  which is git-ignored) names the DBMS or contains one of its result markers,
* no page under ``docs/`` and no top-level Markdown file contains a result
  marker (configuration or pod names, SUT pod names, links to logs,
  ``Experiment is limited to DBMS [...]``),
* every test script that runs the DBMS (``-dbms <name>``) writes its logs to
  ``logs_tests/local``, set after loading the test functions (which default
  to ``logs_tests``) and never changed afterwards,
* ``logs_tests/local/*`` is git-ignored.

A test script that runs such a DBMS must not run published DBMS, since all
its logs go to ``logs_tests/local``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import glob
import os
import re
import subprocess
import unittest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: DBMS key (``-dbms``, configuration names) -> (slug in names of logs and pods, why).
UNPUBLISHED = {
    'SQLServer': ('sqlserver', 'license: results need Microsoft\'s prior written approval (#834)'),
    'CedarDB': ('cedardb', 'results are kept internal'),
}

#: Directory of the logs of these DBMS (git-ignored), as the scripts write it.
LOCAL_LOG_DIR = {
    'sh': re.compile(r'^LOG_DIR="\./logs_tests/local"\s*$'),
    'ps1': re.compile(r'^\$LOG_DIR\s*=\s*"\.\\logs_tests\\local"\s*$'),
}
#: Line that loads the test functions (which set LOG_DIR to logs_tests).
LOAD_FUNCTIONS = {
    'sh': re.compile(r'^(source|\.)\s+\./scripts/testfunctions\.sh\b'),
    'ps1': re.compile(r'^\.\s+\.?\\?scripts\\testfunctions\.ps1\b'),
}
ASSIGN_LOG_DIR = {
    'sh': re.compile(r'^\s*(export\s+)?LOG_DIR='),
    'ps1': re.compile(r'^\s*\$LOG_DIR\s*='),
}


def _markers(key, slug):
    """Regular expressions that only occur in results of the DBMS (case-insensitive)."""
    return [
        # configuration, connection and pod names: CedarDB-1, sqlserver-1-1-1-1-1
        re.compile(r'(?<![\w/.-])' + re.escape(slug) + r'-\d', re.IGNORECASE),
        # SUT pods of a run
        re.compile(r'bexhoma-sut-' + re.escape(slug), re.IGNORECASE),
        # links to logs or summaries outside logs_tests/local
        re.compile(r'logs_tests/(?!local/)\S*' + re.escape(slug), re.IGNORECASE),
        # workload section of a summary
        re.compile(r"limited to DBMS \[[^\]]*'" + re.escape(key) + r"'", re.IGNORECASE),
    ]


def _tracked(path):
    """Files under ``path`` that git tracks (all files when git is not available)."""
    try:
        out = subprocess.run(['git', 'ls-files', '-z', '--', path], cwd=_REPO,
                             capture_output=True, check=True).stdout
        return [f for f in out.decode('utf-8').split('\0') if f]
    except (OSError, subprocess.CalledProcessError):
        root = os.path.join(_REPO, path)
        return [os.path.relpath(os.path.join(d, f), _REPO).replace(os.sep, '/')
                for d, _, files in os.walk(root) for f in files]


def _read(rel):
    with open(os.path.join(_REPO, rel), encoding='utf-8', errors='replace') as f:
        return f.read()


def _hits(text, markers):
    """(line number, line) of every line matching one of the markers."""
    return [(n, line.strip()[:120]) for n, line in enumerate(text.splitlines(), 1)
            if any(m.search(line) for m in markers)]


class TestUnpublishedResults(unittest.TestCase):

    def test_no_logs_in_repository(self):
        files = [f for f in _tracked('logs_tests') if not f.startswith('logs_tests/local/')]
        self.assertTrue(files, 'no tracked logs found, the check would be void')
        for key, (slug, why) in UNPUBLISHED.items():
            markers = _markers(key, slug)
            for rel in files:
                with self.subTest(dbms=key, file=rel):
                    self.assertNotIn(slug, os.path.basename(rel).lower(),
                                     f'{rel}: log of {key} committed ({why})')
                    self.assertEqual(_hits(_read(rel), markers), [],
                                     f'{rel}: results of {key} ({why})')

    def test_no_results_in_docs(self):
        pages = sorted(glob.glob(os.path.join(_REPO, 'docs', '**', '*.md'), recursive=True)
                       + glob.glob(os.path.join(_REPO, '*.md')))
        self.assertTrue(pages)
        for key, (slug, why) in UNPUBLISHED.items():
            markers = _markers(key, slug)
            for page in pages:
                rel = os.path.relpath(page, _REPO).replace(os.sep, '/')
                with self.subTest(dbms=key, page=rel):
                    self.assertEqual(_hits(_read(rel), markers), [],
                                     f'{rel}: results of {key} ({why})')

    def test_scripts_log_locally(self):
        checked = set()
        for path in sorted(glob.glob(os.path.join(_REPO, 'scripts', '*.sh'))
                           + glob.glob(os.path.join(_REPO, 'scripts', '*.ps1'))):
            kind = 'sh' if path.endswith('.sh') else 'ps1'
            rel = os.path.relpath(path, _REPO).replace(os.sep, '/')
            lines = _read(rel).splitlines()
            runs = [k for k in UNPUBLISHED
                    if any(re.search(r'-dbms\s+' + k + r'\b', l) and not l.lstrip().startswith('#')
                           for l in lines)]
            if not runs:
                continue
            checked.update(runs)
            with self.subTest(script=rel):
                load = [i for i, l in enumerate(lines) if LOAD_FUNCTIONS[kind].search(l)]
                local = [i for i, l in enumerate(lines) if LOCAL_LOG_DIR[kind].search(l)]
                assigns = [i for i, l in enumerate(lines) if ASSIGN_LOG_DIR[kind].search(l)]
                first_run = min(i for i, l in enumerate(lines) if re.search(r'-dbms\s+\w', l)
                                and not l.lstrip().startswith('#'))
                self.assertTrue(load, f'{rel} runs {runs} but does not load the test functions')
                self.assertTrue(local, f'{rel} runs {runs} but does not write to logs_tests/local')
                self.assertGreater(local[0], load[0],
                                   f'{rel}: LOG_DIR is set before the test functions, which reset it')
                self.assertLess(local[0], first_run, f'{rel}: LOG_DIR is set after the first run')
                self.assertEqual([i for i in assigns if i > local[0]], [],
                                 f'{rel}: LOG_DIR is changed after it is set to logs_tests/local')
        self.assertEqual(checked, set(UNPUBLISHED),
                         'no test script runs these DBMS, the check would be void')

    def test_local_logs_ignored(self):
        with open(os.path.join(_REPO, '.gitignore'), encoding='utf-8') as f:
            ignored = [l.strip() for l in f]
        self.assertIn('logs_tests/local/*', ignored)


if __name__ == '__main__':
    unittest.main()
