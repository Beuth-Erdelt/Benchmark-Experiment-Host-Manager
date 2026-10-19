# Plan: drop the per-stream SUT metrics of DBMS-Benchmarker pods (#239)

Status: **implemented, committed, image rebuilt, verified on the cluster**
(2026-10-18, 1792347080; see "Verify"). Open: release-notes line (no
release-notes file in the repo). Belongs to issue #239 ("Monitoring when
PVC is active"), comment 4 (2024-01-31): stream metrics are collected twice,
once per stream and once per parallel set of streams; are SUT metrics per
stream needed? Answer here: no.

## Today

Two processes fetch the SUT metrics of a DBMS-Benchmarker benchmark round:

1. **Bexhoma**, after the round, in the dashboard pod
   (`experiments/base.py:2879`, `component_type="benchmarking"`), for the
   window of the whole round, connection = the round's connection name.
   Writes `query_benchmarking_metric_<m>_<connection>.csv`.
2. **Each DBMS-Benchmarker pod**, at the end of its stream, because
   `benchmarker.sh` always passes `-mps` (`images/benchmarker_dbmsbenchmarker/benchmarker.sh:294`,
   `:313`). DBMS-Benchmarker `reporter.py:432-439` fetches every metric of
   its connection config for the stream's window (first query start to last
   query end), with `query='benchmarking'`. The pod's connection is renamed
   to `<connection>-<n>` (`benchmarker.py:2447`), so it writes
   `query_benchmarking_metric_<m>_<connection>-<n>.csv` into its subfolder.

What happens to the files of (2):
- `tools.merge_partial_results` copies every file with `metric` in its name
  from the stream subfolders into the result folder (`tools.py:1950-1957`).
  The names differ from (1) (suffix `-<n>`), so nothing is overwritten.
- `transform_monitoring_results` (bexhoma `evaluators/logger.py:299`,
  DBMS-Benchmarker `metrics.evaluation.py:61`) reads per identity
  (`orig_name` = the round's connection) the file of (1). A per-stream file
  is only read when the file of (1) is missing, and then one stream's window
  stands in for the whole round. (The per-connection files stay in the
  local result folder: 1792320882 still holds 120 per-stream files.)
- Nothing else in bexhoma reads them. `missing_metrics.py:15` scans the pod
  log for "Metrics missing" errors of (2), i.e. it only reports (2)'s own
  failures.

So (2) is never used while (1) succeeds, and when (1) fails, its stand-in
covers the wrong window.

## Cost of (2)

- One full set of Prometheus queries per stream at the end of every
  benchmarker pod; the pod (and the job) ends later.
- The benchmarker pod needs Prometheus access.
- Sub-second streams fetch empty series (#239 comment 1), which appear as
  missing-metric warnings.
- Origin: `-mps` was meant as per-query metrics collected per stream, for
  fast queries (DBMS-Benchmarker `docs/Options.md:147`), from before bexhoma
  fetched each round itself.

## Change

- `images/benchmarker_dbmsbenchmarker/benchmarker.sh`: remove `-mps` from
  both `benchmark.py run` calls and its comment line (`:264`). Rebuild the
  benchmarker image.
- DBMS-Benchmarker: no change; `-mps` stays an option for standalone use.
- Bexhoma: no code change needed. The fallback in
  `transform_monitoring_results` and the log scan in `missing_metrics.py`
  stay for results of old images; they find nothing with the new image.
- Docs: `images/benchmarker_dbmsbenchmarker/README.md:94` (flag table),
  release notes (one line: per-stream SUT metrics are no longer fetched).

## Verify

TPC-H SF1 on PostgreSQL with monitoring, two parallel streams (`-nbp 2`),
new image:
- no `query_benchmarking_metric_*_<connection>-<n>.csv` in the result
  folder before the transform; no "Metrics missing" lines in
  `bexhoma-benchmarker-*.log`;
- the combined `query_benchmarking_metric_*.csv` and the report's SUT
  numbers as before (same round window);
- benchmarker pod ends earlier (time from last query to pod exit).

Result (2026-10-18): TPC-H SF1, PostgreSQL, `-ne 1,2 -m -mc`, code
1792347080, baseline 1792320882 (old image, one stream, `-m`):

| | 1792320882 (`-mps`) | 1792347080 (no `-mps`) |
|---|---|---|
| per-stream metric files | 120 | 0 |
| "Fetch metric interval" in benchmarker logs | 60 | 0 (all 3 pods) |
| "Metrics missing" in benchmarker logs | 9 | 0 |
| pod duration minus stream duration | 38 - 34 = 4 s | 16 - 11, 16 - 12, 16 - 12 = 4-5 s |

- Per-stream fetch gone, as intended; bexhoma's round files
  (`query_benchmarking_metric_*_<connection>.csv`) are written as before.
- No measurable speed-up: the 60 fetches ran in parallel and took under
  ~1 s. The gain is fewer queries and no error lines, not time.
- The SUT numbers cannot be compared run to run (different run, round 1
  stream 11 s instead of 34 s).
- Three monitoring tests failed, **not caused by this change**: round 1's
  stream took 11 s, less than the ~30 s scrape interval, so bexhoma's own
  fetch (`bexhoma-metrics-*-benchmarker.log`, `-benchmarking.log`) saw no
  benchmarker sample and a flat SUT counter (CPU 0.00). The per-stream
  files would not have helped: the fallback is only read when the round
  file is missing, and here it exists. This is #239 comment 1 on bexhoma's
  side (windows shorter than a scrape interval); still open.

## Rest of #239

- Comment 2 (shuffled order, last query is not the last executed): fixed,
  `reporter.py:415-418` takes min start / max end over all queries. Moot
  after this change for the per-stream fetch anyway.
- Comment 1 (sub-second runs, empty data inside the benchmarker): gone
  inside the benchmarker with this change; bexhoma's own fetch has the same
  problem for windows shorter than a scrape interval (see "Verify"), open;
  planned as M1b in `dev/plan-metrics-pod-scope.md`.
- "Stop fetching loading metrics when the PVC already holds data": partly
  covered by reusing the loading metrics of inherited loading
  (`configurations/metrics.py:420`); not checked against the case #239 had
  in mind.
- Comment 5 (benchmarker metrics not per benchmarker pod): the
  concurrent-jobs point of `dev/plan-metrics-pod-scope.md`, decision 6; out
  of scope there for now.
