# Plan: session parameters (sweeps without reload)

Status: **PARKED** (2026-10-29), split out of
[plan-ddl-parameters.md](plan-ddl-parameters.md). Depends on its M1 (config
file per script folder, safe fill function).

## Recommended method today (no code change)

One experiment per value, all on the same loaded PVC:

```
experiment 1:  -rst <class> --set …jit=off   → loads the PVC, runs
experiment 2:  -rst <class> --set …jit=on    → finds the loaded PVC, skips loading, runs
```

- Cleaner than rounds: every value gets a freshly started SUT (same cold
  start, no carry-over from an earlier round), and the setting is applied
  at startup as in production.
- Same configuration name, storage settings and SF in all experiments, so
  the PVC is found; run them one after another (one SUT per PVC).
- **Only for read-only workloads** (TPC-H without `-xrs`, TPC-DS, SSB).
  YCSB, TPC-C and refresh streams change the data, so the next experiment
  would start from modified data: reload instead.
- Comparison across the summaries by hand until studies exist
  ([plan-studies.md](plan-studies.md)).

The per-round sweep below only saves SUT restarts and gives one summary, at
the cost of round-order bias and ~60 lines of Python. Unpark only if
restarts prove too slow or many values per setting are needed.

## Goal

Sweep settings that change how queries and transactions run, but not the
stored data, on **one loaded SUT**: one value per benchmark round instead of
one SUT and one load per value.

## What exists (checked 2026-10-29)

- **`--set`** changes a deployment parameter (server flag, environment
  variable) for the whole experiment: one value, applied at SUT start.
  Settings that need a restart stay there.
