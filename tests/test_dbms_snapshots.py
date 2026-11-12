"""
Characterization (golden-master) tests for the DBMS-specific parts of the entry scripts.

Phase 0 of the plan to remove DBMS-specific code from Python (see the project
memory ``dbms-generic-plan``): while the per-DBMS ``if "X" in args.dbms:``
blocks of the root scripts are replaced by data in ``cluster.config``'s
``dockers:`` section and one generic builder, the experiments they build must
not change. For every entry script and every ``-dbms`` choice the test builds
the experiment against a stub cluster (up to ``process()``) and compares a JSON
dump of each :class:`~bexhoma.configurations.base.SutConfiguration` (all plain
data attributes, including ``experiment_dict``) with a committed snapshot in
``tests/snapshots/``.

A deliberate change is accepted by regenerating the snapshots::

    BEXHOMA_UPDATE_SNAPSHOTS=1 python -m pytest tests/test_dbms_snapshots.py

and reviewing the diff of ``tests/snapshots/``.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import contextlib
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from unittest import mock

from bexhoma.configurations.base import SutConfiguration
from bexhoma.experiments.base import ExperimentBase

from .test_resource_sweep import _AnyDockers, _dbms_choices, _SweepStubCluster
from .test_reset_scripts import _AnyVolumes

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SNAPSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snapshots')
_UPDATE = os.environ.get('BEXHOMA_UPDATE_SNAPSHOTS') == '1'

#: Entry scripts under snapshot.
SCRIPTS = ('hammerdb.py', 'tpch.py', 'tpcds.py', 'ssb.py', 'benchbase.py', 'ycsb.py', 'hardware.py')

#: Variant name -> extra argv. ``default`` builds the plain experiment; the others
#: exercise the sweep/loop parameters that the per-DBMS blocks consume.
VARIANTS = {
    'default': [],
    'ram-sweep': ['-rr', '16Gi,32Gi'],
    'skip-loading': ['-sl'],
    'workers': ['-nw', '2', '-nwr', '2', '-nws', '2'],
    'loading': ['-nlp', '2', '-nlt', '4'],
    'benchmarking': ['-nbp', '2', '-nbt', '4', '-ne', '1,2'],
    'storage': ['-rst', 'shared', '-rss', '10Gi'],
    'tenants': ['-mtn', '2', '-mtb', 'database', '-nlp', '2'],
    'tenants-schema': ['-mtn', '2', '-mtb', 'schema', '-nlp', '2'],
    'tenants-container': ['-mtn', '2', '-mtb', 'container', '-nlp', '2'],
    'flat': ['-xsv', 'flat', '-nw', '2'],
    # Benchbase: the benchmark type (reset scripts, databases and schema creation depend on it), the factors
    # of the throughput target, the connection pooler (PGBouncer) and the replicas of TiDB
    'type-ycsb': ['-xbt', 'ycsb', '-xwl', 'b', '-nw', '2'],
    'type-twitter': ['-xbt', 'twitter'],
    'factors': ['-xnbf', '1,2', '-xtb', '100', '-nbp', '2'],
    'pooling': ['-xnpp', '1,2', '-xnpi', '100,200', '-xnpo', '10'],
    'replicas': ['-xnsr', '2', '-xnpd', '5', '-nw', '3', '-nwr', '2', '-nws', '3'],
    # YCSB: workers without replicas (cluster mode of the key-value systems), the workload and its sizes
    'cluster': ['-nw', '2'],
    'workload': ['-xwl', 'b', '-xop', '2', '-xio', 'ordered', '-xsbs', '100', '-xmet', '60'],
    'distributed': ['-xdim', 'distributed', '-nw', '2', '-dbms', 'PostgreSQL', 'ClickHouse', 'ClickHouseCluster'],
    # Hardware: the benchmark tool and the sweep axes of fio and sockperf
    'hw-sysbench': ['-xht', 'sysbench'],
    'hw-sockperf': ['-xht', 'sockperf', '-xspm', 'pp,ul', '-xspp', 'tcp,udp'],
    'hw-netperf': ['-xht', 'netperf'],
    'hw-fio-sweep': ['-xht', 'fio', '-xfrw', 'randread,randwrite', '-xfbs', '4k,8k', '-xfid', '1,8'],
}

#: Variants only some scripts have the flags for.
ONLY_FOR = {'flat': {'ssb.py'}, 'distributed': {'tpch.py', 'ssb.py'},
            'tenants-schema': {'tpch.py', 'benchbase.py'}, 'tenants-container': {'tpch.py', 'benchbase.py'},
            'type-ycsb': {'benchbase.py'}, 'type-twitter': {'benchbase.py'}, 'factors': {'benchbase.py', 'ycsb.py'},
            'pooling': {'benchbase.py', 'ycsb.py'}, 'replicas': {'benchbase.py', 'ycsb.py'},
            'cluster': {'ycsb.py'}, 'workload': {'ycsb.py'},
            'hw-sysbench': {'hardware.py'}, 'hw-sockperf': {'hardware.py'}, 'hw-netperf': {'hardware.py'},
            'hw-fio-sweep': {'hardware.py'}}

#: Scripts that take only some of the common variants: the hardware benchmark has no DBMS to load,
#: scale out or share between tenants, so those variants build the same experiment as ``default``.
ONLY_VARIANTS = {'hardware.py': {'default', 'ram-sweep', 'benchmarking', 'storage',
                                 'hw-sysbench', 'hw-sockperf', 'hw-netperf', 'hw-fio-sweep'}}

#: Variant argv of a script that differs from the common one.
SCRIPT_ARGV = {('ycsb.py', 'factors'): ['-xnlf', '1,2', '-xnbf', '1,2', '-xtb', '100', '-nbp', '2', '-nlp', '2'],
               ('benchbase.py', 'tenants'): ['-mtn', '2', '-mtb', 'database', '-dbms', 'PostgreSQL', 'MySQL'],
               ('benchbase.py', 'tenants-schema'): ['-mtn', '2', '-mtb', 'schema', '-dbms', 'PostgreSQL'],
               ('benchbase.py', 'tenants-container'): ['-mtn', '2', '-mtb', 'container', '-dbms', 'PostgreSQL', 'MySQL'],
               ('tpch.py', 'tenants'): ['-mtn', '2', '-mtb', 'database', '-nlp', '2', '-dbms', 'PostgreSQL'],
               ('tpch.py', 'tenants-schema'): ['-mtn', '2', '-mtb', 'schema', '-nlp', '2', '-dbms', 'PostgreSQL'],
               ('tpch.py', 'tenants-container'): ['-mtn', '2', '-mtb', 'container', '-nlp', '2', '-dbms', 'PostgreSQL'],
               ('ssb.py', 'distributed'): ['-xdim', 'distributed', '-nw', '2', '-dbms', 'PostgreSQL', 'ClickHouse',
                                           'ClickHouseCluster', 'Citus']}

#: (script, variant) pairs the script refuses by design (it exits with a usage error).
UNSUPPORTED = {('ssb.py', 'tenants'), ('tpcds.py', 'tenants'), ('hammerdb.py', 'tenants'), ('ycsb.py', 'tenants')}

#: Attributes whose value changes from run to run (clock, temp folders, progress state).
_VOLATILE = {'path', 'code', 'experiment_name', 'deployment_infos', 'current_benchmark_start',
             'current_benchmark_connection', 'pod_sut', 'logger',
             # the DBMS's cluster.config entry: data, covered by test_system_descriptors
             'dockertemplate'}
_VOLATILE_PREFIXES = ('time_', 'loading_started', 'loading_finished')

#: The attributes the entry scripts, the builder and the ``dockers:`` descriptors set
#: (the ones that differ between DBMS or variants). Only these are dumped, so a new
#: runtime attribute with a default value does not touch the snapshots. When the
#: builder or a descriptor starts to set another attribute, add it here.
SNAPSHOT_KEYS = frozenset({
    '_jobtemplate_loading', 'additional_labels', 'alias', 'benchmark_list', 'benchmark_list_template',
    'benchmarking_parameters', 'benchmarking_parameters_list', 'benchmarking_parameters_list_template',
    'configuration', 'data_components', 'dialect', 'docker', 'eval_parameters', 'experiment_dict',
    'indexing', 'loading_deactivated', 'loading_parameters', 'max_sut_dbms', 'monitoring_sut',
    'num_loading', 'num_loading_pods', 'num_tenants', 'num_worker', 'path_experiment_docker',
    'prometheus_interval', 'prometheus_timeout', 'pvc_selector', 'resource_sweep', 'resources',
    'script', 'script_target', 'statefulset_name', 'storage', 'storage_label', 'sut_container_name',
    'sut_has_pool', 'sut_parameters', 'sut_pod_name', 'sut_role', 'sut_service_name', 'sut_template',
    'tenant_per', 'volume', 'worker_metric_strip_container',
})


def _is_json(value) -> bool:
    try:
        json.dumps(value)
    except (TypeError, ValueError):
        return False
    return True


def _plain(value):
    """Reduce a value to JSON data with stable order (sets sorted)."""
    if isinstance(value, (set, frozenset)):
        return sorted(_plain(v) for v in value)
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


def dump_configuration(config) -> dict:
    """The plain-data attributes of :data:`SNAPSHOT_KEYS` of a configuration, minus volatile ones."""
    result = {}
    for key, value in sorted(vars(config).items()):
        if key not in SNAPSHOT_KEYS or key in _VOLATILE or key.startswith(_VOLATILE_PREFIXES):
            continue
        value = _plain(value)
        if _is_json(value):
            result[key] = value
    return result


def build_snapshot(script: str, extra_argv: list, dbms: list = None) -> dict:
    """Build the experiment of ``script`` up to ``process()``.

    :param dbms: The ``-dbms`` list; ``None`` for all choices of the script, ``[]`` for no ``-dbms`` at all.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        cluster = _SweepStubCluster(resultfolder=tmp_dir)
        cluster.volumes = _AnyVolumes(cluster.volumes)
        cluster.dockers = _AnyDockers(cluster.dockers)
        captured = []

        def capture(experiment_self):
            # what process() does first: clone every configuration per resource cell
            experiment_self.expand_resource_cells()
            captured.append(experiment_self)

        selected = _dbms_choices(script) if dbms is None else dbms
        command = [script, 'run', *(['-dbms', *selected] if selected else []), *extra_argv]
        with (
            # class-level counter behind the default names (PostgreSQL-1, -2, ...): one
            # script run is one process, so start every build from zero
            mock.patch.dict(SutConfiguration.configurations, clear=True),
            mock.patch('bexhoma.clusters.Kubernetes', return_value=cluster),
            mock.patch.object(ExperimentBase, 'process', capture),
            mock.patch.object(sys, 'argv', command),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            try:
                runpy.run_path(os.path.join(_REPO, script), run_name='__main__')
            except SystemExit:
                pass
        if len(captured) != 1:
            raise AssertionError(f'{script} {extra_argv} did not reach process()')
        experiment = captured[0]
        text = json.dumps({
            'configfolder': cluster.experiments_configfolder,
            # sorted by name: the file then changes only where a configuration changes
            'configurations': sorted((dump_configuration(c) for c in experiment.configurations),
                                     key=lambda c: c.get('configuration', '')),
        }, indent=1, sort_keys=True)
        # mask what varies between runs
        text = text.replace(str(experiment.code), '<CODE>').replace(tmp_dir.replace('\\', '\\\\'), '<TMP>')
        return json.loads(text)


class DbmsSnapshotTest(unittest.TestCase):
    """Every entry script builds, per DBMS, exactly the committed configurations."""

    def check(self, script: str, variant: str) -> None:
        actual = build_snapshot(script, SCRIPT_ARGV.get((script, variant), VARIANTS[variant]))
        path = os.path.join(_SNAPSHOT_DIR, f'{script[:-3]}-{variant}.json')
        if _UPDATE:
            os.makedirs(_SNAPSHOT_DIR, exist_ok=True)
            with open(path, 'w', encoding='utf-8', newline='\n') as file:
                json.dump(actual, file, indent=1, sort_keys=True)
                file.write('\n')
            return
        self.assertTrue(os.path.exists(path), f'no snapshot {path}; run with BEXHOMA_UPDATE_SNAPSHOTS=1')
        with open(path, encoding='utf-8') as file:
            expected = json.load(file)
        # per configuration (matched by name, the order of the DBMS follows cluster.config),
        # so that a failure names the DBMS that changed
        before = {c['configuration']: c for c in expected['configurations']}
        after = {c['configuration']: c for c in actual['configurations']}
        self.assertEqual(sorted(before), sorted(after))
        self.assertEqual(expected['configfolder'], actual['configfolder'])
        for name in sorted(after):
            with self.subTest(script=script, variant=variant, docker=after[name].get('docker'), configuration=name):
                self.assertEqual(before[name], after[name])


def _add_tests():
    for script in SCRIPTS:
        for variant in VARIANTS:
            if (script, variant) in UNSUPPORTED or script not in ONLY_FOR.get(variant, {script}):
                continue
            if variant not in ONLY_VARIANTS.get(script, {variant}):
                continue

            def test(self, script=script, variant=variant):
                self.check(script, variant)
            setattr(DbmsSnapshotTest, f'test_{script[:-3]}_{variant.replace("-", "_")}', test)


_add_tests()

if __name__ == '__main__':
    unittest.main()
