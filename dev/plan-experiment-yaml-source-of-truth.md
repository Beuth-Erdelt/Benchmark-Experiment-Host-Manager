# Plan: `experiment.yaml` as the single source of truth

Status: **draft (2026-11-26), not implemented.** Direction decided by the user; scope, order and open
questions still to settle.

Related: [plan-explicit-rounds](plan-explicit-rounds.md) (first core step),
[Design-Yaml-Experiment-Entry-Script](Design-Yaml-Experiment-Entry-Script.md) (today's TPC-H-only YAML path),
[Design-Catalog-Contract](Design-Catalog-Contract.md) (catalog-driven `experiment.yml`, "Phase 2"),
[plan-start-conditions](plan-start-conditions.md) (later schema extension),
[plan-dbms-generic-verification](plan-dbms-generic-verification.md) (no DBMS names in Python).

---

## 1. Goal and decisions

| # | Decision |
|---|---|
| D1 | One file describes an experiment completely: `experiment.yaml`. A user or an agent writes it. |
| D2 | The experiment dict either goes away or is built from that file. |
| D3 | CLI options are helpers that build an `experiment.yaml` for the most common cases. The file is the powerful part: everything the CLI can do, the file can do, not the other way round. |
| D4 | The Python core stays generic. What belongs to a benchmark lives in `bexhoma/benchmarks/<benchmark>/`; what belongs to a DBMS lives in the `dockers:` section of `cluster.config`. |
| D5 | Structure is explicit (rounds, configurations). Shortcuts (`-ne`, sweeps) are expanded by builders, not by the core at run time. |

---

## 2. Today: three ways in

| Path | Input | How it reaches the objects | Scope |
|---|---|---|---|
| CLI | `tpch.py`, `tpcds.py`, … (`bexhoma/benchmarks/<x>/cli.py`) | argparse → `prepare_testbed(vars(args))` → setters → `add_benchmark_list()` | all benchmarks |
| Catalog-driven | `experiment.yml` + `contracts/contract_catalog.yml` | `bexhoma/spec.py` resolves profiles → **argv** → the benchmark's `run()` | TPC-H, YCSB |
| Self-specified | `experiment.yaml` (`tests/yaml_experiments/`) | `bexhoma/benchmarks/tpch/loader.py` + `builder.py` → parameter dict → `prepare_testbed()` → setters | TPC-H only, one configuration per system, `rounds: [1, 2]` only |

Where the state lives today:

| State | Where | Set from |
|---|---|---|
| Loader and benchmarker entries | `config.experiment_dict` (`loader`, `benchmarker`), per configuration; persisted as `bexhoma-experiment-dict-<config>-<code>.json` and read back by the evaluators | `experiment_dict_template` (benchmark class) + `add_benchmark_list()` |
| Experiment settings (mode, timeouts, monitoring, tenancy, keep SUT, DDL, durability, reset, …) | attributes of the experiment object, plus `experiment.args` / `args_dict` | `prepare_testbed(parameter)` (`bexhoma/experiments/base.py:785`) |
| Benchmark settings (TPC-H `-x…` flags, …) | `default_loading_parameters` / `default_benchmarking_parameters`, labels, query config | `configure_workload()` of the benchmark class, which reads `SimpleNamespace(**parameter)` |
| Configurations (DBMS, resources, storage, SUT parameters, workers, pooling) | configuration objects | `system_builder.build_configuration()` from `args` + `dockers:` |
| Sweeps | expanded into several configurations / rounds | `loading_layouts()`, `loading_variants()`, `pooling_variants()`, resource cells, storage classes, `-ne` |

CLI surface: 51 options in the base parser (`bexhoma/cli_args.py`) and 8–19 per benchmark (about 110
in total). `get_parameter_as_list()` reads list-valued options late, from `args_dict`
(about 50 calls: `num_loading_pods`, `num_benchmarking_threads`, `fio_iodepth`, …); `self.args.mode`
drives `process()`.

---

## 3. Target

```
CLI flags ──────────► builder (benchmarks/<x>/) ──┐
catalog experiment ─► resolver (spec.py) ─────────┼─► resolved experiment.yaml ─► validate ─► objects ─► run
hand / agent file ──► normalise (benchmarks/<x>/)─┘            │
                                                               └─► result folder: bexhoma-experiment-<code>.yaml
```

- **Authored vs. resolved.** A file may use shortcuts (`rounds: [1, 2, 4]`, sweep lists, catalog
  profiles). Normalising turns it into the **resolved form**: explicit configurations, explicit rounds,
  explicit entries, no shortcuts. Normalisers are benchmark code and live in the benchmark folders; the
  core accepts only the resolved form.
- **One run path.** The CLI no longer configures objects itself: it builds the resolved YAML and runs it.
  The catalog path does the same instead of building argv.
- **Persisted.** The resolved file is written to the result folder at start. `summary` mode, resume and
  the evaluators read it. The authored file is copied next to it (as today) for provenance.
- **DBMS details stay in `cluster.config`.** The YAML names a DBMS; image, templates, dialect and
  defaults come from `dockers:`. For reproducibility the used `dockers:` entries are copied into the
  result folder.

### Resolved form (sketch)

```yaml
schema_version: 1.0.0
bexhoma_version: 0.12.x
experiment:
  code: null
  mode: run                 # start | load | run | summary
  repetitions: 1            # -nc
  follow_up_of: null
  timeouts: {benchmark: 600, experiment: null, loading: null}
  max_sut: null
  labels: {usecase: tpc-h}
cluster: {context: null, aws: false, nodes: {sut: null, loading: null, benchmarking: null}}
monitoring: {sut: true, cluster: false, app: false, interval: 30s}
benchmark:                  # owned and validated by bexhoma/benchmarks/<name>/
  name: tpch
  scaling_factor: "10"
  settings: {init_indexes: true, recreate_parameter: false, active_queries: []}
defaults:                   # env shared by all entries of a phase
  loading: {SF: "10"}
  benchmarking: {SF: "10"}
configurations:             # explicit: one per SUT configuration, sweeps already expanded
  - name: PostgreSQL-1-1-1024
    dbms: PostgreSQL        # key of dockers: in cluster.config
    alias: DBMS A
    resources: {cpu: {request: "4", limit: "4"}, memory: {request: 16Gi, limit: 16Gi}}
    storage: {class: null, size: ""}
    sut_parameters: {}
    ddl: {}
    tenancy: null
    keep_sut: false
    loader:                 # today: experiment_dict['loader']
      - {name: tpch, template: ..., parallelism: 8, num_pods: 8, parameters: {}}
    benchmarker:            # today: experiment_dict['benchmarker']; rounds may differ
      - [{name: tpch, parallelism: 1, parameters: {}}]
      - [{name: tpch, parallelism: 2, parameters: {}}]
```

`configurations[i].loader` / `.benchmarker` have exactly the shape of today's experiment dict, so D2
starts as "the dict is a section of the file" and nothing downstream changes at first.

---

## 4. Work packages

| # | Package | Content |
|---|---|---|
| W1 | **Inventory** | Table of every CLI option (base + per benchmark), generated from the parsers: destination (experiment / benchmark / configuration / entry env / builder-only shortcut / runtime-only like `-db`), YAML key, default. The table is the checklist for everything below. A unit test fails when a new option has no row. |
| W2 | **Explicit rounds in the core** | [plan-explicit-rounds](plan-explicit-rounds.md) C1–C4: benchmark lookup by entry name, no per-round side lists, round 0 as template only in builders, `-nc` replays the rounds. |
| W3 | **Settings objects instead of `args`** | Replace `experiment.args` / `args_dict` / `get_parameter_as_list()` and `SimpleNamespace(**parameter)` in the benchmark classes with typed sections read from the resolved YAML. `prepare_testbed()` takes the resolved `experiment:` / `monitoring:` / … sections. Staged: first build today's parameter dict from the YAML (as the TPC-H builder does), then remove the dict. |
| W4 | **Generic loader and validator** | Core schema for the generic sections; each benchmark registers the schema of its `benchmark.settings` and its entry `parameters` through `bexhoma/benchmarks/registry.py`; DBMS compatibility through `system_descriptors`. Errors name the YAML path (`configurations[2].benchmarker[1][0].parallelism`). |
| W5 | **Builder per benchmark** | Split each `bexhoma/benchmarks/<x>/cli.py` into argparse → resolved YAML (pure function, no cluster) and the shared run path. Sweeps (`loading_layouts()`, `pooling_variants()`, resource cells, storage classes) move into the builder side. |
| W6 | **Equivalence tests** | For every command in `scripts/test-docs-*`, the CLI path and the YAML path give the same resolved YAML and the same objects (configurations, experiment dicts, env). Golden files in `tests/`. This is what makes W5 safe. |
| W7 | **`--print-yaml`** | Every entry script can print the resolved YAML for a command line without running it. Users learn the schema from their own commands; agents start from it. Cheap once W5 exists, useful before W8. |
| W8 | **Persist and read back** | Write `bexhoma-experiment-<code>.yaml` at start; `summary` mode, resume, `follow_up_of` and the evaluators read it. Old result folders keep working through the existing `bexhoma-experiment-dict-*.json` reader. |
| W9 | **One YAML entry script** | `bexhoma experiment <file>` runs any benchmark. `bexhoma/benchmarks/tpch/loader.py` / `builder.py` become the TPC-H normaliser on the generic path. |
| W10 | **Catalog path** | `spec.py` produces a resolved YAML instead of argv (Design-Catalog-Contract "Phase 2"). Contract versions bumped. |
| W11 | **Docs** | Schema reference page in `docs/`, one example file per benchmark in `tests/yaml_experiments/`, update [Architecture](../docs/Architecture.md). |

---

## 5. Order

1. W1 inventory: shows the real size of W3–W5.
2. W2 explicit rounds: generic, useful on its own, needed for #925.
3. W5 + W6 for one benchmark (TPC-H, it has the YAML path already), with W3 as far as TPC-H needs it.
4. W7 and W8.
5. W5 + W6 for the other benchmarks (TPC-DS, SSB, YCSB, Benchbase, HammerDB, hardware), finishing W3.
6. W9: one entry script; the TPC-H-specific loader goes away.
7. W11 docs.
8. W10 catalog path, last (agent / contract work is ranked at the end).
9. Later: [start conditions](plan-start-conditions.md) as a schema extension.

---

## 6. Open questions

| # | Question | Proposal |
|---|---|---|
| Q1 | One schema with optional shortcuts, or two schemas (authored, resolved)? | One schema. Shortcuts are allowed in authored files; the resolved file is the same schema with no shortcuts left. |
| Q2 | Sweeps in the file (lists that expand into configurations)? | Allowed as a shortcut, expanded by the benchmark's normaliser. The resolved form lists configurations explicitly. |
| Q3 | Does the experiment dict go away? | Not at first: it becomes the `loader` / `benchmarker` section of each configuration (same shape). Remove the separate attribute once nothing reads it apart from the file. |
| Q4 | `experiment.yml` (catalog-driven) and `experiment.yaml` (self-specified) look alike. | One file name and a `schema_version` key; the catalog form becomes an authored form that the resolver normalises. |
| Q5 | Where does the schema live? | Its own file (e.g. `contracts/contract_experiment.yml`), not inside `contract_catalog.yml`, which is near its size limit. Versioned like the other contracts. |
| Q6 | Runtime-only options (`-db`, `-rp`, `mode`)? | `mode` stays in the file (it decides what a run does); debug and report options stay CLI-only and override the file. |
| Q7 | A CLI run has no authored file. Is the resolved file in the result folder enough to repeat it as `bexhoma experiment <file>`? | Yes; additionally store the command line in it (`provenance.command`), so a reader sees which shortcut produced it. |
