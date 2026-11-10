# Plan: no loading step fails silently (#848)

Status: **implemented 2026-11-10 (W1-W7), not committed, not run on a cluster; images must be rebuilt.** Decisions (user): O1 `backoffLimit: 0`; O2 ClickHouse exit
code only; O3 P4 is included (section 3, W7); O4 fail on `Skipped > 0` only; O5 no `ON_ERROR_STOP`
(default kept); O6 order W1+W5 (+W7), then W2/W3, then W4.

Issue #848 "Do not miss a loading error": scripts detect errors; loader pods are detected when they fail.

Goal: every loader pod (generator + loader container), every schema/index script, every durability and
restore-durability script and every reset script either succeeds or leaves a failed test in the summary.
Nothing may be checked by reading the benchmark data: no `SELECT COUNT(*)`, no `ANALYZE`, no scan of a
user table, nothing that writes. Allowed sources are only what the step itself reports:

- the reply of the load statement (`COPY n`, `Records: n Deleted: 0 Skipped: 0 Warnings: 0`, `n affected rows`),
- exit codes of clients, scripts, containers and pods, the Kubernetes job status,
- reading a server setting (`SHOW`, `@@GLOBAL.x`, `current_setting()`), which changes no data and no cache.

## 1. Related plans

| Plan | What it covers | State |
|---|---|---|
| memory `project_ingestion_verification_plan` (2026-11-05) | loader contract `BEXHOMA_INGEST:<unit>:<expected>:<reported>:<ok\|failed>`, `exit 1` per loader, bexhoma test | planned, not started; becomes W2, W3, W5 here |
| [plan-load-failure-and-sizing](plan-load-failure-and-sizing.md) P3 | loaders fail loudly | open; same as W2 |
| [plan-load-failure-and-sizing](plan-load-failure-and-sizing.md) P4 | script failures, load status, labels, crash on `upload_file` | **partly done since then**: `script_failed()`, `errors_<phase>` labels on pod and PVC, tests `Init scripts without errors` and `Reset scripts ran without errors`. Still open: do not label `data=True` after a failure, stop later phases, PVC removal, `upload_file` crash. These stay in P4 (decision O3) |
| [plan-reset-scripts](plan-reset-scripts.md) | reset contract | done; W4 adds the missing failure exits |
| memory `project_dbms_generic_plan` | no DBMS names in Python | planned; W1/W5 touch `loading.py` and `experiments/base.py`, coordinate the order |

This plan replaces the loader part of the first two and keeps the rest of P4 where it is.

## 2. Current state (checked 2026-11-10)

### Already detected

- Scripts run in the SUT pod (schema, index, tenants, durability, restoredurability, checks): `load_data_asynch`
  saves stdout/stderr, `script_failed()` (`bexhoma/configurations/loading.py:28-44`) matches
  `command terminated with exit code N`, `ERROR|FATAL|PANIC` at the start of a line or after `: `, and Redis
  `ERR…` on stdout. The summary shows `Init scripts without errors` (`experiments/base.py:1883-1975`), and a
  reused PVC brings `errors_<phase>`.
- Reset scripts (SUT and workers): `last_reset_failed` / `workers_failed`, test `Reset scripts ran without errors`.
- A loading job in Kubernetes' terminal `Failed` condition aborts the experiment with a failed runtime test
  (`_loading_abort_reason`, `experiments/base.py:2103`).
- TPC-H generator checks the `dbgen` exit code and the file count (`images/tpch/generator/generator.sh:218`).
- SSB loaders (all DBMS), TPC-H/TPC-DS ClickHouse loaders: `FAILED_TABLES` and `exit 1`.

### Gaps (failures that pass)

