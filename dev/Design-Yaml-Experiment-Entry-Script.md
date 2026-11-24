# Design: YAML-driven experiment entry script

> Status: **implemented; kept as a design note.** The plan dates from
> 2026-07-27. `experiment.py`, `bexhoma/benchmarks/tpch/loader.py`,
> `bexhoma/benchmarks/tpch/builder.py` and
> `tests/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml` exist. Where this note
> and the code disagree, the code is right. For the current structure see
> [Architecture](../docs/Architecture.md).
>
> Since then: the entry script `experiment.py` exists. The per-workload registry of section 2
> (`DBMS_DEFAULTS`, `DEFAULT_REFRESH_TEMPLATE`) no longer exists as a Python table: what it held
> (docker entry, SQL dialect, job templates, storage prefix) is part of the `dockers` section of
> `cluster.config` now, see [Benchmarks of a DBMS](../docs/DBMS.md#benchmarks-of-a-dbms). A DBMS may be named
> in `experiment.yaml` if its `tpch` entry has `experiment_yaml: True`, and the default `alias` of a system is
> the `template.alias` of its DBMS.

## Goal

A new entry script, callable as `bexhoma experiment experiment.yaml`, that
reads a full experiment definition from a YAML file and builds the running
`Experiment`/`SutConfiguration` objects **directly in Python** — no argv is
generated, no subprocess is spawned, nothing is re-parsed through `tpch.py`'s
own CLI. This is a different, parallel path from `bexhoma/spec.py` (see
"Relation to `bexhoma/spec.py`" below).

## Scope decisions (already made — do not re-litigate without reason)

These three were explicitly asked and answered by the user before this plan
was written:

1. **Workload scope: TPC-H only, first.** Prove the design on one workload
   (mirrors `tpch.py`'s per-DBMS loop) before extending to TPC-DS / YCSB /
   Benchbase / HammerDB in follow-up passes.
2. **Per-DBMS build details (docker image key, SQL dialect, jobtemplate
   filenames, storage-config naming) come from a new per-workload registry
   table**, not from fully-explicit YAML. The YAML just names the DBMS plus
   overrides; the registry mirrors today's `if "PostgreSQL" in args.dbms:`
   branches as data instead of code.
3. **The new script still calls `ExperimentBase.prepare_testbed(parameter:
   dict)`.** That method is the internal seam every existing entry script
   already funnels through (~40 fields, expects an argparse-`Namespace`-shaped
   dict). Reimplementing its logic by hand would duplicate a lot of
   already-working code and drift out of sync over time. The dict it expects
   is built **in Python, from the YAML** — never from a typed CLI flag
   string, never via `argv`/subprocess. That is what "does not route to CLI
   parameters" means in this plan: no human-typed flags, no shelling out to
   `tpch.py`; the dict-shaped internal contract is still reused because it's
   the established convention, not a CLI.

## Why `prepare_testbed()` stays in the loop

It's the seam every existing entry script already funnels through. What it
does **not** get in this design is CLI routing: no argv is built, no flags
are typed, no subprocess runs `tpch.py`. We just need its dict populated by
code instead of by argparse.

## Files to add / change

### 1. `tpch.py` (repo root) — extract the parser

Extract the existing argparse block (currently lines ~73–89) into a new
function:

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', ...)
    parser.add_argument('-dbms', ...)
    ... # all the existing -x... arguments, unchanged
    return parser
```

`if __name__ == '__main__':` then calls `parser = build_parser(); args =
parser.parse_args()` exactly as today. **Pure extraction, zero behavior
change.** This makes the parser importable, so the new builder gets real,
single-sourced defaults via `build_parser().parse_args([mode])` instead of
hand-copying ~20 dest names and defaults a second time — which is the wart
`dev/spec_prototype_demo.py` already has today (it duplicates `tpch.py`'s
parser by hand) and should not be repeated.

### 2. `bexhoma/benchmarks/tpch/experiment.py` — add `DBMS_DEFAULTS` (superseded, see the update at the top)

A new, data-only module-level dict, values extracted from (not duplicating
the logic of) `tpch.py`'s existing per-DBMS branches:

```python
DBMS_DEFAULTS = {
    'PostgreSQL': {
        'docker': 'PostgreSQL', 'dialect': 'PostgreSQL',
        'jobtemplate_loading': 'jobtemplate-loading-tpch-PostgreSQL.yml',
        'storage_prefix': 'postgresql',
    },
    'PgDuckDB': {
        'docker': 'PgDuckDB', 'dialect': 'PostgreSQL',
        'jobtemplate_loading': 'jobtemplate-loading-tpch-PostgreSQL.yml',
        'storage_prefix': 'PgDuckDB', 'path_experiment_docker': 'PostgreSQL',
    },
    'MonetDB': {
        'docker': 'MonetDB', 'dialect': 'MonetDB',
        'jobtemplate_loading': 'jobtemplate-loading-tpch-MonetDB.yml',
        'storage_prefix': 'monetdb',
    },
    'MariaDB': {
        'docker': 'MariaDB', 'dialect': 'MySQL',
        'jobtemplate_loading': 'jobtemplate-loading-tpch-MariaDB.yml',
        'storage_prefix': 'mariadb',
    },
    'MySQL': {
        'docker': 'MySQL', 'dialect': 'MySQL',
        'jobtemplate_loading': 'jobtemplate-loading-tpch-MySQL.yml',
        'storage_prefix': 'mysql',
    },
    'CedarDB': {
        'docker': 'CedarDB', 'dialect': 'PostgreSQL',
        'jobtemplate_loading': 'jobtemplate-loading-tpch-PostgreSQL.yml',
        'storage_prefix': 'cedardb',
    },
}
```

**Explicitly excluded from phase 1**: `Citus` (needs worker-sharding
ddl/sut parameters — real per-DBMS *logic*, not data) and container-tenancy
(`tenant_per == 'container'`, the multi-tenant loop in `tpch.py`). Both are
follow-up work once the simple single-cell path is proven.

### 3. `bexhoma/benchmarks/tpch/loader.py` (new)

```python
def load_experiment_yaml(path: str) -> dict:
    """yaml.safe_load wrapper, mirrors bexhoma/spec.py::load_experiment."""

def validate_experiment_yaml(spec: dict) -> None:
    """Required keys present; workload == 'tpch' for now; every
    systems[].dbms key exists in bexhoma.benchmarks.tpch.benchmark.experiment.DBMS_DEFAULTS."""
```

### 4. `bexhoma/benchmarks/tpch/builder.py` (new)

`build_experiment(spec: dict) -> TpchExperiment`:

1. Build `cluster` (`clusters.AWS` / `clusters.Kubernetes`) from
   `spec['cluster']`.
2. Resolve `SF` via the existing `bexhoma.cli_args.resolve_scaling_factor()`
   (unchanged, reused so `mode: summary` keeps resuming with the
   already-persisted scale factor, exactly like every CLI entry script).
3. Construct `TpchExperiment(cluster=..., SF=..., timeout=..., code=...,
   num_experiment_to_apply=...)`. Set `prometheus_interval`,
   `set_active_queries()`, `set_additional_labels()`,
   `set_default_loading_parameters()`, `set_default_benchmarking_parameters()`,
   and refresh-stream enabling — all direct calls with YAML-sourced values,
   exactly like `tpch.py` does today. No CLI flags involved anywhere in this
   step.
4. Build the `parameter` dict for `prepare_testbed()`:
   - baseline: `vars(tpch.build_parser().parse_args([spec['mode']]))` — this
     is `tpch.py`'s own real argparse defaults, gotten by feeding the parser
     a synthetic single-element argv (`[mode]`), not a human-typed command
     line.
   - overlay every YAML-set field onto its argparse **dest** name via a
     small, explicit mapping table (e.g. `experiment.timeout` → `timeout`,
     `tpch.recreate_parameter` → `recreate_parameter`, `rounds` →
     `num_query_executors` joined as a comma string for parity with how
     `prepare_testbed()`/`configure_workload()` expect it).
   - call `experiment.prepare_testbed(parameter)`.
5. For each entry in `spec['systems']`: look up
   `bexhoma.benchmarks.tpch.benchmark.experiment.DBMS_DEFAULTS[dbms]`, build a
   `configurations.default(experiment=experiment, docker=..., dialect=...,
   configuration=..., alias=...)`, and call the same setter sequence
   `tpch.py`'s PostgreSQL branch calls — `set_resources()`, `set_storage()`,
   `set_loading_parameters()`, `set_benchmarking_parameters()`,
   `set_loading()`, `set_sut_parameters()` if given — sourcing every value
   from that system's YAML block, falling back to `storage_prefix` for
   storage naming when the YAML doesn't override it.
6. Call `experiment.add_benchmark_list(rounds)` then `experiment.process()`.

### 5. `experiment.py` (new, repo root)

The entry script itself. Discoverable automatically by
`bexhoma/scripts/cli.py`'s file-walk (`_find_script()`) — **no changes needed
to `cli.py`**.

```python
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a bexhoma experiment from a YAML definition.")
    parser.add_argument('file', nargs='?', default='experiment.yaml',
                         help='path to the experiment YAML file')
    args = parser.parse_args()
    spec = experiment_loader.load_experiment_yaml(args.file)
    experiment_loader.validate_experiment_yaml(spec)
    experiment = experiment_builder.build_experiment(spec)
exit()
```

That positional `file` is the **entire** CLI surface — mode, DBMS list,
resources, everything else comes from the file. Invocation:
`bexhoma experiment experiment.yaml` or `python experiment.py experiment.yaml`.

### 6. `tests/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml` (new)

A worked example, see schema sketch below.

## YAML schema (sketch)

```yaml
workload: tpch
mode: run

# Optional provenance pointers — see "Provenance" section below.
# Purely informational: the builder never loads or resolves these, it only
# copies them into the result folder for reproducibility.
catalog: contracts/contract_catalog.yml
environment: dev/catalog/environment.yml

experiment:
  code: null              # null = new experiment; set to resume an existing one
  num_config: 1           # -nc
  timeout: 600            # -t
  scaling_factor: "100"   # -sf

cluster:
  aws: false
  context: null            # null = current kubectl context

monitoring:
  sut: true                # -m
  cluster: false            # -mc
  app: false                # -ma

rounds: [1, 2, 4]           # -ne sweep (list of client counts)

loading:
  pods: [1]                 # -nlp, one value (no sweep: one configuration per system)
  threads: [1]               # -nlt, one value
  split: 1                   # -xnls, one value, at most pods

tpch:                        # TPC-H's own -x flags
  recreate_parameter: false
  shuffle_queries: false
  init_indexes: true
  init_constraints: true
  init_statistics: true
  init_columns: false
  datatransfer: false
  active_queries: []
  refresh_streams: 0
  refresh_stream_offset: 0
  duckdb_force_execution: false

systems:
  - dbms: PostgreSQL
    configuration: ""          # optional override of configuration name
    alias: "PG"                # optional; default: the template.alias of the DBMS
    resources:
      cpu: {request: "4", limit: "4"}
      memory: {request: "16Gi", limit: "16Gi"}
    storage:
      class: null
      size: ""
    skip_loading: false
    sut_parameters: {}
    loading_parameters: {}     # extra/overriding env for the loader
    benchmarking_parameters: {}
  - dbms: PgDuckDB
    resources:
      cpu: {request: "4", limit: "4"}
      memory: {request: "16Gi", limit: "16Gi"}
    sut_parameters:
      DUCKDB_FORCE_EXECUTION: "true"
```

## Provenance: copy input YAMLs into the result folder

**New requirement, added after the initial plan.** Every experiment result
folder (`{resultfolder}/{code}/`) must end up with a durable copy of exactly
what produced it, mirroring the existing provenance philosophy already in the
codebase (see `docs/AgentResultContract.md`, `report_writer.py`'s
cross-referencing).

1. **Always** copy the `experiment.yaml` that was actually used into
   `{resultfolder}/{code}/experiment.yaml` — do this in `experiment.py` (or
   `tpch_builder.build_experiment()`) right after `code`/`path` are
   known, i.e. right after the `TpchExperiment` is constructed. If an
   experiment is resumed (`experiment.code` already existed), overwrite is
   fine — same experiment, same code, the file should reflect the run that
   is currently happening.
2. **Optionally** the experiment.yaml carries top-level `catalog:` and
   `environment:` keys — plain file paths, resolved relative to the
   experiment.yaml's own directory unless absolute. These are **pure
   provenance pointers**: they record which `catalog.yaml`
   (`bexhoma/spec.py`'s profile/knob catalog) and which `environment.yml`
   (`bexhoma/environment.py`'s cluster snapshot) a human or tool consulted
   while hand-writing this experiment.yaml's `systems:`/resource values. The
   builder **never loads or resolves** them — the experiment.yaml stays
   fully self-specified and authoritative, exactly as designed above; this
   is bookkeeping only, not a second resolution path.
3. If `catalog`/`environment` are present and the referenced files exist,
   copy them too, into `{resultfolder}/{code}/catalog.yaml` and
   `{resultfolder}/{code}/environment.yml` respectively. Missing files (a
   stale path, or the fields simply omitted) are silently skipped — this is
   best-effort provenance, not a hard requirement, so it must never abort an
   otherwise-valid run.
4. Implementation location: a small helper in `bexhoma/benchmarks/tpch/builder.py`,
   e.g. `_copy_provenance_files(spec: dict, spec_path: str, result_path: str)`,
   called once from `build_experiment()` after `experiment.path` exists.
   Plain `shutil.copyfile`, no YAML re-serialization — copy the bytes the
   user actually authored, not a round-tripped `yaml.safe_dump()` of the
   parsed structure (which could silently reformat or drop comments).

This gives full reproducibility: anyone opening a result folder later — a
teammate, a future Claude Code session, an `AgentReport.md` reader — can see
exactly which experiment.yaml (and, if the author used one, which catalog and
environment snapshot) produced this specific run, without needing external
version control history.

## Relation to `bexhoma/spec.py`

Deliberately separate, and left untouched by this plan:

- **`bexhoma/spec.py`** translates a *catalog-driven* `experiment.yml`
  (profiles, `derive:` formulas, resolved against `catalog.yaml`) into a
  **CLI argv**, for a human or CI to actually run. `spec.py` itself is
  workload-agnostic (catalog loading, knob resolution, validation); it
  dispatches by `workload.name` to that workload's own argv builder —
  today `bexhoma/benchmarks/tpch/catalog.py` (`build_tpch_argv()`) and
  `bexhoma/benchmarks/ycsb/catalog.py` (`build_ycsb_argv()`), which own
  the actual `tpch.py`/`ycsb.py` flag mapping and PostgreSQL GUC
  formatting. Scope today: TPC-H against PostgreSQL/PgDuckDB, YCSB against
  PostgreSQL. `experiment.py`'s catalog-driven branch dispatches the
  resolved argv to that workload's own `run()` in-process.
- **This new path** takes a *fully self-specified* `experiment.yaml`
  straight into Python objects — no argv is ever generated, nothing is
  handed to a shell.

Different schema, different files, on purpose. Unifying them (catalog-driven
knob resolution feeding directly into this in-process builder, instead of
`spec.py`'s current argv round-trip) is exactly the "Phase 2" territory
`dev/Design-Catalog-Contract.md` already flags as future work — not part of
this plan. The optional `catalog:`/`environment:` provenance pointers above
are the only place the two paths touch, and only for copying files, never for
resolution.

## Testing

Unit tests for `tpch_loader`/`tpch_builder` against a stub
cluster object (no live Kubernetes cluster needed) — assert the resulting
`TpchExperiment.configurations` list has the right `SutConfiguration`
attributes set, and that the provenance files land in the stub result
folder. Mirrors how `report_writer.py` was tested with fake objects (see
memory: "Docs fixes + agent summary plan").

## Implementation order

1. `tpch.py`: extract `build_parser()`. Verify `python tpch.py run ...`
   behaves identically (no behavior change expected).
2. `bexhoma/benchmarks/tpch/experiment.py`: add `DBMS_DEFAULTS`.
3. `bexhoma/benchmarks/tpch/loader.py`: `load_experiment_yaml()` +
   `validate_experiment_yaml()`.
4. `bexhoma/benchmarks/tpch/builder.py`: `build_experiment()`, including the
   provenance-copy helper.
5. `experiment.py`: the entry script.
6. `tests/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml`: worked example.
7. Unit tests (stub cluster) for loader + builder, including provenance
   copying.
8. Manual smoke test against a real (or kind/minikube) cluster:
   `bexhoma experiment tests/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml`.

## Example Run

The worked example compares PostgreSQL and PgDuckDB at SF 1 in rounds of 1, 2 and 4 clients.
PostgreSQL has the alias set in the YAML (`DBMS A2`), PgDuckDB the `template.alias` of its DBMS, and its SUT runs with `DUCKDB_FORCE_EXECUTION=true`.
The YAML has no keys for node pinning or `-tr`, so the pods go to any node and the result is not checked as with `-tr`.
The run is part of `scripts/test-docs-tpch.sh`:

```bash
bexhoma experiment tests/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml &>$LOG_DIR/docs_tpch_yaml_experiment.log
```

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_yaml_experiment_summary.md" target="_blank" rel="noopener">docs_tpch_yaml_experiment.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 573s 
* Code: 1795449026
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 600.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['PostgreSQL', 'PgDuckDB'].
  * Import is handled by 1 processes (pods).
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1, 2, 4] times the number of benchmarking pods.
  * Experiment is run once.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* pgduckdb-1-1-1-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826148
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* pgduckdb-1-1-2-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826148
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* pgduckdb-1-1-2-1-2 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826148
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* pgduckdb-1-1-3-1-1 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826149
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* pgduckdb-1-1-3-1-2 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826149
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* pgduckdb-1-1-3-1-3 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826149
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* pgduckdb-1-1-3-1-4 uses docker image pgduckdb/pgduckdb:18-v1.1.1
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826149
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'shared_preload_libraries=pg_duckdb', '-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826148
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* postgresql-1-1-2-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826148
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* postgresql-1-1-2-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826148
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* postgresql-1-1-3-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826149
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* postgresql-1-1-3-1-2 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826149
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* postgresql-1-1-3-1-3 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826149
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026
* postgresql-1-1-3-1-4 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:826149
  * datadisk:2758
  * volume_size:1.8T
  * volume_used:807G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_cpu:4
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1795449026

### Ingestion
* PgDuckDB-1: 8 of 8 units ok
* PostgreSQL-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-pgduckdb-1-1795449026-7f9b78f5bd-lsgrk: 0
* bexhoma-sut-postgresql-1-1795449026-567547fddf-dz57k: 0

### Workflow

#### Actual

* DBMS PgDuckDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 3: tpch (4 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: tpch (4 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 3: tpch (4 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 1: tpch (1 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 2: tpch (2 pods)
* DBMS PgDuckDB-1 - Experiment 1 Client 3: tpch (4 pods)

### Loading

#### Per Run

| DBMS           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   threads | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|----------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| PgDuckDB-1-1   |                1 |    1 |       56.00 |           2.00 |            0.00 |         37.00 |           14.00 |              1 |         0 |             | None           |             0 | False         |               64.29 | False               |
| PostgreSQL-1-1 |                1 |    1 |       62.00 |           4.00 |            0.00 |         38.00 |           17.00 |              1 |         0 |             | None           |             0 | False         |               58.06 | False               |

### Benchmarking

#### Per Connection

| connection           | phase            | job                |   experiment_run |   client |   benchmark_run |   child |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:---------------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|--------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1-1-1   | pgduckdb-1-1-1   | pgduckdb-1-1-1-1   |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         21 |            0.63 |             5732.88 |           3771.43 |          -1 |
| pgduckdb-1-1-2-1-1   | pgduckdb-1-1-2   | pgduckdb-1-1-2-1   |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         26 |            0.95 |             3803.83 |           3046.15 |          -1 |
| pgduckdb-1-1-2-1-2   | pgduckdb-1-1-2   | pgduckdb-1-1-2-1   |                1 |        2 |               1 |       2 | 1.00 |               22 |                  22 |         27 |            0.94 |             3824.56 |           2933.33 |          -1 |
| pgduckdb-1-1-3-1-1   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       1 | 1.00 |               22 |                  22 |         50 |            1.77 |             2034.83 |           1584.00 |          -1 |
| pgduckdb-1-1-3-1-2   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       2 | 1.00 |               22 |                  22 |         49 |            1.75 |             2059.82 |           1616.33 |          -1 |
| pgduckdb-1-1-3-1-3   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       3 | 1.00 |               22 |                  22 |         49 |            1.75 |             2061.81 |           1616.33 |          -1 |
| pgduckdb-1-1-3-1-4   | pgduckdb-1-1-3   | pgduckdb-1-1-3-1   |                1 |        3 |               1 |       4 | 1.00 |               22 |                  22 |         50 |            1.78 |             2027.05 |           1584.00 |          -1 |
| postgresql-1-1-1-1-1 | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |       1 | 1.00 |               22 |                  22 |         12 |            0.24 |            14851.05 |           6600.00 |          -1 |
| postgresql-1-1-2-1-1 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       1 | 1.00 |               22 |                  22 |         17 |            0.36 |             9986.63 |           4658.82 |          -1 |
| postgresql-1-1-2-1-2 | postgresql-1-1-2 | postgresql-1-1-2-1 |                1 |        2 |               1 |       2 | 1.00 |               22 |                  22 |         17 |            0.37 |             9843.93 |           4658.82 |          -1 |
| postgresql-1-1-3-1-1 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       1 | 1.00 |               22 |                  22 |         24 |            0.53 |             6734.19 |           3300.00 |          -1 |
| postgresql-1-1-3-1-2 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       2 | 1.00 |               22 |                  22 |         27 |            0.50 |             7178.07 |           2933.33 |          -1 |
| postgresql-1-1-3-1-3 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       3 | 1.00 |               22 |                  22 |         25 |            0.55 |             6502.98 |           3168.00 |          -1 |
| postgresql-1-1-3-1-4 | postgresql-1-1-3 | postgresql-1-1-3-1 |                1 |        3 |               1 |       4 | 1.00 |               22 |                  22 |         26 |            0.56 |             6445.82 |           3046.15 |          -1 |

#### Per Phase

| DBMS             | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| pgduckdb-1-1-1   | pgduckdb-1-1-1   |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         21 |            0.63 |             5732.88 |           3771.43 |          -1 |
| pgduckdb-1-1-2   | pgduckdb-1-1-2   |                1 |        2 |               1 |           2 | 1.00 |               44 |                  44 |         27 |            0.94 |             3814.18 |           5866.67 |          -1 |
| pgduckdb-1-1-3   | pgduckdb-1-1-3   |                1 |        3 |               1 |           4 | 1.00 |               88 |                  88 |         50 |            1.76 |             2045.82 |           6336.00 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         12 |            0.24 |            14851.05 |           6600.00 |          -1 |
| postgresql-1-1-2 | postgresql-1-1-2 |                1 |        2 |               1 |           2 | 1.00 |               44 |                  44 |         17 |            0.36 |             9915.02 |           9317.65 |          -1 |
| postgresql-1-1-3 | postgresql-1-1-3 |                1 |        3 |               1 |           4 | 1.00 |               88 |                  88 |         27 |            0.54 |             6709.20 |          11733.33 |          -1 |

#### Query Completion per Phase

| phase            |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:-----------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| pgduckdb-1-1-1   |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| pgduckdb-1-1-2   |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| pgduckdb-1-1-3   |      4 | 4/4                                 | 4/4                                      | 4/4                            | 4/4                                        | 4/4                                | 4/4                                     | 4/4                                | 4/4                                | 4/4                                      | 4/4                                         | 4/4                                          | 4/4                                             | 4/4                                 | 4/4                                  | 4/4                              | 4/4                                       | 4/4                                        | 4/4                                 | 4/4                              | 4/4                                    | 4/4                                                   | 4/4                                          | yes        |
| postgresql-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |
| postgresql-1-1-2 |      2 | 2/2                                 | 2/2                                      | 2/2                            | 2/2                                        | 2/2                                | 2/2                                     | 2/2                                | 2/2                                | 2/2                                      | 2/2                                         | 2/2                                          | 2/2                                             | 2/2                                 | 2/2                                  | 2/2                              | 2/2                                       | 2/2                                        | 2/2                                 | 2/2                              | 2/2                                    | 2/2                                                   | 2/2                                          | yes        |
| postgresql-1-1-3 |      4 | 4/4                                 | 4/4                                      | 4/4                            | 4/4                                        | 4/4                                | 4/4                                     | 4/4                                | 4/4                                | 4/4                                      | 4/4                                         | 4/4                                          | 4/4                                             | 4/4                                 | 4/4                                  | 4/4                              | 4/4                                       | 4/4                                        | 4/4                                 | 4/4                              | 4/4                                    | 4/4                                                   | 4/4                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   pgduckdb-1-1-1-1-1 |   pgduckdb-1-1-2-1-1 |   pgduckdb-1-1-2-1-2 |   pgduckdb-1-1-3-1-1 |   pgduckdb-1-1-3-1-2 |   pgduckdb-1-1-3-1-3 |   pgduckdb-1-1-3-1-4 |   postgresql-1-1-1-1-1 |   postgresql-1-1-2-1-1 |   postgresql-1-1-2-1-2 |   postgresql-1-1-3-1-1 |   postgresql-1-1-3-1-2 |   postgresql-1-1-3-1-3 |   postgresql-1-1-3-1-4 |
|:----------------------------------------------------|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|
| Pricing Summary Report (TPC-H Q1)                   |              1946.26 |              1147.74 |              2352.36 |              3006.93 |              2374.42 |              2535.59 |              3007.74 |                1765.80 |                1838.09 |                1818.88 |                2281.30 |                9073.95 |                2976.40 |                2935.56 |
| Minimum Cost Supplier Query (TPC-H Q2)              |               332.52 |               791.11 |               419.41 |              1091.77 |               756.43 |               818.70 |               870.99 |                 163.17 |                 187.89 |                 189.31 |                 710.06 |                 528.43 |                 206.08 |                 239.79 |
| Shipping Priority (TPC-H Q3)                        |               665.69 |              1450.71 |              1061.62 |              2474.29 |              2374.59 |              2326.07 |              2949.76 |                 256.84 |                 896.11 |                 888.45 |                 469.12 |                 545.04 |                 651.31 |                 628.21 |
| Order Priority Checking Query (TPC-H Q4)            |               641.78 |               803.61 |              1120.46 |              1777.86 |              1903.32 |              1971.79 |              1710.15 |                 111.22 |                 387.51 |                 453.99 |                 238.42 |                 259.93 |                 312.40 |                 334.79 |
| Local Supplier Volume (TPC-H Q5)                    |               797.61 |              1711.97 |              1888.04 |              3700.46 |              2578.93 |              2193.29 |              3694.84 |                 193.19 |                 300.36 |                 300.62 |                 635.30 |                 333.35 |                 837.85 |                 835.55 |
| Forecasting Revenue Change (TPC-H Q6)               |               431.79 |               662.44 |               603.66 |              1246.79 |              2179.62 |              2194.94 |              1335.96 |                 139.16 |                 449.35 |                 449.94 |                 347.82 |                 546.66 |                 688.37 |                 681.48 |
| Volume Shipping Query (TPC-H Q7)                    |               739.19 |              1594.53 |              1070.21 |              2579.52 |              1927.98 |              1994.02 |              2679.97 |                 223.85 |                 379.22 |                 378.84 |                1306.18 |                 629.03 |                 572.74 |                 572.42 |
| National Market Share (TPC-H Q8)                    |              1443.69 |              1523.74 |              1793.85 |              3953.76 |              3481.07 |              3482.05 |              3865.68 |                 113.28 |                 137.84 |                 142.76 |                 266.11 |                 112.89 |                 301.33 |                 301.44 |
| Product Type Profit Measure (TPC-H Q9)              |               993.95 |              1480.37 |              2557.55 |              3904.14 |              4764.61 |              4366.77 |              3788.52 |                 400.28 |                 732.33 |                 693.37 |                 762.37 |                1047.23 |                1022.64 |                1050.16 |
| Returned Item Reporting Query (TPC-H Q10)           |               606.11 |              1555.28 |               827.65 |              1777.65 |              1877.11 |              1768.06 |              1741.82 |                 222.40 |                 291.62 |                 310.56 |                 647.52 |                1205.09 |                 617.81 |                 616.20 |
| Important Stock Identification (TPC-H Q11)          |               157.32 |               558.82 |               376.42 |               587.46 |               512.29 |               684.34 |               732.07 |                  52.58 |                  59.55 |                  59.18 |                 147.87 |                 122.48 |                  61.32 |                  61.91 |
| Shipping Modes and Order Priority (TPC-H Q12)       |               583.92 |               980.70 |               952.00 |              1805.27 |              1673.93 |              1583.19 |              1805.15 |                 248.17 |                 655.25 |                 654.56 |                 567.30 |                 857.19 |                 609.55 |                 631.89 |
| Customer Distribution (TPC-H Q13)                   |               260.27 |               344.43 |               306.99 |               732.37 |               783.63 |               671.08 |               732.75 |                 692.76 |                 854.29 |                1063.76 |                1052.95 |                2030.82 |                1215.35 |                1250.49 |
| Promotion Effect Query (TPC-H Q14)                  |               648.64 |               675.45 |              1602.65 |              1792.90 |              1620.85 |              1504.61 |              1902.05 |                 445.54 |                 239.22 |                 460.55 |                 350.88 |                 703.05 |                 450.39 |                 525.64 |
| Top Supplier Query (TPC-H Q15)                      |               979.30 |               761.03 |               720.06 |              1852.33 |              1261.35 |              1400.96 |              1734.14 |                 449.14 |                 401.22 |                 308.66 |                 429.68 |                 835.07 |                 409.93 |                 525.07 |
| Parts/Supplier Relationship (TPC-H Q16)             |               265.37 |               314.75 |               416.95 |               605.83 |               593.16 |               500.41 |               516.07 |                 340.48 |                 347.04 |                 289.11 |                 237.32 |                 512.28 |                 362.70 |                 287.38 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |              1293.95 |              2392.45 |              1972.61 |              4664.44 |              3443.86 |              3981.71 |              4263.81 |                 543.57 |                 551.66 |                 584.86 |                1144.35 |                1222.22 |                 880.84 |                2437.75 |
| Large Volume Customer (TPC-H Q18)                   |               569.07 |               720.57 |              1500.98 |              1727.26 |              1505.96 |              1725.67 |              2095.91 |                2179.98 |                4911.37 |                4845.08 |                8044.97 |                3863.13 |                8002.94 |                6933.37 |
| Discounted Revenue (TPC-H Q19)                      |               558.91 |               872.72 |               886.66 |              2277.72 |              2380.26 |              2335.46 |              1776.54 |                  40.42 |                  71.33 |                  88.89 |                 112.43 |                  41.61 |                 125.27 |                 133.49 |
| Potential Part Promotion (TPC-H Q20)                |               646.83 |               981.23 |               926.78 |              1912.76 |              2204.37 |              2301.98 |              2219.17 |                 120.81 |                 138.15 |                 108.64 |                 305.57 |                  86.67 |                 379.02 |                 242.09 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |              2680.11 |              3247.13 |              1927.65 |              3691.41 |              5670.45 |              5969.40 |              4020.01 |                 241.05 |                 444.73 |                 321.56 |                 682.46 |                 305.39 |                 634.23 |                1150.00 |
| Global Sales Opportunity Query (TPC-H Q22)          |               203.64 |               302.82 |               195.76 |               295.87 |               627.09 |               508.85 |               295.22 |                  67.22 |                  74.89 |                  75.11 |                 221.60 |                  68.93 |                 441.89 |                 118.55 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   |        36.16 |      0.58 |           1.75 |                  3.30 |
| pgduckdb-1-1-2-1   |        36.16 |      0.58 |           1.75 |                  3.30 |
| pgduckdb-1-1-3-1   |        36.16 |      0.58 |           1.75 |                  3.30 |
| postgresql-1-1-1-1 |        16.62 |      0.54 |           0.51 |                  1.72 |
| postgresql-1-1-2-1 |        16.62 |      0.54 |           0.51 |                  1.72 |
| postgresql-1-1-3-1 |        16.62 |      0.54 |           0.51 |                  1.72 |

### Loading phase: component data generator

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| pgduckdb-1-1-2-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| pgduckdb-1-1-3-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-3-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS               |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|-------------:|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   |         5.89 |      0.00 |           0.00 |                  0.31 |
| pgduckdb-1-1-2-1   |         5.89 |      0.00 |           0.00 |                  0.31 |
| pgduckdb-1-1-3-1   |         5.89 |      0.00 |           0.00 |                  0.31 |
| postgresql-1-1-1-1 |         3.69 |      0.00 |           0.01 |                  0.30 |
| postgresql-1-1-2-1 |         3.69 |      0.00 |           0.01 |                  0.30 |
| postgresql-1-1-3-1 |         3.69 |      0.00 |           0.01 |                  0.30 |

### Benchmarking phase: SUT deployment

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.76 |           1.81 |                  3.44 |
| pgduckdb-1-1-2-1   | n/a          |      0.93 |           1.86 |                  3.49 |
| pgduckdb-1-1-3-1   | 171.43       |      3.99 |           2.07 |                  3.73 |
| postgresql-1-1-1-1 | n/a          |      0.53 |           1.92 |                  3.55 |
| postgresql-1-1-2-1 | n/a          |      0.42 |           1.89 |                  3.52 |
| postgresql-1-1-3-1 | n/a          |      0.00 |           1.89 |                  3.52 |

### Benchmarking phase: component benchmarker

| DBMS               | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------|:-------------|----------:|---------------:|----------------------:|
| pgduckdb-1-1-1-1   | n/a          |      0.00 |           0.31 |                  0.32 |
| pgduckdb-1-1-2-1   | n/a          |      0.00 |           0.00 |                  0.00 |
| pgduckdb-1-1-3-1   | 46.85        |      0.04 |           0.31 |                  0.31 |
| postgresql-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| postgresql-1-1-3-1 | n/a          |      0.00 |           0.35 |                  0.35 |

### Missing Monitoring Metrics
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage, Working Set [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection pgduckdb-1-1-1-1 (bexhoma-metrics-pgduckdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection pgduckdb-1-1-2-1 (bexhoma-metrics-pgduckdb-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU User Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU System Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-datagenerator.log, expected: data pre-existing)
* CPU Utilization [CPUs] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-1-1 (bexhoma-metrics-postgresql-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU System Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Network Rx Total [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection postgresql-1-1-2-1 (bexhoma-metrics-postgresql-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection postgresql-1-1-3-1 (bexhoma-metrics-postgresql-1-1-3-1-benchmarker.log, expected: phase shorter than scrape interval)
Experiment                    : cleaning up per-connection artefacts
Experiment                    : cleaning up per-connection artefacts completed

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (data pre-existing; job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>