- **Rounds** are entries of `experiment_dict['benchmarker']` (a list of
  rounds, each a list of parallel benchmark entries with `parallelism`,
  `parameters`, `resetscript`), built by the drivers through
  `add_benchmark_list` / `add_benchmarking_parameters`
  ([configurations/base.py:309-385](../bexhoma/configurations/base.py#L309-L385)).
  Drivers without experiment-dict rounds use the legacy `benchmark_list`
  path.
- **Per-round hook**: `_submit_round` runs `exec_reset_script` on the SUT
  before each entry is submitted, only with `-ar`
  ([experiments/base.py:2140-2184](../bexhoma/experiments/base.py#L2140-L2184)).
  `exec_reset_script` uploads the scripts through `prepare_init_dbms`
  before each round (corrected 2026-10-29), now filled with the DDL
  parameters; per-round values would need their own dict there. Scripts
  named for workers are already run on all workers (`split_worker_scripts`,
  e.g. Citus).
- **`init_SQL`** in the docker template is run by DBMS-Benchmarker on every
  connection it opens (e.g. MariaDB `optimizer_switch`, cluster.config):
  per-session, but only for TPC-H, TPC-DS and SSB.
- **Connection info**: `run_pod` copies `eval_parameters` into each
  connection ([benchmarking.py:147-158](../bexhoma/configurations/benchmarking.py#L147-L158)),
  and the summary prints them per connection. Note:
  `c['parameter']['connection_parameter']` is the configuration's dict **by
  reference**, so per-round values must be copied, not mutated in place.

## Proposal

Generic, no driver code, same pattern as the DDL sweep.

- **Scope: system-wide SQL, not per session.** A round applies its values
  with statements that affect all new connections (`ALTER SYSTEM` + reload,
  `SET GLOBAL`, `ALTER ROLE ALL SET`, `SET CLUSTER SETTING`). That reaches
  every benchmark tool (DBMS-Benchmarker, YCSB, BenchBase, HammerDB) without
  touching tool configs; benchmarker pods connect after the script ran.
  `init_SQL` stays as is (per-session, DBMS-Benchmarker only).
- **Files per script folder**:
  - `session-parameters.config`: keys with default, allowed values,
    description (same format as `ddl-parameters.config`).
  - `session.sql` (or `session.sh` / worker variant where needed): the
    statements with `{key}` placeholders. It sets **every** declared key in
    every round (defaults for unswept keys), so no value leaks from one
    round into the next or into the next repetition (`-nc`).
- **CLI**: `-xsp KEY=V1[,V2…]` (same parser as `-xddl`); several keys →
  Cartesian product.
- **Expansion in `process()`**: rounds × combinations, for configurations
  whose folder declares all swept keys; each round entry gets
  `session: {key: value}`. `-nbp 1,2` with `-xsp jit=on,off` gives 4
  rounds. Legacy `benchmark_list` path: not swept, warning.
- **Per round in `_submit_round`**: fill `session.sql` with the round's
  values (M1 fill function), upload as `session_<run>_<client>.sql`,
  execute (also on workers), **independent of `-ar`**, before the reset
  script; failure → round marked like a failed reset. Values go into the
  connection's own copy of `eval_parameters`, so the summary shows them per
  connection.
- **Validation** in `process()` before anything starts: unknown key or
  value → error.

### Python changes

| File | Change | Size |
|---|---|---|
| [bexhoma/configurations/loading.py](../bexhoma/configurations/loading.py) | `exec_session_script(values, script_type)`: fill (M1 function), upload, execute on SUT and workers (reuses `split_worker_scripts`, `run_scripts_on_workers`), return seconds and failures | ~25 lines |
| [bexhoma/cli_args.py](../bexhoma/cli_args.py) | `-xsp KEY=V1[,V2…]`, same parse function as `-xddl` | ~3 lines |
| [bexhoma/experiments/base.py](../bexhoma/experiments/base.py) | `process()`: validate, expand rounds × combinations (experiment-dict path), warn for legacy path; `_submit_round`: call `exec_session_script` before the reset, put the round's values into the connection's `eval_parameters` | ~35 lines |
| [bexhoma/configurations/benchmarking.py](../bexhoma/configurations/benchmarking.py) | copy `connection_parameter` per connection instead of passing the shared dict | 1 line |
| tests/test_session_parameters.py (new) | expansion (product, round count), every key set every round, validation, values per connection | new |

No change: drivers, DBMS-Benchmarker, evaluators, k8s templates.

## Candidates

"Reload" = takes effect for new connections without restart.

| DBMS | Settings | Statement | Notes |
|---|---|---|---|
| PostgreSQL, PgDuckDB | `jit`, `max_parallel_workers_per_gather`, `work_mem`, `random_page_cost`, `effective_io_concurrency`, `plan_cache_mode` | `ALTER SYSTEM SET …; SELECT pg_reload_conf();` | `random_page_cost` should follow the storage class (nvme vs cephcsi, [plan-storage-class-sweep.md](plan-storage-class-sweep.md)); `io_method`, `shared_buffers` need restart → `--set` |
| Citus | as PostgreSQL, plus `citus.max_adaptive_executor_pool_size`, `citus.enable_repartition_joins` | coordinator and workers (worker script) | `plan_cache_mode` on workers is the Citus #8824 workaround ([citus-worker-plan-cache-growth]) |
| MySQL, MariaDB | `optimizer_switch` flags, `join_buffer_size`, `innodb_adaptive_hash_index` | `SET GLOBAL …` | new connections only, fine since pods connect after |
| ClickHouse | `max_threads`, `join_algorithm`, `distributed_product_mode` (Cluster, see DDL plan `sharding_key`) | settings profile of the benchmark user | needs SQL access management or a config file + `SYSTEM RELOAD CONFIG`; **verify** on the template |
| CockroachDB | session vars (e.g. `default_transaction_isolation`), cluster settings | `ALTER ROLE ALL SET …`, `SET CLUSTER SETTING …` | read committed needs a cluster setting; **verify** for v24.2.4 |
| YugabyteDB | YSQL session vars | `ALTER DATABASE … SET …` | read committed needs a tserver flag (restart) → `--set` |

**Transactions**: isolation level (read committed vs serializable) for
PostgreSQL via `ALTER DATABASE … SET default_transaction_isolation`; changes
abort rates and throughput.

**Client side** (prepared statements, batch size, pooling): not settings of
the DBMS but of the benchmark tool; already per round where the tool takes
them as benchmarking parameters (environment of the job). Out of scope here.

## Milestones

- **S0** depends on DDL plan M1 (fill function, config loader, value parser).
- **S1** Python changes above + unit tests.
- **S2** PostgreSQL TPC-H: `jit` × `max_parallel_workers_per_gather`;
  cluster check: values per connection in the summary, each round's script
  in the result folder.
- **S3** Citus (worker script), MySQL/MariaDB, then ClickHouse after the
  settings-profile check.

## Open questions

- **Round order bias**: buffer and OS cache content carries over between
  rounds, as today between `-nbp` rounds. Use `-ar` (reset before each
  round), or interleave values (a, b, a, b) via `-nc`?
- Restore after the last round: with `-ks` the kept SUT keeps the last
  round's values. Run the script once more with defaults at the end, or
  just document it?
- Legacy `benchmark_list` drivers: which ones still use it, and is a
  warning enough?
