# Plan: reset scripts (`-ar`) for every DBMS and benchmark, comparable between systems

Status: **plan only (2026-10-19), nothing implemented.**

Goal: with `-ar`, every benchmark runs a reset before each benchmarking round for every DBMS in scope,
and the reset does the same steps everywhere, so results are comparable between systems and
workloads. Where a step has no equivalent in a DBMS, the script says so instead of leaving it out silently.

Scope:
- DBMS: PostgreSQL, PGBouncer, PgDuckDB, Citus, MySQL, MariaDB, MonetDB, YugabyteDB, CockroachDB,
  TiDB, Dragonfly (standalone, cluster, replica), Redis (standalone, cluster).
  **CedarDB and DatabaseService are out of scope.**
- Benchmarks: YCSB, Benchbase (tpcc, twitter, ycsb, chbenchmark), HammerDB TPC-C, TPC-H, TPC-DS.

Related: [plan-oltp-storage-dbms](plan-oltp-storage-dbms.md) (WP4: scripts on workers),
[plan-storage-class-sweep](plan-storage-class-sweep.md). Issue #667 (Dragonfly `SAVE` on all workers)
is done separately, before this plan.

---

## 1. Decisions (user, 2026-10-19)

| # | Decision |
|---|---|
| D1 | CedarDB and DatabaseService are ignored here (no reset scripts for them). Citus is in scope (revised 2026-10-19). |
| D2 | Scripts stay in the folder structure `experiments/<benchmark>/<DBMS>/` (Benchbase: `experiments/benchbase/<benchmark>/<DBMS>/`). Duplicates between benchmarks are accepted. PGBouncer and PgDuckDB keep using the PostgreSQL folder (`path_experiment_docker`). |
| D3 | `-ar` stays opt-in. |
| D4 | One contract for all reset scripts (section 2). |

---

## 2. Reset contract

Order of the steps (the same for every DBMS):

1. **Maintenance and statistics** - `VACUUM` / `ANALYZE` (or equivalent).
2. **Persist** - write dirty data to disk (`CHECKPOINT`, flush, `SAVE`), so no checkpoint or flush left
   over from loading or the previous round falls into the measured round. Must come after step 1,
   because `VACUUM` dirties pages again.
3. **Reset counters** - zero the cumulative activity counters, so application metrics start at 0.

Rules:
- A step without an equivalent is a comment line `-- step 2 (persist): n/a - <reason>` in the script,
  and listed in the docs table (M10). No substitute operation that does something else (e.g. compaction
  instead of a flush).
- The reset does **not** make caches cold: `CHECKPOINT` writes dirty buffers but keeps them. The comments
  saying "cold-cache starting state" (`benchbase.py:280`, `ycsb.py:238`) are wrong and get fixed (M1).
- Each step runs where the data is (all nodes for distributed systems), or the script documents that it
  covers only one node.
- Scripts may be `.sql` (run through `loadData`, fanned out per tenant for schema/database tenancy) and
  `.sh` (run once in the SUT pod, or on every worker with `script_target('workers')`). Instance-wide steps
  that need a wait loop (MySQL/MariaDB flush) go into a `.sh` file next to the `.sql` file.

---

## 3. Current state and target per DBMS

Today (✅ set, ⚠️ partial, ❌ missing although the CLI offers the DBMS, - not offered):

