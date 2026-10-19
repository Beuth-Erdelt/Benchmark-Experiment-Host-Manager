# Plan: monitoring metrics must not count pods of earlier phases

Status: M1 **implemented and committed** (2026-10-15, `ee7832d3`). M1b
(phases shorter than the scrape interval, added 2026-10-18) **implemented
and committed** (`92964894`); jobs too short inside a long
loading window are left unreliable (decided 2026-10-18). M2, M3 (unit tests)
and M4 **implemented and committed** (`acf87edb`, see "M2-M4: result"): in the
`cluster.config` templates a `{pods}` placeholder (jobs scoped by job name,
one query set per scope, see "How"), `{namespace}`, and the 90 s filter for
stale series (option (a): template change, no code-side query rewriting; no
warning about old copies). M3 cluster runs **done 2026-10-19** (TPC-C SF1
`-nc 2 -rsrp -xnbf 1,4`, YugabyteDB, Citus `-nw 3 -nc 2`). **Plan done.**
SUT gap with inherited loading measured 2026-10-19 (TPC-H SF1 `-rst nvme
-rsr -nc 2 -ne 1,1`, 1792369868): old SUT's last sample 00:38:52, repetition
2's first benchmark window 00:43:00, 248 s (> 90 s); repetition 2 round 1
Max RAM 0.39 GB (fresh SUT, old one not counted). `-ks` keeps only the last
repetition's SUT, so it adds no restart gap. Optional, not run: several
benchmarker jobs per round (`experiment_dict`). Release note: users copy the
cAdvisor queries of `k8s-cluster.config` into their `cluster.config`.

## M2-M4: result (2026-10-18)

- Templates: the 14 cAdvisor queries of `k8s-cluster.config` (and the local
  `cluster.config`) use `pod=~"{pods}", namespace="{namespace}"`; the 11
  instant ones `(X and (time() - timestamp(X)) < 90)`. Checked read-only on
  the cluster Prometheus with the live YugabyteDB loading pods
  (1792348454): all 14 return `success`, with data in namespace `perdelt`
  and none in `monitor`.
- `SutConfiguration.pods_pattern()` (the old literal pattern, default for
  `metrics`, workers, YugabyteDB), `job_pods_pattern()` (`(<job>-)[:58]` +
  `[a-z0-9]{5}`, or `.+` for all loading jobs of a repetition),
  `monitoring_namespace()`; `run_pod()` builds both job names with
  `generate_component_name()` as the manifests do and passes them to
  `get_connection_config(job_pods=)`, which writes `metrics_benchmarker` and
  `metrics_loading`. `fetch()` switches `metrics` to the job set for
  `benchmarker`, `loader`, `datagenerator` when the connection has it.
- Silent check (decision 3), changed: not a string search on the templates
  but on the **stored** queries: `monitoring_math.scoped_job_connections()`
  calls a connection scoped when its job query differs from the one in
  `metrics`. Works on re-evaluation without `cluster.config`; old results and
  old templates (identical sets) keep `max - min` and the 2 x threshold.
- Counting rule (decision 5), **changed**: scoped job total = first value +
  `counter_increase()` (positive steps). The plan's "a value below the last
  one is a new counter and counts fully" is not implemented: the job series
  is a sum over the job's pods, and with the 90 s filter a finished pod
  leaves that sum, so the sum drops while the other pods run on; counting the
  lower value fully would count their CPU twice. A container restart inside
  a job (counter reset) is therefore undercounted by its growth before the
  restart; rare for jobs.
- `short_phase_connections()` and `collect_missing_metrics()` pick the
  threshold per connection (1.2 x for scoped jobs).
- Tests: `tests/test_pods_scope.py` (templates, formatting per branch, job
  patterns incl. `-1-1` vs `-1-10`, other repetitions, truncation, fetch
  query set, scoped detection, counting, thresholds);
  `test_ceph_storage_monitoring` formats with `pods`/`namespace`. 641 tests,
  only the known `test_hardware_baseline` failure.
- Docs: `docs/Monitoring.md` ("Pods of a phase", placeholders, counter
  kind, short-phase table), `docs/Config.md`, `docs/AgentResultContract.md`,
  `contracts/contract_result.yml` (CPU check wording; schema version
  unchanged).
- Cluster, YugabyteDB YCSB (1792356094): all tests passed; fetches used
  `metrics_benchmarker`, `metrics_loading`, `metrics_yb-master`,
  `metrics_yb-tserver`.
- Cluster, M3 run Benchbase TPC-C SF1 PostgreSQL `-nc 2 -rsrp -xnbf 1,4`
  (1792359757, `dev/logs_pod_scope/tpcc_postgresql_m3.log`):
  - SUT loading rep 1 / rep 2: 16.17 / 15.91 CPU-s, Max RAM 0.50 / 0.50 GB
    (no old SUT in rep 2).
  - Benchmarker rounds differ: rep 1 47.79 / 61.61, rep 2 59.32 / 56.30
    CPU-s; round 1's pod series lingered 5 min into round 2 (Prometheus
    pod spans) and is not counted.
  - SUT gap (contradiction "SUT gap after a restart"): rep 1 SUT's last real
    sample ~23:52:55, rep 2 loading window from 23:56:41: ~3.7 min, above
    90 s. Rep 2 SUT pod started 23:54:10, but no phase window starts before
    loading. Resolved for this setup; `-ks`/inherited loading not measured.
  - Loader: CPU 0.09 / 0 and "Monitoring metrics missing" failed: the
    Benchbase loading pod's `sensor` container ran 25 s in a 56-67 s
    window, one sample in rep 1, none in rep 2. The accepted "short job in
    a long loading window" case, not a regression.
