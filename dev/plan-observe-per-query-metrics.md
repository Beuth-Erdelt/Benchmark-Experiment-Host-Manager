# Plan: per-query monitoring selection in the agent contract (`observe.metrics`)

Status: **not implemented, held as a plan** (2026-10-09). No code or contract
changes have been made yet. Builds on `observe:` being re-enabled in catalog
contract 1.9.1.

## Goal

`cluster.config` already lets single monitoring queries be switched on and off
(`active:` per query). Expose that in the agent contract so the agent can
decide per query which metrics a run collects.

## What already exists

- `cluster.config` defines every query with an `active` flag:
  - `monitor.metrics`: 18 hardware queries (5 off by default: GPU, "others").
  - application templates per DBMS exporter (`monitor.postgresql`,
    `monitor.mysql`, ...); `postgresql` has 54 queries, 9 off. PostgreSQL and
    PgDuckDB both map to it (`dockertemplate.monitor.sut.metrics: postgresql`).
- `bexhoma/configurations/metrics.py:198-231` copies those definitions into
  `connectiondata['monitoring']['metrics']` (and `metrics_{statefulset}`);
  that copy is what lands in `connections.config`.
- dbmsbenchmarker `monitor.py:264` returns an empty frame for `active: False`,
  so the query is never sent to Prometheus.
- Evaluation already honours the flag: `collectors/base.py:409`,
  `report_writer.py:496`, `experiments/base.py:2602`.

=> Switching a metric off only means changing `active` in the connection copy
before `connections.config` is written. Fetch, evaluation and report follow.

## Where the vocabulary lives

The two kinds of metrics depend on different things, so they live in
different contracts:

| kind | depends on | lives in |
|---|---|---|
| hardware (`monitor.metrics`) | the cluster's Prometheus/cAdvisor/node-exporter/DCGM | `environment.yml` (generated) |
| application (`monitor.postgresql`, ...) | the system's exporter (postgres_exporter) | catalog, under `systems.<name>` |

Application metrics are a **capability of the system**, the same axis as
`physical_design:` (capability, not selection). So they go to
`systems.PostgreSQL.monitoring:` in `contract_catalog.yml`, and the selection
goes to `observe.metrics` in `experiment.yml`.

- PgDuckDB: `extends:` already falls back to the base's value for any
  top-level key a system does not declare, so PgDuckDB inherits PostgreSQL's
  `monitoring:` without duplication. Only declare it on PgDuckDB if its set
  ever diverges (e.g. DuckDB-engine metrics).
- Size: ~54 entries with key + title (+ kind) is roughly 5-6k characters, on
  a catalog at 47.4k with a 56k whole-file limit. Options: list key + title
  only (drop the PromQL, which the agent never needs); or curate to the ~15
  queries worth choosing between; or do this together with the catalog split
  (one file per system makes this a non-issue).
- Single source of truth: `cluster.config` stays authoritative for the
  queries. The catalog list is keys/titles only; a test asserts every catalog
  key exists in `cluster.config`'s template (and vice versa, or a declared
  out-of-scope list), so they cannot drift.

## Contract shape (proposed)

```yaml
observe:
  monitoring_sut: true
  monitoring_app: true
  metrics:                  # override of the default active flag, per query
    total_gpu_util: true
    pg_locks_count: false
```

- Override map, not an exact list: keeps defaults, can enable default-off
  queries, mirrors the `active:` flag one for one.
- Required (cannot be set `false`): `total_cpu_util_s`, `total_cpu_util`,
  `total_cpu_memory`, `total_cpu_memory_cached` -- read directly by
  `experiments/base.py:2898-2924`; `total_cpu_util_s` also drives the result
  contract's `monitoring_component_cpu_nonzero` check.
- Scope: experiment-wide (like `active_queries`). Per-system
  (`systems[].observe_metrics`) only if needed later.

## Steps

**Environment contract (hardware vocabulary)**
- `bexhoma/environment.py`: `collect_monitoring_metrics(cluster)` reads
  `cluster.config['monitor']['metrics']` -> `monitoring.hardware:` with key,
  title, kind (gauge/counter/ratio), default active, required.
- Bump `environment_contract_version` 1.0.0 -> 1.1.0; doc; `tests/test_environment.py`.

**Catalog contract (application vocabulary + selection)**
- `systems.PostgreSQL.monitoring: {exporter: postgresql, metrics: {key: {title, kind, default}}}`.
- `experiment_schema.fields.observe.fields.metrics` (`type: "map[str,bool]"`,
  semantics, `when:`, required keys).
- `catalog_concepts`: one entry stating capability (systems/environment) vs.
  selection (observe.metrics), like `physical_design`.
- Version 1.9.1 -> 1.10.0 (minor: new field); rationale in
  `contract_catalog_comments.md`; mirror in `docs/AgentCatalogContract.md`.

**Validation (`agent/harness/validation.py`, `bexhoma/spec.py`)**
- `_check_fields` cannot check map keys against two vocabularies, so a
  dedicated check rejects: unknown key; application key not offered by any
  listed system; `false` on a required key; `metrics:` without
  `monitoring_sut`/`monitoring_cluster`; application keys without
  `monitoring_app`.
- Same check in `spec.validate_experiment()` (the non-agent route).

**Mapping to the run**
- `bexhoma/cli_args.py`: new flag, e.g. `-mmo/--monitoring-metric-override
  key=on,key=off`; add to `scripts/_reorder_flags.py`.
- `tpch_catalog.py` / `ycsb_catalog.py` `build_argv()`: emit it from
  `observe.metrics`.
- `experiments/base.py` (~line 492): store `self.monitoring_metric_overrides`.
- `configurations/metrics.py:198-231`: after each `metricdata.copy()` apply
  the override to `active` (hardware, statefulset and application branches).
- Optionally `tpch_builder.py` for the YAML route.

**Result side**
- Inactive queries simply have no `query_{component}_metric_{key}.csv`;
  `contract_result.yml` should say that is expected, and that
  `connections.config` records which metrics were active.
- The application summary takes the first 5 active metrics
  (`experiments/base.py:2600`); the agent's choice changes which 5. Either
  document it or give explicitly enabled keys priority.

**Tests**
- Validation: unknown key, required key off, app key without
  `monitoring_app`, app key for a system without that exporter, valid override.
- `build_argv` emits the flag; metrics.py override flips `active` in
  connection data; catalog keys match `cluster.config` templates.

## Check in `cluster.config` first

- `tikv_store_size_bytes` is defined twice (`cluster.config:230`, `:238`);
  the GiB variant is silently lost.
- Network and filesystem queries are `active: True`, but the catalog's own
  notes say the collector is configured to skip disk and network. If they
  always come back empty, leave them out of the vocabulary or default them off.
