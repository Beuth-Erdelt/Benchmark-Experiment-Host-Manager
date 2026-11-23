# Software Architecture

This page describes how the Python code of Bexhoma is organised, so that you know where a change belongs.
For what runs inside the Kubernetes cluster (SUT, loaders, benchmarkers, monitoring, dashboard), see [Concepts](Concepts.md#architecture).
For adding a benchmark or a DBMS, see [Adding a Benchmark](Adding-a-Benchmark.md) and [Add a New DBMS](DBMS.md#add-a-new-dbms).

Bexhoma is an orchestrator. It runs on your machine, talks to the cluster through `kubectl` and the Kubernetes API, and never runs a benchmark itself: every loader, benchmarker and evaluation runs in a pod.

## Repository

| Folder or file | Contains |
|---|---|
| `bexhoma/` | the Python package, see [Package](#package) |
| `tpch.py`, `ycsb.py`, ... | entry scripts, one per benchmark; each only calls `main()` of `bexhoma/benchmarks/<name>/cli.py` |
| `experiment.py`, `validate_experiment.py` | entry scripts for an `experiment.yml` checked against the catalog contract |
| `k8s-cluster.config` / `cluster.config` | the cluster configuration: credentials, volumes, benchmarkers and, in `dockers`, every DBMS with the benchmarks it supports |
| `experiments/<benchmark>/<dbms>/` | DDL and loading scripts, query files, DDL parameters |
| `k8s/` | manifest templates: SUT deployments, loader and benchmarker jobs, monitoring |
| `images/` | Dockerfiles of the loaders, benchmarkers, the evaluator and monitoring |
| `contracts/` | the catalog contract (input) and the result contract (output), with their rationale in `*_comments.md` |
| `agent/` | the contract-driven agent, see [agent/ARCHITECTURE.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/agent/ARCHITECTURE.md) |
| `scripts/` | `test-docs-*` scripts that produce the documented runs, release and build scripts, collector validations |
| `tests/` | unit tests; no cluster needed, see [Testing](CONTRIBUTING.md#testing) |
| `logs_tests/` | logs of the documented runs |

## Package

The package has three layers: benchmark-specific code builds on generic orchestration, which builds on cluster access. Generic code reaches benchmark-specific code only through the registry; the one exception is `environment.py`, which runs the hardware baseline of `benchmarks/hardware/` directly.

| Layer | Module | Responsibility |
|---|---|---|
| Benchmark-specific | `benchmarks/<name>/` | everything that belongs to one benchmark, up to: CLI, experiment, benchmark, evaluator, collector, catalog argv builder (`catalog.py`, only `tpch` and `ycsb`); `tpch/` also has `loader.py` and `builder.py` for the YAML-driven entry script |
| | `benchmarks/dbmsbenchmarker/` | what TPC-H, TPC-DS and SSB share (benchmark, evaluator, collector); not a benchmark of its own: no CLI, no experiment |
| | `benchmarks/registry.py` | finds the benchmark folders; generic code asks it instead of naming a benchmark |
| Generic orchestration | `benchmarks/base.py`, `benchmarks/refresh.py` | the abstract `Benchmark` and the `Section` tree its summary is built from; `RefreshStreamBenchmark` for stream jobs that run beside a benchmark in the same round |
| | `experiments/base.py`, `experiments/mixed.py` | `ExperimentBase` and `MixedExperiment`: the experiment, its configurations, the main loop, evaluation, summary |
| | `experiments/system_builder.py` | builds one configuration of a DBMS for a benchmark from the `dockers` entry of the cluster configuration |
| | `configurations/` | `SutConfiguration`: one DBMS configuration and its helpers, see [Configuration](#configuration) |
| | `evaluators/`, `collectors/` | generic base classes for the results of one experiment (evaluator) or of several (collector); `evaluators/logger.py` has `LogEvaluator`, which parses benchmarker logs and is the parent of every benchmark-specific evaluator |
| | `monitoring_math.py` | reduces monitoring time series to one value per connection (counter metrics across pod restarts and leftover pods) |
| | `report_writer.py`, `failure_timeline.py`, `sut_restarts.py`, `loading_checks.py`, `missing_metrics.py`, `test_status.py` | the Markdown report and the checks it shows; they read only the result folder |
| | `spec.py`, `spec_argv.py`, `environment.py` | catalog contract: validate an `experiment.yml`, build the command line, describe the cluster in `environment.yml` |
| | `system_descriptors.py`, `ddl_parameters.py`, `load_durability.py` | read DBMS-specific settings from the cluster configuration and the script folders |
| Cluster access | `clusters.py` | `Kubernetes` (and `AWS`): pods, jobs, deployments, PVCs, `kubectl exec`/`cp`, the dashboard and message queue |
| | `cluster_calls.py`, `parallel_steps.py`, `metric_fetching.py` | counting and timing cluster calls, steps of the main loop that run side by side, parallel Prometheus fetches |
| | `ceph_storage.py`, `tls.py` | Ceph facts behind a SUT's volumes (StorageClass, pool, RBD images) for monitoring placeholders, `environment.yml` and spec validation; the self-signed CA and server certificate Secret of a SUT |
| Command line | `scripts/cli.py`, `scripts/experimentsmanager.py`, `cli_args.py` | the `bexhoma` command, the management tool (`status`, `summary`, ...) and the arguments all entry scripts share |

## Flow of a run

`bexhoma tpch run -dbms PostgreSQL ...` goes through these steps:

```
bexhoma (scripts/cli.py)
  └─ tpch.py ─► benchmarks/tpch/cli.py: main()
        ├─ parse arguments (cli_args.make_base_parser + benchmark options)
        ├─ cluster    = clusters.Kubernetes(context)            reads cluster.config
        ├─ experiment = TpchExperiment(cluster, SF, ...)        a MixedExperiment
        ├─ for each DBMS: system_builder.build_configuration()  ─► SutConfiguration
        └─ experiment.process()
              ├─ prepare_testbed()                 monitoring, dashboard, message queue
              ├─ store_workflow_results()          planned workflow into queries.config
              ├─ work_benchmark_list()             the main loop, see below
              ├─ evaluate_results()                evaluation runs in the dashboard pod
              └─ show_summary()                    Benchmark.show_summary() per benchmark
                                                   + report_writer (with -rp)
```

`work_benchmark_list()` is a polling loop: every few seconds it moves each configuration on (start SUT, start monitoring, load, submit benchmarker jobs, stop or repeat) and then harvests finished jobs. It is described step by step in [Main Workflow Loop](WorkBenchmarkList.md).

What a configuration loads and benchmarks is its `experiment_dict`: a list of loader entries and a list of benchmarker rounds, each round a list of benchmarks that run in parallel. It is written to the result folder as `bexhoma-experiment-dict-<configuration>-<code>.json`. Evaluators find a benchmark by its `name` in that file, not by its position.

## Configuration

`SutConfiguration` (`configurations/base.py`) holds the state of one DBMS configuration. Its work is done by helpers it owns (composition, not inheritance):

| Attribute | Class | Does |
|---|---|---|
| `config.lifecycle` | `LifecycleManager` | start and stop the SUT, workers, pooler and monitoring |
| `config.loader` | `LoadingCoordinator` | run loading scripts, submit loader jobs, decide when loading finished and whether it failed |
| `config.runner` | `BenchmarkRunner` | submit benchmarker jobs |
| `config.manifest` | `ManifestBuilder` | fill the manifest templates of `k8s/` |
| `config.metrics` | `MetricsCollector` | fetch Prometheus metrics per phase and component |
| `config.host` | `HostProbe` | host facts, volumes, restarts of SUT pods |
| `config.status` | `ComponentStatus` | whether SUT, workers, monitoring are pending, running, healthy |

New behaviour of a configuration belongs in the helper that owns that subject, not in `SutConfiguration` itself.

## Benchmarks

A benchmark is one folder `bexhoma/benchmarks/<name>/`. Its `__init__.py` registers a `BenchmarkDescriptor` (name, result types, experiment class, collector class, entry script, catalog argv builder) with `benchmarks/registry.py`. The folder holds:

- `cli.py`: arguments and the setup of the experiment,
- `experiment.py`: a subclass of `MixedExperiment` (TPC-H, TPC-DS and SSB share `DbmsBenchmarkerExperiment`),
- `benchmark.py`: a subclass of `Benchmark` (`benchmarks/base.py`) that configures the workload and builds the summary from `Section`s,
- `evaluator.py` and `collector.py`: reading one result folder and comparing several,
- `catalog.py`, if the benchmark can be run from an `experiment.yml`.

Generic code must not name a benchmark; `test_no_benchmark_in_generic.py` checks that. Details: [Adding a Benchmark](Adding-a-Benchmark.md).

## DBMS

Python code does not name a DBMS. Everything specific to a DBMS is in its entry of `dockers` in the cluster configuration: the deployment template, storage prefix, and under `benchmarks` one entry per supported benchmark (loading template, reset scripts, multi-tenancy, defaults). A DBMS without an entry for a benchmark cannot run it. `system_descriptors.py` reads these entries; `test_no_dbms_in_python.py` and `test_system_descriptors.py` keep it that way. Details: [DBMS](DBMS.md#benchmarks-of-a-dbms).

## Results

Every experiment has a code (a timestamp) and a result folder `<resultfolder>/<code>/` in the cluster and locally. It contains `queries.config` (the workload and planned workflow), `connections.config` (one entry per connection with its timings), the experiment dicts, pod logs and descriptions, and the metrics. Everything after the run is computed from that folder alone, so it works on a downloaded result folder too:

- an evaluator (`evaluators/`, `benchmarks/<name>/evaluator.py`) reads one experiment into DataFrames,
- a collector (`collectors/`, `benchmarks/<name>/collector.py`) compares several experiments,
- `bexhoma summary` rebuilds the experiment class of the result folder through the registry and prints the summary again,
- `report_writer.py` writes the tiered Markdown report in `report/`, whose shape is defined by `contracts/contract_result.yml`, see [Agent Report](AgentReport.md).

## Catalog and agent

`experiment.py` takes an `experiment.yml`, validates it against `contracts/contract_catalog.yml` (`spec.py`) and builds the command line of the entry script with the benchmark's argv builder. The command line stays the single source of truth: the catalog path only produces arguments. `environment.py` describes the cluster as `environment.yml`.

The agent in `agent/` uses both contracts to plan, run and answer experiments; see [Agent](Agent.md) and [agent/ARCHITECTURE.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/agent/ARCHITECTURE.md).

## Rules the tests enforce

| Rule | Test |
|---|---|
| no DBMS names in Python | `test_no_dbms_in_python.py` |
| no benchmark names in generic code | `test_no_benchmark_in_generic.py` |
| a benchmark folder is complete | `test_benchmark_contract.py` |
| every `dockers` entry is valid and has its templates | `test_system_descriptors.py` |
| entry scripts build the recorded experiments | `test_dbms_snapshots.py` |
| contracts and code agree | `test_naming_conformance.py` |

What to do when one of them fails: [When a test fails](CONTRIBUTING.md#when-a-test-fails).

## Known structural debt

- `experiments/base.py` (about 4,000 lines) and `clusters.py` (about 3,700 lines) are the largest modules. `work_benchmark_list()` alone is several hundred lines; splitting it into one handler per phase would make the phases testable on their own.
- The legacy `benchmark_list` path of the main loop is still there for configurations without benchmarker entries in `experiment_dict`. The entry scripts call `add_benchmark_list()`, which also fills `experiment_dict`, so they take the `experiment_dict` path.

## Design notes

These pages record why a design was chosen. They are not updated with every change; where they and the code disagree, the code is right.

- [Design: Catalog Contract](Design-Catalog-Contract.md): the catalog contract, its full audit of benchmarks and DBMS, open questions
- [Design: YAML-driven experiment entry script](Design-Yaml-Experiment-Entry-Script.md): `experiment.py` and its builder
- `contracts/contract_catalog_comments.md`, `contracts/contract_result_comments.md`: the rationale of each contract field