- Cluster, workers: YCSB Citus `-nw 3 -nc 2 -rsrp` (1792360184,
  `dev/logs_pod_scope/ycsb_citus_workers.log`). The worker pods keep their
  names across repetitions (StatefulSet), so only the 90 s filter separates
  them:
  - worker loading rep 1 / rep 2: 337.4 / 329.1 CPU-s, Max RAM 3.25 / 2.95 GB;
    SUT loading 111.3 / 103.6; loader 52.6 / 48.5. No old pods counted.
  - All monitoring tests passed. Failed, unrelated to monitoring: worker 0
    `OOMKilled` in rep 2 benchmarking (container limit 64Gi, working set
    51 GB at the last scrape, node cl-worker24 had ~430 GB free), hence "No
    SUT container restarts" and the YCSB FAILED column. Worker 2 stayed at
    1.9 GB while workers 0 and 1 reached ~50 GB.

## Problem

Every pod metric matches pods by
`pod=~"(.*){configuration}-{experiment}(.*)"` (`cluster.config`,
`monitor.metrics`), for the SUT and, with the container swapped, for the
loader, data generator and benchmarker (`configurations/metrics.py::fetch`,
DBMS-Benchmarker `monitor.metrics.fetchMetric`). That selects every pod of
the configuration in the experiment: all repetitions, rounds and jobs. The
queries also have no namespace filter.

**A stopped container stays in the results for 5 minutes.** cAdvisor exposes
its samples with explicit timestamps, for which Prometheus writes no
staleness markers, so a series is returned until the 5-minute lookback runs
out. Seen: the old SUT pod's last raw sample at 00:48:29, still in query
results until ~00:53.

A phase starting in that time sums the old pod's last values with the new
pod's:
- **counters**: `max - min` returned the old pod's lifetime total
  (1792023056 rep 2 loading: 4205 CPU-s, true 147);
- **gauges**: Max RAM includes the old pod (same window: 6.13 GB instead of
  1.80 GB);
- hit: the SUT in the first phase of repetitions 2+ (`-rsrp` loading, or the
  first round when loading is inherited), the benchmarker in round 2+
  (rounds start ~160 s apart; YCSB rounds 1 and 2 report identical totals).
- not hit: rates (`irate(...[5m])`, Max CPU): a flat stale series has rate 0.

Separate, rarer: two jobs of one configuration that really run at the same
time (several benchmarker jobs per round via `experiment_dict`) are both
live, so each job's metrics include the other's.

## Update 2026-10-18: shorter gaps between rounds

`dev/plan-fewer-kubectl-calls.md` (M11, M14, M7) cut the time from the end
of a round to the start of the next one of the same configuration (last
`BEXHOMA_END` to first `BEXHOMA_START`): tenancy_2 202 -> 94 s (91-106 s),
tenancy_8 663 -> 212 s, single SUT estimated 12-40 s. Decision 1 assumed
"phases start at least ~160 s after the previous pod stopped"; that no
longer holds for rounds, so the 90 s filter alone would not keep round k's
benchmarker out of round k+1 (it was never out today either: 5 min linger).

Decided 2026-10-18:
- **Jobs (benchmarker, loader, data generator) are scoped by job name**, the
  main fix for them, not only for concurrent jobs (decision 6 moves in):
  their pods are named `bexhoma-<component>-{configuration}-{experiment}-{run}-{client}[-{benchmark_run}]-<hash>`,
  so a selector on the job's prefix never sees pods of other rounds or
  repetitions, whatever the gap. The job names are known when `run_pod()`
  writes the connection file (one benchmarker job per connection, the
  loading jobs of its repetition); see "How" below. The job counting rule
  (decision 5) then applies to them.
- **The SUT keeps the 90 s filter** (decision 1): its pods change only
  between repetitions, which stay minutes apart (removal + start + loading
  or `delay_prepare`).
- Workers: as the SUT (filter + namespace), unchanged.

### How: one `{pods}` placeholder, one query set per scope

Still option (a) (decision 2): a template change, filled by bexhoma like
`{configuration}` today, no rewriting of formatted queries. No change in
DBMS-Benchmarker or the dashboard image: `metrics.py -mt <name>` already
picks any query set of `connectiondata['monitoring']` and falls back to
`metrics` when it does not exist (DBMS-Benchmarker `metrics.py:96`).

