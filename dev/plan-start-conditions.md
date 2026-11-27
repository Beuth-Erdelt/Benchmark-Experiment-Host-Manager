# Plan: start conditions for benchmarker entries (`start_after`, `start_delay`) at job and pod level

Status: **planned (2026-11-26), not implemented.** Comes out of the discussion of decision 4 in
issue #925 (TPC-DS data maintenance). It is sub-task #0 there: the DM phase becomes an entry in the same
client round that starts after the query streams (`start_after: "tpcds"`), so option (b) of #925 works
and `-ne` keeps its meaning.

Goal: entries of one client round can wait for another entry of the same round to finish, and/or wait a
fixed delay, and each pod of a job can optionally have its own wait on top of that. All waiting happens
inside the pod after the round barrier, before the measurement starts, so measured times contain no
idle time. The existing metrics stay unchanged; the summary makes a staggered start visible.

Related: [plan-reset-scripts](plan-reset-scripts.md) (resets run per entry when it is submitted, which is
unchanged here), issue #925 (TPC-DS DM), multi-benchmark summary (only the primary benchmark drives
`show_summary()`, secondary ones come in through `_show_extra_sections()`).

---

## 1. Decisions (user, 2026-11-26)

| # | Decision |
|---|---|
| D1 | No waiting on the host. bexhoma can't know when a pod has been scheduled, has pulled its image and is running. The only moment all pods of a round share is the round barrier (round counter in Redis reaches 0). Every delay and every dependency is waited for **in the pod script, after the round barrier**. |
| D2 | All entries of a round are still submitted together. The round barrier, the experiment barrier (container tenancy), the start timeout (`BENCHMARK_START_TIMEOUT_MINUTES`) and the main loop's "active jobs" gate stay as they are. |
| D3 | Two levels: job level (entry keys) and an optional pod level (`pod_parameters[i]`). They add up (job condition first, then pod condition) and use different variable names, so the merge in `_pod_configs()` can't run a delay twice. |
| D4 | A pod-level `START_AFTER` names another entry, never a pod of its own job. The job is the unit of evaluation (`time [s]`, throughput, monitoring window), so power and throughput tests belong in separate entries. |
| D5 | Metrics stay as they are. The summary shows the stagger (an offset column per pod, a note at the job). **No** extra metric for the window in which all pods overlap. |
| D6 | Effort is estimated in lines of code, not days. |
| D7 | Every benchmark gets a `#### Per Job` table (between Per Connection and Per Phase), shown when a phase holds more than one job of that evaluator. Per Phase then carries a note pointing to it. |

---

## 2. Background: why this isn't possible today

- [_submit_round()](../bexhoma/experiments/base.py) submits every entry of
  `experiment_dict['benchmarker'][round]` in one loop, with no ordering.
- [_queue_round()](../bexhoma/experiments/base.py) sets one round counter
  `bexhoma-benchmarker-podcount-round-<run>-<client>-<cfg>-<code>` to the summed `parallelism` of all
  entries. Each pod decrements it and waits for ≤ 0 (`images/benchmarker_dbmsbenchmarker/benchmarker.sh`,
  "Wait until all pods of round are ready"). The TPC-H refresh stream relies on this simultaneous start.
- The main loop moves to the next round, or stops the SUT, as soon as a configuration has no jobs left.

The alternative (a) of #925, alternating round types, trips over position-based lookups
(`self.benchmarks[benchmark_run - 1]` in `end_benchmarking()`, `benchmark_run == self.benchmark_run` in
`record_results_complete_test()`) and would change `-ne`.

---

## 3. Configuration

```python
"benchmarker": [[
    {"name": "tpcds", "parallelism": 3, "parameters": {},
     "pod_parameters": [{},                          # stream 1 starts at once
                        {"START_DELAY": "30"},       # stream 2: 30 s later
                        {"START_DELAY": "60"}]},     # stream 3: 60 s later
    {"name": "tpcds_dm", "parallelism": 1, "fixed_parallelism": True,
     "start_after": "tpcds",                         # job level: after all pods of "tpcds"
     "start_delay": 0},
]]
```

