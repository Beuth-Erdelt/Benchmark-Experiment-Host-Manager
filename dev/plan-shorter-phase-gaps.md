# Plan: shorter gaps between loading and benchmarking, and between rounds

Status: plan only, written 2026-10-19. Nothing implemented.

Builds on [plan-fewer-kubectl-calls.md](plan-fewer-kubectl-calls.md) (M11
follow-up wait, M4 more fetches at once, M6 parallel submit/end: done) and
takes up its optional O1 (metric tail), O2 (wake on change) and O3 (background
fetches), which this plan orders and measures against.

## Goal

The SUT should sit idle as briefly as possible between the end of loading and
the first benchmark round, and between two rounds. More importantly, that
idle time should be **controlled**: chosen by the user and the same in every
run, not a random result of polling and loop timing (see "Negative impact").

## Measured today

From the logs in `dev/` (script: parse `benchmarker timespan pods`,
`benchmarker timespan job` and `total times` of the loader; times in seconds):

| Run | Tenants | loading end -> round 1 | round k -> round k+1 | pods end -> `end_benchmarking()` |
|---|---|---|---|---|
| `logs_pod_scope/tpcc_postgresql_m3.log` | 1 | 69-82 | 48-69 | 22 |
| `logs_fewer_calls/tenancy_2.log` | 2 | 117-147 | 91-106 (median 94) | 20-68 (median 30) |
| `logs_fewer_calls/tenancy_8_m6.log` | 8 | 240-319 (median 280) | 119-121 | 39-48 |
| YCSB CockroachDB / Citus / YugabyteDB (1 round) | 1 | 139-317 | - | - |

### Round k -> round k+1, 8 tenants (`tenancy_8_m6.log`, 120 s)

