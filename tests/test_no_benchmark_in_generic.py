"""
Guard: nothing specific to a benchmark in the generic Python code (ratchet).

Design goal: a new benchmark is a new folder under ``bexhoma/benchmarks/`` (plus its
assets in ``experiments/``, ``images/`` and ``k8s/``) and needs no change in any generic
module. Generic code knows only the generic schema (phase, job, connection, pod count,
timings, monitoring metrics); everything else is supplied by the benchmark through a
hook, declared data or a capability flag.

This test scans the generic modules of the ``bexhoma`` package for the names of the
benchmarks and of their tools. Unlike the DBMS guard (:mod:`tests.test_no_dbms_in_python`),
it scans the whole text of a file, *including* docstrings and ``#`` comments: a comment
like "``terminals`` (Benchbase) or ``vusers`` (HammerDB)" marks code that reacts to the
specifics of a benchmark although no name appears in the code itself. Every hit is
either such a special case or a stale example that can be reworded.

Not scanned are the files that belong to one benchmark or tool (:func:`is_benchmark_file`);
they move to ``bexhoma/benchmarks/<name>/`` and are then exempt by their folder.

The existing occurrences are recorded per file in
``tests/benchmark_guard_baseline.json``. The test fails when a file gets *more*
occurrences of a name than recorded (a new violation) and also when it gets *fewer*
(shrink the baseline, so the gain is kept). Regenerate with::

    BEXHOMA_UPDATE_SNAPSHOTS=1 python -m pytest tests/test_no_benchmark_in_generic.py

The goal is an empty baseline.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import collections
import json
import os
import re
import unittest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PACKAGE = 'bexhoma'
_BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'benchmark_guard_baseline.json')
_UPDATE = os.environ.get('BEXHOMA_UPDATE_SNAPSHOTS') == '1'

#: Canonical name -> spellings of a benchmark or of its tool. A spelling matches as
#: written, not inside a longer word (see :func:`_pattern`).
NAMES = {
    'tpch': ('tpch', 'Tpch', 'TPCH', 'tpc-h', 'TPC-H'),
    'tpcds': ('tpcds', 'Tpcds', 'TPCDS', 'tpc-ds', 'TPC-DS'),
    'tpcc': ('tpcc', 'Tpcc', 'TPCC', 'tpc-c', 'TPC-C'),
    'ssb': ('ssb', 'Ssb', 'SSB'),
    'ycsb': ('ycsb', 'Ycsb', 'YCSB'),
    'benchbase': ('benchbase', 'Benchbase', 'BenchBase', 'BENCHBASE'),
    'hammerdb': ('hammerdb', 'Hammerdb', 'HammerDB', 'HAMMERDB'),
    'fio': ('fio', 'Fio', 'FIO'),
    'sysbench': ('sysbench', 'Sysbench', 'SYSBENCH'),
    'sockperf': ('sockperf', 'Sockperf', 'SOCKPERF'),
    'netperf': ('netperf', 'Netperf', 'NETPERF'),
}

#: "hardware" alone is a generic word (hardware metrics of the monitoring); these name the hardware benchmark.
_HARDWARE_BENCHMARK = re.compile(r'Hardware(?:Experiment|Evaluator|Collector)|HARDWARE_TYPE|hardware_type'
                                 r'|(?:experiments|evaluators|collectors|benchmarks)\.[Hh]ardware\b')

#: Files of the layer packages that belong to one benchmark or to one benchmarking tool.
#: They are moved to ``bexhoma/benchmarks/<name>/``; delete an entry when its file has moved.
_BENCHMARK_FILES = {
    # the descriptors of all benchmarks, until each benchmark has a folder of its own
    'bexhoma/benchmarks/registered.py',
    'bexhoma/benchmarks/benchbase.py', 'bexhoma/benchmarks/hardware.py',
    # the baseline of the cluster's hardware is a use of the hardware benchmark; bexhoma.environment
    # imports it, the one place where a generic module depends on a benchmark
    'bexhoma/hardware_baseline.py',
    'bexhoma/benchmarks/ssb.py', 'bexhoma/benchmarks/hammerdb.py', 'bexhoma/benchmarks/tpcds.py',
    'bexhoma/benchmarks/tpch.py',    'bexhoma/collectors/benchbase.py', 'bexhoma/collectors/hardware.py',
    'bexhoma/collectors/hammerdb.py',    'bexhoma/evaluators/benchbase.py', 'bexhoma/evaluators/hardware.py',
    'bexhoma/evaluators/hammerdb.py',    'bexhoma/experiments/benchbase.py', 'bexhoma/experiments/hardware.py',
    'bexhoma/experiments/ssb.py', 'bexhoma/experiments/hammerdb.py', 'bexhoma/experiments/tpcds.py',
    'bexhoma/experiments/tpch.py', 'bexhoma/experiments/tpch_builder.py', 'bexhoma/experiments/tpch_catalog.py',
    'bexhoma/experiments/tpch_loader.py',}


def is_benchmark_file(relative: str) -> bool:
    """Whether a file belongs to one benchmark: listed in :data:`_BENCHMARK_FILES` or in a folder of its own.

    :param relative: Repository-relative path with forward slashes.
    """
    if relative in _BENCHMARK_FILES:
        return True
    parts = relative.split('/')
    # bexhoma/benchmarks/<name>/<file>.py
    return len(parts) >= 4 and parts[0] == _PACKAGE and parts[1] == 'benchmarks'


def _pattern() -> re.Pattern:
    """A spelling matches as written, neither after a letter nor before a lower-case letter.

    So ``fio`` does not match ``profiorm`` and ``ssb`` not ``ssbar``, while ``TpchExperiment``
    and ``tpch_builder`` still match ``Tpch``/``tpch``.
    """
    spellings = sorted({s for group in NAMES.values() for s in group}, key=len, reverse=True)
    return re.compile(r'(?<![A-Za-z])(' + '|'.join(re.escape(s) for s in spellings) + r')(?![a-z])')


_CANONICAL = {spelling: name for name, group in NAMES.items() for spelling in group}


def count_names(text: str) -> dict:
    """``{canonical name: occurrences}`` of benchmark and tool names in a text."""
    counts = collections.Counter(_CANONICAL[match] for match in _pattern().findall(text))
    hardware = len(_HARDWARE_BENCHMARK.findall(text))
    if hardware:
        counts['hardware'] = hardware
    return dict(sorted(counts.items()))


def generic_files() -> list:
    """Repository-relative paths of the generic Python files of the package."""
    files = []
    for folder, _, names in os.walk(os.path.join(_REPO, _PACKAGE)):
        files += [os.path.relpath(os.path.join(folder, n), _REPO).replace('\\', '/') for n in names if n.endswith('.py')]
    return sorted(f for f in files if not is_benchmark_file(f))


def scan() -> dict:
    """``{file: {name: occurrences}}`` of benchmark names in the generic files, files without any left out."""
    result = {}
    for relative in generic_files():
        with open(os.path.join(_REPO, relative), encoding='utf-8') as file:
            counts = count_names(file.read())
        if counts:
            result[relative] = counts
    return result


class NoBenchmarkInGenericTest(unittest.TestCase):
    """Benchmark names in generic code may only decrease against the recorded baseline."""

    def test_baseline_is_not_exceeded_or_stale(self) -> None:
        actual = scan()
        if _UPDATE:
            with open(_BASELINE, 'w', encoding='utf-8', newline='\n') as file:
                json.dump(actual, file, indent=1, sort_keys=True)
                file.write('\n')
            return
        with open(_BASELINE, encoding='utf-8') as file:
            baseline = json.load(file)
        worse, better = [], []
        for relative in sorted(set(actual) | set(baseline)):
            now, before = actual.get(relative, {}), baseline.get(relative, {})
            for name in sorted(set(now) | set(before)):
                if now.get(name, 0) > before.get(name, 0):
                    worse.append(f'{relative}: {name} {before.get(name, 0)} -> {now[name]}')
                elif now.get(name, 0) < before.get(name, 0):
                    better.append(f'{relative}: {name} {before[name]} -> {now.get(name, 0)}')
        self.assertFalse(worse, 'a generic module names a benchmark (also in comments and docstrings); '
                                'supply it from the benchmark by a hook, declared data or a capability flag:\n'
                                + '\n'.join(worse))
        self.assertFalse(better, 'fewer benchmark names than the baseline, regenerate it '
                                 '(BEXHOMA_UPDATE_SNAPSHOTS=1) to keep the gain:\n' + '\n'.join(better))

    def test_benchmark_files_exist(self) -> None:
        """A moved or deleted file must leave the exemption list."""
        missing = sorted(f for f in _BENCHMARK_FILES if not os.path.exists(os.path.join(_REPO, f)))
        self.assertFalse(missing, 'remove from _BENCHMARK_FILES (moved or deleted):\n' + '\n'.join(missing))

    def test_comments_and_docstrings_are_scanned(self) -> None:
        text = '"""For YCSB."""\n\ndef f(threads_column):\n    # terminals (Benchbase) or vusers (HammerDB)\n    return 1\n'
        self.assertEqual(count_names(text), {'benchbase': 1, 'hammerdb': 1, 'ycsb': 1})

    def test_spellings_are_one_name(self) -> None:
        self.assertEqual(count_names("TPC-H tpch TpchExperiment tpch_builder 'tpc-h'"), {'tpch': 5})

    def test_generic_words_do_not_match(self) -> None:
        text = 'hardware metrics, refresh the token, refresh stream, refresh_template, profiorm, config, ssbar, Hardware\n'
        self.assertEqual(count_names(text), {})

    def test_hardware_benchmark_is_found(self) -> None:
        text = 'HardwareEvaluator experiments.HardwareExperiment(cluster) HARDWARE_TYPE fio\n'
        self.assertEqual(count_names(text), {'fio': 1, 'hardware': 3})

    def test_benchmark_folders_are_exempt(self) -> None:
        self.assertTrue(is_benchmark_file('bexhoma/benchmarks/ycsb/evaluator.py'))
        self.assertTrue(is_benchmark_file('bexhoma/experiments/tpch.py'))
        self.assertFalse(is_benchmark_file('bexhoma/benchmarks/base.py'))
        self.assertFalse(is_benchmark_file('bexhoma/benchmarks/__init__.py'))
        self.assertFalse(is_benchmark_file('bexhoma/experiments/base.py'))


if __name__ == '__main__':
    unittest.main()
