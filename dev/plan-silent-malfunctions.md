# Plan: no malfunction stays unnoticed

Status: **implemented on branch silent-malfunctions, cluster-tested 2026-11-24 (section 4c) with the
rebuilt images.** S1-S9 done (section 4), plus S10 (end marker of scripts) and S11 (aborted summary checks
the scripts) found by the cluster tests. P1 done as S12 (2026-11-25: exit code, `-tr` removed), P2 as S13
(UID at the end of a repetition), P5 as S14 (HammerDB run complete), P12 as S15 (`No summary` fails), P7 as S16 (pipes in scripts), P8 as S17 (missing DBMSBenchmarker child named), P10 as S18 (replaced SUT pod not loaded again), P14 as S19 (runtime failures stored); P9 deferred. Open: the other proposals of section 5 and the docs page (section 6).

Goal: every run either does what was planned or leaves a failed (or at least a skipped/warning) test in
the summary. A number in the summary that is wrong because something was missing must not pass silently.

Decisions (user, 2026-11-24):

- D1 Error counts of Benchbase (`error code`), HammerDB (`Error `) and YCSB (`DBException`) are expected.
  They are reported, never a failing test.
- D2 There are no reference answers for all scale factors. Result correctness is only compared between
  runs and DBMS (DBMS-Benchmarker result-set comparison); that is accepted.
- D3 Incomplete generated data is caught by the generator programs' exit code (a completion marker
  written only after exit 0), not by counting lines or rows.
- D4 RF2 deletes have no expected row count; loader timings of parallel loader jobs are still
  overwritten (memory `project_multiloader_timing_limitation`, deferred).

## 1. How the draft tests were done

The findings (sections 2, 3) came from draft tests without the cluster; the fixes were then tested on the
cluster (section 4c). Local Docker containers for the DBMS clients, offline replays of the real
summary code on copies of real result folders, and a search through `D:\data\benchmarks` (result
archive) and `logs_tests/` (584 run logs). Draft script (not in the repo):
`scratchpad/draft/draft_missing_pod.py` copies a Benchbase result folder, removes or cuts one pod's log
and runs `Benchbase.show_summary()` with the real test helpers of `ExperimentBase`.

## 2. Detected (no gap)