| # | Where | What goes wrong |
|---|---|---|
| G1 | 20 loading job templates have `backoffLimit: 1` or `4` (`k8s/jobtemplate-loading-*.yml`) | A loader pod that fails is restarted. If the retry succeeds, the job is `Complete` and `get_job_status()` (`clusters.py:2458`) returns True. Nobody looks at `status.failed`. The first pod may have loaded part of the data, so the retry loads it twice or hits key errors. With `BEXHOMA_SYNCH_LOAD` the retry may wait at the barrier forever. |
| G2 | `check()` (`loading.py:680`) stores the logs of `Failed` loader pods | No test reads them, so a `Failed` pod is not reported. |
| G3 | TPC-H/TPC-DS loaders PostgreSQL, MySQL (+ `loader-parallel.sh`), MariaDB, MonetDB | They compare the reply with `wc -l`, then set `FAILED=0` anyway (pg `images/tpch/loader_postgresql/loader.sh:269`) or end the retry loop with `FAILED=2`. They always `exit 0`. |
| G4 | MySQL/MariaDB `LOAD DATA LOCAL` | With `LOCAL`, duplicate keys and conversion errors become *warnings*, so rows are skipped without an error. Only `Skipped:`/`Warnings:` in the reply show it, and the loader does not check them. |
| G5 | `tpch_refresh` loaders (pg, mysql, mariadb, monetdb) | `exit 0` unconditionally, the INSERT/DELETE replies are not checked. They run as benchmarking jobs, so a failed refresh would be reported, but it never fails. |
| G6 | YCSB generator | `ycsb load` exits 0 even with `[INSERT], Return=ERROR, n`. |
| G7 | Benchbase generator | Exit code of `entrypoint.sh` is not checked. "Unknown benchmark" ends with `exit 0` (`images/benchbase/generator.sh:173`). |
| G8 | HammerDB generator | `exit 0` unconditionally. "SCHEMA COMPLETE" and the warehouse count are not checked. |
| G9 | `tpcds/loader_mysql/loader-parallel.sh` | Loads into `tpch.$basename` (copy-paste bug). |
| G10 | SUT `.sh` scripts with more than one command | `sh script` returns the exit code of the *last* command only. An earlier failure without an `ERROR` line is lost (e.g. `clickhouse-client` prints `Code: 60. DB::Exception`). |
| G11 | Client error formats outside the regex | MonetDB `mclient` (`SELECT: no such table`), ClickHouse (`Code: N. DB::Exception`), `cqlsh` (`InvalidRequest: Error from server`), `psql: error:` (lower case). These are caught only if the client exits non-zero, which is not verified for `mclient` reading stdin and for `cqlsh -f`. |
| G12 | `save-snapshot.sh` (Redis, Valkey, Garnet, Dragonfly) | When the background-save timeout is reached the script `break`s and exits 0 (`experiments/ycsb/Redis/save-snapshot.sh`). |
| G13 | durability / restoredurability scripts | Restoring is not checked. If `SET GLOBAL` silently does not apply (wrong scope, read-only variable, a later script overrides it), the benchmark runs with load settings. The scripts print the value, but nobody compares it. |
| G14 | Generators TPC-DS, SSB | Probably handled like TPC-H (`exit 1` present), but not checked against file count/size. |

## 3. Work packages

### W1. Kubernetes: a failed loader pod is always visible (G1, G2)

1. Set `backoffLimit: 0` in every `k8s/jobtemplate-loading-*.yml`. A loader is not idempotent, so a retry
   cannot repair a half load. Same mechanism for every template, no exceptions (decision O1).
2. `LoadingCoordinator.check()`: for every pod with phase `Failed` (logs are stored there already), record
   `loader_pods_failed` on the configuration: `<pod>: <container> exit <code> (<reason>)`, from the container
   status (`terminated.exitCode`, `reason` such as `Error` or `OOMKilled`). Read job `status.failed` as well,
   in case the pod is already gone.
3. Persisted like `volume_check`: in `connections.config` per connection, and as PVC label `errors_data=<n>`
   (the same pattern as `errors_<phase>`), so a reused volume brings it along.

### W2. Loader contract in every loader image (G3, G4, G5, G9)

Same contract as in the ingestion plan:

