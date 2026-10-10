# Catalog Contract

[`contracts/contract_catalog.yml`](../contracts/contract_catalog.yml) says what
an `experiment.yml` may contain: which workloads and systems exist, their
parameters, knobs and profiles, and the experiment schema. It is the catalog
itself, not a schema for one; where the code says `catalog.yaml`, it means a
copy of this file. Its rationale is in `contracts/contract_catalog_comments.md`.

## In scope

| Workload | Systems | Varies | Produces |
|---|---|---|---|
| `tpch` | PostgreSQL, PgDuckDB | system, concurrency (`rounds`), cpu, memory | per-query latency; Power@Size, Throughput@Size, Geo Times; SQL errors and warnings |
| `ycsb` | PostgreSQL | concurrency (`rounds`); no resource sweep, no `post_load` | throughput and latencies per operation type; time series |

Other workloads and systems run through their own entry scripts, not through
this contract.

## An experiment

```yaml
title: PgDuckDB vs PostgreSQL under concurrency
hypothesis: PgDuckDB has a lower Geo Times than PostgreSQL at every concurrency level
discriminates: [system, concurrency]   # exactly the factors that vary
workload:
  name: tpch
  params: {scaling_factor: 10, active_queries: [1, 13, 18]}
  rounds: [1, 4, 8]                    # concurrent streams per phase
  repetitions: 3
loading: {pods: 8, timeout_minutes: 60} # top level, not under workload
systems:
  - {name: PostgreSQL, profile: analytical-ssd}
  - {name: PgDuckDB, profile: analytical-ssd}
resources:
  cpu: {request: 16, limit: 16}
  memory: {request: 64Gi, limit: 64Gi}
placement: {sut: <node>}
```

[`dev/catalog/experiment.yml`](../dev/catalog/experiment.yml) is the
maintained, runnable example, annotated field by field.

## Rules worth knowing

- `title`, `hypothesis`, `discriminates` are required. `follow_up_of` names the
  experiment code a run continues.
- `loading` is a top-level block. Nested under `workload` it silently resolves
  to nothing.
- `resources.cpu` and `resources.memory` are a single `{request, limit}` or a
  list to sweep. Lists are paired by position, not crossed, and must have the
  same length.
- Each system and resource cell is benchmarked on its own, one SUT at a time
  (`max_sut_experiment: 1`), so systems never share a node.
- A profile derives knobs from the experiment's limits, e.g. `shared_buffers =
  0.3125 × memory_limit` for `analytical-ssd`.
- Memory knob values: an integer with one of the system's units (`40GB`), a
  Kubernetes quantity (`40Gi`), or a bare integer in the knob's base unit.
- TPC-H repetitions: 1 is a smoke test; a comparison needs at least 3.
- Every TPC-H benchmarker pod is limited to 16 cores and 16Gi, independent of
  `resources`, which size only the SUT.
- `duckdb_force_execution: true` makes DuckDB execute every query; `false`
  lets pg_duckdb decide per query, which is not the same as "PostgreSQL only".
- `observe.metrics` lists the hardware metrics the hypothesis relies on;
  required exactly when SUT or cluster monitoring is on.

## Known gaps

- Only `tpch` and `ycsb` translate to a run; `hammerdb`, `benchbase` and
  `tpcds` fail resolution.
- `follow_up_of` is recorded, not verified; nothing checks the named run
  exists or is comparable.
- `extends` merges knobs and profiles only; every other key, including
  `physical_design`, must be repeated.

## The contract

```{literalinclude} ../contracts/contract_catalog.yml
:language: yaml
```