| DBMS | YCSB | Benchbase tpcc | Benchbase twitter/ycsb/chbenchmark | HammerDB | TPC-H | TPC-DS |
|---|---|---|---|---|---|---|
| PostgreSQL | ⚠️ order | ⚠️ order | ❌ (tpcc only) | ⚠️ order | ❌ | ❌ |
| PGBouncer | ❌ | ❌ | ❌ | - | - | - |
| PgDuckDB | - | - | - | - | ❌ | - |
| Citus | ⚠️ coordinator only | ⚠️ | ❌ | ⚠️ | ❌ | - |
| MySQL | ⚠️ no persist | ⚠️ | ❌ | ⚠️ | ❌ | ❌ |
| MariaDB | ⚠️ no persist | ⚠️ | ❌ | ⚠️ | ❌ | ❌ |
| MonetDB | - | - | - | - | ❌ | ❌ |
| YugabyteDB | ⚠️ ANALYZE only | ⚠️ | ❌ | - | - | - |
| CockroachDB | ⚠️ ANALYZE only | ⚠️ | ❌ | - | - | - |
| TiDB | ⚠️ ANALYZE only | ⚠️ | ❌ | - | - | - |
| Dragonfly | ✅ (#667) | - | - | - | - | - |
| Redis | ❌ | - | - | - | - | - |

Target content per DBMS:

| DBMS | 1 Statistics | 2 Persist | 3 Counters |
|---|---|---|---|
| PostgreSQL, PGBouncer, PgDuckDB | `VACUUM VERBOSE ANALYZE` (whole database, no table list) | `CHECKPOINT` | `pg_stat_reset()`, `pg_stat_reset_shared(...)` for the PostgreSQL 18 targets (`bgwriter`, `checkpointer`, `io`, `wal`; M0) |
| Citus | `VACUUM VERBOSE ANALYZE` on the distributed tables (Citus passes it on to the shards) | `SELECT * FROM run_command_on_all_nodes('CHECKPOINT')` (coordinator + workers) | `pg_stat_reset()` and `pg_stat_reset_shared(...)` through `run_command_on_all_nodes` |
| MySQL, MariaDB | `ANALYZE TABLE <tables>` (`.sql`, per benchmark) | `reset-flush.sh`: set `innodb_max_dirty_pages_pct=0`, wait until `Innodb_buffer_pool_pages_dirty = 0` (with timeout), restore the old value | `FLUSH STATUS` (in `reset-flush.sh`, after the flush) |
| MonetDB | `ANALYZE sys.<table>` | `CALL sys.flush_log()` | n/a |
| YugabyteDB | `ANALYZE VERBOSE <tables>` (cluster-wide) | `yb-admin flush_table ysql.<db> <table>` if `yb-admin` is reachable (M0), else n/a | `pg_stat_reset()` - reaches only the tserver behind the service; on all tservers if `script_target('workers')` works for the Helm StatefulSet (M0) |
| CockroachDB | `ANALYZE <tables>` (cluster-wide) | n/a (Pebble flushes on its own; no SQL command) | `SELECT crdb_internal.reset_sql_stats();` (cluster-wide) |
| TiDB | `ANALYZE TABLE <tables>` (cluster-wide) | n/a (no user-invokable flush in SQL) | `FLUSH STATUS` if supported (M0), else n/a |
| Dragonfly | n/a | `SAVE` on every data pod (done, #667) | `CONFIG RESETSTAT` if supported (M0) |
| Redis | n/a | `SAVE` (standalone: SUT pod; cluster: every worker, `script_target` is already `'workers'`) | `CONFIG RESETSTAT` |

---

## 4. Milestones

### M0. Checks on the cluster (no code)

1. Citus 14.2: `run_command_on_all_nodes('CHECKPOINT')` and the stats resets work as `postgres`; the
   result rows (`success`) show a failing node; duration of the worker checkpoints after loading.
2. PostgreSQL 18: valid targets of `pg_stat_reset_shared`; also in the PgDuckDB and Citus images.
3. MySQL 9.7 / MariaDB 12.3: duration of the dirty-page flush after loading (YCSB SF=1, TPC-C SF=16), so
   the timeout in `reset-flush.sh` can be set; can the restored value be read with
   `SELECT @@innodb_max_dirty_pages_pct` before setting it?
4. MonetDB Dec2025: `ANALYZE` syntax, `sys.flush_log()`.
5. YugabyteDB: is `yb-admin` in the helper pod (SUT), with the master addresses? Does
   `get_worker_pods(only_stateful=True)` return the tserver pods (then counters can be reset on all of them)?
6. TiDB 8.5: `FLUSH STATUS`.
7. Dragonfly 2.0.2: `CONFIG RESETSTAT`.
8. TPC-H/TPC-DS (dbmsbenchmarker path): does `set_benchmark_resetscript` reach the round loop
   (`experiments/base.py:2084` or `:2122`), or does the TPC-H experiment build its rounds elsewhere?
9. Benchbase twitter/ycsb/chbenchmark: which DBMS are actually run with them (today only
   `experiments/benchbase/{twitter,ycsb,chbenchmark}/PostgreSQL` exists)? Scripts are made only for those pairs.

### M1. Code: visible behaviour

1. `exec_reset_script` (`configurations/loading.py:982`): skip a script file that does not exist in the
   experiment folder, with a message (as `run_scripts_on_workers` does), instead of running `loadData`
   against a missing file.
2. `-ar` on a configuration without a reset script: one warning per configuration at experiment start.
3. Workload info "A reset script ... runs before each benchmarking round" also for TPC-H and TPC-DS
   (as `benchmarks/ycsb.py:117`).
4. Fix the "cold-cache" comments (section 2).
5. Tests: missing file skipped, warning, info line.

### M2. PostgreSQL family (PostgreSQL, PGBouncer, PgDuckDB)

1. Change the order to statistics -> `CHECKPOINT` -> counters in `ycsb`, `benchbase/tpcc`, `tpcc`.
2. New: `benchbase/{twitter,ycsb,chbenchmark}/PostgreSQL/reset-benchbase.sql`,
   `tpch/PostgreSQL/reset-tpch.sql`, `tpcds/PostgreSQL/reset-tpcds.sql` (same content, whole database).
3. `set_benchmark_resetscript` for PGBouncer (YCSB, Benchbase), PgDuckDB (TPC-H), and for every Benchbase
   benchmark (drop the `if type_of_benchmark == 'tpcc'` for PostgreSQL).

### M3. Citus

1. Existing scripts (`ycsb`, `benchbase/tpcc`, `tpcc`): order statistics -> persist -> counters; the local
   `CHECKPOINT` and the stats resets become `run_command_on_all_nodes(...)`; header comments ("only the
   coordinator") and the comments in `ycsb.py:845`, `benchbase.py:885` updated.
2. New: `tpch/Citus/reset-tpch.sql`, Benchbase benchmarks from M0.9; reset set in `tpch.py`.
3. The scripts stay SQL and run once on the coordinator (no `script_target` change).

### M4. MySQL and MariaDB

1. `.sql`: `ANALYZE TABLE` per benchmark (YCSB, Benchbase all four, HammerDB, TPC-H, TPC-DS); remove
   `FLUSH STATUS` from the `.sql` files.
2. `reset-flush.sh` in every folder that has a MySQL/MariaDB reset: flush with timeout (M0.3), then
   `FLUSH STATUS`. On timeout: message in the log and exit code != 0, the round still starts.
3. Reset lists become `['reset-<benchmark>.sql', 'reset-flush.sh']`.

### M5. MonetDB

`tpch/MonetDB/reset-tpch.sql`, `tpcds/MonetDB/reset-tpcds.sql`; reset set in `tpch.py`, `tpcds.py`.

### M6. YugabyteDB, CockroachDB, TiDB

Extend the existing `ycsb` and `benchbase/tpcc` scripts with steps 2 and 3 per section 3 (or n/a lines);
new scripts for the Benchbase benchmarks from M0.9. YugabyteDB counters on all tservers if M0.5 allows
(`.sh` on workers), else documented as one tserver only.

### M7. Dragonfly and Redis

1. Dragonfly: `CONFIG RESETSTAT` in `save-snapshot.sh` after `SAVE`, if M0.7 is positive.
2. Redis: `experiments/ycsb/Redis/save-snapshot.sh` (`SAVE`, `CONFIG RESETSTAT`); reset set for standalone and
   cluster in `ycsb.py` (cluster already has `script_target('workers')`).

### M8. TPC-H and TPC-DS wiring

Reset set for every DBMS of `tpch.py` and `tpcds.py` (per M0.8). The reset runs before each client round,
so with `-xrs` it also precedes the refresh stream of that round. The one-time post-load steps
(`initstatistics-*`, `CHECKPOINT` in `checkschema-*`) stay.

### M9. Completeness test

A unit test with the matrix of section 3 (benchmark CLI x DBMS in scope): for each pair, the CLI sets a
reset list and every file of it exists in the right folder. New pairs in a CLI then fail the test until
they get a reset.

### M10. Docs

1. `docs/DBMS.md`: section "Reset scripts (`-ar`)" with the contract and the table of section 3
   (incl. the n/a steps).
2. Example pages (YCSB, Benchbase, HammerDB, TPC-H, TPC-DS, per DBMS): one sentence on `-ar` where it is used.
3. Note for comparisons: runs before and after M2/M3/M4 are not directly comparable (PostgreSQL order,
   Citus worker checkpoints, MySQL/MariaDB flush move I/O out of round 1).

### M11. Cluster check

One run per DBMS family with `-ar -nc 2` and two client rounds: reset logs per round present, no
stderr errors except documented NOTICEs, `reset_seconds` reported, step 2 visible (PostgreSQL
`checkpoints_req` +1, for Citus on every worker; MySQL dirty pages 0 before the round; Redis/Dragonfly snapshot files).

---

## 5. Open points (defaults unless the user decides otherwise)

| # | Point | Default |
|---|---|---|
| R1 | MySQL/MariaDB flush timeout | from M0.3, about 2x the measured time, at most 10 min |
| R2 | Flush timeout reached | log + exit code != 0, round starts anyway (no abort) |
| R3 | YugabyteDB persist without `yb-admin` in the helper pod | n/a, no extra pod |
| R4 | Benchbase twitter/ycsb/chbenchmark for DBMS other than PostgreSQL | only the pairs found in M0.9 |
| R5 | TPC-H/TPC-DS reset also before the first round after loading | yes (same as OLTP: before every round) |