1. **Templates** (`k8s-cluster.config`, `monitor.metrics`): the pod pattern
   becomes a placeholder, plus the namespace (decision 4); the duplicated
   `pod=~` goes:
   ```python
   # today
   'query': 'sum(container_cpu_usage_seconds_total{{pod=~"(.*){configuration}-{experiment}(.*)", pod=~"(.*){configuration}-{experiment}(.*)", container="dbms"}})'
   # new
   'query': 'sum(container_cpu_usage_seconds_total{{pod=~"{pods}", namespace="{namespace}", container="dbms"}})'
   ```
   The 90 s filter (decision 1) wraps the selector as planned; for jobs it
   is harmless (their own pods drop out only after their window).
2. **bexhoma fills `{pods}` per scope** in `get_connection_config()` and
   writes one query set per scope into `<connection>.config`:

   | Query set | `{pods}` | for |
   |---|---|---|
   | `metrics` (as today) | `(.*){configuration}-{experiment}(.*)`, today's pattern | SUT and other deployments (`container="dbms"` keeps job pods out) |
   | `metrics_benchmarker` (new) | `bexhoma-benchmarker-{configuration}-{experiment}-{run}-{client}-{benchmark_run}-[a-z0-9]{5}` | the benchmarker job of exactly this connection |
   | `metrics_loading` (new) | `bexhoma-loading-{configuration}-{experiment}-{run}-.+` | all loading and data generator jobs of this repetition (several loaders together, as today) |
   | `metrics_<statefulset>` (as today) | the worker pattern of `set_metric_of_config()` | workers |

   The job patterns are built with `generate_component_name()`, the function
   that names the jobs in the manifest, so they cannot drift apart; the
   legacy path without benchmark index drops `-{benchmark_run}` as the job
   name does. The pod suffix is exactly 5 characters (Prometheus regexes are
   anchored), so `…-1-1` does not match the pods of `…-1-10`.
3. **Fetch**: `MetricsCollector.fetch()` passes `metrics_type` =
   `metrics_benchmarker` for component `benchmarker`, `metrics_loading` for
   `loader` and `datagenerator`. Container swap, CSV names
   (`query_<component_type>_metric_<key>_<connection>.csv`), evaluation,
   summary and report are unchanged: one row per connection as today, only
   the pods behind each row change.

Effect on summary and report:
- one benchmarker per round: rows unchanged; round 1 as today (plus the
  first-value rule of decision 5); rounds 2+ no longer include the previous
  round's pod (Max RAM, CPU [CPUs]); Max CPU (rate) unchanged;
- several benchmarker jobs in one round (`experiment_dict`): today each row
  shows the sum of all jobs of the round (identical rows); then each row
  shows its own job, and the rows of a round add up correctly;
- loader / data generator: rows unchanged, other repetitions excluded.

Care:
- every place that formats a template passes `pods=` and `namespace=`, or a
  new template raises `KeyError`: `set_metric_of_config_default()`, every
  branch of `set_metric_of_config()` (YugabyteDB included), application
  metrics (same function);
- a template without `{pods}` (an old `cluster.config` copy) still formats
  (unused keyword): the job query sets equal `metrics`, today's behaviour,
  silently (decision 3);
- counting rule (decision 5): CSVs of the job query sets contain only the
  job's own pods, the condition for "first value + positive steps";
  `monitoring_math` keys it on the component and the silent check for
  `{pods}` in the template;
- each connection file gets two more copies of the metric definitions
  (~20 queries each), harmless.
- Old results are ignored (decision 7); no marker in the report needed.

