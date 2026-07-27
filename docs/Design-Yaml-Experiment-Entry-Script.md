# Design: YAML-driven experiment entry script

> Status: **planned, not implemented**. This document is the full plan agreed
> with the user on 2026-07-27; hand it to Claude Code on any machine and say
> "implement this plan" to pick up the work.

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

### 2. `bexhoma/experiments/tpch.py` — add `DBMS_DEFAULTS`

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

### 3. `bexhoma/experiment_loader.py` (new)

```python
def load_experiment_yaml(path: str) -> dict:
    """yaml.safe_load wrapper, mirrors bexhoma/spec.py::load_experiment."""

def validate_experiment_yaml(spec: dict) -> None:
    """Required keys present; workload == 'tpch' for now; every
    systems[].dbms key exists in bexhoma.experiments.tpch.DBMS_DEFAULTS."""
```

### 4. `bexhoma/experiment_builder.py` (new)

`build_experiment(spec: dict) -> TpchExperiment`:

1. Build `cluster` (`clusters.AWS` / `clusters.Kubernetes`) from
   `spec['cluster']`.
2. Resolve `SF` via the existing `bexhoma.cli_args.resolve_scaling_factor()`
   (unchanged, reused so `mode: summary` keeps resuming with the
   already-persisted scale factor, exactly like every CLI entry script).
3. Construct `experiments.tpch(cluster=..., SF=..., timeout=..., code=...,
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
   `bexhoma.experiments.tpch.DBMS_DEFAULTS[dbms]`, build a
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

### 6. `dev/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml` (new)

A worked example, see schema sketch below.

## YAML schema (sketch)

```yaml
workload: tpch
mode: run

# Optional provenance pointers — see "Provenance" section below.
# Purely informational: the builder never loads or resolves these, it only
# copies them into the result folder for reproducibility.
catalog: dev/catalog/catalog.yaml
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
  pods: [1]                 # -nlp sweep
  threads: [1]               # -nlt
  split: 1                   # -xnls

tpch:                        # TPC-H's own -x flags
  recreate_parameter: false
  shuffle_queries: false
  init_indexes: false
  init_constraints: false
  init_statistics: false
  init_columns: false
  datatransfer: false
  active_queries: []
  refresh_streams: 0
  refresh_stream_offset: 0
  duckdb_force_execution: false

systems:
  - dbms: PostgreSQL
    configuration: ""          # optional override of configuration name
    alias: "DBMS A2"
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
   `experiment_builder.build_experiment()`) right after `code`/`path` are
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
4. Implementation location: a small helper in `bexhoma/experiment_builder.py`,
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
  `tpch.py` **CLI argv**, for a human or CI to actually run. Scope today:
  TPC-H against PostgreSQL/PgDuckDB only.
- **This new path** takes a *fully self-specified* `experiment.yaml`
  straight into Python objects — no argv is ever generated, nothing is
  handed to a shell.

Different schema, different files, on purpose. Unifying them (catalog-driven
knob resolution feeding directly into this in-process builder, instead of
`spec.py`'s current argv round-trip) is exactly the "Phase 2" territory
`docs/Design-Catalog-Contract.md` already flags as future work — not part of
this plan. The optional `catalog:`/`environment:` provenance pointers above
are the only place the two paths touch, and only for copying files, never for
resolution.

## Testing

Unit tests for `experiment_loader`/`experiment_builder` against a stub
cluster object (no live Kubernetes cluster needed) — assert the resulting
`TpchExperiment.configurations` list has the right `SutConfiguration`
attributes set, and that the provenance files land in the stub result
folder. Mirrors how `report_writer.py` was tested with fake objects (see
memory: "Docs fixes + agent summary plan").

## Implementation order

1. `tpch.py`: extract `build_parser()`. Verify `python tpch.py run ...`
   behaves identically (no behavior change expected).
2. `bexhoma/experiments/tpch.py`: add `DBMS_DEFAULTS`.
3. `bexhoma/experiment_loader.py`: `load_experiment_yaml()` +
   `validate_experiment_yaml()`.
4. `bexhoma/experiment_builder.py`: `build_experiment()`, including the
   provenance-copy helper.
5. `experiment.py`: the entry script.
6. `dev/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml`: worked example.
7. Unit tests (stub cluster) for loader + builder, including provenance
   copying.
8. Manual smoke test against a real (or kind/minikube) cluster:
   `bexhoma experiment dev/yaml_experiments/tpch-postgres-vs-pgduckdb.yaml`.
