# Plan: monitoring metrics must not count pods of earlier phases

Status: M1 **implemented** (2026-10-15, uncommitted). M2-M4 **planned**:
filter stale series in the `cluster.config` templates (decided 2026-10-15,
option (a): template change plus a warning, no code-side query rewriting).

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

## How metrics flow (unchanged by this plan)

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

## Decisions for M2-M4

1. **Drop stale series in the query.** Every cAdvisor instant selector `X`
   in the templates becomes
   `(X and (time() - timestamp(X)) < 90)`. `timestamp()` returns the time
   of the sample the query uses; a live pod's newest sample is at most one
   scrape interval old (28-32 s on this cluster), a stopped pod's keeps
   ageing and drops out after 90 s instead of 5 min. Phases start at least
   ~160 s after the previous pod stopped (rounds), ~3.5 min after a restart.
   Tested on 1792023056 rep 2 loading (see "Evidence").
2. **Option (a): change the shipped template, do not rewrite queries in
   code.** `k8s-cluster.config` gets the filter in the 11 cAdvisor
   instant-selector templates. The 3 templates inside `irate(...[5m])` stay
   unchanged (rate 0 for a stale series). Users copy the new queries into
   their own `cluster.config` (git-ignored). The threshold is a literal `90`
   in the query: visible, and changed by editing the template.
3. **Old copies are detected, not changed.** At experiment start bexhoma
   checks the active `monitor.metrics` templates: a query using a
   `container_*` metric outside `rate`/`irate` and without `timestamp(` is
   reported once ("N cAdvisor metrics do not drop stopped pods' series; see
   k8s-cluster.config"), in the workload info and as a failed test in the
   summary and report, so results from an unfixed config say so.
4. **Namespace filter.** The same 14 cAdvisor templates get
   `namespace="{namespace}"`; the formatting calls supply `namespace`.
   An old template without `{namespace}` keeps working (unused keyword).
5. **Counters after the filter (follow-up to M1).** With stale series gone,
   a job's series contains only its own pods. Then:
   - jobs: total = positive steps + first value (their pods start inside the
     window, so the first value is growth from 0; removes the round-1
     undercount of `max - min`, e.g. 151 vs ~167);
   - guard: an upward jump right after a drop is not counted. Missed scrapes
     longer than 90 s (Prometheus or kubelet restart) would drop a live pod
     for a moment; its reappearance must not count its whole counter again.
   Only switched on when decision 3 finds the filter in place; with an old
   config the jobs keep `max - min`.
6. **Concurrent jobs: out of scope for now.** If needed later, scope only
   the benchmarker by its job name
   (`bexhoma-benchmarker-{configuration}-{experiment}-{run}-{client}-{benchmark_run}-`).

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

Other checks:
- DBMS-Benchmarker's container swap (`str.replace`) and the worker
  `container="dbms"` stripping (`set_metric_of_config`) replace every
  occurrence, so the selector may appear twice.
- `pod-template-hash` and pod UIDs (cAdvisor `id` =
  `/kubepods/<qos>/pod<uid>/<container>`) exist, but are not needed any more.
- The per-stream metrics of DBMS-Benchmarker jobs (`-mps`) use the same
  templates and are covered by the filter; bexhoma does not read them.

## Implementation sketch

### M2: templates and detection

- `k8s-cluster.config`: the 11 instant-selector cAdvisor templates get the
  filter (decision 1) and all 14 the namespace label (decision 4). Keep the
  query shapes as they are (`sum(...)`, `sum(max(...) by (instance))`,
  `sum(max by (pod) (...))`); wrap only the selector.
- `configurations/base.py`: `set_metric_of_config_default` and every branch
  of `set_metric_of_config` pass `namespace=`; check other places that
  format these templates (`environment.py`, hardware baseline).
- Detection (decision 3): a function over `monitor.metrics` returning the
  keys without the filter; called once in `prepare_testbed` when monitoring
  is on; workload info line and a runtime test result.

### M3: tests

- Every cAdvisor instant template in `k8s-cluster.config` has the filter and
  `namespace="{namespace}"`; the `irate` ones are unchanged; all still
  format (no unknown placeholder) and parse as PromQL-shaped strings.
- Detection: an old-style template is reported, the new one is not, rates
  are never reported.
- M1 follow-up (decision 5): job total with first value; reappearance guard;
  old config keeps `max - min` for jobs.
- On the cluster: a short TPC-C SF1 run with `-nc 2 -rsrp -xnbf 1,4`:
  rep 2 loading CPU and Max RAM close to rep 1, benchmarker round 2 CPU no
  longer equal to round 1.

### M4: docs

- `docs/Monitoring.md`: why stopped pods linger, what the filter does, the
  threshold and when to raise it (scrape interval above ~30 s), the warning.
- `docs/Config.md` and release notes: users update the cAdvisor queries in
  their `cluster.config` from `k8s-cluster.config`.
- Result contract: the new test line (additive).

## Rejected alternatives

- **Per-fetch selector rewrite** (scope SUT by ReplicaSet hash, jobs by job
  name, workers by pod UID; write `<connection>-<component_type>.config`
  per fetch): fixes concurrent jobs too, but needs five selector builders,
  string surgery on formatted PromQL, per-fetch files and uploads; fragile.
- **Code-side rewrite of user queries** (option (b)): fixes old copies
  silently, but changes user queries behind their back.

## Risks and open points

- **Scrape interval.** 90 s assumes about 30 s; a cluster scraping every
  60 s needs a higher threshold, and no phase may start within it after the
  previous pod stopped. Documented, editable in the template.
- **Missed scrapes > 90 s** make a live pod vanish briefly: gauges dip,
  counters need the guard (decision 5).
- **Users who do not update** their `cluster.config` keep the old behaviour;
  the warning (decision 3) makes those results recognisable.
- **Workers on the cluster**: verified on SUT, loader, data generator and
  benchmarker of all storage probes (see "All storage probes"), not on
  worker StatefulSets; M3 needs a distributed run with `-nc 2` (e.g. Citus
  or TiDB with `-nw 3`).