Also found 2026-10-18 (tenancy_2 1792334082, not a linger): a loader running
~45 s gets one or two cAdvisor samples at a ~30 s scrape interval. With one
sample, `irate()` returns nothing, so "CPU [CPUs]" is 0 and the counter
total is 0 (`max - min` of one value); with two it works. Tenant 1's loader
had one sample (158 CPU-s) in all 3 repetitions, tenant 2's two. Not fixable
in the query; options: count a single-sample counter series as growth from
0 (decision 5's first-value rule does exactly that for jobs), mark job
metrics with fewer than 2 samples as missing instead of 0, or a shorter
scrape interval.

## How metrics flow

Unchanged by this plan except steps 2 and 3: `{pods}` is filled per scope
and the job fetches pick their own query set (see "How").

1. `cluster.config` `monitor.metrics.<key>.query`: PromQL template.
2. `MetricsCollector.get_connection_config()` formats it per configuration
   (`set_metric_of_config_default`, workers `set_metric_of_config`) into
   `connections.config` / `<connection>.config`.
3. `fetch()` runs DBMS-Benchmarker's `metrics.py` in the dashboard pod; it
   swaps the container label, runs `query_range` (step 1 s), keeps only
   `result[0]`, re-indexes the values to start at the first sample, pads
   missing samples at the end with zeros, writes
   `query_<component_type>_metric_<key>_<connection>.csv`.
4. Bexhoma reduces the CSVs (`monitoring_math.counter_total`, max, mean).

## Done: M1, counter reduction

`bexhoma/monitoring_math.py`: `counter_increase()` (sum of positive steps,
like PromQL `increase()`) and `counter_total(df, component)`; used in
`experiments/base.py` (CPU [CPUs], application counters),
`report_writer.py::_aggregate_metric`, `collectors/base.py`; tests in
`tests/test_monitoring_math.py`.

Positive steps for the SUT side only. Job pods (loader, datagenerator,
benchmarker) start inside the window; because of the re-indexing and the end
padding (step 3) their first value is no baseline, and a job whose first
scrape already shows its CPU would count 0. They keep `max - min`.

Effect on the stored storage probes (only SUT phases change): 1792023056 rep
2/3 loading 4205/4253 -> 147/139; 1792031806 rep 2/3 first round 4408/779 ->
305/293; 1792029787 run 3 526 -> 487; 1792020386 rep 2/3 loading 491/490 ->
489/469; 1791970052 rep 2/3 loading 2517/2461 -> 135/145. Stored results are
corrected on re-evaluation.

## M1b: phases shorter than the scrape interval (planned 2026-10-18)

### Problem

A counter needs two scrapes inside the window to show growth, a gauge one;
a job pod that lives shorter than one scrape interval may never be scraped.
Seen in 1792347080 (TPC-H SF1, `-ne 1,2 -m -mc`, check run of
`dev/plan-stream-metrics.md`): round 1's stream took 11 s, so the SUT
counter stayed flat (CPU 0.00) and the benchmarker had no sample at all
(all metrics "missing"). Three tests failed: SUT and benchmarker "contains
0 or NaN in CPU [CPUs]", "Monitoring metrics missing". Same cause as the
tenancy_2 loader with one sample (see "Update 2026-10-18").

The existing guard does not fire: `experiments/base.py:3430` skips the CPU
test when a series has fewer than `MIN_MONITORING_SAMPLES = 2` values, but
counts **rows**. The fetch runs with a 1 s step and repeats the latest scrape
(or fills zeros) in every row, so 1792347080 round 1 had 14 rows from one
scrape. `missing_metrics.py` knows only two expected reasons (data
pre-existing, sparse), none for short phases.

How much a window can show, at a scrape interval `I` (cluster: 28-32 s).
Every 1 s row holds the latest scrape at or before it, so the first row of a
pod that already runs (SUT, workers) is the scrape **before** the window:

- **SUT / workers (counters):** growth = last scrape in the window minus the
  scrape before it. One scrape inside the window is enough; the counted span
  has about the window's length, shifted earlier by up to `I` (tail missed,
  some time before the start counted). Roughly unbiased at constant load.
- **Jobs (counters):** the pod starts inside the window, there is no scrape
  before it. Today's `max - min` needs two scrapes inside; decision 5's
  first-value rule needs one. The tail after the pod's last scrape is never
  recorded (no scrape after the pod stopped).
- **Gauges (Max RAM):** one sample inside the window; peaks between scrapes
  are missed.

| window | SUT / workers | jobs today (`max - min`) | jobs after decision 5 |
|---|---|---|---|
| < I | maybe no scrape inside: 0 | maybe never scraped | maybe never scraped |
| I to 2I | at least 1 scrape: measurable | 1 or 2 scrapes, by chance | measurable |
| >= 2I | measurable | measurable | measurable |

(`I` with jitter: use `1.2 x I` for "at least one scrape".)

### Decisions

1. **Rule per component** (revised 2026-10-18): SUT and workers not
   measurable below `1.2 x I`; jobs below `2 x I` while they use
   `max - min`, below `1.2 x I` once decision 5 is in. Data-only rules
   ("fewer than 2 distinct values") are rejected: a broken query over a long
   phase is constant too and must still fail.
2. **Scrape interval of the cluster Prometheus as a config key**
   `monitor.scrape_interval` (seconds, default 30) in `cluster.config` /
   `k8s-cluster.config`. Not `prometheus_interval`: that one only sets
   bexhoma's own Prometheus (template `{prometheus_interval}`, 10 s default,
   30 s in the TPC-H builder).
3. **Window length from the fetch log**: `metrics.py` prints
   `Interval length <N>s` into `bexhoma-metrics-{connection}-{component}.log`,
   the same file `missing_metrics.py` already reads. One parser for both
   places.