| Level | Declared as | Reaches the pod as | Available in |
|---|---|---|---|
| Job | entry keys `start_after` (entry name), `start_delay` (s) | plain env `BEXHOMA_JOB_START_AFTER` (full Redis key), `BEXHOMA_JOB_START_DELAY` | every template, including the `tpch_refresh` loaders |
| Pod | `pod_parameters[i]` keys `START_AFTER` (entry name), `START_DELAY` (s) | `BEXHOMA_POD_START_AFTER`, `BEXHOMA_POD_START_DELAY` through the Redis per-pod config | the 5 scripts that read the per-pod config: `benchmarker_dbmsbenchmarker`, `ycsb`, `hammerdb`, `benchbase`, `hardware` |
| Predecessor | — (set by the host when something depends on the entry) | plain env `BEXHOMA_JOB_DONE_KEY` | every template |

The per-pod config mechanism that is reused: `_pod_configs()` (`bexhoma/configurations/base.py`) merges
`parameters` with `pod_parameters[i-1]` into `bexhoma-benchmarker-<connection>-<code>-config-<i>`,
written as `json.dumps` with the job counter in one `MSET` (`BenchmarkRunner.run_pod()`). The pod script
turns each key into `BEXHOMA_POD_<KEY>` with a `tr`/`awk` pipeline.

References use a separate entry key `id`, not `name`. The entry `name` names the benchmark type that
owns the entry: `is_own_benchmark()` matches it against the evaluator's name, so two YCSB entries with
different parameters in one round must both be called `"ycsb"`. `id` is optional and defaults to `name`,
so `start_after: "tpcds"` works without it:

```python
{"name": "ycsb", "id": "ycsb-warmup", "parallelism": 4, "parameters": {"YCSB_WORKLOAD": "a"}},
{"name": "ycsb", "id": "ycsb-main",   "parallelism": 8, "parameters": {"YCSB_WORKLOAD": "b"},
 "start_after": "ycsb-warmup"},
```

The done-counter key uses the resolved position (`benchmark_run`), so `id` is only needed at validation
and resolution time.

Semantics:
- `start_after`: start when every pod of the entry with that `id` **in the same client round and
  repetition** has finished successfully (or its job has ended, see the safety net).
- `start_delay`: seconds, counted from the moment the `start_after` condition is met, or from the round
  barrier when there is none.
- Order in the pod: round barrier → experiment barrier (container tenancy) → job condition → pod
  condition → measurement starts.
- If the predecessor fails, the dependent entry still runs (the failure is recorded as usual). A
  "skip if the predecessor failed" option can follow if needed (section 8).
- `-ne`: the conditions are copied into every round together with the entry. `pod_parameters` has a
  fixed length; pods beyond the list get no pod-level condition (as with the existing mechanism).

---

## 4. Mechanism

### Done-counter
- Key: `bexhoma-benchmarker-done-<experiment_run>-<client>-<benchmark_run>-<configuration>-<code>`,
  where `benchmark_run` is the predecessor's position in the round.
- Created by the host in `_queue_round()` together with the round counter, before any job is submitted,
  with the value `parallelism` of the predecessor. Only for entries that something depends on, at job or
  pod level.
- Each predecessor pod runs `redis-cli decr $BEXHOMA_JOB_DONE_KEY` **only after it has finished
  successfully**, after `BEXHOMA_END`. Not in an exit `trap`: a failed attempt that Kubernetes retries
  would otherwise count twice and release the counter while the retry is still running.
