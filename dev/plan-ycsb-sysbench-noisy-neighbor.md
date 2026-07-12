# Plan: sysbench as a co-located "noisy neighbor" for YCSB

Status: **not implemented, held as a plan**. No code has been written for this yet.

## Goal

Run sysbench (via the existing `HARDWARE_TYPE=sysbench` Hardware benchmark) as a
second job co-located on the same Kubernetes node as a YCSB experiment's SUT pod,
to measure how YCSB throughput/latency degrades under CPU/memory contention from a
noisy neighbor.

## Precedent this plan follows

The TPC-H refresh stream is the existing example of "a second benchmarker job runs
in parallel with the primary one, within the same client round":
`bexhoma/benchmarks/refresh.py::RefreshStreamBenchmark` +
`bexhoma/experiments/tpch.py::enable_refresh_stream()`/`show_summary()`.

## Already generic — confirmed, no changes needed

- **Job submission** (`experiments/base.py:1738-1755`, `work_benchmark_list()`):
  iterates every entry in a round's list and calls `run_pod()` without branching on
  `entry["benchmarker"]`. Mixing a `"ycsb"` entry and a `"hardware"` entry in one
  round already works today, the same way `tpch_refresh` does.
- **Redis sync counters**: the round counter (`experiments/base.py:1719-1723`) sums
  `parallelism` across *all* entries in the round automatically — a new sysbench
  entry joins it for free. The experiment-level counter only activates for
  `tenant_per == 'container'`, which this feature doesn't need.
- **True node co-location**: already exists via `-rnn`/`-rnb`
  (`cli_args.py:68,70`) → `experiments/base.py:552-568` sets
  `nodeSelector['kubernetes.io/hostname']` on the SUT deployment *and*, via
  `cfg.benchmarking_patch`, on **every** benchmarker job in a round
  (`manifest.py:470`). This is a real single-node pin — stronger than the
  pool-type selector that `-mtb container` tenancy relies on today. Running
  `ycsb.py run ... -rnn <hostname>` would already pin the YCSB SUT and the
  sysbench job onto the same node once the sysbench entry exists. No new
  placement code needed.
- **Log/evaluator isolation**: `transform_all_logs_benchmarking()` already filters
  pod logs by `-{benchmark_run}` suffix, so a `HardwareEvaluator` scoped to
  `benchmark_run=2` only sees the sysbench pod's logs, never YCSB's.
- **k8s job template**: `jobtemplate-benchmarking-hardware.yml` already exists and
  (being usable today by `HardwareExperiment`) should already name its main
  container `dbmsbenchmarker`, satisfying `get_job_timing_benchmarking()`'s
  hardcoded container-name requirement.

## Net-new work

1. **`bexhoma/benchmarks/noisy_neighbor.py`** — new `NoisyNeighborBenchmark(Benchmark)`,
   modeled on `RefreshStreamBenchmark` but *not* a bare-timing clone:
   - `create_evaluator()` → `evaluators.hardware(code, path, include_loading=False,
     include_benchmarking=True, benchmark_run=benchmark_run)` — reuses the
     narrow-schema `HardwareEvaluator` (each `HARDWARE_TYPE` now only carries its own
     columns, see `bexhoma/evaluators/hardware.py`), so this gets real sysbench
     CPU/memory metrics, not just wall-clock timing.
   - `configure_workload()` → no-op, same reasoning as `RefreshStreamBenchmark`:
     must not touch `experiment.args`/`experiment.args_dict`, since YCSB's own
     `configure_workload()` already claims those.
   - `show_summary()` → `self.show_summary_section(experiment)`, exactly like
     `RefreshStreamBenchmark.show_summary()` — required so the generic
     per-benchmark loop doesn't print a full duplicate header/workflow section for
     the secondary benchmark.
   - `show_summary_section()` → pull from
     `self.evaluator.get_summary_benchmark_per_connection()` /
     `get_summary_benchmark_per_phase()` (already narrow, sysbench-only columns)
     instead of the raw timing table `RefreshStreamBenchmark` uses.
   - `test_results()` → no-op initially (or optionally reuse
     `HardwareEvaluator.record_tests()`'s sysbench zero-events check).

2. **`experiments/ycsb.py::enable_noisy_neighbor()`** — new method mirroring
   `enable_refresh_stream()`:
   - Appends one entry to `experiment_dict_template["benchmarker"][0]` with
     `"benchmarker": "sysbench_noisy"`, `"template":
     "jobtemplate-benchmarking-hardware.yml"`, `"fixed_parallelism": True`.
   - Sets `HARDWARE_TYPE=sysbench` (and `HARDWARE_SIZE`/`HARDWARE_DURATION`/
     `HARDWARE_THREADS`) in that entry's own `"parameters"` dict — **not**
     `set_default_benchmarking_parameters()`, since that applies to every entry in
     the round including YCSB's. Needs verifying during implementation that
     per-entry `"parameters"` is merged into that job's env distinctly from
     `defaultParameters`.
   - Calls `self.add_benchmark(NoisyNeighborBenchmark(name='sysbench_noisy'))`.

3. **`experiments/ycsb.py::show_summary()`** — currently doesn't exist (YCSB falls
   through to `MixedExperiment.show_summary()`'s generic loop over
   `self.benchmarks`). Need to check whether that generic loop already calls each
   registered benchmark's `show_summary()` in the right position without further
   changes, or whether a `tpch.py`-style override is needed too — same dual-path
   handling (live-run vs. post-hoc `bexhoma summary`) that `tpch.py:134-161` has.

## Open question to resolve during implementation (not now)

Whether `jobtemplate-benchmarking-hardware.yml` unconditionally mounts a PVC
(`HardwareExperiment` always calls `self.set_experiment(volume='hardware')` for its
own fio/sysbench SUT). A sysbench-only noisy-neighbor pod doesn't need a volume at
all — if the template hard-requires one, either a trimmed template variant or an
empty-but-valid volume claim is needed so `YcsbExperiment` (which never calls
`set_experiment(volume='hardware')`) doesn't break on manifest construction.

## Related background

This plan assumes the fio/sysbench/sockperf/netperf `HardwareEvaluator` narrow-schema
work (each `HARDWARE_TYPE` row only carries its own parameter/result columns, no
cross-type zero-fill) is already in place — see `bexhoma/evaluators/hardware.py`
history. That work is what makes reusing `HardwareEvaluator` here clean: the
noisy-neighbor's sysbench columns won't be polluted with unused fio/sockperf/netperf
columns.