- one line per unit (table, file chunk): `BEXHOMA_INGEST:<unit>:<expected>:<reported>:<ok|failed>`;
  `expected` = lines of the file, `reported` = number from the reply of the load statement; empty if unknown;
- retries only for known transient errors (MySQL `ROLLBACK`, connection errors 2002/2013 with backoff, MonetDB
  "failed to start worker thread"); everything else, including a mismatch, is a failed unit;
- at the end `Failed tables: …` and `exit 1` if any unit failed (the SSB pattern).

Per DBMS, the number read from the reply:

| DBMS | Reply | Extra condition |
|---|---|---|
| PostgreSQL (also Citus, YugabyteDB, PgDuckDB through the pg loader) | `COPY n` | - |
| MySQL, MariaDB | `Records: n  Deleted: 0  Skipped: s  Warnings: w` (client in verbose mode, check the flag) | `Skipped = 0`; `Warnings = 0` (decision O4) |
| MonetDB | `n affected rows` | - |
| ClickHouse | none | exit code only, `reported` empty (decision O2) |

Images: `tpch` and `tpcds` loaders pg/mysql/mysql-parallel/mariadb/monetdb (remove the `FAILED=0`
overrides); `ssb` and the ClickHouse loaders only print the marker; `tpch_refresh` loaders compare the INSERT/DELETE reply
with the rows in the refresh file; fix `tpch.$basename` in `tpcds/loader_mysql/loader-parallel.sh`.

Risk: `wc -l` counts lines, not rows (rows with an embedded newline, a missing trailing newline). Check this
per DBMS × benchmark in the first cluster run. If the counts do not match for a valid reason, adjust the
expected count instead of dropping the check.

### W3. Generators of OLTP loaders (G6, G7, G8, G14)

- YCSB: parse the load status block. Fail with `exit 1` if `[INSERT], Return=ERROR` > 0 or
  `[INSERT], Operations` ≠ the record share of this pod. Marker unit = `usertable`.
- Benchbase: `rc=$?` after `entrypoint.sh`; `exit 1` if `rc ≠ 0` or on `Exception`/`ERROR` lines in the
  load log; "Unknown benchmark" → `exit 1`. Marker with empty counts (Benchbase prints none).
- HammerDB: require `SCHEMA COMPLETE` and `ALL VIRTUAL USERS COMPLETE`, and that the number of
  "Loading n Warehouses" = SF; otherwise `exit 1`. Marker unit = warehouses.
- TPC-DS, SSB generators: check the exit code and that the file count matches, as `tpch/generator.sh:204-219` does.

### W4. Scripts in the SUT pod and on workers (G10-G13)

1. **`sh -e` everywhere.** The three runners (`load_data_asynch`, `exec_reset_script`,
   `run_scripts_on_workers`) run `.sh` scripts with `sh -e`, so the first command that fails ends the script
   with its exit code and kubectl reports it. Audit the 90 scripts in `experiments/**/*.sh` for commands that
   may fail on purpose: `grep -q` in `while`/`if` conditions is exempt from `-e`, other cases get `|| true`
   with a comment.
2. **Client error formats.** On the cluster, run once per client a statement that fails without touching
   data (`SELECT * FROM bexhoma_no_such_table;`) through `loadData`, and note the exit code and the message.
   Clients: psql, mysql, mariadb, mclient, clickhouse-client, cockroach, cqlsh, redis-cli, valkey-cli. Wherever
   the exit code is 0, add the message to `_SCRIPT_ERROR_STDERR`/`_STDOUT`, or add the client's
   error-stop flag to `loadData` in `cluster.config` (e.g. `psql -v ON_ERROR_STOP=1`; changes behaviour,
   so for that one see decision O5). Unit tests with the captured messages.
3. **Timeouts are failures.** `save-snapshot.sh` (Redis, Valkey, Garnet, Dragonfly): `exit 1` when the
   timeout is reached, as `reset-flush.sh` already does for MySQL/MariaDB.
