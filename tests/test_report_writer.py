"""
Unit tests for :mod:`bexhoma.report_writer`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd
import yaml

from bexhoma import report_writer
from bexhoma.__version__ import __version__ as BEXHOMA_VERSION


_RESULT_FILES = (
    'experiment.yml',
    'contract_catalog.yml',
    'agent_summary.yml',
    'connections.config',
    'queries.config',
    'postgresql-1-1-1-1.config',
    'bexhoma-sut-postgresql-1-123-1.yml',
    'bexhoma-sut-postgresql-1-123-1-7bd45c7b95-pwzkz.dbms.log',
    'bexhoma-sut-postgresql-1-123-1-7bd45c7b95-pwzkz.describe.log',
    'bexhoma-sut-postgresql-1-123-1-restarts.json',
    'bexhoma-loading-postgresql-1-123-1-1-1.describe.job.log',
    'bexhoma-loading-postgresql-1-123-1-1-1-abcde.describe.log',
    'bexhoma-loading-postgresql-1-123-1-1-1-abcde.sensor.log',
    'bexhoma-benchmarker-postgresql-1-123-1-1-1-qp9nt.dbmsbenchmarker.log',
    'bexhoma-benchmarker-postgresql-1-123-1-1-1-qp9nt.describe.log',
    'query_benchmarking_metric_total_cpu_util.csv',
    'bexhoma-experiment-dict-postgresql-1-123.json',
    'evaluation.json',
)


def _make_result_dir(tmp_dir: str) -> tuple[Path, Path]:
    result_dir = Path(tmp_dir)
    report_dir = result_dir / 'report'
    report_dir.mkdir()
    for name in _RESULT_FILES:
        (result_dir / name).write_text('x\n')
    return result_dir, report_dir


class GroupResultFilesTest(unittest.TestCase):
    """Every result-folder file lands in exactly one files.md group -- the
    first whose pattern matches, so specific kinds win over broad ones."""

    def test_each_file_lands_in_its_specific_group(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir, _report_dir = _make_result_dir(tmp_dir)
            groups = report_writer._group_result_files(result_dir)

        names = {anchor: [path.name for path in paths] for anchor, paths in groups.items()}
        self.assertEqual(names['inputs'], ['contract_catalog.yml', 'experiment.yml'])
        self.assertEqual(names['manifests'], ['bexhoma-sut-postgresql-1-123-1.yml'])
        self.assertEqual(names['sut-describe'], ['bexhoma-sut-postgresql-1-123-1-7bd45c7b95-pwzkz.describe.log'])
        self.assertEqual(len(names['pod-describe']), 2)
        self.assertEqual(names['job-describe'], ['bexhoma-loading-postgresql-1-123-1-1-1.describe.job.log'])
        self.assertEqual(names['sut-logs'], ['bexhoma-sut-postgresql-1-123-1-7bd45c7b95-pwzkz.dbms.log'])
        self.assertEqual(names['benchmarker'], ['bexhoma-benchmarker-postgresql-1-123-1-1-1-qp9nt.dbmsbenchmarker.log'])
        self.assertEqual(names['loading-pods'], ['bexhoma-loading-postgresql-1-123-1-1-1-abcde.sensor.log'])
        self.assertEqual(names['sut-restarts'], ['bexhoma-sut-postgresql-1-123-1-restarts.json'])
        self.assertEqual(len(names['configs']), 3)
        self.assertEqual(names['plans'], ['bexhoma-experiment-dict-postgresql-1-123.json'])
        self.assertEqual(names['other'], ['evaluation.json'])

    def test_every_file_is_grouped_once_except_agent_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir, _report_dir = _make_result_dir(tmp_dir)
            groups = report_writer._group_result_files(result_dir)

        grouped = [path.name for paths in groups.values() for path in paths]
        self.assertEqual(len(grouped), len(set(grouped)))
        self.assertEqual(set(grouped), set(_RESULT_FILES) - {'agent_summary.yml'})


class FilesMdTest(unittest.TestCase):
    """files.md links every raw file exactly once; tier-2 footers link only
    files.md sections, never a raw file."""

    def test_files_md_links_each_file_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir, report_dir = _make_result_dir(tmp_dir)
            groups = report_writer._group_result_files(result_dir)
            lines = report_writer._build_files_md_lines(groups, report_dir)

        links = [line for line in lines if line.startswith('- [')]
        self.assertEqual(len(links), len(_RESULT_FILES) - 1)
        self.assertIn('- [evaluation.json](../evaluation.json)', links)
        self.assertIn('### Kubernetes Manifests', lines)

    def test_provenance_footer_links_files_md_sections_with_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir, _report_dir = _make_result_dir(tmp_dir)
            groups = report_writer._group_result_files(result_dir)
            lines = report_writer._provenance_lines(groups, ('inputs', 'loading-scripts', 'pod-describe'))

        self.assertEqual(lines[0], '### Provenance')
        self.assertIn('- [Experiment Inputs](files.md#inputs): 2 files', lines)
        self.assertIn('- [Other Pod Descriptions](files.md#pod-describe): 2 files', lines)
        self.assertFalse(any('loading-scripts' in line for line in lines))

    def test_no_footer_without_files(self) -> None:
        self.assertEqual(report_writer._provenance_lines({}, ('inputs',)), [])

    def test_tier2_frontmatter_carries_no_path_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir, report_dir = _make_result_dir(tmp_dir)
            groups = report_writer._group_result_files(result_dir)
            report_writer._write_tier2_file(
                report_dir, 'workflow.md', 'workflow', '', [], {},
                report_writer._provenance_lines(groups, ('inputs', 'manifests')),
            )
            text = (report_dir / 'workflow.md').read_text(encoding='utf-8')

        frontmatter = yaml.safe_load(text.split('---\n')[1])
        self.assertNotIn('provenance', frontmatter)
        self.assertNotIn('](../', text)
        self.assertIn('](files.md#manifests)', text)


class ConnectionsMdTest(unittest.TestCase):
    """connections.md repeats no file links per connection."""

    def test_no_per_connection_file_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir, report_dir = _make_result_dir(tmp_dir)
            df_connections = pd.DataFrame([
                {'connection': 'postgresql-1-1-1-1-1', 'configuration': 'PostgreSQL-1'},
                {'connection': 'postgresql-1-1-1-1-2', 'configuration': 'PostgreSQL-1'},
            ])
            lines = report_writer._build_connections_md_lines(df_connections, result_dir, report_dir, {})

        self.assertFalse(any('](../' in line for line in lines))
        self.assertFalse(any('Provenance' in line for line in lines))

    def test_each_parameter_is_listed_once_where_it_stops_varying(self) -> None:
        df_connections = pd.DataFrame([
            {'connection': 'pgduckdb-1-1-1-1-1', 'configuration': 'PgDuckDB-1', 'SF': 10, 'arg': 'a', 'client': 1},
            {'connection': 'pgduckdb-1-1-2-1-1', 'configuration': 'PgDuckDB-1', 'SF': 10, 'arg': 'a', 'client': 2},
            {'connection': 'postgresql-1-1-1-1-1', 'configuration': 'PostgreSQL-1', 'SF': 10, 'arg': 'b', 'client': 1},
        ])
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir, report_dir = _make_result_dir(tmp_dir)
            lines = report_writer._build_connections_md_lines(df_connections, result_dir, report_dir, {})

        self.assertEqual(lines.count('* SF: 10'), 1)
        self.assertEqual(lines.count('* arg: a'), 1)
        self.assertEqual(lines.count('* arg: b'), 1)
        self.assertEqual(lines.count('* client: 1'), 2)
        shared = lines.index('### Shared by All Connections')
        pgduckdb = lines.index('### PgDuckDB-1')
        first = lines.index('#### pgduckdb-1-1-1-1-1')
        self.assertLess(shared, lines.index('* SF: 10'))
        self.assertLess(lines.index('* SF: 10'), pgduckdb)
        self.assertLess(pgduckdb, lines.index('* arg: a'))
        self.assertLess(lines.index('* arg: a'), first)
        self.assertIn('[PgDuckDB-1](#shared-pgduckdb-1)', lines[first + 3])
        self.assertIn('[Shared by All Connections](#shared)', lines[first + 3])
        self.assertIn('<a id="pgduckdb-1-1-1-1-1"></a>', lines)

    def test_a_single_connection_keeps_all_its_parameters(self) -> None:
        df_connections = pd.DataFrame([{'connection': 'postgresql-1-1-1-1-1', 'configuration': 'PostgreSQL-1', 'SF': 10}])
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir, report_dir = _make_result_dir(tmp_dir)
            lines = report_writer._build_connections_md_lines(df_connections, result_dir, report_dir, {})

        self.assertIn('* SF: 10', lines)
        self.assertNotIn('### Shared by All Connections', lines)


class ExperimentDictNameTest(unittest.TestCase):
    """The evaluator reads the experiment dict under its current name, which
    carries the code, and under the name result folders had before."""

    def _load(self, filename: str) -> dict:
        from bexhoma.evaluators.base import EvaluatorBase as evaluator_base

        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir) / '1784910886'
            result_dir.mkdir()
            (result_dir / filename).write_text('{"loader": [1]}')
            evaluator = evaluator_base.__new__(evaluator_base)
            evaluator.path = str(result_dir)
            evaluator._experiment_dict_cache = {}
            return evaluator._load_experiment_dict('PostgreSQL-1')

    def test_current_name_with_code(self) -> None:
        self.assertEqual(self._load('bexhoma-experiment-dict-postgresql-1-1784910886.json'), {'loader': [1]})

    def test_name_before_code_joined_it(self) -> None:
        self.assertEqual(self._load('bexhoma-experiment-dict-PostgreSQL-1.json'), {'loader': [1]})


class _FakeExperiment:
    code = '1784910886'
    workload = {'type': 'tpch'}
    _test_results = [(True, 'ok'), (False, 'bad'), (None, 'skipped')]

    def benchmarking_is_active(self) -> bool:
        return True

    def loading_is_active(self) -> bool:
        return True


class IndexMdFrontmatterTest(unittest.TestCase):
    """report/index.md's frontmatter must record which bexhoma version wrote it."""

    def test_bexhoma_version_is_recorded_in_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            report_dir = Path(tmp_dir) / 'report'
            report_dir.mkdir()
            report_writer._write_index_md(
                report_dir, _FakeExperiment(), total_restarts=0, extra_context={},
                written_sections=[], key_metrics_lines=[], monitoring_summary_lines=[],
            )
            text = (report_dir / 'index.md').read_text(encoding='utf-8')

        frontmatter_text = text.split('---\n')[1]
        frontmatter = yaml.safe_load(frontmatter_text)
        self.assertEqual(frontmatter['bexhoma_version'], BEXHOMA_VERSION)
        self.assertEqual(frontmatter['schema_version'], report_writer.SCHEMA_VERSION)


if __name__ == '__main__':
    unittest.main()