4. **CPU test**: below the rule, *skipped* ("phase shorter than monitoring
   scrape interval", existing text) and the table shows `n/a` instead of
   `0.00` for that connection. Replaces the row-count guard.
5. **Missing metrics**: third expected reason
   `EXPECTED_SHORT_PHASE = "phase shorter than scrape interval"` for gaps in
   a fetch log whose window is below the rule. Then "Monitoring metrics
   missing" is skipped, not failed, when every gap has a reason.
6. **No widening to make up for the scrape interval**: an end widened by
   `I` makes SUT counters count about one interval too much (scrape before
   start to scrape after end), gains nothing for jobs (no scrape after a pod
   stopped), and puts the next round into gauges (gaps between rounds are
   12-40 s since `dev/plan-fewer-kubectl-calls.md`). `extend` and `shift`
   stay as knobs for clocks out of sync, default 0 (2026-10-18; measured
   offset host vs. cluster Prometheus 0.3-0.5 s); docs say `extend` <= 5 s.
   Deferred, only if a run shows the need: interpolate counters at the exact
   start and end between the bracketing scrapes (fetch counters to `end + I`,
   scrape times from the value changes in the 1 s rows).
7. **Interplay with decision 5**: once jobs count their first value (with
   `{pods}` in the template), a job with a single sample gets a real total
   (the tenancy_2 loader); its threshold drops to `1.2 x I` (decision 1).
   M1b uses the same silent `{pods}` check per metric to pick the job
   threshold.
8. **Result contract**: `contract_result.yml` `monitoring_component_cpu_nonzero`
   says "SKIPPED when phase < 1 scrape interval" (update to decision 1) and
   `no_monitoring_metrics_missing.expected_gaps` gets the new reason; additive,
   minor version. The agent harness (`agent/harness/tools.py:2448`) skips
   non-numeric CPU cells, so `n/a` is not listed as an affected phase.

### Implementation

- `cluster.config` / `k8s-cluster.config`: `'scrape_interval': 30` under
  `monitor`.
- `missing_metrics.py`: `fetch_window(path) -> int | None` (parses
  `Interval length`), the new expected reason in `collect_missing_metrics`
  (needs the scrape interval as a parameter).
- `experiments/base.py`: `show_summary_monitoring_table` takes the window
  per connection from the fetch logs; skip + `n/a` per decision 4;
  `MIN_MONITORING_SAMPLES` goes.
- Tests (`tests/test_missing_metrics.py`, a monitoring-summary test):
  SUT window 11 s -> skipped and `n/a`; SUT 45 s -> measured; job 45 s with
  `max - min` -> skipped; 600 s with zeros -> failed; reason only for short
  windows; missing `Interval length` line (old logs) -> old behaviour.
- `contracts/contract_result.yml` and its mirror doc (decision 8).
- Check: re-evaluate 1792347080 locally (no cluster run): round 1 skipped,
  round 2 unchanged.
- `docs/Monitoring.md`: minimum phase length, accuracy of CPU totals
  (about one scrape interval per phase), the key.

### M1b: result (2026-10-18)

Implemented as above: `monitor.scrape_interval` (default 30) in
`k8s-cluster.config` and `cluster.config`; `monitoring_math.min_measurable_window()`
(1.2 x I for SUT/workers, 2 x I for jobs, 1.2 x I for jobs with
`jobs_scoped=True`, for M2); `missing_metrics.fetch_window()` and
`EXPECTED_SHORT_PHASE` (`collect_missing_metrics(..., scrape_interval=)`);
`ExperimentBase.scrape_interval()`, `short_phase_connections()`,
`mark_not_measurable()`; summary and report show `n/a` and test only the
measurable connections (skipped when none is); `MIN_MONITORING_SAMPLES`
removed; result contract 1.12.0 (`report_writer.SCHEMA_VERSION`), its
prose in `docs/AgentResultContract.md`; `docs/Monitoring.md` ("Short
phases"), `docs/Config.md`. Tests: `tests/test_short_phases.py`, new cases
in `tests/test_missing_metrics.py`.

Check, 1792347080 evaluated again locally: both benchmarking rounds (11 s
and 13 s; round 2 is short too, unlike the expectation "round 2
unchanged") show `n/a` for SUT and benchmarker, both CPU tests **skipped**
instead of failed, their gaps carry the new reason; loading tables and
tests unchanged.

**Found: jobs in a long loading window.** "Monitoring metrics missing" still
failed there, on the loader's `CPU Utilization [CPUs]` (`irate`, needs two
samples): the loader pods ran ~8 s inside a 165 s loading window, so the
window rule calls the phase measurable. Same case as the tenancy_2 loader
(one scrape). The window of a loading fetch is the whole loading phase, not
a job's life.

**Decision (2026-10-18): ignored for now.** A job too short for its
metrics is not reliable, and the test may say so; no extra rule.

Tried and taken out: "a missing metric is expected when its fetch saw at
least one but fewer scrapes than the query needs", with the scrapes needed
from the query text (2 for `rate`, `irate`, `increase`, ...) and the scrapes
seen as value runs in the fetch's CSVs. It does not hold:
- a fetch is not one scope: it also holds node metrics (`instance="{host}"`),
  Ceph pool metrics and network metrics without a container filter, which
  change with other targets' scrapes (tenancy_2 tenant 1's loader: 1 run in
  its own container metrics, 5-76 in the others);
- the CSVs are sums over pods: 8 loader pods with one scrape each at
  different times give several runs (1792347080), while every pod's rate is
  empty.

If it is ever needed: (A) take the runs only from a fetched metric with the
same series selector as the missing query (exact for one pod, stays strict
for several); (B) when a metric comes back empty, DBMS-Benchmarker runs
`max(count_over_time(<selector>[<window>]))` and logs the samples per series
(exact for any number of pods; needs a release and a new dashboard image).
Also rejected: the jobs' own spans (`loading_timespans`) as their window
(shorter than the pods' life, would show `n/a` for loaders that had two
scrapes).

### Open

- Done 2026-10-18: `extend` and `shift` never took effect
  (`configurations/metrics.py` read `grafanaextend` / `grafanashift`). Now
  read under their documented names (the `grafana*` names still work);
  `'extend': 20` became `'extend': 0` in `cluster.config` and
  `k8s-cluster.config`; `docs/Config.md` and `docs/Monitoring.md` describe
  both as clock-skew knobs, `extend` <= 5 s (decision 6). No stored result
  changes: both were never applied.

## Decisions for M2-M4

1. **Drop stale series in the query.** Every cAdvisor instant selector `X`
   in the templates becomes
   `(X and (time() - timestamp(X)) < 90)`. `timestamp()` returns the time
   of the sample the query uses; a live pod's newest sample is at most one
   scrape interval old (28-32 s on this cluster), a stopped pod's keeps
   ageing and drops out after 90 s instead of 5 min. Since 2026-10-18 it
   matters for the **SUT and workers**: jobs are scoped by job name
   (decision 6), so the gap between rounds (now 12-40 s) no longer counts;
   for jobs the filter is harmless. Relies on the SUT restarting at least
   90 s after the old pod stopped (assumed ~3.5 min; to be measured, see
   "Contradictions"). Tested on 1792023056 rep 2 loading (see "Evidence").
2. **Option (a): change the shipped template, do not rewrite queries in
   code.** `k8s-cluster.config` gets, in the cAdvisor templates, `{pods}`
   instead of the literal pod pattern (all 14, decision 6), the namespace
   (decision 4), and the filter in the 11 instant-selector templates. The 3
   templates inside `irate(...[5m])` keep no filter (rate 0 for a stale
   series). Bexhoma only fills placeholders, as it does for
   `{configuration}`; formatted queries are never edited. Users copy the
   new queries into their own `cluster.config` (git-ignored). The threshold
   is a literal `90` in the query: visible, and changed by editing the
   template.
3. **Old copies are neither changed nor warned about** (2026-10-18). An
   unchanged `cluster.config` keeps the old behaviour without any message:
   without `{pods}` the job query sets equal `metrics`. Bexhoma only checks
   silently, per metric, whether its template contains `{pods}`. That check
   picks the job counting rule (decision 5) and is reported nowhere. It is a
   string search on the loaded templates, no Prometheus or cluster call.
4. **Namespace filter (required: worker queries carry no experiment code,
   see the TiDB evidence).** The same 14 cAdvisor templates get
   `namespace="{namespace}"`; the formatting calls supply `namespace`.
   An old template without `{namespace}` keeps working (unused keyword).
5. **Counters for job scopes (follow-up to M1).** With `{pods}` set to the
   job's own pods, a job's series contains only its own pods. Then:
   - jobs: total = positive steps + first value (their pods start inside the
     window, so the first value is growth from 0; removes the round-1
     undercount of `max - min`, e.g. 151 vs ~167);
   - guard against gaps: missed scrapes longer than 90 s (Prometheus or
     kubelet restart) drop a live pod for a moment; its reappearance must
     not count its whole counter again. Rule (like PromQL `increase()`):
     after a gap or drop, a value above the last value before it counts
     only the difference (`100, 110, [gap], 125` -> 25, not 135); a value
     below it is a new counter and counts fully.
   Only for job components (loader, data generator, benchmarker) whose
   template contains `{pods}` (decision 3, per metric); otherwise the jobs
   keep `max - min`. Both rules run on the fetched CSV in
   `monitoring_math.py`, no extra query. The gap guard matters for the SUT
   too (it applies to positive steps generally).
6. **Jobs scoped by job name** (changed 2026-10-18, see "Update 2026-10-18"
   and "How"): `{pods}` per query set, `metrics_benchmarker` for the
   connection's benchmarker job, `metrics_loading` for the repetition's
   loading and data generator jobs, built with `generate_component_name()`.
   Fixes rounds following each other within seconds and concurrent jobs.
7. **Old results are ignored** (2026-10-18): the new queries only act when
   Prometheus is queried, so results fetched before them are not re-fetched
   or marked. Re-evaluation still applies M1 (and M1b) to them.

## Evidence (2026-10-15, cluster Prometheus)

Repetition 2 loading of 1792023056 (window 00:51:55-00:53:37), sum over
`pod=~"(.*)postgresql-1-1792023056(.*)", container="dbms"`:

| UTC | CPU plain | CPU filtered | RAM plain GB | RAM filtered GB |
|---|---|---|---|---|
| 00:50:00 | 4206.0 | 0.6 | 4.47 | 0.14 |
| 00:52:00 | 4206.1 | 0.8 | 4.47 | 0.14 |
| 00:52:30 | 4242.3 | 37.0 | 5.36 | 1.03 |
| 00:53:00 | 4353.4 | 148.0 | 6.13 | 1.80 |
| 00:53:30 | 148.0 | 148.0 | 1.80 | 1.80 |

Filtered: CPU in the window 0.8 -> 148 (147, even by `max - min`), Max RAM
1.80 GB (rep 1: 1.82). The old pod is out from 00:50:00, 91 s after its last
sample.

### All storage probes (2026-10-15)

Every `metrics.py` call of the 8 storage experiments (1792020386,
1792023056, 1792029787, 1792031806 and the 10-14 runs 1791970052,
1791980506, 1791996160, 1791998393): 162 fetches, re-run with their own
window, container and formatted query (from `bexhoma-metrics-*.log` and
`<connection>.config`). Ground truth: only the phase's own pods (SUT pod of
the repetition, loading jobs of the repetition, benchmarker job of the
round), from their raw samples; 161 fetches have one (1791998393 loading
lacks the SUT pod description). Script:
`verify_filter.py` / `summarize_verify.py` (session scratchpad).

