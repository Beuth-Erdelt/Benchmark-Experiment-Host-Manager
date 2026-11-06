"""
Tests for :mod:`bexhoma.experiments.system_builder` and the placeholder expansion of the
descriptors (:func:`bexhoma.system_descriptors.expand`).

The configurations the entry scripts build with it are covered by ``test_dbms_snapshots``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import copy
import io
import tempfile
import types
import unittest
from unittest import mock

import benchbase
import tpch

from bexhoma import system_descriptors as sd
from bexhoma.experiments import system_builder as builder

from .test_reset_scripts import _AnyVolumes
from .test_resource_sweep import _SweepStubCluster


def _dockers() -> dict:
    return {
        'B': {'benchmarks': {'x': {'default': True}, 'y': {}}},
        'A': {'benchmarks': {'x': {}, 'y': {'default': True}}},
        'C': {'benchmarks': {'x': {'default': True}}},
        'D': {'benchmarks': {'y': {}}},
    }


class ExpandTest(unittest.TestCase):

    context = {'n': 3, 'name': 'abc', 'flag': True}

    def test_a_whole_placeholder_keeps_the_type(self) -> None:
        self.assertEqual(sd.expand('{n}', self.context), 3)
        self.assertIs(sd.expand('{flag}', self.context), True)

    def test_mixed_text_is_formatted(self) -> None:
        self.assertEqual(sd.expand('{name}-{n}', self.context), 'abc-3')
        self.assertEqual(sd.expand('no placeholder', self.context), 'no placeholder')

    def test_containers_are_expanded_recursively(self) -> None:
        self.assertEqual(sd.expand({'a': ['{n}', 'x{n}'], 'b': {'c': '{name}'}, 'd': 5}, self.context),
                         {'a': [3, 'x3'], 'b': {'c': 'abc'}, 'd': 5})

    def test_reset_script_names_follow_the_benchmark_context(self) -> None:
        scripts = ['reset-ssb{schema_suffix}.sql', 'reset-flush.sh']
        self.assertEqual(sd.expand(scripts, {'schema_suffix': ''}), ['reset-ssb.sql', 'reset-flush.sh'])
        self.assertEqual(sd.expand(scripts, {'schema_suffix': '-flat'}), ['reset-ssb-flat.sql', 'reset-flush.sh'])

    def test_unknown_placeholder_raises(self) -> None:
        with self.assertRaises(KeyError):
            sd.expand('{missing}', self.context)


class SelectionTest(unittest.TestCase):

    def test_default_set_in_config_order(self) -> None:
        self.assertEqual(builder.selected_dockers(_dockers(), 'x', []), ['B', 'C'])
        self.assertEqual(builder.selected_dockers(_dockers(), 'y', None), ['A'])

    def test_named_dbms_in_config_order_not_argument_order(self) -> None:
        self.assertEqual(builder.selected_dockers(_dockers(), 'x', ['C', 'A']), ['A', 'C'])

    def test_incompatible_dbms_is_refused(self) -> None:
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, r"D is not compatible with benchmark 'x'"):
            builder.selected_dockers(_dockers(), 'x', ['B', 'D'])


class ContextTest(unittest.TestCase):

    def test_worker_counts_are_integers(self) -> None:
        args = types.SimpleNamespace(num_worker='2', num_worker_replicas=1, num_worker_shards='3', other='x')
        context = builder.context_of(args)
        self.assertEqual((context['num_worker'], context['num_worker_replicas'], context['num_worker_shards']), (2, 1, 3))
        self.assertEqual(context['other'], 'x')

    def test_entry_parameters_are_expanded(self) -> None:
        dockers = {'A': {'benchmarks': {'x': {'sut_parameters': {'N': '{num_worker}', 'T': 'fixed'}}}}}
        args = types.SimpleNamespace(num_worker='2')
        self.assertEqual(builder.entry_parameters(dockers, 'A', 'x', 'sut_parameters', args), {'N': 2, 'T': 'fixed'})
        self.assertEqual(builder.entry_parameters(dockers, 'A', 'x', 'eval_parameters', args), {})


class LoadingPodsTest(unittest.TestCase):

    def test_no_limit(self) -> None:
        self.assertEqual(builder.limit_loading_pods({}, 'A', 4, 2), (4, 2))

    def test_within_the_limit(self) -> None:
        self.assertEqual(builder.limit_loading_pods({'max_loading_pods': 2}, 'A', 2, 1), (2, 1))

    def test_capped_with_a_message(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(builder.limit_loading_pods({'max_loading_pods': 1}, 'A', 4, 2), (1, 1))
        self.assertEqual(out.getvalue().strip(), 'A: loads with 1 pod, ignoring -nlp 4')

    def test_parallel_only_capped_without_a_message(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(builder.limit_loading_pods({'max_loading_pods': 1}, 'A', 1, 3), (1, 1))
        self.assertEqual(out.getvalue(), '')


class LoadingVariantsTest(unittest.TestCase):

    def test_one_without_declaration(self) -> None:
        self.assertEqual(builder.loading_variants({}, [1, 8]), [{}])

    def test_one_per_thread_count(self) -> None:
        entry = {'per_loading_threads': {'T': '{threads}', 'P': 1}}
        self.assertEqual(builder.loading_variants(entry, [1, '8']), [{'T': 1, 'P': 1}, {'T': 8, 'P': 1}])


class TenantTest(unittest.TestCase):
    """The multi-tenant variants of tpch.py, for a DBMS that declares ``multi_tenancy``."""

    entry = {'multi_tenancy': ['container', 'schema', 'database']}

    def experiment(self, by: str, number: int = 2):
        return types.SimpleNamespace(tenant_per=by, num_tenants=number)

    def test_a_dbms_without_the_flag_has_no_tenants(self) -> None:
        experiment = self.experiment('container')
        self.assertEqual(builder.tenant_ids(experiment, {}), [None])
        self.assertEqual(tpch.tenant_parameters(experiment, {}, None, 'p'), {})

    def test_container_tenancy_is_one_configuration_per_tenant(self) -> None:
        experiment = self.experiment('container', 3)
        self.assertEqual(builder.tenant_ids(experiment, self.entry), [0, 1, 2])
        result = tpch.tenant_parameters(experiment, self.entry, 1, 'p')
        self.assertEqual(result['storage'], 'p-1-3')
        self.assertEqual(result['loading'], {'BEXHOMA_TENANT_BY': 'container', 'BEXHOMA_TENANT_NUM': 3, 'BEXHOMA_TENANT_ID': 1})
        self.assertEqual(result['eval'], {'TENANT_BY': 'container', 'TENANT_NUM': 3, 'TENANT': 1})
        self.assertNotIn('experiment', result)

    def test_schema_tenancy_switches_scripts(self) -> None:
        experiment = self.experiment('schema')
        self.assertEqual(builder.tenant_ids(experiment, self.entry), [None])
        result = tpch.tenant_parameters(experiment, self.entry, None, 'p')
        self.assertEqual(result['storage'], 'p-schema-2')
        self.assertEqual(result['experiment']['script'], 'Schema_tenant')
        self.assertEqual(result['benchmarking']['BEXHOMA_TENANT_ID'], 0)

    def test_no_tenancy_keeps_the_storage_but_still_sets_the_parameters(self) -> None:
        result = tpch.tenant_parameters(self.experiment('', 0), self.entry, None, 'p')
        self.assertNotIn('storage', result)
        self.assertEqual(result['loading']['BEXHOMA_TENANT_BY'], '')
        self.assertEqual(result['eval'], {'TENANT_BY': '', 'TENANT_NUM': 0})


class SelectorTest(unittest.TestCase):
    """``{'$by': name, value: A, '*': B}`` picks by a command line value."""

    selector = {'$by': 'benchmark', 'tpcc': 'false', '*': 'true'}

    def test_a_matching_key_wins(self) -> None:
        self.assertEqual(sd.expand(self.selector, {'benchmark': 'tpcc'}), 'false')

    def test_the_default_applies_otherwise(self) -> None:
        self.assertEqual(sd.expand(self.selector, {'benchmark': 'ycsb'}), 'true')

    def test_without_default_the_value_is_left_out(self) -> None:
        only = {'$by': 'benchmark', 'tpcc': ['reset.sql']}
        self.assertEqual(sd.expand(only, {'benchmark': 'tpcc'}), ['reset.sql'])
        self.assertIsNone(sd.expand(only, {'benchmark': 'ycsb'}))

    def test_selectors_work_inside_parameters(self) -> None:
        params = {'A': 1, 'B': self.selector, 'C': {'$by': 'benchmark', 'tpcc': 'x'}}
        self.assertEqual(sd.expand(params, {'benchmark': 'ycsb'}), {'A': 1, 'B': 'true', 'C': None})

    def test_none_is_dropped_from_parameters(self) -> None:
        self.assertEqual(builder._without_none({'A': 1, 'B': None, 'C': 0}), {'A': 1, 'C': 0})

    def test_the_value_is_validated_as_a_selector_for_list_keys(self) -> None:
        dockers = {'A': {'storage_prefix': 'a', 'template': {'alias': 'a'},
                         'benchmarks': {'x': {'reset_scripts': {'$by': 'benchmark', 'tpcc': ['r.sql']}}}}}
        self.assertEqual(sd.validate_descriptors(dockers, {'x'}), [])


class _Config:
    """Records what ``apply_sut_attributes`` does to a configuration."""

    def __init__(self) -> None:
        self.calls = []
        self.deployment_infos = {}

    def __getattr__(self, name):
        if name.startswith('set_'):
            return lambda *a, **kw: self.calls.append((name, a, kw))
        raise AttributeError(name)


class SutAttributesTest(unittest.TestCase):

    def apply(self, attributes, context=None) -> _Config:
        config = _Config()
        builder.apply_sut_attributes(config, attributes, context or {})
        return config

    def test_setters_and_attributes(self) -> None:
        config = self.apply({'sut_role': 'placeholder', 'pvc_selector': 'app=x', 'monitoring_sut': False,
                             'sut_pod_name': 'pod-', 'data_components': ['tikv']})
        self.assertEqual(config.calls, [('set_sut_role', ('placeholder',), {}), ('set_pvc_selector', ('app=x',), {}),
                                        ('set_data_components', (['tikv'],), {})])
        self.assertIs(config.monitoring_sut, False)
        self.assertEqual(config.sut_pod_name, 'pod-')

    def test_a_dict_is_passed_as_keyword_arguments_and_expanded(self) -> None:
        config = self.apply({'resources': {'replicas_sut': '{n}', 'replicas_pd': 3}}, {'n': 2})
        self.assertEqual(config.calls, [('set_resources', (), {'replicas_sut': 2, 'replicas_pd': 3})])

    def test_stateful_sets_that_helm_manages(self) -> None:
        config = self.apply({'statefulsets': {'tserver': 2, 'master': 1}})
        self.assertEqual(config.deployment_infos['statefulset'], {
            'tserver': {'name': 'tserver', 'pods': ['tserver-0', 'tserver-1'], 'containers': []},
            'master': {'name': 'master', 'pods': ['master-0'], 'containers': []}})


class PoolingTest(unittest.TestCase):

    entry = {'pooling': {'sut_parameters': {'POOL': '{pool_out}', 'MAX': '{pool_in}'},
                         'resources': {'replicas_pooling': '{pool_pods}'}}}

    def test_no_pooler_is_one_variant_without_settings(self) -> None:
        self.assertEqual(builder.pooling_variants({}, [1, 2], [10], [5]), [{}])

    def test_one_variant_per_combination(self) -> None:
        variants = builder.pooling_variants(self.entry, [1, 2], ['100', 200], [10])
        self.assertEqual(len(variants), 4)
        self.assertEqual(variants[0], {'sut_parameters': {'POOL': 10, 'MAX': 100}, 'resources': {'replicas_pooling': 1}})
        self.assertEqual(variants[-1]['sut_parameters'], {'POOL': 10, 'MAX': 200})
        self.assertEqual(variants[-1]['resources'], {'replicas_pooling': 2})


class TenancyErrorTest(unittest.TestCase):
    """The early check of the entry scripts, from the cluster configuration file."""

    def args(self, dbms, number, mode):
        return types.SimpleNamespace(dbms=dbms, multi_tenant_num=number, multi_tenant_by=mode)

    def test_without_tenancy(self) -> None:
        self.assertEqual(builder.tenancy_error('benchbase', self.args([], 0, '')), '')

    def test_supported(self) -> None:
        self.assertEqual(builder.tenancy_error('benchbase', self.args(['PostgreSQL', 'MySQL'], 2, 'database')), '')

    def test_refused_names_the_dbms_and_who_supports_it(self) -> None:
        message = builder.tenancy_error('benchbase', self.args(['PostgreSQL', 'MySQL'], 2, 'schema'))
        self.assertIn('MySQL does not support this tenancy in benchbase', message)
        self.assertIn('PostgreSQL: container, schema, database; MySQL: container, database', message)

    def test_the_default_set_counts(self) -> None:
        self.assertIn('do not support', builder.tenancy_error('benchbase', self.args([], 2, 'database')))


class BenchbaseTenantTest(unittest.TestCase):
    """Benchbase passes the tenant parameters its DBMS declare."""

    postgresql = {'multi_tenancy': ['container', 'schema', 'database'],
                  'tenant_parameters': {'loading': {'T_BY': '{tenant_by}', 'T_NUM': '{num_tenants}', 'T_ID': '{tenant_id}'},
                                        'benchmarking': {'T_BY': '{tenant_by}', 'T_ID': '{tenant_id}'}}}
    mysql = {'multi_tenancy': ['container', 'database'],
             'tenant_parameters': {'loading': {'T_BY': '{tenant_by}'}, 'benchmarking': {'T_BY': '{tenant_by}'}}}

    def experiment(self, by, number=2):
        return types.SimpleNamespace(tenant_per=by, num_tenants=number, multi_tenant_volume=True)

    def test_no_support_no_parameters(self) -> None:
        self.assertEqual(benchbase.tenant_parameters(self.experiment('container'), {}, None, 'p'), {})

    def test_container_tenancy_per_tenant(self) -> None:
        result = benchbase.tenant_parameters(self.experiment('container', 3), self.postgresql, 1, 'p')
        self.assertEqual(result['storage'], 'p-1-3')
        self.assertEqual(result['loading'], {'T_BY': 'container', 'T_NUM': 3, 'T_ID': 1})
        self.assertEqual(result['eval'], {'TENANT_BY': 'container', 'TENANT_NUM': 3, 'TENANT_VOL': True, 'TENANT': 1})
        self.assertNotIn('tenants_per_job', result)

    def test_schema_tenancy_loads_all_tenants_and_switches_scripts(self) -> None:
        result = benchbase.tenant_parameters(self.experiment('schema'), self.postgresql, None, 'p')
        self.assertEqual(result['storage'], 'p-schema-2')
        self.assertEqual(result['tenants_per_job'], 2)
        self.assertEqual(result['experiment'], {'script': 'Schema_tenant', 'indexing': 'Checks_tenant'})
        self.assertEqual(result['benchmarking'], {'T_BY': 'schema', 'T_ID': 0})

    def test_a_dbms_declares_which_parameters_it_gets(self) -> None:
        result = benchbase.tenant_parameters(self.experiment('database'), self.mysql, None, 'm')
        self.assertEqual(result['loading'], {'T_BY': 'database'})
        self.assertNotIn('experiment', result)

    def test_without_tenancy_the_parameters_are_empty_and_the_storage_is_the_prefix(self) -> None:
        result = benchbase.tenant_parameters(self.experiment('', 0), self.postgresql, None, 'p')
        self.assertNotIn('storage', result)
        self.assertNotIn('tenants_per_job', result)
        self.assertEqual(result['loading'], {'T_BY': '', 'T_NUM': 0, 'T_ID': 0})


class _Experiment:
    def __init__(self, template='', loading=True):
        self.jobtemplate_loading = template
        self._loading = loading

    def loading_is_active(self):
        return self._loading


class _LoadingConfig:
    def __init__(self, experiment, deactivated=False):
        self.experiment = experiment
        self.loading_deactivated = deactivated
        self.jobtemplate_loading = ''


class LoadingTemplateTest(unittest.TestCase):
    """A DBMS has the loading job of its entry, there is no default job of another DBMS."""

    def test_the_template_of_the_entry_is_used(self) -> None:
        config = _LoadingConfig(_Experiment())
        builder.set_loading_template(config, {'loading_template': 'job.yml'}, 'A', 'x')
        self.assertEqual(config.jobtemplate_loading, 'job.yml')

    def test_a_dbms_without_one_is_refused_when_loading(self) -> None:
        config = _LoadingConfig(_Experiment())
        with self.assertRaisesRegex(sd.IncompatibleBenchmark,
                                    r"A declares no loading_template for benchmark 'x'.*dockers\.A\.benchmarks\.x"):
            builder.set_loading_template(config, {}, 'A', 'x')

    def test_nothing_is_needed_when_no_loading_happens(self) -> None:
        for config in (_LoadingConfig(_Experiment(), deactivated=True),      # -sl
                       _LoadingConfig(_Experiment(loading=False))):          # a mode without loading
            builder.set_loading_template(config, {}, 'A', 'x')
            self.assertEqual(config.jobtemplate_loading, '')

    def test_a_benchmark_with_a_loading_job_of_its_own_needs_no_entry(self) -> None:
        config = _LoadingConfig(_Experiment(template='jobtemplate-loading-own.yml'))
        builder.set_loading_template(config, {}, 'A', 'x')
        self.assertEqual(config.jobtemplate_loading, '')


class LoadingTemplateInTheScriptsTest(unittest.TestCase):
    """The scripts, with a PostgreSQL that lost its loading_template."""

    def run_tpch(self, *argv):
        import tpch
        with tempfile.TemporaryDirectory() as tmp_dir:
            cluster = _SweepStubCluster(resultfolder=tmp_dir)
            cluster.volumes = _AnyVolumes(cluster.volumes)
            cluster.dockers = copy.deepcopy(cluster.dockers)
            del cluster.dockers['PostgreSQL']['benchmarks']['tpch']['loading_template']
            args = tpch.build_parser().parse_args(['run', '-dbms', 'PostgreSQL', *argv])
            with (
                mock.patch('bexhoma.clusters.Kubernetes', return_value=cluster),
                mock.patch('bexhoma.experiments.base.ExperimentBase.process', lambda self: None),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                tpch.run(args)

    def test_loading_is_refused(self) -> None:
        with self.assertRaisesRegex(sd.IncompatibleBenchmark, 'PostgreSQL declares no loading_template'):
            self.run_tpch()

    def test_skipping_the_loading_needs_no_template(self) -> None:
        self.run_tpch('-sl')

    def test_the_experiment_names_no_default_job(self) -> None:
        for module, name in (('tpch', 'TpchExperiment'), ('tpcds', 'TpcdsExperiment'), ('ssb', 'SsbExperiment')):
            with self.subTest(benchmark=module):
                import importlib
                source = open(importlib.import_module(f'bexhoma.experiments.{module}').__file__, encoding='utf-8').read()
                self.assertNotIn('jobtemplate-loading-' + module + '-PostgreSQL.yml', source)


if __name__ == '__main__':
    unittest.main()