| What | How |
|---|---|
| Loader pod or generator fails | `exit 1` per loader, `BEXHOMA_INGEST` markers, loader pod and job descriptions (`loading_checks.py`) (#848) |
| SQL error in a loading, index or reset script | `script_failed()`: psql/ysqlsh `ERROR:`, mysql/mariadb exit 1, `DB::Exception`, cockroach `ERROR:`, Db2 wrapper (rc&12 → exit 1 + `ERROR:`), Oracle `WHENEVER SQLERROR EXIT FAILURE`, redis-cli `ERR`/`WRONGTYPE` on stdout, `sqlcmd -b` exit 1, cqlsh `Error from server` |
| Benchmarker job ends Failed | terminal job condition `Failed` → runtime test |
| SUT container restarts | `restartCount` of the SUT pods at the end of the run |
| CPU of a component 0 or NaN | per component, skipped when the phase is shorter than one scrape interval |
| Metrics missing | `missing_metrics.collect_missing_metrics` |
| Workflow differs from the plan | `Workflow as planned` (planned rows from `connections.config`) |
| Throughput / latency 0 or NaN | per benchmark `record_tests()` |

## 3. Not detected (findings)

Severity / evidence. "happened" = found in a real run, "offline" = reproduced by replay, "code" = read
from the code only.

| # | Finding | Severity | Evidence |
|---|---|---|---|
| F1 | A broken kubectl stream or connection during a loading, index or reset script counts as success. kubectl's exit code is ignored, its own messages (`error: unable to upgrade connection`, `Unable to connect to the server`, a cut stream) do not match `script_failed()` | high | happened: 1793360424 (MariaDB TPC-DS `initindexes`), `errors_index=0`, index state unknown |
| F2 | A benchmarker pod fails and Kubernetes retries it (`backoffLimit` 1 or 4). The retry finds the child queue empty, falls back to `BEXHOMA_CHILD=1` and runs as a duplicate child 1, alone and late; one child never runs | high | happened: 1790852331 (PgDuckDB, pod evicted for ephemeral storage, 9th pod "I assume this is the first child") |
| F3 | A Benchbase / YCSB / HammerDB / hardware pod without results (log missing, cut, or no result block) is left out; throughput is summed over the remaining pods and all tests pass | high | offline: 1795468620, 2425 → 1212 req/s, `Workflow as planned` passed (planned rows are rebuilt from `parallelism`, not from results) |
| F4 | A partial raw-data folder is reused: the generator prints "Raw folder exists, I do nothing" when at least one `*tbl*` file exists. A failed generator exit code of an earlier run is never seen again | high | code: `images/tpch/generator/generator.sh` |
| F5 | Monitoring active, but no metric came back at all: only `No monitoring metrics missing` passes, no CPU test is recorded | medium | offline replay |
| F6 | Only printed, never a test: pod log not fetched after 9 attempts (`store_pod_log`), pods without start/end times (`get_job_timing`), experiment ended by `--experiment-timeout`, monitoring set unhealthy | medium | code; none of the messages appear in 584 run logs |
| F7 | A SUT pod replaced during the run (evicted, rescheduled) is not seen: the restart test reads `restartCount` of the pods that exist at the end | medium | code; no evicted SUT pod in the archive, needs a cluster run |
| F8 | A run shorter than configured (fewer operations, shorter duration) passes | medium | code |
| F9 | sqlplus `SP2-` errors exit 0 and do not match; `sh -e` does not stop on a failing command inside a pipe or before `&&`; cqlsh `SyntaxException` and mclient errors (no `ERROR` prefix) only show in the exit code | low | local Docker tests (table below) |
| F10 | bexhoma's process exit code is always 0; `test_results()` returns None so "Test successful!" never prints; empty host info (`""` / `0`) is not flagged | low | code |

DBMS clients after a failing statement (local Docker, outputs run through `script_failed()`):

| Client | Goes on? | Exit code | Matched by text? |
|---|---|---|---|
| `mclient` (MonetDB Dec2025-SP3) | yes | 1 | no (`SELECT: no such table`) |
| `cqlsh -f` (Cassandra 5.0.9) | yes | 2 | `Error from server` yes, `SyntaxException` no |
| `sqlplus` with `WHENEVER SQLERROR EXIT` | yes after `SP2-` | 0 | no |
| `sqlcmd -b` (SQL Server 2022) | stops | 1 | no (`Msg 208, Level 16`) |
| `redis-cli` (8.x) | yes | 0 | yes (stdout) |
| `psql` | yes | 0 | yes |
| `mysql` / `mariadb` | stops | 1 | yes |
| `sh -e` with `false \| cat`, `false && true` | yes | 0 | – (`bash -e -o pipefail` exits 1) |

## 4. Fixes

| Step | Fix | Findings | State |
|---|---|---|---|
| S1 | Script outcome from kubectl's exit code. `clusters.exit_code_line()` appends `bexhoma: kubectl exit code N` to stderr when kubectl exits non-zero; `script_failed()` matches it. Loading, index and tenant scripts (`load_data_asynch`), reset scripts and worker scripts (`execute_command_in_pod(..., report_exit=True)`). The line is in the stored stderr log, so the summary's check of the logs sees it too | F1, F9 (mclient, cqlsh, sqlcmd) | done |
| S2 | New test `Results of all benchmarker pods`, per benchmark. Log-based benchmarks (`LogEvaluator.record_results_complete_test`): planned connections (one per pod) against the pods with a parsed result (`rows_with_results`: Benchbase needs the result JSON, YCSB `[OVERALL]`, hardware one result value); missing or the same child from two pods fails. DBMSBenchmarker: per-pod entries of `connections.config` per job against `parallelism`. `natural_sort_rows()` keeps two rows of one connection, the YCSB/Benchbase/HammerDB per-connection tables crashed on them | F2, F3 | done |
| S3 | Benchmarker scripts (benchbase, dbmsbenchmarker, hammerdb, hardware, ycsb) exit 1 with `FATAL: no child number in message queue` instead of running as child 1; bexhoma fills the queue before every job, also for one pod. New test `Benchmarker pods without errors` from the stored benchmarker pod and job descriptions (`loading_checks.check_benchmarker_pods`, same parser as the loader pods) | F2 | done, images rebuilt, cluster run A |
| S4 | TPC-H and TPC-DS generators: `.bexhoma_generated` written at the end, after dbgen/dsdgen, iconv and sed exited 0 (exit codes of iconv and sed are now checked); a raw folder is reused only with it, files without it are deleted (only files: the single-pod folder holds the split subfolders) and generated again. SSB already had `.complete` with staging folders. Consequence: raw folders on the shared volume from images before the marker are generated once more | F4 | done, images rebuilt, cluster runs (4c) |
| S5 | `Monitoring returned data` fails when monitoring was on, a phase ran and no component returned anything (per component no data can be right, e.g. no loading phase). Runtime failures (`_record_runtime_failure`): `--experiment-timeout`, a pod log without `BEXHOMA_START/END`, a pod log `store_pod_log` gave up on (`cluster.logs_not_stored`) | F5, F6 | done |
| S6 | `SUT pods not replaced`: UID of the SUT pod when loading started (`sut_pod_uid_loading` in `connections.config`) and of every SUT and worker pod when a round started (`hostsystem['pod_uid']`, read by `get_host_all()` anyway); more than one UID per pod and repetition fails. Hidden in the printed host lists | F7 | done |
| S7 | Benchbase: `Every pod ran for the configured time` (`Elapsed Time (nanoseconds)` ≥ 99 % of `BENCHBASE_TIME`). YCSB: `Execution Phase: every pod ran its configured operations` (sum of `[<OP>].Operations` incl. FAILED, RMW counted once, against `YCSB_OPERATIONS` of the pod) | F8 | done; HammerDB: section 5 |
| S8 | `SP2-nnnn` on stdout matches. **Not** `bash -o pipefail`: the pipes in `experiments/**/*.sh` (all six kinds: S16) include the MySQL/MariaDB `$(mysql ... \| cut)` (a failure ends in the flush timeout and `exit 1` anyway) and `while redis-cli ... \| grep -q`, which pipefail could end early through SIGPIPE. Instead the rule is in `experiments/README.md` ("How a failing script is noticed") | F9 | done |
| S9 | `test_results()` of experiments, mixed experiments and benchmarks return `0`/`1` (the "Test successful!" line could never print). `Host information complete` (warning when RAM, CPU, cores or node is empty); it found the MySQL CPU probe gap (4b) | F10 | done; exit code: S12 |

### 4b. Verification (offline, 2026-11-24)

- Unit tests: `tests/test_silent_malfunctions.py` (S1-S11, including the end marker and the aborted summary).
- Full test suite: passes except `test_system_descriptors::test_local_config_declares_the_same` (6 subtests),
  which fails on dev as well (the local `cluster.config` differs from `k8s-cluster.config`).
- `bexhoma summary` on copies of 78 recent result folders (Benchbase, YCSB, HammerDB, hardware, TPC-H, TPC-DS,
  SSB; scratchpad, `cluster.config` pointing there): no traceback, none of the new tests failed. `Results of all
  benchmarker pods` and `Benchmarker pods without errors` passed 78 times, `Every pod ran for the configured
  time` 17, `every pod ran its configured operations` 30, `Monitoring returned data` 33. `SUT pods not replaced`
  is not recorded for them (no UIDs in older results).
- `Host information complete` warned 4 times, always MySQL: CPU empty. Cause: the CPU probe used `more`, which
  `mysql:8.4` does not have (checked in the image). Fixed: `grep -m1 'model name' /proc/cpuinfo`.
- Broken copies: YCSB 1795444672 with one log deleted and one log duplicated (retry with the same child) fails
  `Results of all benchmarker pods - missing: postgresql-1-1-1-1-1 - same child twice: postgresql-1-1-2-1-7`
  while `Workflow as planned` still passes; before, the summary crashed on the duplicate. HammerDB 1795423770
  with the log cut before the result fails it as well.
- Benchmarker pod check on the real folders: 1790852331 `gdjd8 Failed: dbmsbenchmarker exit 137` (the evicted
  pod), 1794823963 and 1794004383 the failed refresh pods; clean runs pass.
- Generators in Docker (debian, stubs for dbgen/dsdgen and redis-cli): failed generation → next run generates
  again; marker → reused; legacy folder without marker → generated again, split subfolder kept.

### 4c. Cluster tests (2026-11-24, rebuilt images, logs in `logs_tests/local/silent_*.log`)

| Run | Code | What | Result |
|---|---|---|---|
| TPC-H, TPC-DS, YCSB, Benchbase, HammerDB, hardware fio (PostgreSQL, SF 1-4, 2 loader / 2 benchmarker pods) | 1795553594 ... | normal runs | all tests passed, no traceback; new tests passed; both TPC-H generator pods printed "no completion marker: generate again" for the old raw folder |
| A: YCSB, one of 2 benchmarker pods deleted while running | 1795556476 | S3 | the retry pod printed `FATAL: no child number in message queue` and exited 1, the job failed (backoffLimit 1). Failed: job Failed, `Start and end time in pod log ...ft729`, throughput NaN, `Results of all benchmarker pods - missing: ...-1, ...-2`, `Benchmarker pods without errors` |
| B: TPC-H SF 10, SUT pod deleted (graceful) during the index script | 1795557106 | S1, S6 | PostgreSQL's smart shutdown let the index script finish (7 of 7, exit 0, correct). The scripts after it got exit code 2 (`bexhoma: kubectl exit code 2`). bexhoma saw the new pod as "not loaded yet" and loaded again; a loader job failed, the experiment aborted with loader tests failed |
| C: TPC-H SF 1, `-ne 2` | | S2 with 2 DBMSBenchmarker pods | all passed |
| D: TPC-H SF 1, `-ne 2`, with S10 | | end marker | all 7 scripts printed `BEXHOMA_SCRIPT_END:ok`, all tests passed |
| B2: as B, with S10 | 1795558454 | | as B; the scripts after the deletion end with `BEXHOMA_SCRIPT_END:failed` |
| B3: as B, pod deleted with `--grace-period=0 --force` | 1795559036 | | index script cut after 4 of 7 (`FATAL: terminating connection`, `BEXHOMA_SCRIPT_END:failed`). The experiment aborted before its first result, and that short summary did not check the scripts: fixed (S11), replayed on the folder: `Init scripts without errors (failed: ... initindexes ...)` |

Added after the cluster tests:

| Step | Fix |
|---|---|
| S10 | Every script run in a pod is wrapped (`clusters.wrap_script`): `( cmd ) && echo BEXHOMA_SCRIPT_END:ok \|\| echo BEXHOMA_SCRIPT_END:failed`; `failed` matches, a missing marker (pod or stream gone before the end, whatever kubectl's exit code) adds `bexhoma: script ended without BEXHOMA_SCRIPT_END`. No `$?`, so the local shell (cmd.exe or sh) passes it unchanged; checked through kubectl on the cluster |
| S11 | `show_summary_aborted()` also records `Init scripts without errors` from the stored script logs |
| S12 (P1) | Exit code always on, `-tr` removed. `_print_test_summary()` counts printed and failed tests (never reset, so a mixed experiment adds up its benchmarks); `process()` ends with `tests_outcome()`: `Test successful!` or `Tests failed: N of M`, returns 1 on a failed test (skipped and warnings do not fail). Entry scripts, `experiment.py` and `bexhoma summary` exit with it. `-tr` did only a smoke test (results readable, `Test successful!` before the summary) and one workload sentence; removed with the `test_results()` methods of experiments, benchmarks and evaluators, from all scripts and docs, and as YCSB `verify_result` from the catalog (1.15.0). `-tr` is refused with a message: argparse would otherwise read it as `-t r`. Callers checked: test scripts ignore the exit code, the agent harness goes by `report/index.md`. Offline: clean folder exits 0, broken YCSB and HammerDB copies exit 1 |
| S13 (P2) | Third UID reading: the end-of-repetition restart snapshot (`bexhoma-sut-*-restarts.json`) stores each pod's `uid` (one `get_pod_uid()` per pod and repetition). `_test_sut_pods_not_replaced()` fails when a snapshot UID is none of the UIDs read at loading start or at a round start of that repetition (`... (after the last round started)`); with one round per repetition, this is the only reading after benchmarking. The restart counter cannot see a replacement: `restartCount` belongs to one pod object, a new pod starts at 0. Also reads the UIDs of additional SUT pods (`sut` list). Older snapshots without `uid`: nothing changes |
| S14 (P5) | HammerDB, evaluator only (no image change: `benchmarker.sh` already prints `End N seconds` / `Duration N seconds` around `hammerdbcli`, HammerDB prints `<n> VU TEST`, `Test complete, Taking end Transaction Count.`, `Vuser <n>:FINISHED FAILED`). Two tests from the logs of the pods with results: `No virtual user FINISHED FAILED` (a virtual user that ended with an error, e.g. could not connect, is a malfunction; transaction errors stay counted only, D1) and `Every pod ran for the configured time` (every started VU test completed, wall time of `hammerdbcli` >= 99 % of (rampup + duration) per VU test). Archive: 180 pods, ratio 1.02-1.36, no `FINISHED FAILED` in 198 logs, one log with transaction errors and `FINISHED SUCCESS`; 23 recent runs pass both tests. Logs without the lines (older images) are left out |
| S15 (P12) | `bexhoma summary` of a result folder whose workload `type` no benchmark claims (e.g. the former HammerDB type `tpcc`, 29 results such as 1794418182) records the failed test `No summary: workload type 'tpcc' belongs to no benchmark` and exits 1. Former type names are not mapped |
| S16 (P7) | `tests/test_loading_checks.py` lists every pipe outside quotes and comments of `experiments/**/*.sh` in `ALLOWED_PIPES`, with how a failure in front of it is noticed; a new pipe fails the test, a stale entry too. 17 pipe lines in 93 scripts, 6 kinds: MySQL/MariaDB `$($MYSQL ... | cut -f2)` (12), Cassandra `nodetool compactionstats | ...`, CockroachDB `cockroach sql ... | tail -n 1` (empty value, loop until timeout, exit 1), Garnet `echo "$reply" | grep -q` (`reply=$(redis-cli SAVE)` already stops `sh -e`), Redis/Valkey `while ...-cli INFO persistence | grep -q` (the `SAVE` after it fails or prints `ERR`); none hides a failure. The scanner leaves out quoted `|` (SQL Server `bcp -t "|"`). Garnet `save-snapshot.sh`: the checkpoint timeout now writes to stderr and exits 1; before, it echoed `ERR checkpoint already in progress`, which `script_failed()` matched already, while the script exited 0. Rule and test named in `experiments/README.md` |
| S17 (P8) | DBMSBenchmarker `Results of all benchmarker pods` names the missing child numbers of a job (`postgresql-1-1-3-1 (3 of 4, missing child 3)`), from the entries' names (`<job>-<child>`). Reduced from the proposal: since S3 a retried pod exits when the child queue is empty, so a duplicate child cannot happen any more and pod names in the entries are not needed. Checked on 1795449026 with one entry left out |
| S18 (P10) | A SUT pod replaced after its loading started is not loaded again: the new pod has no labels, so it looked "not loaded yet" and bexhoma started the schema scripts again (run B, 1795557106, lines 109-111) while old loader jobs could still write through the service. `LoadingCoordinator.start_exec()` keeps the first UID of the repetition (`sut_pod_uid_at_loading_start`, cleared by `reset_sut()` between repetitions) and, for a different UID, calls `fail_loading_fatally("SUT pod ... replaced during loading|during benchmarking (n rounds submitted) (UID a -> b); it is not loaded again")`. The same happens during benchmarking: every loop pass runs `loader.check()`, which takes the state from the pod labels, so a replacement pod looked unloaded and was loaded again while benchmarker pods ran. A repetition with an inherited volume writes the labels into the pod template, so a replacement keeps them and is not reloaded (S6/S13 report it): the experiment aborts with diagnostics. Also found: before, the second start overwrote the UID, so after a successful second load S6 saw only the new pod and passed. The abort ends the repetition before its restart snapshot (S13), so S18 writes it with the new pod and its UID (`store_replaced_pod_snapshot()`); `SUT pods not replaced` then fails too. Cluster run E (2026-11-25, 1795612329, `logs_tests/local/silent_disrupt_ycsb_sut_deleted_benchmarking.log`): YCSB, SUT pod deleted 30 s after both benchmarker pods ran: `replaced during benchmarking (1 round submitted) (UID 15201c7a-... -> 4620404a-...); it is not loaded again`, abort, `Tests failed: 3 of 14`. That run had the code before the snapshot: `SUT pods not replaced` passed; replayed with the snapshot it fails, `bexhoma summary` exits 1 |
| S19 (P14) | Runtime failures are stored in `bexhoma-runtime-failures.json` in the result folder. Every failure found while running goes through `_record_runtime_failure()` (before, four places appended to `_runtime_test_results` directly: loading abort, image pull wait, benchmark start abort, failed benchmarking job); it writes the file (atomic, once per reason; not without an existing result folder, so stand-ins write nothing). The summaries start from `runtime_test_results()`, memory and file merged. Replay on run E with the stored abort reason: `bexhoma summary` shows it, `Tests failed: 4 of 17`, exit 1 |

Not reproduced: a kubectl stream that breaks while the pod keeps running (S1/S10 cover it by exit code and marker).
Also found while preparing the runs (not a failing run): `-nbp` is silently ignored by TPC-H/TPC-DS
(parallel benchmarker pods are `-ne`), see P9.

## 5. Proposals for catches that are still missing

| # | Gap | Proposal |
|---|---|---|
| P1 | done (S12) | - |
| P2 | done (S13) | - |
| P3 | done (4c, S10) | - |
| P4 | done (4c) | - |
| P5 | done (S14) | - |
| P6 | Monitoring: (case 1) a component's fetch never ran, or (case 2, P13) it ran and failed; neither fails a test, see 5b | Options and costs in 5b; recommended E (expected-metrics list, 2026-11-27) |
| P7 | done (S16) | - |
| P8 | done (S17) | - |
| P9 | `-nbp` and `-nbt` are accepted and silently ignored by TPC-H, TPC-DS and SSB (DBMSBenchmarker); no script or docs page passes them there | Deferred (user, 2026-11-25): DBMSBenchmarker may get multi-threading later. Semantics: elsewhere `-nbp`/`-nbt` split one client's load over pods (total constant), `-ne` multiplies whole clients; a DBMSBenchmarker stream (`numProcesses` 1) cannot be split, its parallel streams are `-ne`. So mapping `-nbp` to `-ne` is wrong. Options then: A refuse with that explanation (small, 3 entry scripts), C every entry script declares the base flags it uses (medium, ~40 flags) |
| P10 | done (S18) | - |
| P11 | Benchmarks that terminate pods or containers on purpose (e.g. time to recover) fail the replacement and restart tests, and since S18 a replaced SUT pod aborts the experiment | Separate plan: `dev/plan-planned-disruptions.md` (not started, deliberately later) |
| P12 | done (S15); mapping `tpcc` to HammerDB not done | - |
| P13 | Monitoring fetch failed (case 2 of P6): see 5b | part of 5b |
| P14 | done (S19) | - |

### 5b. Monitoring fetches (P6, P13)

`Monitoring metrics missing` is negative evidence: `collect_missing_metrics()` scans `bexhoma-metrics-*.log`
for DBMSBenchmarker's `Metrics missing for` lines. Without such a line it passes. `Monitoring returned data`
fails only when every component is empty; the per-component CPU test exists only for a component with a table.

- Case 1: the fetch of a component never ran (code path skipped it, exception before it). No log, no table, no test.
- Case 2: the fetch ran and failed before querying (dashboard pod gone, stream broken, `metrics.py` traceback,
  wrong arguments). The log holds the error, nothing matches. `fetch()` uses `execute_command_in_pod()` without
  `report_exit=True` and checks nothing. `MetricFetchBatch.run()` repeats a fetch with a traceback once, but
  does not check the repeat.

Facts: each fetch is queued in `MetricFetchBatch`; the component is registered in
`workload['monitoring_components']` when queued (experiment level, not per connection).

| | What | Case 1 | Case 2 | Cost |
|---|---|---|---|---|
| A. Fetch log check | `report_exit=True` + S10 end marker; summary: the last attempt per `bexhoma-metrics-*.log` has no traceback, no `kubectl exit code`, an end marker. `Monitoring fetches without errors` | no | yes, incl. the unchecked repeat | small (~30 lines, reuses S1/S10); older results partly (tracebacks already logged); no API calls, no image |
| B. Fetch ledger | `MetricFetchBatch` writes queued (connection, component) and final outcome to `bexhoma-metrics-fetches.json`; summary requires ok for each | partly (queued but lost; not never queued) | yes | small-medium (~50 lines); new results only; overlaps A |
| C. Per component, coarse | every registered component has data for at least one connection, unless its phase ran nowhere (no load, `load` mode, optional data generator) | yes, component level | consequence (no data) | medium (~60 lines); "phase ran" rules per component type (SUT loading/benchmarking, loader, data generator, benchmarker, workers, pool); archive replay |
| D. Per connection, exact | per (connection, component) from `connections.config` (`time_loading`, `loading_inherited`/`_deactivated`, job timespans, short phases, tenants, `copy_fetched`): fail if the phase ran without data, else skip with reason | yes, fully | consequence | high (~150 lines), most special cases, false-alarm risk; broad replay (`-nc`, `-sl`, reused volumes, multi-tenant); older results too |

| Combination | Covers | Cost | Left |
|---|---|---|---|
| A + C (recommended) | case 2 directly; case 1 when a whole component has no data | ~90 lines, a day with replay | one connection without data while others have it (e.g. repetition 2) |
| A + D | both, per connection | ~180 lines, several days | zero-filled case stays with `Monitoring metrics missing` |
| B + C | as A + C, a lost fetch named | ~110 lines | ledger only for new results; same per-connection gap |
| A alone | case 2 | smallest | case 1 |

Earlier recommendation: A + C now; D later if the per-connection gap matters. Replaced by E (user, 2026-11-27).

#### E. Expected-metrics list, checked against the result folder (recommended)

Check the result instead of the logs: bexhoma writes down every metric it fetches, the summary checks that
each one is in the result folder. Three rules (user, 2026-11-27):

- **Presence only, never values.** A metric that is 0 over the whole window can be correct (e.g. number of
  vacuums when none ran), so can NaN (e.g. a ratio without activity). Values stay with the tests that know
  the metric: `Monitoring metrics missing` (Prometheus returned no series, with its `sparse` /
  `activity_dependent` reasons) and the CPU test per component. E does not read the `Metrics missing for`
  lines.
- **Nothing from the dashboard pod.** The pod may delete results. The check reads only the local result
  folder; nothing is restored from or compared with the pod.
- **Works on a cleaned and a published folder.** It needs only files that `-rp` and an export keep.

File layout (from 1793529751): per connection `query_{component_type}_metric_{metric}_{connection}.csv`
(the pattern of `bexhoma-copy-metrics.sh`), header line = connection name, then one value per line, no
timestamps. Aggregate `query_{component_type}_metric_{metric}.csv`, one column per connection, written by
`metrics.evaluation.py` in the pod and by `transform_monitoring_results()` locally.

**E1. List, written while running.** `MetricFetchBatch.add_fetch()` appends one row per active metric of the
fetch's metric set (`connectiondata['monitoring'][metrics_type]` after `JOB_QUERY_SETS`, without metrics
switched off by `switch_off_unresolved`) to `bexhoma-metrics-expected.csv`:

```
connection,component_type,metrics_type,metric,time_start,time_end,source
postgresql-1-1-1024-1,loading,metrics,total_cpu_util,1795553600,1795553900,fetch
postgresql-1-1-1024-2,loading,metrics,total_cpu_util,1795553600,1795553900,copy
```

- Rows go in under the batch lock (`parallel_steps` queues from several threads); the file is rewritten
  atomically (tmp + rename), key (connection, component_type, metric), a later row replaces an earlier one.
- `copy_fetched()` adds the target's rows with `source=copy` (same window and metrics as the source).
- The number of rows goes into the workload (`queries.config`, `monitoring_expected_metrics: N`). A folder
  whose `queries.config` names a list that is not there fails (`list missing`) instead of being skipped as
  an older result: a removed list must not turn the check off.
- The list holds connection, component and metric names and Unix times only: nothing that
  `dev/plan-publish-bundle.md` redacts (nodes, IPs, paths, endpoints, credentials).
- Uploaded with `connections.config` at the end of every batch, only because `-fe` downloads the pod folder
  over the local one and an older list in the pod would overwrite the newer local one. The check never
  needs the pod's copy.

**E2. Check per row** (pure function on a folder, next to `missing_metrics`). A row is present when either:

- the per-connection file exists (run, first summary; also a folder `-rp` did not clean), or
- the aggregate has a column for the connection (after `-rp`: `transform_monitoring_results()` merges the
  per-connection files into the aggregate and **deletes them**). The column is named `orig_name` of the
  connection (job level), falling back to `name`; the row's connection is mapped to both through
  `connections.config`.

A per-connection file and a column correspond one to one: a header-only file becomes a column of NaN, a
missing file no column. So "present" gives the same answer before and after the cleanup, which a value
check (empty, all NaN) could not. Status `missing` otherwise.

No exceptions are needed for short windows or optional components: `metrics.py` writes a file for every
metric it queried, also when Prometheus returned nothing (zero-filled). To be confirmed in E5 for a query
that fails with an HTTP error or an exception inside `metrics.py`; if no file is written then, that is
exactly the case to catch.

**E3. Fetch never queued (case 1).** The list cannot see a fetch that was never queued, so a second source
the fetch code does not write: the phase times in `connections.config`.

- `time_loading` > 0 and not `loading_inherited` / `loading_deactivated` → rows for `loading` and `loader`
  of that connection must exist.
- a benchmarker job with a timespan → rows for `benchmarking` and `benchmarker`.
- extra components (data generator, workers, pool) only through the list (their "phase ran" rules are D's
  expensive part).

A missing row is status `not fetched`.

**E4. Test and `bexhoma summary`.** One test: `All expected metrics present` (`missing: n of m`, up to 5
examples). When the fetch log `bexhoma-metrics-{connection}-{component}.log` is in the folder, its last lines
are quoted (what A did); without it the test is the same, only shorter. `bexhoma summary` must give the same
test lines as the run's own summary, on the run folder, on a folder cleaned by `-rp`, and on a published copy.

| Needed | Why | Kept by `-rp` | Kept by an export |
|---|---|---|---|
| `queries.config` | workload, `monitoring_expected_metrics` | yes | yes (needed by every summary) |
| `connections.config` | E3, `orig_name` of a connection | yes | yes |
| `bexhoma-metrics-expected.csv` | E1 | yes | must be kept (add to the bundle's file list) |
| per-connection CSVs or aggregates | E2 | aggregates | at least the aggregates |
| `bexhoma-metrics-*.log` | only the quoted lines | yes | optional |

- No list and no `monitoring_expected_metrics` (results before E): **skipped**, reason `no expected-metrics
  list (older result)`; E3 is skipped too. The archive keeps its exit codes.
- Monitoring off (no rows, `monitoring_components` empty): no test.
- The summary writes no file of its own into the result folder except `report/metrics-check.csv` with `-rp`,
  so a repeated summary gives the same output.
- Order in `show_summary()`: the tests run before the `-rp` cleanup, so the first `-rp` summary sees the
  per-connection files, every later one the aggregates; E2 makes both the same.
- `-fe` on a folder the pod lost files of: the download overwrites only what the pod still has, local files
  stay. If the pod's aggregates lack connections and overwrite complete local ones after a cleanup, the
  folder really lost data and E reports it as `missing`.
- Aborted experiment: `show_summary_aborted()` records the test too (as S11); rows exist only for phases that
  ended.
- Exit code: a `missing`, `not fetched` or `list missing` row fails the test → `tests_outcome()` 1.

**E5. Verification.**

- Unit tests on small synthetic folders: clean; file deleted; header-only file (present); all-zero and
  all-NaN files (present); connection without rows although `time_loading` > 0; `loading_inherited`; `copy`
  rows; list deleted although `queries.config` names it (fails); older folder (skipped). Each case also after
  `transform_monitoring_results()` (aggregate only, per-pod `name` vs. job `orig_name`): same statuses.
- `bexhoma summary -rp` twice on the same copy: same test lines and exit code both times.
- A copy with only the files of the E4 table (aggregates, no fetch logs, no connection subfolders): same
  statuses as the full folder.
- `metrics.py` with a broken query (HTTP error) and with an exception: does it write a file? (see E2).
- Replay with `bexhoma summary` on copies of the 78 folders of 4b: all skipped, exit codes as before.
- Cluster: one normal run each of TPC-H (`-nc 2`, copy rows), YCSB, Benchbase with monitoring; on copies
  delete one CSV, remove all files of repetition 2, delete the list → `bexhoma summary` fails the test and
  exits 1; the untouched folder passes and gives the same test lines as the run's own summary.

Cost: ~110 lines + tests, no image change, no extra API calls. Left: an extra component that is never
queued; a stale file of an earlier fetch with the same connection name (not possible today: every
repetition has its own connection name).

## 6. Later: docs page

When everything is done: a page in `docs/` that lists all mechanisms that catch errors (tests, labels,
markers, exit codes, logs), without history or plans (see memory `feedback_docs_content_rules`).