4. **Restored durability is checked.** Every `restoredurability-<level>.*` ends with a read of the setting
   and fails if it is not the saved value: MySQL/MariaDB `.sh` compares `@@GLOBAL.x` with
   `bexhoma.saved_settings` and `exit 1`; PostgreSQL `.sql` uses a `DO` block with `RAISE EXCEPTION` when
   `current_setting('…')` differs (it reads only and prints `ERROR`, which `script_failed` already catches).
   `durability-<level>.*` checks the value it set in the same way. Reading a setting changes nothing.
5. Index scripts need nothing beyond 1 and 2: `CREATE INDEX`/`ALTER TABLE` errors already produce `ERROR`
   lines or a non-zero exit.

### W5. bexhoma: test, summary, report (G2 + markers)

1. Parse `BEXHOMA_INGEST` lines from the stored loader pod logs (`bexhoma-loading-*.log`, at the same place
   as `_get_tenant_loading_from_logs`, `evaluators/base.py`). Store per connection: units ok/failed, and the
   failed pods from W1.
2. New test in `_show_loading_provenance` (`experiments/base.py:1848`):
   `Loader pods without errors`, which
   - fails if a pod is `Failed`, a unit is `failed`, or a loader pod log has no end marker (killed);
   - is skipped for reused storage without `errors_data`, and for results from before the markers existed;
   - passes otherwise.
   Summary section "Ingestion" (units, expected/reported per configuration, only on failure in full).
3. Refresh stream: the benchmarking-job path (`experiments/base.py:2535`) records failed pods as runtime
   tests already; W2 only adds the failing exit.
4. `report_writer.py`: row for the new test in the failed-test table (`~l.230-241`), with the logs to look at.
5. Contract: add the test name to the result contract (`contracts/`), bump the minor version.

### W7. Load status (P4 of plan-load-failure-and-sizing, included per O3)

Found while checking: `start_sut` reuses **any** existing PVC as a finished load
(`lifecycle.py get_labels_from_loaded_pvc`), also one labelled `loaded=False` from an aborted or
half-finished load. This is a silent failure too.

1. A volume is labelled `loaded=True` only after a clean load: no failed scripts (`errors_<phase>` > 0),
   no SUT restart during loading, no other recorded failure. Otherwise it gets `loaded=False loading_failed=True`.
   The SUT pod still gets `loaded=True` (the phase is over; benchmarking runs and the tests report it).
2. Reuse: a PVC with `loaded=False` or `loading_failed=True`, found before the experiment's first
   repetition, is refused with "remove it (-rsr)", the same way as a storage-class mismatch. A later
   repetition that finds the volume this experiment loaded goes on (its failure is already in the tests).
   A PVC without a `loaded` label (from before the label existed) is reused as before. No PVC is deleted
   automatically.
3. SUT restart between the start of loading and its end → `loading_failed` (restart counts of the SUT pod
   at loading start vs. end).
4. `upload_file` error in the index phase → load failed, the experiment is aborted with diagnostics
   (as for a failed loading job), so `-ks` and the result upload work as usual. The schema phase already catches it.
5. A loading job that fails (with `backoffLimit: 0`, every failed pod) already aborts the experiment.
6. Test `Loading completed without failures` from the persisted `loading_failed` reasons per connection.

### W6. Docs and tests

- Unit tests: marker parser, test outcome (pass/fail/skip), `sh -e` command build, extended
  `script_failed`, `check()` with a fake `Failed` pod and with `status.failed > 0`.
- `docs/`: loader contract (marker, exit codes, what counts as failed), the new test, `backoffLimit: 0`.

## 3b. Implementation notes (2026-11-10)

Done, unit-tested (`tests/test_loading_checks.py`, full suite green), **not yet run on a cluster, images not rebuilt**:

| WP | What | Where |
|---|---|---|
| W1 | `backoffLimit: 0` in all 21 loading job templates | `k8s/jobtemplate-loading-*.yml` |
| W5 | Parser from the result folder: pod describes (`Status: Failed`, container exit code), job describes (`Pods Statuses: ... / n Failed`), `BEXHOMA_INGEST` lines; test `Loader pods without errors`, summary sections Ingestion / Loader Pods with Errors | `bexhoma/loading_checks.py`, `experiments/base.py _show_loader_pod_checks` |
| W7 | `loading_failed` reasons per repetition (SUT restart during loading, index scripts not uploaded → fatal, aborts); PVC `loaded=True` only after a clean load, else `loaded=False loading_failed=True`; inherited volume not relabelled; reuse of `loaded=False`/`loading_failed=True` refused before repetition 1 (`SutConfiguration.check_volume_loaded`); test `Loading completed without failures` | `configurations/loading.py`, `base.py`, `lifecycle.py`, `metrics.py`, `experiments/base.py` |
| W2 | TPC-H/TPC-DS loaders pg, mysql, mariadb, monetdb: one attempt (retry ≤ 10 only on ROLLBACK / MonetDB thread/login errors), reply compared with `wc -l` (pg `COPY n`, MySQL/MariaDB `SELECT ROW_COUNT()` after `LOAD DATA` = O4, MonetDB `n affected rows`), marker per file, `exit 1`. SSB + ClickHouse loaders: markers only. tpch_refresh pg/mysql/mariadb/monetdb: RF1 counts, RF2 exit code (psql `ON_ERROR_STOP=1` inside the image), markers, `exit 1` | `images/{tpch,tpcds,ssb,tpch_refresh}/loader_*/loader.sh` |
| W3 | YCSB: `[INSERT]` OK count = `insertcount` of the workload file, no non-OK return, no `INSERT-FAILED`; "start time has already passed" now `exit 1`. Benchbase: exit code, "Finished loading data into", no `[ERROR` line; unknown benchmark `exit 1`. HammerDB: SCHEMA COMPLETE, ALL VIRTUAL USERS COMPLETE, no FINISHED FAILED, warehouses = SF. TPC-DS generator: `dsdgen` exit code + `.dat` files | `images/{ycsb,benchbase,hammerdb,tpcds}/generator*` |
| W4 | `sh -e` in the three script runners; `script_failed` also matches `<client>: error:`, `DB::Exception`, `Error from server`; PostgreSQL/Citus `durability-*.sql` (77 files) end with a `DO` block that raises if a value did not take effect | `configurations/loading.py`, `experiments/**/durability-*.sql` |
| W6 | Docs: Concepts (loader contract, volume label), DBMS.md "Failed loads", AgentResultContract known gap; result contract 1.14.0 with the two tests; report validity rows | `docs/`, `contracts/contract_result.yml`, `report_writer.py` |

Follow-up (user, 2026-11-10): `-xld relaxed` together with `--set synchronous_commit=on` must load relaxed
and benchmark with synchronous commits. `--set` puts `-c` on the postgres command line, which `ALTER SYSTEM`
cannot change, so the old scripts silently loaded with `on`. Now:
- PostgreSQL/Citus `durability-durable|relaxed.sql` keep `ALTER SYSTEM` (reaches open sessions) and also set
  `synchronous_commit` per database (`ALTER DATABASE <current_database()> SET`, which wins over the command line
  for new sessions; Citus also `run_command_on_workers`). The restore scripts reset both. Checks read only
  `pg_db_role_setting` (coordinator and every worker), the restore check fails if a database setting is left.
- `fsync`/`full_page_writes` are server-wide only: scripts declare them (`-- server-wide: fsync=off ...`,
  49 files); `SutConfiguration.load_durability_conflicts()` compares with the configuration's `--set`
  operations at loading start; a conflict ends the load before anything is loaded
  (`LoadingCoordinator.fail_loading_fatally`) and the experiment aborts with the reason. The script upload
  failure of the schema phase now takes the same path (before: message only, unloaded SUT benchmarked).
