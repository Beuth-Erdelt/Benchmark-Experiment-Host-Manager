# Plan: no malfunction stays unnoticed

Status: **implemented on branch silent-malfunctions, cluster-tested 2026-11-24 (section 4c) with the
rebuilt images.** S1-S9 done (section 4), plus S10 (end marker of scripts) and S11 (aborted summary checks
the scripts) found by the cluster tests. Open: the proposals of section 5 and the docs page (section 6).

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

Nothing ran on the cluster. Local Docker containers for the DBMS clients, offline replays of the real
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
| S3 | Benchmarker scripts (benchbase, dbmsbenchmarker, hammerdb, hardware, ycsb) exit 1 with `FATAL: no child number in message queue` instead of running as child 1; bexhoma fills the queue before every job, also for one pod. New test `Benchmarker pods without errors` from the stored benchmarker pod and job descriptions (`loading_checks.check_benchmarker_pods`, same parser as the loader pods) | F2 | done, images to build |
| S4 | TPC-H and TPC-DS generators: `.bexhoma_generated` written at the end, after dbgen/dsdgen, iconv and sed exited 0 (exit codes of iconv and sed are now checked); a raw folder is reused only with it, files without it are deleted (only files: the single-pod folder holds the split subfolders) and generated again. SSB already had `.complete` with staging folders. Consequence: raw folders on the shared volume from images before the marker are generated once more | F4 | done, images to build |
| S5 | `Monitoring returned data` fails when monitoring was on, a phase ran and no component returned anything (per component no data can be right, e.g. no loading phase). Runtime failures (`_record_runtime_failure`): `--experiment-timeout`, a pod log without `BEXHOMA_START/END`, a pod log `store_pod_log` gave up on (`cluster.logs_not_stored`) | F5, F6 | done |
| S6 | `SUT pods not replaced`: UID of the SUT pod when loading started (`sut_pod_uid_loading` in `connections.config`) and of every SUT and worker pod when a round started (`hostsystem['pod_uid']`, read by `get_host_all()` anyway); more than one UID per pod and repetition fails. Hidden in the printed host lists | F7 | done |
| S7 | Benchbase: `Every pod ran for the configured time` (`Elapsed Time (nanoseconds)` ≥ 99 % of `BENCHBASE_TIME`). YCSB: `Execution Phase: every pod ran its configured operations` (sum of `[<OP>].Operations` incl. FAILED, RMW counted once, against `YCSB_OPERATIONS` of the pod) | F8 | done; HammerDB: section 5 |
| S8 | `SP2-nnnn` on stdout matches. **Not** `bash -o pipefail`: the only pipes in `experiments/**/*.sh` are the MySQL/MariaDB `$(mysql ... \| cut)` (a failure ends in the flush timeout and `exit 1` anyway) and `while redis-cli ... \| grep -q`, which pipefail could end early through SIGPIPE. Instead the rule is in `experiments/README.md` ("How a failing script is noticed") | F9 | done |
| S9 | `test_results()` of experiments, mixed experiments and benchmarks return `0`/`1` (the "Test successful!" line could never print). `Host information complete` (warning when RAM, CPU, cores or node is empty); it found the MySQL CPU probe gap (4b) | F10 | done; exit code: section 5 |

### 4b. Verification (offline, 2026-11-24)

- Unit tests: `tests/test_silent_malfunctions.py`.
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

Not reproduced: a kubectl stream that breaks while the pod keeps running (S1/S10 cover it by exit code and marker).
Also found: `-nbp` is silently ignored by TPC-H/TPC-DS (parallel benchmarker pods are `-ne`), see P9.

## 5. Proposals for catches that are still missing

| # | Gap | Proposal |
|---|---|---|
| P1 | bexhoma exits 0 even when a test failed | Opt-in exit code (e.g. `BEXHOMA_FAIL_ON_TEST=1` or a flag) after the summary. Not default: the `test-docs-*` scripts run many experiments in a row and grep `TEST failed` already |
| P2 | A SUT pod replaced after the last round's host information was read (during the last round) is not seen by S6 | Store the UID in the end-of-repetition restart snapshot (`bexhoma-sut-*-restarts.json`) and compare it in the test; one API read per pod and repetition |
| P3 | done (4c, S10) | - |
| P4 | done (4c) | - |
| P5 | HammerDB: a run shorter than `HAMMERDB_DURATION` is not compared | HammerDB prints no elapsed time; add `BEXHOMA_START/END` around the timed test in the benchmarker script and compare with rampup + duration |
| P6 | Monitoring of one component returns nothing while others do | Needs to know which phases ran per component (e.g. from the connection's timespans); then a skipped/failed test per component |
| P7 | A new script with a failure-relevant command in a pipe | Test that lists the allowed pipes in `experiments/**/*.sh` (like the restore-script test in `test_loading_checks.py`) |
| P8 | Duplicate child for DBMSBenchmarker only shows as "n of m" per job; which child ran twice is not named | DBMSBenchmarker per-pod entries could carry the pod name; then name both pods |
| P9 | `-nbp` is accepted and silently ignored by TPC-H/TPC-DS (DBMSBenchmarker uses `-ne`) | Refuse `-nbp` other than 1 for these benchmarks, or map it |
| P10 | A replaced SUT pod during loading makes bexhoma load the new, empty pod again while the old loader jobs still run | Abort the repetition when the SUT pod's UID changes during loading (S6 has the UID at loading start) |

## 6. Later: docs page

When everything is done: a page in `docs/` that lists all mechanisms that catch errors (tests, labels,
markers, exit codes, logs), without history or plans (see memory `feedback_docs_content_rules`).