CPU totals off by more than 2 % or 0.5 CPU-s:

| Component | Fetches | Today | M1 only | Filter + M1 | Filter + job rule |
|---|---|---|---|---|---|
| SUT loading | 32 | 15 | 0 | 0 | 0 |
| SUT benchmarking | 45 | 4 | 0 | 0 | 0 |
| Benchmarker | 45 | 22 | 22 | 0 | 0 |
| Loader | 33 | 0 | 0 | 1 | 0 |
| Data generator | 6 | 0 | 0 | 0 | 0 |
| **All** | **161** | **41** | **22** | **1** | **0** |

Largest remaining deviation: 0.03 CPU-s. Max RAM off by more than 2 % or
0.01 GB: 18 today (14 SUT loading, 2 SUT benchmarking, 2 benchmarker), 0
with the filter (largest deviation 0.000 GB).

Read:
- today a quarter of all CPU totals is wrong, in both directions (TPC-C
  round 4 benchmarker 1043 instead of 1650, YCSB round 2 126 instead of 102);
- M1 alone fixes the SUT, not the benchmarker (as designed);
- the filter fixes the benchmarker and every Max RAM;
- decision 5 is needed: without the first value, 1792020386 rep 3 loader
  gives 311.7 instead of 327.9 (its first scrape already carried CPU);