| Part | Time | Where |
|---|---|---|
| job pods end -> pass notices it | 0-30 s poll + pass time | `self.wait(intervals_wait)`, 30 s |
| end 8 jobs: store pod logs, describe, delete, `end_benchmarking()`, `check_volumes()` | 22-29 s | `_end_finished_jobs()` [base.py:2133](../bexhoma/experiments/base.py#L2133) |
| fetch benchmarking metrics (16 sets, 8 at once) | 19-22 s | `end_batch.run()` [base.py:2698](../bexhoma/experiments/base.py#L2698) |
| wait to next pass | 0 s | M11 |
| next pass up to submission, `run_pod()` x 8 | about 15 s | `_submit_round()` [base.py:2065](../bexhoma/experiments/base.py#L2065) |
| job pods scheduled, started, Redis barrier | about 20-30 s | outside bexhoma |

With 1 tenant the same parts are smaller (fetch 8 s, submission 8 s, gap 48-69 s).

### Loading end -> round 1

1 tenant (`tpcc_postgresql_m3.log`, 82 s): loader ends -> noticed (0-30 s +
pass) -> index scripts started in a thread (pass 28 s) -> **full 30 s wait,
although the index took a few seconds** -> next pass submits (15 s) -> pods
start.

8 tenants, one container per tenant: all tenants wait for each other on
purpose (`tenant_per == 'container'`), so the median 280 s mostly comes from
the last tenant's loader. On top of that, the index scripts of all 8
tenants are started **one after the other in a single pass (150 s, 64
kubectl calls)** [base.py:2455-2468](../bexhoma/experiments/base.py#L2455),
then a 30 s wait, then submission (35 s).

The loading metric fetch is **not** in the way: it is queued while round 1 is
submitted and runs afterwards ([base.py:2680-2681](../bexhoma/experiments/base.py#L2680)).

## Steps

Sorted by gain per risk. Each step lists its gain, risk and negative impact.

### G0 - measure the gaps in every run (do first)

Print wall-clock time on `Loop pass` lines. Write the idle times per
configuration (loading end -> round 1, round k -> k+1, pods end -> noticed,
submitted -> pods start) into the result folder, e.g. as
`bexhoma-gaps-{code}.json`, and show them in `index.md`'s Health Summary or
`timing.md`.

- Gain: no speed-up itself. Every later step can be checked, and runs say how
  long the SUT was idle (needed for comparability, see G8).
- Risk: low. Only new output.
- Negative impact: one more result file.

### G1 - fetch round k's metrics after round k+1 is submitted

Keep the `end_batch` of a pass and run it in the **next** pass, after that
pass's submissions, the way `submit_batch` already works. Before
`stop_sut()` and at the end of the loop, run any batch still pending.

- Gain: fetch time leaves the gap: 8 s (1 tenant) to 19-22 s (8 tenants) per
  round.
- Risk: low.
  - The per-configuration Prometheus ([lifecycle.py:1578](../bexhoma/configurations/lifecycle.py#L1578)) exists at least until
    `stop_sut()`, which never runs in the same pass as the job end.
  - `connections.config` / `<connection>.config` are uploaded before the
    fetch (M13 order): keep `_upload_ended_job_files()` where it is.
  - If bexhoma dies, at most one pass of fetches is lost. Abort paths
    (`-xt`, loading abort, exceptions) must run the pending batch in a
    `finally`.
- Negative impact:
  - Round k's metrics are fetched while round k+1 runs, so Prometheus and the
    dashboard pod (`metrics.py`, pandas) work during a measurement. Check
    that the dashboard pod is not on a SUT or benchmarker node.
  - The fetch log of round k ends up in the log next to round k+1's
    submission, which is harder to read.
  - Side benefit: the fetch runs later, so the metric tail (O1) is more
    complete.

### G2 - async loading/index scripts wake the loop

The script threads (`load_data_asynch`, [loading.py:25](../bexhoma/configurations/loading.py#L25))
set `cfg.loading_finished` and then the loop sleeps the full 30 s. Instead,
give the experiment a `threading.Event` that the thread sets when it ends,
and have `self.wait()` return early when it is set.

- Gain: up to 30 s per repetition for loading -> round 1 (index finished
  in a few seconds, the loop waited 30 s).
- Risk: low. Pass logic unchanged; only the wait ends earlier. The
  `MAX_FOLLOW_UP_WAITS_IN_A_ROW` guard keeps a misbehaving thread from
  causing a tight loop.
- Negative impact: the SUT gets less quiet time after the index build
  (autovacuum/analyze, checkpoints of the load). That time was never
  controlled; G8 makes it explicit.

### G3 - start the index scripts of all tenants side by side

In container tenancy, `load_data(script_type='index')` runs for each tenant
one after the other in one pass (150 s for 8 tenants). Run them through
`_run_parallel_steps()` like the round submissions (M6).

- Gain: about 100-130 s per repetition with 8 tenants; nothing with 1.
- Risk: medium. Same thread-safety questions M6 answered for submissions:
  shared `connections.config`, PVC labels, `CALL_STATS`, prints. Reuse the M6
  locks.
- Negative impact: 8 index builds start at the same time on the same node
  and storage (that is the tenancy setup), so the index phase can get slower
  per tenant. Loading time per tenant changes; it is in the results
  (`time_index`).

### G4 - finish the job end after the next submission

Of what `_end_finished_jobs()` does, only reading the timing
(`get_job_timing_benchmarking`) and marking the job as ended must happen
before the next round. Storing pod logs, the describe, deleting pods and the
job, and `check_volumes()` can run after the next submission, like G1.

- Gain: most of 22-29 s (8 tenants), a few seconds with 1 tenant.
- Risk: medium.
  - Pod logs must be stored before the pods are deleted, so keep them until
    then (the job stays listed; `_ended_jobs()` already makes listed ended
    jobs harmless).
  - `check_volumes()` runs at job end ([base.py:2180](../bexhoma/experiments/base.py#L2180)) and at submission
    ([benchmarking.py:157](../bexhoma/configurations/benchmarking.py#L157)). Check whether one of them is enough.
  - The next round's pod counters (Redis) and the old job's pods must not
    get mixed up. Job names are unique per round, so this should hold, but
    test it.
- Negative impact:
  - Old job pods (Completed) stay up to one pass longer. They hold no CPU
    but count toward namespace quotas, if any.
  - The size measured after round k is now taken while round k+1 runs; the
    value can include round k+1's first writes. Measure before submission if
    the size per round matters (it is shown per round today).

### G5 - submit the next round in the same pass that ends the job

Today a pass first submits, then ends jobs; a job ended in pass P is followed
up in pass P+1 (0 s wait, but the start of a full pass). Run the submission
step again for configurations whose job ended in this pass, or put the end
section before the submit section.

- Gain: the start of one pass (about 2-15 s, more with many tenants).
- Risk: **high**. The submit section also decides "can be stopped",
  `stop_sut()`, repetitions, `-ms` slots and skipped rounds; it relies on
  ended jobs being gone from the cluster lists. Reordering touches every one
  of these paths. Only worth it after G0-G4, if the measured remainder still
  justifies it.
- Negative impact: none on results beyond a shorter gap; the risk is to
  correctness of the loop.

### G6 - wake on job end (O2 of the earlier plan)

Let the wait end when a benchmarker job completes, instead of polling every
30 s (list jobs every 5 s, or a watch).

- Gain: detection 0-30 s -> 0-5 s; also makes the gap much less random.
- Risk: medium.
  - More API calls (2-3 list calls per 5 s per experiment).
  - During cluster outages a check can block like a pass does today.
  - With an early detection the fetch would cut the metric tail. G1 or O3
    (fetch only when `now >= time_end + extend + 2 x scrape interval`) is
    required first.
- Negative impact: more load on the API server for the whole run, also for
  parallel experiments.

### G7 - background fetches (O3 of the earlier plan)

The fetch queue runs in its own thread pool and no pass waits for it.
Barriers: before `stop_sut()` while the per-configuration Prometheus exists,
before `evaluate_results()`, and in abort paths.

- Gain over G1: other tenants are served while fetches run. With 1 tenant,
  nothing over G1.
- Risk: medium-high. Concurrent writes to `connections.config` in the
  dashboard pod (today serialised by the batch), uploads racing with fetches,
  errors surfacing late. After the per-configuration Prometheus is
  deprecated, the `stop_sut()` barrier goes.
- Negative impact: same as G1, but metric work is spread over the whole run
  instead of between rounds, so it overlaps measurements more often.

### G8 - controlled pause (recommended alongside G1-G6)

Add `--round-pause SECONDS` (and/or a pause after loading): the next round is
submitted no earlier than `SECONDS` after the previous round's pods ended.
Default to today's typical gap or 0, as decided (see "Open questions").

- Gain: no speed-up. It makes the idle time a parameter instead of a side
  effect of bexhoma's speed, so faster bexhoma versions do not change
  results.
- Risk: low.
- Negative impact: a non-zero default keeps runs as long as today.

### Not planned: start the next round's pods early

Submit round k+1 shortly before round k ends; its pods start and wait on a
Redis key that the last pod of round k sets. This would take bexhoma out of
the critical path entirely (gap = a few seconds).
Not planned because:
- JVM start of BenchBase/YCSB clients and pod scheduling would overlap round
  k's measurement.
- Reset scripts and per-round parameter changes need the gap.
- A failed round k must stop round k+1.
- Timeouts (`BENCHMARK_START_TIMEOUT_MINUTES`, round skip) would need
  rework.

## Risks and negative impact (all steps)

- **Results change; runs before and after are not directly comparable.**
  DBMS do background work between rounds and after loading: checkpoints,
  autovacuum/analyze, compaction, cache flush, replication catch-up. With a
  shorter gap this work overlaps the next round: lower throughput or higher
  latency at the start of round k+1, different steady state. The earlier
  plan already saw TPC-C about 10% lower after M11/M14 (not yet separated
  from cluster noise). Mention in release notes; G0 records the gap, G8
  makes it a parameter.
- **The gap stays random without G6/G8.** Even after G1-G4, the 0-30 s
  detection delay remains, so the idle time varies per round and tenant.
  Shorter but random is not better for comparisons than longer but random.
- **Metric work during measurement (G1, G7).** Prometheus queries and
  `metrics.py` run while the next round measures. Harmless only if the
  dashboard pod and Prometheus are not on SUT/benchmarker nodes.
- **Metric tail.** Fetching earlier (G6 without G1/O3) cuts the last
  scrapes; fetching later (G1, G7) improves it. Order of steps matters.
- **Lost metrics on crash.** Every deferred fetch is lost if bexhoma dies
  before it runs: one pass with G1, more with G7. Abort paths must flush.
- **Per-configuration Prometheus.** Deleted by `stop_sut()`; any deferral
  needs a barrier before it until that component is deprecated.
- **Tenancy.** G3 runs 8 index builds at once (slower per tenant). With G4/G5
  tenants may start rounds at slightly different times when jobs end in
  different passes; container tenancy keeps its Redis barrier, other
  tenancy modes do not have one.
- **Complexity and debugging.** Out-of-order log lines (fetch of round k
  after submission of k+1), late-reported fetch errors, more threads. G5 and
  G7 change the loop's structure; regressions there have hit before
  (`-ms` gap, keep-SUT KeyError).
- **Cluster load.** G6 adds API calls for the whole run; G3 adds parallel
  exec calls.

## Expected

| | today, 1 tenant | after G1, G2, G4 | + G6 | today, 8 tenants | after G1-G4 | + G6 |
|---|---|---|---|---|---|---|
| round k -> k+1 | 48-69 s | about 35-55 s | about 25-30 s | about 120 s | about 70 s | about 45-50 s |
| loading end -> round 1 | 69-82 s | about 40-50 s | about 30 s | 240-319 s | about 110-190 s | about 90-170 s |

Rest: pod start and Redis barrier (20-30 s), `run_pod()` submission (8-15 s).
These are estimates from one log each; G0 will confirm them.

## Tests

- G1: an ended job's fetch is queued, runs after the next pass's
  submissions; a pending batch runs before `stop_sut()`, at loop end, and in
  abort paths (mocked fetches, assert order).
- G2: `wait()` returns early when the event is set; a set event without a
  state change does not loop more than `MAX_FOLLOW_UP_WAITS_IN_A_ROW`.
- G3: index scripts of all tenants are started once each, in parallel; a
  failing tenant marks only itself as finished/failed, as today.
- G4: pods are stored before deletion; an ended job still listed is not
  ended twice; next round's counters unaffected.
- G8: next submission not before `end + pause`.

## Cluster check

Same as the earlier plan: `tenancy_8` and `tpcc_postgresql` (1 tenant, 2
rounds, `-nc 2`). Compare G0's gap numbers before/after, result file counts,
missing metrics (no new gaps), metric tail (last CSV timestamp vs
`time_end + extend`), and throughput per round with and without G8 pause.

## Order

1. G0 (measure), G8 (pause parameter) - small, make the rest checkable.
2. G1, G2 - low risk, clear gain.
3. G4, then G3 if container tenancy matters.
4. Cluster check.
5. G6 only if the detection delay dominates; needs G1.
6. G5, G7 only if still needed; G7 better after the per-configuration
   Prometheus is deprecated.

## Open questions

- Default of G8: 0 (fastest) or a fixed pause such as 30 s (comparable to
  most runs so far)?
- Is the per-round DB size (G4, `check_volumes()`) used anywhere that needs
  it before the next round?
- Is the dashboard pod pinned away from SUT/benchmarker nodes on the cluster?
