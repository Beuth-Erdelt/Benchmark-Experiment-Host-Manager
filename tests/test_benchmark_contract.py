"""
The contract of a benchmark: what every folder ``bexhoma/benchmarks/<name>/`` provides.

A benchmark is added as one folder. Its ``__init__`` defines a ``DESCRIPTOR``
(:class:`bexhoma.benchmarks.registry.BenchmarkDescriptor`), and the registry finds
the folder by itself. This test checks every registered benchmark for what generic
code relies on, so that a new benchmark that misses something fails here with a
message, not later on a cluster:

* its classes are subclasses of the generic ones, and defined in its own folder;
* the experiment can be built, registers at least one benchmark and names its asset
  folder ``experiments/<...>`` and its job templates in ``k8s/``, which exist; a job
  without a template of its own takes it per DBMS from ``cluster.config``, and those
  templates exist as well;
* the evaluator implements the two summary tables;
* the entry script exists;
* names and types are unique.

The dependency test checks the direction of imports: generic code never imports a
benchmark folder (it reaches them through the registry), and a benchmark folder
imports only generic code and the DBMSBenchmarker tool family.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import ast
import os
import tempfile
import unittest

from bexhoma.benchmarks import registry
from bexhoma.benchmarks.base import Benchmark
from bexhoma.collectors.base import CollectorBase
from bexhoma.evaluators.base import EvaluatorBase
from bexhoma.evaluators.logger import LogEvaluator
from bexhoma.experiments.base import ExperimentBase

from bexhoma.system_descriptors import load_dockers

from .stubs import StubCluster
from .test_resource_sweep import _AnyVolumes

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BENCHMARKS = os.path.join(_REPO, 'bexhoma', 'benchmarks')

#: A folder every other benchmark folder may import from: the tool behind TPC-H, TPC-DS and SSB.
_SHARED_FOLDERS = {'dbmsbenchmarker'}
#: Generic modules that import a benchmark folder, with the folder. Each is a deliberate exception.
_GENERIC_EXCEPTIONS = {
    # the baseline of the cluster's hardware is a use of the hardware benchmark
    ('bexhoma/environment.py', 'hardware'),
}


def _folder_of(module: str) -> str:
    """``tpch`` for ``bexhoma.benchmarks.tpch.catalog``; ``''`` for generic modules."""
    parts = module.split('.')
    if len(parts) >= 3 and parts[:2] == ['bexhoma', 'benchmarks'] and \
            os.path.isdir(os.path.join(_BENCHMARKS, parts[2])):
        return parts[2]
    return ''


def _imports(path: str) -> set:
    """Modules a file imports, at the top or inside functions, relative imports resolved."""
    relative = os.path.relpath(path, _REPO).replace(os.sep, '.')[:-3]
    package = relative.rsplit('.', 1)[0] if not relative.endswith('__init__') else relative[:-len('.__init__')]
    with open(path, encoding='utf-8') as file:
        tree = ast.parse(file.read())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found |= {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package.split('.')
                base = base[:len(base) - node.level + 1]
                module = '.'.join(base + ([node.module] if node.module else []))
            else:
                module = node.module or ''
            found.add(module)
            # "from bexhoma.benchmarks import tpch" imports the folder itself
            found |= {f'{module}.{alias.name}' for alias in node.names}
    return found


def _package_files() -> list:
    files = []
    for folder, _, names in os.walk(os.path.join(_REPO, 'bexhoma')):
        files += [os.path.join(folder, name) for name in names if name.endswith('.py')]
    return sorted(files)


def _stub_cluster(tmp_dir: str) -> StubCluster:
    cluster = StubCluster(resultfolder=tmp_dir)
    cluster.volumes = _AnyVolumes(cluster.volumes)
    return cluster


def _defined_in_folder(cls: type, name: str) -> bool:
    return cls.__module__.startswith(f'bexhoma.benchmarks.{name}.') or cls.__module__ == f'bexhoma.benchmarks.{name}'


class BenchmarkContractTest(unittest.TestCase):
    """Every registered benchmark provides what generic code relies on."""

    def setUp(self) -> None:
        self.descriptors = registry.descriptors()

    def test_every_folder_is_registered(self) -> None:
        folders = {name for name in os.listdir(_BENCHMARKS)
                   if os.path.isfile(os.path.join(_BENCHMARKS, name, '__init__.py'))}
        self.assertEqual(folders, {descriptor.name for descriptor in self.descriptors})

    def test_names_and_types_are_unique(self) -> None:
        types = [type_name for descriptor in self.descriptors for type_name in descriptor.types]
        self.assertEqual(len(types), len(set(types)), types)
        for descriptor in self.descriptors:
            with self.subTest(benchmark=descriptor.name):
                self.assertTrue(descriptor.types, 'a benchmark is found by at least one type')

    def test_collector(self) -> None:
        for descriptor in self.descriptors:
            with self.subTest(benchmark=descriptor.name):
                self.assertIsNotNone(descriptor.collector)
                self.assertTrue(issubclass(descriptor.collector, CollectorBase))

    def test_entry_script(self) -> None:
        for descriptor in self.descriptors:
            if descriptor.experiment is None:
                continue
            with self.subTest(benchmark=descriptor.name):
                self.assertTrue(descriptor.entry_script, 'a benchmark with an experiment has an entry script')
                self.assertTrue(os.path.isfile(os.path.join(_REPO, descriptor.entry_script)), descriptor.entry_script)

    def test_experiment(self) -> None:
        for descriptor in self.descriptors:
            if descriptor.experiment is None:
                continue
            with self.subTest(benchmark=descriptor.name):
                experiment_class = descriptor.experiment
                self.assertTrue(issubclass(experiment_class, ExperimentBase))
                self.assertTrue(_defined_in_folder(experiment_class, descriptor.name), experiment_class.__module__)
                with tempfile.TemporaryDirectory() as tmp_dir:
                    cluster = _stub_cluster(tmp_dir)
                    experiment = experiment_class(cluster=cluster, code='1')
                    # the scripts and configs of the benchmark, per DBMS
                    folder = cluster.experiments_configfolder
                    self.assertTrue(folder.startswith('experiments/'), folder)
                    self.assertTrue(os.path.isdir(os.path.join(_REPO, folder)), folder)
                    # the job templates of its loader and benchmarker entries
                    template = getattr(experiment, 'experiment_dict_template', {}) or {}
                    entries = list(template.get('loader', []))
                    for round_entries in template.get('benchmarker', []):
                        entries += round_entries
                    self.assertTrue(entries, 'the experiment declares its jobs')
                    for entry in entries:
                        # empty: the template is set per DBMS from cluster.config (see test_templates_per_dbms)
                        if entry['template']:
                            self.assertTrue(os.path.isfile(os.path.join(_REPO, 'k8s', entry['template'])), entry['template'])
                    # its benchmarks and their evaluators
                    self.assertTrue(experiment.benchmarks, 'the experiment registers a benchmark')
                    for benchmark in experiment.benchmarks:
                        self.assertIsInstance(benchmark, Benchmark)
                        evaluator = benchmark.create_evaluator(code='1', path=tmp_dir, benchmark_run=1)
                        self.assertIsInstance(evaluator, EvaluatorBase)

    def test_evaluator_implements_the_summary_tables(self) -> None:
        for descriptor in self.descriptors:
            if descriptor.experiment is None:
                continue
            with self.subTest(benchmark=descriptor.name), tempfile.TemporaryDirectory() as tmp_dir:
                experiment = descriptor.experiment(cluster=_stub_cluster(tmp_dir), code='1')
                evaluator = experiment.benchmarks[0].create_evaluator(code='1', path=tmp_dir, benchmark_run=1)
                for method in ('get_summary_benchmark_per_connection', 'get_summary_benchmark_per_phase'):
                    implementation = getattr(type(evaluator), method)
                    self.assertIsNot(implementation, getattr(LogEvaluator, method), f'{method} is not implemented')

    def test_templates_per_dbms(self) -> None:
        """The job templates that cluster.config names for a benchmark exist in ``k8s/``."""
        dockers = load_dockers(os.path.join(_REPO, 'k8s-cluster.config'))
        names = {descriptor.name for descriptor in self.descriptors}
        for docker, entry in dockers.items():
            for benchmark, settings in (entry.get('benchmarks') or {}).items():
                with self.subTest(dbms=docker, benchmark=benchmark):
                    self.assertIn(benchmark, names, 'cluster.config names a benchmark that is not registered')
                    for key in ('loading_template', 'refresh_template'):
                        template = (settings or {}).get(key)
                        if isinstance(template, str) and template:
                            self.assertTrue(os.path.isfile(os.path.join(_REPO, 'k8s', template)), template)

    def test_argv_builder_is_callable(self) -> None:
        for descriptor in self.descriptors:
            if descriptor.argv_builder is not None:
                with self.subTest(benchmark=descriptor.name):
                    self.assertTrue(callable(descriptor.argv_builder))

    def test_benchmark_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            Benchmark(name='nothing')


class DependencyDirectionTest(unittest.TestCase):
    """Generic code does not import benchmarks; benchmarks import only generic code and the shared tool."""

    def test_generic_code_imports_no_benchmark(self) -> None:
        found = []
        for path in _package_files():
            relative = os.path.relpath(path, _REPO).replace(os.sep, '/')
            if _folder_of(relative.replace('/', '.')[:-3]):
                continue
            for module in _imports(path):
                folder = _folder_of(module)
                if folder and (relative, folder) not in _GENERIC_EXCEPTIONS:
                    found.append(f'{relative} imports {module}')
        self.assertFalse(found, 'generic code reaches a benchmark through bexhoma.benchmarks.registry:\n'
                         + '\n'.join(sorted(set(found))))

    def test_benchmarks_import_no_other_benchmark(self) -> None:
        found = []
        for path in _package_files():
            relative = os.path.relpath(path, _REPO).replace(os.sep, '/')
            own = _folder_of(relative.replace('/', '.')[:-3])
            if not own:
                continue
            for module in _imports(path):
                folder = _folder_of(module)
                if folder and folder != own and folder not in _SHARED_FOLDERS:
                    found.append(f'{relative} imports {module}')
        self.assertFalse(found, 'a benchmark folder imports another one:\n' + '\n'.join(sorted(set(found))))

    def test_the_exceptions_are_still_needed(self) -> None:
        for relative, folder in _GENERIC_EXCEPTIONS:
            with self.subTest(module=relative):
                modules = _imports(os.path.join(_REPO, relative))
                self.assertTrue(any(_folder_of(module) == folder for module in modules),
                                f'{relative} no longer imports {folder}: remove the exception')


if __name__ == '__main__':
    unittest.main()