- loader and data generator were never hit (repetitions are far more than
  5 min apart).

Not covered by these runs: worker StatefulSets (all single PostgreSQL),
truly concurrent jobs of one configuration, missed scrapes (the
reappearance guard of decision 5). The truth comes from the same cAdvisor
data, so it verifies which pods are counted, not cAdvisor itself.

### TiDB with worker StatefulSets (1792064085, 2026-10-15)

BenchBase TPC-C SF16 on TiDB (3 SQL replicas as the SUT Deployment, PD and
TiKV as worker StatefulSets, 3 pods each), `-nc 1`, rounds `-nbp 1,2`,
nvme. All 16 fetches (SUT, loader, benchmarker, PD and TiKV, loading and
benchmarking) agree with the ground truth for every method, CPU and Max RAM:
no restart, and the rounds are 527 s apart (PostgreSQL runs: ~160 s). So the
filter is harmless on StatefulSets and a multi-replica SUT; the worker
linger itself is still untested.

Found:
- **Worker queries carry no experiment code** (and no namespace):
  `pod=~"(.*)bexhoma-pd-tidb-nvme-benchbase-tpcc-16-(.*)"`. Worker pods are
  named after the storage configuration, so every experiment of the same
  configuration has the same worker pod names; Prometheus still held the
  previous experiment's incarnations (10:24-10:58). A run within 5 min of
  the previous one is covered by the filter; **another user running the
  same configuration at the same time is summed in for the whole run**, and
  only the namespace filter prevents that: decision 4 is required, not
  optional.
- **The cgroup `id` format differs per node** (systemd
  `.../kubepods-burstable-pod<uid_with_underscores>.slice/...` on one node,
  cgroupfs `/kubepods/burstable/pod<uid>/...` on the others). Confirms
  rejecting UID-based worker selectors; the filter does not depend on it.
- **Round spacing depends on the DBMS** (160 s PostgreSQL, 527 s TiDB): the
  90 s threshold relies on the minimum gap, not the typical one.

Next run to close the gap: the same TiDB experiment with `-nc 2` (restart,
worker pods get the same names again), ideally twice in a row (back-to-back
experiments).

Other checks:
- DBMS-Benchmarker's container swap (`str.replace`) and the worker
  `container="dbms"` stripping (`set_metric_of_config`) replace every
  occurrence, so the selector may appear twice.
- `pod-template-hash` and pod UIDs (cAdvisor `id` =
  `/kubepods/<qos>/pod<uid>/<container>`) exist, but are not needed any more.
- The per-stream metrics of DBMS-Benchmarker jobs (`-mps`) use the same
  templates and are covered by the filter; bexhoma does not read them.

## Implementation sketch

### M2: templates, query sets, fetch

- `k8s-cluster.config`: in the 14 cAdvisor templates the doubled
  `pod=~"(.*){configuration}-{experiment}(.*)"` becomes one
  `pod=~"{pods}"` plus `namespace="{namespace}"`; the 11 instant-selector
  templates get the filter (decision 1). Keep the query shapes as they are
  (`sum(...)`, `sum(max(...) by (instance))`, `sum(max by (pod) (...))`);
  wrap only the selector.
- `configurations/base.py`: `set_metric_of_config_default` and every branch
  of `set_metric_of_config` (YugabyteDB included) pass `pods=` and
  `namespace=`. These two are the only places that format the templates
  (both called from `configurations/metrics.py`; checked 2026-10-18).