- **Safety net:** when `_end_finished_jobs()` ends the predecessor's job, whether it succeeded or reached
  the terminal `Failed` state, the host sets the counter to 0. A pod killed by OOM or eviction never
  decrements; without this the dependent pod would wait forever. The host keeps a map job name → done key
  from the submission. A round deleted by `_skip_benchmark_round_if_not_started()` zeroes its counters too.

### Per-round values are not stored in `experiment_dict`
The keys contain `experiment_run` and `client`, so they must not be written into the persisted
`experiment_dict` (it is reused for `-nc` repetitions and read back by the evaluators). The host builds
them per submission and hands them to `run_pod()` as a new argument `extra_parameters`, merged into both
the container env and the per-pod configs. Pod-level `START_AFTER` names are rewritten to keys in a copy
of `pod_parameters`.

### Pod script block

```bash
wait_for_start() {   # $1 = done-counter key (optional), $2 = delay in s (optional), $3 = label
    if [ -n "$1" ]; then
        echo "Waiting ($3) for $1"
        while : ; do
            N="$(redis-cli -h 'bexhoma-messagequeue' get "$1")"
            [[ "$N" =~ ^-?[0-9]+$ ]] && test "$N" -le 0 && break
            sleep 1
        done
    fi
    if test "${2:-0}" -gt 0; then echo "Delay ($3) $2 s"; sleep "$2"; fi
}
# ... round barrier (and experiment barrier) as today ...
echo "BEXHOMA_ROUND_READY:$(date -u +%s)"
wait_for_start "$BEXHOMA_JOB_START_AFTER" "$BEXHOMA_JOB_START_DELAY" job
wait_for_start "$BEXHOMA_POD_START_AFTER" "$BEXHOMA_POD_START_DELAY" pod
######################## Start measurement of time ########################
# ... benchmark ...
# after BEXHOMA_END, only on success:
if [ -n "$BEXHOMA_JOB_DONE_KEY" ]; then redis-cli -h 'bexhoma-messagequeue' decr "$BEXHOMA_JOB_DONE_KEY"; fi
```

The `tpch_refresh` loaders don't read the per-pod config, so they get the job-level wait only (they run
with `fixed_parallelism` 1 anyway).

### Parser fix
The `awk` parser for the per-pod config only exports values in quotes (`NF>=4`). `json.dumps` writes
numbers without quotes, so `{"START_DELAY": 30}` is dropped silently. This already affects any numeric
`pod_parameters` value today. Fix the parser in the 5 scripts to accept unquoted numbers as well; the
host also converts `START_DELAY` to a string, so old images still work.

### Validation (host, when the experiment dict is built)
Over one graph per round, where both a job-level `start_after` and a pod-level `START_AFTER` on entry A
naming B are an edge A → B:
- the referenced `id` exists in the same round,
- an `id` that is referenced is unique within its round (otherwise the error lists the matching
  positions); entries that nobody references may share an `id`, e.g. two `"ycsb"` entries,
- no self-dependency (at pod level that would be a pod waiting for a counter it is part of, so its job
  never finishes),
- no cycles,
- delays are integers ≥ 0,
- a warning when `pod_parameters` is longer than the smallest `parallelism` of the entry over all rounds.

---

## 5. Summary

Metrics are unchanged (D5). What the evaluators do today when pods start staggered:

| Evaluator | Measured | Pods combined as | Effect of a stagger on the metric | Time series |
|---|---|---|---|---|
| DBMSBenchmarker | client side, per query | `time [s]` = latest end − earliest start, `Throughput@Size` = executions × 3600 / `time [s]` × SF | drops: the idle time before late pods start counts toward the span | — |
| YCSB | client side | sum of the pods' own rates, max of the pods' own runtimes | stagger hidden; the sum can overstate the load carried at once | indexed by `sec` since each pod's own start, then summed: misaligned |
| Benchbase | client side | sum of the pods' own rates (`Throughput`, `Goodput`) | as YCSB | indexed by seconds since each pod's first measurement, then summed: misaligned |
| HammerDB | **server side** (DBMS transaction counter) | mean | stays a true server throughput, includes the ramp-up | each pod records the same server curve, shifted by its own start; the mean blurs it |