- Checked locally with `postgres:18 -c synchronous_commit=on` (Docker): old relaxed script → new sessions `on`
  (the silent case); new scripts → loader sessions `off`, after restore `on`; durable and relaxed+unsafe
  sequences end at the configured values; `-c fsync=on` + unsafe script → `ERROR: load durability: fsync is on, not off`.
- Open: Citus (does Citus propagate `ALTER DATABASE ... SET`, and do coordinator→worker connections pick up the
  worker database setting); PGBouncer: server connections pooled before the durability script keep the old
  value (only with `--set synchronous_commit`).

Findings while implementing:
- The old pg loader check `*"copy $lines"*` never matched (psql prints `COPY n`); the MySQL one `*"$lines affected row"*` neither (no output without `-v`).
- `loader-parallel.sh` (TPC-H/TPC-DS MySQL) is not copied into the images; only the `tpch.` → `tpcds.` bug was fixed.
- G12 is already caught: after the timeout `SAVE` answers `ERR ...` on stdout, which `script_failed` matches. Scripts unchanged.
- Check over 177 stored result folders with loader pods: the new parser flags only the two ClickHouse runs that really failed (1794009695, 1794010308); no SUT script log is newly flagged by the extended patterns.

Not done / open:
- G11 on the cluster: exit code of `mclient` (stdin) and `cqlsh -f` on an error; add a pattern if 0.
- MySQL/MariaDB restoredurability: no check that `@@GLOBAL` equals the saved value (plain MySQL SQL cannot raise an error outside a stored program; needs a `.sh` wrapper). Citus durability check covers the coordinator only.
- Benchbase has no row counts (marker with empty counts).

## 4. Verification on the cluster (script: dev/test-loading-failures.ps1; images rebuilt 2026-11-10)

1. One clean run per DBMS × benchmark that W2/W3 touches (pg, mysql, mariadb, monetdb, clickhouse × tpch/tpcds/ssb;
   tpch `-xrs`; ycsb; hammerdb; benchbase): no failed unit, `expected = reported`.
2. Deliberately broken runs that leave real data alone:
   - loader pointed at a wrong schema / database (DatabaseService without `schema`) → unit failed, pod `Failed`, test failed;
   - kill the SUT container during ingest (`kubectl exec … kill 1`) → loader pod `Failed`, no retry, test failed;
   - a schema script with `SELECT * FROM bexhoma_no_such_table;` in the middle of a `.sh` → `Init scripts without errors` failed;
   - restoredurability with a wrong expected value → script failed.
3. A reused volume of the broken run → refused with "remove it (-rsr)".
4. `-xld relaxed --set ...synchronous_commit=on` (PostgreSQL and Citus): loader sessions `off`
   (`pg_stat_activity` / loader log of `SHOW`), benchmark sessions `on`, `Init scripts without errors` passed.
5. `-xld unsafe --set ...fsync=on` (PostgreSQL): refused before loading, experiment aborted with the reason.

## 5. Open decisions (user)

| # | Question | Proposal |
|---|---|---|
| O1 | `backoffLimit: 0` for all loading jobs, or keep retries and only report failed pods | 0: a retry on a half load is not a repair |
| O2 | ClickHouse row count: exit code only, or read `written_rows` from `system.query_log` (read-only, system table, not user data) | exit code only first; query_log later if needed |
| O3 | Only detect and report here, or also stop later phases / not label `data=True` (P4 of plan-load-failure-and-sizing) | report here; P4 behaviour separately |
| O4 | MySQL/MariaDB: fail on any `Warnings > 0` or only on `Skipped > 0` | `Skipped > 0` fails; warnings are logged and counted, fail after the first clean run shows they are 0 |
| O5 | psql `ON_ERROR_STOP=1` in `loadData` (script stops at the first error instead of going on) | no: detection is already there; keep the behaviour |
| O6 | Order | W1 + W5 first (pure bexhoma, visible right away), then W2/W3 (images), then W4 |
