# Plan: per-query monitoring selection in the agent contract (`observe.metrics`)

Status: **partly implemented** (2026-10-09). Done in `bexhoma/environment.py`
(environment contract 1.2.0): node occupancy from Prometheus (section "Node
occupancy from Prometheus") and the `monitoring:` section with the hardware
metrics (`title`, `kind`, `active`, `required`, `available`, `source_sha256`).
Also done (catalog contract 1.10.0): `observe.metrics` for hardware metrics,
validated in `spec.validate_experiment()`/`validate_environment()`, passed as
`-mm key=on,...`, checked against `cluster.config` by the experiment and
applied in `configurations/metrics.py`. Revised the same day: it is a list of
the metrics the hypothesis relies on (switched on, required whenever hardware
monitoring is on), not the override map proposed under "Contract shape"
below; see `contracts/contract_catalog_comments.md`.
Not done: the refresh on agent start, the staleness check (`source_sha256`
is written but not compared), and application metrics in the catalog
(waits for the catalog split). Builds on `observe:` being re-enabled in catalog
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

### environment.yml: where it lives, and staleness

- In-cluster agent (`agent/lifecycle_controller.py:326-334`): `cluster.config`
  is copied from the input directory to the agent root, then
  `python -m bexhoma.environment` regenerates
  `<state_root>/investigations/<lifecycle_id>/environment.yml` at the start of
  every investigation. The hardware list would be read from that same
  `cluster.config`, so it is current at investigation start.
- Local runs (`agent.harness.agent`, `agent.lifecycle`): default
  `environment.yml` in the working directory, written by hand with
  `bexhoma environment create`. It goes stale when `cluster.config` changes.
  (`validate_experiment.py` defaults to `dev/catalog/environment.yml`.)
- Every submitted experiment stages a copy (`submitted-environment.yml`) and
  archives it into the result folder; `environment_sha256` is in the
  trajectory. All experiments and follow-ups of one investigation share
  that one snapshot.
- Plain bexhoma runs (`tpch.py`, `ycsb.py`, `experiment.py` without the agent)
  never read environment.yml; they read `cluster.config` directly.

Staleness guard:
- Write `monitoring.source_sha256` (hash of `cluster.config['monitor']`) into
  environment.yml. Validation compares it against the `cluster.config` it
  can see and rejects with "environment.yml is stale, regenerate" on
  mismatch.
- Applying overrides in `configurations/metrics.py`: an override key that is
  not in the loaded `cluster.config` fails the run before anything is
  deployed (never silently ignored).
- `connections.config` already records the effective `active` flags, so the
  result shows what was actually collected.
- Add a cheap mode (e.g. `bexhoma environment create --monitoring-only`) that
  refreshes only the `monitoring:` section from `cluster.config` without
  probing the cluster.
- The same drift risk applies to application metrics in the catalog; the
  catalog-vs-`cluster.config` key test covers that.

### Refresh environment.yml on every local agent start

Same behaviour as the in-cluster start, so a `cluster.config` change cannot
go unnoticed locally either.

- Default on; `--no-refresh-environment` for offline/replay runs. Free
  resources go stale within days anyway, not only the monitoring list.
- Not a full rebuild: the hardware baseline (`nodes[].hardware_baseline`,
  `network_matrix`, `hardware_baseline_failed_nodes`) comes from the opt-in,
  cluster-mutating `-xhw` sweep (minutes, pods on every node). The local
  `environment.yml` contains such results. The refresh regenerates nodes,
  free resources, storage classes, limits and `monitoring:`, and carries
  the baseline over from the previous file with its original timestamp.
  `--refresh-environment=full` reruns the sweep.
- Write a fresh copy per investigation next to its trajectories; read the
  user's `environment.yml` only as the baseline source, never overwrite it.
- Move `_refresh_environment` (`agent/lifecycle_controller.py:285`) into
  `bexhoma/environment.py` as a shared function with a `keep_baseline_from`
  option; call it from both the in-cluster and the local start. The
  in-cluster start currently drops the baseline too (it never passes `-xhw`).
- With refresh on every start, the `source_sha256` staleness check matters
  less for agent runs, but stays for `validate_experiment.py` and
  `--no-refresh-environment`.

### Node occupancy from Prometheus

Today `collect_node_usage()` (`bexhoma/environment.py:379`) lists every pod
cluster-wide through the Kubernetes API and sums container requests. On a
shared cluster that listing is usually forbidden (403), and every node's
`free:` stays empty. Prometheus already holds the same facts via
kube-state-metrics, readable without cluster-wide pod RBAC.

Queries (Python port of the PowerShell prototype), all `sum by (node)`:

- allocatable: `kube_node_status_allocatable{resource="cpu"|"memory"}`
- requests: `kube_pod_container_resource_requests{resource=...}`
  `and on(namespace,pod) (kube_pod_status_phase{phase=~"Pending|Running"} == 1)`
- limits: the same with `kube_pod_container_resource_limits`

Per node in `nodes[]`:

- `free`: allocatable - requests (as today, same units/format)
- new `requested` and `limits_pct` (limits / allocatable, i.e. overcommit:
  a node at 250% limits can be squeezed even when requests leave room)
- `occupancy_source: prometheus | kubernetes_api | unavailable` and
  `collected_at`

Implementation:

- Prometheus URL from `cluster.config['monitor']['service_monitoring']`
  (already ends in `/api/v1/`, e.g. `https://prometheus.datexis.com/api/v1/`),
  formatted like `configurations/metrics.py:167-171` does. If it is a
  cluster-internal service name, reach it via port-forward or skip.
- Order: Prometheus first; fall back to the Kubernetes API listing; else
  leave `free` empty with a warning (current degrade-and-continue behaviour).
- Treat an empty `kube_node_status_allocatable` result as "no
  kube-state-metrics" and fall back, rather than reporting zero.
- Deduplicate before summing (`max by (namespace,pod,container,resource,node)`)
  so HA Prometheus pairs or two kube-state-metrics replicas do not double
  the requests.
- Keep only nodes in the curated `nodes[]` (tainted nodes stay excluded);
  convert bytes/cores through the existing `_format_quantity`.
- Requests include Pending pods (already scheduled, about to start) as in
  the prototype; init containers are ignored, as today.
- Optional: actual load per node (node-exporter CPU busy %, memory used)
  as `current_load`, since low requests do not mean a quiet node. Separate
  decision; it is noisier and changes between scrape and run.
- Pure helpers for the arithmetic (as `_compute_free_resources`), so tests
  run against canned Prometheus JSON without a cluster.

Environment contract: the `monitoring:` section and the new occupancy keys
go into one bump, 1.0.0 -> 1.1.0.

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
