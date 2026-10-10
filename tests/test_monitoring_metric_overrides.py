"""
Tests for switching single hardware metrics per experiment (``observe.metrics`` / ``-mm``).

Covers the whole path: the ``-mm`` parser and formatter, the catalog and
environment checks in :mod:`bexhoma.spec`, ``build_argv`` emitting the flag,
the experiment's check against ``cluster.config``, and the override being
applied to the metric definitions copied into each connection.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import argparse
import copy
import types
import unittest

import ycsb
from bexhoma import spec as catalog_spec
from bexhoma.cli_args import format_metric_overrides, parse_metric_overrides
from bexhoma.configurations.metrics import apply_metric_override
from bexhoma.experiments.base import ExperimentBase
from tests.test_ycsb_catalog import _BASE_SPEC, _CATALOG_FILE

_ENVIRONMENT = {
    'nodes': [],
    'monitoring': {'hardware': {
        'total_cpu_util': {'title': 'CPU', 'kind': 'gauge', 'active': True, 'required': True, 'available': True},
        'total_gpu_util': {'title': 'GPU', 'kind': 'gauge', 'active': False, 'required': False, 'available': True},
        'total_fs_read': {'title': 'FS', 'kind': 'counter', 'active': True, 'required': False, 'available': False},
    }},
}


def _with_metrics(metrics, **observe):
    spec = copy.deepcopy(_BASE_SPEC)
    # The minimal environment below has no nodes, so nothing may be pinned.
    del spec['placement']
    spec['observe'] = {'monitoring_sut': True, **observe, 'metrics': metrics}
    return spec


class ParseAndFormatTest(unittest.TestCase):
    """``-mm key=on,key=off`` round-trips and rejects malformed entries."""

    def test_round_trip(self):
        overrides = {'total_gpu_util': True, 'total_network_rx': False}
        self.assertEqual(parse_metric_overrides(format_metric_overrides(overrides)), overrides)

    def test_true_false_and_blanks_are_accepted(self):
        self.assertEqual(parse_metric_overrides(' a=TRUE, ,b=false '), {'a': True, 'b': False})

    def test_malformed_entries_are_usage_errors(self):
        for text in ('a', 'a=maybe', '=on'):
            with self.subTest(text), self.assertRaises(argparse.ArgumentTypeError):
                parse_metric_overrides(text)

    def test_parser_accepts_the_flag(self):
        args = ycsb.build_parser().parse_args(['-m', '-mm', 'total_gpu_util=on', 'run'])
        self.assertEqual(args.monitoring_metrics, {'total_gpu_util': True})

    def test_parser_default_is_no_overrides(self):
        self.assertEqual(ycsb.build_parser().parse_args(['run']).monitoring_metrics, {})


class SpecValidationTest(unittest.TestCase):
    """The catalog shape and the environment both constrain ``observe.metrics``."""

    def setUp(self):
        self.catalog = catalog_spec.load_catalog(_CATALOG_FILE)

    def test_must_be_a_list_of_keys(self):
        for metrics in ({'total_gpu_util': True}, 'total_gpu_util', [1]):
            with self.subTest(metrics), self.assertRaisesRegex(catalog_spec.SpecError, 'list of hardware metric keys'):
                catalog_spec.validate_experiment(self.catalog, _with_metrics(metrics))

    def test_needs_hardware_monitoring(self):
        spec = _with_metrics(['total_gpu_util'])
        spec['observe']['monitoring_sut'] = False
        with self.assertRaisesRegex(catalog_spec.SpecError, 'monitoring_sut or observe.monitoring_cluster'):
            catalog_spec.validate_experiment(self.catalog, spec)

    def test_hardware_monitoring_needs_metrics(self):
        for observe in ({'monitoring_sut': True}, {'monitoring_cluster': True}, {'monitoring_sut': True, 'metrics': []}):
            spec = copy.deepcopy(_BASE_SPEC)
            spec['observe'] = observe
            with self.subTest(observe), self.assertRaisesRegex(catalog_spec.SpecError, 'names no metric'):
                catalog_spec.validate_experiment(self.catalog, spec)

    def test_no_monitoring_needs_no_metrics(self):
        spec = copy.deepcopy(_BASE_SPEC)
        spec['observe'] = {'monitoring_sut': False}
        catalog_spec.validate_experiment(self.catalog, spec)

    def test_environment_accepts_known_metrics(self):
        # A required, default-active metric may be listed: the hypothesis relies on it.
        catalog_spec.validate_environment(_ENVIRONMENT, _with_metrics(['total_gpu_util', 'total_cpu_util']))

    def test_environment_rejections(self):
        for metrics, expected in (
            (['total_disk_magic'], 'not a hardware metric'),
            (['total_fs_read'], 'no data'),
        ):
            with self.subTest(metrics), self.assertRaisesRegex(catalog_spec.SpecError, expected):
                catalog_spec.validate_environment(_ENVIRONMENT, _with_metrics(metrics))

    def test_environment_without_metric_list_asks_for_regeneration(self):
        with self.assertRaisesRegex(catalog_spec.SpecError, 'regenerate'):
            catalog_spec.validate_environment({'nodes': []}, _with_metrics(['total_gpu_util']))

    def test_build_argv_switches_listed_metrics_on(self):
        argv = catalog_spec.build_argv(self.catalog, _with_metrics(['total_gpu_util', 'total_cpu_util']))
        args = ycsb.build_parser().parse_args(argv)
        self.assertEqual(args.monitoring_metrics, {'total_gpu_util': True, 'total_cpu_util': True})

    def test_build_argv_without_monitoring_emits_nothing(self):
        spec = copy.deepcopy(_BASE_SPEC)
        del spec['observe']
        self.assertNotIn('-mm', catalog_spec.build_argv(self.catalog, spec))


class ExperimentOverrideTest(unittest.TestCase):
    """The experiment checks overrides against cluster.config before deploying."""

    def setUp(self):
        self.experiment = types.SimpleNamespace(cluster=types.SimpleNamespace(config={
            'credentials': {'k8s': {'monitor': {'metrics': {
                'total_cpu_util': {'active': True}, 'total_gpu_util': {'active': False},
            }}}},
        }))

    def _set(self, overrides, monitoring_enabled=True):
        ExperimentBase.set_monitoring_metric_overrides(self.experiment, overrides, monitoring_enabled)

    def test_known_overrides_are_stored(self):
        self._set({'total_gpu_util': True})
        self.assertEqual(self.experiment.monitoring_metric_overrides, {'total_gpu_util': True})

    def test_unknown_key_stops_the_run(self):
        with self.assertRaisesRegex(ValueError, 'does not define'):
            self._set({'total_gpu_utl': True})

    def test_required_metric_cannot_be_switched_off(self):
        with self.assertRaisesRegex(ValueError, 'required'):
            self._set({'total_cpu_util': False})

    def test_overrides_need_monitoring(self):
        with self.assertRaisesRegex(ValueError, '-m'):
            self._set({'total_gpu_util': True}, monitoring_enabled=False)

    def test_no_overrides_without_monitoring_is_fine(self):
        self._set({}, monitoring_enabled=False)
        self.assertEqual(self.experiment.monitoring_metric_overrides, {})


class ApplyOverrideTest(unittest.TestCase):
    """The override replaces only ``active``, on a copy."""

    def test_override_replaces_active_on_a_copy(self):
        definition = {'active': False, 'query': 'q', 'title': 'GPU'}
        metric = apply_metric_override('total_gpu_util', definition, {'total_gpu_util': True})
        self.assertEqual(metric, {'active': True, 'query': 'q', 'title': 'GPU'})
        self.assertFalse(definition['active'])

    def test_metric_without_override_keeps_its_default(self):
        definition = {'active': False, 'query': 'q'}
        self.assertEqual(apply_metric_override('other', definition, {'total_gpu_util': True}), definition)


if __name__ == '__main__':
    unittest.main()