- `configurations/metrics.py` `get_connection_config()`: besides `metrics`
  and `metrics_<statefulset>`, write `metrics_benchmarker` and
  `metrics_loading` with the job patterns of "How" (step 2), from
  `generate_component_name()`.
- `MetricsCollector.fetch()`: `metrics_type="metrics_benchmarker"` for
  component `benchmarker`, `"metrics_loading"` for `loader` and
  `datagenerator`. No change in DBMS-Benchmarker (`metrics.py -mt` falls
  back to `metrics`).
- Silent check (decision 3): a helper telling per metric key whether its
  template contains `{pods}`; used by the job counting rule only, no
  output.

### M3: tests

- Every cAdvisor template in `k8s-cluster.config` has `pod=~"{pods}"` once
  and `namespace="{namespace}"`; the instant ones the filter, the `irate`
  ones not; all still format (no unknown placeholder) and parse as
  PromQL-shaped strings; an old-style template formats with `pods=` and
  `namespace=` passed (unused keywords).
- Job patterns: equal to the names `generate_component_name()` gives the
  jobs; `...-1-1` does not match pods of `...-1-10`; the legacy path without
  benchmark index; the loading pattern matches loader and data generator
  pods of the repetition and no other repetition's.
- Connection file: `metrics_benchmarker` / `metrics_loading` present, with
  the connection's own job; `fetch()` passes the right `metrics_type`.
- Silent check: true for the new templates, false for old-style ones.
- M1 follow-up (decision 5): job total with first value; gap guard
  (`100, 110, [gap], 125` -> 25; drop to a lower value counts fully); old
  config keeps `max - min` for jobs.
- On the cluster: a short TPC-C SF1 run with `-nc 2 -rsrp -xnbf 1,4`:
  rep 2 loading CPU and Max RAM close to rep 1, benchmarker round 2 CPU no
  longer equal to round 1; the SUT restart gap measured (see
  "Contradictions"). A second run with several benchmarker jobs per round
  (`experiment_dict`) if one is at hand: rows of a round differ and add up.

### M4: docs

- `docs/Monitoring.md`: why stopped pods linger, `{pods}` and the query sets
  per scope, what the filter does, the threshold and when to raise it
  (scrape interval above ~30 s).
- `docs/Config.md` (placeholders `{pods}`, `{namespace}`) and release notes:
  users update the cAdvisor queries in their `cluster.config` from
  `k8s-cluster.config`; without it nothing warns and the old behaviour
  stays.

## Contradictions to settle before M2 (found 2026-10-18)

- Resolved by "How" (2026-10-18): **jobs by job name vs. decision 2** (the
  job name enters as the `{pods}` placeholder, filled like `{configuration}`,
  no string surgery; decision 2 reworded) and **decision 3's silent check**
  (now checks for `{pods}`).
- Open: **SUT gap after a restart.** Decision 1 assumes the SUT restarts
  ~3.5 min after the old pod stopped; `dev/plan-fewer-kubectl-calls.md` M12
  (resets right after `stop_sut()`) and M11 may have shortened that, and
  with `-ks`/inherited loading the first round follows the new SUT directly.
  Measure in the M3 cluster run; if below 90 s, the SUT needs a lower
  threshold or its own scoping (ReplicaSet hash).

## Rejected alternatives

- **Per-fetch selector rewrite** (scope SUT by ReplicaSet hash, jobs by job
  name, workers by pod UID; write `<connection>-<component_type>.config`
  per fetch): fixes concurrent jobs too, but needs five selector builders,
  string surgery on formatted PromQL, per-fetch files and uploads; fragile.
  The adopted `{pods}` solution keeps only the job-name part, as a template
  placeholder filled once per connection file, with the existing
  `metrics.py -mt` mechanism; SUT and workers keep their patterns.
- **Code-side rewrite of user queries** (option (b)): fixes old copies
  silently, but changes user queries behind their back.

## Risks and open points

- **Scrape interval.** 90 s assumes about 30 s; a cluster scraping every
  60 s needs a higher threshold, and no SUT phase may start within it after
  the previous SUT pod stopped (jobs are scoped by name). Documented,
  editable in the template.
- **Job name drift.** `{pods}` for jobs must equal the manifest's job names;
  built by the same `generate_component_name()`, covered by M3 tests.
- **Missed scrapes > 90 s** make a live pod vanish briefly: gauges dip,
  counters need the guard (decision 5).
- **Users who do not update** their `cluster.config` keep the old behaviour,
  and nothing marks those results (decision 3).
- **Prometheus load.** The filter evaluates each cAdvisor selector twice per
  step (step 1 s), so roughly twice the server work per query; the number
  of queries stays the same. Not timed; the 162 re-run fetches showed no
  problem.
- **Workers on the cluster**: verified on SUT, loader, data generator and
  benchmarker of all storage probes (see "All storage probes"), not on
  worker StatefulSets; M3 needs a distributed run with `-nc 2` (e.g. Citus
  or TiDB with `-nw 3`).
