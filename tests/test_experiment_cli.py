"""
Unit tests for ``experiment.py``'s schema dispatch (catalog-driven vs
self-specified experiment YAML files).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import os
import tempfile
import types
import unittest
from unittest import mock

import experiment as experiment_cli
from bexhoma.experiments import tpch_loader as experiment_loader

_CATALOG_DRIVEN_FILE = 'dev/catalog/experiment.yml'
_CATALOG_FILE = 'contracts/contract_catalog.yml'
_SELF_SPECIFIED_FILE = 'dev/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml'


class IsCatalogDrivenTest(unittest.TestCase):
    """Tests for :func:`experiment.is_catalog_driven`."""

    def test_detects_catalog_driven_schema(self) -> None:
        spec = experiment_loader.load_experiment_yaml(_CATALOG_DRIVEN_FILE)
        self.assertTrue(experiment_cli.is_catalog_driven(spec))

    def test_detects_self_specified_schema(self) -> None:
        spec = experiment_loader.load_experiment_yaml(_SELF_SPECIFIED_FILE)
        self.assertFalse(experiment_cli.is_catalog_driven(spec))


class DefaultCatalogPathTest(unittest.TestCase):
    """Tests for :func:`experiment.default_catalog_path`."""

    def test_resolves_alongside_experiment_file(self) -> None:
        """Pure path arithmetic (a same-named catalog.yaml next to the experiment
        file), independent of whether one actually exists there — the real
        catalog now lives at contracts/contract_catalog.yml instead."""
        path = experiment_cli.default_catalog_path(_CATALOG_DRIVEN_FILE)
        self.assertEqual(path, os.path.abspath(os.path.join('dev', 'catalog', 'catalog.yaml')))


class RunExperimentYamlDispatchTest(unittest.TestCase):
    """Tests for :func:`experiment.run_experiment_yaml`'s schema-based dispatch."""

    def test_catalog_driven_file_resolves_and_calls_tpch_run(self) -> None:
        """A catalog-driven file is translated into a real argv and handed to tpch.run().

        Passes catalog_path explicitly: contract_catalog.yml no longer sits
        alongside dev/catalog/experiment.yml (see DefaultCatalogPathTest), so
        the default "alongside" lookup would not find it.
        """
        import tpch
        with mock.patch.object(tpch, 'run') as mock_run:
            experiment_cli.run_experiment_yaml(_CATALOG_DRIVEN_FILE, _CATALOG_FILE)
        mock_run.assert_called_once()
        parsed_args = mock_run.call_args[0][0]
        self.assertEqual(parsed_args.mode, 'run')
        self.assertEqual(sorted(parsed_args.dbms), ['PgDuckDB', 'PostgreSQL'])
        self.assertEqual(parsed_args.scaling_factor, '10')

    def test_self_specified_file_routes_to_experiment_builder(self) -> None:
        """A self-specified file is validated and handed to experiment_builder, not tpch.run()."""
        import tpch
        with mock.patch.object(experiment_cli.tpch_builder, 'build_experiment') as mock_build, \
             mock.patch.object(tpch, 'run') as mock_run:
            experiment_cli.run_experiment_yaml(_SELF_SPECIFIED_FILE)
        mock_build.assert_called_once()
        mock_run.assert_not_called()

    def test_catalog_driven_run_passes_a_provenance_callback_to_tpch_run(self) -> None:
        """The catalog-driven branch must give tpch.run() an on_experiment_built
        callback, so the experiment.yml + contracts still land in the result
        folder even though tpch.run() itself never returns the built experiment."""
        import tpch
        with mock.patch.object(tpch, 'run') as mock_run:
            experiment_cli.run_experiment_yaml(_CATALOG_DRIVEN_FILE, _CATALOG_FILE)
        callback = mock_run.call_args.kwargs['on_experiment_built']
        self.assertTrue(callable(callback))

        with tempfile.TemporaryDirectory() as tmp_dir:
            stub_experiment = types.SimpleNamespace(path=tmp_dir)
            with mock.patch.object(experiment_cli, '_copy_catalog_provenance') as mock_copy:
                callback(stub_experiment)
            mock_copy.assert_called_once_with(tmp_dir, _CATALOG_DRIVEN_FILE, _CATALOG_FILE)


class CopyCatalogProvenanceTest(unittest.TestCase):
    """Tests for :func:`experiment._copy_catalog_provenance`."""

    def test_copies_experiment_yaml_catalog_and_result_contract(self) -> None:
        with tempfile.TemporaryDirectory() as result_dir:
            experiment_cli._copy_catalog_provenance(result_dir, _CATALOG_DRIVEN_FILE, _CATALOG_FILE)
            self.assertTrue(os.path.isfile(os.path.join(result_dir, 'experiment.yml')))
            self.assertTrue(os.path.isfile(os.path.join(result_dir, 'contract_catalog.yml')))
            self.assertTrue(os.path.isfile(os.path.join(result_dir, 'contract_result.yml')))
            with open(os.path.join(result_dir, 'contract_catalog.yml'), 'r', encoding='utf-8') as copied, \
                 open(_CATALOG_FILE, 'r', encoding='utf-8') as original:
                self.assertEqual(copied.read(), original.read())

    def test_missing_catalog_override_is_silently_skipped(self) -> None:
        """A --catalog path that doesn't exist must not abort provenance copying
        of the other two files -- this is best-effort, not a hard requirement."""
        with tempfile.TemporaryDirectory() as result_dir:
            experiment_cli._copy_catalog_provenance(result_dir, _CATALOG_DRIVEN_FILE, 'does-not-exist.yml')
            self.assertTrue(os.path.isfile(os.path.join(result_dir, 'experiment.yml')))
            self.assertFalse(os.path.isfile(os.path.join(result_dir, 'contract_catalog.yml')))
            self.assertTrue(os.path.isfile(os.path.join(result_dir, 'contract_result.yml')))


if __name__ == '__main__':
    unittest.main()
