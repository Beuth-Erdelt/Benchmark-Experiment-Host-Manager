# Adding a Benchmark

A benchmark is one folder, `bexhoma/benchmarks/<name>/`. Bexhoma finds the folder by
itself; no other Python file changes. What the benchmark needs outside Python (scripts
per DBMS, job templates, images, the entries in `cluster.config`) has its usual place
in the repository.

This page lists what the folder contains, what lives outside it, and the tests that
check a new benchmark.

## The folder

```
bexhoma/benchmarks/<name>/
├── __init__.py     the DESCRIPTOR: what generic code needs to know
├── benchmark.py    the Benchmark subclass: evaluator and workload description
├── experiment.py   the experiment class: jobs, asset folder, storage label
├── evaluator.py    parses the pod logs of one experiment into DataFrames
├── collector.py    reads several experiments, through the evaluator
├── cli.py          the command line of the entry script
└── catalog.py      optional: argv builder for experiment.yml (catalog workloads)
```

The existing folders are working examples. `ycsb/` has every part; `tpcds/` and `ssb/`
show a benchmark that reuses a tool family (`dbmsbenchmarker/`) and only adds its own
benchmark, experiment and command line.

### `__init__.py`: the descriptor

```python
from bexhoma.benchmarks.registry import BenchmarkDescriptor
from .benchmark import MyBenchmark
from .collector import MyCollector
from .evaluator import MyEvaluator
from .experiment import MyExperiment

DESCRIPTOR = BenchmarkDescriptor(
    name='mybench', types=('mybench',), experiment=MyExperiment, collector=MyCollector,
    entry_script='mybench.py')
```

| Field | Meaning |
|---|---|
| `name` | Canonical name. Equals the folder name, the asset folder `experiments/<name>/` and the key of the benchmark in `cluster.config`. |
| `types` | Names a result folder uses for the benchmark: the workload `type` in `queries.config` and the `type` of its entries in `benchmark_sequence`. Unique across all benchmarks. |
| `experiment` | Experiment class that `bexhoma summary` rebuilds for a result folder of one of `types`. |
| `collector` | Collector class for a benchmark run of one of `types` (used by `MixedCollector`). |
| `entry_script` | File name of the entry script in the repository root. |
| `argv_builder` | Optional: `(catalog, experiment) -> argv` for a catalog workload of this name. |

The registry (`bexhoma/benchmarks/registry.py`) imports every folder on first use.
A folder that fails to import, or defines no `DESCRIPTOR`, raises: a benchmark never
vanishes silently.

### `benchmark.py`

A subclass of `bexhoma.benchmarks.base.Benchmark`. Two methods are required (the class
is abstract):

* `create_evaluator(code, path, benchmark_run)` returns the benchmark's evaluator.
* `configure_workload(experiment, parameter)` adds the description of the workload to
  `experiment.workload`, from the command line arguments.

The summary is built by `Benchmark.show_summary()`. Optional hooks add to it:
`_show_loading_sections`, `_show_extra_sections`, `_build_key_metrics_section`,
`_results_notes`, `_build_completion_sections`, `_prepare_evaluator`.

### `experiment.py`

A subclass of `bexhoma.experiments.mixed.MixedExperiment`. Its `__init__` sets

* the asset folder: `self.cluster.set_experiments_configfolder('experiments/<name>')`,
* the volume and its init scripts: `self.set_experiment(volume='<name>', script=..., indexing=...)`,
* the workload: `self.set_workload(name=..., info=..., type='<name>')`,
* `self.storage_label`, used to match persistent volumes to the experiment,
* the jobs: `self.experiment_dict_template` with a `loader` and a `benchmarker` list;
  each entry names its job template in `k8s/`. An empty template means the loading job
  is taken per DBMS from `loading_template` in `cluster.config`.
* the benchmark: `self.add_benchmark(MyBenchmark(...))`.

### `evaluator.py`

A subclass of `bexhoma.evaluators.logger.LogEvaluator`.

* `log_to_df(filename)` parses one pod log into a DataFrame with the tool's own column
  names.
* `column_names` maps the tool's names to the common ones (`threads`, `errors`, `SF`),
  for example `{'terminals': 'threads'}`. Everything that reads the per-pod DataFrames
  gets the common names.
* `get_summary_benchmark_per_connection()` and `get_summary_benchmark_per_phase()` are
  required. End them with `identity_first()` so that the tables start like those of
  every other benchmark:
  `phase, job, experiment_run, client, benchmark_run, child` per connection and
  `phase, experiment_run, client, benchmark_run, pod_count` per phase.
* `benchmarking_set_datatypes()`, `benchmarking_aggregate_by_parallel_pods()` and
  `get_summary_loading_per_run()` have defaults; override where the benchmark's metrics
  need typing or aggregation of their own.
* `record_tests(...)` records the pass/fail tests of the benchmark's metrics.

### `collector.py`

A subclass of `bexhoma.collectors.base.CollectorBase` whose `get_evaluator(code)` returns
the benchmark's evaluator.

### `cli.py` and the root script

`cli.py` builds the argument parser (with `bexhoma.cli_args.make_base_parser()` as a
parent) and defines `main()`. The entry script in the repository root only calls it:

```python
from bexhoma.benchmarks.mybench.cli import main

if __name__ == '__main__':
    main()
```

`bexhoma mybench run ...` and `python mybench.py run ...` then both work.

## Outside the folder

| What | Where |
|---|---|
| Scripts per DBMS (schema, checks, reset, durability) and the workload/connection configs | `experiments/<name>/<DBMS>/`, `experiments/<name>/` |
| Job templates of loader and benchmarker | `k8s/jobtemplate-loading-<name>.yml`, `k8s/jobtemplate-benchmarking-<name>.yml` |
| Images of loader and benchmarker | `images/<name>/` |
| Init scripts of the volume | `volumes.<name>.initscripts` in `cluster.config` (and `k8s-cluster.config`) |
| Which DBMS can run it, and how | `dockers.<DBMS>.benchmarks.<name>` in `cluster.config`; a DBMS without this key is not compatible |

The keys of a `benchmarks` entry (`loading_template`, `reset_scripts`,
`loading_parameters`, `refresh_template`, ...) are documented in
`bexhoma/system_descriptors.py`.

## Rules

* **Generic code does not know benchmarks.** Nothing outside `bexhoma/benchmarks/<name>/`
  names a benchmark or reacts to its columns, parameters or attributes. What generic
  code needs comes from the benchmark: a hook, declared data in the descriptor, or a
  capability flag.
* **A benchmark folder imports only generic code**, plus the DBMSBenchmarker tool family
  (`bexhoma/benchmarks/dbmsbenchmarker/`) where the benchmark runs its queries through it.
* Shared code between two benchmarks is duplicated rather than imported from one
  another; a building block every benchmark needs belongs in a generic module.

## Tests

| Test | Checks |
|---|---|
| `tests/test_benchmark_contract.py` | Every registered benchmark: classes, asset folder, job templates (also those in `cluster.config`), summary tables, entry script shim, unique names; the direction of imports |
| `tests/test_no_benchmark_in_generic.py` | No benchmark name in generic modules, comments and docstrings included |
| `tests/test_null_benchmark.py` | The generic summary works for a benchmark with generic data only |
| `tests/test_dbms_snapshots.py` | What each entry script builds per DBMS; add the new script to `SCRIPTS` and record its snapshots with `BEXHOMA_UPDATE_SNAPSHOTS=1` |

Run them with `python -m pytest tests`. `scripts/result_baseline.py` compares what
bexhoma makes of finished experiments before and after a change.
