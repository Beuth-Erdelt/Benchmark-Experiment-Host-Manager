# Plan: reset scripts (`-ar`) for every DBMS and benchmark, comparable between systems

Status: **done (2026-10-21).** M0-M11 implemented, committed and checked on the cluster
(`scripts/test-docs-reset.sh`); fixes from the M11 run in 979506a3 and 1c3be9b9 (MonetDB persist n/a),
the HammerDB MySQL load race it exposed in d48712b6. Details in section 6. Optional: watch the
MySQL/MariaDB flush time at larger SF (600 s timeout); YugabyteDB persist needs `yb-admin`.

Goal: with `-ar`, every benchmark runs a reset before each benchmarking round for every DBMS in scope,
and the reset does the same steps everywhere, so results are comparable between systems and
workloads. Where a step has no equivalent in a DBMS, the script says so instead of leaving it out silently.

Scope:
- DBMS: PostgreSQL, PGBouncer, PgDuckDB, Citus, MySQL, MariaDB, MonetDB, YugabyteDB, CockroachDB,
  TiDB, Dragonfly (standalone, cluster, replica), Redis (standalone, cluster).
  **DatabaseService is out of scope.** CedarDB added 2026-10-31 (#830): statistics only.
- Benchmarks: YCSB, Benchbase (tpcc, twitter, ycsb, chbenchmark), HammerDB TPC-C, TPC-H, TPC-DS.

Related: [plan-oltp-storage-dbms](plan-oltp-storage-dbms.md) (WP4: scripts on workers),
[plan-storage-class-sweep](plan-storage-class-sweep.md). Issue #667 (Dragonfly `SAVE` on all workers)
is done separately, before this plan.

---

## 1. Decisions (user, 2026-10-19)

| # | Decision |
|---|---|
| D1 | DatabaseService is ignored here (no reset scripts). Citus is in scope (revised 2026-10-19), CedarDB too (revised 2026-10-31). |
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
| MonetDB | `ANALYZE sys.<table>` | n/a (no `sys.flush_log()` in Dec2025, see section 6) | n/a |
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

---

## 6. Implementation notes (2026-10-19)

M0 answered from code and templates (no cluster run):

| M0 | Answer |
|---|---|
| 2 | All PostgreSQL-family images are 18 (`postgres:18.6`, `pgduckdb:18-v1.1.1`, `citus:14.2.0`): targets `bgwriter`, `checkpointer`, `io`, `wal`. |
| 5 | The YugabyteDB helper pod is `postgres:15.0`: no `yb-admin`, so persist is n/a (R3). `script_target('workers')` does not work (`run_scripts_on_workers` uses container `dbms`, the Helm tserver container is `yb-tserver`). Counters instead: `reset-counters.sh` in the helper pod connects to every tserver pod directly. Checked on the cluster 2026-10-19 (YugabyteDB 2025.2.7, from a `postgres:15.0` pod): `yb-tserver-N.yb-tservers` (short names) resolve and accept `psql -U yugabyte`; `pg_stat_reset()` changes `stats_reset` only on the tserver it runs on; `yb-tserver-service` spread 6 connections over 2 of 3 tservers, so the old single reset hit a random tserver. |
| 8 | TPC-H/TPC-DS use the experiment-dict path (`experiment_dict_template` in `experiments/tpch.py`, `tpcds.py`), so `set_benchmark_resetscript` reaches the round loop. With `-xrs` the template has a second entry `tpch_refresh`; the reset targets `name='tpch'` only, otherwise it would run twice per round. |
| 9 | Benchbase twitter/ycsb/chbenchmark folders exist for PostgreSQL only: resets for PostgreSQL and PGBouncer (R4). |

Open on the cluster: M0.1 (Citus worker checkpoint duration, `success` rows), M0.3 (MySQL/MariaDB flush
duration; timeout set to 600 s = R1 maximum, `reset-flush.sh` has `TIMEOUT=600`), M0.4 (MonetDB
`sys.flush_log()`), M0.6 (TiDB `FLUSH STATUS`), M0.7 (Dragonfly `CONFIG RESETSTAT`). All of them are in
the scripts; a statement that is not supported only writes an error to the stderr log, the round still starts.

Deviations from the plan:
- Citus: `run_command_on_workers(...)` plus the same statement locally on the coordinator, not
  `run_command_on_all_nodes`, which reaches the coordinator only if it is registered in `pg_dist_node`.
- MySQL/MariaDB `.sql`: table names qualified with the database (`ycsb.usertable`, `tpch.*`, `tpcds.*`) or
  `USE <db>` (Benchbase `benchbase`, HammerDB `tpcc`). The old YCSB scripts ran `ANALYZE TABLE usertable`
  against the default database of `loadData`. Same for TiDB (`ycsb.usertable`, `benchbase.*`).
- MariaDB `reset-flush.sh` connects as root (`MARIADB_ROOT_PASSWORD` of the container), because `SET GLOBAL`
  needs it; `loadData` uses user `bexhoma`.
- `reset-flush.sh` exits early (code 1) if it cannot read `innodb_max_dirty_pages_pct`, so a broken connection
  does not wait for the full timeout.
- `experiments/tpcc/CockroachDB/reset-tpcc.sql` (not offered by `hammerdb.py`) follows the contract too;
  `experiments/tpcc/SingleStore` is unchanged.
- M1.2 also warns when a listed script is missing in the folder (`ExperimentBase.warn_missing_reset_scripts`).
- Docs anchor: `docs/DBMS.md#reset-scripts--ar`.

M11 run 2026-10-20 (`scripts/test-docs-reset.sh`, YCSB, Benchbase, HammerDB, TPC-H; TPC-DS pending):
every configuration ran its reset before both rounds, no warnings.
- Confirmed: MySQL/MariaDB flush reaches 0 dirty pages and restores the setting (YCSB SF 1: MySQL
  140-165 s, MariaDB up to 291 s, below the 600 s timeout; watch larger SF); Citus 18/18 worker
  commands `success = t`; YugabyteDB counters on 3 tservers; Dragonfly `CONFIG RESETSTAT` OK (M0.7);
  TiDB `FLUSH STATUS` OK (M0.6); TPC-H `-xrs`: one reset per round.
- Fixed after the run: Benchbase TiDB loads into `test`, not `benchbase` (table names unqualified again);
  MonetDB reset never ran, because the reset path did not escape the newline in `loadData`
  (`exec_reset_script` now does, as the loading path); the test script's Benchbase PGBouncer run lacked
  pooler flags (throughput 0).
- M0.4 answered 2026-10-21 (reruns 1792538505 TPC-H, 1792538525 TPC-DS): the reset now runs before both
  rounds, but MonetDB Dec2025-SP3 has no `sys.flush_log()` ("no such operator"). `sys.functions` has
  only `suspend/resume_log_flushing` (pause the background WAL flusher), `logging.flush` (trace log),
  `vacuum`, `hot_snapshot`: none forces the WAL into the BATs, so persist is n/a for MonetDB.
- HammerDB MySQL did not load (`tpcc` missing, NOPM 0), unrelated to the reset: race between loader
  and SUT schema init, fixed in d48712b6 (loading waits for `schema=True`), cluster checks OK.
- 2026-10-21: test script aligned: MonetDB comments say persist n/a; YCSB PGBouncer with pooler flags
  (`-xnpp 1 -xnpi 128 -xnpo 64`); Citus HammerDB/TPC-H with `-nwr 1 -nws 48` as YCSB/Benchbase.

Tests: `tests/test_reset_scripts.py` (completeness matrix per CLI incl. all Benchbase benchmarks, `-xrs`,
step order, no braces, Citus workers, identical flush scripts, missing-file skip, warning, info line).
