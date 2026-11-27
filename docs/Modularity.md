# Concept: Modularity

Bexhoma keeps three things apart:

* a **DBMS** (the system under test) is configuration: an entry in `cluster.config`, a deployment manifest and scripts,
* a **benchmark** (the workload) is one Python folder plus its scripts, job templates and images,
* the **pairing** of a DBMS and a benchmark is declared per DBMS in `cluster.config` and filled by files in the asset folder of the benchmark.

Adding a DBMS changes no Python file, adding a benchmark changes no Python file outside its own folder, and making an existing benchmark run on an existing DBMS changes no Python file at all.

| Task | Python | Configuration | Files |
|---|---|---|---|
| [Add a DBMS](#adding-a-dbms) | none | `dockers.<DBMS>` in `cluster.config` | `k8s/deploymenttemplate-<DBMS>.yml`, `experiments/<benchmark>/<DBMS>/` |
| [Add a benchmark](#adding-a-benchmark) | `bexhoma/benchmarks/<name>/` | `volumes.<name>`, `dockers.<DBMS>.benchmarks.<name>` | `experiments/<name>/`, `k8s/jobtemplate-*-<name>.yml`, `images/<name>/`, entry script `<name>.py` |
| [Run a benchmark on a DBMS](#making-a-benchmark-run-on-a-dbms) | none | `dockers.<DBMS>.benchmarks.<benchmark>` | `experiments/<benchmark>/<DBMS>/`, loading job template where the benchmark needs one |

## Adding a DBMS

A DBMS is added by configuration alone: an entry in the `dockers` section of `cluster.config`, a deployment manifest in `k8s/` and DDL scripts in `experiments/`. No Python file changes.
The [DBMS](DBMS.md) page is the reference for the entry and the deployment template.

To add a DBMS called `NewDBMS`:

1. **Add a configuration entry** in the `dockers` section of `cluster.config` following the [Configuration Reference](DBMS.md#configuration-reference).

2. **Create a deployment manifest** at `k8s/deploymenttemplate-NewDBMS.yml`.
   Copy `k8s/deploymenttemplate-Dummy.yml` as a starting point and adjust the image, port, and resource defaults.

3. **Add DDL scripts** in a subfolder of `experiments/`, e.g., `experiments/tpch/NewDBMS/` for TPC-H.

4. **Declare the benchmarks** it can run in `benchmarks` of the entry, with `storage_prefix` and `template.alias`, see [Benchmarks of a DBMS](DBMS.md#benchmarks-of-a-dbms) and [Making a Benchmark Run on a DBMS](#making-a-benchmark-run-on-a-dbms).
   No entry script has to be changed: `-dbms` offers every DBMS that has an entry for the benchmark, and the configuration is built from the entry.
   The key of the entry must match the YAML filename of the deployment template (`docker='NewDBMS'`).

   If a JDBC driver is missing, raise an issue at https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues.

5. **Add an example page** `docs/Example-NewDBMS.md` with a test script `scripts/test-docs-newdbms.sh` and `.ps1`, whose runs are in the order of the page.
   All example pages of a DBMS have the same structure:

   * a short introduction and references (as links), including the test script
   * the main use case (`Perform <Benchmark> Benchmark`): a quick run without monitoring, with subsections Status, Cleanup and Evaluate Results
   * Monitoring: a run of at least one minute of benchmarking with `-m`, and Application Metrics (`-ma`) where the DBMS has an exporter
   * Persistent Storage: a run with `-rst` and `-nc 2`, so the second repetition uses the loaded volume
   * Variants, where the DBMS has them (cluster, replication, components, ...), one subsection with an example result each
   * Technical Details: configuration of bexhoma, deployment, schema and scripts, DDL parameters, load durability and reset scripts
   * one section per further use case (benchmark)

   Logs are named `docs_<benchmark>_<dbms>[_<role>].log`, e.g. `_monitoring`, `_appmetrics`, `_storage`, `_cluster`; [TestCases](TestCases.md) lists all test scripts.
   Add the page to `docs/index.rst` and a short section with a link to [DBMS](DBMS.md).

## Adding a Benchmark

A benchmark is one folder, `bexhoma/benchmarks/<name>/`. Bexhoma finds the folder by
itself; no other Python file changes. What the benchmark needs outside Python (scripts
per DBMS, job templates, images, the entries in `cluster.config`) has its usual place
in the repository.

### The folder

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

#### `__init__.py`: the descriptor

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

#### `benchmark.py`

A subclass of `bexhoma.benchmarks.base.Benchmark`. Two methods are required (the class
is abstract):

* `create_evaluator(code, path, benchmark_run)` returns the benchmark's evaluator.
* `configure_workload(experiment, parameter)` adds the description of the workload to
  `experiment.workload`, from the command line arguments.

The summary is built by `Benchmark.show_summary()`. Optional hooks add to it:
`_show_loading_sections`, `_show_extra_sections`, `_build_key_metrics_section`,
`_results_notes`, `_build_completion_sections`, `_prepare_evaluator`.

#### `experiment.py`

A subclass of `bexhoma.experiments.mixed.MixedExperiment`. Its `__init__` sets

* the asset folder: `self.cluster.set_experiments_configfolder('experiments/<name>')`,
* the volume and its init scripts: `self.set_experiment(volume='<name>', script=..., indexing=...)`,
* the workload: `self.set_workload(name=..., info=..., type='<name>')`,
* `self.storage_label`, used to match persistent volumes to the experiment,
* the jobs: `self.experiment_dict_template` with a `loader` and a `benchmarker` list;
  each entry names its job template in `k8s/`. An empty template means the loading job
  is taken per DBMS from `loading_template` in `cluster.config`.
* the benchmark: `self.add_benchmark(MyBenchmark(...))`.

#### `evaluator.py`

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

#### `collector.py`

A subclass of `bexhoma.collectors.base.CollectorBase` whose `get_evaluator(code)` returns
the benchmark's evaluator.

#### `cli.py` and the root script

`cli.py` builds the argument parser (with `bexhoma.cli_args.make_base_parser()` as a
parent) and defines `main()`. The entry script in the repository root only calls it:

```python
from bexhoma.benchmarks.mybench.cli import main

if __name__ == '__main__':
    main()
```

`bexhoma mybench run ...` and `python mybench.py run ...` then both work.

### Outside the folder

| What | Where |
|---|---|
| Scripts per DBMS (schema, checks, reset, durability) and the workload/connection configs | `experiments/<name>/<DBMS>/`, `experiments/<name>/` |
| Job templates of loader and benchmarker | `k8s/jobtemplate-loading-<name>.yml`, `k8s/jobtemplate-benchmarking-<name>.yml` |
| Images of loader and benchmarker | `images/<name>/` |
| Init scripts of the volume | `volumes.<name>.initscripts` in `cluster.config` (and `k8s-cluster.config`) |
| Which DBMS can run it, and how | `dockers.<DBMS>.benchmarks.<name>` in `cluster.config`; a DBMS without this key is not compatible |

The keys of a `benchmarks` entry (`loading_template`, `reset_scripts`,
`loading_parameters`, `refresh_template`, ...) are documented in
`bexhoma/system_descriptors.py`. A new benchmark runs on no DBMS until at least one
DBMS declares it, see [Making a Benchmark Run on a DBMS](#making-a-benchmark-run-on-a-dbms).

### Rules

* **Generic code does not know benchmarks.** Nothing outside `bexhoma/benchmarks/<name>/`
  names a benchmark or reacts to its columns, parameters or attributes. What generic
  code needs comes from the benchmark: a hook, declared data in the descriptor, or a
  capability flag.
* **A benchmark folder imports only generic code**, plus the DBMSBenchmarker tool family
  (`bexhoma/benchmarks/dbmsbenchmarker/`) where the benchmark runs its queries through it.
* Shared code between two benchmarks is duplicated rather than imported from one
  another; a building block every benchmark needs belongs in a generic module.

### Tests

| Test | Checks |
|---|---|
| `tests/test_benchmark_contract.py` | Every registered benchmark: classes, asset folder, job templates (also those in `cluster.config`), summary tables, entry script shim, unique names; the direction of imports |
| `tests/test_no_benchmark_in_generic.py` | No benchmark name in generic modules, comments and docstrings included |
| `tests/test_null_benchmark.py` | The generic summary works for a benchmark with generic data only |
| `tests/test_dbms_snapshots.py` | What each entry script builds per DBMS; add the new script to `SCRIPTS` and record its snapshots with `BEXHOMA_UPDATE_SNAPSHOTS=1` |

Run them with `python -m pytest tests`. `scripts/result_baseline.py` compares what
bexhoma makes of finished experiments before and after a change.

## Making a Benchmark Run on a DBMS

Compatibility is not coded anywhere in Python. It is the sum of a declaration in the
configuration and the files the benchmark needs for this DBMS.

### Where compatibility is declared

`dockers.<DBMS>.benchmarks` has one key per benchmark the DBMS can run, named like the
benchmark (`tpch`, `tpcds`, `ssb`, `ycsb`, `benchbase`, `hammerdb`, ...).
**A missing key means that the DBMS cannot run that benchmark**: `-dbms` of the entry
script offers exactly the DBMS that have the key, and `default: True` makes the DBMS run
when `-dbms` is not given. The entry holds everything the benchmark needs to know about
this DBMS; its keys are listed in [Benchmarks of a DBMS](DBMS.md#benchmarks-of-a-dbms).

### What a pairing consists of

| Part | Where | Used by |
|---|---|---|
| Declaration | `dockers.<DBMS>.benchmarks.<benchmark>` in `cluster.config` | every benchmark |
| Schema, checks, reset and durability scripts | `experiments/<benchmark>/<DBMS>/` (Benchbase: `experiments/benchbase/<-xbt>/<DBMS>/`) | every benchmark that loads into a DBMS |
| Loading job | `loading_template` of the entry, a job template in `k8s/`, with a loader image in `images/<benchmark>/` (e.g. `images/tpch/loader_postgresql`) | TPC-H, TPC-DS, SSB |
| Driver selection | `loading_parameters` / `benchmarking_parameters` of the entry, e.g. `BEXHOMA_DBMS_TYPE` (YCSB binding), `BENCHBASE_PROFILE`, `HAMMERDB_TYPE` | YCSB, Benchbase, HammerDB (they bring their own loading job) |
| SQL dialect | `template.dialect` of the DBMS and query variants under that key in `experiments/<benchmark>/queries-*.config` | TPC-H, TPC-DS, SSB (DBMSBenchmarker) |
| Connection | `template.JDBC` of the DBMS; the driver is in the image of the tool | benchmarks that connect via JDBC |
| DDL parameters | `experiments/<benchmark>/<DBMS>/ddl-parameters.config` | optional, see [DDL parameters](DBMS.md#ddl-parameters--xddl) |

**Scripts.** The script lists are per benchmark, not per DBMS: `volumes.<benchmark>.initscripts`
in `cluster.config` names the scripts of each loading step (`Schema`, `Index`, `Checks`, ...,
chosen with `-xis` and the indexing options). Bexhoma runs those of the list that are
in the folder of the DBMS. A missing SQL script is skipped and listed in the summary
(`loading scripts not in folder, skipped: ...`); a missing shell script is skipped silently,
since shell scripts are optional by design. The file names are those of the lists, e.g.
`initschema-tpch.sql`, `checkschema-tpch.sql`, `reset-tpch.sql`,
`durability-<level>.sql` and `restoredurability-<level>.sql`; the conventions of these
files are in `experiments/README.md`.

**Shared script folders.** A DBMS that accepts the scripts of another one names it in
`base_system` and has no folder of its own: PgDuckDB, OrioleDB and PGBouncer use
`experiments/<benchmark>/PostgreSQL/`.

**Dialect.** A query of DBMSBenchmarker has one standard text and optional variants
keyed by dialect (`'MySQL': """select ..."""`). A DBMS uses the variant of its
`template.dialect` and the standard text where there is none, so a new pairing only
adds variants for queries the DBMS does not accept as they are.

### Steps

To make an existing benchmark `<benchmark>` run on an existing DBMS `<DBMS>`:

1. **Scripts.** Create `experiments/<benchmark>/<DBMS>/` with the scripts of
   `volumes.<benchmark>.initscripts` the DBMS needs, starting from the folder of a similar
   DBMS: at least the schema (`initschema-<benchmark>.sql`) and, where the list has one,
   the post-load check (`checkschema-<benchmark>.sql`); add `reset-<benchmark>.sql` for
   `-ar` and the durability scripts for `-xld`. Alternatively set `base_system` if the scripts of
   another DBMS work unchanged.
2. **Loading.** For TPC-H, TPC-DS and SSB: a loading job template
   `k8s/jobtemplate-loading-<benchmark>-<DBMS>.yml`, reusing a loader image of
   `images/<benchmark>/` where the DBMS speaks its protocol (MariaDB ColumnStore uses
   the MariaDB template). For YCSB, Benchbase and HammerDB: the parameters that select the
   driver of the tool for this DBMS.
3. **Queries.** For benchmarks run by DBMSBenchmarker, add query variants under the
   `template.dialect` of the DBMS where the standard text fails.
4. **Declare.** Add `<benchmark>` to `dockers.<DBMS>.benchmarks` with the keys the
   pairing needs (`loading_template`, `reset_scripts`, `*_parameters`,
   `max_loading_pods`, ...). Limits of the DBMS go here, not into Python: e.g.
   `max_loading_pods: 1` for a DBMS that loses rows with parallel loading pods.
5. **Check and run.** Run `python -m pytest tests/test_system_descriptors.py` (keys, types,
   job templates), record the snapshot of the new pairing in `tests/test_dbms_snapshots.py`
   with `BEXHOMA_UPDATE_SNAPSHOTS=1`, and run `python -m pytest tests` (among others
   `test_load_durability.py` and `test_loading_checks.py` check the new scripts).
   Then run the benchmark, e.g. `python tpch.py run -dbms <DBMS> -sf 1`, and check
   that the summary has no skipped scripts and no failed tests.
6. **Document.** Add a section for the benchmark to `docs/Example-<DBMS>.md` and a run to
   its test script, see [Adding a DBMS](#adding-a-dbms).
