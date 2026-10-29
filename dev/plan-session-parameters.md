# Plan: session parameters (sweeps without reload)

Status: **plan only** (2026-10-29), split out of
[plan-ddl-parameters.md](plan-ddl-parameters.md). Depends on its M1 (config
file per script folder, safe filling).

## Goal

Sweep settings that change how queries and transactions run, but not the
stored data, on **one loaded SUT**: one value per benchmark round instead of
one SUT and one load per value.

## What exists

- `--set` changes a deployment parameter (server flag, environment
  variable) for the whole experiment: one value, no sweep, applied at SUT
  start, so a new value needs a new SUT.
- Reset scripts (`-ar`) already run before each round
  ([plan-reset-scripts.md](plan-reset-scripts.md)): a natural place to apply
  a per-round setting.

## Candidates

**Planner and executor** (session or `ALTER SYSTEM` + reload, no restart)

| DBMS | Settings |
|---|---|
| PostgreSQL, Citus, PgDuckDB | `jit`, `max_parallel_workers_per_gather`, `work_mem`, `random_page_cost` (should follow the storage class: nvme vs cephcsi, see [plan-storage-class-sweep.md](plan-storage-class-sweep.md)), `effective_io_concurrency`, `plan_cache_mode` |
| Citus | `citus.max_adaptive_executor_pool_size`, `citus.enable_repartition_joins` |
| ClickHouse | `max_threads`, `join_algorithm` |
| MySQL, MariaDB | `optimizer_switch` flags, `join_buffer_size`, `innodb_adaptive_hash_index` (global, dynamic) |

**Transactions**

- Isolation level for OLTP: read committed vs serializable (PostgreSQL,
  CockroachDB, YugabyteDB); changes abort rates and throughput.

**Client side** (benchmark tool configuration, not the DBMS)

- Prepared statements, batch size, connection pooling (PGBouncer exists as a
  configuration).

## Proposal

- Second file per script folder: `experiments/<bench>/<dbms>/session-parameters.config`,
  same format as `ddl-parameters.config` (default, allowed values,
  description per key; default = current behaviour).
- Values filled into a per-round session script (system-wide settings via
  `ALTER SYSTEM` + reload or `SET GLOBAL`), run after the reset script.
- A sweep creates rounds instead of configurations; the value goes into the
  round's eval parameters, so summaries can group by it.
- Settings that need a restart (e.g. `shared_buffers`, PG 18 `io_method`)
  stay with `--set`.

## Open questions

- Per-session settings (isolation level, `SET` in a query file) only reach
  the benchmark's own connections: through DBMS-Benchmarker's connection
  init for TPC-H/TPC-DS/SSB, through the tool config for YCSB/BenchBase/
  HammerDB. Which tools allow that?
- Does a system-wide change between rounds leave state behind (plan cache,
  buffer content) that biases the next round? Reset order to define.
