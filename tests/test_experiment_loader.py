"""
Unit tests for :mod:`bexhoma.experiment_loader`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import copy
import os
import tempfile
import unittest

import yaml

from bexhoma.experiment_loader import (
    ExperimentYamlError,
    load_experiment_yaml,
    validate_experiment_yaml,
)

_VALID_SPEC = {
    'workload': 'tpch',
    'mode': 'run',
    'systems': [
        {'dbms': 'PostgreSQL'},
        {'dbms': 'PgDuckDB'},
    ],
}


class LoadExperimentYamlTest(unittest.TestCase):
    """Tests for :func:`load_experiment_yaml`."""

    def test_round_trips_yaml_content(self) -> None:
        """Loading a YAML file returns the same structure that was written."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = os.path.join(tmp_dir, 'experiment.yaml')
            with open(path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(_VALID_SPEC, f)
            loaded = load_experiment_yaml(path)
        self.assertEqual(loaded, _VALID_SPEC)


class ValidateExperimentYamlTest(unittest.TestCase):
    """Tests for :func:`validate_experiment_yaml`."""

    def test_accepts_valid_spec(self) -> None:
        """A spec with all required fields and known DBMS names passes validation."""
        validate_experiment_yaml(copy.deepcopy(_VALID_SPEC))

    def test_rejects_missing_required_field(self) -> None:
        """A spec missing 'systems' is rejected."""
        spec = copy.deepcopy(_VALID_SPEC)
        del spec['systems']
        with self.assertRaises(ExperimentYamlError):
            validate_experiment_yaml(spec)

    def test_rejects_unsupported_workload(self) -> None:
        """Only 'tpch' is translatable today; other workloads must be rejected."""
        spec = copy.deepcopy(_VALID_SPEC)
        spec['workload'] = 'ycsb'
        with self.assertRaises(ExperimentYamlError):
            validate_experiment_yaml(spec)

    def test_rejects_empty_systems_list(self) -> None:
        """An empty 'systems' list is rejected."""
        spec = copy.deepcopy(_VALID_SPEC)
        spec['systems'] = []
        with self.assertRaises(ExperimentYamlError):
            validate_experiment_yaml(spec)

    def test_rejects_unknown_dbms(self) -> None:
        """A DBMS name absent from DBMS_DEFAULTS is rejected."""
        spec = copy.deepcopy(_VALID_SPEC)
        spec['systems'].append({'dbms': 'Oracle'})
        with self.assertRaises(ExperimentYamlError):
            validate_experiment_yaml(spec)

    def test_rejects_system_missing_dbms_key(self) -> None:
        """A systems entry without a 'dbms' key is rejected."""
        spec = copy.deepcopy(_VALID_SPEC)
        spec['systems'].append({'alias': 'no dbms here'})
        with self.assertRaises(ExperimentYamlError):
            validate_experiment_yaml(spec)


if __name__ == '__main__':
    unittest.main()