Changes:
1. **Offset column per pod:** `BEXHOMA_START − BEXHOMA_ROUND_READY`, parsed from the stored pod logs, in
   the per-connection tables of all evaluators (shared code in the base evaluator).
2. **Note at the job when the offsets differ**, worded per evaluator:
   - DBMSBenchmarker: "pods start staggered by up to N s; `time [s]` and `Throughput@Size` include the
     ramp-up."
   - YCSB, Benchbase: "pods start staggered by up to N s; throughput is the sum of each pod's own rate and
     assumes the pods ran at the same time."
   - HammerDB: "pods start staggered by up to N s; NOPM/TPM are server-side and include the ramp-up."
3. **Time series aligned by absolute time** in YCSB, Benchbase and HammerDB: index by
   `timestamp − earliest timestamp over the job's pods` instead of seconds since each pod's own start.
   All three parsers already read the absolute timestamp of each line (YCSB `date_time`, Benchbase and
   HammerDB `dt`), so no image change is needed. For HammerDB the copies then match, and the mean is the
   server's actual curve.
4. **DM / dependent entries:** the section of the dependent benchmark (like `RefreshStreamBenchmark`)
   shows begin, end, duration and the offset.
5. **Ordering test** in `record_tests`: each dependent job's begin ≥ its predecessor's end.
6. **Per Job table (D7).** All 5 evaluators (DBMSBenchmarker, YCSB, Benchbase, HammerDB, hardware) build
   `#### Per Phase` by grouping on `phase`, so several jobs of one evaluator in a round become one row.
   That already happens today for two same-type entries running side by side; with `start_after` the
   phase row combines jobs that never ran together:
   - DBMSBenchmarker: `time [s]` is the max over the jobs and executions are summed, so
     `Throughput@Size` is overstated.
   - YCSB, Benchbase: the rates of all jobs are summed; latencies are averaged or maxed over different
     workloads.
   - HammerDB: NOPM/TPM are averaged over windows that don't overlap.

   Every evaluator's aggregation already supports `columns=['job']`; no summary uses it yet. Changes:
   - `evaluators/logger.py`: `IDENTITY_PER_JOB = ('phase', 'job', 'experiment_run', 'client',
     'benchmark_run', 'pod_count')` and `get_summary_benchmark_per_job()`.
   - Each evaluator's `get_summary_benchmark_per_phase()` becomes a shared builder that takes the grouping
     as a parameter (`['phase']` or `['job']`, plus `tenant_id` with tenants), used by both tables.
   - `Benchmark._results_sections()` adds `#### Per Job` when some phase has more than one job of the
     evaluator, so stdout and the Markdown report both get it, plus a note at Per Phase: "several jobs in
     this phase; see Per Job".
   - `record_tests` keeps working on Per Phase (`df_reduced`); the report's column glossary
     (`report_writer.py`) gets the Per Job table.

Unaffected: query sections (evaluators select their connections by entry name through
`is_own_benchmark()`), the workflow planned/actual check (structure only), and monitoring windows (taken
from `BEXHOMA_START`/`BEXHOMA_END`, which come after the wait).

---

## 6. Milestones

| # | Piece | Where | LOC |
|---|---|---|---|
| M1 | Entry keys `id`, `start_after` / `start_delay`, pod keys `START_AFTER` / `START_DELAY`; validation (section 4); YAML experiment schema | `configurations/base.py`, `experiment.py` schema | ~75 |
| M2 | Done-counters in `_queue_round()`; `extra_parameters` for `run_pod()` (env and per-pod configs); name → key rewrite for pod level; job → done key map; safety net in `_end_finished_jobs()` and the skip path | `experiments/base.py`, `configurations/benchmarking.py` | ~55 |
| M3 | Pod scripts: `wait_for_start()`, two calls, `BEXHOMA_ROUND_READY`, decrement on success, in the 5 benchmarker scripts and the 8 `tpch_refresh` loaders (job level only there); the TPC-DS DM loaders get it when they are written | `images/*` (13 scripts), then rebuild the images | ~20 × 13 ≈ 260 |
| M4 | `awk` parser fix for unquoted numbers | 5 benchmarker scripts | ~3 × 5 ≈ 15 |
| M5 | Offset column per pod; stagger note per evaluator; ordering test | `evaluators/base.py`, the 4 evaluators | ~50 |
| M6 | Time series aligned by absolute time | YCSB, Benchbase, HammerDB evaluators | ~10 × 3 ≈ 30 |
| M6b | Per Job table (D7): `IDENTITY_PER_JOB`, `get_summary_benchmark_per_job()`, per-phase builders parameterised by grouping, section and note in `_results_sections()`, glossary | `evaluators/logger.py`, 5 evaluators, `benchmarks/base.py`, `report_writer.py` | ~25 + 5 × 10 + 15 ≈ 90 |
| M7 | Unit tests: validation (unknown `id`, ambiguous `id`, self-dependency, cycles at both levels), keys and env per round, merge without a double delay, safety net, offset parsing, time-series alignment, ordering test, Per Job table (shown only with several jobs per phase, one row per job, per evaluator) | `tests/` | ~410 |
| M8 | Docs: `bexhoma/experiments/README.md` (experiment dict keys), `docs/` page section; a `scripts/test-docs-*` entry, written in `.ps1` first and synced to `.sh` | | ~80 |
| M9 | Live check on the cluster (started by the user): e.g. TPC-H with the refresh stream and `start_after: "tpch"`, and YCSB with `pod_parameters` delays 0/30/60 | | — |

Total: about 145 lines of Python in bexhoma, about 170 lines in the evaluators and the summary, about
275 lines of shell (mostly the same block copied 13 times), about 410 lines of tests and about 80 lines
of docs.

M6b (Per Job) doesn't depend on the start conditions: it fixes a summary that is already misleading for
two same-type entries in one round, and can land first.

If the images shared one snippet file for the barrier and the wait, M3 would shrink to about 25 lines
plus 13 `source` calls. Out of scope here; the barrier block is copied into 34 scripts today.

---

## 7. Use in #925 (TPC-DS data maintenance)

`enable_data_maintenance()` in `bexhoma/benchmarks/tpcds/experiment.py` adds, next to the `tpcds` entry
of every round:

```python
{"name": "tpcds_dm", "benchmarker": "tpcds_maintenance", "template": "",
 "parallelism": 1, "num_pods": 1, "fixed_parallelism": True,
 "start_after": "tpcds", "target": "sut", "parameters": {}}
```

The DM job's measured time starts when every query stream of the round has finished, which is the end of
the spec's throughput test. The DM benchmark class reports begin, end, duration, offset and the
per-function times.

---

## 8. Open points

- Looking up evaluators by entry name in `end_benchmarking()` / `end_loading()` /
  `record_results_complete_test()` (`self.evaluators[name]` instead of `self.benchmarks[benchmark_run - 1]`)
  is **not** needed here: start conditions keep the same layout in every round, so positions stay
  correct. It matters only for rounds with different layouts; a separate robustness fix (~15 LOC).

- Skip the dependent entry if its predecessor failed (host sets a `...-failed` key instead of 0, and the
  pod exits with a marker in its log)? Default for now: run anyway.
- Should a dependent pod's waiting time be capped (fail after N minutes)? With the safety net the wait
  ends when the predecessor job ends; a predecessor that hangs forever already blocks the round today.
- How Benchbase and HammerDB templates name their containers: the offset parsing assumes the stored pod
  logs contain `BEXHOMA_ROUND_READY` and `BEXHOMA_START`; check every template once in M5.
